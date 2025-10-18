import sys
import os
import importlib.util

# Load the agent module directly from the search-agent folder (invalid package name with hyphen)
base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
agent_path = os.path.join(base, 'search-agent', 'agent.py')
spec = importlib.util.spec_from_file_location('agent', agent_path)
agent = importlib.util.module_from_spec(spec)
sys.modules['agent'] = agent
spec.loader.exec_module(agent)
search_google = agent.search_google


if __name__ == '__main__':
    print('Running search_google("python programming")...')
    res = agent.search_google('python programming')
    print('Result keys:', list(res.keys()))
    print('total_found:', res.get('total_found') if 'total_found' in res else 'n/a')
    print('Sample results count:', len(res.get('results', [])))
    if res.get('error'):
        print('Error:', res.get('error'))
    if res.get('results'):
        for r in res['results'][:3]:
            print('-', r.get('title'), '|', r.get('url'))
