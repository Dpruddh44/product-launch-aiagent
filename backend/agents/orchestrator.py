from .base_agent import AgentState
from .competitive_research_agent import CompetitiveResearchAgent
from .sentiment_agent import SentimentAnalysisAgent
from .strategy_agent import LaunchStrategyAgent
from typing import Dict
from datetime import datetime


class AgentOrchestrator:
    def __init__(self):
        self.competitive_agent = CompetitiveResearchAgent()
        self.sentiment_agent = SentimentAnalysisAgent()
        self.strategy_agent = LaunchStrategyAgent()
    
    def run_analysis(self, product_name: str, competitors: str = "") -> Dict:
        state = AgentState()
        
        task = f"{product_name}"
        if competitors:
            task += f" vs {competitors}"
        
        state.add_message("system", f"Starting multi-agent analysis for: {task}")
        
        state = self.competitive_agent.execute(state, task)
        
        state = self.sentiment_agent.execute(state, task)
        
        state = self.strategy_agent.execute(state, task)
        
        state.add_message("system", "Multi-agent analysis complete")
        
        report = self.generate_final_report(state, product_name)
        
        return report
    
    def generate_final_report(self, state: AgentState, product_name: str) -> Dict:
        return {
            "product_name": product_name,
            "analysis_timestamp": datetime.now().isoformat(),
            "executive_summary": self.create_executive_summary(state),
            "competitive_intelligence": state.competitor_data,
            "sentiment_analysis": state.sentiment_data,
            "launch_strategy": state.recommendations,
            "agent_logs": state.messages,
            "data_sources": {
                "search_results_count": len(state.search_results),
                "scraped_pages_count": len(state.scraped_data),
                "sentiment_samples": state.sentiment_data.get('total_samples', 0)
            }
        }
    
    def create_executive_summary(self, state: AgentState) -> Dict:
        competitor_data = state.competitor_data
        sentiment_data = state.sentiment_data
        recommendations = state.recommendations
        
        summary = {
            "overview": "",
            "key_insights": [],
            "top_recommendations": []
        }
        
        competitors_analyzed = competitor_data.get('competitors_analyzed', 0)
        overall_sentiment = sentiment_data.get('overall_sentiment', 'neutral')
        readiness = recommendations.get('launch_readiness', {})
        readiness_level = readiness.get('readiness_level', 'Medium')
        
        summary["overview"] = (
            f"Analysis of {competitors_analyzed} competitors with {overall_sentiment} market sentiment. "
            f"Launch readiness assessed as {readiness_level}."
        )
        
        if competitor_data.get('key_findings'):
            summary["key_insights"].extend(competitor_data['key_findings'])
        
        if sentiment_data.get('insights'):
            summary["key_insights"].extend(sentiment_data['insights'])
        
        if recommendations.get('key_recommendations'):
            summary["top_recommendations"] = recommendations['key_recommendations'][:5]
        
        return summary
