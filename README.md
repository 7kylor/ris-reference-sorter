# RIS Reference Sorter

A modern Flask web application for managing academic references. Process RIS files, extract citations from URLs (arXiv, DOI, PubMed, and web pages), format references in multiple citation styles, and export in various formats. Features a clean, minimal UI with real-time search and comprehensive reference management.

## Features

### Core Functionality

- **Multiple File Upload**: Upload one or multiple RIS files at once with drag-and-drop support
- **URL-Based Citation Extraction**: Add references directly from URLs:
  - arXiv papers (PDF or abstract pages)
  - DOI links (via CrossRef API)
  - PubMed articles (via E-utilities API)
  - Generic web pages (HTML parsing with metadata extraction)
- **Automatic Sorting**: References sorted alphabetically by first author's last name
- **Duplicate Removal**: Automatically removes duplicate references based on title, authors, and year
- **Merge Collections**: Merge new uploads with existing references or start fresh

### Citation Styles

Support for five major academic citation styles:

- **APA** (American Psychological Association)
- **MLA** (Modern Language Association)
- **Chicago** (Chicago Manual of Style)
- **Harvard** (Harvard Referencing)
- **IEEE** (Institute of Electrical and Electronics Engineers)

Dynamic style switching - change citation style and see all references reformatted instantly.

### Export Options

Export references in multiple formats:

- **Plain Text**: References separated by double line breaks
- **Numbered List**: References with sequential numbering
- **Markdown**: References formatted as markdown list items
- **BibTeX**: Standard BibTeX format for LaTeX
- **RIS**: Research Information Systems format for compatibility

### User Interface

- **Modern, Minimal Design**: Clean, fast, and clutter-free interface
- **Sticky Navigation Bar**: Always-accessible controls with:
  - Statistics display (total references, files processed, duplicates removed)
  - Search functionality (real-time filtering)
- **Compact Layout**: All controls grouped logically next to relevant actions
- **Individual Reference Management**: Copy or delete individual references
- **Bulk Operations**: Copy all references or download entire collection
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Session Management**: Keep references loaded between uploads for easy merging

### Advanced Features

- **Real-time Search**: Filter references instantly as you type
- **Individual Reference Actions**: Copy or delete specific references
- **Statistics Dashboard**: View processing statistics in the navbar
- **Toast Notifications**: User-friendly feedback for all actions
- **Error Handling**: Graceful handling of network errors and missing data
- **Fallback Mechanisms**: Automatic fallback to generic extraction if specialized methods fail

## Supported File Formats

- `.ris` - Research Information Systems format
- `.txt` - Plain text RIS files

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Quick Setup

1. **Clone or download the project**:

   ```bash
   cd ris-reference-sorter-1
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:

   ```bash
   python app.py
   ```

4. **Open your browser** and go to:

   ```text
   http://localhost:5030
   ```

### Alternative Installation with Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### Using the Setup Script

On macOS/Linux, you can use the provided setup script:

```bash
chmod +x setup.sh
./setup.sh
```

## Usage

### Basic Usage

1. **Upload Files**:

   - Drag and drop RIS files onto the upload area, or
   - Click "Browse Files" to select files manually
   - Multiple files can be uploaded simultaneously

2. **Add References from URLs**:

   - Enter a URL in the "Add URL" field (supports arXiv, DOI, PubMed, or any webpage)
   - Click "Add" button
   - The system automatically detects the URL type and extracts metadata
   - Reference is added to your collection

3. **Process References**:

   - Click "Upload & Sort References"
   - The application will parse all RIS files, remove duplicates, and sort alphabetically

4. **Choose Upload Mode**:

   - **Start Fresh**: Replace all current references with new uploads
   - **Merge with Current**: Add new references to existing collection

5. **View Results**:

   - See processing statistics in the navbar (total references, files processed, duplicates removed)
   - Browse the sorted reference list
   - Use the search bar to filter references in real-time

6. **Manage References**:
   - **Change Citation Style**: Select a style from the dropdown to reformat all references
   - **Copy Individual**: Click the copy icon next to any reference
   - **Delete Individual**: Click the delete icon next to any reference
   - **Copy All**: Use the "Copy" button with selected export format
   - **Download**: Use the "Download" button to export in selected format
   - **Clear All**: Remove all references to start over

### URL Examples

- **arXiv**: `https://arxiv.org/pdf/2207.05221` or `https://arxiv.org/abs/2207.05221`
- **DOI**: `https://doi.org/10.1000/xyz` or `https://example.com/doi/10.1000/xyz`
- **PubMed**: `https://pubmed.ncbi.nlm.nih.gov/12345678`
- **Web Page**: Any website URL (extracts title, authors, and metadata from HTML)

