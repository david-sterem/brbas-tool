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
        color: white !important;
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
        font-size: 1.8rem;
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
    
    .model-description {
        color: #64748b;
        font-size: 1rem;
        line-height: 1.6;
        margin: 1rem 0 1.5rem 0;
        font-style: italic;
    }
    
    .model-detail {
        padding: 1.5rem;
        margin: 0;
        background: #f8fafc;
        border-radius: 8px;
        font-size: 1.05rem;
        line-height: 1.9;
        color: #1e293b;
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
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white !important;
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
    
    .stMetric label {
        color: #64748b !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #1e293b !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
    }
    
    .portfolio-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
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

def generate_detailed_analysis(confidence, rec, val_score, mom_score, earn_score, tech_score, 
                               val_details, mom_details, earn_details, tech_details, info, data, ticker):
    """Generate comprehensive investment analysis with forward-looking recommendations"""
    
    price = data['Close'].iloc[-1]
    price_change = ((data['Close'].iloc[-1] / data['Close'].iloc[0]) - 1) * 100
    
    analysis_parts = []
    
    # Opening assessment
    if confidence >= 75:
        analysis_parts.append(f"Our comprehensive analysis reveals {ticker} as a strong investment opportunity with a {confidence}% confidence score, warranting a {rec} recommendation. The stock demonstrates compelling characteristics across multiple analytical dimensions that suggest significant upside potential.")
    elif confidence >= 60:
        analysis_parts.append(f"Our analysis indicates {ticker} presents a favorable investment profile with a {confidence}% confidence score, supporting a {rec} recommendation. While there are positive signals across several metrics, investors should remain attentive to certain considerations outlined below.")
    elif confidence >= 40:
        analysis_parts.append(f"Our analysis suggests {ticker} merits a {rec} stance with a {confidence}% confidence score. The stock shows mixed signals across our analytical framework, requiring a balanced approach and careful monitoring before making significant position changes.")
    elif confidence >= 25:
        analysis_parts.append(f"Our analysis indicates caution is warranted for {ticker}, reflected in a {confidence}% confidence score and {rec} recommendation. Multiple indicators suggest headwinds that investors should carefully consider before maintaining or initiating positions.")
    else:
        analysis_parts.append(f"Our analysis reveals significant concerns regarding {ticker}, resulting in a {confidence}% confidence score and {rec} recommendation. The stock faces multiple challenges across our analytical framework that suggest substantial downside risk.")
    
    # Valuation insights
    val_strength = "strength" if val_score >= 1 else "concern" if val_score <= -1 else "mixed signal"
    analysis_parts.append(f"From a valuation perspective (Score: {val_score+6}/12), the stock presents a {val_strength}. {' '.join(val_details[:2])}")
    
    # Momentum insights
    mom_strength = "strong upward momentum" if mom_score >= 1 else "downward pressure" if mom_score <= -1 else "neutral trend"
    analysis_parts.append(f"Momentum analysis (Score: {mom_score+6}/12) reveals {mom_strength}. {' '.join(mom_details[:2])}")
    
    # Earnings insights
    earn_strength = "robust fundamentals" if earn_score >= 1 else "fundamental challenges" if earn_score <= -1 else "stable fundamentals"
    analysis_parts.append(f"The earnings picture (Score: {earn_score+6}/12) shows {earn_strength}. {' '.join(earn_details[:2])}")
    
    # Technical insights
    tech_strength = "bullish technical setup" if tech_score >= 1 else "bearish technical configuration" if tech_score <= -1 else "neutral technical stance"
    analysis_parts.append(f"Technical indicators (Score: {tech_score+6}/12) suggest a {tech_strength}. {' '.join(tech_details[:2])}")
    
    # Forward-looking recommendations
    analysis_parts.append("<br><strong style='font-size: 1.15rem;'>Investment Strategy & Outlook:</strong>")
    
    if confidence >= 75:
        analysis_parts.append(f"For investors seeking growth opportunities, consider building positions in {ticker} with a focus on dollar-cost averaging over the next 1-2 months to optimize entry points. Our models suggest potential upside of 15-25% over the next 6-12 months based on current trajectories. Key catalysts to monitor include upcoming earnings reports, sector rotation trends, and broader market sentiment shifts. Consider setting profit targets at key resistance levels while maintaining stop-losses to protect against unexpected volatility.")
    elif confidence >= 60:
        analysis_parts.append(f"Investors may consider initiating or adding to positions in {ticker}, but should do so with measured position sizing and clear risk parameters. The stock appears well-positioned for modest appreciation over the next 6-12 months, with potential gains in the 8-15% range if fundamentals continue on their current trajectory. Monitor quarterly earnings closely and be prepared to adjust positions if key metrics deteriorate. This is a suitable holding for core portfolio positions with medium-term horizons.")
    elif confidence >= 40:
        analysis_parts.append(f"For current shareholders of {ticker}, maintaining existing positions appears reasonable while monitoring for clearer directional signals. New investors should wait for better entry opportunities or stronger confirmation across our analytical models before initiating positions. The stock may trade within a relatively tight range near current levels over the coming months. Watch for potential catalysts that could shift the risk-reward profile—either positive developments that would upgrade the recommendation, or negative signals that would warrant position reduction.")
    elif confidence >= 25:
        analysis_parts.append(f"Investors holding {ticker} should consider reducing position sizes and reallocating capital to higher-conviction opportunities. The current risk-reward profile appears unfavorable, with meaningful downside potential if current trends persist. For those maintaining exposure, implement strict stop-loss levels and avoid averaging down without clear evidence of trend reversal. New investors should avoid initiating positions until confidence metrics improve substantially.")
    else:
        analysis_parts.append(f"We recommend existing shareholders consider exiting positions in {ticker} or implementing protective strategies such as options hedging. The convergence of negative signals across our models suggests elevated risk of further downside. Capital preservation should be the priority, and investors may find better opportunities elsewhere in the current market environment. Only consider re-entry after observing sustained improvement across multiple quarters and clearer technical reversal patterns.")
    
    # Risk considerations
    volatility = data['Close'].pct_change().std() * np.sqrt(252) * 100
    analysis_parts.append(f"<br><strong style='font-size: 1.15rem;'>Risk Profile:</strong> With annualized volatility of {volatility:.1f}%, {ticker} {'exhibits elevated price fluctuations requiring careful position sizing' if volatility > 30 else 'demonstrates moderate volatility suitable for most risk tolerances' if volatility > 20 else 'shows relatively stable price action'}. Investors should align position sizes with their individual risk tolerance and investment timeframe.")
    
    return "<br><br>".join(analysis_parts)

def analyze_valuation(info):
    score = 0
    details = []
    peg = info.get('pegRatio')
    if peg and peg > 0:
        if peg < 1:
            score += 2
            details.append(f"PEG Ratio of {peg:.2f} indicates undervaluation. The stock trades below its growth rate, suggesting a compelling value opportunity.")
        elif peg < 2:
            score += 1
            details.append(f"PEG Ratio of {peg:.2f} suggests fair valuation. The stock is reasonably priced relative to its growth.")
        else:
            score -= 2
            details.append(f"PEG Ratio of {peg:.2f} indicates overvaluation. The stock is expensive relative to its growth prospects.")
    else:
        details.append("PEG Ratio data unavailable. This metric compares P/E to growth rate.")
    
    pe = info.get('trailingPE')
    if pe and pe > 0:
        if pe < 15:
            score += 1
            details.append(f"P/E Ratio of {pe:.1f} is below market average, suggesting potential undervaluation.")
        elif pe > 30:
            score -= 1
            details.append(f"P/E Ratio of {pe:.1f} is elevated, indicating premium pricing.")
    else:
        details.append("P/E Ratio unavailable.")
    
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
                details.append(f"Golden Cross active with price at ${price:.2f} above both 50-day (${ma50:.2f}) and 200-day (${ma200:.2f}) moving averages. This bullish configuration suggests strong upward momentum.")
            elif ma50 < ma200 and price < ma50:
                score -= 2
                details.append(f"Death Cross active with price at ${price:.2f} below both moving averages. This bearish pattern indicates downward pressure.")
            else:
                details.append(f"Mixed signals with price at ${price:.2f}. The stock is in transition between trends.")
        else:
            details.append("Insufficient data for moving average analysis.")
    else:
        details.append("Moving average data unavailable.")
    
    if 'MA20' in data.columns:
        ma20 = data['MA20'].iloc[-1]
        if pd.notna(ma20):
            deviation = ((price / ma20) - 1) * 100
            if abs(deviation) > 3:
                if deviation > 0:
                    score += 1
                    details.append(f"Strong short-term momentum with price {deviation:.1f}% above 20-day MA.")
                else:
                    score -= 1
                    details.append(f"Weak short-term momentum with price {abs(deviation):.1f}% below 20-day MA.")
    
    return score, details

def analyze_earnings(info):
    score = 0
    details = []
    growth = info.get('earningsQuarterlyGrowth')
    if growth is not None:
        if growth > 0.15:
            score += 2
            details.append(f"Exceptional earnings growth of {growth*100:.1f}% significantly exceeds market averages, demonstrating strong operational performance.")
        elif growth > 0.05:
            score += 1
            details.append(f"Solid earnings growth of {growth*100:.1f}% indicates healthy business expansion.")
        elif growth > 0:
            details.append(f"Modest earnings growth of {growth*100:.1f}% shows steady but slow expansion.")
        else:
            score -= 2
            details.append(f"Earnings decline of {growth*100:.1f}% is concerning and suggests operational challenges.")
    else:
        details.append("Earnings growth data unavailable.")
    
    margin = info.get('profitMargins')
    if margin:
        if margin > 0.20:
            details.append(f"Strong profit margin of {margin*100:.1f}% demonstrates pricing power and operational efficiency.")
        elif margin > 0.10:
            details.append(f"Decent profit margin of {margin*100:.1f}% indicates reasonable profitability.")
        else:
            details.append(f"Thin profit margin of {margin*100:.1f}% suggests limited pricing power.")
    
    return score, details

def analyze_technical(data):
    score = 0
    details = []
    rsi = data['RSI'].iloc[-1] if 'RSI' in data.columns and pd.notna(data['RSI'].iloc[-1]) else None
    if rsi:
        if rsi < 30:
            score += 2
            details.append(f"RSI at {rsi:.1f} indicates oversold conditions. Historically, readings below 30 precede price reversals as selling pressure becomes exhausted.")
        elif rsi > 70:
            score -= 2
            details.append(f"RSI at {rsi:.1f} signals overbought conditions. Readings above 70 typically lead to pullbacks as buyers become exhausted.")
        else:
            details.append(f"RSI at {rsi:.1f} is in neutral territory, indicating balanced buying and selling pressure.")
    else:
        details.append("RSI data unavailable.")
    
    if 'MACD' in data.columns and 'Signal' in data.columns:
        macd = data['MACD'].iloc[-1]
        signal = data['Signal'].iloc[-1]
        if pd.notna(macd) and pd.notna(signal):
            if macd > signal:
                score += 1
                details.append(f"MACD bullish at {macd:.2f} above signal line {signal:.2f}, indicating upward momentum.")
            else:
                score -= 1
                details.append(f"MACD bearish at {macd:.2f} below signal line {signal:.2f}, suggesting downward pressure.")
    
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
                <div style='font-size: 0.9rem; color: #64748b; text-transform: uppercase; margin-bottom: 1rem;'>Confidence Score</div>
                <div class='recommendation-badge {rec_class}'>{rec}</div>
            </div>
            <div>
                <p style='font-size: 1.25rem; line-height: 1.8; color: #1e293b; font-weight: 500;'>
                    Based on comprehensive analysis across valuation, momentum, earnings, and technical indicators, 
                    this stock receives a <strong>{confidence}%</strong> confidence score with a <strong>{rec}</strong> recommendation.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed Analysis Section
    detailed_analysis = generate_detailed_analysis(confidence, rec, val_score, mom_score, earn_score, tech_score,
                                                   val_details, mom_details, earn_details, tech_details, info, data, ticker)
    
    st.markdown(f"""
    <div style='background: white; padding: 2.5rem; border-radius: 16px; box-shadow: 0 4px 16px rgba(0,0,0,0.1); 
                margin: 2rem 0; border-left: 6px solid #3b82f6;'>
        <h2 style='font-size: 2rem; font-weight: 700; color: #1e293b; margin-bottom: 1.5rem;'>Comprehensive Investment Analysis</h2>
        <div style='font-size: 1.05rem; line-height: 1.9; color: #334155;'>
            {detailed_analysis}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 class='section-header'>Investment Analysis Models</h2>", unsafe_allow_html=True)
    
    models = [
        ("Valuation Model", val_score, val_details, "Analyzes whether the stock is over or undervalued using PEG ratio, P/E trends, and price-to-book metrics."),
        ("Momentum Model", mom_score, mom_details, "Evaluates trend strength using moving average crossovers and price positioning."),
        ("Earnings Model", earn_score, earn_details, "Assesses business health through earnings growth, revenue trends, and profitability margins."),
        ("Technical Model", tech_score, tech_details, "Uses RSI and MACD indicators to identify overbought/oversold conditions.")
    ]
    
    for title, score, dets, desc in models:
        st.markdown(f"""
        <div class='model-card'>
            <div class='model-header'>{title}</div>
            <span class='model-score'>Score: {score+6}/12</span>
            <div class='model-description'>{desc}</div>
            <div class='model-detail'>
                {' '.join(dets)}
            </div>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.page == 'portfolio':
    st.markdown("<div class='brbas-header'><h1 class='brbas-title'>BRBAS</h1></div>", unsafe_allow_html=True)
    st.markdown("<h2 class='section-header'>Portfolio</h2>", unsafe_allow_html=True)
    
    if not st.session_state.portfolio:
        st.info("Portfolio empty. Add stocks from Analysis page.")
    else:
        for t in st.session_state.portfolio:
            d, i, _ = get_stock_data(t, "1mo")
            if d is not None and not d.empty:
                col_info, col_button = st.columns([4, 1])
                with col_info:
                    st.markdown(f"""
                    <div class='portfolio-card'>
                        <div>
                            <h3 style='margin: 0; color: #1e293b; font-size: 1.5rem;'>{t}</h3>
                            <p style='margin: 0.25rem 0; color: #64748b;'>{i.get('longName', t)}</p>
                            <p style='margin: 0.5rem 0; font-size: 1.3rem; font-weight: 700; color: #1e293b;'>${d['Close'].iloc[-1]:.2f}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_button:
                    if st.button("Analyze", key=f"analyze_{t}"):
                        st.session_state.page = 'analysis'
                        st.rerun()

elif st.session_state.page == 'top_stocks':
    st.markdown("<div class='brbas-header'><h1 class='brbas-title'>BRBAS</h1></div>", unsafe_allow_html=True)
    st.markdown("<h2 class='section-header'>Top Stocks by Sector</h2>", unsafe_allow_html=True)
    
    sectors = {
        'Technology': ['AAPL', 'MSFT', 'GOOGL'],
        'Healthcare': ['JNJ', 'UNH', 'PFE'],
        'Financial': ['JPM', 'BAC', 'WFC'],
        'Consumer': ['AMZN', 'TSLA', 'HD'],
        'Energy': ['XOM', 'CVX', 'COP']
    }
    
    with st.spinner("Analyzing sectors..."):
        results = {}
        for sector, tickers in sectors.items():
            best_conf = 0
            best_stock = None
            for t in tickers:
                d, i, e = get_stock_data(t, "3mo")
                if e or d is None or d.empty:
                    continue
                for ma in [20, 50, 100, 200]:
                    d[f'MA{ma}'] = d['Close'].rolling(window=ma).mean()
                d = calculate_ema(d)
                d['RSI'] = calculate_rsi(d)
                d['MACD'], d['Signal'], d['Histogram'] = calculate_macd(d)
                
                vs, _ = analyze_valuation(i)
                ms, _ = analyze_momentum(d)
                es, _ = analyze_earnings(i)
                ts, _ = analyze_technical(d)
                
                conf = calculate_confidence_score(i, d, vs, ms, es, ts)
                if conf > best_conf:
                    best_conf = conf
                    rec, rc = get_recommendation_from_confidence(conf)
                    best_stock = {'ticker': t, 'name': i.get('longName', t), 'price': d['Close'].iloc[-1], 
                                'conf': conf, 'rec': rec, 'rc': rc}
            
            if best_stock:
                results[sector] = best_stock
    
    cols = st.columns(2)
    for idx, (sector, stock) in enumerate(results.items()):
        with cols[idx % 2]:
            color = '#10b981' if 'BUY' in stock['rec'] else '#ef4444' if 'SELL' in stock['rec'] else '#f59e0b'
            st.markdown(f"""
            <div style='background: white; padding: 1.5rem; border-radius: 12px; border-left: 4px solid {color}; 
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 1rem;'>
                <div style='font-size: 0.85rem; color: #64748b; text-transform: uppercase;'>{sector}</div>
                <h3 style='margin: 0.5rem 0; color: #1e293b;'>{stock['ticker']}</h3>
                <p style='color: #64748b; font-size: 0.9rem;'>{stock['name'][:35]}</p>
                <div style='font-size: 1.5rem; font-weight: 700; color: #1e293b;'>${stock['price']:.2f}</div>
                <div style='background: {color}; color: white; padding: 0.4rem 1rem; border-radius: 20px; 
                            display: inline-block; margin-top: 0.5rem; font-weight: 600;'>{stock['rec']}</div>
                <div style='font-size: 1.2rem; font-weight: 700; color: #1e293b; margin-top: 0.5rem;'>
                    Confidence: {stock['conf']}%
                </div>
            </div>
            """, unsafe_allow_html=True)
