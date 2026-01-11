from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from config import settings
from tools.sentiment_analyzer import SentimentAnalyzer
from tools.web_scraper import WebScraper
from tools.search_tool import SearchTool
from agents.competitive_research_agent import CompetitiveResearchAgent
from agents.base_agent import AgentState
from agents.sentiment_agent import SentimentAnalysisAgent
from agents.strategy_agent import LaunchStrategyAgent
from agents.orchestrator import AgentOrchestrator
from pydantic import BaseModel
class AnalysisRequest(BaseModel):
    product_name: str
    competitors: str = ""








app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message":  "This product is amazing! I love it!",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

@app.post("/test-sentiment")
async def test_sentiment(texts: List[str]):
    analyzer = SentimentAnalyzer()
    results = analyzer.analyze_batch(texts)
    overall = analyzer.get_overall_sentiment(texts)
    
    return {
        "individual_results": results,
        "overall_analysis": overall
    }
@app.post("/test-scraper")
async def test_scraper(url: str):
    scraper = WebScraper()
    result = scraper.extract_product_info(url)
    return result


@app.post("/test-search")
async def test_search(query: str):
    searcher = SearchTool()
    results = searcher.search(query)
    return {"query": query, "results": results}

@app.post("/test-competitive-agent")
async def test_competitive_agent(task: str):
    state = AgentState()
    agent = CompetitiveResearchAgent()
    
    result_state = agent.execute(state, task)
    
    return result_state.to_dict()

@app.post("/test-sentiment-agent")
async def test_sentiment_agent(task: str):
    state = AgentState()
    agent = SentimentAnalysisAgent()
    
    result_state = agent.execute(state, task)
    
    return result_state.to_dict()


@app.post("/test-strategy-agent")
async def test_strategy_agent(task: str):
    state = AgentState()
    
    competitive_agent = CompetitiveResearchAgent()
    state = competitive_agent.execute(state, task)
    
    sentiment_agent = SentimentAnalysisAgent()
    state = sentiment_agent.execute(state, task)
    
    strategy_agent = LaunchStrategyAgent()
    state = strategy_agent.execute(state, task)
    
    return state.to_dict()

@app.post("/analyze-product-launch")
async def analyze_product_launch(request: AnalysisRequest):
    orchestrator = AgentOrchestrator()
    
    report = orchestrator.run_analysis(
        product_name=request.product_name,
        competitors=request.competitors
    )
    
    return report

@app.post("/quick-analysis")
async def quick_analysis(product_name: str):
    orchestrator = AgentOrchestrator()
    report = orchestrator.run_analysis(product_name)
    
    return {
        "product": product_name,
        "executive_summary": report["executive_summary"],
        "launch_readiness": report["launch_strategy"]["launch_readiness"],
        "top_recommendations": report["launch_strategy"]["key_recommendations"][:3],
        "sentiment": report["sentiment_analysis"]["overall_sentiment"],
        "competitors_analyzed": report["competitive_intelligence"]["competitors_analyzed"]
    }

