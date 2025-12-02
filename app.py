#!/usr/bin/env python3
"""
RIS Reference Sorter Flask Application
Imports RIS files, sorts references, and allows copying of sorted results
"""

import os
import io
import json
from typing import Dict, List, Union
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session
from werkzeug.utils import secure_filename
import rispy

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

ALLOWED_EXTENSIONS = {'ris', 'txt'}

def allowed_file(filename: str) -> bool:
    """Check if file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def format_reference(entry: Dict[str, Union[str, List[str], int]]) -> str:
    """Convert RIS entry to formatted citation"""
    try:
        # Extract key fields
        authors = entry.get('authors', [])
        title = entry.get('title', '')
        journal = entry.get('journal_name', '') or entry.get('secondary_title', '')
        year = entry.get('year', '')
        volume = entry.get('volume', '')
        issue = entry.get('number', '')
        pages = entry.get('start_page', '')
        end_page = entry.get('end_page', '')
        doi = entry.get('doi', '')
        url = entry.get('url', '')
        
        # Format authors
        if authors:
            if len(authors) == 1:
                author_str = authors[0]
            elif len(authors) <= 3:
                author_str = ', '.join(authors[:-1]) + ', & ' + authors[-1]
            else:
                author_str = ', '.join(authors[:3]) + ', et al.'
        else:
            author_str = 'Unknown Author'
        
        # Build citation
        citation = f"{author_str}"
        
        if year:
            citation += f" ({year})"
        
        if title:
            citation += f". {title}"
        
        if journal:
            citation += f". {journal}"
            
            if volume:
                citation += f", {volume}"
                if issue:
                    citation += f"({issue})"
            
            if pages:
                if end_page:
                    citation += f", {pages}-{end_page}"
                else:
                    citation += f", {pages}"
        
        if doi:
            citation += f". https://doi.org/{doi}"
        elif url:
            citation += f". {url}"
        
        citation += "."
        
        return citation.replace("..", ".")
        
    except Exception as e:
        # Fallback formatting
        return f"Error formatting reference: {str(e)}"

def get_sort_key(citation: str) -> str:
    """Extract first author's last name for sorting"""
    try:
        # Split by comma to get first author
        first_part = citation.split(',')[0].strip()
        # Extract last name (first word before comma)
        if ' ' in first_part:
            return first_part.split()[0]
        return first_part
    except:
        return citation[:20]  # Fallback

def parse_ris_file(file_content: bytes, encoding: str = 'utf-8') -> list[str]:
    """Parse RIS file content and return list of references"""
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
            formatted_ref = format_reference(entry)
            if formatted_ref and formatted_ref.strip():
                references.append(formatted_ref)
                
    except UnicodeDecodeError:
        # Try different encodings
        if encoding != 'latin-1':
            try:
                text_content = file_content.decode('latin-1') if isinstance(file_content, bytes) else file_content
                file_like = io.StringIO(text_content)
                entries = rispy.load(file_like)
                
                for entry in entries:
                    formatted_ref = format_reference(entry)
                    if formatted_ref and formatted_ref.strip():
                        references.append(formatted_ref)
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
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    """Handle file upload and process RIS files"""
    # Get current references from session
    current_references = session.get('references', [])
    
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
                
                # Parse the RIS file from memory
                references = parse_ris_file(file_content)
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
    
    # Remove duplicates
    unique_refs = list(dict.fromkeys(all_references))
    
    # Sort references alphabetically by first author
    sorted_refs = sorted(unique_refs, key=lambda x: get_sort_key(x).lower())
    
    # Update session storage
    session['references'] = sorted_refs
    
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
        'existing_references_count': len(current_references) - len(new_references) if merge_mode else 0
    }
    
    return render_template('results.html', references=sorted_refs, stats=stats)

@app.route('/clear', methods=['POST'])
def clear_references():
    """Clear all current references"""
    session.pop('references', None)
    flash('All references cleared successfully')
    return redirect(url_for('index'))

@app.route('/current_stats')
def current_stats():
    """Get current reference statistics"""
    current_references = session.get('references', [])
    return jsonify({
        'count': len(current_references),
        'has_references': len(current_references) > 0
    })

@app.route('/api/export', methods=['POST'])
def export_references():
    """API endpoint to export references in different formats"""
    data = request.get_json()
    references = data.get('references', [])
    format_type = data.get('format', 'text')
    
    if format_type == 'text':
        # Plain text format with double newlines
        exported = '\n\n'.join(references)
    elif format_type == 'numbered':
        # Numbered list
        exported = '\n\n'.join(f"{i+1}. {ref}" for i, ref in enumerate(references))
    elif format_type == 'markdown':
        # Markdown format
        exported = '\n\n'.join(f"- {ref}" for ref in references)
    else:
        exported = '\n\n'.join(references)
    
    return jsonify({'exported_text': exported})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5030) 