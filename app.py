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
        padding: 3rem 0;
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        margin: -2rem -3rem 2rem -3rem;
        box-shadow: 0 4px 20px rgba(30, 64, 175, 0.15);
    }
    
    .brbas-title {
        font-size: 5rem;
        font-weight: 800;
        color: white;
        letter-spacing: 1rem;
        margin: 0;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }
    
    .sidebar-title {
        font-size: 2.5rem !important;
        font-weight: 800;
        letter-spacing: 0.5rem;
        text-align: center;
        margin-bottom: 2rem !important;
    }
    
    .model-card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #3b82f6;
        margin: 1.5rem 0;
    }
    
    .model-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 1rem;
    }
    
    .model-score {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border-radius: 50px;
        font-weight: 700;
        font-size: 1.2rem;
        margin-bottom: 1rem;
    }
    
    .model-detail {
        padding: 1rem;
        margin: 0.75rem 0;
        background: #f8fafc;
        border-left: 3px solid #3b82f6;
        border-radius: 4px;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    .section-header {
        font-size: 2rem;
        font-weight: 700;
        color: #1e293b;
        margin: 3rem 0 1.5rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 3px solid #3b82f6;
    }
    
    .confidence-card {
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        border-left: 6px solid #3b82f6;
        margin: 2rem 0;
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
    
    .strong-buy { background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; }
    .buy { background: linear-gradient(135deg, #34d399 0%, #10b981 100%); color: white; }
    .hold { background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%); color: white; }
    .sell { background: linear-gradient(135deg, #f87171 0%, #ef4444 100%); color: white; }
    .strong-sell { background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); color: white; }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e40af 0%, #1e3a8a 100%);
    }
    
    [data-testid="stSidebar"] button {
        width: 100%;
        background: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    .stMetric {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    }
</style>
""", unsafe_allow_html=True)

# Session state
if 'page' not in st.session_state:
    st.session_state.page = 'analysis'
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []

# Sidebar
with st.sidebar:
    st.markdown("<h1 class='sidebar-title'>BRBAS</h1>", unsafe_allow_html=True)
    if st.button("Stock Analysis"):
        st.session_state.page = 'analysis'
    if st.button("Compare Stocks"):
        st.session_state.page = 'compare'
    if st.button("Portfolio"):
        st.session_state.page = 'portfolio'
    if st.button("Top Stocks"):
        st.session_state.page = 'top_stocks'

def search_ticker(query):
    mapping = {
        'apple': 'AAPL', 'microsoft': 'MSFT', 'google': 'GOOGL', 'amazon': 'AMZN',
        'tesla': 'TSLA', 'meta': 'META', 'nvidia': 'NVDA'
    }
    return mapping.get(query.lower(), query.upper())

def truncate_description(text, max_length=300):
    if len(text) <= max_length:
        return text
    truncated = text[:max_length]
    last_period = truncated.rfind('.')
    if last_period > max_length * 0.7:
        return truncated[:last_period + 1]
    return truncated[:truncated.rfind(' ')] + '.'

def calculate_confidence_score(info, data, val_score, mom_score, earn_score, tech_score):
    weights = {'valuation': 0.30, 'momentum': 0.25, 'earnings': 0.25, 'technical': 0.20}
    val_norm = ((val_score + 6) / 12) * 100
    mom_norm = ((mom_score + 6) / 12) * 100
    earn_norm = ((earn_score + 6) / 12) * 100
    tech_norm = ((tech_score + 6) / 12) * 100
    return round(val_norm * weights['valuation'] + mom_norm * weights['momentum'] + 
                 earn_norm * weights['earnings'] + tech_norm * weights['technical'], 1)

def get_recommendation_from_confidence(confidence):
    if confidence >= 75: return "STRONG BUY", "strong-buy"
    elif confidence >= 60: return "BUY", "buy"
    elif confidence >= 40: return "HOLD", "hold"
    elif confidence >= 25: return "SELL", "sell"
    else: return "STRONG SELL", "strong-sell"

def calculate_rsi(data, period=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    return 100 - (100 / (1 + gain / loss))

def calculate_macd(data, fast=12, slow=26, signal=9):
    exp1 = data['Close'].ewm(span=fast, adjust=False).mean()
    exp2 = data['Close'].ewm(span=slow, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    return macd, signal_line, macd - signal_line

def calculate_ema(data, periods=[8, 21, 50]):
    for period in periods:
        data[f'EMA{period}'] = data['Close'].ewm(span=period, adjust=False).mean()
    return data

def analyze_valuation(info):
    score = 0
    details = []
    peg = info.get('pegRatio')
    if peg and peg > 0:
        if peg < 1:
            score += 2
            details.append(f"PEG Ratio of {peg:.2f} indicates undervaluation. The stock trades below its growth rate.")
        elif peg < 2:
            score += 1
            details.append(f"PEG Ratio of {peg:.2f} suggests fair valuation.")
        else:
            score -= 2
            details.append(f"PEG Ratio of {peg:.2f} indicates overvaluation relative to growth.")
    else:
        details.append("PEG Ratio unavailable.")
    return score, details

def analyze_momentum(data):
    score = 0
    details = []
    price = data['Close'].iloc[-1]
    if 'MA50' in data.columns and 'MA200' in data.columns:
        ma50 = data['MA50'].iloc[-1]
        ma200 = data['MA200'].iloc[-1]
        if pd.notna(ma50) and pd.notna(ma200):
            if ma50 > ma200 and price > ma50:
                score += 2
                details.append(f"Golden Cross active. Price ${price:.2f} above both moving averages.")
            elif ma50 < ma200 and price < ma50:
                score -= 2
                details.append(f"Death Cross active. Price ${price:.2f} below both moving averages.")
    else:
        details.append("Moving average data unavailable.")
    return score, details

def analyze_earnings(info):
    score = 0
    details = []
    growth = info.get('earningsQuarterlyGrowth')
    if growth is not None:
        if growth > 0.15:
            score += 2
            details.append(f"Strong earnings growth of {growth*100:.1f}% significantly exceeds market averages.")
        elif growth > 0:
            score += 1
            details.append(f"Positive earnings growth of {growth*100:.1f}%.")
        else:
            score -= 2
            details.append(f"Negative earnings growth of {growth*100:.1f}% is concerning.")
    else:
        details.append("Earnings growth data unavailable.")
    return score, details

def analyze_technical(data):
    score = 0
    details = []
    rsi = data['RSI'].iloc[-1] if 'RSI' in data.columns and pd.notna(data['RSI'].iloc[-1]) else None
    if rsi:
        if rsi < 30:
            score += 2
            details.append(f"RSI at {rsi:.1f} indicates oversold conditions.")
        elif rsi > 70:
            score -= 2
            details.append(f"RSI at {rsi:.1f} signals overbought conditions.")
        else:
            details.append(f"RSI at {rsi:.1f} is neutral.")
    else:
        details.append("RSI data unavailable.")
    return score, details

@st.cache_data(ttl=300)
def get_stock_data(ticker, period):
    try:
        stock = yf.Ticker(ticker)
        return stock.history(period=period), stock.info, None
    except Exception as e:
        return None, None, str(e)

# PAGES
if st.session_state.page == 'analysis':
    st.markdown("<div class='brbas-header'><h1 class='brbas-title'>BRBAS</h1></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([4, 2, 2])
    with col1:
        ticker = search_ticker(st.text_input("", "AAPL", placeholder="Ticker or company", label_visibility="collapsed"))
    with col2:
        period = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y", "2y"], index=3, label_visibility="collapsed")
    with col3:
        depth = st.selectbox("Depth", ["Standard", "Detailed"], index=0, label_visibility="collapsed")
    
    with st.spinner(f"Analyzing {ticker}..."):
        data, info, error = get_stock_data(ticker, period)
    
    if error or data is None or data.empty:
        st.error("Data unavailable")
        st.stop()
    
    for ma in [20, 50, 100, 200]:
        data[f'MA{ma}'] = data['Close'].rolling(window=ma).mean()
    data = calculate_ema(data)
    data['RSI'] = calculate_rsi(data)
    data['MACD'], data['Signal'], data['Histogram'] = calculate_macd(data)
    
    val_score, val_details = analyze_valuation(info)
    mom_score, mom_details = analyze_momentum(data)
    earn_score, earn_details = analyze_earnings(info)
    tech_score, tech_details = analyze_technical(data)
    
    confidence = calculate_confidence_score(info, data, val_score, mom_score, earn_score, tech_score)
    rec, rec_class = get_recommendation_from_confidence(confidence)
    
    if ticker not in st.session_state.portfolio:
        if st.button("Add to Portfolio"):
            st.session_state.portfolio.append(ticker)
            st.success(f"Added {ticker}")
    
    desc = truncate_description(info.get('longBusinessSummary', 'No description.'), 300)
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%); padding: 2rem; border-radius: 16px; color: white; margin-bottom: 2rem;'>
        <h2 style='margin: 0; font-size: 2.5rem;'>{info.get('longName', ticker)}</h2>
        <p style='margin: 0.5rem 0; font-size: 1.2rem;'>{ticker} | {info.get('exchange', 'N/A')}</p>
        <p style='margin: 1rem 0;'>{desc}</p>
    </div>
    """, unsafe_allow_html=True)
    
    price = data['Close'].iloc[-1]
    change = ((data['Close'].iloc[-1] / data['Close'].iloc[0]) - 1) * 100
    
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Price", f"${price:.2f}", f"{change:+.2f}%")
    c2.metric("Market Cap", f"${info.get('marketCap', 0)/1e9:.1f}B")
    c3.metric("P/E", f"{info.get('trailingPE', 0):.2f}")
    c4.metric("Volume", f"{data['Volume'].iloc[-1]/1e6:.1f}M")
    c5.metric("52W Range", f"${info.get('fiftyTwoWeekLow', 0):.0f}-{info.get('fiftyTwoWeekHigh', 0):.0f}")
    
    st.markdown(f"""
    <div class='confidence-card'>
        <div style='display: grid; grid-template-columns: 1fr 2fr; gap: 2rem;'>
            <div style='text-align: center;'>
                <div style='font-size: 4rem; font-weight: 800; color: #3b82f6;'>{confidence}%</div>
                <div style='font-size: 0.9rem; color: #64748b; text-transform: uppercase;'>Confidence</div>
                <div class='recommendation-badge {rec_class}'>{rec}</div>
            </div>
            <div>
                <p style='font-size: 1.1rem; line-height: 1.8;'>Based on comprehensive analysis, this stock shows a {confidence}% confidence score.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 class='section-header'>Investment Analysis Models</h2>", unsafe_allow_html=True)
    
    for title, score, dets in [
        ("Valuation Model", val_score, val_details),
        ("Momentum Model", mom_score, mom_details),
        ("Earnings Model", earn_score, earn_details),
        ("Technical Model", tech_score, tech_details)
    ]:
        st.markdown(f"""
        <div class='model-card'>
            <div class='model-header'>{title}</div>
            <span class='model-score'>Score: {score+6}/12</span>
        </div>
        """, unsafe_allow_html=True)
        for det in dets:
            st.markdown(f"<div class='model-detail'>{det}</div>", unsafe_allow_html=True)

elif st.session_state.page == 'portfolio':
    st.markdown("<div class='brbas-header'><h1 class='brbas-title'>BRBAS</h1></div>", unsafe_allow_html=True)
    st.markdown("<h2 class='section-header'>Portfolio</h2>", unsafe_allow_html=True)
    
    if not st.session_state.portfolio:
        st.info("Portfolio empty. Add stocks from Analysis page.")
    else:
        for t in st.session_state.portfolio:
            d, i, _ = get_stock_data(t, "1mo")
            if d is not None:
                st.write(f"**{t}**: ${d['Close'].iloc[-1]:.2f}")
                if st.button(f"Remove {t}", key=f"rm_{t}"):
                    st.session_state.portfolio.remove(t)
                    st.rerun()

elif st.session_state.page == 'top_stocks':
    st.markdown("<div class='brbas-header'><h1 class='brbas-title'>BRBAS</h1></div>", unsafe_allow_html=True)
    st.markdown("<h2 class='section-header'>Top Stocks</h2>", unsafe_allow_html=True)
    st.info("Top stocks feature - analyze major sectors for highest confidence picks")