### Export Formats

- **Text**: Plain text format, references separated by double line breaks
- **Numbered**: Sequential numbering added to each reference
- **Markdown**: Formatted as markdown list items
- **BibTeX**: Standard BibTeX format for LaTeX documents
- **RIS**: Research Information Systems format for compatibility with other tools

### Example RIS File Format

```ris
TY  - JOUR
AU  - Smith, John
AU  - Doe, Jane
TI  - Sample Research Paper Title
JO  - Journal of Sample Research
VL  - 15
IS  - 3
SP  - 123
EP  - 145
PY  - 2023
DO  - 10.1000/sample.doi
ER  -

TY  - BOOK
AU  - Author, Sample
TI  - Sample Book Title
PB  - Sample Publisher
PY  - 2022
ER  -
```

## API Endpoints

### Web Routes

- `GET /` - Main upload page (redirects to results if references exist)
- `POST /upload` - Process uploaded RIS files
- `POST /clear` - Clear all references from session

### API Routes

- `POST /api/add_url` - Add reference from URL

  ```json
  {
    "url": "https://arxiv.org/pdf/2207.05221",
    "style": "apa"
  }
  ```

- `POST /api/delete_reference` - Delete a specific reference by index

  ```json
  {
    "index": 0
  }
  ```

- `POST /api/change_style` - Change citation style for all references

  ```json
  {
    "style": "mla"
  }
  ```

- `POST /api/export` - Export references in different formats

  ```json
  {
    "reference_data": [...],
    "format": "text|numbered|markdown|bibtex|ris",
    "style": "apa|mla|chicago|harvard|ieee"
  }
  ```

- `GET /current_stats` - Get current statistics (JSON)

## Configuration

The application can be configured by modifying these settings in `app.py`:

```python
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
```

Default port is `5030` (configurable in `app.py`).

## Technical Details

### Dependencies

- **Flask** (3.0.3): Web framework
- **rispy** (0.8.0): RIS file parsing library
- **Werkzeug** (3.0.3): WSGI utilities for security
- **requests** (2.31.0): HTTP library for API calls
- **beautifulsoup4** (4.12.2): HTML parsing for web page metadata
- **lxml** (4.9.3): XML/HTML parser backend

### File Processing

1. Files are read into memory (serverless-compatible)
2. Each RIS file is parsed using the `rispy` library
3. References are stored as dictionaries in Flask session
4. Duplicates are removed based on title, authors, and year
5. References are sorted alphabetically by first author's last name
6. References are formatted on-demand based on selected citation style

### URL Metadata Extraction

The application uses specialized methods for different URL types:

1. **arXiv**: Uses arXiv API (`export.arxiv.org/api/query`) to fetch paper metadata
2. **DOI**: Uses CrossRef API (`api.crossref.org`) to resolve DOI and fetch metadata
3. **PubMed**: Uses PubMed E-utilities API to fetch article information
4. **Generic Web Pages**: Parses HTML with BeautifulSoup, extracts metadata from:
   - `<title>` tags
   - Open Graph meta tags
   - Structured data (JSON-LD, microdata)
   - Meta tags for authors and publication dates

