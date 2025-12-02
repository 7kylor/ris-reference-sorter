# RIS Reference Sorter

A modern, open-source Flask web application for managing academic references. Process RIS files, extract citations from URLs (arXiv, DOI, PubMed, and web pages), format references in multiple citation styles, and export in various formats. Features a clean, minimal UI with real-time search and comprehensive reference management.

**Version**: 2.1.0  
**Last Updated**: December 2, 2025  
**License**: MIT License (Free and Open Source)  
**Python Version**: 3.14+

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
- [API Documentation](#api-documentation)
- [Architecture](#architecture)
- [Development](#development)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## Overview

RIS Reference Sorter is a comprehensive web-based tool designed for researchers, students, and academics who need to manage, organize, and format academic references. The application supports multiple input methods, citation styles, and export formats, making it a versatile solution for reference management.

### Key Highlights

- **Free and Open Source**: MIT License - use, modify, and distribute freely
- **No Database Required**: Session-based storage, perfect for serverless deployment
- **Multiple Citation Styles**: APA, MLA, Chicago, Harvard, and IEEE
- **URL Citation Extraction**: Automatic metadata extraction from arXiv, DOI, PubMed, and web pages
- **Modern UI**: Clean, responsive design with real-time search and filtering
- **Export Flexibility**: Multiple export formats including BibTeX and RIS

## Features

### Core Functionality

#### File Upload and Processing

- **Multiple File Upload**: Upload one or multiple RIS files simultaneously with drag-and-drop support
- **File Format Support**: Supports `.ris` and `.txt` files containing RIS-formatted data
- **Automatic Parsing**: Intelligent RIS file parsing with encoding detection (UTF-8, Latin-1)
- **Duplicate Detection**: Automatically identifies and removes duplicate references based on title, authors, and year
- **Alphabetical Sorting**: References sorted automatically by first author's last name
- **Merge Capabilities**: Merge new uploads with existing references or start fresh

#### URL-Based Citation Extraction

- **arXiv Support**: Extract citations from arXiv papers (PDF or abstract pages)
  - Uses arXiv API for reliable metadata extraction
  - Handles both `/abs/` and `/pdf/` URLs
  - Extracts title, authors, publication year, abstract, and category
- **DOI Support**: Extract citations from DOI links via CrossRef API
  - Automatic DOI resolution
  - Extracts journal information, volume, pages, and publication details
- **PubMed Support**: Extract citations from PubMed articles
  - Uses PubMed E-utilities API
  - Extracts article metadata including authors, journal, and publication year
- **Generic Web Pages**: Extract citations from any webpage
  - HTML parsing with BeautifulSoup
  - Extracts metadata from Open Graph tags, structured data (JSON-LD), and meta tags
  - Fallback mechanisms for missing data

#### Citation Style Formatting

Support for five major academic citation styles with dynamic switching:

- **APA (7th Edition)**: American Psychological Association style
  - Format: Author, A. A., & Author, B. B. (Year). Title. _Journal_, Volume(Issue), Pages. DOI
- **MLA (9th Edition)**: Modern Language Association style
  - Format: Author, First Name, and Second Author. "Title." _Journal_, vol. Volume, no. Issue, Year, pp. Pages.
- **Chicago (17th Edition)**: Chicago Manual of Style
  - Format: Author, First Name, and Second Author. "Title." _Journal_ Volume, no. Issue (Year): Pages.
- **Harvard**: Harvard Referencing style
  - Format: Author, F. and Author, S. (Year) 'Title', _Journal_, Volume(Issue), pp. Pages.
- **IEEE**: Institute of Electrical and Electronics Engineers style
  - Format: A. Author and B. Author, "Title," _Journal_, vol. Volume, no. Issue, pp. Pages, Year.

**Dynamic Style Switching**: Change citation style and see all references reformatted instantly without re-uploading.

#### Export Options

Export references in multiple formats:

- **Plain Text**: References separated by double line breaks
- **Numbered List**: References with sequential numbering (1., 2., 3., ...)
- **Markdown**: References formatted as markdown list items
- **BibTeX**: Standard BibTeX format for LaTeX documents
- **RIS**: Research Information Systems format for compatibility with other reference managers

#### User Interface Features

- **Modern, Minimal Design**: Clean, fast, and clutter-free interface
- **Sticky Navigation Bar**: Always-accessible controls with:
  - Statistics display (total references, files processed, duplicates removed)
  - Real-time search functionality
  - Quick actions (clear, export)
- **Compact Layout**: All controls grouped logically next to relevant actions
- **Individual Reference Management**:
  - Copy individual references to clipboard
  - Delete individual references
- **Bulk Operations**:
  - Copy all references in selected format
  - Download entire collection
  - Clear all references
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Session Management**: Keep references loaded between uploads for easy merging
- **Real-time Search**: Filter references instantly as you type
- **Toast Notifications**: User-friendly feedback for all actions
- **Error Handling**: Graceful handling of network errors and missing data

### Advanced Features

- **Fallback Mechanisms**: Automatic fallback to generic extraction if specialized methods fail
- **Encoding Detection**: Automatic detection and handling of different file encodings
- **Error Recovery**: Comprehensive error handling with user-friendly messages
- **API Rate Limiting**: Handles API rate limits gracefully
- **Serverless Compatible**: Designed for serverless deployment (Vercel, AWS Lambda, etc.)

## Installation

### Prerequisites

- **Python 3.14 or higher** (required)
- **pip** (Python package installer)
- **Internet connection** (for URL metadata extraction)

### Quick Setup

1. **Clone or download the project**:

   ```bash
   git clone <repository-url>
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

4. **Open your browser** and navigate to:

   ```
   http://localhost:5030
   ```

### Alternative Installation with Virtual Environment

Using a virtual environment is recommended for isolation:

```bash
# Create virtual environment (requires Python 3.14+)
python3.14 -m venv venv

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

The setup script will automatically:

- Check for Python 3.14 or higher
- Install all dependencies
- Create necessary directories
- Start the application

## Quick Start

### 1. Upload RIS Files

1. Navigate to the homepage
2. Drag and drop RIS files onto the upload area, or click "Browse Files" to select files manually
3. Multiple files can be uploaded simultaneously
4. Select your preferred citation style (APA, MLA, Chicago, Harvard, or IEEE)
5. Choose upload mode:
   - **Start Fresh**: Replace all current references with new uploads
   - **Merge with Current**: Add new references to existing collection
6. Click "Upload & Sort References"

### 2. Add References from URLs

1. Enter a URL in the "Add URL" field (supports arXiv, DOI, PubMed, or any webpage)
2. Click "Add" button or press Enter
3. The system automatically detects the URL type and extracts metadata
4. Reference is added to your collection

### 3. Manage References

- **Change Citation Style**: Select a style from the dropdown to reformat all references
- **Search**: Use the search bar to filter references in real-time
- **Copy Individual**: Click the copy icon next to any reference
- **Delete Individual**: Click the delete icon next to any reference
- **Export**: Select export format and click "Copy" or "Download"
- **Clear All**: Remove all references to start over

## Usage Guide

### Supported File Formats

#### RIS Format

The application supports standard RIS format files. Example RIS entry:

```ris
TY  - JOUR
AU  - Smith, John A.
AU  - Doe, Jane B.
TI  - Sample Research Paper Title
JO  - Journal of Sample Research
VL  - 15
IS  - 3
SP  - 123
EP  - 145
PY  - 2023
DO  - 10.1000/sample.doi
ER  -
```

**Supported RIS Tags**:

- `TY` - Type of reference (JOUR, BOOK, CHAP, CONF, THES, RPRT, ELEC)
- `AU` - Author(s)
- `TI` - Title
- `JO` - Journal name
- `VL` - Volume
- `IS` - Issue
- `SP` - Start page
- `EP` - End page
- `PY` - Publication year
- `DO` - DOI
- `UR` - URL
- `PB` - Publisher
- `ER` - End of reference

### URL Examples

#### arXiv Papers

```
https://arxiv.org/pdf/2207.05221
https://arxiv.org/abs/2207.05221
```

#### DOI Links

```
https://doi.org/10.1000/xyz
https://example.com/doi/10.1000/xyz
```

#### PubMed Articles

```
https://pubmed.ncbi.nlm.nih.gov/12345678
```

#### Generic Web Pages

```
https://example.com/article
https://blog.example.com/post
```

### Citation Style Examples

#### APA Style

```
Smith, J. A., & Doe, J. B. (2023). Sample Research Paper Title. Journal of Sample Research, 15(3), 123-145. https://doi.org/10.1000/sample.doi
```

#### MLA Style

```
Smith, John A., and Jane B. Doe. "Sample Research Paper Title." Journal of Sample Research, vol. 15, no. 3, 2023, pp. 123-145, https://doi.org/10.1000/sample.doi.
```

#### Chicago Style

```
Smith, John A., and Jane B. Doe. "Sample Research Paper Title." Journal of Sample Research 15, no. 3 (2023): 123-145. https://doi.org/10.1000/sample.doi.
```

#### Harvard Style

```
Smith, J. A. & Doe, J. B. 2023, 'Sample Research Paper Title', Journal of Sample Research, vol. 15, no. 3, pp. 123-145, DOI: 10.1000/sample.doi.
```

#### IEEE Style

```
J. A. Smith and J. B. Doe, "Sample Research Paper Title," Journal of Sample Research, vol. 15, no. 3, pp. 123-145, 2023, doi: 10.1000/sample.doi.
```

### Export Format Examples

#### Plain Text

```
Smith, J. A., & Doe, J. B. (2023). Sample Research Paper Title. Journal of Sample Research, 15(3), 123-145.

Author, A. (2022). Another Paper. Journal Name, 10(2), 45-67.
```

#### Numbered List

```
1. Smith, J. A., & Doe, J. B. (2023). Sample Research Paper Title. Journal of Sample Research, 15(3), 123-145.

2. Author, A. (2022). Another Paper. Journal Name, 10(2), 45-67.
```

#### Markdown

```
- Smith, J. A., & Doe, J. B. (2023). Sample Research Paper Title. Journal of Sample Research, 15(3), 123-145.

- Author, A. (2022). Another Paper. Journal Name, 10(2), 45-67.
```

#### BibTeX

```bibtex
@article{0001,
  author = {Smith, John A. and Doe, Jane B.},
  title = {Sample Research Paper Title},
  journal = {Journal of Sample Research},
  year = {2023},
  volume = {15},
  pages = {123-145},
  doi = {10.1000/sample.doi}
}
```

## API Documentation

### Web Routes

#### `GET /`

Main upload page. Redirects to results page if references exist in session.

**Response**: HTML page with upload form or results page

#### `POST /upload`

Process uploaded RIS files.

**Request**:

- `files`: List of uploaded RIS files
- `citation_style`: Citation style (apa, mla, chicago, harvard, ieee)
- `merge_mode`: Upload mode ('new' or 'merge')

**Response**: HTML results page with formatted references

#### `POST /clear`

Clear all references from session.

**Response**: Redirect to index page

#### `GET /about`

About page.

**Response**: HTML about page

#### `GET /terms`

Terms of Service page.

**Response**: HTML terms page

#### `GET /privacy`

Privacy Policy page.

**Response**: HTML privacy page

### API Endpoints

#### `POST /api/add_url`

Add reference from URL with metadata extraction.

**Request Body**:

```json
{
  "url": "https://arxiv.org/pdf/2207.05221",
  "style": "apa"
}
```

**Response**:

```json
{
  "success": true,
  "reference": "Formatted citation string",
  "total_count": 5,
  "metadata": {
    "title": "Paper Title",
    "authors": ["Author 1", "Author 2"],
    "year": "2022",
    "source": "arXiv"
  }
}
```

**Error Response**:

```json
{
  "error": "URL is required"
}
```

#### `POST /api/delete_reference`

Delete a specific reference by index.

**Request Body**:

```json
{
  "index": 0
}
```

**Response**:

```json
{
  "success": true,
  "references": ["Formatted reference 1", "Formatted reference 2"],
  "total_count": 2
}
```

**Error Response**:

```json
{
  "error": "Invalid index"
}
```

#### `POST /api/change_style`

Change citation style for all references.

**Request Body**:

```json
{
  "style": "mla"
}
```

**Response**:

```json
{
  "success": true,
  "references": ["Formatted reference 1", "Formatted reference 2"],
  "style": "mla"
}
```

#### `POST /api/export`

Export references in different formats.

**Request Body**:

```json
{
  "reference_data": [
    {
      "authors": ["Smith, John"],
      "title": "Title",
      "year": "2023",
      ...
    }
  ],
  "format": "text|numbered|markdown|bibtex|ris",
  "style": "apa|mla|chicago|harvard|ieee"
}
```

**Response**:

```json
{
  "exported_text": "Exported references in selected format"
}
```

#### `GET /current_stats`

Get current reference statistics.

**Response**:

```json
{
  "count": 10,
  "has_references": true,
  "style": "apa"
}
```

## Architecture

### Project Structure

```
ris-reference-sorter-1/
├── app.py                 # Main Flask application
├── citation_formatter.py  # Citation style formatting module
├── url_metadata.py        # URL metadata extraction module
├── requirements.txt       # Python dependencies
├── runtime.txt           # Python runtime version
├── setup.sh              # Setup script for macOS/Linux
├── vercel.json           # Vercel deployment configuration
├── .gitignore            # Git ignore rules
├── .vercelignore         # Vercel ignore rules
├── api/
│   └── index.py          # Vercel serverless function entry point
├── templates/
│   ├── base.html         # Base template with navbar
│   ├── index.html        # Upload page
│   ├── results.html      # Results page with reference list
│   ├── about.html        # About page
│   ├── terms.html        # Terms of Service page
│   └── privacy.html      # Privacy Policy page
├── sample_references.ris # Sample RIS file for testing
├── additional_references.ris # Additional sample RIS file
├── README.md             # This file
├── TESTING.md            # Testing documentation
└── URL_METADATA.md       # URL metadata extraction documentation
```

### Technical Stack

#### Backend

- **Flask 3.1.2**: Web framework
- **rispy 0.10.0**: RIS file parsing library
- **Werkzeug 3.1.4**: WSGI utilities for security
- **requests 2.32.5**: HTTP library for API calls
- **beautifulsoup4 4.14.3**: HTML parsing for web page metadata
- **lxml 6.0.2**: XML/HTML parser backend

#### Frontend

- **Jinja2**: Template engine (included with Flask)
- **Vanilla JavaScript**: No frameworks, pure JavaScript
- **Custom CSS**: No external CSS frameworks
- **Inline SVG Icons**: No icon libraries

### Data Flow

1. **File Upload Flow**:

   - User uploads RIS file(s) → Flask receives files → Parse RIS format → Extract references → Remove duplicates → Sort alphabetically → Store in session → Format according to style → Display results

2. **URL Citation Flow**:

   - User enters URL → Detect URL type → Call appropriate API/extraction method → Extract metadata → Create reference entry → Add to session → Remove duplicates → Sort → Format → Return formatted citation

3. **Style Change Flow**:
   - User selects new style → Retrieve references from session → Reformat all references → Update display → Store style preference in session

### Session Management

The application uses Flask sessions for reference storage:

- References stored as dictionaries (not formatted strings)
- Citation style preference stored in session
- Session persists across page reloads
- Serverless-compatible (no database required)

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

References are formatted according to the selected citation style using the `CitationFormatter` class. Each style follows its respective formatting guidelines with proper handling of:

- Author formatting (single, multiple, et al.)
- Title formatting (italics, quotes)
- Journal formatting
- Volume, issue, and page formatting
- DOI and URL formatting
- Publication year placement

## Development

### Setting Up Development Environment

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd ris-reference-sorter-1
   ```

2. **Create virtual environment**:

   ```bash
   python3.14 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run in debug mode**:
   ```bash
   python app.py
   ```

### Code Style

- Follow PEP 8 Python style guide
- Use type hints for function parameters and return types
- Write docstrings for all functions and classes
- Keep functions small and focused
- Use meaningful variable names

### Adding New Citation Styles

To add a new citation style:

1. Add the style to `CitationStyle` enum in `citation_formatter.py`
2. Implement formatting method `format_<style_name>()` in `CitationFormatter` class
3. Add style to the `format()` method switch statement
4. Update templates to include the new style option
5. Update documentation

### Adding New URL Types

To add support for a new URL type:

1. Add URL detection logic in `URLMetadataExtractor.extract()`
2. Implement extraction method `_extract_<type>()` in `URLMetadataExtractor` class
3. Return dictionary with RIS-compatible fields
4. Add fallback handling for errors
5. Update documentation

### Testing

See `TESTING.md` for comprehensive testing guide.

### Debug Mode

To run in debug mode:

```python
app.run(debug=True, host='0.0.0.0', port=5030)
```

Debug mode provides:

- Automatic reloading on code changes
- Detailed error messages
- Debug toolbar (if installed)

## Deployment

### Vercel Deployment

The project includes Vercel configuration (`vercel.json`). To deploy:

1. **Install Vercel CLI**:

   ```bash
   npm i -g vercel
   ```

2. **Deploy**:

   ```bash
   vercel
   ```

3. **Production deployment**:
   ```bash
   vercel --prod
   ```

### Other Platforms

#### Heroku

1. Create `Procfile`:

   ```
   web: python app.py
   ```

2. Deploy:
   ```bash
   heroku create
   git push heroku main
   ```

#### AWS Lambda

Use Zappa or Serverless Framework to deploy Flask app to AWS Lambda.

#### Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.14-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5030
CMD ["python", "app.py"]
```

Build and run:

```bash
docker build -t ris-reference-sorter .
docker run -p 5030:5030 ris-reference-sorter
```

### Environment Variables

Set these environment variables for production:

- `SECRET_KEY`: Flask secret key for session security
- `FLASK_ENV`: Set to `production` for production deployment

## Configuration

### Application Settings

Modify these settings in `app.py`:

```python
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
```

### Port Configuration

Default port is `5030`. Change in `app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=YOUR_PORT)
```

## Troubleshooting

### Common Issues

#### File Upload Fails

- Check file format (`.ris` or `.txt`)
- Ensure file size is under 16MB
- Verify the file contains valid RIS format data

#### No References Found

- Verify the RIS file format is correct
- Check that the file contains proper RIS tags (TY, AU, TI, etc.)
- Try opening the file in a text editor to verify format

#### URL Extraction Fails

- Check your internet connection
- Verify the URL is accessible
- Some websites may block automated access
- Try the URL in a browser first to ensure it's valid
- Check API rate limits (CrossRef, PubMed)

#### Encoding Issues

- The application tries UTF-8 first, then falls back to Latin-1 encoding
- If issues persist, try converting your file to UTF-8 encoding

#### API Rate Limiting

- CrossRef and PubMed APIs may have rate limits
- If you encounter rate limiting, wait a few moments and try again
- Consider implementing caching for frequently accessed URLs

#### Port Already in Use

Change the port in `app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=YOUR_PORT)
```

#### Module Not Found Errors

1. Make sure you're in the virtual environment:

   ```bash
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate  # Windows
   ```

2. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt
   ```

#### Session Issues

- Clear your browser cookies for the application domain
- Restart the Flask application
- Check that `SECRET_KEY` is set correctly

## Contributing

Contributions are welcome! This is an open-source project, and we appreciate your help.

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**:
   - Follow the code style guidelines
   - Add tests if applicable
   - Update documentation
4. **Commit your changes**:
   ```bash
   git commit -m "Add: description of your feature"
   ```
5. **Push to your branch**:
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Submit a pull request**

### Contribution Guidelines

- Write clear commit messages
- Add tests for new features
- Update documentation as needed
- Follow existing code style
- Ensure all tests pass
- Be respectful and constructive in discussions

### Areas for Contribution

- Additional citation styles
- Support for more URL types (IEEE Xplore, ACM Digital Library, etc.)
- Batch URL processing
- Manual metadata editing interface
- Export to additional formats
- User authentication and persistent storage
- Performance optimizations
- UI/UX improvements
- Documentation improvements
- Bug fixes

## License

This project is licensed under the MIT License - see the LICENSE file for details.

**MIT License** means:

- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use
- ✅ Patent use

**Free and Open Source**: This project is completely free to use, modify, and distribute. No restrictions, no fees, no hidden costs.

## Support

### Getting Help

- **Documentation**: Check this README and other documentation files
- **Issues**: Open an issue on GitHub for bugs or feature requests
- **Discussions**: Use GitHub Discussions for questions and ideas

### Resources

- **RIS Format**: [RIS Format Specification](<https://en.wikipedia.org/wiki/RIS_(file_format)>)
- **Citation Styles**:
  - [APA Style Guide](https://apastyle.apa.org/)
  - [MLA Style Guide](https://style.mla.org/)
  - [Chicago Manual of Style](https://www.chicagomanualofstyle.org/)
  - [Harvard Referencing](https://www.harvard.edu/)
  - [IEEE Editorial Style Manual](https://www.ieee.org/)

### Reporting Issues

When reporting issues, please include:

- Python version
- Operating system
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages (if any)

## Changelog

### Version 2.1.0 (December 2, 2025)

- **Updated Dependencies**: Upgraded to latest versions of all dependencies
- **Python 3.14 Support**: Updated minimum Python version requirement to 3.14
- **Enhanced UI/UX**: Improved home page design with hero section and feature highlights
- **Performance Improvements**: Updated libraries for better performance and security

### Version 2.0.0

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

## Acknowledgments

- **rispy**: RIS file parsing library
- **Flask**: Web framework
- **BeautifulSoup**: HTML parsing
- **arXiv API**: For arXiv paper metadata
- **CrossRef API**: For DOI resolution
- **PubMed E-utilities**: For PubMed article metadata

## Contact

For questions, suggestions, or contributions, please open an issue on GitHub.

---

**Made with ❤️ for researchers, students, and academics worldwide**

**Free and Open Source** - Use it, modify it, share it!
