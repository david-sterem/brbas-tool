import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="BARBAS", layout="wide", page_icon="📊", initial_sidebar_state="expanded")

# Revolut-inspired CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main {
        background: #000000;
        padding: 0;
    }
    
    .block-container {
        padding: 1.5rem 2rem;
        max-width: 1400px;
    }
    
    .barbas-header {
        background: #000000;
        padding: 2rem 0 1rem 0;
        margin: -1.5rem -2rem 2rem -2rem;
    }
    
    .barbas-title {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        letter-spacing: -0.02em !important;
        margin: 0 0 0.5rem 2rem !important;
    }
    
    .barbas-subtitle {
        font-size: 0.95rem;
        color: #666666;
        margin: 0 0 0 2rem;
        font-weight: 400;
    }
    
    .card {
        background: #0A0A0A;
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid #1a1a1a;
        margin: 1rem 0;
    }
    
    .card-title {
        font-size: 0.875rem;
        font-weight: 600;
        color: #999999;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background: #0A0A0A;
        padding: 1.25rem;
        border-radius: 12px;
        border: 1px solid #1a1a1a;
        transition: all 0.2s;
    }
    
    .metric-card:hover {
        border-color: #333333;
        transform: translateY(-2px);
    }
    
    .metric-label {
        font-size: 0.8rem;
        color: #666666;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff;
    }
    
    .metric-change {
        font-size: 0.875rem;
        font-weight: 600;
        margin-top: 0.25rem;
    }
    
    .positive {
        color: #00D084;
    }
    
    .negative {
        color: #FF3B69;
    }
    
    .section-header {
        font-size: 1.25rem;
        font-weight: 700;
        color: #ffffff;
        margin: 2.5rem 0 1rem 0;
        letter-spacing: -0.01em;
    }
    
    .signal-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
        margin: 0.5rem 0.5rem 0.5rem 0;
    }
    
    .signal-buy {
        background: rgba(0, 208, 132, 0.15);
        color: #00D084;
        border: 1px solid rgba(0, 208, 132, 0.3);
    }
    
    .signal-sell {
        background: rgba(255, 59, 105, 0.15);
        color: #FF3B69;
        border: 1px solid rgba(255, 59, 105, 0.3);
    }
    
    .signal-neutral {
        background: rgba(153, 153, 153, 0.15);
        color: #999999;
        border: 1px solid rgba(153, 153, 153, 0.3);
    }
    
    [data-testid="stSidebar"] {
        background: #0A0A0A;
        border-right: 1px solid #1a1a1a;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    [data-testid="stSidebar"] button {
        width: 100%;
        background: transparent;
        color: white !important;
        border: 1px solid #1a1a1a;
        padding: 0.875rem;
        border-radius: 8px;
        margin: 0.25rem 0;
        font-weight: 500;
        font-size: 0.95rem;
        transition: all 0.2s;
    }
    
    [data-testid="stSidebar"] button:hover {
        background: #1a1a1a;
        border-color: #333333;
    }
    
    .stTextInput input {
        background: #0A0A0A !important;
        border: 1px solid #1a1a1a !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        font-size: 1rem !important;
    }
    
    .stSelectbox > div > div {
        background: #0A0A0A !important;
        border: 1px solid #1a1a1a !important;
        color: white !important;
        border-radius: 8px !important;
    }
    
    .risk-bar {
        height: 8px;
        border-radius: 4px;
        margin-top: 0.5rem;
        background: #1a1a1a;
        overflow: hidden;
    }
    
    .risk-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.3s ease;
    }
    
    .info-text {
        color: #999999;
        font-size: 0.875rem;
        line-height: 1.6;
        margin: 0.5rem 0;
    }
    
    h1, h2, h3 {
        color: #ffffff !important;
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
    st.markdown("<div style='padding: 1rem 0;'><h2 style='margin:0; font-size: 1.5rem;'>BARBAS</h2><p style='color: #666; font-size: 0.85rem; margin: 0.25rem 0 0 0;'>Stock Analysis Platform</p></div>", unsafe_allow_html=True)
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    if st.button("📊 Stock Analysis"):
        st.session_state.page = 'analysis'
    if st.button("💼 Portfolio"):
        st.session_state.page = 'portfolio'
    if st.button("⚙️ Settings"):
        st.session_state.page = 'settings'

def search_ticker(query):
    mapping = {
        'apple': 'AAPL', 'microsoft': 'MSFT', 'google': 'GOOGL', 'alphabet': 'GOOGL',
        'amazon': 'AMZN', 'tesla': 'TSLA', 'meta': 'META', 'facebook': 'META',
        'nvidia': 'NVDA', 'netflix': 'NFLX', 'amd': 'AMD', 'intel': 'INTC',
        'disney': 'DIS', 'coca cola': 'KO', 'pepsi': 'PEP', 'walmart': 'WMT'
    }
    return mapping.get(query.lower(), query.upper())

def calculate_stochastic(high, low, close, k_period=14, d_period=3):
    lowest_low = low.rolling(window=k_period).min()
    highest_high = high.rolling(window=k_period).max()
    k_percent = ((close - lowest_low) / (highest_high - lowest_low)) * 100
    d_percent = k_percent.rolling(window=d_period).mean()
    return k_percent, d_percent

def calculate_moving_averages(data, short=50, long=200):
    data['MA_short'] = data['Close'].rolling(window=short).mean()
    data['MA_long'] = data['Close'].rolling(window=long).mean()
    return data

def detect_signals(data):
    signals = []
    
    # Stochastic signals
    current_k = data['STOCH_K'].iloc[-1]
    current_d = data['STOCH_D'].iloc[-1]
    prev_k = data['STOCH_K'].iloc[-2]
    prev_d = data['STOCH_D'].iloc[-2]
    
    if prev_k <= prev_d and current_k > current_d and current_k < 80:
        signals.append(('BUY', 'Stochastic Bullish Crossover', 'Strong'))
    elif prev_k >= prev_d and current_k < current_d and current_k > 20:
        signals.append(('SELL', 'Stochastic Bearish Crossover', 'Strong'))
    
    if current_k < 20:
        signals.append(('BUY', 'Oversold Condition', 'Medium'))
    elif current_k > 80:
        signals.append(('SELL', 'Overbought Condition', 'Medium'))
    
    # Moving average signals
    if 'MA_short' in data.columns and 'MA_long' in data.columns:
        current_short = data['MA_short'].iloc[-1]
        current_long = data['MA_long'].iloc[-1]
        prev_short = data['MA_short'].iloc[-2]
        prev_long = data['MA_long'].iloc[-2]
        
        if prev_short <= prev_long and current_short > current_long:
            signals.append(('BUY', 'Golden Cross', 'Very Strong'))
        elif prev_short >= prev_long and current_short < current_long:
            signals.append(('SELL', 'Death Cross', 'Very Strong'))
    
    return signals

def calculate_risk_metrics(data, info):
    returns = data['Close'].pct_change().dropna()
    volatility = returns.std() * np.sqrt(252) * 100
    
    # Risk categories
    if volatility < 20:
        risk_level = "Low"
        risk_color = "#00D084"
        risk_percent = 25
    elif volatility < 35:
        risk_level = "Medium"
        risk_color = "#FFA500"
        risk_percent = 50
    elif volatility < 50:
        risk_level = "High"
        risk_color = "#FF8C00"
        risk_percent = 75
    else:
        risk_level = "Very High"
        risk_color = "#FF3B69"
        risk_percent = 100
    
    beta = info.get('beta', 1.0)
    if beta is None:
        beta = 1.0
    
    return {
        'volatility': volatility,
        'risk_level': risk_level,
        'risk_color': risk_color,
        'risk_percent': risk_percent,
        'beta': beta
    }

def generate_investment_outlook(data, signals, risk_metrics):
    current_price = data['Close'].iloc[-1]
    price_change_1m = ((data['Close'].iloc[-1] / data['Close'].iloc[-20]) - 1) * 100 if len(data) > 20 else 0
    
    buy_signals = sum(1 for s in signals if s[0] == 'BUY')
    sell_signals = sum(1 for s in signals if s[0] == 'SELL')
    
    if buy_signals > sell_signals and risk_metrics['risk_level'] in ['Low', 'Medium']:
        outlook = "BULLISH"
        outlook_color = "#00D084"
        recommendation = "Consider buying with proper position sizing"
    elif sell_signals > buy_signals or risk_metrics['risk_level'] == 'Very High':
        outlook = "BEARISH"
        outlook_color = "#FF3B69"
        recommendation = "Consider reducing position or waiting for better entry"
    else:
        outlook = "NEUTRAL"
        outlook_color = "#999999"
        recommendation = "Hold current positions and monitor for clearer signals"
    
    return {
        'outlook': outlook,
        'color': outlook_color,
        'recommendation': recommendation,
        'confidence': min(100, abs(buy_signals - sell_signals) * 25 + 50)
    }

@st.cache_data(ttl=300)
def get_stock_data(ticker, period):
    try:
        stock = yf.Ticker(ticker)
        return stock.history(period=period), stock.info, None
    except Exception as e:
        return None, None, str(e)

# MAIN ANALYSIS PAGE
if st.session_state.page == 'analysis':
    st.markdown("<div class='barbas-header'><h1 class='barbas-title'>BARBAS</h1><p class='barbas-subtitle'>Professional Stock Analysis & Trading Signals</p></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        ticker = search_ticker(st.text_input("", "AAPL", placeholder="Search ticker or company name...", label_visibility="collapsed"))
    with col2:
        period = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3, label_visibility="collapsed")
    
    with st.spinner(f"Analyzing {ticker}..."):
        data, info, error = get_stock_data(ticker, period)
    
    if error or data is None or data.empty:
        st.markdown("<div class='card'><p style='color: #FF3B69; text-align: center;'>Unable to fetch data for this ticker</p></div>", unsafe_allow_html=True)
        st.stop()
    
    # Calculate indicators
    data['STOCH_K'], data['STOCH_D'] = calculate_stochastic(data['High'], data['Low'], data['Close'])
    data = calculate_moving_averages(data)
    
    # Detect signals
    signals = detect_signals(data)
    risk_metrics = calculate_risk_metrics(data, info)
    outlook = generate_investment_outlook(data, signals, risk_metrics)
    
    # Stock header
    price = data['Close'].iloc[-1]
    price_open = data['Open'].iloc[0]
    change = price - price_open
    change_pct = (change / price_open) * 100
    
    st.markdown(f"""
    <div class='card'>
        <h2 style='margin: 0 0 0.5rem 0; font-size: 1.75rem; font-weight: 700;'>{info.get('longName', ticker)}</h2>
        <p style='margin: 0 0 1.5rem 0; color: #666; font-size: 0.95rem;'>{ticker} • {info.get('exchange', 'N/A')}</p>
        <div style='display: flex; align-items: baseline; gap: 1rem;'>
            <span style='font-size: 3rem; font-weight: 700; color: white;'>${price:.2f}</span>
            <span class='{"positive" if change >= 0 else "negative"}' style='font-size: 1.25rem; font-weight: 600;'>
                {'+' if change >= 0 else ''}{change:.2f} ({'+' if change_pct >= 0 else ''}{change_pct:.2f}%)
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>MARKET CAP</div>
            <div class='metric-value'>${info.get('marketCap', 0)/1e9:.1f}B</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        pe_ratio = info.get('trailingPE', 0)
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>P/E RATIO</div>
            <div class='metric-value'>{pe_ratio:.2f if pe_ratio else 'N/A'}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        volume = data['Volume'].iloc[-1]
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>VOLUME</div>
            <div class='metric-value'>{volume/1e6:.1f}M</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>52W HIGH</div>
            <div class='metric-value'>${info.get('fiftyTwoWeekHigh', 0):.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>52W LOW</div>
            <div class='metric-value'>${info.get('fiftyTwoWeekLow', 0):.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Investment Outlook Section
    st.markdown("<h2 class='section-header'>Investment Outlook</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div class='card'>
            <div style='display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;'>
                <div style='background: {outlook['color']}22; color: {outlook['color']}; padding: 0.5rem 1.5rem; border-radius: 20px; font-weight: 700; font-size: 1.1rem;'>
                    {outlook['outlook']}
                </div>
                <div style='color: #666; font-size: 0.9rem;'>Confidence: {outlook['confidence']}%</div>
            </div>
            <p class='info-text' style='font-size: 1rem; color: #ccc; margin-bottom: 1rem;'>{outlook['recommendation']}</p>
            
            <div style='margin-top: 1.5rem;'>
                <div class='card-title'>ACTIVE SIGNALS</div>
                {''.join([f"<span class='signal-badge signal-{s[0].lower()}'>{s[0]}: {s[1]} ({s[2]})</span>" for s in signals]) if signals else "<p class='info-text'>No active signals detected</p>"}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='card'>
            <div class='card-title'>RISK ASSESSMENT</div>
            <div style='margin-bottom: 1.5rem;'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;'>
                    <span style='color: white; font-weight: 600; font-size: 1.1rem;'>{risk_metrics['risk_level']}</span>
                    <span style='color: #666; font-size: 0.9rem;'>{risk_metrics['volatility']:.1f}% volatility</span>
                </div>
                <div class='risk-bar'>
                    <div class='risk-fill' style='width: {risk_metrics['risk_percent']}%; background: {risk_metrics['risk_color']};'></div>
                </div>
            </div>
            <div style='margin-top: 1.5rem;'>
                <div style='color: #666; font-size: 0.85rem; margin-bottom: 0.25rem;'>Beta</div>
                <div style='color: white; font-size: 1.25rem; font-weight: 600;'>{risk_metrics['beta']:.2f}</div>
                <p class='info-text' style='margin-top: 0.5rem; font-size: 0.8rem;'>
                    {"Less volatile than market" if risk_metrics['beta'] < 1 else "More volatile than market" if risk_metrics['beta'] > 1 else "Moves with market"}
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Chart
    st.markdown("<h2 class='section-header'>Price & Technical Indicators</h2>", unsafe_allow_html=True)
    
    fig = make_subplots(
        rows=2, cols=1,
        row_heights=[0.7, 0.3],
        vertical_spacing=0.05,
        subplot_titles=('Price Chart', 'Stochastic Oscillator')
    )
    
    # Candlestick
    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            increasing_line_color='#00D084',
            decreasing_line_color='#FF3B69',
            increasing_fillcolor='#00D084',
            decreasing_fillcolor='#FF3B69',
            showlegend=False,
            name='Price'
        ), row=1, col=1
    )
    
    # Moving Averages
    if 'MA_short' in data.columns:
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['MA_short'],
                line=dict(color='#3B82F6', width=1.5),
                name='MA 50',
            ), row=1, col=1
        )
    
    if 'MA_long' in data.columns:
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['MA_long'],
                line=dict(color='#8B5CF6', width=1.5),
                name='MA 200',
            ), row=1, col=1
        )
    
    # Stochastic %K
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['STOCH_K'],
            line=dict(color='#00D084', width=2),
            name='%K',
        ), row=2, col=1
    )
    
    # Stochastic %D
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['STOCH_D'],
            line=dict(color='#3B82F6', width=2),
            name='%D'
        ), row=2, col=1
    )
    
    # Stochastic levels
    fig.add_hline(y=80, col=1, row=2, line_color='#FF3B69', line_width=1, line_dash='dash', opacity=0.5)
    fig.add_hline(y=20, col=1, row=2, line_color='#00D084', line_width=1, line_dash='dash', opacity=0.5)
    fig.add_hline(y=50, col=1, row=2, line_color='#666666', line_width=1, line_dash='dot', opacity=0.3)
    
    # Layout
    fig.update_layout(
        plot_bgcolor='#0A0A0A',
        paper_bgcolor='#0A0A0A',
        font=dict(family='Inter, sans-serif', color='#ffffff', size=12),
        height=700,
        xaxis=dict(
            rangeslider=dict(visible=False),
            gridcolor='#1a1a1a',
            showgrid=True
        ),
        xaxis2=dict(gridcolor='#1a1a1a', showgrid=True),
        yaxis=dict(gridcolor='#1a1a1a', showgrid=True),
        yaxis2=dict(gridcolor='#1a1a1a', showgrid=True, range=[-5, 105]),
        showlegend=True,
        legend=dict(
            bgcolor='rgba(0,0,0,0)',
            bordercolor='#1a1a1a',
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        hovermode='x unified',
        margin=dict(l=0, r=0, t=60, b=0)
    )
    
    fig.update_xaxes(showline=True, linewidth=1, linecolor='#1a1a1a')
    fig.update_yaxes(showline=True, linewidth=1, linecolor='#1a1a1a')
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Trading Strategy
    st.markdown("<h2 class='section-header'>Trading Strategy Recommendations</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        current_k = data['STOCH_K'].iloc[-1]
        current_d = data['STOCH_D'].iloc[-1]
        
        st.markdown(f"""
        <div class='card'>
            <div class='card-title'>STOCHASTIC ANALYSIS</div>
            <div style='margin-bottom: 1rem;'>
                <div style='color: #666; font-size: 0.85rem;'>%K (Fast Signal)</div>
                <div style='color: white; font-size: 1.5rem; font-weight: 600;'>{current_k:.2f}</div>
            </div>
            <div style='margin-bottom: 1.5rem;'>
                <div style='color: #666; font-size: 0.85rem;'>%D (Slow Signal)</div>
                <div style='color: white; font-size: 1.5rem; font-weight: 600;'>{current_d:.2f}</div>
            </div>
            <p class='info-text'>
                {'🟢 <strong style="color: #00D084;">OVERSOLD ZONE</strong> - Stock may be undervalued. Consider accumulating positions.' if current_k < 20 
                else '🔴 <strong style="color: #FF3B69;">OVERBOUGHT ZONE</strong> - Stock may be overvalued. Consider taking profits.' if current_k > 80
                else '⚪ <strong>NEUTRAL ZONE</strong> - Wait for clearer signals before entering positions.'}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='card'>
            <div class='card-title'>POSITION SIZING GUIDE</div>
            <p class='info-text' style='margin-bottom: 1rem;'>Based on {risk_metrics['risk_level']} risk level:</p>
            <div style='margin-bottom: 0.75rem;'>
                <div style='display: flex; justify-content: space-between;'>
                    <span style='color: #666;'>Conservative</span>
                    <span style='color: white; font-weight: 600;'>{"2-3%" if risk_metrics['risk_level'] == 'Low' else "1-2%" if risk_metrics['risk_level'] == 'Medium' else "0.5-1%" if risk_metrics['risk_level'] == 'High' else "<0.5%"}</span>
                </div>
            </div>
            <div style='margin-bottom: 0.75rem;'>
                <div style='display: flex; justify-content: space-between;'>
                    <span style='color: #666;'>Moderate</span>
                    <span style='color: white; font-weight: 600;'>{"5-7%" if risk_metrics['risk_level'] == 'Low' else "3-5%" if risk_metrics['risk_level'] == 'Medium' else "1-3%" if risk_metrics['risk_level'] == 'High' else "0.5-1%"}</span>
                </div>
            </div>
            <div>
                <div style='display: flex; justify-content: space-between;'>
                    <span style='color: #666;'>Aggressive</span>
                    <span style='color: white; font-weight: 600;'>{"10-15%" if risk_metrics['risk_level'] == 'Low' else "7-10%" if risk_metrics['risk_level'] == 'Medium' else "3-5%" if risk_metrics['risk_level'] == 'High' else "1-2%"}</span>
                </div>
            </div>
            <p class='info-text' style='margin-top: 1rem; font-size: 0.75rem; color: #666;'>
                * Percentages represent allocation of total portfolio value
            </p>
        </div>
        """, unsafe_allow_html=True)
