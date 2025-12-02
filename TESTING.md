# Local Testing Guide

This guide will help you test the RIS Reference Sorter application locally.

**Last Updated**: December 2, 2025

## Prerequisites

- Python 3.14 or higher
- pip (Python package installer)

## Quick Start

### Option 1: Using the Setup Script (Recommended)

1. Make the setup script executable:

   ```bash
   chmod +x setup.sh
   ```

2. Run the setup script:

   ```bash
   ./setup.sh
   ```

   This will:

   - Check Python installation
   - Install all dependencies
   - Create necessary directories
   - Start the application

### Option 2: Manual Setup

1. **Create a virtual environment** (recommended):

   ```bash
   python3 -m venv venv

   # On macOS/Linux:
   source venv/bin/activate

   # On Windows:
   venv\Scripts\activate
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python3 app.py
   ```

## Accessing the Application

Once the application is running, open your web browser and navigate to:

```
http://localhost:5030
```

## Testing Features

### 1. Test File Upload

1. Use the sample RIS files included in the project:

   - `sample_references.ris`
   - `additional_references.ris`

2. On the homepage:

   - Drag and drop a RIS file onto the upload area, OR
   - Click "Browse Files" and select a RIS file

3. Select a citation style (APA, MLA, Chicago, Harvard, or IEEE)

4. Choose upload mode:

   - **Start Fresh**: Replace all references
   - **Merge with Current**: Add to existing references

5. Click "Upload & Sort References"

### 2. Test URL Citation

1. On the homepage, find the red header section
2. Paste a URL (e.g., `https://www.example.com/article`)
3. Click "Add Citation" or press Enter
4. The citation will be added to your collection

### 3. Test Citation Style Switching

1. After uploading references, you'll see the results page
2. Use the "Citation Style" dropdown to change styles
3. References will reformat automatically without re-uploading

### 4. Test Search/Filter

1. On the results page, use the search box
2. Type keywords, author names, or titles
3. References will filter in real-time

### 5. Test Export Options

1. On the results page, select an export format:

   - Plain Text
   - Numbered List
   - Markdown
   - BibTeX
   - RIS

2. Click "Copy" to copy to clipboard
3. Click "Download" to download as a file

### 6. Test Individual Reference Copy

1. On the results page, click the copy icon next to any reference
2. The reference will be copied to your clipboard

## Testing Different Citation Styles

Try uploading the same RIS file and switching between styles to see how formatting changes:

- **APA**: Author, A. (Year). Title. Journal, Volume(Issue), Pages.
- **MLA**: Author, A. "Title." Journal, vol. Volume, no. Issue, Year, pp. Pages.
- **Chicago**: Author, A. "Title." Journal Volume, no. Issue (Year): Pages.
- **Harvard**: Author, A Year, Title, Journal, Volume(Issue), pp.Pages.
- **IEEE**: Author, A., "Title," Journal, vol. Volume, no. Issue, pp. Pages, Year.

## Troubleshooting

### Port Already in Use

If port 5030 is already in use, you can change it in `app.py`:

```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=YOUR_PORT)
```

### Module Not Found Errors

If you get import errors:

1. Make sure you're in the virtual environment:

   ```bash
   source venv/bin/activate  # macOS/Linux
   # or
   venv\Scripts\activate  # Windows
   ```

2. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Session Issues

The application uses Flask sessions. If you encounter session-related issues:

1. Clear your browser cookies for `localhost:5030`
2. Restart the Flask application

### File Upload Issues

- Ensure files have `.ris` or `.txt` extension
- Check that files contain valid RIS format data
- Maximum file size is 16MB

## Sample RIS File Format

If you want to create your own test file, use this format:

```
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

## Development Mode

The application runs in debug mode by default, which provides:

- Automatic reloading on code changes
- Detailed error messages
- Debug toolbar (if installed)

To disable debug mode, change in `app.py`:

```python
app.run(debug=False, host='0.0.0.0', port=5030)
```

## Testing Checklist

- [ ] Application starts without errors
- [ ] Homepage loads correctly
- [ ] Can upload RIS files
- [ ] Can add citations via URL
- [ ] Citation styles work correctly
- [ ] Can switch citation styles dynamically
- [ ] Search/filter works
- [ ] Export formats work (Copy and Download)
- [ ] Individual reference copy works
- [ ] Merge mode works correctly
- [ ] Clear all references works
- [ ] Session persists across page reloads

## Next Steps

After testing locally, you can:

1. Deploy to Vercel (configuration already included)
2. Deploy to other platforms (Heroku, AWS, etc.)
3. Add more citation styles
4. Enhance URL citation with metadata extraction
5. Add user authentication for persistent storage
