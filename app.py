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
        
        # EDUCATIONAL CONTEXT
        with st.expander("📚 Understanding the Stochastic Oscillator (Click to Expand)"):
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
        
        # Display sector
        st.info(f"**Sector:** {fundamental_analysis['sector']}")
        
        # Key metrics
        st.write("**Key Financial Metrics:**")
        metrics_cols = st.columns(len(fundamental_analysis['metrics']))
        for idx, (metric, value) in enumerate(fundamental_analysis['metrics'].items()):
            with metrics_cols[idx]:
                st.metric(metric, value)
        
        st.markdown("---")
        
        # Fundamental rating
        fund_score = fundamental_analysis['rating']
        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric("Fundamental Score", f"{fund_score:.0f}/100")
            st.metric("Recommendation", fundamental_analysis['recommendation'])
        
        with col2:
            # Score interpretation
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
        
        # Strengths
        if fundamental_analysis['strengths']:
            st.write("**✅ Fundamental Strengths:**")
            for strength in fundamental_analysis['strengths']:
                st.success(f"• {strength}")
        
        # Weaknesses
        if fundamental_analysis['weaknesses']:
            st.write("**⚠️ Fundamental Concerns:**")
            for weakness in fundamental_analysis['weaknesses']:
                st.warning(f"• {weakness}")
        
        st.markdown("---")
        
        # Sector-specific guidance
        st.write("**📖 Sector-Specific Investment Considerations:**")
        
        if fundamental_analysis['sector'] == 'Financial Services':
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
            
        elif fundamental_analysis['sector'] == 'Technology':
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
            
        elif fundamental_analysis['sector'] == 'Industrial':
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
            
        elif fundamental_analysis['sector'] == 'Energy':
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
            
        elif fundamental_analysis['sector'] == 'Consumer Cyclical':
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
            
        elif fundamental_analysis['sector'] == 'Consumer Defensive':
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
        st.subheader("🎯 Combined Investment Recommendation")
        
        # Display combined score prominently
        score_col1, score_col2, score_col3 = st.columns(3)
        with score_col1:
            st.metric("Technical Score", f"{stoch_score:.0f}/100", 
                     help="Based on stochastic oscillator analysis")
        with score_col2:
            st.metric("Fundamental Score", f"{fund_score:.0f}/100",
                     help="Based on sector-specific financial metrics")
        with score_col3:
            st.metric("Combined Score", f"{combined_score:.0f}/100",
                     help="Equal weight of technical and fundamental scores")
        
        st.markdown("---")
        
        # Generate integrated recommendation
        st.write("**🎯 Integrated Investment Thesis:**")
        
        # Best case: Both strong
        if stoch_score >= 60 and fund_score >= 60:
            st.success("**🌟 HIGH CONVICTION BUY**")
            st.write(f"""
            **Why This Is Compelling:**
            
            {ticker} presents a rare alignment of both technical and fundamental factors:
            
            **Technical Perspective:** The stochastic oscillator shows {position.lower()} conditions with 
            {'strong bullish momentum' if k_momentum > 0 else 'potential reversal setup'}. This suggests 
            favorable entry timing from a price action standpoint.
            
            **Fundamental Perspective:** The company demonstrates {fundamental_analysis['recommendation'].lower()} 
            fundamentals with a score of {fund_score:.0f}/100. Key financial metrics support the valuation, 
            indicating the business quality justifies current or higher prices.
            
            **Combined View:** When strong fundamentals align with favorable technical entry points, 
            historical data shows these setups produce above-average risk-adjusted returns. The technical 
            timing reduces drawdown risk while fundamentals support medium-term upside.
            
            **Action:** Consider this a high-probability opportunity for {"aggressive" if combined_score >= 75 else "moderate"} 
            position sizing. The dual confirmation reduces false signal risk.
            """)
            
        # Good case: One strong, one moderate
        elif (stoch_score >= 60 and fund_score >= 45) or (stoch_score >= 45 and fund_score >= 60):
            st.info("**✅ QUALIFIED BUY**")
            
            if stoch_score > fund_score:
                st.write(f"""
                **Mixed Signals - Technical Leading:**
                
                The technical setup is stronger than fundamentals, creating a "trade vs. invest" decision point:
                
                **Technical Strength:** {ticker} shows favorable stochastic readings that historically 
                precede short to medium-term rallies. Entry timing appears opportune.
                
                **Fundamental Caution:** While not alarming, the fundamental score of {fund_score:.0f}/100 
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
                
                **Fundamental Strength:** {ticker} demonstrates solid financial health (score: {fund_score:.0f}/100) 
                that should support long-term value creation. The business quality is evident.
                
                **Technical Caution:** Current stochastic readings of {current_k:.1f} suggest {position.lower()} 
                conditions. {"This may indicate the stock needs more time to consolidate" if current_k > 50 else "While oversold, momentum hasn't confirmed yet"}.
                
                **Recommendation:** Appropriate for patient, fundamental investors willing to dollar-cost average. 
                Consider building positions in tranches as technical confirmation emerges. Strong fundamentals 
                reduce downside risk, but timing may require patience.
                """)
                
        # Weak case: One weak
        elif stoch_score < 45 or fund_score < 45:
            st.warning("**⚠️ HOLD / AVOID**")
            
            if stoch_score < 45 and fund_score < 45:
                st.write(f"""
                **Dual Weakness Identified:**
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
    # Check if already in portfolio
    for stock in st.session_state.portfolio:
        if stock['ticker'] == ticker:
            # Update existing entry
            stock['stoch_k'] = current_k
            stock['stoch_d'] = current_d
            stock['momentum'] = k_momentum
            stock['trend'] = trend
            stock['position'] = "OVERSOLD" if current_k < 20 else "OVERBOUGHT" if current_k > 80 else "NEUTRAL"
            stock['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M")
            return False  # Already existed
    
    # Add new entry
    st.session_state.portfolio.append({
        'ticker': ticker,
        'stoch_k': current_k,
        'stoch_d': current_d,
        'momentum': k_momentum,
        'trend': trend,
        'position': "OVERSOLD" if current_k < 20 else "OVERBOUGHT" if current_k > 80 else "NEUTRAL",
        'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    return True  # New addition

def remove_from_portfolio(ticker):
    """Remove stock from portfolio"""
    st.session_state.portfolio = [s for s in st.session_state.portfolio if s['ticker'] != ticker]

def get_prospective_stocks():
    """Return a curated list of popular stocks to analyze"""
    return {
        "Tech Giants": ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA'],
        "Finance": ['JPM', 'BAC', 'GS', 'WFC', 'V', 'MA', 'BRK-B'],
        "Healthcare": ['JNJ', 'UNH', 'PFE', 'ABBV', 'TMO', 'ABT', 'MRK'],
        "Consumer": ['WMT', 'HD', 'NKE', 'SBUX', 'MCD', 'DIS', 'COST'],
        "Energy": ['XOM', 'CVX', 'COP', 'SLB', 'EOG', 'MPC', 'PSX'],
        "Telecom": ['T', 'VZ', 'TMUS', 'CMCSA'],
        "Industrial": ['BA', 'CAT', 'GE', 'HON', 'UPS', 'MMM', 'DE'],
        "Crypto/Fintech": ['COIN', 'SQ', 'PYPL', 'HOOD']
    }

def analyze_multiple_stocks(tickers, period="1mo"):
    """Analyze multiple stocks and return their stochastic data"""
    results = []
    
    for ticker in tickers:
        try:
            data, info, error = get_stock_data(ticker, period)
            
            if error or data is None or data.empty:
                continue
                
            if len(data) < 14:  # Need at least 14 days for stochastic
                continue
                
            k_period = 14
            d_period = 3
            
            # Calculate stochastic
            data['STOCH_K'], data['STOCH_D'] = calculate_stochastic(
                data['High'], data['Low'], data['Close'], k_period, d_period
            )
            
            # Skip if stochastic calculation failed
            if data['STOCH_K'].isna().all() or data['STOCH_D'].isna().all():
                continue
            
            current_k = data['STOCH_K'].iloc[-1]
            current_d = data['STOCH_D'].iloc[-1]
            
            # Skip if values are NaN
            if pd.isna(current_k) or pd.isna(current_d):
                continue
            
            k_momentum = current_k - data['STOCH_K'].iloc[-5] if len(data) >= 5 else 0
            recent_k = data['STOCH_K'].iloc[-10:] if len(data) >= 10 else data['STOCH_K']
            trend = "bullish" if recent_k.is_monotonic_increasing else "bearish" if recent_k.is_monotonic_decreasing else "mixed"
            
            price = data['Close'].iloc[-1]
            change = ((data['Close'].iloc[-1] / data['Close'].iloc[0]) - 1) * 100 if len(data) > 0 else 0
            
            position = "OVERSOLD" if current_k < 20 else "OVERBOUGHT" if current_k > 80 else "NEUTRAL"
            score = calculate_stochastic_score(current_k, current_d, k_momentum, trend)
            
            # Detect crossovers
            if len(data) >= 2:
                prev_k = data['STOCH_K'].iloc[-2]
                prev_d = data['STOCH_D'].iloc[-2]
                if pd.isna(prev_k) or pd.isna(prev_d):
                    bullish_cross = False
                    bearish_cross = False
                else:
                    bullish_cross = (prev_k <= prev_d) and (current_k > current_d)
                    bearish_cross = (prev_k >= prev_d) and (current_k < current_d)
            else:
                bullish_cross = False
                bearish_cross = False
            
            results.append({
                'ticker': ticker,
                'name': info.get('longName', ticker) if info else ticker,
                'price': price,
                'change': change,
                'stoch_k': current_k,
                'stoch_d': current_d,
                'momentum': k_momentum,
                'trend': trend,
                'position': position,
                'score': score,
                'bullish_cross': bullish_cross,
                'bearish_cross': bearish_cross,
                'volume': data['Volume'].iloc[-1] if 'Volume' in data.columns else 0
            })
        except Exception as e:
            # Skip this ticker and continue
            continue
    
    return results

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

def get_sector_from_info(info):
    """Determine sector from stock info"""
    sector = info.get('sector', '').lower()
    industry = info.get('industry', '').lower()
    
    # Map to our analysis categories
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
        'rating': 0,  # Out of 100
        'recommendation': ''
    }
    
    # Common metrics for all sectors
    market_cap = info.get('marketCap', 0)
    pe_ratio = info.get('trailingPE', info.get('forwardPE'))
    revenue = info.get('totalRevenue', 0)
    
    if sector == 'Financial Services':
        # Financial-specific metrics
        roe = info.get('returnOnEquity', 0) * 100 if info.get('returnOnEquity') else None
        book_value = info.get('bookValue')
        pb_ratio = info.get('priceToBook')
        
        analysis['metrics'] = {
            'P/E Ratio': pe_ratio,
            'ROE': f"{roe:.1f}%" if roe else 'N/A',
            'Price-to-Book': pb_ratio,
            'Book Value': f"${book_value:.2f}" if book_value else 'N/A'
        }
        
        # Rating logic
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
        # Tech-specific metrics
        revenue_growth = info.get('revenueGrowth', 0) * 100 if info.get('revenueGrowth') else None
        gross_margin = info.get('grossMargins', 0) * 100 if info.get('grossMargins') else None
        free_cash_flow = info.get('freeCashflow', 0)
        
        analysis['metrics'] = {
            'P/E Ratio': pe_ratio,
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
        
    elif sector == 'Industrial':
        # Industrial-specific metrics
        operating_margin = info.get('operatingMargins', 0) * 100 if info.get('operatingMargins') else None
        debt_to_equity = info.get('debtToEquity')
        
        analysis['metrics'] = {
            'P/E Ratio': pe_ratio,
            'Operating Margin': f"{operating_margin:.1f}%" if operating_margin else 'N/A',
            'Debt-to-Equity': f"{debt_to_equity:.2f}" if debt_to_equity else 'N/A'
        }
        
        score = 50
        if operating_margin and operating_margin > 12:
            analysis['strengths'].append(f"Strong operating margin of {operating_margin:.1f}% shows efficiency")
            score += 15
        elif operating_margin and operating_margin < 6:
            analysis['weaknesses'].append(f"Low operating margin of {operating_margin:.1f}%")
            score -= 10
        
        if debt_to_equity and debt_to_equity < 100:
            analysis['strengths'].append(f"Healthy D/E ratio of {debt_to_equity:.0f}% indicates manageable debt")
            score += 10
        elif debt_to_equity and debt_to_equity > 200:
            analysis['weaknesses'].append(f"High D/E ratio of {debt_to_equity:.0f}% raises leverage concerns")
            score -= 15
        
        analysis['rating'] = max(0, min(100, score))
        
    elif sector == 'Energy':
        # Energy-specific metrics
        pb_ratio = info.get('priceToBook')
        ebitda = info.get('ebitda', 0)
        debt_to_equity = info.get('debtToEquity')
        
        analysis['metrics'] = {
            'P/B Ratio': pb_ratio,
            'EBITDA': f"${ebitda/1e9:.2f}B" if ebitda else 'N/A',
            'Debt-to-Equity': f"{debt_to_equity:.2f}" if debt_to_equity else 'N/A'
        }
        
        score = 50
        if pb_ratio and pb_ratio < 1.5:
            analysis['strengths'].append(f"Attractive P/B of {pb_ratio:.2f} relative to asset base")
            score += 15
        
        if ebitda and ebitda > 0:
            analysis['strengths'].append("Positive EBITDA demonstrates operational profitability")
            score += 10
        
        if debt_to_equity and debt_to_equity < 80:
            analysis['strengths'].append("Conservative leverage supports commodity price volatility")
            score += 15
        elif debt_to_equity and debt_to_equity > 150:
            analysis['weaknesses'].append(f"High debt-to-equity of {debt_to_equity:.0f}% is risky in cyclical sector")
            score -= 15
        
        analysis['rating'] = max(0, min(100, score))
        
    elif sector == 'Consumer Cyclical':
        # Consumer cyclical metrics
        revenue_growth = info.get('revenueGrowth', 0) * 100 if info.get('revenueGrowth') else None
        gross_margin = info.get('grossMargins', 0) * 100 if info.get('grossMargins') else None
        
        analysis['metrics'] = {
            'P/E Ratio': pe_ratio,
            'Revenue Growth': f"{revenue_growth:.1f}%" if revenue_growth else 'N/A',
            'Gross Margin': f"{gross_margin:.1f}%" if gross_margin else 'N/A'
        }
        
        score = 50
        if revenue_growth and revenue_growth > 10:
            analysis['strengths'].append(f"Strong revenue growth of {revenue_growth:.1f}% indicates market share gains")
            score += 15
        
        if gross_margin and gross_margin > 35:
            analysis['strengths'].append(f"Solid gross margin of {gross_margin:.1f}% reflects pricing power")
            score += 10
        elif gross_margin and gross_margin < 20:
            analysis['weaknesses'].append(f"Thin gross margin of {gross_margin:.1f}% limits profitability")
            score -= 10
        
        analysis['rating'] = max(0, min(100, score))
        
    elif sector == 'Consumer Defensive':
        # Defensive consumer metrics
        dividend_yield = info.get('dividendYield', 0) * 100 if info.get('dividendYield') else None
        payout_ratio = info.get('payoutRatio', 0) * 100 if info.get('payoutRatio') else None
        operating_margin = info.get('operatingMargins', 0) * 100 if info.get('operatingMargins') else None
        
        analysis['metrics'] = {
            'P/E Ratio': pe_ratio,
            'Dividend Yield': f"{dividend_yield:.2f}%" if dividend_yield else 'N/A',
            'Payout Ratio': f"{payout_ratio:.1f}%" if payout_ratio else 'N/A',
            'Operating Margin': f"{operating_margin:.1f}%" if operating_margin else 'N/A'
        }
        
        score = 50
        if dividend_yield and dividend_yield > 2.5:
            analysis['strengths'].append(f"Attractive dividend yield of {dividend_yield:.2f}%")
            score += 15
        
        if payout_ratio and 40 < payout_ratio < 70:
            analysis['strengths'].append(f"Sustainable payout ratio of {payout_ratio:.0f}%")
            score += 10
        elif payout_ratio and payout_ratio > 90:
            analysis['weaknesses'].append(f"High payout ratio of {payout_ratio:.0f}% may be unsustainable")
            score -= 10
        
        if operating_margin and operating_margin > 15:
            analysis['strengths'].append("Strong operating margin demonstrates pricing resilience")
            score += 10
        
        analysis['rating'] = max(0, min(100, score))
        
    else:
        # Generic analysis for other sectors
        profit_margin = info.get('profitMargins', 0) * 100 if info.get('profitMargins') else None
        
        analysis['metrics'] = {
            'P/E Ratio': pe_ratio,
            'Profit Margin': f"{profit_margin:.1f}%" if profit_margin else 'N/A'
        }
        
        score = 50
        if profit_margin and profit_margin > 10:
            analysis['strengths'].append(f"Healthy profit margin of {profit_margin:.1f}%")
            score += 10
        
        analysis['rating'] = max(0, min(100, score))
    
    # Generate recommendation
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
    """Calculate a score from 0-100 based on stochastic signals"""
    score = 50  # Start neutral
    
    # Position scoring
    if k < 20:
        score += 20  # Oversold is good for buying
    elif k > 80:
        score -= 20  # Overbought is risky
    
    # Crossover scoring
    if k > d:
        score += 10  # Bullish alignment
    else:
        score -= 10  # Bearish alignment
    
    # Momentum scoring
    if momentum > 10:
        score += 15
    elif momentum > 0:
        score += 5
    elif momentum > -10:
        score -= 5
    else:
        score -= 15
    
    # Trend scoring
    if trend == "bullish":
        score += 5
    elif trend == "bearish":
        score -= 5
    
    return max(0, min(100, score))  # Clamp between 0-100

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
    
    # CRITICAL INVESTMENT ANALYSIS
    st.markdown("---")
    st.header("📊 CRITICAL INVESTMENT ANALYSIS")
    st.markdown("---")
    
    current_k = data['STOCH_K'].iloc[-1]
    current_d = data['STOCH_D'].iloc[-1]
    prev_k = data['STOCH_K'].iloc[-2]
    prev_d = data['STOCH_D'].iloc[-2]
    
    # Detect crossovers
    bullish_cross = (prev_k <= prev_d) and (current_k > current_d)
    bearish_cross = (prev_k >= prev_d) and (current_k < current_d)
    
    # Calculate momentum
    k_momentum = current_k - data['STOCH_K'].iloc[-5]
    
    # Determine trend strength
    recent_k = data['STOCH_K'].iloc[-10:]
    trend_direction = "bullish" if recent_k.is_monotonic_increasing else "bearish" if recent_k.is_monotonic_decreasing else "mixed"
    
    # Calculate stochastic score
    stoch_score = calculate_stochastic_score(current_k, current_d, k_momentum, trend_direction)
    
    # Get sector and fundamental analysis
    sector = get_sector_from_info(info)
    fundamental_analysis = analyze_fundamentals(info, sector)
    
    # Combined investment score (50% technical, 50% fundamental)
    combined_score = (stoch_score + fundamental_analysis['rating']) / 2
    
    # Add to portfolio button
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
    
    # MARKET POSITION
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
    
    st.markdown("---")
    
    # DUAL ANALYSIS FRAMEWORK
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
        
        # Trading strategies
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
        
        # EDUCATIONAL CONTEXT
        with st.expander("📚 Understanding the Stochastic Oscillator (Click to Expand)"):
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
    
    # CROSSOVER SIGNALS
    st.subheader("🔄 Crossover Signals (Most Critical)")
    
    if bullish_cross:
        st.success("**🚀 BULLISH CROSSOVER DETECTED - BUY SIGNAL**")
        st.write(f"""
        The fast line (%K = {current_k:.1f}) has just crossed ABOVE the slow line (%D = {current_d:.1f}). 
        This is a **buy signal** indicating potential upward momentum.
        
        **Signal Strength:** {'VERY STRONG' if current_k < 30 else 'STRONG' if current_k < 50 else 'MODERATE'}
        - Crossovers in oversold territory (<20) are most reliable
        - This crossover occurred at {current_k:.1f}, which is {'in oversold territory - excellent entry point' if current_k < 20 else 'in neutral territory - decent signal' if current_k < 80 else 'in overbought territory - late entry, be cautious'}
        
        **Recommended Action:** Consider initiating or adding to positions, but confirm with volume and price action.
        """)
        
    elif bearish_cross:
        st.error("**📉 BEARISH CROSSOVER DETECTED - SELL SIGNAL**")
        st.write(f"""
        The fast line (%K = {current_k:.1f}) has just crossed BELOW the slow line (%D = {current_d:.1f}). 
        This is a **sell signal** indicating potential downward momentum.
        
        **Signal Strength:** {'VERY STRONG' if current_k > 70 else 'STRONG' if current_k > 50 else 'MODERATE'}
        - Crossovers in overbought territory (>80) are most reliable
        - This crossover occurred at {current_k:.1f}, which is {'in overbought territory - strong sell signal' if current_k > 80 else 'in neutral territory - watch closely' if current_k > 20 else 'in oversold territory - may be oversold bounce ending'}
        
        **Recommended Action:** Consider taking profits, reducing position size, or exiting entirely if risk-averse.
        """)
        
    else:
        st.info("**No Recent Crossover Detected**")
        k_above = current_k > current_d
        st.write(f"""
        %K is currently {'ABOVE' if k_above else 'BELOW'} %D, suggesting {'bullish' if k_above else 'bearish'} momentum remains intact.
        
        **What to Watch For:**
        - {'A bearish crossover (%K crossing below %D) would signal weakening momentum' if k_above else 'A bullish crossover (%K crossing above %D) would signal strengthening momentum'}
        - Monitor the gap between %K and %D - narrowing suggests potential crossover coming
        - Current gap: {abs(current_k - current_d):.1f} points
        """)
    
    # MOMENTUM ANALYSIS
    st.subheader("📈 Momentum & Trend Analysis")
    
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
    
    # RISK ASSESSMENT
    st.subheader("⚡ Risk Assessment & Probability")
    
    # Calculate risk score
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
    
    # TRADING STRATEGY RECOMMENDATIONS
    st.subheader("💡 Strategic Recommendations")
    
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
    
    # EDUCATIONAL CONTEXT
    with st.expander("📚 Understanding the Stochastic Oscillator (Click to Expand)"):
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
    
    st.markdown("---")
    st.caption("⚠️ This analysis is for educational purposes only and does not constitute financial advice. Always conduct your own research and consult with a licensed financial advisor before making investment decisions.")

# PORTFOLIO PAGE
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
    
    # Summary metrics at the top
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
    
    # Alerts section
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
    
    # Filter and sort options
    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        filter_by = st.selectbox("Filter by Position", 
                                ["All Positions", "Oversold Only", "Overbought Only", "Neutral Only"],
                                index=0)
    with col2:
        sort_by = st.selectbox("Sort by", 
                              ["Ticker", "Position", "Momentum", "Stochastic Score", "Last Updated"],
                              index=3)
    with col3:
        sort_order = st.radio("Order", ["Ascending ↑", "Descending ↓"], horizontal=True, index=1)
    
    # Apply filters
    filtered_portfolio = st.session_state.portfolio.copy()
    
    if filter_by == "Oversold Only":
        filtered_portfolio = [s for s in filtered_portfolio if s['position'] == 'OVERSOLD']
    elif filter_by == "Overbought Only":
        filtered_portfolio = [s for s in filtered_portfolio if s['position'] == 'OVERBOUGHT']
    elif filter_by == "Neutral Only":
        filtered_portfolio = [s for s in filtered_portfolio if s['position'] == 'NEUTRAL']
    
    # Sort portfolio
    sort_key_map = {
        "Ticker": lambda x: x['ticker'],
        "Position": lambda x: x['position'],
        "Momentum": lambda x: x['momentum'],
        "Stochastic Score": lambda x: calculate_stochastic_score(x['stoch_k'], x['stoch_d'], x['momentum'], x['trend']),
        "Last Updated": lambda x: x['last_updated']
    }
    
    sorted_portfolio = sorted(filtered_portfolio, 
                             key=sort_key_map[sort_by],
                             reverse=(sort_order == "Descending ↓"))
    
    st.markdown("---")
    
    # Display portfolio stocks
    st.subheader(f"📈 Your Stocks ({len(sorted_portfolio)})")
    
    if not sorted_portfolio:
        st.info("No stocks match your current filter.")
    
    for i, stock in enumerate(sorted_portfolio):
        score = calculate_stochastic_score(stock['stoch_k'], stock['stoch_d'], 
                                          stock['momentum'], stock['trend'])
        
        # Determine position styling
        if stock['position'] == 'OVERSOLD':
            position_color = "#10b981"
            position_emoji = "🟢"
            position_badge = "OVERSOLD - BUY SIGNAL"
        elif stock['position'] == 'OVERBOUGHT':
            position_color = "#ef4444"
            position_emoji = "🔴"
            position_badge = "OVERBOUGHT - SELL SIGNAL"
        else:
            position_color = "#6b7280"
            position_emoji = "⚪"
            position_badge = "NEUTRAL"
        
        # Trend styling
        if stock['trend'] == 'bullish':
            trend_emoji = "📈"
            trend_color = "#10b981"
        elif stock['trend'] == 'bearish':
            trend_emoji = "📉"
            trend_color = "#ef4444"
        else:
            trend_emoji = "➡️"
            trend_color = "#6b7280"
        
        # Score styling
        if score >= 70:
            score_color = "#10b981"
            score_label = "Strong Buy"
        elif score >= 50:
            score_color = "#3b82f6"
            score_label = "Moderate Buy"
        elif score >= 30:
            score_color = "#f59e0b"
            score_label = "Hold"
        else:
            score_color = "#ef4444"
            score_label = "Consider Selling"
        
        # Momentum styling
        momentum_color = "#10b981" if stock['momentum'] > 0 else "#ef4444"
        momentum_direction = "↑" if stock['momentum'] > 0 else "↓"
        
        # Create expandable card for each stock
        with st.expander(f"{position_emoji} **{stock['ticker']}** - {position_badge} | Score: {score}/100", expanded=False):
            # Main metrics row
            metric_col1, metric_col2, metric_col3, metric_col4, metric_col5 = st.columns(5)
            
            with metric_col1:
                st.metric("Stochastic %K", f"{stock['stoch_k']:.1f}")
            with metric_col2:
                st.metric("Stochastic %D", f"{stock['stoch_d']:.1f}")
            with metric_col3:
                st.metric("5-Day Momentum", f"{stock['momentum']:+.1f}", 
                         delta_color="normal" if stock['momentum'] > 0 else "inverse")
            with metric_col4:
                st.metric("10-Day Trend", f"{stock['trend'].title()}")
            with metric_col5:
                st.metric("Signal Score", f"{score}/100")
            
            # Signal interpretation
            st.markdown("**Signal Interpretation:**")
            
            if stock['position'] == 'OVERSOLD':
                st.success(f"✅ {stock['ticker']} is oversold and may be a good buying opportunity. The stock has experienced significant selling pressure.")
            elif stock['position'] == 'OVERBOUGHT':
                st.warning(f"⚠️ {stock['ticker']} is overbought and may be due for a pullback. Consider taking profits or waiting for a better entry.")
            else:
                st.info(f"ℹ️ {stock['ticker']} is in a neutral range. Wait for clearer signals before making trading decisions.")
            
            # Crossover status
            if stock['stoch_k'] > stock['stoch_d']:
                st.write(f"📊 **Crossover Status:** %K is above %D (Bullish alignment)")
            else:
                st.write(f"📊 **Crossover Status:** %K is below %D (Bearish alignment)")
            
            # Action buttons row
            btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)
            
            with btn_col1:
                if st.button(f"📊 Analyze", key=f"analyze_{stock['ticker']}", use_container_width=True):
                    st.session_state.page = 'analysis'
                    st.session_state.selected_ticker = stock['ticker']
                    st.rerun()
            
            with btn_col2:
                if st.button(f"🔄 Refresh Data", key=f"refresh_{stock['ticker']}", use_container_width=True):
                    with st.spinner(f"Updating {stock['ticker']}..."):
                        data, info, error = get_stock_data(stock['ticker'], "1mo")
                        if data is not None and not data.empty:
                            k_period = 14
                            d_period = 3
                            data['STOCH_K'], data['STOCH_D'] = calculate_stochastic(
                                data['High'], data['Low'], data['Close'], k_period, d_period
                            )
                            current_k = data['STOCH_K'].iloc[-1]
                            current_d = data['STOCH_D'].iloc[-1]
                            k_momentum = current_k - data['STOCH_K'].iloc[-5]
                            recent_k = data['STOCH_K'].iloc[-10:]
                            trend = "bullish" if recent_k.is_monotonic_increasing else "bearish" if recent_k.is_monotonic_decreasing else "mixed"
                            
                            add_to_portfolio(stock['ticker'], current_k, current_d, k_momentum, trend)
                            st.success(f"✅ {stock['ticker']} updated!")
                            st.rerun()
            
            with btn_col3:
                st.caption(f"Last Updated: {stock['last_updated']}")
            
            with btn_col4:
                if st.button(f"🗑️ Remove", key=f"remove_{stock['ticker']}", use_container_width=True):
                    remove_from_portfolio(stock['ticker'])
                    st.success(f"Removed {stock['ticker']}")
                    st.rerun()
    
    st.markdown("---")
    
    # Bulk actions section
    st.subheader("⚙️ Bulk Actions")
    
    bulk_col1, bulk_col2, bulk_col3 = st.columns(3)
    
    with bulk_col1:
        if st.button("🔄 Refresh All Stocks", use_container_width=True, type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for idx, stock in enumerate(st.session_state.portfolio):
                status_text.text(f"Updating {stock['ticker']}... ({idx + 1}/{len(st.session_state.portfolio)})")
                
                data, info, error = get_stock_data(stock['ticker'], "1mo")
                if data is not None and not data.empty:
                    k_period = 14
                    d_period = 3
                    data['STOCH_K'], data['STOCH_D'] = calculate_stochastic(
                        data['High'], data['Low'], data['Close'], k_period, d_period
                    )
                    current_k = data['STOCH_K'].iloc[-1]
                    current_d = data['STOCH_D'].iloc[-1]
                    k_momentum = current_k - data['STOCH_K'].iloc[-5]
                    recent_k = data['STOCH_K'].iloc[-10:]
                    trend = "bullish" if recent_k.is_monotonic_increasing else "bearish" if recent_k.is_monotonic_decreasing else "mixed"
                    add_to_portfolio(stock['ticker'], current_k, current_d, k_momentum, trend)
                
                progress_bar.progress((idx + 1) / len(st.session_state.portfolio))
            
            status_text.text("✅ All stocks updated!")
            st.success(f"Successfully updated {len(st.session_state.portfolio)} stocks!")
            st.rerun()
    
    with bulk_col2:
        portfolio_df = pd.DataFrame(st.session_state.portfolio)
        
        # Add calculated score column
        portfolio_df['score'] = portfolio_df.apply(
            lambda row: calculate_stochastic_score(row['stoch_k'], row['stoch_d'], 
                                                   row['momentum'], row['trend']), 
            axis=1
        )
        
        csv = portfolio_df.to_csv(index=False)
        st.download_button(
            label="📥 Export to CSV",
            data=csv,
            file_name=f"barbas_portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with bulk_col3:
        if st.button("🗑️ Clear Portfolio", use_container_width=True, type="secondary"):
            if st.session_state.get('confirm_clear', False):
                st.session_state.portfolio = []
                st.session_state.confirm_clear = False
                st.success("Portfolio cleared!")
                st.rerun()
            else:
                st.session_state.confirm_clear = True
                st.warning("⚠️ Click again to confirm")
    
    # Portfolio statistics
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

# DISCOVER STOCKS PAGE
elif st.session_state.page == 'discover':
    st.title("🔍 Discover Prospective Stocks")
    st.markdown("Explore curated stock opportunities based on stochastic oscillator analysis")
    
    # Sector selection
    st.subheader("📂 Select Sector to Analyze")
    
    stock_categories = get_prospective_stocks()
    
    col1, col2 = st.columns([3, 2])
    with col1:
        selected_sector = st.selectbox(
            "Choose a sector",
            list(stock_categories.keys()),
            index=0
        )
    with col2:
        analysis_period = st.selectbox(
            "Analysis Period",
            ["1mo", "3mo", "6mo"],
            index=0
        )
    
    st.markdown(f"**Analyzing {len(stock_categories[selected_sector])} stocks in {selected_sector}**")
    
    if st.button(f"🔍 Analyze {selected_sector} Sector", use_container_width=True, type="primary"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        debug_info = st.empty()
        
        tickers = stock_categories[selected_sector]
        results = []
        failed_tickers = []
        error_messages = []
        
        for idx, ticker in enumerate(tickers):
            status_text.text(f"Analyzing {ticker}... ({idx + 1}/{len(tickers)})")
            progress_bar.progress((idx + 1) / len(tickers))
            
            try:
                # Add small delay to avoid rate limiting
                if idx > 0:
                    time.sleep(0.8)
                
                # Fetch data directly without cache for discovery
                stock = yf.Ticker(ticker)
                data = stock.history(period=analysis_period)
                
                debug_info.text(f"Debug: {ticker} returned {len(data) if data is not None and not data.empty else 0} rows")
                
                if data is None or data.empty:
                    failed_tickers.append(ticker)
                    error_messages.append(f"{ticker}: No data returned")
                    continue
                
                if len(data) < 14:
                    failed_tickers.append(ticker)
                    error_messages.append(f"{ticker}: Only {len(data)} days of data (need 14+)")
                    continue
                
                info = stock.info
                
                k_period = 14
                d_period = 3
                
                # Calculate stochastic
                lowest_low = data['Low'].rolling(window=k_period).min()
                highest_high = data['High'].rolling(window=k_period).max()
                k_percent = ((data['Close'] - lowest_low) / (highest_high - lowest_low)) * 100
                d_percent = k_percent.rolling(window=d_period).mean()
                
                data['STOCH_K'] = k_percent
                data['STOCH_D'] = d_percent
                
                current_k = data['STOCH_K'].iloc[-1]
                current_d = data['STOCH_D'].iloc[-1]
                
                if pd.isna(current_k) or pd.isna(current_d):
                    failed_tickers.append(ticker)
                    error_messages.append(f"{ticker}: Stochastic calculation resulted in NaN")
                    continue
                
                k_momentum = current_k - data['STOCH_K'].iloc[-5] if len(data) >= 5 else 0
                recent_k = data['STOCH_K'].iloc[-10:] if len(data) >= 10 else data['STOCH_K']
                trend = "bullish" if recent_k.is_monotonic_increasing else "bearish" if recent_k.is_monotonic_decreasing else "mixed"
                
                price = data['Close'].iloc[-1]
                change = ((data['Close'].iloc[-1] / data['Close'].iloc[0]) - 1) * 100 if len(data) > 0 else 0
                
                position = "OVERSOLD" if current_k < 20 else "OVERBOUGHT" if current_k > 80 else "NEUTRAL"
                score = calculate_stochastic_score(current_k, current_d, k_momentum, trend)
                
                # Detect crossovers
                if len(data) >= 2:
                    prev_k = data['STOCH_K'].iloc[-2]
                    prev_d = data['STOCH_D'].iloc[-2]
                    if pd.isna(prev_k) or pd.isna(prev_d):
                        bullish_cross = False
                        bearish_cross = False
                    else:
                        bullish_cross = (prev_k <= prev_d) and (current_k > current_d)
                        bearish_cross = (prev_k >= prev_d) and (current_k < current_d)
                else:
                    bullish_cross = False
                    bearish_cross = False
                
                results.append({
                    'ticker': ticker,
                    'name': info.get('longName', ticker) if info else ticker,
                    'price': price,
                    'change': change,
                    'stoch_k': current_k,
                    'stoch_d': current_d,
                    'momentum': k_momentum,
                    'trend': trend,
                    'position': position,
                    'score': score,
                    'bullish_cross': bullish_cross,
                    'bearish_cross': bearish_cross,
                    'volume': data['Volume'].iloc[-1] if 'Volume' in data.columns else 0
                })
                
                error_messages.append(f"{ticker}: ✓ Success")
                
            except Exception as e:
                failed_tickers.append(ticker)
                error_messages.append(f"{ticker}: Error - {str(e)}")
                continue
        
        progress_bar.empty()
        status_text.empty()
        debug_info.empty()
        
        # Show detailed error log
        with st.expander("📋 View Detailed Analysis Log"):
            for msg in error_messages:
                st.text(msg)
        
        if results:
            st.session_state.discovery_results = results
            st.session_state.discovery_sector = selected_sector
            
            if failed_tickers:
                st.warning(f"⚠️ Analyzed {len(results)} out of {len(tickers)} stocks successfully. Failed: {', '.join(failed_tickers)}")
            else:
                st.success(f"✅ Successfully analyzed all {len(results)} stocks in {selected_sector}!")
            st.rerun()
        else:
            st.error(f"❌ Unable to fetch data for any stocks in {selected_sector}.")
            st.write("**Possible reasons:**")
            st.write("- 🚫 Yahoo Finance API is rate limiting your requests")
            st.write("- 🌐 Network connectivity issues")
            st.write("- ❌ All ticker symbols are invalid or delisted")
            st.write("- 📊 No data available for the selected time period")
            st.info("💡 **Try this:** Wait 2-3 minutes and try a different sector, or try the 'Tech Giants' sector which usually has reliable data.")
    
    # Display results if they exist
    if 'discovery_results' in st.session_state and st.session_state.discovery_results:
        results = st.session_state.discovery_results
        sector = st.session_state.get('discovery_sector', 'Selected Sector')
        
        st.markdown("---")
        
        # Summary statistics
        st.subheader(f"📊 {sector} Sector Overview")
        
        oversold_count = sum(1 for r in results if r['position'] == 'OVERSOLD')
        overbought_count = sum(1 for r in results if r['position'] == 'OVERBOUGHT')
        neutral_count = sum(1 for r in results if r['position'] == 'NEUTRAL')
        bullish_cross_count = sum(1 for r in results if r['bullish_cross'])
        bearish_cross_count = sum(1 for r in results if r['bearish_cross'])
        
        avg_score = sum(r['score'] for r in results) / len(results)
        avg_momentum = sum(r['momentum'] for r in results) / len(results)
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        col1.metric("Stocks Analyzed", len(results))
        col2.metric("Oversold 🟢", oversold_count)
        col3.metric("Overbought 🔴", overbought_count)
        col4.metric("Bullish Crosses", bullish_cross_count)
        col5.metric("Avg Score", f"{avg_score:.0f}/100")
        col6.metric("Avg Momentum", f"{avg_momentum:+.1f}")
        
        st.markdown("---")
        
        # Filters and sorting
        st.subheader("🎯 Filter & Sort Results")
        
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        
        with filter_col1:
            position_filter = st.multiselect(
                "Filter by Position",
                ["OVERSOLD", "NEUTRAL", "OVERBOUGHT"],
                default=["OVERSOLD", "NEUTRAL", "OVERBOUGHT"]
            )
        
        with filter_col2:
            signal_filter = st.selectbox(
                "Signal Filter",
                ["All Signals", "Bullish Crosses Only", "Bearish Crosses Only", "No Recent Crosses"],
                index=0
            )
        
        with filter_col3:
            sort_by_discover = st.selectbox(
                "Sort by",
                ["Score (High to Low)", "Score (Low to High)", "Momentum", "Position", "Price Change"],
                index=0
            )
        
        # Apply filters
        filtered_results = [r for r in results if r['position'] in position_filter]
        
        if signal_filter == "Bullish Crosses Only":
            filtered_results = [r for r in filtered_results if r['bullish_cross']]
        elif signal_filter == "Bearish Crosses Only":
            filtered_results = [r for r in filtered_results if r['bearish_cross']]
        elif signal_filter == "No Recent Crosses":
            filtered_results = [r for r in filtered_results if not r['bullish_cross'] and not r['bearish_cross']]
        
        # Sort results
        if sort_by_discover == "Score (High to Low)":
            filtered_results = sorted(filtered_results, key=lambda x: x['score'], reverse=True)
        elif sort_by_discover == "Score (Low to High)":
            filtered_results = sorted(filtered_results, key=lambda x: x['score'])
        elif sort_by_discover == "Momentum":
            filtered_results = sorted(filtered_results, key=lambda x: x['momentum'], reverse=True)
        elif sort_by_discover == "Position":
            filtered_results = sorted(filtered_results, key=lambda x: x['position'])
        elif sort_by_discover == "Price Change":
            filtered_results = sorted(filtered_results, key=lambda x: x['change'], reverse=True)
        
        st.markdown("---")
        
        # TOP OPPORTUNITIES - REVISED TO SHOW TOP 3 BY SCORE
        st.success("🌟 **TOP 3 OPPORTUNITIES IN THIS SECTOR**")
        st.write("Ranked by highest stochastic score and momentum - these are the strongest signals in the sector!")
        
        # Sort by score first, then by momentum as tiebreaker
        top_opportunities = sorted(filtered_results, key=lambda x: (x['score'], x['momentum']), reverse=True)[:3]
        
        if top_opportunities:
            rank_emojis = ["🥇", "🥈", "🥉"]
            
            for idx, stock in enumerate(top_opportunities):
                # Determine recommendation strength
                if stock['score'] >= 70:
                    strength = "STRONG BUY"
                    strength_color = "#10b981"
                elif stock['score'] >= 60:
                    strength = "BUY"
                    strength_color = "#3b82f6"
                elif stock['score'] >= 50:
                    strength = "MODERATE BUY"
                    strength_color = "#f59e0b"
                elif stock['score'] >= 40:
                    strength = "HOLD"
                    strength_color = "#6b7280"
                else:
                    strength = "AVOID"
                    strength_color = "#ef4444"
                
                with st.expander(f"{rank_emojis[idx]} **#{idx+1} - {stock['ticker']}** ({stock['name']}) | Score: **{stock['score']}/100** | {strength}", expanded=True):
                    # Key metrics
                    met_col1, met_col2, met_col3, met_col4, met_col5 = st.columns(5)
                    met_col1.metric("Price", f"${stock['price']:.2f}", f"{stock['change']:+.2f}%")
                    met_col2.metric("Position", stock['position'])
                    met_col3.metric("Stochastic %K", f"{stock['stoch_k']:.1f}")
                    met_col4.metric("Momentum", f"{stock['momentum']:+.1f}")
                    met_col5.metric("Trend", stock['trend'].title())
                    
                    # Why this stock ranked
                    st.markdown(f"**Why #{idx+1}:**")
                    reasons = []
                    
                    if stock['score'] >= 70:
                        reasons.append(f"✅ **Exceptional Score ({stock['score']}/100)** - Among the highest in the sector")
                    elif stock['score'] >= 60:
                        reasons.append(f"✅ **Strong Score ({stock['score']}/100)** - Above average signals")
                    elif stock['score'] >= 50:
                        reasons.append(f"⚠️ **Moderate Score ({stock['score']}/100)** - Decent but not exceptional")
                    else:
                        reasons.append(f"⚠️ **Below Average Score ({stock['score']}/100)** - Weak signals currently")
                    
                    if stock['position'] == 'OVERSOLD':
                        reasons.append("✅ **Oversold Position** - Potential buying opportunity, stock may be undervalued")
                    elif stock['position'] == 'OVERBOUGHT':
                        reasons.append("⚠️ **Overbought Position** - Stock may be overextended, caution advised")
                    else:
                        reasons.append("ℹ️ **Neutral Position** - No extreme technical signals")
                    
                    if stock['momentum'] > 10:
                        reasons.append(f"✅ **Strong Positive Momentum (+{stock['momentum']:.1f})** - Accelerating upward")
                    elif stock['momentum'] > 0:
                        reasons.append(f"✅ **Positive Momentum (+{stock['momentum']:.1f})** - Moving in right direction")
                    elif stock['momentum'] > -10:
                        reasons.append(f"⚠️ **Slight Negative Momentum ({stock['momentum']:.1f})** - Minor weakness")
                    else:
                        reasons.append(f"⚠️ **Strong Negative Momentum ({stock['momentum']:.1f})** - Downward pressure")
                    
                    if stock['trend'] == 'bullish':
                        reasons.append("✅ **Bullish Trend** - Consistently rising over 10 days")
                    elif stock['trend'] == 'bearish':
                        reasons.append("⚠️ **Bearish Trend** - Consistently falling over 10 days")
                    else:
                        reasons.append("ℹ️ **Mixed Trend** - Choppy price action")
                    
                    if stock['bullish_cross']:
                        reasons.append("🚀 **BULLISH CROSSOVER DETECTED** - %K crossed above %D (buy signal!)")
                    
                    if stock['bearish_cross']:
                        reasons.append("📉 **Bearish Crossover Detected** - %K crossed below %D (sell signal)")
                    
                    for reason in reasons:
                        st.markdown(f"- {reason}")
                    
                    # Investment recommendation
                    st.markdown(f"**Investment Recommendation:**")
                    
                    if stock['score'] >= 70 and stock['position'] == 'OVERSOLD':
                        st.success(f"🎯 **STRONG BUY CANDIDATE** - {stock['ticker']} shows exceptional technical strength with oversold positioning. This is one of the best opportunities in the {sector} sector right now. Consider initiating or adding to positions.")
                    elif stock['score'] >= 60 and stock['position'] == 'OVERSOLD':
                        st.success(f"✅ **BUY CANDIDATE** - {stock['ticker']} has strong signals and is oversold. Good risk/reward setup for entry.")
                    elif stock['score'] >= 60:
                        st.info(f"📊 **SOLID CHOICE** - {stock['ticker']} has good technical signals. Consider for watchlist or opportunistic entry on dips.")
                    elif stock['score'] >= 50:
                        st.info(f"⚖️ **MODERATE OPPORTUNITY** - {stock['ticker']} shows decent signals but lacks strong conviction. Better opportunities may exist.")
                    elif stock['position'] == 'OVERBOUGHT':
                        st.warning(f"⏸️ **WAIT FOR PULLBACK** - {stock['ticker']} is overbought. Consider waiting for better entry point or taking profits if you own it.")
                    else:
                        st.warning(f"⏳ **HOLD/WAIT** - {stock['ticker']} lacks strong technical signals currently. Monitor for better setup.")
                    
                    # Action buttons
                    btn_col1, btn_col2 = st.columns(2)
                    with btn_col1:
                        if st.button(f"📊 Full Deep-Dive Analysis", key=f"analyze_top_{stock['ticker']}", use_container_width=True, type="primary"):
                            st.session_state.page = 'analysis'
                            st.session_state.selected_ticker = stock['ticker']
                            st.rerun()
                    with btn_col2:
                        is_in_portfolio = any(s['ticker'] == stock['ticker'] for s in st.session_state.portfolio)
                        if not is_in_portfolio:
                            if st.button(f"⭐ Add to Portfolio", key=f"add_top_{stock['ticker']}", use_container_width=True):
                                add_to_portfolio(stock['ticker'], stock['stoch_k'], stock['stoch_d'], 
                                               stock['momentum'], stock['trend'])
                                st.success(f"Added {stock['ticker']} to your portfolio!")
                                st.rerun()
                        else:
                            st.success("✓ Already in Portfolio")
        else:
            st.info("No stocks available in this filter. Try adjusting your criteria.")
        
        st.markdown("---")
        
        # ALL RESULTS
        st.subheader(f"📋 All Results ({len(filtered_results)} stocks)")
        
        if not filtered_results:
            st.info("No stocks match your current filters. Try adjusting the filters above.")
        
        for stock in filtered_results:
            # Position styling
            if stock['position'] == 'OVERSOLD':
                position_emoji = "🟢"
                position_style = "background-color: #d1fae5; padding: 10px; border-radius: 8px; border-left: 4px solid #10b981;"
            elif stock['position'] == 'OVERBOUGHT':
                position_emoji = "🔴"
                position_style = "background-color: #fee2e2; padding: 10px; border-radius: 8px; border-left: 4px solid #ef4444;"
            else:
                position_emoji = "⚪"
                position_style = "background-color: #f3f4f6; padding: 10px; border-radius: 8px; border-left: 4px solid #6b7280;"
            
            # Trend emoji
            trend_emoji = "📈" if stock['trend'] == 'bullish' else "📉" if stock['trend'] == 'bearish' else "➡️"
            
            # Signal badge
            signal_badge = ""
            if stock['bullish_cross']:
                signal_badge = "🚀 BULLISH CROSS"
            elif stock['bearish_cross']:
                signal_badge = "📉 BEARISH CROSS"
            
            with st.container():
                st.markdown(f"<div style='{position_style}'>", unsafe_allow_html=True)
                
                header_col1, header_col2 = st.columns([3, 1])
                with header_col1:
                    st.markdown(f"### {position_emoji} {stock['ticker']} - {stock['name']}")
                    if signal_badge:
                        st.markdown(f"**{signal_badge}**")
                with header_col2:
                    st.metric("Score", f"{stock['score']}/100")
                
                metric_col1, metric_col2, metric_col3, metric_col4, metric_col5 = st.columns(5)
                metric_col1.metric("Price", f"${stock['price']:.2f}", f"{stock['change']:+.2f}%")
                metric_col2.metric("Position", stock['position'])
                metric_col3.metric("%K", f"{stock['stoch_k']:.1f}")
                metric_col4.metric("Momentum", f"{stock['momentum']:+.1f}")
                metric_col5.metric("Trend", f"{trend_emoji} {stock['trend'].title()}")
                
                # Analysis text
                if stock['position'] == 'OVERSOLD':
                    st.info(f"💡 **Potential Buy:** {stock['ticker']} is oversold. Consider adding to watchlist or initiating a position.")
                elif stock['position'] == 'OVERBOUGHT':
                    st.warning(f"⚠️ **Caution:** {stock['ticker']} is overbought. May be due for a pullback.")
                else:
                    st.write(f"ℹ️ {stock['ticker']} is in neutral territory. Wait for clearer signals.")
                
                # Action buttons
                action_col1, action_col2 = st.columns(2)
                with action_col1:
                    if st.button(f"📊 Full Analysis", key=f"analyze_{stock['ticker']}", use_container_width=True):
                        st.session_state.page = 'analysis'
                        st.session_state.selected_ticker = stock['ticker']
                        st.rerun()
                
                with action_col2:
                    is_in_portfolio = any(s['ticker'] == stock['ticker'] for s in st.session_state.portfolio)
                    if not is_in_portfolio:
                        if st.button(f"⭐ Add to Portfolio", key=f"add_{stock['ticker']}", use_container_width=True):
                            add_to_portfolio(stock['ticker'], stock['stoch_k'], stock['stoch_d'], 
                                           stock['momentum'], stock['trend'])
                            st.success(f"Added {stock['ticker']} to portfolio!")
                            st.rerun()
                    else:
                        st.success("✓ Already in Portfolio")
                
                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("")  # spacing
        
        # Bulk add to portfolio
        if filtered_results:
            st.markdown("---")
            st.subheader("⚡ Bulk Actions")
            
            if st.button(f"⭐ Add All {len(filtered_results)} Filtered Stocks to Portfolio", 
                        use_container_width=True, type="secondary"):
                added_count = 0
                for stock in filtered_results:
                    if not any(s['ticker'] == stock['ticker'] for s in st.session_state.portfolio):
                        add_to_portfolio(stock['ticker'], stock['stoch_k'], stock['stoch_d'], 
                                       stock['momentum'], stock['trend'])
                        added_count += 1
                
                if added_count > 0:
                    st.success(f"✅ Added {added_count} new stocks to your portfolio!")
                    st.rerun()
                else:
                    st.info("All filtered stocks are already in your portfolio.")
    
    # Educational section
    st.markdown("---")
    with st.expander("💡 How to Use the Discovery Page"):
        st.write("""
        **The Discovery Page helps you find trading opportunities across different sectors:**
        
        1. **Select a Sector** - Choose from Tech Giants, Finance, Healthcare, Consumer, Energy, Telecom, Industrial, or Crypto/Fintech
        
        2. **Click Analyze** - The system will scan all stocks in that sector using stochastic oscillator analysis
        
        3. **Review Top Opportunities** - Stocks with high scores and oversold positions appear first as potential buying opportunities
        
        4. **Filter Results** - Narrow down stocks by position (oversold/overbought), signals, or sort by various metrics
        
        5. **Take Action** - Click "Full Analysis" for detailed charts and signals, or "Add to Portfolio" to track the stock
        
        **What to Look For:**
        - 🟢 **Oversold stocks with high scores (60+)** = Best buying opportunities
        - 🚀 **Bullish crossovers in oversold territory** = Strong buy signals
        - 📈 **Positive momentum + bullish trend** = Confirmation of upward movement
        
        **Remember:** Use this as a screening tool. Always perform full analysis before investing!
        """)
