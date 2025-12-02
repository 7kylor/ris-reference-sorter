#!/usr/bin/env python3
"""
RIS Reference Sorter Flask Application
Imports RIS files, sorts references, and allows copying of sorted results

Last Updated: December 2, 2025
Python Version: 3.14+
"""

import os
import io
import json
from typing import Dict, List, Union, Optional
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session
from werkzeug.utils import secure_filename
import rispy
from citation_formatter import CitationFormatter, CitationStyle
from url_metadata import URLMetadataExtractor

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

ALLOWED_EXTENSIONS = {'ris', 'txt'}

def allowed_file(filename: str) -> bool:
    """Check if file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def format_reference(entry: Dict[str, Union[str, List[str], int]], style: CitationStyle = CitationStyle.APA) -> str:
    """Convert RIS entry to formatted citation using specified style"""
    return CitationFormatter.format(entry, style)


def parse_ris_file(file_content: bytes, encoding: str = 'utf-8', style: CitationStyle = CitationStyle.APA) -> List[Dict]:
    """Parse RIS file content and return list of reference dictionaries"""
    references = []
    
    try:
        # Decode file content
        if isinstance(file_content, bytes):
            text_content = file_content.decode(encoding)
        else:
            text_content = file_content
            
        # Create StringIO object for rispy
        file_like = io.StringIO(text_content)
        entries = rispy.load(file_like)
            
        for entry in entries:
            references.append(entry)
                
    except UnicodeDecodeError:
        # Try different encodings
        if encoding != 'latin-1':
            try:
                text_content = file_content.decode('latin-1') if isinstance(file_content, bytes) else file_content
                file_like = io.StringIO(text_content)
                entries = rispy.load(file_like)
                
                for entry in entries:
                    references.append(entry)
            except Exception as e:
                raise Exception(f"Could not parse RIS file: {str(e)}")
        else:
            raise Exception(f"Could not parse RIS file: encoding error")
    except Exception as e:
        raise Exception(f"Error parsing RIS file: {str(e)}")
    
    return references

@app.route('/')
def index():
    """Main page with file upload form"""
    current_style = session.get('citation_style', 'apa')
    current_references = session.get('references', [])
    
    # If there are references, show them
    if current_references:
        try:
            style = CitationStyle(current_style.lower())
        except ValueError:
            style = CitationStyle.APA
        
        formatted_refs = [format_reference(ref, style) for ref in current_references]
        
        stats = {
            'total_files': 0,
            'total_references': len(current_references),
            'unique_references': len(current_references),
            'duplicates_removed': 0,
            'processed_files': [],
            'errors': [],
            'operation_mode': 'existing',
            'new_references_count': 0,
            'existing_references_count': len(current_references),
            'citation_style': current_style
        }
        
        return render_template('results.html', 
                             references=formatted_refs, 
                             reference_data=current_references, 
                             stats=stats, 
                             citation_style=current_style)
    
    return render_template('index.html', citation_style=current_style)

@app.route('/upload', methods=['POST'])
def upload_files():
    """Handle file upload and process RIS files"""
    # Get current references from session (stored as dicts)
    current_references = session.get('references', [])
    
    # Get citation style
    style_str = request.form.get('citation_style', session.get('citation_style', 'apa'))
    try:
        style = CitationStyle(style_str.lower())
    except ValueError:
        style = CitationStyle.APA
    
    session['citation_style'] = style.value
    
    if 'files' not in request.files:
        flash('No files selected')
        return redirect(url_for('index'))
    
    files = request.files.getlist('files')
    merge_mode = request.form.get('merge_mode', 'new') == 'merge'
    
    if not files or all(file.filename == '' for file in files):
        flash('No files selected')
        return redirect(url_for('index'))
    
    new_references = []
    processed_files = []
    errors = []
    
    # Process each uploaded file (in-memory for serverless compatibility)
    for file in files:
        if file and file.filename and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                
                # Read file content into memory
                file_content = file.read()
                
                # Parse the RIS file from memory (returns list of dicts)
                references = parse_ris_file(file_content, style=style)
                new_references.extend(references)
                processed_files.append(filename)
                
            except Exception as e:
                errors.append(f"Error processing {file.filename}: {str(e)}")
        else:
            errors.append(f"Invalid file type: {file.filename}. Only .ris and .txt files are allowed.")
    
    if not new_references:
        flash('No valid references found in uploaded files')
        return redirect(url_for('index'))
    
    # Handle merge or new mode
    if merge_mode and current_references:
        # Merge with existing references
        all_references = current_references + new_references
        operation_mode = "merged"
    else:
        # Start fresh with new references
        all_references = new_references
        operation_mode = "new"
    
    # Remove duplicates based on a unique identifier (title + authors + year)
    seen = set()
    unique_refs = []
    for ref in all_references:
        authors = tuple(ref.get('authors', []))
        title = ref.get('title', '')
        year = ref.get('year', '')
        key = (title.lower(), tuple(authors), str(year))
        if key not in seen:
            seen.add(key)
            unique_refs.append(ref)
    
    # Sort references alphabetically by first author
    def get_ref_sort_key(ref: Dict) -> str:
        authors = ref.get('authors', [])
        if authors:
            return authors[0].split(',')[0].strip().lower()
        return ref.get('title', '').lower()
    
    sorted_refs = sorted(unique_refs, key=get_ref_sort_key)
    
    # Update session storage (store as dicts, not formatted strings)
    session['references'] = sorted_refs
    
    # Format references for display
    formatted_refs = [format_reference(ref, style) for ref in sorted_refs]
    
    # Statistics
    stats = {
        'total_files': len(processed_files),
        'total_references': len(all_references),
        'unique_references': len(unique_refs),
        'duplicates_removed': len(all_references) - len(unique_refs),
        'processed_files': processed_files,
        'errors': errors,
        'operation_mode': operation_mode,
        'new_references_count': len(new_references),
        'existing_references_count': len(current_references) - len(new_references) if merge_mode else 0,
        'citation_style': style.value
    }
    
    return render_template('results.html', references=formatted_refs, reference_data=sorted_refs, stats=stats, citation_style=style.value)

@app.route('/api/add_url', methods=['POST'])
def add_url_citation():
    """Add citation from URL with full metadata extraction"""
    data = request.get_json()
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    # Basic URL validation
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    style_str = data.get('style', session.get('citation_style', 'apa'))
    try:
        style = CitationStyle(style_str.lower())
    except ValueError:
        style = CitationStyle.APA
    
    # Extract metadata from URL
    extractor = URLMetadataExtractor()
    try:
        reference_entry = extractor.extract(url)
    except Exception as e:
        # Fallback if extraction fails
        reference_entry = {
            'type_of_reference': 'ELEC',
            'authors': [],
            'title': url.split('//')[-1].split('/')[0] if '//' in url else url,
            'url': url,
            'year': '',
            'journal_name': '',
            'doi': ''
        }
    
    # Ensure URL is set
    reference_entry['url'] = url
    
    # Get current references
    current_references = session.get('references', [])
    current_references.append(reference_entry)
    
    # Remove duplicates
    seen = set()
    unique_refs = []
    for ref in current_references:
        authors = tuple(ref.get('authors', []))
        title = ref.get('title', '')
        year = ref.get('year', '')
        url_ref = ref.get('url', '')
        # Use URL as part of key to avoid duplicates from same URL
        key = (title.lower(), tuple(authors), str(year), url_ref.lower())
        if key not in seen:
            seen.add(key)
            unique_refs.append(ref)
    
    # Sort
    def get_ref_sort_key(ref: Dict) -> str:
        authors = ref.get('authors', [])
        if authors:
            return authors[0].split(',')[0].strip().lower()
        return ref.get('title', '').lower()
    
    sorted_refs = sorted(unique_refs, key=get_ref_sort_key)
    session['references'] = sorted_refs
    
    formatted_ref = format_reference(reference_entry, style)
    
    return jsonify({
        'success': True,
        'reference': formatted_ref,
        'total_count': len(sorted_refs),
        'metadata': {
            'title': reference_entry.get('title', ''),
            'authors': reference_entry.get('authors', []),
            'year': reference_entry.get('year', ''),
            'source': reference_entry.get('journal_name', '') or reference_entry.get('type_of_reference', '')
        }
    })

@app.route('/api/delete_reference', methods=['POST'])
def delete_reference():
    """Delete a single reference by index"""
    data = request.get_json()
    index = data.get('index')
    
    if index is None:
        return jsonify({'error': 'Index is required'}), 400
    
    current_references = session.get('references', [])
    
    if 0 <= index < len(current_references):
        current_references.pop(index)
        session['references'] = current_references
        
        # Reformat references for response
        style_str = session.get('citation_style', 'apa')
        try:
            style = CitationStyle(style_str.lower())
        except ValueError:
            style = CitationStyle.APA
        
        formatted_refs = [format_reference(ref, style) for ref in current_references]
        
        return jsonify({
            'success': True,
            'references': formatted_refs,
            'total_count': len(current_references)
        })
    else:
        return jsonify({'error': 'Invalid index'}), 400

@app.route('/clear', methods=['POST'])
def clear_references():
    """Clear all current references"""
    session.pop('references', None)
    session.pop('citation_style', None)
    flash('All references cleared successfully')
    return redirect(url_for('index'))

@app.route('/current_stats')
def current_stats():
    """Get current reference statistics"""
    current_references = session.get('references', [])
    style = session.get('citation_style', 'apa')
    return jsonify({
        'count': len(current_references),
        'has_references': len(current_references) > 0,
        'style': style
    })

@app.route('/api/export', methods=['POST'])
def export_references():
    """API endpoint to export references in different formats"""
    data = request.get_json()
    reference_data = data.get('reference_data', [])
    format_type = data.get('format', 'text')
    style_str = data.get('style', session.get('citation_style', 'apa'))
    
    try:
        style = CitationStyle(style_str.lower())
    except ValueError:
        style = CitationStyle.APA
    
    # Format references according to style
    formatted_refs = [format_reference(ref, style) for ref in reference_data]
    
    if format_type == 'text':
        # Plain text format with double newlines
        exported = '\n\n'.join(formatted_refs)
    elif format_type == 'numbered':
        # Numbered list
        exported = '\n\n'.join(f"{i+1}. {ref}" for i, ref in enumerate(formatted_refs))
    elif format_type == 'markdown':
        # Markdown format
        exported = '\n\n'.join(f"- {ref}" for ref in formatted_refs)
    elif format_type == 'bibtex':
        # BibTeX format
        exported = export_bibtex(reference_data)
    elif format_type == 'ris':
        # RIS format
        exported = export_ris(reference_data)
    else:
        exported = '\n\n'.join(formatted_refs)
    
    return jsonify({'exported_text': exported})

@app.route('/api/change_style', methods=['POST'])
def change_style():
    """Change citation style and reformat references"""
    data = request.get_json()
    style_str = data.get('style', 'apa')
    
    try:
        style = CitationStyle(style_str.lower())
    except ValueError:
        style = CitationStyle.APA
    
    session['citation_style'] = style.value
    
    # Get current references from session
    current_references = session.get('references', [])
    
    # Reformat all references
    formatted_refs = [format_reference(ref, style) for ref in current_references]
    
    return jsonify({
        'success': True,
        'references': formatted_refs,
        'style': style.value
    })

def export_bibtex(references: List[Dict]) -> str:
    """Export references in BibTeX format"""
    bibtex_entries = []
    
    for i, ref in enumerate(references):
        entry_type_map = {
            'JOUR': 'article',
            'BOOK': 'book',
            'CHAP': 'incollection',
            'CONF': 'inproceedings',
            'THES': 'phdthesis',
            'RPRT': 'techreport'
        }
        
        ref_type = ref.get('type_of_reference', 'JOUR')
        bibtex_type = entry_type_map.get(ref_type, 'misc')
        
        authors = ref.get('authors', [])
        title = ref.get('title', '')
        journal = ref.get('journal_name', '') or ref.get('secondary_title', '')
        year = ref.get('year', '')
        volume = ref.get('volume', '')
        pages = ref.get('start_page', '')
        doi = ref.get('doi', '')
        
        entry = f"@{{{bibtex_type.lower()}}}{{{i+1:04d}"
        if authors:
            entry += f",\n  author = {{{' and '.join(authors)}}}"
        if title:
            entry += f",\n  title = {{{title}}}"
        if journal:
            entry += f",\n  journal = {{{journal}}}"
        if year:
            entry += f",\n  year = {{{year}}}"
        if volume:
            entry += f",\n  volume = {{{volume}}}"
        if pages:
            entry += f",\n  pages = {{{pages}}}"
        if doi:
            entry += f",\n  doi = {{{doi}}}"
        entry += "\n}"
        
        bibtex_entries.append(entry)
    
    return '\n\n'.join(bibtex_entries)

def export_ris(references: List[Dict]) -> str:
    """Export references in RIS format"""
    ris_entries = []
    
    for ref in references:
        entry = []
        ref_type = ref.get('type_of_reference', 'JOUR')
        entry.append(f"TY  - {ref_type}")
        
        authors = ref.get('authors', [])
        for author in authors:
            entry.append(f"AU  - {author}")
        
        title = ref.get('title', '')
        if title:
            entry.append(f"TI  - {title}")
        
        journal = ref.get('journal_name', '') or ref.get('secondary_title', '')
        if journal:
            entry.append(f"JO  - {journal}")
        
        year = ref.get('year', '')
        if year:
            entry.append(f"PY  - {year}")
        
        volume = ref.get('volume', '')
        if volume:
            entry.append(f"VL  - {volume}")
        
        issue = ref.get('number', '')
        if issue:
            entry.append(f"IS  - {issue}")
        
        pages = ref.get('start_page', '')
        if pages:
            entry.append(f"SP  - {pages}")
        
        end_page = ref.get('end_page', '')
        if end_page:
            entry.append(f"EP  - {end_page}")
        
        doi = ref.get('doi', '')
        if doi:
            entry.append(f"DO  - {doi}")
        
        url = ref.get('url', '')
        if url:
            entry.append(f"UR  - {url}")
        
        entry.append("ER  - ")
        ris_entries.append('\n'.join(entry))
    
    return '\n\n'.join(ris_entries)

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/terms')
def terms():
    """Terms of Service page"""
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    """Privacy Policy page"""
    return render_template('privacy.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5030) 