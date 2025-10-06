with tab3:
        st.subheader("🎯 Combined Investment Recommendation")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Technical Score", f"{stoch_score:.0f}/100", help="Based on stochastic oscillator")
        col2.metric("Fundamental Score", f"{fundamental_analysis['rating']:.0f}/100", help="Based on financial metrics")
        col3.metric("Combined Score", f"{combined_score:.0f}/100", help="Equal weight average")
        
        st.markdown("---")
        
        st.write("**🎯 Integrated Investment Thesis:**")
        
        # Best case: Both strong
        if stoch_score >= 60 and fundamental_analysis['rating'] >= 60:
            st.success("**🌟 HIGH CONVICTION BUY**")
            st.write(f"""
            **Why This Is Compelling:**
            
            {ticker} presents a rare alignment of both technical and fundamental factors:
            
            **Technical Perspective:** The stochastic oscillator shows {position.lower()} conditions with 
            {'strong bullish momentum' if k_momentum > 0 else 'potential reversal setup'}. This suggests 
            favorable entry timing from a price action standpoint.
            
            **Fundamental Perspective:** The company demonstrates {fundamental_analysis['recommendation'].lower()} 
            fundamentals with a score of {fundamental_analysis['rating']:.0f}/100. Key financial metrics support the valuation, 
            indicating the business quality justifies current or higher prices.
            
            **Combined View:** When strong fundamentals align with favorable technical entry points, 
            historical data shows these setups produce above-average risk-adjusted returns. The technical 
            timing reduces drawdown risk while fundamentals support medium-term upside.
            
            **Action:** Consider this a high-probability opportunity for {"aggressive" if combined_score >= 75 else "moderate"} 
            position sizing. The dual confirmation reduces false signal risk.
            """)
            
        # Good case: One strong, one moderate
        elif (stoch_score >= 60 and fundamental_analysis['rating'] >= 45) or (stoch_score >= 45 and fundamental_analysis['rating'] >= 60):
            st.info("**✅ QUALIFIED BUY**")
            
            if stoch_score > fundamental_analysis['rating']:
                st.write(f"""
                **Mixed Signals - Technical Leading:**
                
                The technical setup is stronger than fundamentals, creating a "trade vs. invest" decision point:
                
                **Technical Strength:** {ticker} shows favorable stochastic readings that historically 
                precede short to medium-term rallies. Entry timing appears opportune.
                
                **Fundamental Caution:** While not alarming, the fundamental score of {fundamental_analysis['rating']:.0f}/100 
                suggests the company faces some financial headwinds or valuation concerns that limit 
                long-term conviction.
                
                **Recommendation:** Suitable for swing traders and tactical investors (1-3 month holding period). 
                Consider smaller position sizes and have clear exit targets. The technical setup may produce 
                profits, but weak fundamentals mean you're timing a trade, not buying a business.
                """)
            else:
                st.write(f"""
                **Mixed Signals - Fundamental Leading:**
                
                The company quality exceeds the current technical setup, suggesting a "buy the dip" opportunity:
                
                **Fundamental Strength:** {ticker} demonstrates solid financial health (score: {fundamental_analysis['rating']:.0f}/100) 
                that should support long-term value creation. The business quality is evident.
                
                **Technical Caution:** Current stochastic readings of {current_k:.1f} suggest {position.lower()} 
                conditions. {"This may indicate the stock needs more time to consolidate" if current_k > 50 else "While oversold, momentum hasn't confirmed yet"}.
                
                **Recommendation:** Appropriate for patient, fundamental investors willing to dollar-cost average. 
                Consider building positions in tranches as technical confirmation emerges. Strong fundamentals 
                reduce downside risk, but timing may require patience.
                """)
                
        # Weak case: One or both weak
        elif stoch_score < 45 or fundamental_analysis['rating'] < 45:
            st.warning("**⚠️ HOLD / AVOID**")
            
            if stoch_score < 45 and fundamental_analysis['rating'] < 45:
                st.write(f"""
                **Dual Weakness Identified:**
                
                Both technical and fundamental analysis raise concerns about {ticker}:
                
                **Technical Issues:** Stochastic score of {stoch_score:.0f}/100 indicates {position.lower()} 
                conditions with {"deteriorating momentum" if k_momentum < 0 else "uncertain direction"}. 
                Price action suggests continued weakness or consolidation ahead.
                
                **Fundamental Issues:** Financial metrics score only {fundamental_analysis['rating']:.0f}/100, indicating structural 
                concerns with valuation, profitability, or growth. The business fundamentals don't support 
                current price levels.
                
                **Recommendation:** AVOID new positions. If already holding, consider reducing exposure or 
                exiting entirely. When both technical and fundamental factors align negatively, the probability 
                of near-term underperformance increases substantially. Better opportunities exist elsewhere.
                
                **Risk:** Buying into dual weakness often results in "value traps" where stocks continue 
                declining as both price action AND business fundamentals deteriorate.
                """)
                
            elif stoch_score < 45:
                st.write(f"""
                **Technical Weakness Despite Strong Fundamentals:**
                
                {ticker} presents a puzzle - good business, poor price action:
                
                **The Good:** Fundamental score of {fundamental_analysis['rating']:.0f}/100 suggests the underlying business 
                has quality characteristics that should eventually be recognized by the market.
                
                **The Challenge:** Technical score of {stoch_score:.0f}/100 with {position.lower()} stochastic 
                readings indicates sellers dominate current price action. {ticker} is in a downtrend or 
                consolidation despite good fundamentals.
                
                **What This Means:** Often when good companies show poor technicals, it signals either:
                1. Market is pricing in future fundamental deterioration not yet visible
                2. Temporary sentiment disconnect that will correct
                3. Sector rotation away from this area regardless of company quality
                
                **Recommendation:** WAIT for technical confirmation before entering. Use price alerts at 
                key technical levels. Strong fundamentals reduce catastrophic risk, but poor technicals 
                suggest timing is premature. "Right stock, wrong time."
                """)
                
            else:  # fundamental_analysis['rating'] < 45
                st.write(f"""
                **Fundamental Weakness Despite Technical Strength:**
                
                {ticker} shows favorable technical setup but concerning fundamentals - a classic "sucker rally" risk:
                
                **The Setup:** Technical score of {stoch_score:.0f}/100 suggests {position.lower()} conditions 
                that often precede bounces. Traders may be attracted to oversold readings.
                
                **The Problem:** Fundamental score of {fundamental_analysis['rating']:.0f}/100 indicates serious business concerns:
                {fundamental_analysis['weaknesses'][0] if fundamental_analysis['weaknesses'] else 'weak financial metrics'}
                
                **What This Means:** Stocks can rally on technical oversold bounces even when fundamentally broken. 
                These "dead cat bounces" trap investors who ignore business quality. Without fundamental support, 
                technical rallies often fail and new lows are made.
                
                **Recommendation:** AVOID unless you're an experienced short-term trader with tight stops. 
                The risk/reward is unfavorable for investors. When fundamentals are poor, technical rallies 
                become selling opportunities rather than buying opportunities.
                """)
        
        else:
            st.info("**⚖️ NEUTRAL / HOLD**")
            st.write("Signals are mixed. Consider waiting for clearer conviction before making investment decisions.")
        
        st.markdown("---")
        
        # Comparison table
        st.write("**📊 Factor Comparison:**")
        
        comparison_data = {
            'Factor': ['Technical Signal', 'Fundamental Health', 'Risk Level', 'Time Horizon', 'Position Sizing'],
            'Assessment': [
                f"{'Bullish' if stoch_score >= 60 else 'Bearish' if stoch_score < 45 else 'Neutral'} ({stoch_score:.0f}/100)",
                f"{'Strong' if fundamental_analysis['rating'] >= 60 else 'Weak' if fundamental_analysis['rating'] < 45 else 'Fair'} ({fundamental_analysis['rating']:.0f}/100)",
                f"{'Low' if combined_score >= 65 else 'High' if combined_score < 50 else 'Moderate'}",
                f"{'Long-term' if fundamental_analysis['rating'] >= 60 else 'Short-term' if stoch_score >= 60 else 'N/A'}",
                f"{'Large (5-10%)' if combined_score >= 70 else 'Small (1-3%)' if combined_score >= 50 else 'None (0%)'}"
            ]
        }
        
        st.table(comparison_data)
        
        st.markdown("---")
        
        # Final verdict
        st.write("**⚖️ Final Verdict:**")
        
        if combined_score >= 70:
            st.success(f"""
            **STRONG BUY - High Conviction**
            
            Combined score of {combined_score:.0f}/100 represents a high-quality opportunity where both 
            technical timing and fundamental valueimport streamlit as st
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

# Session state
if 'page' not in st.session_state:
    st.session_state.page = 'analysis'
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []

# Helper functions
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

# ANALYSIS PAGE
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
    
    # Calculate stochastic
    k_period = 14
    d_period = 3
    data['STOCH_K'], data['STOCH_D'] = calculate_stochastic(data['High'], data['Low'], data['Close'])
    
    # Display stock info
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
    
    # Chart
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
    
    # Analysis section
    st.markdown("---")
    
    # Calculate all metrics BEFORE using them
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
    
    # Portfolio buttons
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
    
    # Current Position
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
            st.write("""
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
            
        elif position == "OVERBOUGHT":
            st.warning("**OVERBOUGHT TERRITORY - CAUTION ADVISED**")
            st.write(f"**What This Means:** {ticker} is trading in overbought territory with a %K reading of {current_k:.1f}. This indicates strong buying pressure but also suggests limited upside in the near term.")
            st.write("""
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
            st.write(f"**What This Means:** {ticker} is trading in neutral territory with a %K reading of {current_k:.1f}. The stock is neither oversold nor overbought, suggesting balanced supply and demand.")
            st.write("""
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
        
        # Crossover Analysis
        st.write("**🔄 Crossover Signals (Most Critical):**")
        
        if bullish_cross:
            st.success("**🚀 BULLISH CROSSOVER DETECTED - BUY SIGNAL**")
            st.write(f"The fast line (%K = {current_k:.1f}) has just crossed ABOVE the slow line (%D = {current_d:.1f}). This is a **buy signal** indicating potential upward momentum.")
            
            signal_strength = 'VERY STRONG' if current_k < 30 else 'STRONG' if current_k < 50 else 'MODERATE'
            crossover_quality = 'in oversold territory - excellent entry point' if current_k < 20 else 'in neutral territory - decent signal' if current_k < 80 else 'in overbought territory - late entry, be cautious'
            
            st.write(f"""
            **Signal Strength:** {signal_strength}
            - Crossovers in oversold territory (<20) are most reliable
            - This crossover occurred at {current_k:.1f}, which is {crossover_quality}
            
            **Recommended Action:** Consider initiating or adding to positions, but confirm with volume and price action.
            """)
            
        elif bearish_cross:
            st.error("**📉 BEARISH CROSSOVER DETECTED - SELL SIGNAL**")
            st.write(f"The fast line (%K = {current_k:.1f}) has just crossed BELOW the slow line (%D = {current_d:.1f}). This is a **sell signal** indicating potential downward momentum.")
            
            signal_strength = 'VERY STRONG' if current_k > 70 else 'STRONG' if current_k > 50 else 'MODERATE'
            crossover_quality = 'in overbought territory - strong sell signal' if current_k > 80 else 'in neutral territory - watch closely' if current_k > 20 else 'in oversold territory - may be oversold bounce ending'
            
            st.write(f"""
            **Signal Strength:** {signal_strength}
            - Crossovers in overbought territory (>80) are most reliable
            - This crossover occurred at {current_k:.1f}, which is {crossover_quality}
            
            **Recommended Action:** Consider taking profits, reducing position size, or exiting entirely if risk-averse.
            """)
            
        else:
            st.info("**No Recent Crossover Detected**")
            k_above = current_k > current_d
            momentum_direction = 'bullish' if k_above else 'bearish'
            potential_signal = 'A bearish crossover (%K crossing below %D) would signal weakening momentum' if k_above else 'A bullish crossover (%K crossing above %D) would signal strengthening momentum'
            
            st.write(f"""
            %K is currently {'ABOVE' if k_above else 'BELOW'} %D, suggesting {momentum_direction} momentum remains intact.
            
            **What to Watch For:**
            - {potential_signal}
            - Monitor the gap between %K and %D - narrowing suggests potential crossover coming
            - Current gap: {abs(current_k - current_d):.1f} points
            """)
        
        st.markdown("---")
        
        # Momentum & Trend
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
        
        # Risk Assessment
        st.write("**⚡ Risk Assessment & Probability:**")
        
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
            st.error("**HIGH RISK** - Multiple warning signals present. Consider defensive positioning.")
        elif risk_score >= 1:
            st.warning("**MODERATE RISK** - Some caution warranted. Monitor closely.")
        else:
            st.success("**LOWER RISK** - Technical picture appears more favorable.")
        
        if risk_factors:
            st.write("**Key Risk Factors:**")
            for factor in risk_factors:
                st.write(f"- {factor}")
        
        st.markdown("---")
        
        # Trading Strategies
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
            It answers: "Where is the current price relative to the recent high-low range?"
            
            **The Two Lines:**
            - **%K (Fast Line):** Raw calculation = (Current Close - 14-day Low) / (14-day High - 14-day Low) × 100
            - **%D (Slow Line):** 3-day moving average of %K, smooths out noise
            
            **Key Zones:**
            - **Below 20:** Oversold - stock has fallen significantly, potential bounce
            - **Above 80:** Overbought - stock has risen significantly, potential pullback
            - **20-80:** Neutral zone - no extreme signals
            
            **Why It Works:**
            Markets move in cycles of buying and selling pressure. When a stock closes near its recent lows repeatedly, 
            it's often oversold and due for a bounce. When it closes near recent highs, it's often overbought and due for a rest.
            
            **Limitations:**
            - Can stay overbought/oversold for extended periods in strong trends
            - Generates false signals in choppy, directionless markets
            - Lagging indicator - signals come after moves have started
            - Should never be used in isolation
            """)
    
    
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
                st.success("**STRONG FUNDAMENTALS** - Company shows excellent financial health")
            elif fundamental_analysis['rating'] >= 60:
                st.success("**SOLID FUNDAMENTALS** - Company has good financial metrics")
            elif fundamental_analysis['rating'] >= 50:
                st.info("**FAIR FUNDAMENTALS** - Company is adequately valued")
            elif fundamental_analysis['rating'] >= 40:
                st.warning("**WEAK FUNDAMENTALS** - Some financial concerns present")
            else:
                st.error("**POOR FUNDAMENTALS** - Significant financial weaknesses")
        
        st.markdown("---")
        
        if fundamental_analysis['strengths']:
            st.write("**✅ Fundamental Strengths:**")
            for s in fundamental_analysis['strengths']:
                st.success(f"• {s}")
        
        if fundamental_analysis['weaknesses']:
            st.write("**⚠️ Fundamental Concerns:**")
            for w in fundamental_analysis['weaknesses']:
                st.warning(f"• {w}")
        
        st.markdown("---")
        
        st.write("**📖 Sector-Specific Investment Considerations:**")
        
        if sector == 'Financial Services':
            st.write("""
            **What Drives Financial Stocks:**
            - Interest rate environment (higher rates = better margins)
            - Loan growth and credit quality
            - Regulatory changes and capital requirements
            - Economic growth and consumer confidence
            
            **What to Look For:**
            - ROE > 15% indicates efficient capital deployment
            - P/B ratio < 1.5 may signal undervaluation
            - Growing deposits and stable loan portfolio
            - Strong risk management and diversified revenue
            
            **Technical Correlation:**
            Financial stocks often show strong technical patterns during rate hike cycles. If fundamentals 
            are strong (high ROE, good P/B) AND technicals show oversold conditions, this creates a 
            compelling "value + timing" opportunity.
            """)
            
        elif sector == 'Technology':
            st.write("""
            **What Drives Technology Stocks:**
            - Innovation cycles and product launches
            - Cloud adoption and AI growth trends
            - Market share gains and competitive positioning
            - Regulatory scrutiny and antitrust concerns
            
            **What to Look For:**
            - Revenue growth > 15% YoY shows market leadership
            - Gross margins > 60% indicate pricing power and moats
            - Positive and growing free cash flow
            - Scalable business models with high customer retention
            
            **Technical Correlation:**
            Tech stocks can remain overbought for extended periods during bull markets. However, when 
            fundamentals weaken (slowing growth, margin compression) AND technical indicators turn 
            bearish, this signals a high-probability exit point.
            """)
            
        elif sector == 'Industrial':
            st.write("""
            **What Drives Industrial Stocks:**
            - Economic growth and GDP expansion
            - Infrastructure spending and government contracts
            - Supply chain health and commodity prices
            - Global trade dynamics
            
            **What to Look For:**
            - Operating margins > 12% show operational efficiency
            - Debt-to-Equity < 100% indicates financial flexibility
            - Growing order backlogs signal future revenue
            - Diversified customer base reduces concentration risk
            
            **Technical Correlation:**
            Industrial stocks are cyclical and respond to economic data. Strong fundamentals (high margins, 
            low debt) combined with oversold technical readings often mark excellent entry points before 
            economic recovery accelerates.
            """)
            
        elif sector == 'Energy':
            st.write("""
            **What Drives Energy Stocks:**
            - Crude oil and natural gas prices
            - OPEC+ production decisions
            - Geopolitical tensions and supply disruptions
            - Transition to renewable energy sources
            
            **What to Look For:**
            - P/B ratio and EV/EBITDA for better valuation gauges
            - Low production costs and break-even points
            - Strong reserves and diversification strategies
            - Balance sheet strength to weather commodity volatility
            
            **Technical Correlation:**
            Energy stocks are highly volatile and commodity-driven. When oil prices stabilize and technical 
            indicators show oversold conditions while fundamentals remain solid (low debt, good reserves), 
            this creates asymmetric risk/reward setups.
            """)
            
        elif sector == 'Consumer Cyclical':
            st.write("""
            **What Drives Consumer Cyclical Stocks:**
            - Consumer confidence and discretionary spending
            - Employment levels and wage growth
            - Inflation and purchasing power
            - Seasonal trends and shopping patterns
            
            **What to Look For:**
            - Same-store sales growth > 5%
            - Strong brand recognition and pricing power
            - Healthy gross margins (> 35%)
            - Global diversification reduces single-market risk
            
            **Technical Correlation:**
            Consumer cyclicals lead economic recoveries. When fundamentals improve (rising sales, margins) 
            and technicals show bullish crossovers from oversold levels, this often precedes significant 
            multi-month rallies.
            """)
            
        elif sector == 'Consumer Defensive':
            st.write("""
            **What Drives Consumer Defensive Stocks:**
            - Steady demand regardless of economic conditions
            - Inflation's impact on input costs vs. pricing power
            - Brand loyalty and market share stability
            - Dividend sustainability and growth
            
            **What to Look For:**
            - Consistent earnings and revenue (low volatility)
            - Dividend yield > 2.5% with sustainable payout ratios
            - Operating margins > 15% show pricing resilience
            - Strong balance sheets for dividend security
            
            **Technical Correlation:**
            Defensive stocks often become overbought during market fear. However, if fundamentals remain 
            rock-solid (stable earnings, safe dividend) and technicals show extreme oversold readings during 
            market panic, this creates rare value opportunities in quality names.
            """)
        
        else:
            st.write("""
            **General Investment Considerations:**
            - Understand the company's business model and competitive positioning
            - Analyze revenue and earnings trends over multiple quarters
            - Assess balance sheet health and debt levels
            - Consider industry tailwinds and headwinds
            - Evaluate management quality and capital allocation
            """)
    
    
    with tab3:
        st.subheader("Combined Recommendation")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Technical", f"{stoch_score:.0f}/100")
        col2.metric("Fundamental", f"{fundamental_analysis['rating']:.0f}/100")
        col3.metric("Combined", f"{combined_score:.0f}/100")
        
        st.markdown("---")
        
        if stoch_score >= 60 and fundamental_analysis['rating'] >= 60:
            st.success("**🌟 HIGH CONVICTION BUY**")
            st.write("Both technical and fundamental analysis are positive.")
        elif combined_score >= 60:
            st.info("**✅ QUALIFIED BUY**")
            st.write("Mixed signals but overall positive.")
        elif combined_score >= 50:
            st.warning("**⏸️ HOLD**")
            st.write("Neutral signals. Wait for better setup.")
        else:
            st.error("**❌ AVOID**")
            st.write("Multiple concerns present.")
    
    st.markdown("---")
    
    # Crossover signals
    if bullish_cross:
        st.success(f"**🚀 BULLISH CROSSOVER** - %K crossed above %D")
    elif bearish_cross:
        st.error(f"**📉 BEARISH CROSSOVER** - %K crossed below %D")
    else:
        st.info(f"**No recent crossover** - %K is {'above' if current_k > current_d else 'below'} %D")

# PORTFOLIO PAGE
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

# DISCOVER PAGE
elif st.session_state.page == 'discover':
    st.title("🔍 Discover Stocks")
    st.write("Scan popular stocks by sector")
    
    sectors = get_prospective_stocks()
    selected_sector = st.selectbox("Select Sector", list(sectors.keys()))
    
    if st.button(f"Analyze {selected_sector}", type="primary"):
        st.info(f"Analyzing {len(sectors[selected_sector])} stocks in {selected_sector}...")
        st.write("This feature requires additional implementation for bulk analysis.")
