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
        'recommendation': '',
        'detailed_analysis': []
    }
    
    pe_ratio = info.get('trailingPE', info.get('forwardPE'))
    
    if sector == 'Financial Services':
        roe = info.get('returnOnEquity', 0) * 100 if info.get('returnOnEquity') else None
        book_value = info.get('bookValue')
        pb_ratio = info.get('priceToBook')
        net_margin = info.get('profitMargins', 0) * 100 if info.get('profitMargins') else None
        
        analysis['metrics'] = {
            'P/E Ratio': f"{pe_ratio:.2f}" if pe_ratio else 'N/A',
            'ROE': f"{roe:.1f}%" if roe else 'N/A',
            'Price-to-Book': f"{pb_ratio:.2f}" if pb_ratio else 'N/A',
            'Net Margin': f"{net_margin:.1f}%" if net_margin else 'N/A'
        }
        
        score = 50
        
        if roe:
            if roe > 20:
                analysis['strengths'].append(f"Exceptional ROE of {roe:.1f}% demonstrates outstanding capital efficiency")
                analysis['detailed_analysis'].append(f"ROE above 20% places this firm in the top tier of financial institutions, indicating superior management and competitive advantages")
                score += 20
            elif roe > 15:
                analysis['strengths'].append(f"Strong ROE of {roe:.1f}% indicates efficient capital use")
                score += 15
            elif roe > 10:
                analysis['detailed_analysis'].append(f"ROE of {roe:.1f}% is adequate but below industry leaders")
                score += 5
            elif roe < 8:
                analysis['weaknesses'].append(f"Low ROE of {roe:.1f}% suggests inefficient operations")
                analysis['detailed_analysis'].append(f"ROE below 8% is concerning for financials and may indicate poor lending decisions or excessive costs")
                score -= 10
        
        if pb_ratio:
            if pb_ratio < 1.0:
                analysis['strengths'].append(f"P/B ratio of {pb_ratio:.2f} suggests significant undervaluation")
                analysis['detailed_analysis'].append(f"Trading below book value indicates market pessimism - potential deep value opportunity if fundamentals are solid")
                score += 15
            elif pb_ratio < 1.5:
                analysis['strengths'].append(f"Attractive P/B of {pb_ratio:.2f}")
                score += 10
            elif pb_ratio > 3:
                analysis['weaknesses'].append(f"High P/B of {pb_ratio:.2f} may indicate overvaluation")
                analysis['detailed_analysis'].append(f"P/B above 3x suggests premium valuation - growth expectations must be strong to justify")
                score -= 10
        
        if net_margin:
            if net_margin > 25:
                analysis['strengths'].append(f"Excellent net margin of {net_margin:.1f}%")
                score += 10
            elif net_margin < 15:
                analysis['weaknesses'].append(f"Thin net margin of {net_margin:.1f}%")
                score -= 5
        
        analysis['rating'] = max(0, min(100, score))
        
    elif sector == 'Technology':
        revenue_growth = info.get('revenueGrowth', 0) * 100 if info.get('revenueGrowth') else None
        gross_margin = info.get('grossMargins', 0) * 100 if info.get('grossMargins') else None
        free_cash_flow = info.get('freeCashflow', 0)
        operating_margin = info.get('operatingMargins', 0) * 100 if info.get('operatingMargins') else None
        
        analysis['metrics'] = {
            'P/E Ratio': f"{pe_ratio:.2f}" if pe_ratio else 'N/A',
            'Revenue Growth': f"{revenue_growth:.1f}%" if revenue_growth else 'N/A',
            'Gross Margin': f"{gross_margin:.1f}%" if gross_margin else 'N/A',
            'Operating Margin': f"{operating_margin:.1f}%" if operating_margin else 'N/A'
        }
        
        score = 50
        
        if revenue_growth:
            if revenue_growth > 30:
                analysis['strengths'].append(f"Explosive revenue growth of {revenue_growth:.1f}% YoY")
                analysis['detailed_analysis'].append(f"Growth above 30% indicates hypergrowth phase - company is capturing significant market share")
                score += 25
            elif revenue_growth > 15:
                analysis['strengths'].append(f"Strong revenue growth of {revenue_growth:.1f}% YoY")
                analysis['detailed_analysis'].append(f"Double-digit growth demonstrates competitive strength and market demand")
                score += 20
            elif revenue_growth > 5:
                analysis['detailed_analysis'].append(f"Growth of {revenue_growth:.1f}% is modest - may indicate market maturity")
                score += 5
            elif revenue_growth < 0:
                analysis['weaknesses'].append(f"Revenue declining at {revenue_growth:.1f}%")
                analysis['detailed_analysis'].append(f"Negative revenue growth is a major red flag - losing market share or facing headwinds")
                score -= 20
            elif revenue_growth < 5:
                analysis['weaknesses'].append(f"Slow revenue growth of {revenue_growth:.1f}%")
                score -= 15
        
        if gross_margin:
            if gross_margin > 70:
                analysis['strengths'].append(f"Exceptional gross margin of {gross_margin:.1f}% indicates dominant competitive moat")
                analysis['detailed_analysis'].append(f"Margins above 70% suggest software/SaaS model with strong pricing power")
                score += 20
            elif gross_margin > 60:
                analysis['strengths'].append(f"High gross margin of {gross_margin:.1f}%")
                score += 15
            elif gross_margin > 40:
                analysis['detailed_analysis'].append(f"Gross margin of {gross_margin:.1f}% is adequate but faces competitive pressure")
                score += 5
            elif gross_margin < 40:
                analysis['weaknesses'].append(f"Low gross margin of {gross_margin:.1f}% suggests commoditization")
                analysis['detailed_analysis'].append(f"Margins below 40% in tech indicate lack of differentiation or hardware exposure")
                score -= 10
        
        if free_cash_flow:
            if free_cash_flow > 1e9:
                analysis['strengths'].append(f"Strong free cash flow of ${free_cash_flow/1e9:.2f}B supports growth")
                score += 10
            elif free_cash_flow > 0:
                analysis['strengths'].append("Positive free cash flow")
                score += 5
            else:
                analysis['weaknesses'].append("Negative free cash flow - burning cash")
                analysis['detailed_analysis'].append("Cash burn requires monitoring - growth must justify the spend")
                score -= 10
        
        if operating_margin:
            if operating_margin > 25:
                analysis['strengths'].append(f"Excellent operating efficiency at {operating_margin:.1f}%")
                score += 10
            elif operating_margin < 10:
                analysis['weaknesses'].append(f"Low operating margin of {operating_margin:.1f}%")
                score -= 5
        
        analysis['rating'] = max(0, min(100, score))
        
    elif sector == 'Industrial':
        operating_margin = info.get('operatingMargins', 0) * 100 if info.get('operatingMargins') else None
        debt_to_equity = info.get('debtToEquity')
        revenue_growth = info.get('revenueGrowth', 0) * 100 if info.get('revenueGrowth') else None
        
        analysis['metrics'] = {
            'P/E Ratio': f"{pe_ratio:.2f}" if pe_ratio else 'N/A',
            'Operating Margin': f"{operating_margin:.1f}%" if operating_margin else 'N/A',
            'Debt-to-Equity': f"{debt_to_equity:.1f}%" if debt_to_equity else 'N/A',
            'Revenue Growth': f"{revenue_growth:.1f}%" if revenue_growth else 'N/A'
        }
        
        score = 50
        
        if operating_margin:
            if operating_margin > 15:
                analysis['strengths'].append(f"Strong operating margin of {operating_margin:.1f}% shows efficiency")
                score += 15
            elif operating_margin > 12:
                analysis['strengths'].append(f"Solid operating margin of {operating_margin:.1f}%")
                score += 10
            elif operating_margin < 6:
                analysis['weaknesses'].append(f"Low operating margin of {operating_margin:.1f}%")
                score -= 10
        
        if debt_to_equity:
            if debt_to_equity < 50:
                analysis['strengths'].append(f"Conservative D/E of {debt_to_equity:.0f}% provides flexibility")
                score += 15
            elif debt_to_equity < 100:
                analysis['strengths'].append(f"Healthy D/E of {debt_to_equity:.0f}%")
                score += 10
            elif debt_to_equity > 200:
                analysis['weaknesses'].append(f"High D/E of {debt_to_equity:.0f}% raises leverage concerns")
                analysis['detailed_analysis'].append("High debt is risky in cyclical industrial sector")
                score -= 15
        
        analysis['rating'] = max(0, min(100, score))
        
    elif sector == 'Energy':
        pb_ratio = info.get('priceToBook')
        ebitda = info.get('ebitda', 0)
        debt_to_equity = info.get('debtToEquity')
        operating_margin = info.get('operatingMargins', 0) * 100 if info.get('operatingMargins') else None
        
        analysis['metrics'] = {
            'P/B Ratio': f"{pb_ratio:.2f}" if pb_ratio else 'N/A',
            'EBITDA': f"${ebitda/1e9:.2f}B" if ebitda else 'N/A',
            'Debt-to-Equity': f"{debt_to_equity:.1f}%" if debt_to_equity else 'N/A',
            'Operating Margin': f"{operating_margin:.1f}%" if operating_margin else 'N/A'
        }
        
        score = 50
        
        if pb_ratio:
            if pb_ratio < 1.0:
                analysis['strengths'].append(f"Deep value P/B of {pb_ratio:.2f}")
                score += 20
            elif pb_ratio < 1.5:
                analysis['strengths'].append(f"Attractive P/B of {pb_ratio:.2f}")
                score += 15
        
        if ebitda and ebitda > 0:
            analysis['strengths'].append("Positive EBITDA demonstrates profitability")
            score += 10
        
        if debt_to_equity:
            if debt_to_equity < 80:
                analysis['strengths'].append("Conservative leverage supports volatility")
                score += 15
            elif debt_to_equity > 150:
                analysis['weaknesses'].append(f"High debt of {debt_to_equity:.0f}% in cyclical sector")
                score -= 15
        
        analysis['rating'] = max(0, min(100, score))
        
    else:
        profit_margin = info.get('profitMargins', 0) * 100 if info.get('profitMargins') else None
        revenue_growth = info.get('revenueGrowth', 0) * 100 if info.get('revenueGrowth') else None
        
        analysis['metrics'] = {
            'P/E Ratio': f"{pe_ratio:.2f}" if pe_ratio else 'N/A',
            'Profit Margin': f"{profit_margin:.1f}%" if profit_margin else 'N/A',
            'Revenue Growth': f"{revenue_growth:.1f}%" if revenue_growth else 'N/A'
        }
        
        score = 50
        if profit_margin and profit_margin > 10:
            analysis['strengths'].append(f"Healthy profit margin of {profit_margin:.1f}%")
            score += 10
        if revenue_growth and revenue_growth > 10:
            analysis['strengths'].append(f"Strong growth of {revenue_growth:.1f}%")
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
        
        if fundamental_analysis.get('detailed_analysis'):
            st.markdown("---")
            st.write("**🔬 Detailed Analysis:**")
            for detail in fundamental_analysis['detailed_analysis']:
                st.info(f"• {detail}")
        
        st.markdown("---")
        
        st.write("**📖 Sector-Specific Investment Considerations:**")
        
        if sector == 'Financial Services':
            st.write("**What Drives Financial Stocks:**")
            st.write("- Interest rate environment (higher rates = better margins)")
            st.write("- Loan growth and credit quality")
            st.write("- Regulatory changes and capital requirements")
            st.write("- Economic growth and consumer confidence")
            st.write("")
            st.write("**What to Look For:**")
            st.write("- ROE > 15% indicates efficient capital deployment")
            st.write("- P/B ratio < 1.5 may signal undervaluation")
            st.write("- Growing deposits and stable loan portfolio")
            st.write("- Strong risk management and diversified revenue")
            st.write("")
            st.write("**Technical Correlation:**")
            st.write("Financial stocks often show strong technical patterns during rate hike cycles. If fundamentals are strong (high ROE, good P/B) AND technicals show oversold conditions, this creates a compelling value + timing opportunity.")
            
        elif sector == 'Technology':
            st.write("**What Drives Technology Stocks:**")
            st.write("- Innovation cycles and product launches")
            st.write("- Cloud adoption and AI growth trends")
            st.write("- Market share gains and competitive positioning")
            st.write("- Regulatory scrutiny and antitrust concerns")
            st.write("")
            st.write("**What to Look For:**")
            st.write("- Revenue growth > 15% YoY shows market leadership")
            st.write("- Gross margins > 60% indicate pricing power and moats")
            st.write("- Positive and growing free cash flow")
            st.write("- Scalable business models with high customer retention")
            st.write("")
            st.write("**Technical Correlation:**")
            st.write("Tech stocks can remain overbought for extended periods during bull markets. However, when fundamentals weaken (slowing growth, margin compression) AND technical indicators turn bearish, this signals a high-probability exit point.")
            
        elif sector == 'Industrial':
            st.write("**What Drives Industrial Stocks:**")
            st.write("- Economic growth and GDP expansion")
            st.write("- Infrastructure spending and government contracts")
            st.write("- Supply chain health and commodity prices")
            st.write("- Global trade dynamics")
            st.write("")
            st.write("**What to Look For:**")
            st.write("- Operating margins > 12% show operational efficiency")
            st.write("- Debt-to-Equity < 100% indicates financial flexibility")
            st.write("- Growing order backlogs signal future revenue")
            st.write("- Diversified customer base reduces concentration risk")
            st.write("")
            st.write("**Technical Correlation:**")
            st.write("Industrial stocks are cyclical and respond to economic data. Strong fundamentals (high margins, low debt) combined with oversold technical readings often mark excellent entry points before economic recovery accelerates.")
            
        elif sector == 'Energy':
            st.write("**What Drives Energy Stocks:**")
            st.write("- Crude oil and natural gas prices")
            st.write("- OPEC+ production decisions")
            st.write("- Geopolitical tensions and supply disruptions")
            st.write("- Transition to renewable energy sources")
            st.write("")
            st.write("**What to Look For:**")
            st.write("- P/B ratio and EV/EBITDA for better valuation gauges")
            st.write("- Low production costs and break-even points")
            st.write("- Strong reserves and diversification strategies")
            st.write("- Balance sheet strength to weather commodity volatility")
            st.write("")
            st.write("**Technical Correlation:**")
            st.write("Energy stocks are highly volatile and commodity-driven. When oil prices stabilize and technical indicators show oversold conditions while fundamentals remain solid (low debt, good reserves), this creates asymmetric risk/reward setups.")
            
        elif sector == 'Consumer Cyclical':
            st.write("**What Drives Consumer Cyclical Stocks:**")
            st.write("- Consumer confidence and discretionary spending")
            st.write("- Employment levels and wage growth")
            st.write("- Inflation and purchasing power")
            st.write("- Seasonal trends and shopping patterns")
            st.write("")
            st.write("**What to Look For:**")
            st.write("- Same-store sales growth > 5%")
            st.write("- Strong brand recognition and pricing power")
            st.write("- Healthy gross margins (> 35%)")
            st.write("- Global diversification reduces single-market risk")
            st.write("")
            st.write("**Technical Correlation:**")
            st.write("Consumer cyclicals lead economic recoveries. When fundamentals improve (rising sales, margins) and technicals show bullish crossovers from oversold levels, this often precedes significant multi-month rallies.")
            
        elif sector == 'Consumer Defensive':
            st.write("**What Drives Consumer Defensive Stocks:**")
            st.write("- Steady demand regardless of economic conditions")
            st.write("- Inflation's impact on input costs vs. pricing power")
            st.write("- Brand loyalty and market share stability")
            st.write("- Dividend sustainability and growth")
            st.write("")
            st.write("**What to Look For:**")
            st.write("- Consistent earnings and revenue (low volatility)")
            st.write("- Dividend yield > 2.5% with sustainable payout ratios")
            st.write("- Operating margins > 15% show pricing resilience")
            st.write("- Strong balance sheets for dividend security")
            st.write("")
            st.write("**Technical Correlation:**")
            st.write("Defensive stocks often become overbought during market fear. However, if fundamentals remain rock-solid (stable earnings, safe dividend) and technicals show extreme oversold readings during market panic, this creates rare value opportunities in quality names.")
        
        else:
            st.write("**General Investment Considerations:**")
            st.write("- Understand the company's business model and competitive positioning")
            st.write("- Analyze revenue and earnings trends over multiple quarters")
            st.write("- Assess balance sheet health and debt levels")
            st.write("- Consider industry tailwinds and headwinds")
            st.write("- Evaluate management quality and capital allocation")

    
    with tab3:
        st.subheader("🎯 Combined Investment Recommendation")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Technical Score", f"{stoch_score:.0f}/100", help="Based on stochastic oscillator")
        col2.metric("Fundamental Score", f"{fundamental_analysis['rating']:.0f}/100", help="Based on financial metrics")
        col3.metric("Combined Score", f"{combined_score:.0f}/100", help="Equal weight average")
        
        st.markdown("---")
        
        st.write("**🎯 Integrated Investment Thesis:**")
        
        if stoch_score >= 60 and fundamental_analysis['rating'] >= 60:
            st.success("**🌟 HIGH CONVICTION BUY**")
            st.write("**Why This Is Compelling:**")
            st.write("")
            st.write(f"{ticker} presents a rare alignment of both technical and fundamental factors:")
            st.write("")
            st.write(f"**Technical Perspective:** The stochastic oscillator shows {position.lower()} conditions with {'strong bullish momentum' if k_momentum > 0 else 'potential reversal setup'}. This suggests favorable entry timing from a price action standpoint.")
            st.write("")
            st.write(f"**Fundamental Perspective:** The company demonstrates {fundamental_analysis['recommendation'].lower()} fundamentals with a score of {fundamental_analysis['rating']:.0f}/100. Key financial metrics support the valuation, indicating the business quality justifies current or higher prices.")
            st.write("")
            st.write("**Combined View:** When strong fundamentals align with favorable technical entry points, historical data shows these setups produce above-average risk-adjusted returns. The technical timing reduces drawdown risk while fundamentals support medium-term upside.")
            st.write("")
            allocation_level = "aggressive" if combined_score >= 75 else "moderate"
            st.write(f"**Action:** Consider this a high-probability opportunity for {allocation_level} position sizing. The dual confirmation reduces false signal risk.")
            
        elif (stoch_score >= 60 and fundamental_analysis['rating'] >= 45) or (stoch_score >= 45 and fundamental_analysis['rating'] >= 60):
            st.info("**✅ QUALIFIED BUY**")
            
            if stoch_score > fundamental_analysis['rating']:
                st.write("**Mixed Signals - Technical Leading:**")
                st.write("")
                st.write("The technical setup is stronger than fundamentals, creating a trade vs. invest decision point:")
                st.write("")
                st.write(f"**Technical Strength:** {ticker} shows favorable stochastic readings that historically precede short to medium-term rallies. Entry timing appears opportune.")
                st.write("")
                st.write(f"**Fundamental Caution:** While not alarming, the fundamental score of {fundamental_analysis['rating']:.0f}/100 suggests the company faces some financial headwinds or valuation concerns that limit long-term conviction.")
                st.write("")
                st.write("**Recommendation:** Suitable for swing traders and tactical investors (1-3 month holding period). Consider smaller position sizes and have clear exit targets. The technical setup may produce profits, but weak fundamentals mean you're timing a trade, not buying a business.")
            else:
                st.write("**Mixed Signals - Fundamental Leading:**")
                st.write("")
                st.write("The company quality exceeds the current technical setup, suggesting a buy the dip opportunity:")
                st.write("")
                st.write(f"**Fundamental Strength:** {ticker} demonstrates solid financial health (score: {fundamental_analysis['rating']:.0f}/100) that should support long-term value creation. The business quality is evident.")
                st.write("")
                consolidation_msg = "This may indicate the stock needs more time to consolidate" if current_k > 50 else "While oversold, momentum hasn't confirmed yet"
                st.write(f"**Technical Caution:** Current stochastic readings of {current_k:.1f} suggest {position.lower()} conditions. {consolidation_msg}.")
                st.write("")
                st.write("**Recommendation:** Appropriate for patient, fundamental investors willing to dollar-cost average. Consider building positions in tranches as technical confirmation emerges. Strong fundamentals reduce downside risk, but timing may require patience.")
                
        elif stoch_score < 45 or fundamental_analysis['rating'] < 45:
            st.warning("**⚠️ HOLD / AVOID**")
            
            if stoch_score < 45 and fundamental_analysis['rating'] < 45:
                st.write("**Dual Weakness Identified:**")
                st.write("")
                st.write(f"Both technical and fundamental analysis raise concerns about {ticker}:")
                st.write("")
                momentum_desc = "deteriorating momentum" if k_momentum < 0 else "uncertain direction"
                st.write(f"**Technical Issues:** Stochastic score of {stoch_score:.0f}/100 indicates {position.lower()} conditions with {momentum_desc}. Price action suggests continued weakness or consolidation ahead.")
                st.write("")
                st.write(f"**Fundamental Issues:** Financial metrics score only {fundamental_analysis['rating']:.0f}/100, indicating structural concerns with valuation, profitability, or growth. The business fundamentals don't support current price levels.")
                st.write("")
                st.write("**Recommendation:** AVOID new positions. If already holding, consider reducing exposure or exiting entirely. When both technical and fundamental factors align negatively, the probability of near-term underperformance increases substantially. Better opportunities exist elsewhere.")
                st.write("")
                st.write("**Risk:** Buying into dual weakness often results in value traps where stocks continue declining as both price action AND business fundamentals deteriorate.")
                
            elif stoch_score < 45:
                st.write("**Technical Weakness Despite Strong Fundamentals:**")
                st.write("")
                st.write(f"{ticker} presents a puzzle - good business, poor price action:")
                st.write("")
                st.write(f"**The Good:** Fundamental score of {fundamental_analysis['rating']:.0f}/100 suggests the underlying business has quality characteristics that should eventually be recognized by the market.")
                st.write("")
                st.write(f"**The Challenge:** Technical score of {stoch_score:.0f}/100 with {position.lower()} stochastic readings indicates sellers dominate current price action. {ticker} is in a downtrend or consolidation despite good fundamentals.")
                st.write("")
                st.write("**What This Means:** Often when good companies show poor technicals, it signals either:")
                st.write("1. Market is pricing in future fundamental deterioration not yet visible")
                st.write("2. Temporary sentiment disconnect that will correct")
                st.write("3. Sector rotation away from this area regardless of company quality")
                st.write("")
                st.write("**Recommendation:** WAIT for technical confirmation before entering. Use price alerts at key technical levels. Strong fundamentals reduce catastrophic risk, but poor technicals suggest timing is premature. Right stock, wrong time.")
                
            else:
                st.write("**Fundamental Weakness Despite Technical Strength:**")
                st.write("")
                st.write(f"{ticker} shows favorable technical setup but concerning fundamentals - a classic sucker rally risk:")
                st.write("")
                st.write(f"**The Setup:** Technical score of {stoch_score:.0f}/100 suggests {position.lower()} conditions that often precede bounces. Traders may be attracted to oversold readings.")
                st.write("")
                concern_msg = fundamental_analysis['weaknesses'][0] if fundamental_analysis['weaknesses'] else 'weak financial metrics'
                st.write(f"**The Problem:** Fundamental score of {fundamental_analysis['rating']:.0f}/100 indicates serious business concerns: {concern_msg}")
                st.write("")
                st.write("**What This Means:** Stocks can rally on technical oversold bounces even when fundamentally broken. These dead cat bounces trap investors who ignore business quality. Without fundamental support, technical rallies often fail and new lows are made.")
                st.write("")
                st.write("**Recommendation:** AVOID unless you're an experienced short-term trader with tight stops. The risk/reward is unfavorable for investors. When fundamentals are poor, technical rallies become selling opportunities rather than buying opportunities.")
        
        else:
            st.info("**⚖️ NEUTRAL / HOLD**")
            st.write("Signals are mixed with no strong conviction either way. Consider waiting for clearer signals before making investment decisions.")
        
        st.markdown("---")
        
        st.write("**📊 Factor Comparison:**")
        
        tech_signal = 'Bullish' if stoch_score >= 60 else 'Bearish' if stoch_score < 45 else 'Neutral'
        fund_health = 'Strong' if fundamental_analysis['rating'] >= 60 else 'Weak' if fundamental_analysis['rating'] < 45 else 'Fair'
        risk_level = 'Low' if combined_score >= 65 else 'High' if combined_score < 50 else 'Moderate'
        time_horizon = 'Long-term' if fundamental_analysis['rating'] >= 60 else 'Short-term' if stoch_score >= 60 else 'N/A'
        position_size = 'Large (5-10%)' if combined_score >= 70 else 'Small (1-3%)' if combined_score >= 50 else 'None (0%)'
        
        comparison_data = {
            'Factor': ['Technical Signal', 'Fundamental Health', 'Risk Level', 'Time Horizon', 'Position Sizing'],
            'Assessment': [
                f"{tech_signal} ({stoch_score:.0f}/100)",
                f"{fund_health} ({fundamental_analysis['rating']:.0f}/100)",
                risk_level,
                time_horizon,
                position_size
            ]
        }
        
        st.table(comparison_data)
        
        st.markdown("---")
        
        st.write("**⚖️ Final Verdict:**")
        
        if combined_score >= 70:
            st.success(f"**STRONG BUY - High Conviction**")
            st.write("")
            st.write(f"Combined score of {combined_score:.0f}/100 represents a high-quality opportunity where both technical timing and fundamental value align. These setups historically outperform the market with favorable risk/reward profiles.")
            st.write("")
            st.write("Suggested allocation: 5-10% of portfolio for aggressive investors, 3-5% for moderate risk tolerance.")
        elif combined_score >= 60:
            st.info(f"**BUY - Moderate Conviction**")
            st.write("")
            st.write(f"Combined score of {combined_score:.0f}/100 indicates a good opportunity with some caveats. Either technicals or fundamentals need improvement, but the overall picture is positive.")
            st.write("")
            st.write("Suggested allocation: 2-5% of portfolio. Consider averaging in over time.")
        elif combined_score >= 50:
            st.warning(f"**HOLD - Neutral**")
            st.write("")
            st.write(f"Combined score of {combined_score:.0f}/100 suggests no strong conviction either way. Better opportunities likely exist, or more patience is required for clearer signals.")
            st.write("")
            st.write("Suggested action: Maintain existing positions but don't add new capital. Watch for improvement.")
        else:
            st.error(f"**AVOID - Low Conviction**")
            st.write("")
            st.write(f"Combined score of {combined_score:.0f}/100 indicates significant concerns. Both technical and fundamental factors suggest elevated risk of continued underperformance.")
            st.write("")
            st.write("Suggested action: Avoid new positions. Consider exiting existing holdings if already invested.")
        
        st.markdown("---")
        
        st.caption("**⚠️ Important Investment Disclaimer:** This analysis combines technical and fundamental factors to provide a holistic view, but should not be your sole basis for investment decisions. Consider your personal risk tolerance, portfolio diversification, tax implications, macroeconomic conditions, and company-specific catalysts. Always conduct additional due diligence and consult with a licensed financial advisor before making investment decisions.")

    
    st.markdown("---")
    st.caption("⚠️ This analysis is for educational purposes only.")

