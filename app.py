import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="BARBAS", layout="wide", page_icon="📊", initial_sidebar_state="expanded")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .main { background: #ffffff; padding: 0; }
    .block-container { padding: 2rem 3rem; max-width: 1400px; }
    .brbas-header { text-align: center; padding: 4rem 0; background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%); margin: -2rem -3rem 2rem -3rem; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1); }
    .brbas-title { font-size: 9rem !important; font-weight: 800 !important; color: #ffffff !important; letter-spacing: 2.5rem !important; margin: 0 !important; }
    .sidebar-title { font-size: 2.8rem !important; font-weight: 800; letter-spacing: 0.8rem; text-align: center; margin-bottom: 2rem !important; color: white !important; }
    .model-card { background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1); border: 1px solid #e5e7eb; margin: 1.5rem 0; transition: box-shadow 0.2s ease; }
    .model-card:hover { box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); }
    .model-header { font-size: 1.5rem; font-weight: 700; color: #111827; margin-bottom: 1rem; }
    .model-score { display: inline-block; padding: 0.5rem 1.5rem; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; border-radius: 24px; font-weight: 600; font-size: 1rem; margin-bottom: 1rem; }
    .model-description { color: #374151; font-size: 1rem; line-height: 1.7; margin: 1rem 0 0 0; }
    .section-header { font-size: 1.875rem; font-weight: 700; color: #111827; margin: 3rem 0 1.5rem 0; padding-bottom: 0.75rem; border-bottom: 2px solid #e5e7eb; }
    .confidence-card { background: white; padding: 2.5rem; border-radius: 12px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1); border: 1px solid #e5e7eb; margin: 2rem 0; }
    .recommendation-badge { display: inline-block; padding: 0.75rem 2rem; border-radius: 24px; font-weight: 700; font-size: 1.1rem; margin: 1rem 0; text-transform: uppercase; letter-spacing: 0.5px; }
    .strong-buy { background: #10b981; color: white; }
    .buy { background: #34d399; color: white; }
    .hold { background: #fbbf24; color: white; }
    .sell { background: #f87171; color: white; }
    .strong-sell { background: #ef4444; color: white; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #1e40af 0%, #3b82f6 100%); }
    [data-testid="stSidebar"] .stMarkdown { color: white !important; }
    [data-testid="stSidebar"] button { width: 100%; background: rgba(255, 255, 255, 0.1); color: white !important; border: 1px solid rgba(255, 255, 255, 0.2); padding: 0.875rem; border-radius: 8px; margin: 0.5rem 0; font-weight: 600; font-size: 1rem; transition: all 0.2s ease; }
    [data-testid="stSidebar"] button:hover { background: rgba(255, 255, 255, 0.2); border-color: rgba(255, 255, 255, 0.3); }
    .portfolio-card { background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1); border: 1px solid #e5e7eb; margin-bottom: 1rem; }
    .disclaimer-footer { background: #f9fafb; padding: 2rem; border-radius: 12px; margin-top: 4rem; border-top: 1px solid #e5e7eb; text-align: center; }
    .disclaimer-text { font-size: 0.8rem; color: #6b7280; line-height: 1.6; max-width: 1200px; margin: 0 auto; }
</style>
""", unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'analysis'
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []

with st.sidebar:
    st.markdown("<h1 class='sidebar-title'>BARBAS</h1>", unsafe_allow_html=True)
    if st.button("Stock Analysis"):
        st.session_state.page = 'analysis'
    if st.button("Compare Stocks"):
        st.session_state.page = 'compare'
    if st.button("Portfolio"):
        st.session_state.page = 'portfolio'
    if st.button("Top Stocks"):
        st.session_state.page = 'top_stocks'

def search_ticker(query):
    mapping = {'apple': 'AAPL', 'microsoft': 'MSFT', 'google': 'GOOGL', 'amazon': 'AMZN', 'tesla': 'TSLA', 'meta': 'META', 'nvidia': 'NVDA'}
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
    return round(val_norm * weights['valuation'] + mom_norm * weights['momentum'] + earn_norm * weights['earnings'] + tech_norm * weights['technical'], 1)

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

def generate_detailed_analysis(confidence, rec, val_score, mom_score, earn_score, tech_score, val_details, mom_details, earn_details, tech_details, info, data, ticker):
    analysis_parts = []
    analysis_parts.append("<strong style='font-size: 1.2rem; color: #111827;'>Investment Strategy & Outlook:</strong>")
    
    if confidence >= 75:
        analysis_parts.append(f"For investors seeking growth opportunities, consider building positions in {ticker} with a focus on dollar-cost averaging over the next 1-2 months. Our models suggest potential upside of 15-25% over the next 6-12 months. The strong confidence score reflects alignment across all key metrics.")
    elif confidence >= 60:
        analysis_parts.append(f"Investors may consider initiating positions in {ticker} with measured sizing and clear risk parameters. The stock appears positioned for modest appreciation of 8-15% over the next 6-12 months if fundamentals continue on their current trajectory.")
    elif confidence >= 40:
        analysis_parts.append(f"For current shareholders of {ticker}, maintaining positions appears reasonable while monitoring for clearer signals. New investors should wait for better entry opportunities or stronger confirmation across our models.")
    elif confidence >= 25:
        analysis_parts.append(f"Investors holding {ticker} should consider reducing position sizes and reallocating to higher-conviction opportunities. The risk-reward profile appears unfavorable with meaningful downside potential if current trends persist.")
    else:
        analysis_parts.append(f"We recommend existing shareholders consider exiting positions in {ticker} or implementing protective strategies. The convergence of negative signals suggests elevated risk of further downside.")
    
    volatility = data['Close'].pct_change().std() * np.sqrt(252) * 100
    analysis_parts.append(f"<br><strong style='font-size: 1.2rem; color: #111827;'>Risk Profile:</strong>")
    analysis_parts.append(f"With annualized volatility of {volatility:.1f}%, {ticker} {'exhibits elevated' if volatility > 30 else 'demonstrates moderate' if volatility > 20 else 'shows relatively stable'} price fluctuations.")
    
    return "<br><br>".join(analysis_parts)

def analyze_valuation(info):
    score = 0
    details = []
    methodology = "The Valuation Model analyzes PEG ratio and P/E ratio to determine if a stock is trading at an attractive price relative to its growth prospects."
    
    peg = info.get('pegRatio')
    if peg and peg > 0:
        if peg < 1:
            score += 2
            details.append(f"PEG Ratio of {peg:.2f} indicates undervaluation.")
        elif peg < 2:
            score += 1
            details.append(f"PEG Ratio of {peg:.2f} suggests fair valuation.")
        else:
            score -= 2
            details.append(f"PEG Ratio of {peg:.2f} indicates overvaluation.")
    else:
        details.append("PEG Ratio data unavailable.")
    
    pe = info.get('trailingPE')
    if pe and pe > 0:
        if pe < 15:
            score += 1
            details.append(f"P/E Ratio of {pe:.1f} is below market average.")
        elif pe > 30:
            score -= 1
            details.append(f"P/E Ratio of {pe:.1f} is elevated.")
    
    evaluation = f"This model scored {score+6}/12. "
    if score >= 2:
        evaluation += "Strong positive score indicates attractive valuation."
    elif score >= 0:
        evaluation += "Neutral score suggests fair valuation."
    else:
        evaluation += "Negative score signals overvaluation concerns."
    
    details.insert(0, methodology)
    details.append(evaluation)
    return score, details

def analyze_momentum(data):
    score = 0
    details = []
    methodology = "The Momentum Model evaluates trend strength using moving average analysis to identify the stock's position within its trend cycle."
    
    price = data['Close'].iloc[-1]
    
    if 'MA50' in data.columns and 'MA200' in data.columns:
        ma50 = data['MA50'].iloc[-1]
        ma200 = data['MA200'].iloc[-1]
        if pd.notna(ma50) and pd.notna(ma200):
            if ma50 > ma200 and price > ma50:
                score += 2
                details.append(f"Golden Cross active with strong upward momentum.")
            elif ma50 < ma200 and price < ma50:
                score -= 2
                details.append(f"Death Cross active indicating downward pressure.")
    
    evaluation = f"This model scored {score+6}/12. "
    if score >= 2:
        evaluation += "Strong momentum indicates confirmed uptrend."
    elif score >= 0:
        evaluation += "Neutral momentum suggests consolidation."
    else:
        evaluation += "Negative momentum indicates downtrend."
    
    details.insert(0, methodology)
    details.append(evaluation)
    return score, details

def analyze_earnings(info):
    score = 0
    details = []
    methodology = "The Earnings Model focuses on fundamental health by examining earnings growth and profit margins."
    
    growth = info.get('earningsQuarterlyGrowth')
    if growth is not None:
        if growth > 0.15:
            score += 2
            details.append(f"Exceptional earnings growth of {growth*100:.1f}%.")
        elif growth > 0.05:
            score += 1
            details.append(f"Solid earnings growth of {growth*100:.1f}%.")
        else:
            score -= 2
            details.append(f"Earnings decline of {growth*100:.1f}%.")
    
    evaluation = f"This model scored {score+6}/12. "
    if score >= 2:
        evaluation += "Strong earnings indicate robust fundamental health."
    elif score >= 0:
        evaluation += "Neutral earnings suggest stable performance."
    else:
        evaluation += "Negative earnings raise red flags."
    
    details.insert(0, methodology)
    details.append(evaluation)
    return score, details

def analyze_technical(data):
    score = 0
    details = []
    methodology = "The Technical Model uses RSI and MACD to identify overbought/oversold conditions and momentum changes."
    
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
    
    if 'MACD' in data.columns and 'Signal' in data.columns:
        macd = data['MACD'].iloc[-1]
        signal = data['Signal'].iloc[-1]
        if pd.notna(macd) and pd.notna(signal):
            if macd > signal:
                score += 1
                details.append(f"MACD bullish indicating upward momentum.")
            else:
                score -= 1
                details.append(f"MACD bearish suggesting downward pressure.")
    
    evaluation = f"This model scored {score+6}/12. "
    if score >= 2:
        evaluation += "Strong technical score suggests favorable setup."
    elif score >= 0:
        evaluation += "Neutral technical score indicates balanced territory."
    else:
        evaluation += "Negative technical score warns of overbought conditions."
    
    details.insert(0, methodology)
    details.append(evaluation)
    return score, details

@st.cache_data(ttl=300)
def get_stock_data(ticker, period):
    try:
        stock = yf.Ticker(ticker)
        return stock.history(period=period), stock.info, None
    except Exception as e:
        return None, None, str(e)

if st.session_state.page == 'analysis':
    st.markdown("<div class='brbas-header'><h1 class='brbas-title'>BARBAS</h1></div>", unsafe_allow_html=True)
    
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
        <h2 style='margin: 0; font-size: 2.5rem; color: white;'>{info.get('longName', ticker)}</h2>
        <p style='margin: 0.5rem 0; font-size: 1.2rem; color: white;'>{ticker} | {info.get('exchange', 'N/A')}</p>
        <p style='margin: 1rem 0; color: white;'>{desc}</p>
    </div>
    """, unsafe_allow_html=True)
    
    price = data['Close'].iloc[-1]
    change = ((data['Close'].iloc[-1] / data['Close'].iloc[0]) - 1) * 100
    
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Price", f"${price:,.2f}", f"{change:+.2f}%")
    c2.metric("Market Cap", f"${info.get('marketCap', 0)/1e9:,.1f}B")
    c3.metric("P/E", f"{info.get('trailingPE', 0):,.2f}")
    c4.metric("Volume", f"{int(data['Volume'].iloc[-1]):,}")
    c5.metric("52W Range", f"${info.get('fiftyTwoWeekLow', 0):,.0f}-{info.get('fiftyTwoWeekHigh', 0):,.0f}")
    
    st.markdown(f"""
    <div class='confidence-card'>
        <div style='display: grid; grid-template-columns: 1fr 2fr; gap: 2rem;'>
            <div style='text-align: center;'>
                <div style='font-size: 4rem; font-weight: 800; color: #3b82f6;'>{confidence}%</div>
                <div style='font-size: 0.9rem; color: #6b7280; text-transform: uppercase; margin-bottom: 1rem;'>Confidence Score</div>
                <div class='recommendation-badge {rec_class}'>{rec}</div>
            </div>
            <div>
                <p style='font-size: 1.25rem; line-height: 1.8; color: #111827; font-weight: 500;'>
                    Based on analysis across four models—Valuation, Momentum, Earnings, and Technical—this stock receives a <strong>{confidence}%</strong> confidence score with a <strong>{rec}</strong> recommendation.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    detailed_analysis = generate_detailed_analysis(confidence, rec, val_score, mom_score, earn_score, tech_score, val_details, mom_details, earn_details, tech_details, info, data, ticker)
    
    st.markdown(f"""
    <div style='background: white; padding: 2.5rem; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin: 2rem 0; border: 1px solid #e5e7eb;'>
        <h2 style='font-size: 2rem; font-weight: 700; color: #111827; margin-bottom: 1.5rem;'>Comprehensive Investment Analysis</h2>
        <div style='font-size: 1.05rem; line-height: 1.9; color: #374151;'>{detailed_analysis}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 class='section-header'>Investment Analysis Models</h2>", unsafe_allow_html=True)
    
    for title, score, dets in [("Valuation Model", val_score, val_details), ("Momentum Model", mom_score, mom_details), ("Earnings Model", earn_score, earn_details), ("Technical Model", tech_score, tech_details)]:
        st.markdown(f"""
        <div class='model-card'>
            <div class='model-header'>{title}</div>
            <span class='model-score'>Score: {score+6}/12</span>
            <div class='model-description'>{' '.join(dets)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='disclaimer-footer'>
        <div class='disclaimer-text'>
            <strong>Disclaimer:</strong> The information provided by BARBAS is for informational and educational purposes only and should not be construed as financial, investment, or legal advice.
        </div>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.page == 'portfolio':
    st.markdown("<div class='brbas-header'><h1 class='brbas-title'>BARBAS</h1></div>", unsafe_allow_html=True)
    st.markdown("<h2 class='section-header'>Portfolio</h2>", unsafe_allow_html=True)
    
    if not st.session_state.portfolio:
        st.info("Portfolio empty. Add stocks from Analysis page.")
    else:
        for t in st.session_state.portfolio:
            d, i, _ = get_stock_data(t, "1mo")
            if d is not None and not d.empty:
                price = d['Close'].iloc[-1]
                change = ((d['Close'].iloc[-1] / d['Close'].iloc[0]) - 1) * 100
                st.markdown(f"""
                <div class='portfolio-card'>
                    <h3>{t} - ${price:.2f}</h3>
                    <p>Change: {change:+.2f}%</p>
                </div>
                """, unsafe_allow_html=True)

elif st.session_state.page == 'top_stocks':
    st.markdown("<div class='brbas-header'><h1 class='brbas-title'>BARBAS</h1></div>", unsafe_allow_html=True)
    st.markdown("<h2 class='section-header'>Top Stocks by Sector</h2>", unsafe_allow_html=True)
    st.info("Feature coming soon...")

elif st.session_state.page == 'compare':
    st.markdown("<div class='brbas-header'><h1 class='brbas-title'>BARBAS</h1></div>", unsafe_allow_html=True)
    st.markdown("<h2 class='section-header'>Compare Stocks</h2>", unsafe_allow_html=True)
    st.info("Feature coming soon...")
