"""
URL metadata extraction module
Handles extraction of citation metadata from various URL types including arXiv, DOI, and general web pages
"""
import re
import requests
from typing import Dict, Optional, List
from urllib.parse import urlparse, parse_qs
from datetime import datetime


class URLMetadataExtractor:
    """Extract metadata from URLs for citation purposes"""
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def extract(self, url: str) -> Dict[str, any]:
        """Extract metadata from URL"""
        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Handle special URL types
        if 'arxiv.org' in url:
            return self._extract_arxiv(url)
        elif 'doi.org' in url or '/doi/' in url:
            return self._extract_doi(url)
        elif 'pubmed.ncbi.nlm.nih.gov' in url:
            return self._extract_pubmed(url)
        else:
            return self._extract_generic(url)
    
    def _extract_arxiv(self, url: str) -> Dict[str, any]:
        """Extract metadata from arXiv URL"""
        try:
            # Extract arXiv ID from URL
            arxiv_id = None
            if '/abs/' in url:
                arxiv_id = url.split('/abs/')[-1].split('?')[0].split('#')[0]
            elif '/pdf/' in url:
                arxiv_id = url.split('/pdf/')[-1].split('.pdf')[0].split('?')[0]
            elif '/e-print/' in url:
                arxiv_id = url.split('/e-print/')[-1].split('?')[0]
            
            if not arxiv_id:
                # Try to extract from URL path
                parts = urlparse(url).path.split('/')
                for part in parts:
                    if re.match(r'^\d{4}\.\d{4,5}(v\d+)?$', part):
                        arxiv_id = part
                        break
            
            if not arxiv_id:
                return self._create_fallback_entry(url, 'arXiv paper')
            
            # Use arXiv API
            api_url = f'http://export.arxiv.org/api/query?id_list={arxiv_id}'
            response = self.session.get(api_url, timeout=self.timeout)
            
            if response.status_code == 200:
                import xml.etree.ElementTree as ET
                root = ET.fromstring(response.content)
                
                # Parse arXiv XML response
                entry = root.find('{http://www.w3.org/2005/Atom}entry')
                if entry is not None:
                    title_elem = entry.find('{http://www.w3.org/2005/Atom}title')
                    title = title_elem.text.strip() if title_elem is not None and title_elem.text else ''
                    
                    # Remove arXiv title prefix
                    title = re.sub(r'^\[.*?\]\s*', '', title)
                    
                    # Extract authors
                    authors = []
                    for author in entry.findall('{http://www.w3.org/2005/Atom}author'):
                        name_elem = author.find('{http://www.w3.org/2005/Atom}name')
                        if name_elem is not None and name_elem.text:
                            authors.append(name_elem.text.strip())
                    
                    # Extract published date
                    published_elem = entry.find('{http://www.w3.org/2005/Atom}published')
                    year = ''
                    if published_elem is not None and published_elem.text:
                        try:
                            date = datetime.fromisoformat(published_elem.text.replace('Z', '+00:00'))
                            year = str(date.year)
                        except:
                            pass
                    
                    # Extract abstract
                    summary_elem = entry.find('{http://www.w3.org/2005/Atom}summary')
                    abstract = summary_elem.text.strip() if summary_elem is not None and summary_elem.text else ''
                    
                    # Extract primary category
                    primary_category = ''
                    primary_elem = entry.find('{http://arxiv.org/schemas/atom}primary_category')
                    if primary_elem is not None:
                        primary_category = primary_elem.get('term', '')
                    
                    return {
                        'type_of_reference': 'JOUR',
                        'authors': authors,
                        'title': title,
                        'year': year,
                        'journal_name': f'arXiv preprint arXiv:{arxiv_id}',
                        'url': url,
                        'doi': '',
                        'abstract': abstract,
                        'primary_category': primary_category,
                        'arxiv_id': arxiv_id
                    }
            
        except Exception as e:
            print(f"Error extracting arXiv metadata: {e}")
        
        # Fallback: try to extract from PDF metadata or HTML
        return self._extract_generic(url)
    
    def _extract_doi(self, url: str) -> Dict[str, any]:
        """Extract metadata from DOI URL"""
        try:
            # Extract DOI from URL
            doi = None
            if 'doi.org/' in url:
                doi = url.split('doi.org/')[-1].split('?')[0].split('#')[0]
            elif '/doi/' in url:
                doi = url.split('/doi/')[-1].split('?')[0].split('#')[0]
            
            if not doi:
                return self._create_fallback_entry(url, 'DOI document')
            
            # Use CrossRef API
            crossref_url = f'https://api.crossref.org/works/{doi}'
            response = self.session.get(crossref_url, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                if 'message' in data:
                    msg = data['message']
                    
                    # Extract title
                    title = ''
                    if 'title' in msg and msg['title']:
                        title = ' '.join(msg['title'])
                    
                    # Extract authors
                    authors = []
                    if 'author' in msg:
                        for author in msg['author']:
                            given = author.get('given', '')
                            family = author.get('family', '')
                            if family:
                                author_name = f"{family}, {given}".strip(', ')
                                authors.append(author_name)
                    
                    # Extract year
                    year = ''
                    if 'published-print' in msg and msg['published-print'].get('date-parts'):
                        year = str(msg['published-print']['date-parts'][0][0])
                    elif 'published-online' in msg and msg['published-online'].get('date-parts'):
                        year = str(msg['published-online']['date-parts'][0][0])
                    
                    # Extract journal
                    journal = ''
                    if 'container-title' in msg and msg['container-title']:
                        journal = ' '.join(msg['container-title'])
                    
                    # Extract volume and pages
                    volume = str(msg.get('volume', '')) if msg.get('volume') else ''
                    pages = ''
                    if 'page' in msg:
                        pages = str(msg['page'])
                    
                    return {
                        'type_of_reference': 'JOUR',
                        'authors': authors,
                        'title': title,
                        'year': year,
                        'journal_name': journal,
                        'volume': volume,
                        'start_page': pages,
                        'url': url,
                        'doi': doi
                    }
        
        except Exception as e:
            print(f"Error extracting DOI metadata: {e}")
        
        return self._extract_generic(url)
    
    def _extract_pubmed(self, url: str) -> Dict[str, any]:
        """Extract metadata from PubMed URL"""
        try:
            # Extract PubMed ID
            pm_id = None
            if 'pubmed.ncbi.nlm.nih.gov' in url:
                pm_id = url.split('/')[-1].split('?')[0].split('#')[0]
            
            if not pm_id or not pm_id.isdigit():
                return self._create_fallback_entry(url, 'PubMed article')
            
            # Use PubMed API
            api_url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pm_id}&retmode=xml'
            response = self.session.get(api_url, timeout=self.timeout)
            
            if response.status_code == 200:
                import xml.etree.ElementTree as ET
                root = ET.fromstring(response.content)
                
                # Parse PubMed XML
                article = root.find('.//PubmedArticle')
                if article is not None:
                    # Extract title
                    title_elem = article.find('.//ArticleTitle')
                    title = title_elem.text if title_elem is not None and title_elem.text else ''
                    
                    # Extract authors
                    authors = []
                    for author in article.findall('.//Author'):
                        last_name = author.find('LastName')
                        first_name = author.find('ForeName')
                        if last_name is not None and last_name.text:
                            name = last_name.text
                            if first_name is not None and first_name.text:
                                name += f", {first_name.text}"
                            authors.append(name)
                    
                    # Extract year
                    year = ''
                    pub_date = article.find('.//PubDate/Year')
                    if pub_date is not None and pub_date.text:
                        year = pub_date.text
                    
                    # Extract journal
                    journal_elem = article.find('.//Journal/Title')
                    journal = journal_elem.text if journal_elem is not None and journal_elem.text else ''
                    
                    return {
                        'type_of_reference': 'JOUR',
                        'authors': authors,
                        'title': title,
                        'year': year,
                        'journal_name': journal,
                        'url': url,
                        'doi': ''
                    }
        
        except Exception as e:
            print(f"Error extracting PubMed metadata: {e}")
        
        return self._extract_generic(url)
    
    def _extract_generic(self, url: str) -> Dict[str, any]:
        """Extract metadata from generic web page"""
        try:
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            if response.status_code != 200:
                return self._create_fallback_entry(url, 'Web page')
            
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = ''
            if soup.title:
                title = soup.title.string.strip() if soup.title.string else ''
            
            # Try meta tags
            if not title:
                meta_title = soup.find('meta', property='og:title')
                if meta_title and meta_title.get('content'):
                    title = meta_title['content']
            
            if not title:
                meta_title = soup.find('meta', {'name': 'title'})
                if meta_title and meta_title.get('content'):
                    title = meta_title['content']
            
            # Extract authors from meta tags
            authors = []
            author_meta = soup.find_all('meta', {'name': re.compile(r'author', re.I)})
            for meta in author_meta:
                content = meta.get('content', '')
                if content:
                    # Split multiple authors
                    for author in content.split(','):
                        authors.append(author.strip())
            
            # Try to find authors in structured data
            if not authors:
                # Look for JSON-LD structured data
                json_scripts = soup.find_all('script', type='application/ld+json')
                for script in json_scripts:
                    try:
                        import json
                        data = json.loads(script.string)
                        if isinstance(data, dict):
                            if 'author' in data:
                                author_data = data['author']
                                if isinstance(author_data, list):
                                    for auth in author_data:
                                        if isinstance(auth, dict):
                                            name = auth.get('name', '')
                                            if name:
                                                authors.append(name)
                                        elif isinstance(auth, str):
                                            authors.append(auth)
                                elif isinstance(author_data, dict):
                                    name = author_data.get('name', '')
                                    if name:
                                        authors.append(name)
                    except:
                        pass
            
            # Extract date
            year = ''
            date_meta = soup.find('meta', property='article:published_time')
            if date_meta and date_meta.get('content'):
                try:
                    date_str = date_meta['content']
                    date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    year = str(date.year)
                except:
                    pass
            
            if not year:
                date_meta = soup.find('meta', {'name': re.compile(r'date', re.I)})
                if date_meta and date_meta.get('content'):
                    try:
                        date_str = date_meta['content']
                        # Try to parse various date formats
                        for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%d %B %Y', '%B %d, %Y']:
                            try:
                                date = datetime.strptime(date_str[:10], fmt)
                                year = str(date.year)
                                break
                            except:
                                continue
                    except:
                        pass
            
            # Extract description/abstract
            description = ''
            desc_meta = soup.find('meta', property='og:description')
            if desc_meta and desc_meta.get('content'):
                description = desc_meta['content']
            
            if not description:
                desc_meta = soup.find('meta', {'name': 'description'})
                if desc_meta and desc_meta.get('content'):
                    description = desc_meta['content']
            
            return {
                'type_of_reference': 'ELEC',
                'authors': authors if authors else [],
                'title': title if title else url.split('//')[-1].split('/')[0],
                'year': year,
                'journal_name': '',
                'url': url,
                'doi': '',
                'abstract': description
            }
        
        except Exception as e:
            print(f"Error extracting generic metadata: {e}")
            return self._create_fallback_entry(url, 'Web page')
    
    def _create_fallback_entry(self, url: str, source_type: str) -> Dict[str, any]:
        """Create a fallback reference entry when extraction fails"""
        domain = urlparse(url).netloc or url.split('//')[-1].split('/')[0]
        return {
            'type_of_reference': 'ELEC',
            'authors': [],
            'title': f'{source_type} from {domain}',
            'year': '',
            'journal_name': '',
            'url': url,
            'doi': ''
        }
