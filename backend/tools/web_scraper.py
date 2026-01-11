import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import time


class WebScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_page(self, url: str) -> Dict:
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            title = soup.find('title')
            title_text = title.get_text().strip() if title else "No title found"
            
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            description = meta_desc['content'] if meta_desc and meta_desc.get('content') else ""
            
            headings = [h.get_text().strip() for h in soup.find_all(['h1', 'h2', 'h3'])]
            
            paragraphs = [p.get_text().strip() for p in soup.find_all('p') if len(p.get_text().strip()) > 50]
            
            links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.startswith('http'):
                    links.append(href)
            
            return {
                "url": url,
                "title": title_text,
                "description": description,
                "headings": headings[:10],
                "content_snippets": paragraphs[:5],
                "external_links": links[:10],
                "status": "success"
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "url": url,
                "status": "error",
                "error": str(e)
            }
    
    def scrape_multiple(self, urls: List[str], delay: float = 1.0) -> List[Dict]:
        results = []
        for url in urls:
            result = self.scrape_page(url)
            results.append(result)
            time.sleep(delay)
        return results
    
    def extract_product_info(self, url: str) -> Dict:
        data = self.scrape_page(url)
        
        if data['status'] == 'error':
            return data
        
        pricing_keywords = ['price', 'pricing', 'cost', '$', '€', '£']
        features_keywords = ['feature', 'benefit', 'capability', 'includes']
        
        pricing_info = []
        features_info = []
        
        for snippet in data.get('content_snippets', []):
            snippet_lower = snippet.lower()
            if any(keyword in snippet_lower for keyword in pricing_keywords):
                pricing_info.append(snippet)
            if any(keyword in snippet_lower for keyword in features_keywords):
                features_info.append(snippet)
        
        return {
            "url": url,
            "title": data.get('title'),
            "description": data.get('description'),
            "pricing_mentions": pricing_info[:3],
            "feature_mentions": features_info[:5],
            "status": "success"
        }
