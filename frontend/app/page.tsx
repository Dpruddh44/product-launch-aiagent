'use client';

import { useState } from 'react';
import axios from 'axios';
import { Sparkles, TrendingUp, Target, Clock, AlertCircle, Loader2 } from 'lucide-react';

export default function Home() {
  const [productName, setProductName] = useState('');
  const [competitors, setCompetitors] = useState('');
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState<any>(null);
  const [error, setError] = useState('');

  const analyzeProduct = async () => {
    if (!productName.trim()) {
      setError('Please enter a product name');
      return;
    }

    setLoading(true);
    setError('');
    setReport(null);

    try {
      const response = await axios.post('http://localhost:8000/analyze-product-launch', {
        product_name: productName,
        competitors: competitors
      });

      setReport(response.data);
    } catch (err) {
      setError('Failed to analyze product. Please check if the backend is running.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-black text-white p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12 mt-8">
          <div className="flex items-center justify-center mb-4">
            <Sparkles className="w-8 h-8 text-gold-400 mr-3" />
            <h1 className="text-5xl font-bold bg-gradient-to-r from-gold-300 via-gold-400 to-gold-500 bg-clip-text text-transparent gold-text-glow">
              Launch Intelligence
            </h1>
          </div>
          <p className="text-gray-400 text-lg">
            AI-Powered Multi-Agent Analysis Platform
          </p>
        </div>

        {/* Input Section */}
        <div className="bg-gradient-to-br from-gray-900 to-black border border-gold-500/20 rounded-2xl p-8 mb-8 gold-glow">
          <div className="space-y-6">
            <div>
              <label className="block text-gold-400 font-semibold mb-3 text-sm uppercase tracking-wide">
                Product Name *
              </label>
              <input
                type="text"
                value={productName}
                onChange={(e) => setProductName(e.target.value)}
                placeholder="Enter product name (e.g., Notion, Slack)"
                className="w-full px-6 py-4 bg-black border-2 border-gold-500/30 rounded-xl text-white placeholder-gray-500 focus:border-gold-400 focus:outline-none focus:ring-2 focus:ring-gold-400/20 transition-all"
                disabled={loading}
              />
            </div>

            <div>
              <label className="block text-gold-400 font-semibold mb-3 text-sm uppercase tracking-wide">
                Competitors (Optional)
              </label>
              <input
                type="text"
                value={competitors}
                onChange={(e) => setCompetitors(e.target.value)}
                placeholder="Enter competitors (e.g., Obsidian, Roam Research)"
                className="w-full px-6 py-4 bg-black border-2 border-gold-500/30 rounded-xl text-white placeholder-gray-500 focus:border-gold-400 focus:outline-none focus:ring-2 focus:ring-gold-400/20 transition-all"
                disabled={loading}
              />
            </div>

            {error && (
              <div className="flex items-center gap-2 bg-red-900/20 border border-red-500/30 rounded-lg p-4">
                <AlertCircle className="w-5 h-5 text-red-400" />
                <p className="text-red-400">{error}</p>
              </div>
            )}

            <button
              onClick={analyzeProduct}
              disabled={loading}
              className="w-full bg-gradient-to-r from-gold-500 to-gold-600 hover:from-gold-400 hover:to-gold-500 text-black font-bold py-4 px-8 rounded-xl transition-all transform hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-3 shadow-lg shadow-gold-500/50"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Analyzing...
                </>
              ) : (
                <>
                  <Sparkles className="w-5 h-5" />
                  Analyze Product Launch
                </>
              )}
            </button>
          </div>
        </div>

        {/* Results Section */}
        {report && (
          <div className="space-y-6 animate-fadeIn">
            {/* Executive Summary */}
            <div className="bg-gradient-to-br from-gold-900/20 to-black border-2 border-gold-500/30 rounded-2xl p-8 gold-glow">
              <h2 className="text-2xl font-bold text-gold-400 mb-4 flex items-center gap-2">
                <Target className="w-6 h-6" />
                Executive Summary
              </h2>
              <p className="text-gray-300 text-lg leading-relaxed mb-6">
                {report.executive_summary?.overview}
              </p>
              
              {report.executive_summary?.key_insights && report.executive_summary.key_insights.length > 0 && (
                <div className="space-y-2">
                  <h3 className="text-gold-300 font-semibold mb-3">Key Insights:</h3>
                  {report.executive_summary.key_insights.map((insight: string, idx: number) => (
                    <div key={idx} className="flex items-start gap-3 bg-black/40 p-4 rounded-lg border border-gold-500/10">
                      <div className="w-2 h-2 rounded-full bg-gold-400 mt-2"></div>
                      <p className="text-gray-300">{insight}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <StatCard
                icon={<TrendingUp className="w-6 h-6" />}
                title="Launch Readiness"
                value={report.launch_strategy?.launch_readiness?.readiness_level || 'N/A'}
                subtitle={`Score: ${report.launch_strategy?.launch_readiness?.readiness_score || 0}/100`}
              />
              <StatCard
                icon={<Sparkles className="w-6 h-6" />}
                title="Market Sentiment"
                value={report.sentiment_analysis?.overall_sentiment || 'N/A'}
                subtitle={`${report.sentiment_analysis?.total_samples || 0} samples analyzed`}
              />
              <StatCard
                icon={<Target className="w-6 h-6" />}
                title="Competitors"
                value={report.competitive_intelligence?.competitors_analyzed || 0}
                subtitle="Companies analyzed"
              />
            </div>

            {/* Recommendations */}
            {report.executive_summary?.top_recommendations && (
              <div className="bg-gradient-to-br from-gray-900 to-black border border-gold-500/20 rounded-2xl p-8">
                <h2 className="text-2xl font-bold text-gold-400 mb-6 flex items-center gap-2">
                  <Clock className="w-6 h-6" />
                  Top Recommendations
                </h2>
                <div className="space-y-3">
                  {report.executive_summary.top_recommendations.map((rec: string, idx: number) => (
                    <div key={idx} className="flex items-start gap-4 bg-black/60 p-5 rounded-xl border border-gold-500/10 hover:border-gold-500/30 transition-all">
                      <span className="flex-shrink-0 w-8 h-8 rounded-full bg-gold-500 text-black font-bold flex items-center justify-center">
                        {idx + 1}
                      </span>
                      <p className="text-gray-300 pt-1">{rec}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </main>
  );
}

function StatCard({ icon, title, value, subtitle }: any) {
  return (
    <div className="bg-gradient-to-br from-gray-900 to-black border border-gold-500/20 rounded-xl p-6 hover:border-gold-500/40 transition-all">
      <div className="flex items-center gap-3 mb-3">
        <div className="text-gold-400">{icon}</div>
        <h3 className="text-gray-400 text-sm uppercase tracking-wide">{title}</h3>
      </div>
      <p className="text-3xl font-bold text-white mb-1 capitalize">{value}</p>
      <p className="text-gray-500 text-sm">{subtitle}</p>
    </div>
  );
}
