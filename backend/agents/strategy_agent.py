from .base_agent import BaseAgent, AgentState
from typing import Dict, List


class LaunchStrategyAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="StrategyAdvisor",
            role="Launch Strategy Consultant"
        )
    
    def execute(self, state: AgentState, task: str) -> AgentState:
        self.log_action(state, "Synthesizing insights for launch strategy")
        
        competitor_data = state.competitor_data
        sentiment_data = state.sentiment_data
        
        strategy = self.generate_strategy(task, competitor_data, sentiment_data)
        state.recommendations = strategy
        
        self.log_action(state, "Launch strategy recommendations generated")
        
        return state
    
    def generate_strategy(self, task: str, competitor_data: Dict, sentiment_data: Dict) -> Dict:
        recommendations = {
            "launch_readiness": self.assess_launch_readiness(competitor_data, sentiment_data),
            "positioning_strategy": self.create_positioning_strategy(competitor_data, sentiment_data),
            "key_recommendations": self.generate_recommendations(competitor_data, sentiment_data),
            "risk_assessment": self.assess_risks(competitor_data, sentiment_data),
            "timeline_suggestion": self.suggest_timeline(sentiment_data)
        }
        
        return recommendations
    
    def assess_launch_readiness(self, competitor_data: Dict, sentiment_data: Dict) -> Dict:
        score = 0
        factors = []
        
        if competitor_data:
            competitors_count = competitor_data.get('competitors_analyzed', 0)
            if competitors_count > 0:
                score += 30
                factors.append(f"Analyzed {competitors_count} competitors")
        
        if sentiment_data:
            overall_sentiment = sentiment_data.get('overall_sentiment', 'neutral')
            if overall_sentiment == 'positive':
                score += 40
                factors.append("Positive market sentiment detected")
            elif overall_sentiment == 'neutral':
                score += 25
                factors.append("Neutral market sentiment")
            else:
                score += 10
                factors.append("Negative sentiment - caution advised")
        
        score += 30
        factors.append("Basic market research completed")
        
        readiness_level = "High" if score >= 70 else "Medium" if score >= 40 else "Low"
        
        return {
            "readiness_score": score,
            "readiness_level": readiness_level,
            "contributing_factors": factors
        }
    
    def create_positioning_strategy(self, competitor_data: Dict, sentiment_data: Dict) -> Dict:
        strategy = {
            "differentiation_opportunities": [],
            "target_positioning": "",
            "messaging_focus": []
        }
        
        if competitor_data:
            competitors_count = competitor_data.get('competitors_analyzed', 0)
            if competitors_count > 0:
                strategy["differentiation_opportunities"].append(
                    f"Differentiate from {competitors_count} identified competitors"
                )
                strategy["target_positioning"] = "Position as modern alternative with unique features"
        
        if sentiment_data:
            overall_sentiment = sentiment_data.get('overall_sentiment', 'neutral')
            if overall_sentiment == 'positive':
                strategy["messaging_focus"].append("Amplify existing positive sentiment")
                strategy["messaging_focus"].append("Leverage community enthusiasm")
            else:
                strategy["messaging_focus"].append("Address pain points and concerns")
                strategy["messaging_focus"].append("Build trust through transparency")
        
        if not strategy["differentiation_opportunities"]:
            strategy["differentiation_opportunities"].append("Focus on unique value proposition")
        
        if not strategy["target_positioning"]:
            strategy["target_positioning"] = "Position as innovative solution in the market"
        
        return strategy
    
    def generate_recommendations(self, competitor_data: Dict, sentiment_data: Dict) -> List[str]:
        recommendations = []
        
        if competitor_data:
            competitors_count = competitor_data.get('competitors_analyzed', 0)
            if competitors_count > 2:
                recommendations.append("Conduct deeper competitive analysis to identify gaps")
            
            key_findings = competitor_data.get('key_findings', [])
            if key_findings:
                recommendations.append("Leverage competitor insights for pricing strategy")
        
        if sentiment_data:
            sentiment = sentiment_data.get('overall_sentiment', 'neutral')
            distribution = sentiment_data.get('sentiment_distribution', {})
            
            if sentiment == 'positive':
                recommendations.append("Capitalize on positive sentiment with early launch")
            elif sentiment == 'negative':
                recommendations.append("Address negative feedback before launch")
                recommendations.append("Consider soft launch to test messaging")
            
            negative_count = distribution.get('negative', 0)
            if negative_count > 0:
                recommendations.append("Prepare FAQ addressing common concerns")
        
        recommendations.append("Build pre-launch email list and community")
        recommendations.append("Create content marketing strategy")
        recommendations.append("Plan influencer outreach campaign")
        
        return recommendations[:7]
    
    def assess_risks(self, competitor_data: Dict, sentiment_data: Dict) -> List[str]:
        risks = []
        
        if competitor_data:
            competitors_count = competitor_data.get('competitors_analyzed', 0)
            if competitors_count > 3:
                risks.append("High competition - differentiation critical")
        
        if sentiment_data:
            sentiment = sentiment_data.get('overall_sentiment', 'neutral')
            distribution = sentiment_data.get('sentiment_distribution', {})
            
            negative_percent = 0
            total = sum(distribution.values())
            if total > 0:
                negative_percent = (distribution.get('negative', 0) / total) * 100
            
            if negative_percent > 30:
                risks.append("Significant negative sentiment detected")
            
            if sentiment == 'neutral':
                risks.append("Lack of strong market enthusiasm")
        
        if not risks:
            risks.append("Low risk - market conditions favorable")
        
        return risks
    
    def suggest_timeline(self, sentiment_data: Dict) -> Dict:
        timeline = {
            "recommended_launch_window": "",
            "phases": []
        }
        
        if sentiment_data:
            sentiment = sentiment_data.get('overall_sentiment', 'neutral')
            
            if sentiment == 'positive':
                timeline["recommended_launch_window"] = "2-4 weeks (fast track)"
                timeline["phases"] = [
                    "Week 1-2: Finalize product and messaging",
                    "Week 3: Soft launch to early adopters",
                    "Week 4: Full public launch"
                ]
            else:
                timeline["recommended_launch_window"] = "6-8 weeks (gradual approach)"
                timeline["phases"] = [
                    "Week 1-3: Address feedback and refine product",
                    "Week 4-5: Beta testing with select users",
                    "Week 6-7: Build marketing momentum",
                    "Week 8: Official launch"
                ]
        else:
            timeline["recommended_launch_window"] = "4-6 weeks (standard)"
            timeline["phases"] = [
                "Week 1-2: Market research and positioning",
                "Week 3-4: Pre-launch marketing",
                "Week 5-6: Launch execution"
            ]
        
        return timeline
