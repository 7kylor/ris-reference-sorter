# RIS Reference Sorter

A Flask web application that processes RIS (Research Information Systems) files, automatically sorts academic references alphabetically, removes duplicates, and provides easy copying and export functionality.

## Features

- **Multiple File Upload**: Upload one or multiple RIS files at once
- **Automatic Sorting**: References sorted alphabetically by first author's last name
- **Duplicate Removal**: Automatically removes duplicate references
- **Merge Collections**: Merge new uploads with existing references or start fresh
- **Easy Copying**: Copy individual references or all references at once
- **Export Options**: Export in different formats (Plain text, Numbered list, Markdown)
- **Statistics**: View processing statistics and file information
- **Modern UI**: Beautiful, responsive web interface with drag-and-drop support
- **Mobile Friendly**: Works on desktop, tablet, and mobile devices
- **Session Management**: Keep references loaded between uploads for easy merging

## Screenshot

The application features:

- Drag-and-drop file upload area
- Real-time file selection display
- Comprehensive statistics dashboard
- Individual and bulk copy functionality
- Multiple export formats
- Responsive design with Bootstrap

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
   cd ris-reference-sorter
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

   ```
   http://localhost:5000
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

## Usage

### Basic Usage

1. **Upload Files**:
   - Drag and drop RIS files onto the upload area, or
   - Click "Browse Files" to select files manually
   - Multiple files can be uploaded simultaneously

2. **Process References**:
   - Click "Upload & Sort References"
   - The application will parse all RIS files, remove duplicates, and sort alphabetically

3. **Choose Upload Mode**:
   - **Start Fresh**: Replace all current references with new uploads
   - **Merge with Current**: Add new references to existing collection

4. **View Results**:
   - See processing statistics (files processed, unique references, duplicates removed)
   - Browse the sorted reference list
   - Switch between expanded and compact view modes

5. **Copy/Export References**:
   - Copy individual references using the copy button
   - Copy all references at once in different formats
   - Download references as a text file

6. **Manage Collection**:
   - Add more files to existing collection
   - Clear all references to start over

### Export Formats

- **Plain Text**: References separated by double line breaks
- **Numbered List**: References with sequential numbering
- **Markdown**: References formatted as markdown list items

### Example RIS File Format

```
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

- `GET /` - Main upload page
- `POST /upload` - Process uploaded RIS files

### API Routes

- `POST /api/export` - Export references in different formats

  ```json
  {
    "references": ["reference1", "reference2"],
    "format": "text|numbered|markdown"
  }
  ```

## Configuration

The application can be configured by modifying these settings in `app.py`:

```python
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
```

## Technical Details

### Dependencies

- **Flask**: Web framework
- **rispy**: RIS file parsing library
- **Werkzeug**: WSGI utilities for security

### File Processing

1. Files are temporarily uploaded to the `uploads` folder
2. Each RIS file is parsed using the `rispy` library
3. References are formatted into standard citation format
4. Duplicates are removed based on exact text matching
5. References are sorted alphabetically by first author's last name
6. Temporary files are cleaned up after processing

### Citation Format

The application formats references following a standard academic citation style:

```
Author, A., & Author, B. (Year). Title of the paper. Journal Name, Volume(Issue), Pages. DOI/URL
```

## Troubleshooting

### Common Issues

1. **File Upload Fails**:
   - Check file format (.ris or .txt)
   - Ensure file size is under 16MB
   - Verify the file contains valid RIS format data

2. **No References Found**:
   - Verify the RIS file format is correct
   - Check that the file contains proper RIS tags (TY, AU, TI, etc.)

3. **Encoding Issues**:
   - The application tries UTF-8 first, then falls back to Latin-1 encoding
   - If issues persist, try converting your file to UTF-8 encoding

### Debug Mode

To run in debug mode for development:

```python
app.run(debug=True, host='0.0.0.0', port=5000)
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

## Changelog

### Version 1.0.0

- Initial release
- Multi-file RIS upload support
- Automatic sorting and duplicate removal
- Multiple export formats
- Responsive web interface
- Copy to clipboard functionality
