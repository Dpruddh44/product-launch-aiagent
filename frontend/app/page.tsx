'use client';

import { useState } from 'react';
import axios from 'axios';
import { Sparkles, TrendingUp, Target, Clock, AlertCircle, Loader2 } from 'lucide-react';
import styles from './page.module.css';

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
        competitors: competitors || ''
      }, { timeout: 45000 });

      setReport(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Analysis taking too long. Try simpler queries.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className={styles.main}>
      <div className={styles.container}>
        {/* Header */}
        <header className={styles.header}>
          <div className={styles.logo}>
            <Sparkles className={styles.icon} size={40} />
            <h1>Launch Intelligence</h1>
          </div>
          <p className={styles.subtitle}>AI Multi-Agent Analysis Platform</p>
        </header>

        {/* Input Form */}
        <div className={styles.formCard}>
          <div className={styles.formGroup}>
            <label className={styles.label}>Product Name *</label>
            <input
              type="text"
              value={productName}
              onChange={(e) => setProductName(e.target.value)}
              placeholder="Notion, Slack, Figma..."
              className={styles.input}
              disabled={loading}
            />
          </div>

          <div className={styles.formGroup}>
            <label className={styles.label}>Competitors (Optional)</label>
            <input
              type="text"
              value={competitors}
              onChange={(e) => setCompetitors(e.target.value)}
              placeholder="Obsidian, Roam Research..."
              className={styles.input}
              disabled={loading}
            />
          </div>

          {error && (
            <div className={styles.errorCard}>
              <AlertCircle size={20} />
              <span>{error}</span>
            </div>
          )}

          <button 
            onClick={analyzeProduct}
            disabled={loading || !productName.trim()}
            className={`${styles.analyzeBtn} ${loading ? styles.loading : ''}`}
          >
            {loading ? (
              <>
                <Loader2 className="animate-spin" size={24} />
                <span>Analyzing...</span>
              </>
            ) : (
              <>
                <Sparkles size={24} />
                <span>Analyze Launch Strategy</span>
              </>
            )}
          </button>
        </div>

        {/* Results */}
        {report && (
          <div className={styles.results}>
            <div className={styles.summaryCard}>
              <div className={styles.cardHeader}>
                <Target size={28} />
                <h2>Executive Summary</h2>
              </div>
              <p>{report.executive_summary?.overview}</p>
              
              {report.executive_summary?.key_insights?.length > 0 && (
                <div className={styles.insights}>
                  {report.executive_summary.key_insights.slice(0, 4).map((insight: string, i: number) => (
                    <div key={i} className={styles.insightItem}>
                      <div className={styles.bullet}></div>
                      <span>{insight}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className={styles.statsGrid}>
              <div className={`${styles.statCard} ${styles.cardHover}`}>
                <TrendingUp size={28} />
                <h3>Launch Readiness</h3>
                <div className={styles.statValue}>
                  {report.launch_strategy?.launch_readiness?.readiness_level || 'Medium'}
                </div>
                <small>{report.launch_strategy?.launch_readiness?.readiness_score}/100</small>
              </div>

              <div className={`${styles.statCard} ${styles.cardHover}`}>
                <Sparkles size={28} />
                <h3>Market Sentiment</h3>
                <div className={styles.statValue}>
                  {report.sentiment_analysis?.overall_sentiment || 'Neutral'}
                </div>
                <small>{report.sentiment_analysis?.total_samples || 0} samples</small>
              </div>

              <div className={`${styles.statCard} ${styles.cardHover}`}>
                <Target size={28} />
                <h3>Competitors</h3>
                <div className={styles.statValue}>
                  {report.competitive_intelligence?.competitors_analyzed || 0}
                </div>
                <small>Analyzed</small>
              </div>
            </div>

            {report.executive_summary?.top_recommendations?.length > 0 && (
              <div className={styles.recommendationsCard}>
                <div className={styles.cardHeader}>
                  <Clock size={28} />
                  <h2>Top Recommendations</h2>
                </div>
                <div className={styles.recList}>
                  {report.executive_summary.top_recommendations.slice(0, 5).map((rec: string, i: number) => (
                    <div key={i} className={`${styles.recItem} ${styles.cardHover}`}>
                      <span className={styles.recNumber}>{i + 1}</span>
                      <p>{rec}</p>
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
