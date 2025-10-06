import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from scipy import stats
import warnings
import time

warnings.filterwarnings('ignore')

st.set_page_config(page_title="BARBAS", layout="wide", page_icon="📊")

if 'page' not in st.session_state:
    st.session_state.page = 'analysis'
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []

def add_to_portfolio(ticker, current_k, current_d, k_momentum, trend):
    for stock in st.session_state.portfolio:
        if stock['ticker'] == ticker:
            stock['stoch_k'] = current_k
            stock['stoch_d'] = current_d
            stock['momentum'] = k_momentum
            stock['trend'] = trend
            stock['position'] = "OVERSOLD" if current_k < 20 else "OVERBOUGHT" if current_k > 80 else "NEUTRAL"
            stock['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M")
            return False
    
    st.session_state.portfolio.append({
        'ticker': ticker,
        'stoch_k': current_k,
        'stoch_d': current_d,
        'momentum': k_momentum,
        'trend': trend,
        'position': "OVERSOLD" if current_k < 20 else "OVERBOUGHT" if current_k > 80 else "NEUTRAL",
        'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    return True

def remove_from_portfolio(ticker):
    st.session_state.portfolio = [s for s in st.session_state.portfolio if s['ticker'] != ticker]

def search_ticker(query):
    mapping = {
        'apple': 'AAPL', 'microsoft': 'MSFT', 'google': 'GOOGL', 'amazon': 'AMZN',
        'tesla': 'TSLA', 'meta': 'META', 'nvidia': 'NVDA'
    }
    return mapping.get(query.lower(), query.upper())

def calculate_stochastic(high, low, close, k_period=14, d_period=3):
    lowest_low = low.rolling(window=k_period).min()
    highest_high = high.rolling(window=k_period).max()
    k_percent = ((close - lowest_low) / (highest_high - lowest_low)) * 100
    d_percent = k_percent.rolling(window=d_period).mean()
    return k_percent, d_percent

def calculate_stochastic_score(k, d, momentum, trend):
    score = 50
    if k < 20:
        score += 20
    elif k > 80:
        score -= 20
    if k > d:
        score += 10
    else:
        score -= 10
    if momentum > 10:
        score += 15
    elif momentum > 0:
        score += 5
    elif momentum > -10:
        score -= 5
    else:
        score -= 15
    if trend == "bullish":
        score += 5
    elif trend == "bearish":
        score -= 5
    return max(0, min(100, score))

def get_sector_from_info(info):
    sector = info.get('sector', '').lower()
    industry = info.get('industry', '').lower()
    
    if 'financial' in sector or 'bank' in industry or 'insurance' in industry:
        return 'Financial Services'
    elif 'technology' in sector or 'software' in industry or 'semiconductor' in industry:
        return 'Technology'
    elif 'industrial' in sector or 'aerospace' in industry or 'defense' in industry:
        return 'Industrial'
    elif 'energy' in sector or 'oil' in industry or 'gas' in industry:
        return 'Energy'
    elif 'real estate' in sector or 'reit' in industry:
        return 'Real Estate'
    elif 'consumer' in sector or 'retail' in industry or 'automotive' in industry:
        return 'Consumer Cyclical'
    elif 'consumer defensive' in sector or 'consumer staples' in sector:
        return 'Consumer Defensive'
    elif 'communication' in sector or 'media' in industry or 'telecom' in industry:
        return 'Communication Services'
    elif 'basic materials' in sector or 'materials' in sector:
        return 'Basic Materials'
    elif 'utilities' in sector or 'utility' in industry:
        return 'Utilities'
    else:
        return 'Other'

def analyze_fundamentals(info, sector):
    analysis = {
        'sector': sector,
        'metrics': {},
        'strengths': [],
        'weaknesses': [],
        'rating': 0,
        'recommendation': ''
    }
    
    pe_ratio = info.get('trailingPE', info.get('forwardPE'))
    
    if sector == 'Financial Services':
        roe = info.get('returnOnEquity', 0) * 100 if info.get('returnOnEquity') else None
        book_value = info.get('bookValue')
        pb_ratio = info.get('priceToBook')
        
        analysis['metrics'] = {
            'P/E Ratio': f"{pe_ratio:.2f}" if pe_ratio else 'N/A',
            'ROE': f"{roe:.1f}%" if roe else 'N/A',
            'Price-to-Book': f"{pb_ratio:.2f}" if pb_ratio else 'N/A',
            'Book Value': f"${book_value:.2f}" if book_value else 'N/A'
        }
        
        score = 50
        if roe and roe > 15:
            analysis['strengths'].append(f"Strong ROE of {roe:.1f}%")
            score += 15
        elif roe and roe < 8:
            analysis['weaknesses'].append(f"Low ROE of {roe:.1f}%")
            score -= 10
        
        if pb_ratio and pb_ratio < 1.5:
            analysis['strengths'].append(f"Attractive P/B of {pb_ratio:.2f}")
            score += 10
        elif pb_ratio and pb_ratio > 3:
            analysis['weaknesses'].append(f"High P/B of {pb_ratio:.2f}")
            score -= 10
        
        analysis['rating'] = max(0, min(100, score))
        
    elif sector == 'Technology':
        revenue_growth = info.get('revenueGrowth', 0) * 100 if info.get('revenueGrowth') else None
        gross_margin = info.get('grossMargins', 0) * 100 if info.get('grossMargins') else None
        free_cash_flow = info.get('freeCashflow', 0)
        
        analysis['metrics'] = {
            'P/E Ratio': f"{pe_ratio:.2f}" if pe_ratio else 'N/A',
            'Revenue Growth': f"{revenue_growth:.1f}%" if revenue_growth else 'N/A',
            'Gross Margin': f"{gross_margin:.1f}%" if gross_margin else 'N/A',
            'Free Cash Flow': f"${free_cash_flow/1e9:.2f}B" if free_cash_flow else 'N/A'
        }
        
        score = 50
        if revenue_growth and revenue_growth > 15:
            analysis['strengths'].append(f"Strong revenue growth of {revenue_growth:.1f}%")
            score += 20
        elif revenue_growth and revenue_growth < 5:
            analysis['weaknesses'].append(f"Slow revenue growth of {revenue_growth:.1f}%")
            score -= 15
        
        if gross_margin and gross_margin > 60:
            analysis['strengths'].append(f"High gross margin of {gross_margin:.1f}%")
            score += 15
        elif gross_margin and gross_margin < 40:
            analysis['weaknesses'].append(f"Low gross margin of {gross_margin:.1f}%")
            score -= 10
        
        if free_cash_flow and free_cash_flow > 0:
            analysis['strengths'].append("Positive free cash flow")
            score += 10
        
        analysis['rating'] = max(0, min(100, score))
        
    else:
        profit_margin = info.get('profitMargins', 0) * 100 if info.get('profitMargins') else None
        
        analysis['metrics'] = {
            'P/E Ratio': f"{pe_ratio:.2f}" if pe_ratio else 'N/A',
            'Profit Margin': f"{profit_margin:.1f}%" if profit_margin else 'N/A'
        }
        
        score = 50
        if profit_margin and profit_margin > 10:
            analysis['strengths'].append(f"Healthy profit margin of {profit_margin:.1f}%")
            score += 10
        
        analysis['rating'] = max(0, min(100, score))
    
    if analysis['rating'] >= 70:
        analysis['recommendation'] = "STRONG BUY"
    elif analysis['rating'] >= 60:
        analysis['recommendation'] = "BUY"
    elif analysis['rating'] >= 50:
        analysis['recommendation'] = "HOLD"
    elif analysis['rating'] >= 40:
        analysis['recommendation'] = "UNDERPERFORM"
    else:
        analysis['recommendation'] = "SELL"
    
    return analysis

@st.cache_data(ttl=300)
def get_stock_data(ticker, period):
    try:
        stock = yf.Ticker(ticker)
        return stock.history(period=period), stock.info, None
    except Exception as e:
        return None, None, str(e)

def get_prospective_stocks():
    return {
        "Tech Giants": ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA'],
        "Finance": ['JPM', 'BAC', 'GS', 'WFC', 'V', 'MA', 'BRK-B'],
        "Healthcare": ['JNJ', 'UNH', 'PFE', 'ABBV', 'TMO', 'ABT', 'MRK'],
        "Consumer": ['WMT', 'HD', 'NKE', 'SBUX', 'MCD', 'DIS', 'COST'],
        "Energy": ['XOM', 'CVX', 'COP', 'SLB', 'EOG', 'MPC', 'PSX'],
        "Industrial": ['BA', 'CAT', 'GE', 'HON', 'UPS', 'MMM', 'DE']
    }

with st.sidebar:
    st.title("BARBAS")
    if st.button("📊 Stock Analysis"):
        st.session_state.page = 'analysis'
    if st.button("📁 My Portfolio"):
        st.session_state.page = 'portfolio'
    if st.button("🔍 Discover Stocks"):
        st.session_state.page = 'discover'
    
    st.markdown("---")
    st.caption(f"Stocks in Portfolio: {len(st.session_state.portfolio)}")

if st.session_state.page == 'analysis':
    st.title("BARBAS Stock Analysis")
    
    col1, col2 = st.columns([4, 2])
    with col1:
        default_ticker = st.session_state.get('selected_ticker', 'AAPL')
        ticker_input = st.text_input("Enter ticker or company name", default_ticker, key="ticker_input")
        ticker = search_ticker(ticker_input)
        if 'selected_ticker' in st.session_state:
            del st.session_state.selected_ticker
    with col2:
        period = st.selectbox("Time Period", ["1mo", "3mo", "6mo", "1y", "2y"], index=3)
    
    with st.spinner(f"Analyzing {ticker}..."):
        data, info, error = get_stock_data(ticker, period)
    
    if error or data is None or data.empty:
        st.error("Unable to fetch data. Please check the ticker symbol.")
        st.stop()
    
    k_period = 14
    d_period = 3
    data['STOCH_K'], data['STOCH_D'] = calculate_stochastic(data['High'], data['Low'], data['Close'])
    
    st.header(f"{info.get('longName', ticker)}")
    st.text(f"{ticker} | {info.get('exchange', 'N/A')}")
    
    price = data['Close'].iloc[-1]
    change = ((data['Close'].iloc[-1] / data['Close'].iloc[0]) - 1) * 100
    
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Price", f"${price:.2f}", f"{change:+.2f}%")
    c2.metric("Market Cap", f"${info.get('marketCap', 0)/1e9:.1f}B")
    c3.metric("P/E", f"{info.get('trailingPE', 0):.2f}" if info.get('trailingPE') else 'N/A')
    c4.metric("Volume", f"{data['Volume'].iloc[-1]/1e6:.1f}M")
    c5.metric("52W Range", f"${info.get('fiftyTwoWeekLow', 0):.0f}-{info.get('fiftyTwoWeekHigh', 0):.0f}")
    
    st.subheader("Stochastic Oscillator Chart")
    
    fig = make_subplots(rows=2, cols=1, row_heights=[0.7, 0.3], vertical_spacing=0.03,
                        subplot_titles=(f'{ticker} Price', 'Stochastic Oscillator'))
    
    fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'],
                                  low=data['Low'], close=data['Close'], name='Price'), row=1, col=1)
    
    fig.add_trace(go.Scatter(x=data.index, y=data['STOCH_K'], line=dict(color='orange', width=2),
                            name='%K (Fast)'), row=2, col=1)
    
    fig.add_trace(go.Scatter(x=data.index, y=data['STOCH_D'], line=dict(color='black', width=2),
                            name='%D (Slow)'), row=2, col=1)
    
    fig.update_yaxes(range=[-10, 110], row=2, col=1)
    fig.add_hline(y=0, col=1, row=2, line_color="gray", line_width=2)
    fig.add_hline(y=100, col=1, row=2, line_color="gray", line_width=2)
    fig.add_hline(y=20, col=1, row=2, line_color='blue', line_width=2, line_dash='dash')
    fig.add_hline(y=80, col=1, row=2, line_color='blue', line_width=2, line_dash='dash')
    
    fig.update_layout(height=800, xaxis=dict(rangeslider=dict(visible=False)), showlegend=True, hovermode='x unified')
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    current_k = data['STOCH_K'].iloc[-1]
    current_d = data['STOCH_D'].iloc[-1]
    prev_k = data['STOCH_K'].iloc[-2]
    prev_d = data['STOCH_D'].iloc[-2]
    
    bullish_cross = (prev_k <= prev_d) and (current_k > current_d)
    bearish_cross = (prev_k >= prev_d) and (current_k < current_d)
    
    k_momentum = current_k - data['STOCH_K'].iloc[-5]
    recent_k = data['STOCH_K'].iloc[-10:]
    trend_direction = "bullish" if recent_k.is_monotonic_increasing else "bearish" if recent_k.is_monotonic_decreasing else "mixed"
    
    stoch_score = calculate_stochastic_score(current_k, current_d, k_momentum, trend_direction)
    sector = get_sector_from_info(info)
    fundamental_analysis = analyze_fundamentals(info, sector)
    combined_score = (stoch_score + fundamental_analysis['rating']) / 2
    position = "OVERSOLD" if current_k < 20 else "OVERBOUGHT" if current_k > 80 else "NEUTRAL"
    
    is_in_portfolio = any(s['ticker'] == ticker for s in st.session_state.portfolio)
    
    col_a, col_b = st.columns([1, 1])
    with col_a:
        if st.button("⭐ Add to Portfolio" if not is_in_portfolio else "✓ In Portfolio", 
                     disabled=is_in_portfolio, use_container_width=True):
            if add_to_portfolio(ticker, current_k, current_d, k_momentum, trend_direction):
                st.success(f"Added {ticker}!")
                st.rerun()
    with col_b:
        if is_in_portfolio:
            if st.button("🗑️ Remove", use_container_width=True):
                remove_from_portfolio(ticker)
                st.success(f"Removed {ticker}!")
                st.rerun()
    
    st.subheader("🎯 Current Market Position")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Stochastic %K", f"{current_k:.1f}", f"{k_momentum:+.1f} (5-day)")
    col2.metric("Stochastic %D", f"{current_d:.1f}")
    col3.metric("Position", position)
    col4.metric("Combined Score", f"{combined_score:.0f}/100")
    
    st.markdown("---")
    st.header("📊 COMPREHENSIVE INVESTMENT ANALYSIS")
    
    tab1, tab2, tab3 = st.tabs(["🔬 Technical", "💼 Fundamental", "🎯 Combined"])
    
    with tab1:
        st.subheader("⚠️ Critical Technical Signal Analysis")
        
        if position == "OVERSOLD":
            st.error("**OVERSOLD TERRITORY - HIGH PRIORITY SIGNAL**")
            st.write(f"**What This Means:** {ticker} is trading in oversold territory with a %K reading of {current_k:.1f}. This suggests the stock has experienced significant selling pressure and may be approaching a technical bottom.")
            st.write("**Investment Implications:**")
            st.write("- The stock is potentially undervalued on a short-term technical basis")
            st.write("- Historical patterns suggest oversold conditions often precede rebounds")
            st.write("- Risk/reward ratio may favor buyers at this level")
            st.write("- **However:** Oversold can remain oversold - don't catch a falling knife")
            st.write("")
            st.write("**Action Considerations:**")
            st.write("- For aggressive traders: Consider scaling into a position")
            st.write("- For conservative investors: Wait for confirmation of reversal (watch for %K crossing above %D)")
            st.write("- Set tight stop-losses if entering, as the stock could continue lower")
            st.write("- Monitor volume for signs of capitulation or accumulation")
            
        elif position == "OVERBOUGHT":
            st.warning("**OVERBOUGHT TERRITORY - CAUTION ADVISED**")
            st.write(f"**What This Means:** {ticker} is trading in overbought territory with a %K reading of {current_k:.1f}. This indicates strong buying pressure but also suggests limited upside in the near term.")
            st.write("**Investment Implications:**")
            st.write("- The rally may be overextended and due for consolidation or pullback")
            st.write("- Momentum is strong, but price may have run ahead of fundamentals")
            st.write("- Risk/reward ratio currently favors taking profits rather than initiating new positions")
            st.write("- **However:** Strong trends can remain overbought for extended periods")
            st.write("")
            st.write("**Action Considerations:**")
            st.write("- For current holders: Consider taking partial profits or tightening stop-losses")
            st.write("- For potential buyers: Wait for a pullback to more favorable entry levels")
            st.write("- Watch for bearish divergence (price making new highs while %K fails to)")
            st.write("- Overbought + bearish crossover = strong sell signal")
            
        else:
            st.info("**NEUTRAL RANGE - BALANCED MARKET CONDITIONS**")
            st.write(f"**What This Means:** {ticker} is trading in neutral territory with a %K reading of {current_k:.1f}. The stock is neither oversold nor overbought, suggesting balanced supply and demand.")
            st.write("**Investment Implications:**")
            st.write("- No extreme technical signals at this time")
            st.write("- Market is in equilibrium - wait for clearer directional signals")
            st.write("- Risk/reward is unclear without additional confirmation")
            st.write("")
            st.write("**Action Considerations:**")
            st.write("- Wait for the stock to enter oversold (<20) or overbought (>80) territory")
            st.write("- Focus on crossover signals and momentum shifts")
            st.write("- Use this time to monitor fundamentals and build a watchlist")
            st.write("- Consider other technical indicators to supplement stochastic analysis")
        
        st.markdown("---")
        
        st.write("**🔄 Crossover Signals (Most Critical):**")
        
        if bullish_cross:
            st.success("**🚀 BULLISH CROSSOVER DETECTED - BUY SIGNAL**")
            st.write(f"The fast line (%K = {current_k:.1f}) has just crossed ABOVE the slow line (%D = {current_d:.1f}). This is a **buy signal** indicating potential upward momentum.")
            
            signal_strength = 'VERY STRONG' if current_k < 30 else 'STRONG' if current_k < 50 else 'MODERATE'
            crossover_quality = 'in oversold territory - excellent entry point' if current_k < 20 else 'in neutral territory - decent signal' if current_k < 80 else 'in overbought territory - late entry, be cautious'
            
            st.write(f"**Signal Strength:** {signal_strength}")
            st.write("- Crossovers in oversold territory (<20) are most reliable")
            st.write(f"- This crossover occurred at {current_k:.1f}, which is {crossover_quality}")
            st.write("")
            st.write("**Recommended Action:** Consider initiating or adding to positions, but confirm with volume and price action.")
            
        elif bearish_cross:
            st.error("**📉 BEARISH CROSSOVER DETECTED - SELL SIGNAL**")
            st.write(f"The fast line (%K = {current_k:.1f}) has just crossed BELOW the slow line (%D = {current_d:.1f}). This is a **sell signal** indicating potential downward momentum.")
            
            signal_strength = 'VERY STRONG' if current_k > 70 else 'STRONG' if current_k > 50 else 'MODERATE'
            crossover_quality = 'in overbought territory - strong sell signal' if current_k > 80 else 'in neutral territory - watch closely' if current_k > 20 else 'in oversold territory - may be oversold bounce ending'
            
            st.write(f"**Signal Strength:** {signal_strength}")
            st.write("- Crossovers in overbought territory (>80) are most reliable")
            st.write(f"- This crossover occurred at {current_k:.1f}, which is {crossover_quality}")
            st.write("")
            st.write("**Recommended Action:** Consider taking profits, reducing position size, or exiting entirely if risk-averse.")
            
        else:
            st.info("**No Recent Crossover Detected**")
            k_above = current_k > current_d
            momentum_direction = 'bullish' if k_above else 'bearish'
            potential_signal = 'A bearish crossover (%K crossing below %D) would signal weakening momentum' if k_above else 'A bullish crossover (%K crossing above %D) would signal strengthening momentum'
            
            st.write(f"%K is currently {'ABOVE' if k_above else 'BELOW'} %D, suggesting {momentum_direction} momentum remains intact.")
            st.write("")
            st.write("**What to Watch For:**")
            st.write(f"- {potential_signal}")
            st.write("- Monitor the gap between %K and %D - narrowing suggests potential crossover coming")
            st.write(f"- Current gap: {abs(current_k - current_d):.1f} points")
        
        st.markdown("---")
        
        st.write("**📈 Momentum & Trend Analysis:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**5-Day Momentum:**")
            if k_momentum > 10:
                st.success(f"+{k_momentum:.1f} - Strong upward momentum")
            elif k_momentum > 0:
                st.info(f"+{k_momentum:.1f} - Positive momentum")
            elif k_momentum > -10:
                st.warning(f"{k_momentum:.1f} - Negative momentum")
            else:
                st.error(f"{k_momentum:.1f} - Strong downward momentum")
        
        with col2:
            st.write("**10-Day Trend:**")
            if trend_direction == "bullish":
                st.success("Consistently rising - strong uptrend")
            elif trend_direction == "bearish":
                st.error("Consistently falling - strong downtrend")
            else:
                st.info("Mixed signals - choppy/sideways action")
        
        st.markdown("---")
        
        st.write("**⚡ Risk Assessment:**")
        
        risk_factors = []
        risk_score = 0
        
        if current_k > 80:
            risk_factors.append("Overbought condition increases pullback risk")
            risk_score += 2
        if current_k < 20:
            risk_factors.append("Oversold condition suggests potential reversal")
            risk_score -= 1
        if bearish_cross:
            risk_factors.append("Recent bearish crossover signals downside")
            risk_score += 2
        if bullish_cross:
            risk_factors.append("Recent bullish crossover signals upside")
            risk_score -= 1
        if abs(k_momentum) > 15:
            risk_factors.append("High momentum suggests volatility ahead")
            risk_score += 1
        
        if risk_score >= 3:
            st.error("**HIGH RISK** - Multiple warning signals present")
        elif risk_score >= 1:
            st.warning("**MODERATE RISK** - Some caution warranted")
        else:
            st.success("**LOWER RISK** - Technical picture appears favorable")
        
        if risk_factors:
            st.write("**Key Risk Factors:**")
            for factor in risk_factors:
                st.write(f"- {factor}")
    
    with tab2:
        st.subheader("💼 Fundamental Valuation Analysis")
        
        st.info(f"**Sector:** {sector}")
        
        st.write("**Key Financial Metrics:**")
        cols = st.columns(len(fundamental_analysis['metrics']))
        for idx, (metric, value) in enumerate(fundamental_analysis['metrics'].items()):
            cols[idx].metric(metric, value)
        
        st.markdown("---")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric("Fundamental Score", f"{fundamental_analysis['rating']:.0f}/100")
            st.metric("Rating", fundamental_analysis['recommendation'])
        
        with col2:
            if fundamental_analysis['rating'] >= 70:
                st.success("**STRONG FUNDAMENTALS**")
            elif fundamental_analysis['rating'] >= 60:
                st.success("**SOLID FUNDAMENTALS**")
            elif fundamental_analysis['rating'] >= 50:
                st.info("**FAIR FUNDAMENTALS**")
            else:
                st.warning("**WEAK FUNDAMENTALS**")
        
        if fundamental_analysis['strengths']:
            st.write("**✅ Strengths:**")
            for s in fundamental_analysis['strengths']:
                st.success(f"• {s}")
        
        if fundamental_analysis['weaknesses']:
            st.write("**⚠️ Concerns:**")
            for w in fundamental_analysis['weaknesses']:
                st.warning(f"• {w}")
    
    with tab3:
        st.subheader("🎯 Combined Investment Recommendation")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Technical Score", f"{stoch_score:.0f}/100")
        col2.metric("Fundamental Score", f"{fundamental_analysis['rating']:.0f}/100")
        col3.metric("Combined Score", f"{combined_score:.0f}/100")
        
        st.markdown("---")
        
        if stoch_score >= 60 and fundamental_analysis['rating'] >= 60:
            st.success("**🌟 HIGH CONVICTION BUY**")
            st.write("Both technical and fundamental analysis are strongly positive.")
        elif combined_score >= 60:
            st.info("**✅ QUALIFIED BUY**")
            st.write("Mixed signals but overall positive outlook.")
        elif combined_score >= 50:
            st.warning("**⏸️ HOLD**")
            st.write("Neutral signals. Wait for better setup.")
        else:
            st.error("**❌ AVOID**")
            st.write("Multiple concerns present.")
    
    st.markdown("---")
    st.caption("⚠️ This analysis is for educational purposes only.")

elif st.session_state.page == 'portfolio':
    st.title("📁 My Portfolio")
    
    if not st.session_state.portfolio:
        st.info("Portfolio empty. Add stocks from Analysis page.")
        if st.button("Go to Analysis"):
            st.session_state.page = 'analysis'
            st.rerun()
    else:
        oversold = sum(1 for s in st.session_state.portfolio if s['position'] == 'OVERSOLD')
        overbought = sum(1 for s in st.session_state.portfolio if s['position'] == 'OVERBOUGHT')
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total", len(st.session_state.portfolio))
        col2.metric("Oversold 🟢", oversold)
        col3.metric("Overbought 🔴", overbought)
        
        st.markdown("---")
        
        for stock in st.session_state.portfolio:
            score = calculate_stochastic_score(stock['stoch_k'], stock['stoch_d'], stock['momentum'], stock['trend'])
            
            with st.expander(f"{stock['ticker']} - {stock['position']} | Score: {score}/100"):
                col1, col2, col3 = st.columns(3)
                col1.metric("%K", f"{stock['stoch_k']:.1f}")
                col2.metric("Momentum", f"{stock['momentum']:+.1f}")
                col3.metric("Trend", stock['trend'].title())
                
                btn1, btn2 = st.columns(2)
                with btn1:
                    if st.button(f"📊 Analyze", key=f"analyze_{stock['ticker']}"):
                        st.session_state.page = 'analysis'
                        st.session_state.selected_ticker = stock['ticker']
                        st.rerun()
                with btn2:
                    if st.button(f"🗑️ Remove", key=f"remove_{stock['ticker']}"):
                        remove_from_portfolio(stock['ticker'])
                        st.rerun()

elif st.session_state.page == 'discover':
    st.title("🔍 Discover Stocks")
    st.write("Scan popular stocks by sector")
    
    sectors = get_prospective_stocks()
    selected_sector = st.selectbox("Select Sector", list(sectors.keys()))
    
    if st.button(f"Analyze {selected_sector}", type="primary"):
        st.info(f"Analyzing {len(sectors[selected_sector])} stocks in {selected_sector}...")
        st.write("Feature ready for expansion with bulk stock analysis.")