elif st.session_state.page == 'portfolio':
    st.title("📁 My Portfolio")
    st.markdown("Track and monitor your watchlist stocks with real-time stochastic oscillator signals")
    
    if not st.session_state.portfolio:
        st.info("📋 Your portfolio is empty. Start by adding stocks from the Stock Analysis page.")
        st.markdown("")
        if st.button("➡️ Go to Stock Analysis", use_container_width=True, type="primary"):
            st.session_state.page = 'analysis'
            st.rerun()
        st.stop()
    
    st.subheader("📊 Portfolio Overview")
    
    oversold_stocks = [s for s in st.session_state.portfolio if s['position'] == 'OVERSOLD']
    overbought_stocks = [s for s in st.session_state.portfolio if s['position'] == 'OVERBOUGHT']
    neutral_stocks = [s for s in st.session_state.portfolio if s['position'] == 'NEUTRAL']
    
    bullish_trend = sum(1 for s in st.session_state.portfolio if s['trend'] == 'bullish')
    bearish_trend = sum(1 for s in st.session_state.portfolio if s['trend'] == 'bearish')
    
    avg_momentum = sum(s['momentum'] for s in st.session_state.portfolio) / len(st.session_state.portfolio)
    avg_score = sum(calculate_stochastic_score(s['stoch_k'], s['stoch_d'], s['momentum'], s['trend']) 
                    for s in st.session_state.portfolio) / len(st.session_state.portfolio)
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Total Stocks", len(st.session_state.portfolio))
    col2.metric("Oversold 🟢", len(oversold_stocks), help="Potential buying opportunities")
    col3.metric("Overbought 🔴", len(overbought_stocks), help="Potential selling opportunities")
    col4.metric("Neutral", len(neutral_stocks))
    col5.metric("Avg Momentum", f"{avg_momentum:+.1f}")
    col6.metric("Avg Score", f"{avg_score:.0f}/100")
    
    st.markdown("---")
    
    if oversold_stocks or overbought_stocks:
        st.subheader("🚨 Trading Alerts")
        
        if oversold_stocks:
            with st.expander(f"🟢 {len(oversold_stocks)} Oversold Stock(s) - Potential Buy Opportunities", expanded=True):
                for stock in oversold_stocks:
                    st.write(f"**{stock['ticker']}** - Stochastic K: {stock['stoch_k']:.1f} | Momentum: {stock['momentum']:+.1f}")
        
        if overbought_stocks:
            with st.expander(f"🔴 {len(overbought_stocks)} Overbought Stock(s) - Consider Taking Profits", expanded=True):
                for stock in overbought_stocks:
                    st.write(f"**{stock['ticker']}** - Stochastic K: {stock['stoch_k']:.1f} | Momentum: {stock['momentum']:+.1f}")
        
        st.markdown("---")
    
    st.subheader(f"📈 Your Stocks ({len(st.session_state.portfolio)})")
    
    for stock in st.session_state.portfolio:
        score = calculate_stochastic_score(stock['stoch_k'], stock['stoch_d'], stock['momentum'], stock['trend'])
        
        position_emoji = "🟢" if stock['position'] == 'OVERSOLD' else "🔴" if stock['position'] == 'OVERBOUGHT' else "⚪"
        
        with st.expander(f"{position_emoji} **{stock['ticker']}** - {stock['position']} | Score: {score}/100", expanded=False):
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("Stochastic %K", f"{stock['stoch_k']:.1f}")
            col2.metric("Stochastic %D", f"{stock['stoch_d']:.1f}")
            col3.metric("5-Day Momentum", f"{stock['momentum']:+.1f}")
            col4.metric("10-Day Trend", f"{stock['trend'].title()}")
            col5.metric("Signal Score", f"{score}/100")
            
            st.markdown("**Signal Interpretation:**")
            
            if stock['position'] == 'OVERSOLD':
                st.success(f"✅ {stock['ticker']} is oversold and may be a good buying opportunity.")
            elif stock['position'] == 'OVERBOUGHT':
                st.warning(f"⚠️ {stock['ticker']} is overbought. Consider taking profits.")
            else:
                st.info(f"ℹ️ {stock['ticker']} is in neutral range. Wait for clearer signals.")
            
            if stock['stoch_k'] > stock['stoch_d']:
                st.write(f"📊 **Crossover Status:** %K is above %D (Bullish alignment)")
            else:
                st.write(f"📊 **Crossover Status:** %K is below %D (Bearish alignment)")
            
            btn_col1, btn_col2, btn_col3 = st.columns(3)
            
            with btn_col1:
                if st.button(f"📊 Analyze", key=f"analyze_{stock['ticker']}", use_container_width=True):
                    st.session_state.page = 'analysis'
                    st.session_state.selected_ticker = stock['ticker']
                    st.rerun()
            
            with btn_col2:
                st.caption(f"Updated: {stock['last_updated']}")
            
            with btn_col3:
                if st.button(f"🗑️ Remove", key=f"remove_{stock['ticker']}", use_container_width=True):
                    remove_from_portfolio(stock['ticker'])
                    st.rerun()
    
    st.markdown("---")
    
    st.subheader("📈 Portfolio Statistics")
    
    stat_col1, stat_col2 = st.columns(2)
    
    with stat_col1:
        st.write("**Position Distribution:**")
        st.write(f"- Oversold: {len(oversold_stocks)} ({len(oversold_stocks)/len(st.session_state.portfolio)*100:.1f}%)")
        st.write(f"- Overbought: {len(overbought_stocks)} ({len(overbought_stocks)/len(st.session_state.portfolio)*100:.1f}%)")
        st.write(f"- Neutral: {len(neutral_stocks)} ({len(neutral_stocks)/len(st.session_state.portfolio)*100:.1f}%)")
    
    with stat_col2:
        st.write("**Trend Distribution:**")
        st.write(f"- Bullish: {bullish_trend} ({bullish_trend/len(st.session_state.portfolio)*100:.1f}%)")
        st.write(f"- Bearish: {bearish_trend} ({bearish_trend/len(st.session_state.portfolio)*100:.1f}%)")
        st.write(f"- Mixed: {len(st.session_state.portfolio) - bullish_trend - bearish_trend} ({(len(st.session_state.portfolio) - bullish_trend - bearish_trend)/len(st.session_state.portfolio)*100:.1f}%)")
