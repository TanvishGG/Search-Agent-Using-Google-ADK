import os
from urllib.parse import quote_plus
import requests
from bs4 import BeautifulSoup

from google.adk.agents import Agent

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

TIMEOUT = 10


def search_google(query: str) -> dict:
    """Search using Google Custom Search API (CSE)."""
    api_key = os.environ.get('SEARCH_API_KEY')
    search_engine_id = os.environ.get('GOOGLE_CSE_ID')

    if not api_key or not search_engine_id:
        return {'query': query, 'error': 'Missing SEARCH_API_KEY or GOOGLE_CSE_ID'}

    try:
        response = requests.get(
            'https://www.googleapis.com/customsearch/v1',
            params={'key': api_key, 'cx': search_engine_id, 'q': query, 'num': 10},
            headers=HEADERS,
            timeout=TIMEOUT
        )
        response.raise_for_status()
        
        data = response.json()
        results = [
            {'title': item.get('title', ''), 'url': item.get('link', ''), 'snippet': item.get('snippet', '')}
            for item in data.get('items', [])
        ]
        
        total = data.get('searchInformation', {}).get('totalResults')
        return {
            'query': query,
            'source': 'google',
            'results': results,
            'total_found': int(total) if total else len(results)
        }

    except requests.RequestException as e:
        return {'query': query, 'error': f'Request failed: {str(e)}'}
    except Exception as e:
        return {'query': query, 'error': str(e)}




