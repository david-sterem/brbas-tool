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

st.set_page_config(page_title="BRBAS", layout="wide", page_icon="📊")

# Session state
if 'page' not in st.session_state:
    st.session_state.page = 'analysis'
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []

def add_to_portfolio(ticker, current_k, current_d, k_momentum, trend):
    """Add stock to portfolio if not already there"""
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
    """Remove stock from portfolio"""
    st.session_state.portfolio = [s for s in st.session_state.portfolio if s['ticker'] != ticker]

def search_ticker(query):
    """Map company names to tickers"""
    mapping = {
        'apple': 'AAPL', 'microsoft': 'MSFT', 'google': 'GOOGL', 'amazon': 'AMZN',
        'tesla': 'TSLA', 'meta': 'META', 'nvidia': 'NVDA'
    }
    return mapping.get(query.lower(), query.upper())

def calculate_stochastic(high, low, close, k_period=14, d_period=3):
    """Calculate Stochastic Oscillator"""
    lowest_low = low.rolling(window=k_period).min()
    highest_high = high.rolling(window=k_period).max()
    k_percent = ((close - lowest_low) / (highest_high - lowest_low)) * 100
    d_percent = k_percent.rolling(window=d_period).mean()
    return k_percent, d_percent

def calculate_stochastic_score(k, d, momentum, trend):
    """Calculate a score from 0-100 based on stochastic signals"""
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
    """Determine sector from stock info"""
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
    """Comprehensive fundamental analysis based on sector"""
    analysis = {
        'sector': sector,
        'metrics': {},
        'strengths': [],
        'weaknesses': [],
        'rating': 0,
        'recommendation': ''
    }
    
    market_cap = info.get('marketCap', 0)
    pe_ratio = info.get('trailingPE', info.get('forwardPE'))
    revenue = info.get('totalRevenue', 0)
    
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
            analysis['strengths'].append(f"Strong ROE of {roe:.1f}% indicates efficient capital use")
            score += 15
        elif roe and roe < 8:
            analysis['weaknesses'].append(f"Low ROE of {roe:.1f}% suggests inefficient operations")
            score -= 10
        
        if pb_ratio and pb_ratio < 1.5:
            analysis['strengths'].append(f"P/B ratio of {pb_ratio:.2f} suggests undervaluation")
            score += 10
        elif pb_ratio and pb_ratio > 3:
            analysis['weaknesses'].append(f"High P/B ratio of {pb_ratio:.2f} may indicate overvaluation")
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
            analysis['strengths'].append(f"Exceptional revenue growth of {revenue_growth:.1f}% YoY")
            score += 20
        elif revenue_growth and revenue_growth < 5:
            analysis['weaknesses'].append(f"Sluggish revenue growth of {revenue_growth:.1f}%")
            score -= 15
        
        if gross_margin and gross_margin > 60:
            analysis['strengths'].append(f"High gross margin of {gross_margin:.1f}% indicates strong competitive moat")
            score += 15
        elif gross_margin and gross_margin < 40:
            analysis['weaknesses'].append(f"Lower gross margin of {gross_margin:.1f}% suggests pricing pressure")
            score -= 10
        
        if free_cash_flow and free_cash_flow > 0:
            analysis['strengths'].append("Positive free cash flow supports growth investments")
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
    """Fetch stock data from Yahoo Finance"""
    try:
        stock = yf.Ticker(ticker)
        return stock.history(period=period), stock.info, None
    except Exception as e:
        return None, None, str(e)

# Sidebar
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

