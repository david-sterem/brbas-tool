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

st.set_page_config(page_title="BRBAS", layout="wide", page_icon="📊")

# Session state
if 'page' not in st.session_state:
    st.session_state.page = 'analysis'

# Sidebar
with st.sidebar:
    st.title("BARBAS")
    if st.button("Stock Analysis"):
        st.session_state.page = 'analysis'

def search_ticker(query):
    """Map company names to tickers"""
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
    """Fetch stock data from Yahoo Finance"""
    try:
        stock = yf.Ticker(ticker)
        return stock.history(period=period), stock.info, None
    except Exception as e:
        return None, None, str(e)

# MAIN PAGE
if st.session_state.page == 'analysis':
    st.title("BARBAS")
    
    col1, col2 = st.columns([4, 2])
    with col1:
        ticker = search_ticker(st.text_input("Ticker or Company", "AAPL"))
    with col2:
        period = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y", "2y"], index=3)
    
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
    st.header(f"{info.get('longName', ticker)}")
    st.text(f"{ticker} | {info.get('exchange', 'N/A')}")
    
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
    st.subheader("Stochastic Oscillator Chart")
    
    # Create chart with two subplots
    fig = make_subplots(rows=2, cols=1, 
                        row_heights=[0.7, 0.3],
                        vertical_spacing=0.03,
                        subplot_titles=(f'{ticker} Price', 'Stochastic Oscillator'))
    
    # Candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='Price'
        ), row=1, col=1
    )
    
    # %K (Fast Signal)
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['STOCH_K'],
            line=dict(color='orange', width=2),
            name='%K (Fast)',
        ), row=2, col=1
    )
    
    # %D (Slow signal)
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['STOCH_D'],
            line=dict(color='black', width=2),
            name='%D (Slow)'
        ), row=2, col=1
    )
    
    # Set y-axis range for stochastic
    fig.update_yaxes(range=[-10, 110], row=2, col=1)
    
    # Add reference lines
    fig.add_hline(y=0, col=1, row=2, line_color="gray", line_width=2)
    fig.add_hline(y=100, col=1, row=2, line_color="gray", line_width=2)
    fig.add_hline(y=20, col=1, row=2, line_color='blue', line_width=2, line_dash='dash')
    fig.add_hline(y=80, col=1, row=2, line_color='blue', line_width=2, line_dash='dash')
    
    # Update layout
    fig.update_layout(
        height=800,
        xaxis=dict(rangeslider=dict(visible=False)),
        showlegend=True,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add interpretation
    st.subheader("Stochastic Oscillator Interpretation")
    
    current_k = data['STOCH_K'].iloc[-1]
    current_d = data['STOCH_D'].iloc[-1]
    
    st.write(f"**Current Values:**")
    st.write(f"- %K (Fast): {current_k:.2f}")
    st.write(f"- %D (Slow): {current_d:.2f}")
    
    st.write("**Signal Interpretation:**")
    if current_k < 20:
        st.write("OVERSOLD - The stock may be undervalued and due for a bounce.")
    elif current_k > 80:
        st.write("OVERBOUGHT - The stock may be overvalued and due for a pullback.")
    else:
        st.write("NEUTRAL - The stock is in a balanced trading range.")
    
    st.write("**About the Stochastic Oscillator:**")
    st.write("""
    The Stochastic Oscillator compares a stock's closing price to its price range over a specific period (typically 14 days). 
    It generates two lines: %K (fast) and %D (slow, which is a moving average of %K).
    
    - Below 20: Oversold condition - potential buying opportunity
    - Above 80: Overbought condition - potential selling opportunity
    - %K crosses above %D: Bullish signal
    - %K crosses below %D: Bearish signal
    """)
