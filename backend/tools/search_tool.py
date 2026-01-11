import requests
from typing import List, Dict


class SearchTool:
    def __init__(self):
        self.base_url = "https://api.duckduckgo.com/"
    
    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        try:
            params = {
                'q': query,
                'format': 'json',
                'no_html': 1,
                'skip_disambig': 1
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            data = response.json()
            
            results = []
            
            if data.get('AbstractURL'):
                results.append({
                    'title': data.get('Heading', 'No title'),
                    'snippet': data.get('AbstractText', 'No description'),
                    'url': data.get('AbstractURL')
                })
            
            for topic in data.get('RelatedTopics', [])[:max_results]:
                if isinstance(topic, dict) and 'Text' in topic:
                    results.append({
                        'title': topic.get('Text', '').split(' - ')[0],
                        'snippet': topic.get('Text', ''),
                        'url': topic.get('FirstURL', '')
                    })
            
            return results[:max_results]
            
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def search_competitor(self, company_name: str, product_name: str = "") -> List[Dict]:
        query = f"{company_name} {product_name} product features pricing"
        return self.search(query.strip())