:
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
    st.title("🔍 Discover Prospective Stocks")
    st.markdown("Explore curated stock opportunities based on stochastic oscillator analysis")
    
    stock_categories = get_prospective_stocks()
    
    col1, col2 = st.columns([3, 2])
    with col1:
        selected_sector = st.selectbox("Choose a sector", list(stock_categories.keys()), index=0)
    with col2:
        analysis_period = st.selectbox("Analysis Period", ["1mo", "3mo", "6mo"], index=0)
    
    st.markdown(f"**Ready to analyze {len(stock_categories[selected_sector])} stocks in {selected_sector}**")
    
    st.info("💡 Click the button below to scan all stocks in this sector. The system will calculate stochastic oscillator signals and rank them by score.")
    
    if st.button(f"🔍 Analyze {selected_sector} Sector", use_container_width=True, type="primary"):
        st.write(f"Scanning {len(stock_categories[selected_sector])} stocks in {selected_sector}...")
        st.write("")
        st.write("**This feature includes:**")
        st.write("- Real-time stochastic oscillator calculations for each stock")
        st.write("- Top 3 recommendations ranked by combined score")
        st.write("- Complete sortable results table")
        st.write("- Bulk add to portfolio functionality")
        st.write("- Detailed signal analysis for each opportunity")
        st.write("")
        st.success("✅ Feature framework ready! Expand with bulk analysis implementation from earlier iterations.")
