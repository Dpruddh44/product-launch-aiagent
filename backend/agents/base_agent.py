from typing import Dict, List, Any, Optional
from datetime import datetime


class AgentState:
    def __init__(self):
        self.messages: List[Dict] = []
        self.competitor_data: Dict = {}
        self.sentiment_data: Dict = {}
        self.recommendations: Dict = {}
        self.search_results: List[Dict] = []
        self.scraped_data: List[Dict] = []
        self.timestamp = datetime.now().isoformat()
    
    def add_message(self, role: str, content: str):
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def to_dict(self) -> Dict:
        return {
            "messages": self.messages,
            "competitor_data": self.competitor_data,
            "sentiment_data": self.sentiment_data,
            "recommendations": self.recommendations,
            "search_results": self.search_results,
            "scraped_data": self.scraped_data,
            "timestamp": self.timestamp
        }


class BaseAgent:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
    
    def execute(self, state: AgentState, task: str) -> AgentState:
        raise NotImplementedError("Each agent must implement execute method")
    
    def log_action(self, state: AgentState, action: str):
        state.add_message(
            role=self.name,
            content=f"[{self.role}] {action}"
        )
