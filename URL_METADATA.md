# URL Metadata Extraction

The application now includes comprehensive URL metadata extraction capabilities.

**Last Updated**: December 2, 2025

## Supported URL Types

### 1. arXiv Papers

- **Example**: `https://arxiv.org/pdf/2207.05221` or `https://arxiv.org/abs/2207.05221`
- **Extracts**:
  - Title (with arXiv prefix removed)
  - Authors
  - Publication year
  - Abstract
  - Primary category
  - arXiv ID
- **Method**: Uses arXiv API (`export.arxiv.org/api/query`)

### 2. DOI Links

- **Example**: `https://doi.org/10.1000/xyz` or `https://example.com/doi/10.1000/xyz`
- **Extracts**:
  - Title
  - Authors
  - Publication year
  - Journal name
  - Volume and pages
  - DOI
- **Method**: Uses CrossRef API (`api.crossref.org`)

### 3. PubMed Articles

- **Example**: `https://pubmed.ncbi.nlm.nih.gov/12345678`
- **Extracts**:
  - Title
  - Authors
  - Publication year
  - Journal name
- **Method**: Uses PubMed E-utilities API

### 4. Generic Web Pages

- **Example**: Any website URL
- **Extracts**:
  - Page title (from `<title>` tag or Open Graph meta tags)
  - Authors (from meta tags or structured data)
  - Publication date (from meta tags)
  - Description/abstract
- **Method**: HTML parsing with BeautifulSoup

## Features

- **Automatic Detection**: Automatically detects URL type and uses appropriate extraction method
- **Fallback Handling**: If specialized extraction fails, falls back to generic HTML parsing
- **Error Handling**: Gracefully handles network errors and missing data
- **User Feedback**: Shows loading state and detailed success messages

## Installation

The following dependencies are required (already in `requirements.txt`):

```
requests==2.32.5
beautifulsoup4==4.14.3
lxml==6.0.2
```

Install with:

```bash
pip install -r requirements.txt
```

## Usage

Simply paste a URL into the "Add from URL" field and click "Add". The system will:

1. Detect the URL type
2. Fetch metadata using appropriate API or HTML parsing
3. Create a properly formatted citation entry
4. Add it to your reference collection

## Example

**Input**: `https://arxiv.org/pdf/2207.05221`

**Extracted Metadata**:

- Title: "Language Models (Mostly) Know What They Know"
- Authors: ["Kadavath, Saurav", "Conerly, Tom", ...]
- Year: 2022
- Journal: "arXiv preprint arXiv:2207.05221"
- URL: Original URL preserved

## Technical Details

### URLMetadataExtractor Class

The `URLMetadataExtractor` class handles all metadata extraction:

```python
extractor = URLMetadataExtractor()
metadata = extractor.extract(url)
```

Returns a dictionary with RIS-compatible fields:

- `type_of_reference`: Reference type (JOUR, ELEC, etc.)
- `authors`: List of author names
- `title`: Document title
- `year`: Publication year
- `journal_name`: Journal or source name
- `url`: Original URL
- `doi`: DOI if available
- Additional fields as available

### Error Handling

- Network timeouts: 10 seconds default
- Missing data: Uses fallback values
- API failures: Falls back to HTML parsing
- Invalid URLs: Creates basic entry with URL

## Limitations

- Some websites may block automated access
- Rate limiting may apply to APIs (CrossRef, PubMed)
- Complex websites may require additional parsing logic
- Some metadata may not be available for all sources

## Future Improvements

- Add support for more academic databases (IEEE Xplore, ACM Digital Library)
- Cache metadata to reduce API calls
- Support for batch URL processing
- Manual metadata editing interface
