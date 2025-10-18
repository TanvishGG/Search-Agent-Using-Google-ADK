# Search Agent Using Google ADK

A powerful search agent built with the Google Agent Development Kit (ADK) that performs web searches and content extraction.

## Overview

This project implements a sophisticated, autonomous search agent powered by **Google's Agent Development Kit (ADK)** and the **Gemini 2.5 Flash** model. It's designed to be a multi-platform research tool that leverages AI to intelligently search, extract, and organize information from the web.

### What Makes It Special

**🔗 Multi-Source Search**: Instead of relying on a single search engine, the agent can search across:
- Google
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

3. Set up environment variables:
Go to the search-agent folder, then create a `.env` file based on `.env.example` and add your Google API credentials:
```
GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=your_google_genai_api_key
GOOGLE_CSE_ID=your_google_custom_search_engine_id
SEARCH_API_KEY=your_google_search_api_key
```
- **GOOGLE_GENAI_USE_VERTEXAI**: Set to 0 to use standard Google AI API (or 1 for Vertex AI)
- **GOOGLE_API_KEY**: Your Google Gemini API key. Get it from [Google AI Studio](https://aistudio.google.com/app/apikey)
- **GOOGLE_CSE_ID**: Your Google Custom Search Engine ID. Create a custom search engine at [Google Custom Search](https://programmablesearchengine.google.com/)
- **SEARCH_API_KEY**: Your Google Search API key for programmatic search access. Get it from [Google Cloud Console](https://console.cloud.google.com/)

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the App:
```bash
adk web
```

6. Open the URL from the terminal

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

#### `search_google(query: str) -> dict`
Performs a web search using Google Custom Search API (CSE).
- **Input**: `query` - Search query string
- **Output**: Dictionary with query, source, results, and total count
- **Uses**: `SEARCH_API_KEY` and `GOOGLE_CSE_ID` environment variables
- **Returns per result**: title, URL, snippet

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
- **Returns per post**: title, URL, subreddit, score, num_comments, author, selftext (truncated to 500 chars)

#### `search_reddit_r(subreddit: str, query: str, sort: str) -> dict`
Searches within a specific subreddit.
- **Input**:
  - `subreddit` - Subreddit name (without r/)
  - `query` - Search query string
  - `sort` - Sort by (default: "relevance")
- **Output**: Dictionary with query, subreddit, and post results
- **Returns per post**: title, URL, score, num_comments, author, selftext (truncated to 500 chars)

#### `search_stackoverflow(query: str, sort: str) -> dict`
Searches Stack Overflow for questions.
- **Input**:
  - `query` - Search query string
  - `sort` - Sort by (default: "relevance")
- **Output**: Dictionary with query, total count, and question results
- **Returns per question**: title, URL, score, answer_count, is_answered, tags, body (truncated to 300 chars)

#### `search_wikipedia(query: str) -> dict`
Searches Wikipedia for articles.
- **Input**: `query` - Search query string
- **Output**: Dictionary with query and article results
- **Returns per article**: title, URL, snippet, content (truncated to 1000 chars)

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