All extraction methods include fallback mechanisms for error handling.

### Citation Formatting

References are formatted according to the selected citation style using the `CitationFormatter` class. Each style follows its respective formatting guidelines:

- **APA**: Author, A. A., & Author, B. B. (Year). Title. _Journal_, Volume(Issue), Pages. DOI
- **MLA**: Author, First Name, and Second Author. "Title." _Journal_, vol. Volume, no. Issue, Year, pp. Pages.
- **Chicago**: Author, First Name, and Second Author. "Title." _Journal_ Volume, no. Issue (Year): Pages.
- **Harvard**: Author, F. and Author, S. (Year) 'Title', _Journal_, Volume(Issue), pp. Pages.
- **IEEE**: A. Author and B. Author, "Title," _Journal_, vol. Volume, no. Issue, pp. Pages, Year.

### Architecture

- **Backend**: Flask application with session-based storage
- **Frontend**: Jinja2 templates with vanilla JavaScript (no frameworks)
- **Styling**: Custom CSS with CSS variables (no Bootstrap or external CSS frameworks)
- **Icons**: Inline SVG icons (no icon libraries)
- **State Management**: Flask sessions for reference storage

## Troubleshooting

### Common Issues

1. **File Upload Fails**:

   - Check file format (.ris or .txt)
   - Ensure file size is under 16MB
   - Verify the file contains valid RIS format data

2. **No References Found**:

   - Verify the RIS file format is correct
   - Check that the file contains proper RIS tags (TY, AU, TI, etc.)

3. **URL Extraction Fails**:

   - Check your internet connection
   - Verify the URL is accessible
   - Some websites may block automated access
   - Try the URL in a browser first to ensure it's valid

4. **Encoding Issues**:

   - The application tries UTF-8 first, then falls back to Latin-1 encoding
   - If issues persist, try converting your file to UTF-8 encoding

5. **API Rate Limiting**:
   - CrossRef and PubMed APIs may have rate limits
   - If you encounter rate limiting, wait a few moments and try again

### Debug Mode

To run in debug mode for development:

```python
app.run(debug=True, host='0.0.0.0', port=5030)
```

## Project Structure

```text
ris-reference-sorter-1/
├── app.py                 # Main Flask application
├── citation_formatter.py  # Citation style formatting module
├── url_metadata.py        # URL metadata extraction module
├── requirements.txt       # Python dependencies
├── setup.sh              # Setup script
├── templates/
│   ├── base.html         # Base template with navbar
│   ├── index.html        # Upload page
│   └── results.html      # Results page with reference list
├── README.md             # This file
├── URL_METADATA.md       # URL metadata extraction documentation
└── TESTING.md            # Testing documentation
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For support or questions:

- Check the troubleshooting section above
- Review the RIS file format requirements
- Ensure all dependencies are properly installed
- See `URL_METADATA.md` for URL extraction details

## Changelog

### Version 2.0.0 (Current)

- **Major UI/UX Overhaul**: Complete redesign with minimal, clean interface
- **URL Metadata Extraction**: Support for arXiv, DOI, PubMed, and generic web pages
- **Multiple Citation Styles**: Added APA, MLA, Chicago, Harvard, and IEEE formatting
- **Dynamic Style Switching**: Change citation style and see instant reformatting
- **Search Functionality**: Real-time filtering of references
- **Individual Reference Management**: Copy and delete individual references
- **Enhanced Export Formats**: Added BibTeX and RIS export options
- **Improved Navigation**: Sticky navbar with statistics and search
- **Better Error Handling**: Comprehensive error handling and fallback mechanisms
- **Session Management**: Improved reference storage and management

### Version 1.0.0

- Initial release
- Multi-file RIS upload support
- Automatic sorting and duplicate removal
- Multiple export formats (Text, Numbered, Markdown)
- Responsive web interface
- Copy to clipboard functionality