# MAIN ANALYSIS PAGE
if st.session_state.page == 'analysis':
    st.title("BARBAS")
    
    col1, col2 = st.columns([4, 2])
    with col1:
        default_ticker = st.session_state.get('selected_ticker', 'AAPL')
        ticker_input = st.text_input("Ticker or Company", default_ticker, label_visibility="collapsed")
        ticker = search_ticker(ticker_input)
        if 'selected_ticker' in st.session_state:
            del st.session_state.selected_ticker
    with col2:
        period = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y", "2y"], index=3, label_visibility="collapsed")
    
    with st.spinner(f"Analyzing {ticker}..."):
        data, info, error = get_stock_data(ticker, period)
    
    if error or data is None or data.empty:
        st.error("Data unavailable")
        st.stop()
    
    k_period = 14
    d_period = 3
    
    data['n_high'] = data['High'].rolling(k_period).max()
    data['n_low'] = data['Low'].rolling(k_period).min()
    data['%K'] = (data['Close'] - data['n_low']) * 100 / (data['n_high'] - data['n_low'])
    data['%D'] = data['%K'].rolling(d_period).mean()
    data['STOCH_K'], data['STOCH_D'] = calculate_stochastic(data['High'], data['Low'], data['Close'])
    
    st.header(f"{info.get('longName', ticker)}")
    st.text(f"{ticker} | {info.get('exchange', 'N/A')}")
    
    price = data['Close'].iloc[-1]
    change = ((data['Close'].iloc[-1] / data['Close'].iloc[0]) - 1) * 100
    
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Price", f"${price:.2f}", f"{change:+.2f}%")
    c2.metric("Market Cap", f"${info.get('marketCap', 0)/1e9:.1f}B")
    c3.metric("P/E", f"{info.get('trailingPE', 0):.2f}")
    c4.metric("Volume", f"{data['Volume'].iloc[-1]/1e6:.1f}M")
    c5.metric("52W Range", f"${info.get('fiftyTwoWeekLow', 0):.0f}-{info.get('fiftyTwoWeekHigh', 0):.0f}")
    
    st.subheader("Stochastic Oscillator Chart")
    
    fig = make_subplots(rows=2, cols=1, 
                        row_heights=[0.7, 0.3],
                        vertical_spacing=0.03,
                        subplot_titles=(f'{ticker} Price', 'Stochastic Oscillator'))
    
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
    
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['STOCH_K'],
            line=dict(color='orange', width=2),
            name='%K (Fast)',
        ), row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['STOCH_D'],
            line=dict(color='black', width=2),
            name='%D (Slow)'
        ), row=2, col=1
    )
    
    fig.update_yaxes(range=[-10, 110], row=2, col=1)
    fig.add_hline(y=0, col=1, row=2, line_color="gray", line_width=2)
    fig.add_hline(y=100, col=1, row=2, line_color="gray", line_width=2)
    fig.add_hline(y=20, col=1, row=2, line_color='blue', line_width=2, line_dash='dash')
    fig.add_hline(y=80, col=1, row=2, line_color='blue', line_width=2, line_dash='dash')
    
    fig.update_layout(
        height=800,
        xaxis=dict(rangeslider=dict(visible=False)),
        showlegend=True,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.header("📊 COMPREHENSIVE INVESTMENT ANALYSIS")
    st.markdown("*Combining technical signals with fundamental valuation for complete market insight*")
    
    tab1, tab2, tab3 = st.tabs(["🔬 Technical Analysis", "💼 Fundamental Analysis", "🎯 Combined Recommendation"])
    
    with tab1:
        st.subheader("⚠️ Technical Signal Analysis")
        
        if current_k < 20:
            st.error("**OVERSOLD TERRITORY - HIGH PRIORITY SIGNAL**")
            st.write(f"""
            **What This Means:** {ticker} is trading in oversold territory with a %K reading of {current_k:.1f}. 
            This suggests the stock has experienced significant selling pressure and may be approaching a technical bottom.
            
            **Investment Implications:**
            - The stock is potentially undervalued on a short-term technical basis
            - Historical patterns suggest oversold conditions often precede rebounds
            - Risk/reward ratio may favor buyers at this level
            - **However:** Oversold can remain oversold - don't catch a falling knife
            
            **Action Considerations:**
            - For aggressive traders: Consider scaling into a position
            - For conservative investors: Wait for confirmation of reversal (watch for %K crossing above %D)
            - Set tight stop-losses if entering, as the stock could continue lower
            - Monitor volume for signs of capitulation or accumulation
            """)
            
        elif current_k > 80:
            st.warning("**OVERBOUGHT TERRITORY - CAUTION ADVISED**")
            st.write(f"""
            **What This Means:** {ticker} is trading in overbought territory with a %K reading of {current_k:.1f}. 
            This indicates strong buying pressure but also suggests limited upside in the near term.
            
            **Investment Implications:**
            - The rally may be overextended and due for consolidation or pullback
            - Momentum is strong, but price may have run ahead of fundamentals
            - Risk/reward ratio currently favors taking profits rather than initiating new positions
            - **However:** Strong trends can remain overbought for extended periods
            
            **Action Considerations:**
            - For current holders: Consider taking partial profits or tightening stop-losses
            - For potential buyers: Wait for a pullback to more favorable entry levels
            - Watch for bearish divergence (price making new highs while %K fails to)
            - Overbought + bearish crossover = strong sell signal
            """)
            
        else:
            st.info("**NEUTRAL RANGE - BALANCED MARKET CONDITIONS**")
            st.write(f"""
            **What This Means:** {ticker} is trading in neutral territory with a %K reading of {current_k:.1f}. 
            The stock is neither oversold nor overbought, suggesting balanced supply and demand.
            
            **Investment Implications:**
            - No extreme technical signals at this time
            - Market is in equilibrium - wait for clearer directional signals
            - Risk/reward is unclear without additional confirmation
            
            **Action Considerations:**
            - Wait for the stock to enter oversold (<20) or overbought (>80) territory
            - Focus on crossover signals and momentum shifts
            - Use this time to monitor fundamentals and build a watchlist
            - Consider other technical indicators to supplement stochastic analysis
            """)
        
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
        
        st.write("**💡 Strategic Recommendations:**")
        
        st.write("""
        **For Day Traders:**
        - Use stochastic crossovers as entry/exit signals
        - Best signals occur in oversold (<20) and overbought (>80) zones
        - Combine with volume analysis for confirmation
        - Set tight stops (2-3%) to limit downside
        
        **For Swing Traders:**
        - Enter on bullish crossovers in oversold territory
        - Exit on bearish crossovers in overbought territory
        - Hold through neutral zone unless crossover signals change
        - Target 5-10% moves over 1-3 week timeframes
        
        **For Long-Term Investors:**
        - Use extreme oversold readings (<20) to add to positions
        - Don't panic sell on overbought readings in strong uptrends
        - Focus more on monthly stochastic readings for major trend changes
        - Combine with fundamental analysis - technicals alone are insufficient
        
        **Important Caveats:**
        - Stochastic oscillator works best in ranging markets, less reliable in strong trends
        - False signals are common - always use stop-losses
        - No single indicator should drive investment decisions
        - Consider market conditions, fundamentals, and overall trend
        """)
        
        with st.expander("📚 Understanding the Stochastic Oscillator"):
            st.write("""
            **What It Measures:**
            The Stochastic Oscillator compares a stock's closing price to its price range over a specific period (default: 14 days).
            
            **The Two Lines:**
            - **%K (Fast Line):** Raw calculation = (Current Close - 14-day Low) / (14-day High - 14-day Low) × 100
            - **%D (Slow Line):** 3-day moving average of %K
            
            **Key Zones:**
            - **Below 20:** Oversold - potential bounce
            - **Above 80:** Overbought - potential pullback
            - **20-80:** Neutral zone
            
            **Limitations:**
            - Can stay overbought/oversold for extended periods
            - Generates false signals in choppy markets
            - Should never be used in isolation
            """)
    
    with tab2:
        st.subheader("💼 Fundamental Valuation Analysis")
        
        st.info(f"**Sector:** {fundamental_analysis['sector']}")
        
        st.write("**Key Financial Metrics:**")
        metrics_cols = st.columns(len(fundamental_analysis['metrics']))
        for idx, (metric, value) in enumerate(fundamental_analysis['metrics'].items()):
            with metrics_cols[idx]:
                st.metric(metric, value)
        
        st.markdown("---")
        
        fund_score = fundamental_analysis['rating']
        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric("Fundamental Score", f"{fund_score:.0f}/100")
            st.metric("Recommendation", fundamental_analysis['recommendation'])
        
        with col2:
            if fund_score >= 70:
                st.success("**STRONG FUNDAMENTALS** - Company shows excellent financial health")
            elif fund_score >= 60:
                st.success("**SOLID FUNDAMENTALS** - Company has good financial metrics")
            elif fund_score >= 50:
                st.info("**FAIR FUNDAMENTALS** - Company is adequately valued")
            elif fund_score >= 40:
                st.warning("**WEAK FUNDAMENTALS** - Some financial concerns present")
            else:
                st.error("**POOR FUNDAMENTALS** - Significant financial weaknesses")
        
        st.markdown("---")
        
        if fundamental_analysis['strengths']:
            st.write("**✅ Fundamental Strengths:**")
            for strength in fundamental_analysis['strengths']:
                st.success(f"• {strength}")
        
        if fundamental_analysis['weaknesses']:
            st.write("**⚠️ Fundamental Concerns:**")
            for weakness in fundamental_analysis['weaknesses']:
                st.warning(f"• {weakness}")
        
        st.markdown("---")
        
        st.write("**📖 Sector-Specific Investment Considerations:**")
        
        if fundamental_analysis['sector'] == 'Financial Services':
            st.write("""
            **What Drives Financial Stocks:**
            - Interest rate environment
            - Loan growth and credit quality
            - Regulatory changes
            
            **What to Look For:**
            - ROE > 15%
            - P/B ratio < 1.5
            - Strong risk management
            """)
        elif fundamental_analysis['sector'] == 'Technology':
            st.write("""
            **What Drives Technology Stocks:**
            - Innovation cycles
            - Cloud adoption and AI growth
            - Market share gains
            
            **What to Look For:**
            - Revenue growth > 15%
            - Gross margins > 60%
            - Positive free cash flow
            """)
    
    with tab3:
        st.subheader("🎯 Combined Investment Recommendation")
        
        score_col1, score_col2, score_col3 = st.columns(3)
        with score_col1:
            st.metric("Technical Score", f"{stoch_score:.0f}/100")
        with score_col2:
            st.metric("Fundamental Score", f"{fund_score:.0f}/100")
        with score_col3:
            st.metric("Combined Score", f"{combined_score:.0f}/100")
        
        st.markdown("---")
        
        st.write("**🎯 Integrated Investment Thesis:**")
        
        if stoch_score >= 60 and fund_score >= 60:
            st.success("**🌟 HIGH CONVICTION BUY**")
            st.write(f"""
            {ticker} presents a rare alignment of both technical and fundamental factors.
            
            **Technical:** Shows {position.lower()} conditions with favorable momentum.
            **Fundamental:** Strong fundamentals (score: {fund_score:.0f}/100) support the valuation.
            
            **Action:** Consider this a high-probability opportunity for position sizing.
            """)
        elif (stoch_score >= 60 and fund_score >= 45) or (stoch_score >= 45 and fund_score >= 60):
            st.info("**✅ QUALIFIED BUY**")
            st.write("Mixed signals - one metric is stronger than the other. Proceed with caution.")
        else:
            st.warning("**⚠️ HOLD / AVOID**")
            st.write("Both technical and fundamental concerns present. Better opportunities may exist.")
    
    st.markdown("---")
    
    st.subheader("🔄 Crossover Signals")
    
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
    
    is_in_portfolio = any(s['ticker'] == ticker for s in st.session_state.portfolio)
    
    col_a, col_b, col_c = st.columns([1, 1, 3])
    with col_a:
        if st.button("⭐ Add to Portfolio" if not is_in_portfolio else "✓ In Portfolio", 
                     disabled=is_in_portfolio,
                     use_container_width=True):
            if add_to_portfolio(ticker, current_k, current_d, k_momentum, trend_direction):
                st.success(f"Added {ticker} to portfolio!")
                st.rerun()
    with col_b:
        if is_in_portfolio:
            if st.button("🗑️ Remove", use_container_width=True):
                remove_from_portfolio(ticker)
                st.success(f"Removed {ticker} from portfolio!")
                st.rerun()
    
    st.subheader("🎯 Current Market Position")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Stochastic %K", f"{current_k:.1f}", f"{k_momentum:+.1f} (5-day)")
    with col2:
        st.metric("Stochastic %D", f"{current_d:.1f}")
    with col3:
        position = "OVERSOLD" if current_k < 20 else "OVERBOUGHT" if current_k > 80 else "NEUTRAL"
        st.metric("Position", position)
    with col4:
        st.metric("Combined Score", f"{combined_score:.0f}/100", help="Weighted average of technical and fundamental analysis")
    
    st.subheader("🔄 Crossover Signals")
    
    if bullish_cross:
        st.success("**🚀 BULLISH CROSSOVER DETECTED - BUY SIGNAL**")
        st.write(f"The fast line (%K = {current_k:.1f}) crossed ABOVE the slow line (%D = {current_d:.1f}).")
    elif bearish_cross:
        st.error("**📉 BEARISH CROSSOVER DETECTED - SELL SIGNAL**")
        st.write(f"The fast line (%K = {current_k:.1f}) crossed BELOW the slow line (%D = {current_d:.1f}).")
    else:
        st.info("**No Recent Crossover Detected**")
        st.write(f"%K is currently {'ABOVE' if current_k > current_d else 'BELOW'} %D.")
    
    st.markdown("---")
    st.caption("⚠️ This analysis is for educational purposes only and does not constitute financial advice.")

elif st.session_state.page == 'portfolio':
    st.title("📁 My Portfolio")
    
    if not st.session_state.portfolio:
        st.info("Your portfolio is empty. Add stocks from the Stock Analysis page.")
        if st.button("Go to Stock Analysis"):
            st.session_state.page = 'analysis'
            st.rerun()
    else:
        oversold = sum(1 for s in st.session_state.portfolio if s['position'] == 'OVERSOLD')
        overbought = sum(1 for s in st.session_state.portfolio if s['position'] == 'OVERBOUGHT')
        neutral = sum(1 for s in st.session_state.portfolio if s['position'] == 'NEUTRAL')
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Stocks", len(st.session_state.portfolio))
        col2.metric("Oversold", oversold)
        col3.metric("Overbought", overbought)
        col4.metric("Neutral", neutral)
        
        st.markdown("---")
        
        for stock in st.session_state.portfolio:
            score = calculate_stochastic_score(stock['stoch_k'], stock['stoch_d'], 
                                              stock['momentum'], stock['trend'])
            
            with st.expander(f"{stock['ticker']} - {stock['position']} | Score: {score}/100"):
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Stochastic %K", f"{stock['stoch_k']:.1f}")
                col2.metric("Momentum", f"{stock['momentum']:+.1f}")
                col3.metric("Trend", stock['trend'].title())
                col4.metric("Score", f"{score}/100")
                
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if st.button(f"Analyze {stock['ticker']}", key=f"analyze_{stock['ticker']}"):
                        st.session_state.page = 'analysis'
                        st.session_state.selected_ticker = stock['ticker']
                        st.rerun()
                with btn_col2:
                    if st.button(f"Remove", key=f"remove_{stock['ticker']}"):
                        remove_from_portfolio(stock['ticker'])
                        st.rerun()

elif st.session_state.page == 'discover':
    st.title("🔍 Discover Stocks")
    st.info("Discover page - coming soon!")
