import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="BRBAS", layout="wide", page_icon="📊", initial_sidebar_state="expanded")

# Professional CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 0;
    }
    
    .block-container {
        padding: 2rem 3rem;
        max-width: 1600px;
    }
    
    .brbas-header {
        text-align: center;
        padding: 2rem 0 1.5rem 0;
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        margin: -2rem -3rem 2rem -3rem;
        box-shadow: 0 4px 20px rgba(30, 64, 175, 0.15);
    }
    
    .brbas-title {
        font-size: 3rem;
        font-weight: 800;
        color: white;
        letter-spacing: 0.5rem;
        margin: 0;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    
    .search-bar-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
        margin-bottom: 2rem;
        display: flex;
        gap: 1rem;
        align-items: center;
    }
    
    .confidence-card {
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        border-left: 6px solid #3b82f6;
        margin: 2rem 0;
    }
    
    .confidence-score {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1;
        margin: 0;
    }
    
    .recommendation-badge {
        display: inline-block;
        padding: 0.75rem 2rem;
        border-radius: 50px;
        font-weight: 700;
        font-size: 1.2rem;
        margin: 1rem 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .strong-buy {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
    }
    
    .buy {
        background: linear-gradient(135deg, #34d399 0%, #10b981 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(52, 211, 153, 0.3);
    }
    
    .hold {
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(251, 191, 36, 0.3);
    }
    
    .sell {
        background: linear-gradient(135deg, #f87171 0%, #ef4444 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(248, 113, 113, 0.3);
    }
    
    .strong-sell {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3);
    }
    
    .advice-text {
        font-size: 1.1rem;
        line-height: 1.8;
        color: #334155;
        margin: 1.5rem 0;
        font-weight: 500;
    }
    
    .company-header {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(30, 64, 175, 0.2);
    }
    
    .company-name {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0 0 0.5rem 0;
        color: white;
    }
    
    .company-description {
        font-size: 1rem;
        line-height: 1.6;
        margin: 1rem 0;
        opacity: 0.95;
    }
    
    .tag {
        display: inline-block;
        padding: 0.4rem 1rem;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        margin-right: 0.5rem;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .section-header {
        font-size: 1.75rem;
        font-weight: 700;
        color: #1e293b;
        margin: 3rem 0 1.5rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 3px solid #3b82f6;
    }
    
    .stMetric {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        border: 1px solid #e2e8f0;
    }
    
    .stMetric label {
        color: #64748b !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #1e293b !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e40af 0%, #1e3a8a 100%);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white !important;
    }
    
    [data-testid="stSidebar"] button {
        width: 100%;
        background: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 0.75rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        font-weight: 600;
        transition: all 0.2s;
    }
    
    [data-testid="stSidebar"] button:hover {
        background: rgba(255, 255, 255, 0.2);
        border-color: rgba(255, 255, 255, 0.4);
        transform: translateX(5px);
    }
    
    /* Micro-interactions and Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
    }
    
    @keyframes shimmer {
        0% {
            background-position: -1000px 0;
        }
        100% {
            background-position: 1000px 0;
        }
    }
    
    .company-header {
        animation: fadeInUp 0.6s ease-out;
    }
    
    .stMetric {
        animation: fadeInUp 0.4s ease-out;
        animation-fill-mode: both;
    }
    
    .stMetric:nth-child(1) { animation-delay: 0.1s; }
    .stMetric:nth-child(2) { animation-delay: 0.2s; }
    .stMetric:nth-child(3) { animation-delay: 0.3s; }
    .stMetric:nth-child(4) { animation-delay: 0.4s; }
    .stMetric:nth-child(5) { animation-delay: 0.5s; }
    
    .stMetric:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .confidence-card {
        animation: fadeInUp 0.7s ease-out;
        transition: all 0.3s ease;
    }
    
    .confidence-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 36px rgba(0, 0, 0, 0.15);
    }
    
    .confidence-score {
        animation: pulse 2s ease-in-out infinite;
    }
    
    .recommendation-badge {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: default;
    }
    
    .recommendation-badge:hover {
        transform: scale(1.1);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
    }
    
    .company-name {
        transition: all 0.3s ease;
    }
    
    .company-name:hover {
        transform: scale(1.02);
        text-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    .tag {
        transition: all 0.2s ease;
        cursor: pointer;
    }
    
    .tag:hover {
        background: rgba(255, 255, 255, 0.35);
        transform: translateY(-2px);
    }
    
    .section-header {
        animation: slideIn 0.5s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, #3b82f6, transparent);
        animation: shimmer 2s linear infinite;
    }
    
    .stTextInput input:focus,
    .stSelectbox select:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        transform: scale(1.01);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .stButton button {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
    }
    
    .stButton button:active {
        transform: translateY(0);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    .stButton button::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton button:hover::after {
        width: 300px;
        height: 300px;
    }
    
    .stDataFrame {
        animation: fadeInUp 0.5s ease-out;
        transition: all 0.3s ease;
    }
    
    .stDataFrame:hover {
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    
    .stExpander {
        transition: all 0.3s ease;
    }
    
    .stExpander:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(59, 130, 246, 0.05);
        border-color: #3b82f6;
    }
    
    /* Loading shimmer effect */
    .loading-shimmer {
        background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
        background-size: 1000px 100%;
        animation: shimmer 2s linear infinite;
    }
    
    /* Smooth page transitions */
    .main > div {
        animation: fadeInUp 0.4s ease-out;
    }
    
    /* Interactive chart container */
    .stPlotlyChart {
        animation: fadeInUp 0.6s ease-out;
        transition: all 0.3s ease;
    }
    
    .stPlotlyChart:hover {
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
        transform: scale(1.01);
    }
    
    /* Tooltip enhancement */
    [data-testid="stTooltipIcon"] {
        transition: all 0.2s ease;
    }
    
    [data-testid="stTooltipIcon"]:hover {
        transform: scale(1.2) rotate(15deg);
    }
    
    /* Card hover effects */
    div[style*='background: white'][style*='padding: 1.5rem'] {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    div[style*='background: white'][style*='padding: 1.5rem']:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.15);
    }
    
    /* Success/Error message animations */
    .stSuccess, .stError, .stWarning, .stInfo {
        animation: slideIn 0.4s ease-out;
    }
    
    /* Smooth scrolling */
    html {
        scroll-behavior: smooth;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'analysis'
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []

# Sidebar Navigation
with st.sidebar:
    st.markdown("<h1 style='color: white; text-align: center; margin-bottom: 2rem;'>BRBAS</h1>", unsafe_allow_html=True)
    
    if st.button("📊 Stock Analysis"):
        st.session_state.page = 'analysis'
    if st.button("⚖️ Compare Stocks"):
        st.session_state.page = 'compare'
    if st.button("⭐ Portfolio"):
        st.session_state.page = 'portfolio'
    
    st.markdown("---")
    st.markdown("<p style='color: rgba(255,255,255,0.7); font-size: 0.85rem; text-align: center;'>Professional Stock Analysis Platform</p>", unsafe_allow_html=True)

# Helper functions
def search_ticker(query):
    """Search for ticker by company name"""
    try:
        # Common stock mappings
        mapping = {
            'apple': 'AAPL', 'microsoft': 'MSFT', 'google': 'GOOGL', 'amazon': 'AMZN',
            'tesla': 'TSLA', 'meta': 'META', 'nvidia': 'NVDA', 'netflix': 'NFLX',
            'disney': 'DIS', 'walmart': 'WMT', 'coca cola': 'KO', 'pepsi': 'PEP'
        }
        
        query_lower = query.lower()
        if query_lower in mapping:
            return mapping[query_lower]
        return query.upper()
    except:
        return query.upper()

def calculate_confidence_score(info, data, valuation_score, momentum_score, earnings_score, technical_score):
    weights = {
        'valuation': 0.30,
        'momentum': 0.25,
        'earnings': 0.25,
        'technical': 0.20
    }
    
    val_normalized = ((valuation_score + 6) / 12) * 100
    mom_normalized = ((momentum_score + 6) / 12) * 100
    earn_normalized = ((earnings_score + 6) / 12) * 100
    tech_normalized = ((technical_score + 6) / 12) * 100
    
    confidence = (
        val_normalized * weights['valuation'] +
        mom_normalized * weights['momentum'] +
        earn_normalized * weights['earnings'] +
        tech_normalized * weights['technical']
    )
    
    return round(confidence, 1)

def get_recommendation_from_confidence(confidence):
    if confidence >= 75:
        return "STRONG BUY", "strong-buy"
    elif confidence >= 60:
        return "BUY", "buy"
    elif confidence >= 40:
        return "HOLD", "hold"
    elif confidence >= 25:
        return "SELL", "sell"
    else:
        return "STRONG SELL", "strong-sell"

def generate_detailed_advice(confidence, recommendation, ticker, info, valuation_score, momentum_score, earnings_score, technical_score, valuation_details, momentum_details, earnings_details, technical_details):
    """Generate comprehensive analytical advice"""
    company_name = info.get('longName', ticker)
    
    # Base recommendation
    if confidence >= 75:
        base = f"Considering {company_name}'s strong fundamentals, positive momentum indicators, and robust earnings trajectory, I recommend **accumulating a position** in {ticker}. The data suggests significant upside potential with manageable risk."
    elif confidence >= 60:
        base = f"Based on {company_name}'s favorable valuation metrics and positive technical indicators, I recommend **initiating or adding to a position** in {ticker}. Monitor for any changes in market conditions."
    elif confidence >= 40:
        base = f"Given {company_name}'s mixed signals across valuation, momentum, and earnings metrics, I recommend **holding existing positions** in {ticker} and waiting for clearer directional signals before making additional moves."
    elif confidence >= 25:
        base = f"Considering {company_name}'s deteriorating fundamentals and weak technical indicators, I recommend **reducing exposure** to {ticker}. Consider reallocating capital to stronger opportunities."
    else:
        base = f"Given {company_name}'s significant headwinds across multiple analysis dimensions, I recommend **exiting positions** in {ticker}. The risk-reward profile is currently unfavorable."
    
    # Detailed breakdown
    analysis = f"\n\n**Detailed Analysis:**\n\n"
    
    # Valuation insights
    analysis += f"**Valuation ({valuation_score+6}/12):** "
    peg = info.get('pegRatio', None)
    pe = info.get('trailingPE', None)
    pb = info.get('priceToBook', None)
    
    if valuation_score >= 2:
        analysis += f"The stock appears undervalued. "
        if peg and peg < 1:
            analysis += f"The PEG ratio of {peg:.2f} indicates the stock is trading below its growth rate, suggesting a compelling value opportunity. "
        if pe and pe < 20:
            analysis += f"With a P/E ratio of {pe:.1f}, the stock is reasonably priced relative to earnings. "
    elif valuation_score <= -2:
        analysis += f"Valuation metrics raise concerns. "
        if peg and peg > 2:
            analysis += f"The PEG ratio of {peg:.2f} suggests the stock is expensive relative to its growth prospects. "
        if pe and pe > 30:
            analysis += f"The elevated P/E ratio of {pe:.1f} indicates premium pricing that may not be justified. "
    else:
        analysis += f"Valuation appears fair. "
    
    # Momentum insights
    analysis += f"\n\n**Momentum ({momentum_score+6}/12):** "
    if momentum_score >= 2:
        analysis += f"Strong bullish momentum is evident. "
        for detail in momentum_details:
            if "Golden Cross" in detail:
                analysis += f"The stock has formed a golden cross pattern with the 50-day moving average crossing above the 200-day MA, a classically bullish technical signal. "
        analysis += f"This suggests institutional accumulation and sustained buying pressure. "
    elif momentum_score <= -2:
        analysis += f"Momentum indicators are concerning. "
        for detail in momentum_details:
            if "Death Cross" in detail:
                analysis += f"A death cross has formed, with the 50-day MA falling below the 200-day MA, signaling potential further downside. "
        analysis += f"This pattern often precedes extended periods of underperformance. "
    
    # Earnings insights
    analysis += f"\n\n**Earnings & Growth ({earnings_score+6}/12):** "
    earnings_growth = info.get('earningsQuarterlyGrowth', None)
    revenue_growth = info.get('revenueGrowth', None)
    profit_margin = info.get('profitMargins', None)
    
    if earnings_score >= 2:
        analysis += f"The company demonstrates strong fundamental health. "
        if earnings_growth and earnings_growth > 0.15:
            analysis += f"Quarterly earnings growth of {earnings_growth*100:.1f}% significantly exceeds market averages, indicating robust business performance. "
        if profit_margin and profit_margin > 0.15:
            analysis += f"Profit margins of {profit_margin*100:.1f}% suggest efficient operations and pricing power. "
    elif earnings_score <= -2:
        analysis += f"Fundamental performance is weak. "
        if earnings_growth and earnings_growth < 0:
            analysis += f"Negative earnings growth of {earnings_growth*100:.1f}% signals operational challenges or market headwinds. "
    
    # Technical insights
    analysis += f"\n\n**Technical Analysis ({technical_score+6}/12):** "
    for detail in technical_details:
        if "Oversold" in detail:
            analysis += f"The RSI indicator shows oversold conditions, which historically precede price reversals and present potential entry opportunities. "
        elif "Overbought" in detail:
            analysis += f"The RSI suggests overbought conditions, indicating the stock may be due for a pullback or consolidation period. "
    
    # Risk factors
    beta = info.get('beta', None)
    if beta:
        if beta > 1.5:
            analysis += f"\n\n**Risk Assessment:** High volatility (Beta: {beta:.2f}) suggests this stock experiences larger price swings than the broader market. Position sizing should reflect this elevated risk profile."
        elif beta < 0.5:
            analysis += f"\n\n**Risk Assessment:** Low volatility (Beta: {beta:.2f}) indicates relative stability, making this suitable for conservative portfolios."
    
    return base + analysis

def calculate_rsi(data, period=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(data, fast=12, slow=26, signal=9):
    exp1 = data['Close'].ewm(span=fast, adjust=False).mean()
    exp2 = data['Close'].ewm(span=slow, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    histogram = macd - signal_line
    return macd, signal_line, histogram

def calculate_ema(data, periods=[8, 21, 50]):
    for period in periods:
        data[f'EMA{period}'] = data['Close'].ewm(span=period, adjust=False).mean()
    return data

def analyze_valuation(info):
    valuation_score = 0
    valuation_details = []
    
    peg = info.get('pegRatio', None)
    if peg and peg > 0:
        if peg < 1:
            valuation_score += 2
            valuation_details.append(f"✓ PEG Ratio: **{peg:.2f}** — Undervalued relative to growth")
        elif peg < 1.5:
            valuation_score += 1
            valuation_details.append(f"○ PEG Ratio: **{peg:.2f}** — Fairly valued")
        elif peg < 2:
            valuation_score -= 1
            valuation_details.append(f"○ PEG Ratio: **{peg:.2f}** — Slightly overvalued")
        else:
            valuation_score -= 2
            valuation_details.append(f"✗ PEG Ratio: **{peg:.2f}** — Significantly overvalued")
    
    pe = info.get('trailingPE', None)
    forward_pe = info.get('forwardPE', None)
    
    if pe and forward_pe and pe > 0 and forward_pe > 0:
        if forward_pe < pe * 0.9:
            valuation_score += 1
            valuation_details.append(f"✓ P/E improving: **{pe:.1f}** → **{forward_pe:.1f}**")
        elif forward_pe > pe * 1.1:
            valuation_score -= 1
            valuation_details.append(f"✗ P/E deteriorating: **{pe:.1f}** → **{forward_pe:.1f}**")
    
    pb = info.get('priceToBook', None)
    if pb and pb > 0:
        if pb < 1:
            valuation_score += 1
            valuation_details.append(f"✓ P/B: **{pb:.2f}** — Trading below book value")
        elif pb > 5:
            valuation_score -= 1
            valuation_details.append(f"✗ P/B: **{pb:.2f}** — Premium valuation")
    
    return valuation_score, valuation_details

def analyze_momentum(data):
    momentum_score = 0
    momentum_details = []
    
    current_price = data['Close'].iloc[-1]
    
    if 'MA50' in data.columns and 'MA200' in data.columns:
        ma50 = data['MA50'].iloc[-1]
        ma200 = data['MA200'].iloc[-1]
        
        if pd.notna(ma50) and pd.notna(ma200):
            if ma50 > ma200 and current_price > ma50:
                momentum_score += 2
                momentum_details.append("✓ **Golden Cross** — Price above 50-MA & 200-MA")
            elif ma50 < ma200 and current_price < ma50:
                momentum_score -= 2
                momentum_details.append("✗ **Death Cross** — Price below 50-MA & 200-MA")
    
    if 'MA20' in data.columns:
        ma20 = data['MA20'].iloc[-1]
        if pd.notna(ma20):
            if current_price > ma20 * 1.03:
                momentum_score += 1
                momentum_details.append(f"✓ Strong momentum: **{((current_price/ma20 - 1)*100):.1f}%** above 20-MA")
            elif current_price < ma20 * 0.97:
                momentum_score -= 1
                momentum_details.append(f"✗ Weak momentum: **{((current_price/ma20 - 1)*100):.1f}%** below 20-MA")
    
    return momentum_score, momentum_details

def analyze_earnings(info):
    earnings_score = 0
    earnings_details = []
    
    earnings_growth = info.get('earningsQuarterlyGrowth', None)
    if earnings_growth:
        if earnings_growth > 0.15:
            earnings_score += 2
            earnings_details.append(f"✓ Earnings growth: **{earnings_growth*100:.1f}%** — Strong")
        elif earnings_growth > 0.05:
            earnings_score += 1
            earnings_details.append(f"○ Earnings growth: **{earnings_growth*100:.1f}%** — Positive")
        elif earnings_growth < -0.10:
            earnings_score -= 2
            earnings_details.append(f"✗ Earnings declining: **{earnings_growth*100:.1f}%**")
    
    revenue_growth = info.get('revenueGrowth', None)
    if revenue_growth:
        if revenue_growth > 0.20:
            earnings_score += 1
            earnings_details.append(f"✓ Revenue growth: **{revenue_growth*100:.1f}%** — Accelerating")
        elif revenue_growth < 0:
            earnings_score -= 1
            earnings_details.append(f"✗ Revenue declining: **{revenue_growth*100:.1f}%**")
    
    return earnings_score, earnings_details

def analyze_technical(data):
    technical_score = 0
    technical_details = []
    
    current_rsi = data['RSI'].iloc[-1] if 'RSI' in data.columns and pd.notna(data['RSI'].iloc[-1]) else None
    if current_rsi:
        if current_rsi < 30:
            technical_score += 2
            technical_details.append(f"✓ RSI: **{current_rsi:.1f}** — Oversold, potential reversal")
        elif current_rsi > 70:
            technical_score -= 2
            technical_details.append(f"✗ RSI: **{current_rsi:.1f}** — Overbought, potential pullback")
        else:
            technical_details.append(f"○ RSI: **{current_rsi:.1f}** — Neutral territory")
    
    if 'MACD' in data.columns and 'Signal' in data.columns:
        current_macd = data['MACD'].iloc[-1]
        current_signal = data['Signal'].iloc[-1]
        
        if pd.notna(current_macd) and pd.notna(current_signal):
            if current_macd > current_signal:
                technical_score += 1
                technical_details.append("✓ **MACD bullish** — Above signal line")
            else:
                technical_score -= 1
                technical_details.append("✗ **MACD bearish** — Below signal line")
    
    return technical_score, technical_details

@st.cache_data(ttl=300)
def get_stock_data(ticker, period):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period=period)
        info = stock.info
        return data, info, None
    except Exception as e:
        return None, None, str(e)

# STOCK ANALYSIS PAGE
if st.session_state.page == 'analysis':
    st.markdown("""
    <div class='brbas-header'>
        <h1 class='brbas-title'>BRBAS</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Search bar in white container
    search_col1, search_col2, search_col3 = st.columns([4, 2, 2])
    
    with search_col1:
        ticker_input = st.text_input("", value="AAPL", placeholder="Enter stock ticker or company name (e.g., AAPL or Apple)", label_visibility="collapsed", key="ticker_search")
        ticker = search_ticker(ticker_input)
    
    with search_col2:
        period = st.selectbox("Time Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3, key="period_select")
    
    with search_col3:
        analysis_depth = st.selectbox("Analysis Depth", ["Standard", "Detailed", "Advanced"], index=1, key="depth_select")
    
    # Load and process data
    with st.spinner(f"Analyzing {ticker}..."):
        data, info, error = get_stock_data(ticker, period)
    
    if error:
        st.error(f"Error: {error}")
        st.stop()
    
    if data is None or data.empty:
        st.error(f"No data available for {ticker}")
        st.stop()
    
    # Calculate indicators
    for ma_period in [20, 50, 100, 200]:
        data[f'MA{ma_period}'] = data['Close'].rolling(window=ma_period).mean()
    
    data = calculate_ema(data, [8, 21, 50])
    data['RSI'] = calculate_rsi(data)
    data['MACD'], data['Signal'], data['Histogram'] = calculate_macd(data)
    
    # Run analyses
    valuation_score, valuation_details = analyze_valuation(info)
    momentum_score, momentum_details = analyze_momentum(data)
    earnings_score, earnings_details = analyze_earnings(info)
    technical_score, technical_details = analyze_technical(data)
    
    confidence = calculate_confidence_score(info, data, valuation_score, momentum_score, earnings_score, technical_score)
    recommendation, rec_class = get_recommendation_from_confidence(confidence)
    advice = generate_detailed_advice(confidence, recommendation, ticker, info, valuation_score, momentum_score, earnings_score, technical_score, valuation_details, momentum_details, earnings_details, technical_details)
    
    # Add to portfolio button
    if ticker not in st.session_state.portfolio:
        if st.button("⭐ Add to Portfolio"):
            st.session_state.portfolio.append(ticker)
            st.success(f"Added {ticker} to portfolio!")
    
    # Company Header - Full description
    business_summary = info.get('longBusinessSummary', 'No description available.')
    
    st.markdown(f"""
    <div class='company-header'>
        <div class='company-name'>{info.get('longName', ticker)}</div>
        <div style='font-size: 1.2rem; opacity: 0.9; font-weight: 600;'>{ticker} • {info.get('exchange', 'N/A')}</div>
        <div class='company-description'>{business_summary}</div>
        <div style='margin-top: 1rem;'>
            <span class='tag'>{info.get('sector', 'N/A')}</span>
            <span class='tag'>{info.get('industry', 'N/A')}</span>
            <span class='tag'>{info.get('country', 'N/A')}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    current_price = data['Close'].iloc[-1]
    price_change = data['Close'].iloc[-1] - data['Close'].iloc[0]
    pct_change = (price_change / data['Close'].iloc[0]) * 100
    
    with col1:
        st.metric("Current Price", f"${current_price:.2f}", f"{pct_change:+.2f}%")
    
    with col2:
        market_cap = info.get('marketCap', 0)
        cap_display = f"${market_cap/1e9:.1f}B" if market_cap > 1e9 else f"${market_cap/1e6:.1f}M"
        st.metric("Market Cap", cap_display)
    
    with col3:
        pe_ratio = info.get('trailingPE', 0)
        st.metric("P/E Ratio", f"{pe_ratio:.2f}" if pe_ratio else "N/A")
    
    with col4:
        volume = data['Volume'].iloc[-1]
        avg_volume = data['Volume'].mean()
        vol_change = ((volume / avg_volume) - 1) * 100
        st.metric("Volume", f"{volume/1e6:.1f}M", f"{vol_change:+.1f}%")
    
    with col5:
        high_52w = info.get('fiftyTwoWeekHigh', 0)
        low_52w = info.get('fiftyTwoWeekLow', 0)
        st.metric("52W Range", f"${low_52w:.0f} - ${high_52w:.0f}")
    
    # Confidence Card with detailed advice
    st.markdown(f"""
    <div class='confidence-card'>
        <div style='display: grid; grid-template-columns: 1fr 2fr; gap: 2rem; align-items: center;'>
            <div style='text-align: center;'>
                <div class='confidence-score'>{confidence}%</div>
                <div class='confidence-label'>Confidence Score</div>
                <div class='recommendation-badge {rec_class}' style='margin-top: 1.5rem;'>{recommendation}</div>
            </div>
            <div>
                <div class='advice-text'>{advice}</div>
                <div style='margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #e2e8f0;'>
                    <small style='color: #64748b;'><strong>Analysis Breakdown:</strong> Valuation ({valuation_score+6}/12) • Momentum ({momentum_score+6}/12) • Earnings ({earnings_score+6}/12) • Technical ({technical_score+6}/12)</small>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Price Chart
    st.markdown("<h2 class='section-header'>Price Performance</h2>", unsafe_allow_html=True)
    
    fig = make_subplots(
        rows=4, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.5, 0.15, 0.15, 0.15],
        subplot_titles=['Price', 'Volume', 'RSI', 'MACD']
    )
    
    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='Price',
            increasing_line_color='#10b981',
            decreasing_line_color='#ef4444'
        ),
        row=1, col=1
    )
    
    colors = {'EMA8': '#3b82f6', 'EMA21': '#8b5cf6', 'EMA50': '#f59e0b'}
    for ema, color in colors.items():
        if ema in data.columns:
            fig.add_trace(
                go.Scatter(x=data.index, y=data[ema], name=ema, line=dict(color=color, width=2)),
                row=1, col=1
            )
    
    colors_vol = ['#ef4444' if data['Close'].iloc[i] < data['Open'].iloc[i] else '#10b981' for i in range(len(data))]
    fig.add_trace(go.Bar(x=data.index, y=data['Volume'], name='Volume', marker_color=colors_vol, opacity=0.6), row=2, col=1)
    
    fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], name='RSI', line=dict(color='#8b5cf6', width=2)), row=3, col=1)
    fig.add_hline(y=70, line_dash="dash", line_color="#ef4444", row=3, col=1, opacity=0.5)
    fig.add_hline(y=30, line_dash="dash", line_color="#10b981", row=3, col=1, opacity=0.5)
    
    fig.add_trace(go.Scatter(x=data.index, y=data['MACD'], name='MACD', line=dict(color='#3b82f6', width=2)), row=4, col=1)
    fig.add_trace(go.Scatter(x=data.index, y=data['Signal'], name='Signal', line=dict(color='#f59e0b', width=2)), row=4, col=1)
    colors_hist = ['#ef4444' if val < 0 else '#10b981' for val in data['Histogram']]
    fig.add_trace(go.Bar(x=data.index, y=data['Histogram'], name='Histogram', marker_color=colors_hist, opacity=0.5), row=4, col=1)
    
    fig.update_layout(
        height=800,
        showlegend=True,
        xaxis_rangeslider_visible=False,
        hovermode='x unified',
        template='plotly_white',
        paper_bgcolor='white',
        plot_bgcolor='#f8fafc',
        font=dict(color='#1e293b', size=11, family='Inter'),
        legend=dict(bgcolor='white', bordercolor='#e2e8f0', borderwidth=1)
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#e2e8f0')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e2e8f0')
    
    st.plotly_chart(fig, use_container_width=True)

# COMPARE STOCKS PAGE
elif st.session_state.page == 'compare':
    st.markdown("""
    <div class='brbas-header'>
        <h1 class='brbas-title'>Compare Stocks</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Enter 2-3 stock tickers to compare")
    
    comp_col1, comp_col2, comp_col3, comp_col4 = st.columns([3, 3, 3, 2])
    
    with comp_col1:
        ticker1 = st.text_input("Stock 1", value="AAPL", key="comp1").upper()
    with comp_col2:
        ticker2 = st.text_input("Stock 2", value="MSFT", key="comp2").upper()
    with comp_col3:
        ticker3 = st.text_input("Stock 3 (optional)", value="", key="comp3").upper()
    with comp_col4:
        comp_period = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y"], index=2)
    
    if st.button("Compare Stocks", type="primary"):
        tickers_to_compare = [t for t in [ticker1, ticker2, ticker3] if t]
        
        if len(tickers_to_compare) < 2:
            st.warning("Please enter at least 2 stocks")
        else:
            comparison_data = []
            
            for ticker_comp in tickers_to_compare:
                with st.spinner(f"Analyzing {ticker_comp}..."):
                    data_comp, info_comp, error_comp = get_stock_data(ticker_comp, comp_period)
                    
                    if error_comp or data_comp is None or data_comp.empty:
                        st.error(f"Could not load {ticker_comp}")
                        continue
                    
                    for ma_period in [20, 50, 100, 200]:
                        data_comp[f'MA{ma_period}'] = data_comp['Close'].rolling(window=ma_period).mean()
                    
                    data_comp = calculate_ema(data_comp, [8, 21, 50])
                    data_comp['RSI'] = calculate_rsi(data_comp)
                    data_comp['MACD'], data_comp['Signal'], data_comp['Histogram'] = calculate_macd(data_comp)
                    
                    val_score, val_details = analyze_valuation(info_comp)
                    mom_score, mom_details = analyze_momentum(data_comp)
                    earn_score, earn_details = analyze_earnings(info_comp)
                    tech_score, tech_details = analyze_technical(data_comp)
                    
                    conf = calculate_confidence_score(info_comp, data_comp, val_score, mom_score, earn_score, tech_score)
                    rec, rec_class = get_recommendation_from_confidence(conf)
                    
                    current_price_comp = data_comp['Close'].iloc[-1]
                    price_change_comp = data_comp['Close'].iloc[-1] - data_comp['Close'].iloc[0]
                    pct_change_comp = (price_change_comp / data_comp['Close'].iloc[0]) * 100
                    
                    comparison_data.append({
                        'Ticker': ticker_comp,
                        'Company': info_comp.get('longName', ticker_comp),
                        'Price': f"${current_price_comp:.2f}",
                        'Change': f"{pct_change_comp:+.2f}%",
                        'Confidence': f"{conf}%",
                        'Recommendation': rec,
                        'Valuation': f"{val_score+6}/12",
                        'Momentum': f"{mom_score+6}/12",
                        'Earnings': f"{earn_score+6}/12",
                        'Technical': f"{tech_score+6}/12",
                        'Market Cap': f"${info_comp.get('marketCap', 0)/1e9:.1f}B" if info_comp.get('marketCap', 0) > 1e9 else "N/A",
                        'P/E': f"{info_comp.get('trailingPE', 0):.2f}" if info_comp.get('trailingPE') else "N/A",
                        'PEG': f"{info_comp.get('pegRatio', 0):.2f}" if info_comp.get('pegRatio') else "N/A",
                        'Sector': info_comp.get('sector', 'N/A')
                    })
            
            if comparison_data:
                st.markdown("### Comparison Results")
                
                cols = st.columns(len(comparison_data))
                
                for idx, stock_data in enumerate(comparison_data):
                    with cols[idx]:
                        rec = stock_data['Recommendation']
                        if 'BUY' in rec:
                            card_color = '#10b981'
                        elif 'SELL' in rec:
                            card_color = '#ef4444'
                        else:
                            card_color = '#f59e0b'
                        
                        st.markdown(f"""
                        <div style='background: white; padding: 1.5rem; border-radius: 12px; 
                                    border-left: 4px solid {card_color}; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                            <h3 style='margin: 0; color: #1e293b;'>{stock_data['Ticker']}</h3>
                            <p style='color: #64748b; font-size: 0.9rem;'>{stock_data['Company'][:30]}</p>
                            <div style='margin: 1rem 0;'>
                                <div style='font-size: 1.5rem; font-weight: 700;'>{stock_data['Price']}</div>
                                <div style='color: {"#10b981" if "+" in stock_data["Change"] else "#ef4444"}; font-weight: 600;'>{stock_data['Change']}</div>
                            </div>
                            <div style='background: {card_color}; color: white; padding: 0.5rem; 
                                        border-radius: 8px; text-align: center; font-weight: 700;'>
                                {stock_data['Recommendation']}
                            </div>
                            <div style='font-size: 1.2rem; font-weight: 700; text-align: center; margin-top: 1rem;'>
                                {stock_data['Confidence']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("**Scores:**")
                        st.write(f"Valuation: {stock_data['Valuation']}")
                        st.write(f"Momentum: {stock_data['Momentum']}")
                        st.write(f"Earnings: {stock_data['Earnings']}")
                        st.write(f"Technical: {stock_data['Technical']}")
                
                st.markdown("---")
                st.dataframe(pd.DataFrame(comparison_data), use_container_width=True, hide_index=True)

# PORTFOLIO PAGE
elif st.session_state.page == 'portfolio':
    st.markdown("""
    <div class='brbas-header'>
        <h1 class='brbas-title'>My Portfolio</h1>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.portfolio:
        st.info("Your portfolio is empty. Add stocks from the Stock Analysis page.")
    else:
        st.markdown(f"### Tracking {len(st.session_state.portfolio)} stocks")
        
        portfolio_data = []
        
        for ticker_port in st.session_state.portfolio:
            data_port, info_port, error_port = get_stock_data(ticker_port, "1mo")
            
            if not error_port and data_port is not None and not data_port.empty:
                current_price = data_port['Close'].iloc[-1]
                price_change = data_port['Close'].iloc[-1] - data_port['Close'].iloc[0]
                pct_change = (price_change / data_port['Close'].iloc[0]) * 100
                
                portfolio_data.append({
                    'Ticker': ticker_port,
                    'Company': info_port.get('longName', ticker_port),
                    'Price': current_price,
                    'Change': pct_change,
                    'Market Cap': info_port.get('marketCap', 0),
                    'P/E': info_port.get('trailingPE', 0)
                })
        
        if portfolio_data:
            cols = st.columns(min(3, len(portfolio_data)))
            
            for idx, stock in enumerate(portfolio_data):
                with cols[idx % 3]:
                    change_color = "#10b981" if stock['Change'] > 0 else "#ef4444"
                    
                    st.markdown(f"""
                    <div style='background: white; padding: 1.5rem; border-radius: 12px; 
                                box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 1rem;'>
                        <h3 style='margin: 0; color: #1e293b;'>{stock['Ticker']}</h3>
                        <p style='color: #64748b; font-size: 0.9rem;'>{stock['Company'][:30]}</p>
                        <div style='font-size: 1.8rem; font-weight: 700; color: #1e293b;'>${stock['Price']:.2f}</div>
                        <div style='color: {change_color}; font-weight: 600; font-size: 1.1rem;'>{stock['Change']:+.2f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Analyze {stock['Ticker']}", key=f"analyze_{stock['Ticker']}"):
                        st.session_state.page = 'analysis'
                        st.rerun()
                    
                    if st.button(f"Remove {stock['Ticker']}", key=f"remove_{stock['Ticker']}"):
                        st.session_state.portfolio.remove(stock['Ticker'])
                        st.rerun()
        
        if st.button("Clear Portfolio"):
            st.session_state.portfolio = []
            st.rerun()
