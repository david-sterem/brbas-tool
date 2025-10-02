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

st.set_page_config(page_title="BRBAS - Professional Stock Analysis", layout="wide", page-icon="📊")

# Professional Light Theme CSS
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
        padding: 3rem 0 2rem 0;
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        margin: -2rem -3rem 2rem -3rem;
        box-shadow: 0 4px 20px rgba(30, 64, 175, 0.15);
    }
    
    .brbas-title {
        font-size: 4rem;
        font-weight: 800;
        color: white;
        letter-spacing: 0.5rem;
        margin: 0;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    
    .brbas-subtitle {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.9);
        letter-spacing: 0.3rem;
        margin-top: 0.5rem;
        font-weight: 300;
    }
    
    .search-container {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
        margin-bottom: 2rem;
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
    
    .confidence-label {
        font-size: 0.9rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 600;
        margin-top: 0.5rem;
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
        line-height: 1.7;
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
    
    .company-ticker {
        font-size: 1.2rem;
        opacity: 0.9;
        font-weight: 600;
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
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        border: 2px solid #e2e8f0;
        color: #64748b;
        font-weight: 600;
        transition: all 0.2s;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        border-color: #3b82f6;
        background: #f8fafc;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        color: white;
        border-color: #3b82f6;
    }
    
    .disclaimer {
        background: #fee2e2;
        border: 2px solid #ef4444;
        padding: 2rem;
        border-radius: 12px;
        margin: 3rem 0;
    }
    
    .disclaimer-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #991b1b;
        margin-bottom: 1rem;
    }
    
    .disclaimer-text {
        color: #7f1d1d;
        line-height: 1.7;
        font-size: 0.95rem;
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
</style>
""", unsafe_allow_html=True)

# BRBAS Header
st.markdown("""
<div class='brbas-header'>
    <h1 class='brbas-title'>BRBAS</h1>
    <p class='brbas-subtitle'>PROFESSIONAL STOCK ANALYSIS PLATFORM</p>
</div>
""", unsafe_allow_html=True)

# Search and Filter Section
with st.container():
    st.markdown("<div class='search-container'>", unsafe_allow_html=True)
    
    col_search1, col_search2, col_search3 = st.columns([3, 2, 2])
    
    with col_search1:
        ticker = st.text_input("", value="AAPL", placeholder="Enter stock ticker (e.g., AAPL, TSLA, GOOGL)", label_visibility="collapsed").upper()
    
    with col_search2:
        period = st.selectbox("Time Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)
    
    with col_search3:
        analysis_depth = st.selectbox("Analysis Depth", ["Standard", "Detailed", "Advanced"], index=1)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Function definitions
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

def generate_advice(confidence, recommendation, ticker, info):
    company_name = info.get('longName', ticker)
    
    if confidence >= 75:
        return f"Considering {company_name}'s strong fundamentals, positive momentum indicators, and robust earnings trajectory, I recommend **accumulating a position** in {ticker}. The data suggests significant upside potential with manageable risk."
    elif confidence >= 60:
        return f"Based on {company_name}'s favorable valuation metrics and positive technical indicators, I recommend **initiating or adding to a position** in {ticker}. Monitor for any changes in market conditions."
    elif confidence >= 40:
        return f"Given {company_name}'s mixed signals across valuation, momentum, and earnings metrics, I recommend **holding existing positions** in {ticker} and waiting for clearer directional signals before making additional moves."
    elif confidence >= 25:
        return f"Considering {company_name}'s deteriorating fundamentals and weak technical indicators, I recommend **reducing exposure** to {ticker}. Consider reallocating capital to stronger opportunities."
    else:
        return f"Given {company_name}'s significant headwinds across multiple analysis dimensions, I recommend **exiting positions** in {ticker}. The risk-reward profile is currently unfavorable."

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

# Load and process data
with st.spinner(f"🔍 Analyzing {ticker}..."):
    data, info, error = get_stock_data(ticker, period)

if error:
    st.error(f"❌ Error: {error}")
    st.stop()

if data is None or data.empty:
    st.error(f"❌ No data available for {ticker}")
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
advice = generate_advice(confidence, recommendation, ticker, info)

# Company Header
st.markdown(f"""
<div class='company-header'>
    <div class='company-name'>{info.get('longName', ticker)}</div>
    <div class='company-ticker'>{ticker} • {info.get('exchange', 'N/A')}</div>
    <div class='company-description'>{info.get('longBusinessSummary', 'No description available.')[:300]}...</div>
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

# Confidence Card
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
st.markdown("<h2 class='section-header'>📈 Price Performance</h2>", unsafe_allow_html=True)

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

# Analysis Tabs
st.markdown("<h2 class='section-header'>🔬 Detailed Analysis Models</h2>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📊 Valuation", "🚀 Momentum", "💰 Earnings", "⚡ Technical"])

with tab1:
    st.markdown(f"### Score: **{valuation_score+6}/12**")
    for detail in valuation_details:
        st.markdown(f"- {detail}")
    
    vcol1, vcol2, vcol3, vcol4 = st.columns(4)
    with vcol1:
        st.metric("P/E Ratio", f"{info.get('trailingPE', 0):.2f}" if info.get('trailingPE') else "N/A")
    with vcol2:
        st.metric("PEG Ratio", f"{info.get('pegRatio', 0):.2f}" if info.get('pegRatio') else "N/A")
    with vcol3:
        st.metric("P/B Ratio", f"{info.get('priceToBook', 0):.2f}" if info.get('priceToBook') else "N/A")
    with vcol4:
        st.metric("EV/EBITDA", f"{info.get('enterpriseToEbitda', 0):.2f}" if info.get('enterpriseToEbitda') else "N/A")

with tab2:
    st.markdown(f"### Score: **{momentum_score+6}/12**")
    for detail in momentum_details:
        st.markdown(f"- {detail}")
    
    mcol1, mcol2, mcol3, mcol4 = st.columns(4)
    with mcol1:
        ema8 = data['EMA8'].iloc[-1] if 'EMA8' in data.columns and pd.notna(data['EMA8'].iloc[-1]) else None
        st.metric("8-Day EMA", f"${ema8:.2f}" if ema8 else "N/A")
    with mcol2:
        ema21 = data['EMA21'].iloc[-1] if 'EMA21' in data.columns and pd.notna(data['EMA21'].iloc[-1]) else None
        st.metric("21-Day EMA", f"${ema21:.2f}" if ema21 else "N/A")
    with mcol3:
        ma50 = data['MA50'].iloc[-1] if 'MA50' in data.columns and pd.notna(data['MA50'].iloc[-1]) else None
        st.metric("50-Day MA", f"${ma50:.2f}" if ma50 else "N/A")
    with mcol4:
        ma200 = data['MA200'].iloc[-1] if 'MA200' in data.columns and pd.notna(data['MA200'].iloc[-1]) else None
        st.metric("200-Day MA", f"${ma200:.2f}" if ma200 else "N/A")

with tab3:
    st.markdown(f"### Score: **{earnings_score+6}/12**")
    for detail in earnings_details:
        st.markdown(f"- {detail}")
    
    ecol1, ecol2, ecol3, ecol4 = st.columns(4)
    with ecol1:
        st.metric("EPS (TTM)", f"${info.get('trailingEps', 0):.2f}" if info.get('trailingEps') else "N/A")
    with ecol2:
        st.metric("Forward EPS", f"${info.get('forwardEps', 0):.2f}" if info.get('forwardEps') else "N/A")
    with ecol3:
        profit_margin = info.get('profitMargins', None)
        st.metric("Profit Margin", f"{profit_margin*100:.1f}%" if profit_margin else "N/A")
    with ecol4:
        roe = info.get('returnOnEquity', None)
        st.metric("ROE", f"{roe*100:.1f}%" if roe else "N/A")

with tab4:
    st.markdown(f"### Score: **{technical_score+6}/12**")
    for detail in technical_details:
        st.markdown(f"- {detail}")
    
    tcol1, tcol2, tcol3, tcol4 = st.columns(4)
    with tcol1:
        current_rsi = data['RSI'].iloc[-1] if 'RSI' in data.columns and pd.notna(data['RSI'].iloc[-1]) else None
        st.metric("RSI (14)", f"{current_rsi:.1f}" if current_rsi else "N/A")
    with tcol2:
        current_macd = data['MACD'].iloc[-1] if 'MACD' in data.columns and pd.notna(data['MACD'].iloc[-1]) else None
        st.metric("MACD", f"{current_macd:.2f}" if current_macd else "N/A")
    with tcol3:
        daily_vol = data['Close'].pct_change().std() * 100
        st.metric("Daily Volatility", f"{daily_vol:.2f}%")
    with tcol4:
        beta = info.get('beta', None)
        st.metric("Beta", f"{beta:.2f}" if beta else "N/A")

# Statistics
st.markdown("<h2 class='section-header'>📋 Detailed Statistics</h2>", unsafe_allow_html=True)

with st.expander("📊 Price & Volume Statistics", expanded=False):
    stat_col1, stat_col2, stat_col3 = st.columns(3)
    
    with stat_col1:
        st.markdown("**Price Statistics**")
        st.dataframe(pd.DataFrame({
            'Metric': ['Mean', 'Median', 'Std Dev', 'Min', 'Max'],
            'Value': [
                f"${data['Close'].mean():.2f}",
                f"${data['Close'].median():.2f}",
                f"${data['Close'].std():.2f}",
                f"${data['Close'].min():.2f}",
                f"${data['Close'].max():.2f}"
            ]
        }), hide_index=True, use_container_width=True)
    
    with stat_col2:
        st.markdown("**Volume Statistics**")
        st.dataframe(pd.DataFrame({
            'Metric': ['Mean', 'Median', 'Max', 'Min', 'Total'],
            'Value': [
                f"{data['Volume'].mean():,.0f}",
                f"{data['Volume'].median():,.0f}",
                f"{data['Volume'].max():,.0f}",
                f"{data['Volume'].min():,.0f}",
                f"{data['Volume'].sum():,.0f}"
            ]
        }), hide_index=True, use_container_width=True)
    
    with stat_col3:
        st.markdown("**Volatility Metrics**")
        daily_returns = data['Close'].pct_change()
        st.dataframe(pd.DataFrame({
            'Metric': ['Daily Vol', 'Annual Vol', 'Max Drawdown', 'Sharpe Ratio'],
            'Value': [
                f"{daily_returns.std()*100:.2f}%",
                f"{daily_returns.std()*np.sqrt(252)*100:.2f}%",
                f"{((data['Close'] / data['Close'].cummax() - 1).min()*100):.2f}%",
                f"{(daily_returns.mean() / daily_returns.std() * np.sqrt(252)):.2f}" if daily_returns.std() != 0 else "N/A"
            ]
        }), hide_index=True, use_container_width=True)

with st.expander("💼 Fundamental Data", expanded=False):
    fund_col1, fund_col2 = st.columns(2)
    
    with fund_col1:
        st.markdown("**Financial Metrics**")
        st.markdown(f"- **Revenue (TTM):** ${info.get('totalRevenue', 0)/1e9:.2f}B")
        st.markdown(f"- **Gross Profit:** ${info.get('grossProfits', 0)/1e9:.2f}B")
        st.markdown(f"- **EBITDA:** ${info.get('ebitda', 0)/1e9:.2f}B")
        st.markdown(f"- **Operating Cash Flow:** ${info.get('operatingCashflow', 0)/1e9:.2f}B")
        st.markdown(f"- **Free Cash Flow:** ${info.get('freeCashflow', 0)/1e9:.2f}B")
    
    with fund_col2:
        st.markdown("**Balance Sheet**")
        st.markdown(f"- **Total Cash:** ${info.get('totalCash', 0)/1e9:.2f}B")
        st.markdown(f"- **Total Debt:** ${info.get('totalDebt', 0)/1e9:.2f}B")
        st.markdown(f"- **Debt to Equity:** {info.get('debtToEquity', 0):.2f}")
        st.markdown(f"- **Current Ratio:** {info.get('currentRatio', 0):.2f}")
        st.markdown(f"- **Quick Ratio:** {info.get('quickRatio', 0):.2f}")

with st.expander("🎯 Analyst Ratings & Targets", expanded=False):
    analyst_col1, analyst_col2, analyst_col3 = st.columns(3)
    
    with analyst_col1:
        recommendation = info.get('recommendationKey', 'N/A')
        st.metric("Analyst Rating", recommendation.replace('_', ' ').title() if recommendation != 'N/A' else 'N/A')
    
    with analyst_col2:
        target_high = info.get('targetHighPrice', None)
        st.metric("Target High", f"${target_high:.2f}" if target_high else "N/A")
    
    with analyst_col3:
        target_low = info.get('targetLowPrice', None)
        st.metric("Target Low", f"${target_low:.2f}" if target_low else "N/A")

# Disclaimer
st.markdown("""
<div class='disclaimer'>
    <div class='disclaimer-title'>⚠️ IMPORTANT LEGAL DISCLAIMER</div>
    <div class='disclaimer-text'>
        <strong>This platform is for educational and informational purposes only.</strong><br><br>
        
        The information provided by BRBAS does NOT constitute financial, investment, trading, or any other type of professional advice. All data, analysis, models, and recommendations are presented as hypothetical tools for learning purposes only.<br><br>
        
        <strong>You are solely responsible for your own investment decisions.</strong> Past performance does not guarantee future results. All investments carry risk, including the potential loss of principal. Market conditions can change rapidly, and no analysis or model can predict future performance with certainty.<br><br>
        
        Before making any investment decisions, you should:<br>
        • Conduct your own independent research and due diligence<br>
        • Consult with a qualified financial advisor<br>
        • Consider your own financial situation, goals, and risk tolerance<br>
        • Understand that you may lose some or all of your investment<br><br>
        
        <strong>Data Sources:</strong> This platform aggregates data from Yahoo Finance and other publicly available sources. While we strive for accuracy, we cannot guarantee the completeness, accuracy, or timeliness of any information presented. All data should be independently verified.<br><br>
        
        <strong>No Liability:</strong> The creators, operators, and contributors of BRBAS assume no liability for any trading losses, investment decisions, or financial outcomes resulting from the use of this platform.<br><br>
        
        By using this platform, you acknowledge that you understand and accept these terms and that you are using this tool entirely at your own risk.
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("<div style='text-align: center; padding: 2rem; color: #64748b; font-size: 0.9rem;'>", unsafe_allow_html=True)
st.markdown("**BRBAS** — Professional Stock Analysis Platform | Built with Python, Streamlit & yFinance")
st.markdown(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.markdown("</div>", unsafe_allow_html=True)
