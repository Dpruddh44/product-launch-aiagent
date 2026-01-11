from .base_agent import BaseAgent, AgentState
from tools.search_tool import SearchTool
from tools.web_scraper import WebScraper
from typing import Dict, List


class CompetitiveResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="CompetitiveResearcher",
            role="Competitive Intelligence Analyst"
        )
        self.search_tool = SearchTool()
        self.scraper = WebScraper()
    
    def execute(self, state: AgentState, task: str) -> AgentState:
        self.log_action(state, f"Starting competitive research for: {task}")
        
        competitors = self.extract_competitors(task)
        
        for competitor in competitors:
            self.log_action(state, f"Researching competitor: {competitor}")
            
            search_results = self.search_tool.search_competitor(competitor)
            state.search_results.extend(search_results)
            
            for result in search_results[:2]:
                if result.get('url'):
                    scraped = self.scraper.extract_product_info(result['url'])
                    if scraped.get('status') == 'success':
                        state.scraped_data.append(scraped)
        
        analysis = self.analyze_competitors(state.scraped_data, state.search_results)
        state.competitor_data = analysis
        
        self.log_action(state, f"Completed research on {len(competitors)} competitors")
        
        return state
    
    def extract_competitors(self, task: str) -> List[str]:
        words = task.split()
        competitors = []
        
        for i, word in enumerate(words):
            if word.lower() in ['vs', 'versus', 'competitor', 'competitors']:
                if i + 1 < len(words):
                    competitors.append(words[i + 1])
            elif word.lower() == 'and' and i > 0 and i + 1 < len(words):
                competitors.append(words[i + 1])
        
        if not competitors and len(words) > 0:
            competitors.append(words[0])
        
        return competitors[:3]
    
    def analyze_competitors(self, scraped_data: List[Dict], search_results: List[Dict]) -> Dict:
        competitor_summary = {}
        
        for data in scraped_data:
            url = data.get('url', 'unknown')
            competitor_summary[url] = {
                "title": data.get('title', ''),
                "pricing_info": data.get('pricing_mentions', []),
                "features": data.get('feature_mentions', []),
                "description": data.get('description', '')
            }
        
        return {
            "competitors_analyzed": len(scraped_data),
            "total_sources": len(search_results),
            "competitor_details": competitor_summary,
            "key_findings": self.extract_key_findings(scraped_data)
        }
    
    def extract_key_findings(self, scraped_data: List[Dict]) -> List[str]:
        findings = []
        
        pricing_count = sum(1 for d in scraped_data if d.get('pricing_mentions'))
        if pricing_count > 0:
            findings.append(f"Found pricing information for {pricing_count} competitors")
        
        feature_count = sum(1 for d in scraped_data if d.get('feature_mentions'))
        if feature_count > 0:
            findings.append(f"Identified features for {feature_count} competitors")
        
        return findings
