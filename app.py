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
        font-size: 7rem !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        letter-spacing: 2.5rem !important;
        margin: 0 !important;
        text-shadow: none !important;
    }
    
    .model-card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #3b82f6;
        margin: 1.5rem 0;
    }
    
    .section-header {
        font-size: 2rem;
        font-weight: 700;
        color: #1e293b;
        margin: 3rem 0 1.5rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 3px solid #3b82f6;
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

# Sidebar
with st.sidebar:
    st.markdown("<h1 class='sidebar-title'>BARBAS</h1>", unsafe_allow_html=True)
    if st.button("Stock Analysis"):
        st.session_state.page = 'analysis'

def search_ticker(query):
    mapping = {
        'apple': 'AAPL', 'microsoft': 'MSFT', 'google': 'GOOGL', 'amazon': 'AMZN',
        'tesla': 'TSLA', 'meta': 'META', 'nvidia': 'NVDA'
    }
    return mapping.get(query.lower(), query.upper())

def calculate_stochastic(high, low, close, k_period=14, d_period=3):
    """
    Calculate Stochastic Oscillator
    %K = (Current Close - Lowest Low) / (Highest High - Lowest Low) * 100
    %D = 3-period SMA of %K
    """
    lowest_low = low.rolling(window=k_period).min()
    highest_high = high.rolling(window=k_period).max()
    
    # Calculate %K
    k_percent = ((close - lowest_low) / (highest_high - lowest_low)) * 100
    
    # Calculate %D (3-period SMA of %K)
    d_percent = k_percent.rolling(window=d_period).mean()
    
    return k_percent, d_percent

@st.cache_data(ttl=300)
def get_stock_data(ticker, period):
    try:
        stock = yf.Ticker(ticker)
        return stock.history(period=period), stock.info, None
    except Exception as e:
        return None, None, str(e)

# MAIN PAGE
if st.session_state.page == 'analysis':
    st.markdown("<div class='brbas-header'><h1 class='brbas-title'>BARBAS</h1></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([4, 2])
    with col1:
        ticker = search_ticker(st.text_input("", "AAPL", placeholder="Ticker or company", label_visibility="collapsed"))
    with col2:
        period = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y", "2y"], index=3, label_visibility="collapsed")
    
    with st.spinner(f"Analyzing {ticker}..."):
        data, info, error = get_stock_data(ticker, period)
    
    if error or data is None or data.empty:
        st.error("Data unavailable")
        st.stop()
    
    # Define periods for stochastic
    k_period = 14
    d_period = 3
    
    # Calculate stochastic values
    data['n_high'] = data['High'].rolling(k_period).max()
    data['n_low'] = data['Low'].rolling(k_period).min()
    data['%K'] = (data['Close'] - data['n_low']) * 100 / (data['n_high'] - data['n_low'])
    data['%D'] = data['%K'].rolling(d_period).mean()
    
    # Also calculate using the function
    data['STOCH_K'], data['STOCH_D'] = calculate_stochastic(data['High'], data['Low'], data['Close'])
    
    # Display stock info
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%); padding: 2rem; border-radius: 16px; color: white; margin-bottom: 2rem;'>
        <h2 style='margin: 0; font-size: 2.5rem;'>{info.get('longName', ticker)}</h2>
        <p style='margin: 0.5rem 0; font-size: 1.2rem;'>{ticker} | {info.get('exchange', 'N/A')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display key metrics
    price = data['Close'].iloc[-1]
    change = ((data['Close'].iloc[-1] / data['Close'].iloc[0]) - 1) * 100
    
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Price", f"${price:.2f}", f"{change:+.2f}%")
    c2.metric("Market Cap", f"${info.get('marketCap', 0)/1e9:.1f}B")
    c3.metric("P/E", f"{info.get('trailingPE', 0):.2f}")
    c4.metric("Volume", f"{data['Volume'].iloc[-1]/1e6:.1f}M")
    c5.metric("52W Range", f"${info.get('fiftyTwoWeekLow', 0):.0f}-{info.get('fiftyTwoWeekHigh', 0):.0f}")
    
    # Create the stochastic chart
    st.markdown("<h2 class='section-header'>Stochastic Oscillator Chart</h2>", unsafe_allow_html=True)
    
    # Create our primary chart with two subplots
    fig = make_subplots(rows=2, cols=1, 
                        row_heights=[0.7, 0.3],
                        vertical_spacing=0.03,
                        subplot_titles=(f'{ticker} Price', 'Stochastic Oscillator'))
    
    # Create Candlestick chart with overlaid price line
    fig.append_trace(
        go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            increasing_line_color='#ff9900',
            decreasing_line_color='black',
            showlegend=False
        ), row=1, col=1
    )
    
    # Price Line
    fig.append_trace(
        go.Scatter(
            x=data.index,
            y=data['Open'],
            line=dict(color='#ff9900', width=1),
            name='Open',
        ), row=1, col=1
    )
    
    # Fast Signal (%K)
    fig.append_trace(
        go.Scatter(
            x=data.index,
            y=data['STOCH_K'],
            line=dict(color='#ff9900', width=2),
            name='%K (Fast)',
        ), row=2, col=1
    )
    
    # Slow signal (%D)
    fig.append_trace(
        go.Scatter(
            x=data.index,
            y=data['STOCH_D'],
            line=dict(color='#000000', width=2),
            name='%D (Slow)'
        ), row=2, col=1
    )
    
    # Extend y-axis for stochastic
    fig.update_yaxes(range=[-10, 110], row=2, col=1)
    
    # Add upper/lower bounds
    fig.add_hline(y=0, col=1, row=2, line_color="#666", line_width=2)
    fig.add_hline(y=100, col=1, row=2, line_color="#666", line_width=2)
    
    # Add overbought/oversold lines
    fig.add_hline(y=20, col=1, row=2, line_color='#336699', line_width=2, line_dash='dash')
    fig.add_hline(y=80, col=1, row=2, line_color='#336699', line_width=2, line_dash='dash')
    
    # Make it pretty
    layout = go.Layout(
        plot_bgcolor='#efefef',
        font_family='Monospace',
        font_color='#000000',
        font_size=14,
        height=800,
        xaxis=dict(rangeslider=dict(visible=False)),
        showlegend=True,
        hovermode='x unified'
    )
    
    fig.update_layout(layout)
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
    
    # Add interpretation
    st.markdown("<h2 class='section-header'>Stochastic Oscillator Interpretation</h2>", unsafe_allow_html=True)
    
    current_k = data['STOCH_K'].iloc[-1]
    current_d = data['STOCH_D'].iloc[-1]
    
    st.markdown(f"""
    <div class='model-card'>
        <h3>Current Values</h3>
        <p><strong>%K (Fast):</strong> {current_k:.2f}</p>
        <p><strong>%D (Slow):</strong> {current_d:.2f}</p>
        
        <h3>Signal Interpretation</h3>
        <p>
            {'<strong style="color: #ef4444;">OVERSOLD</strong> - The stock may be undervalued and due for a bounce.' if current_k < 20 else
             '<strong style="color: #10b981;">OVERBOUGHT</strong> - The stock may be overvalued and due for a pullback.' if current_k > 80 else
             '<strong>NEUTRAL</strong> - The stock is in a balanced trading range.'}
        </p>
        
        <h3>About the Stochastic Oscillator</h3>
        <p>
            The Stochastic Oscillator compares a stock's closing price to its price range over a specific period (typically 14 days). 
            It generates two lines: %K (fast) and %D (slow, which is a moving average of %K).
        </p>
        <ul>
            <li><strong>Below 20:</strong> Oversold condition - potential buying opportunity</li>
            <li><strong>Above 80:</strong> Overbought condition - potential selling opportunity</li>
            <li><strong>%K crosses above %D:</strong> Bullish signal</li>
            <li><strong>%K crosses below %D:</strong> Bearish signal</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