def fetch_url_content(url: str) -> dict:
    """Fetch and parse content from a URL."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)

        if response.status_code != 200:
            return {'url': url, 'error': f'HTTP {response.status_code}'}

        content_type = response.headers.get('content-type', '').lower()

        if 'text/html' in content_type:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for elem in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                elem.decompose()

            main_content = None
            for selector in ['main', 'article', '.content', '.main-content', '#content', '#main']:
                main_content = soup.select_one(selector)
                if main_content:
                    break

            content = main_content.get_text(separator='\n', strip=True) if main_content else soup.get_text()
            title = soup.title.string if soup.title else url

            return {
                'url': url,
                'title': title,
                'content': content,
                'status_code': response.status_code
            }

        return {
            'url': url,
            'content': response.text,
            'content_type': content_type,
            'status_code': response.status_code
        }

    except Exception as e:
        return {'url': url, 'error': str(e)}


def write_to_file(file_name: str, content: str) -> dict:
    """Write content to a file in the data directory."""
    try:
        if not file_name or not content:
            return {"status": "error", "error": "Invalid file name or content"}

        file_name = os.path.basename(file_name)
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, "data", file_name)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return {
            "file_name": file_path,
            "status": "success",
            "size": len(content)
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}

def get_current_data_files() -> dict:
    """Get a list of current file names in the data directory."""
    try:
        base_dir = os.path.dirname(__file__)
        data_dir = os.path.join(base_dir, "data")

        if not os.path.exists(data_dir):
            return {"status": "success", "files": []}

        files = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]

        return {
            "status": "success",
            "files": files
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


def read_from_file(file_name: str) -> dict:
    """Read content from a file."""
    try:
        if not file_name:
            return {"status": "error", "error": "Invalid file name"}

        file_name = os.path.basename(file_name)
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, "data", file_name)

        if not os.path.exists(file_path):
            return {"status": "error", "error": "File not found"}

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return {
            "file_name": file_path,
            "content": content,
            "size": len(content),
            "status": "success"
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


def search_github(query: str, sort: str) -> dict:
    """Search GitHub for repositories."""
    try:
        sort_value = sort or "stars"
        headers = {
            'User-Agent': HEADERS['User-Agent'],
            'Accept': 'application/vnd.github.v3+json'
        }

        url = f"https://api.github.com/search/repositories?q={quote_plus(query)}&sort={sort_value}&order=desc&per_page=10"
        response = requests.get(url, headers=headers, timeout=TIMEOUT)

        if response.status_code != 200:
            return {'query': query, 'error': f'HTTP {response.status_code}'}

        data = response.json()
        results = [
            {
                'name': repo['full_name'],
                'url': repo['html_url'],
                'description': repo.get('description', ''),
                'stars': repo.get('stargazers_count', 0),
                'language': repo.get('language', ''),
                'updated_at': repo.get('updated_at', '')
            }
            for repo in data.get('items', [])
        ]

        return {
            'query': query,
            'total_count': data.get('total_count', 0),
            'results': results
        }

    except Exception as e:
        return {'query': query, 'error': str(e)}


def search_reddit(query: str, sort: str) -> dict:
    """Search Reddit for posts."""
    try:
        sort_value = sort or "relevance"
        headers = {'User-Agent': HEADERS['User-Agent']}
        url = f"https://www.reddit.com/search.json?q={quote_plus(query)}&sort={sort_value}&limit=10"
        response = requests.get(url, headers=headers, timeout=TIMEOUT)

        if response.status_code != 200:
            return {'query': query, 'error': f'HTTP {response.status_code}'}

        data = response.json()
        results = []

        for post in data.get('data', {}).get('children', []):
            post_data = post['data']
            selftext = post_data.get('selftext', '')
            results.append({
                'title': post_data.get('title', ''),
                'url': f"https://reddit.com{post_data.get('permalink', '')}",
                'subreddit': post_data.get('subreddit', ''),
                'score': post_data.get('score', 0),
                'num_comments': post_data.get('num_comments', 0),
                'author': post_data.get('author', ''),
                'selftext': selftext[:500] + '...' if len(selftext) > 500 else selftext
            })

        return {'query': query, 'results': results}

    except Exception as e:
        return {'query': query, 'error': str(e)}


def search_reddit_r(subreddit: str, query: str, sort: str) -> dict:
    """Search a specific subreddit."""
    try:
        sort_value = sort or "relevance"
        headers = {'User-Agent': HEADERS['User-Agent']}
        url = f"https://www.reddit.com/r/{subreddit}/search.json?q={quote_plus(query)}&sort={sort_value}&restrict_sr=1&limit=10"
        response = requests.get(url, headers=headers, timeout=TIMEOUT)

        if response.status_code != 200:
            return {'query': query, 'subreddit': subreddit, 'error': f'HTTP {response.status_code}'}

        data = response.json()
        results = []

        for post in data.get('data', {}).get('children', []):
            post_data = post['data']
            selftext = post_data.get('selftext', '')
            results.append({
                'title': post_data.get('title', ''),
                'url': f"https://reddit.com{post_data.get('permalink', '')}",
                'score': post_data.get('score', 0),
                'num_comments': post_data.get('num_comments', 0),
                'author': post_data.get('author', ''),
                'selftext': selftext[:500] + '...' if len(selftext) > 500 else selftext
            })

        return {'query': query, 'subreddit': subreddit, 'results': results}

    except Exception as e:
        return {'query': query, 'subreddit': subreddit, 'error': str(e)}


def search_stackoverflow(query: str, sort: str) -> dict:
    """Search Stack Overflow for questions."""
    try:
        sort_value = sort or "relevance"
        url = f"https://api.stackexchange.com/2.3/search/advanced?order=desc&sort={sort_value}&q={quote_plus(query)}&site=stackoverflow&pagesize=10&filter=withbody"
        response = requests.get(url, timeout=TIMEOUT)

        if response.status_code != 200:
            return {'query': query, 'error': f'HTTP {response.status_code}'}

        data = response.json()
        results = []

        for question in data.get('items', []):
            body = question.get('body', '')
            results.append({
                'title': question.get('title', ''),
                'url': question.get('link', ''),
                'score': question.get('score', 0),
                'answer_count': question.get('answer_count', 0),
                'is_answered': question.get('is_answered', False),
                'tags': question.get('tags', []),
                'body': body[:300] + '...' if len(body) > 300 else body
            })

        return {
            'query': query,
            'total': data.get('total', 0),
            'results': results
        }

    except Exception as e:
        return {'query': query, 'error': str(e)}

def search_wikipedia(query: str) -> dict:
    """Search Wikipedia for articles."""
    try:
        headers = {
            'User-Agent': HEADERS['User-Agent'],
            'Accept': 'application/json'
        }
        url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={quote_plus(query)}&format=json&srlimit=10&srprop=title|snippet"
        response = requests.get(url, headers=headers, timeout=TIMEOUT)

        if response.status_code != 200:
            return {'query': query, 'error': f'HTTP {response.status_code}'}

        data = response.json()
        
        if 'error' in data:
            return {'query': query, 'error': data['error'].get('info', 'Unknown error')}

        results = []

        for result in data.get('query', {}).get('search', []):
            page_content = _get_wikipedia_page_content(result['title'])
            results.append({
                'title': result['title'],
                'url': f"https://en.wikipedia.org/wiki/{quote_plus(result['title'])}",
                'snippet': result.get('snippet', ''),
                'content': page_content[:1000] + '...' if len(page_content) > 1000 else page_content
            })

        return {'query': query, 'results': results}

    except Exception as e:
        return {'query': query, 'error': str(e)}


def _get_wikipedia_page_content(title: str) -> str:
    """Get full Wikipedia page content."""
    try:
        headers = {
            'User-Agent': HEADERS['User-Agent'],
            'Accept': 'application/json'
        }
        url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&titles={quote_plus(title)}&format=json&exintro=false&explaintext=true"
        response = requests.get(url, headers=headers, timeout=TIMEOUT)

        if response.status_code == 200:
            data = response.json()
            pages = data.get('query', {}).get('pages', {})

            for page_id, page_data in pages.items():
                if page_id != '-1':
                    return page_data.get('extract', '')
        return ""
    except Exception:
        return ""


root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful search agent that can search the web and answer questions.',
    instruction='You are an advanced search agent. Use the scraping tools to search the web, GitHub, Reddit, Stack Overflow, and Wikipedia. You can also fetch content from URLs and read/write files in the data directory. Always try to use the tools to get the most accurate and up-to-date information.',
    tools=[
        search_google,
        search_github,
        search_reddit,
        search_reddit_r,
        search_stackoverflow,
        search_wikipedia,
        fetch_url_content,
        write_to_file,
        get_current_data_files,
        read_from_file
    ],
)
