# Search Agent Using Google ADK

A powerful search agent built with the Google Agent Development Kit (ADK) that performs web searches and content extraction.

## Overview

This project implements a sophisticated, autonomous search agent powered by **Google's Agent Development Kit (ADK)** and the **Gemini 2.5 Flash** model. It's designed to be a multi-platform research tool that leverages AI to intelligently search, extract, and organize information from the web.

### What Makes It Special

**🔗 Multi-Source Search**: Instead of relying on a single search engine, the agent can search across:
- Google & DuckDuckGo (with intelligent fallback)
- GitHub repositories
- Reddit communities and discussions
- Stack Overflow questions and answers
- Wikipedia articles

## Technology Stack

- **Python 3.7+**
- **Google ADK** - Agent Development Kit for building AI agents
- **BeautifulSoup4** - HTML parsing and content extraction
- **Requests** - HTTP library for web requests

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Search-Agent-Using-Google-ADK
```

2. Create Virtual Environment:
```bash
python -m venv venv
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the App:
```bash
adk web
```

5. Open the URL from the terminal

## Dependencies

The project requires the following Python packages:
- `requests>=2.25.0` - HTTP requests library
- `beautifulsoup4>=4.9.0` - HTML/XML parsing
- `google-adk` - Google Agent Development Kit

## Project Structure

```
Search-Agent-Using-Google-ADK/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
└── search-agent/
    ├── __init__.py          # Package initialization
    ├── agent.py             # Main agent implementation
    ├── __pycache__/         # Python cache directory
    └── data/                # Storage for search results and content
```

## Tools & Functions

The search agent includes the following tools that can be used autonomously:

#### `search_web(query: str) -> dict`
Performs a web search with intelligent fallback.
- **Input**: `query` - Search query string
- **Output**: Dictionary with query, source (google/duckduckgo), results, and total count
- **Features**:
  - Tries Google first
  - Falls back to DuckDuckGo if no results found
  - Returns structured results with title, URL, and snippet

#### `search_github(query: str, sort: str) -> dict`
Searches GitHub for repositories.
- **Input**: 
  - `query` - Search query string
  - `sort` - Sort by (default: "stars", options: stars, forks, updated)
- **Output**: Dictionary with query, total count, and repository results
- **Returns per repo**: name, URL, description, stars, language, updated_at

#### `search_reddit(query: str, sort: str) -> dict`
Searches Reddit for posts across all subreddits.
- **Input**:
  - `query` - Search query string
  - `sort` - Sort by (default: "relevance")
- **Output**: Dictionary with query and post results
- **Returns per post**: title, URL, subreddit, score, comments, author, text excerpt

#### `search_reddit_r(subreddit: str, query: str, sort: str) -> dict`
Searches within a specific subreddit.
- **Input**:
  - `subreddit` - Subreddit name (without r/)
  - `query` - Search query string
  - `sort` - Sort by (default: "relevance")
- **Output**: Dictionary with query, subreddit, and post results
- **Returns per post**: title, URL, score, comments, author, text excerpt

#### `search_stackoverflow(query: str, sort: str) -> dict`
Searches Stack Overflow for questions.
- **Input**:
  - `query` - Search query string
  - `sort` - Sort by (default: "relevance")
- **Output**: Dictionary with query, total count, and question results
- **Returns per question**: title, URL, score, answer count, is_answered, tags, body excerpt

#### `search_wikipedia(query: str) -> dict`
Searches Wikipedia for articles.
- **Input**: `query` - Search query string
- **Output**: Dictionary with query and article results
- **Returns per article**: title, URL, snippet, full content excerpt

#### `fetch_url_content(url: str) -> dict`
Extracts and parses content from a URL.
- **Input**: `url` - URL string
- **Output**: Dictionary with URL, title, content, and status code

#### `write_to_file(file_name: str, content: str) -> dict`
Saves content to a file in the data directory.
- **Input**:
  - `file_name` - Name for the file
  - `content` - Content to write
- **Output**: Status dictionary with file path, success status, and content size

#### `get_current_data_files() -> dict`
Lists all files in the data directory.
- **Output**: Dictionary with success status and list of file names

#### `read_from_file(file_name: str) -> dict`
Reads content from a file in the data directory.
- **Input**: `file_name` - Name of the file to read
- **Output**: Dictionary with file path, content, size, and status

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.
