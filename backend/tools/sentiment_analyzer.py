from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import Dict, List
from datetime import datetime


class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
    
    def analyze_text(self, text: str) -> Dict:
        scores = self.analyzer.polarity_scores(text)
        
        if scores['compound'] >= 0.05:
            sentiment = "positive"
        elif scores['compound'] <= -0.05:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        return {
            "text": text,
            "sentiment": sentiment,
            "scores": {
                "positive": scores['pos'],
                "negative": scores['neg'],
                "neutral": scores['neu'],
                "compound": scores['compound']
            },
            "timestamp": datetime.now().isoformat()
        }
    
    def analyze_batch(self, texts: List[str]) -> List[Dict]:
        results = []
        for text in texts:
            results.append(self.analyze_text(text))
        return results
    
    def get_overall_sentiment(self, texts: List[str]) -> Dict:
        analyses = self.analyze_batch(texts)
        
        total_compound = sum(a['scores']['compound'] for a in analyses)
        avg_compound = total_compound / len(analyses) if analyses else 0
        
        sentiment_counts = {
            "positive": sum(1 for a in analyses if a['sentiment'] == 'positive'),
            "negative": sum(1 for a in analyses if a['sentiment'] == 'negative'),
            "neutral": sum(1 for a in analyses if a['sentiment'] == 'neutral')
        }
        
        return {
            "total_analyzed": len(analyses),
            "average_compound_score": avg_compound,
            "sentiment_distribution": sentiment_counts,
            "overall_sentiment": "positive" if avg_compound >= 0.05 else "negative" if avg_compound <= -0.05 else "neutral"
        }
