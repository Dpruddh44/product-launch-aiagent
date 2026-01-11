from .base_agent import BaseAgent, AgentState
from tools.sentiment_analyzer import SentimentAnalyzer
from tools.reddit_scraper import RedditScraper
from typing import Dict, List


class SentimentAnalysisAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="SentimentAnalyzer",
            role="Social Media Sentiment Analyst"
        )
        self.sentiment_tool = SentimentAnalyzer()
        self.reddit_scraper = RedditScraper()
    
    def execute(self, state: AgentState, task: str) -> AgentState:
        self.log_action(state, f"Starting sentiment analysis for: {task}")
        
        keywords = self.extract_keywords(task)
        
        all_texts = []
        
        for keyword in keywords:
            self.log_action(state, f"Collecting social media data for: {keyword}")
            
            reddit_posts = self.reddit_scraper.search_posts(keyword, limit=5)
            
            for post in reddit_posts:
                if post.get('title'):
                    all_texts.append(post['title'])
                if post.get('text') and len(post['text']) > 10:
                    all_texts.append(post['text'])
                
                comments = self.reddit_scraper.get_comments(post.get('url', ''), limit=10)
                all_texts.extend(comments)
        
        if not all_texts:
            all_texts = [
                f"Sample positive text about {task}",
                f"Sample negative feedback regarding {task}",
                f"Neutral opinion on {task}"
            ]
            self.log_action(state, "No social media data available, using sample texts")
        
        self.log_action(state, f"Analyzing sentiment for {len(all_texts)} text samples")
        
        sentiment_results = self.sentiment_tool.analyze_batch(all_texts[:50])
        overall_sentiment = self.sentiment_tool.get_overall_sentiment(all_texts[:50])
        
        analysis = self.create_sentiment_report(sentiment_results, overall_sentiment, keywords)
        state.sentiment_data = analysis
        
        self.log_action(state, f"Sentiment analysis complete: {overall_sentiment['overall_sentiment']}")
        
        return state
    
    def extract_keywords(self, task: str) -> List[str]:
        words = task.lower().split()
        
        stop_words = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'vs', 'versus']
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        
        return keywords[:3]
    
    def create_sentiment_report(self, results: List[Dict], overall: Dict, keywords: List[str]) -> Dict:
        positive_samples = [r for r in results if r['sentiment'] == 'positive']
        negative_samples = [r for r in results if r['sentiment'] == 'negative']
        
        return {
            "keywords_analyzed": keywords,
            "total_samples": overall['total_analyzed'],
            "overall_sentiment": overall['overall_sentiment'],
            "sentiment_distribution": overall['sentiment_distribution'],
            "average_score": overall['average_compound_score'],
            "positive_mentions": len(positive_samples),
            "negative_mentions": len(negative_samples),
            "sample_positive_comments": [p['text'][:100] for p in positive_samples[:3]],
            "sample_negative_comments": [n['text'][:100] for n in negative_samples[:3]],
            "insights": self.generate_insights(overall)
        }
    
    def generate_insights(self, overall: Dict) -> List[str]:
        insights = []
        
        sentiment = overall['overall_sentiment']
        distribution = overall['sentiment_distribution']
        
        if sentiment == 'positive':
            insights.append("Overall sentiment is positive - strong market reception")
        elif sentiment == 'negative':
            insights.append("Overall sentiment is negative - potential concerns to address")
        else:
            insights.append("Overall sentiment is neutral - mixed market reception")
        
        total = distribution['positive'] + distribution['negative'] + distribution['neutral']
        if total > 0:
            pos_percent = (distribution['positive'] / total) * 100
            neg_percent = (distribution['negative'] / total) * 100
            
            insights.append(f"{pos_percent:.1f}% positive mentions, {neg_percent:.1f}% negative mentions")
        
        return insights
