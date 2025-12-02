"""
Citation formatter module supporting multiple citation styles
Supports: APA, MLA, Chicago, Harvard, IEEE
"""
from typing import Dict, List, Union, Optional
from enum import Enum


class CitationStyle(Enum):
    """Supported citation styles"""
    APA = "apa"
    MLA = "mla"
    CHICAGO = "chicago"
    HARVARD = "harvard"
    IEEE = "ieee"


class CitationFormatter:
    """Formats RIS entries according to different citation styles"""
    
    @staticmethod
    def format_authors(authors: List[str], style: CitationStyle) -> str:
        """Format author list according to citation style"""
        if not authors:
            return "Unknown Author"
        
        if style == CitationStyle.APA:
            if len(authors) == 1:
                return authors[0]
            elif len(authors) <= 7:
                if len(authors) == 2:
                    return f"{authors[0]}, & {authors[1]}"
                else:
                    return ', '.join(authors[:-1]) + ', & ' + authors[-1]
            else:
                return ', '.join(authors[:6]) + ', ... ' + authors[-1]
        
        elif style == CitationStyle.MLA:
            if len(authors) == 1:
                return authors[0]
            elif len(authors) == 2:
                return f"{authors[0]} and {authors[1]}"
            else:
                return ', '.join(authors[:-1]) + ', and ' + authors[-1]
        
        elif style == CitationStyle.CHICAGO:
            if len(authors) == 1:
                return authors[0]
            elif len(authors) <= 10:
                if len(authors) == 2:
                    return f"{authors[0]} and {authors[1]}"
                else:
                    return ', '.join(authors[:-1]) + ', and ' + authors[-1]
            else:
                return ', '.join(authors[:10]) + ', et al.'
        
        elif style == CitationStyle.HARVARD:
            if len(authors) == 1:
                return authors[0]
            elif len(authors) <= 3:
                return ', '.join(authors[:-1]) + ' & ' + authors[-1]
            else:
                return authors[0] + ' et al.'
        
        elif style == CitationStyle.IEEE:
            if len(authors) == 1:
                return authors[0]
            elif len(authors) <= 6:
                return ', '.join(authors)
            else:
                return ', '.join(authors[:6]) + ' et al.'
        
        return ', '.join(authors)
    
    @staticmethod
    def format_apa(entry: Dict[str, Union[str, List[str], int]]) -> str:
        """Format citation in APA 7th edition style"""
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
        entry_type = entry.get('type_of_reference', 'JOUR')
        
        author_str = CitationFormatter.format_authors(authors, CitationStyle.APA)
        
        if entry_type == 'JOUR':
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
        
        elif entry_type == 'BOOK':
            publisher = entry.get('publisher', '')
            city = entry.get('place_published', '')
            citation = f"{author_str}"
            if year:
                citation += f" ({year})"
            if title:
                citation += f". {title}"
            if city and publisher:
                citation += f". {publisher}"
            elif publisher:
                citation += f". {publisher}"
            citation += "."
        
        else:
            citation = f"{author_str}"
            if year:
                citation += f" ({year})"
            if title:
                citation += f". {title}"
            if journal:
                citation += f". {journal}"
            if doi:
                citation += f". https://doi.org/{doi}"
            elif url:
                citation += f". {url}"
            citation += "."
        
        return citation.replace("..", ".").strip()
    
    @staticmethod
    def format_mla(entry: Dict[str, Union[str, List[str], int]]) -> str:
        """Format citation in MLA 9th edition style"""
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
        
        author_str = CitationFormatter.format_authors(authors, CitationStyle.MLA)
        
        citation = f"{author_str}"
        if title:
            citation += f'. "{title}"'
        if journal:
            citation += f". {journal}"
            if volume and issue:
                citation += f", vol. {volume}, no. {issue}"
            elif volume:
                citation += f", vol. {volume}"
            if year:
                citation += f", {year}"
            if pages:
                if end_page:
                    citation += f", pp. {pages}-{end_page}"
                else:
                    citation += f", p. {pages}"
        elif year:
            citation += f". {year}"
        if doi:
            citation += f", https://doi.org/{doi}"
        elif url:
            citation += f", {url}"
        citation += "."
        
        return citation.replace("..", ".").strip()
    
    @staticmethod
    def format_chicago(entry: Dict[str, Union[str, List[str], int]]) -> str:
        """Format citation in Chicago 17th edition style"""
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
        
        author_str = CitationFormatter.format_authors(authors, CitationStyle.CHICAGO)
        
        citation = f"{author_str}"
        if title:
            citation += f'. "{title}"'
        if journal:
            citation += f". {journal}"
            if volume and issue:
                citation += f" {volume}, no. {issue}"
            elif volume:
                citation += f" {volume}"
            if year:
                citation += f" ({year})"
            if pages:
                if end_page:
                    citation += f": {pages}-{end_page}"
                else:
                    citation += f": {pages}"
        elif year:
            citation += f". {year}"
        if doi:
            citation += f". https://doi.org/{doi}"
        elif url:
            citation += f". {url}"
        citation += "."
        
        return citation.replace("..", ".").strip()
    
    @staticmethod
    def format_harvard(entry: Dict[str, Union[str, List[str], int]]) -> str:
        """Format citation in Harvard style"""
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
        
        author_str = CitationFormatter.format_authors(authors, CitationStyle.HARVARD)
        
        citation = f"{author_str}"
        if year:
            citation += f" {year}"
        if title:
            citation += f", {title}"
        if journal:
            citation += f", {journal}"
            if volume:
                citation += f", {volume}"
                if issue:
                    citation += f"({issue})"
            if pages:
                if end_page:
                    citation += f", pp.{pages}-{end_page}"
                else:
                    citation += f", p.{pages}"
        if doi:
            citation += f", DOI: {doi}"
        elif url:
            citation += f", Available at: {url}"
        citation += "."
        
        return citation.replace("..", ".").strip()
    
    @staticmethod
    def format_ieee(entry: Dict[str, Union[str, List[str], int]]) -> str:
        """Format citation in IEEE style"""
        authors = entry.get('authors', [])
        title = entry.get('title', '')
        journal = entry.get('journal_name', '') or entry.get('secondary_title', '')
        year = entry.get('year', '')
        volume = entry.get('volume', '')
        issue = entry.get('number', '')
        pages = entry.get('start_page', '')
        end_page = entry.get('end_page', '')
        doi = entry.get('doi', '')
        
        author_str = CitationFormatter.format_authors(authors, CitationStyle.IEEE)
        
        citation = f"{author_str}"
        if title:
            citation += f', "{title}"'
        if journal:
            citation += f", {journal}"
            if volume:
                citation += f", vol. {volume}"
                if issue:
                    citation += f", no. {issue}"
            if pages:
                if end_page:
                    citation += f", pp. {pages}-{end_page}"
                else:
                    citation += f", pp. {pages}"
            if year:
                citation += f", {year}"
        elif year:
            citation += f", {year}"
        if doi:
            citation += f", doi: {doi}"
        citation += "."
        
        return citation.replace("..", ".").strip()
    
    @staticmethod
    def format(entry: Dict[str, Union[str, List[str], int]], style: CitationStyle = CitationStyle.APA) -> str:
        """Format citation according to specified style"""
        try:
            if style == CitationStyle.APA:
                return CitationFormatter.format_apa(entry)
            elif style == CitationStyle.MLA:
                return CitationFormatter.format_mla(entry)
            elif style == CitationStyle.CHICAGO:
                return CitationFormatter.format_chicago(entry)
            elif style == CitationStyle.HARVARD:
                return CitationFormatter.format_harvard(entry)
            elif style == CitationStyle.IEEE:
                return CitationFormatter.format_ieee(entry)
            else:
                return CitationFormatter.format_apa(entry)
        except Exception as e:
            return f"Error formatting reference: {str(e)}"
