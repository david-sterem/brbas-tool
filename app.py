momentum_details.append(f"Normal volume activity at **{(volume_ratio * 100):.0f}%** of average. Current volume confirms the price movement but doesn't indicate exceptional institutional interest.")
    
    return momentum_score, momentum_details

def analyze_earnings(info):
    earnings_score = 0
    earnings_details = []
    
    earnings_growth = info.get('earningsQuarterlyGrowth', None)
    revenue_growth = info.get('revenueGrowth', None)
    profit_margin = info.get('profitMargins', None)
    roe = info.get('returnOnEquity', None)
    
    # Earnings growth analysis
    if earnings_growth is not None:
        if earnings_growth > 0.15:
            earnings_score += 2
            earnings_details.append(f"Exceptional quarterly earnings growth of **{earnings_growth*100:.1f}%** significantly exceeds market averages (typically 5-10%). This demonstrates strong operational performance, pricing power, and market share gains. Such growth rates are sustainable only with strong competitive advantages.")
        elif earnings_growth > 0.05:
            earnings_score += 1
            earnings_details.append(f"Solid earnings growth of **{earnings_growth*100:.1f}%** indicates healthy business expansion. While not exceptional, this positive trajectory suggests the company is successfully growing profits and managing costs effectively.")
        elif earnings_growth > 0:
            earnings_details.append(f"Modest earnings growth of **{earnings_growth*100:.1f}%** shows the company is expanding, though at a slower pace than market leaders. This moderate growth may indicate a maturing business or competitive pressures.")
        elif earnings_growth > -0.10:
            earnings_score -= 1
            earnings_details.append(f"Slight earnings decline of **{earnings_growth*100:.1f}%** raises concerns. While temporary setbacks occur, consistent negative growth suggests operational challenges, margin compression, or market headwinds that management must address.")
        else:
            earnings_score -= 2
            earnings_details.append(f"Significant earnings decline of **{earnings_growth*100:.1f}%** is a major red flag. This substantial contraction indicates serious operational problems, loss of market share, or fundamental business model challenges requiring immediate strategic intervention.")
    else:
        earnings_details.append("Quarterly earnings growth data unavailable. This metric is critical for assessing business momentum and is one of the primary drivers of stock price appreciation over time.")
    
    # Revenue growth
    if revenue_growth is not None:
        if revenue_growth > 0.20:
            earnings_score += 1
            earnings_details.append(f"Outstanding revenue growth of **{revenue_growth*100:.1f}%** indicates exceptional market demand and strong competitive positioning. Top-line growth at this rate typically reflects successful product launches, market expansion, or disruptive innovation.")
        elif revenue_growth > 0.10:
            earnings_details.append(f"Healthy revenue growth of **{revenue_growth*100:.1f}%** shows the company is successfully capturing market share and expanding its customer base. Double-digit revenue growth is a positive indicator of business health.")
        elif revenue_growth > 0:
            earnings_details.append(f"Moderate revenue growth of **{revenue_growth*100:.1f}%** indicates steady business expansion, though the company may be facing increased competition or market saturation limiting faster growth.")
        else:
            earnings_score -= 1
            earnings_details.append(f"Revenue decline of **{revenue_growth*100:.1f}%** is concerning. Shrinking top-line revenue suggests loss of customers, market share, or relevance. Even if profits are maintained, revenue contraction limits future growth potential.")
    else:
        earnings_details.append("Revenue growth data unavailable. Top-line growth is essential for long-term business sustainability and is often more important than short-term profit fluctuations.")
    
    # Profitability metrics
    if profit_margin is not None:
        if profit_margin > 0.20:
            earnings_details.append(f"Exceptional profit margin of **{profit_margin*100:.1f}%** demonstrates strong pricing power, operational efficiency, and competitive moat. Companies with margins above 20% typically have sustainable competitive advantages.")
        elif profit_margin > 0.10:
            earnings_details.append(f"Solid profit margin of **{profit_margin*100:.1f}%** indicates effective cost management and decent pricing power. This is respectable for most industries and suggests a viable business model.")
        elif profit_margin > 0:
            earnings_details.append(f"Thin profit margin of **{profit_margin*100:.1f}%** suggests low pricing power and tight cost controls. The company has limited buffer for economic downturns or unexpected expenses.")
        else:
            earnings_details.append(f"Negative profit margin of **{profit_margin*100:.1f}%** means the company is losing money on operations. This is only acceptable for early-stage growth companies investing heavily for future returns.")
    else:
        earnings_details.append("Profit margin data unavailable. This metric reveals how efficiently the company converts revenue into profit and indicates pricing power and operational excellence.")
    
    # Return on Equity
    if roe is not None:
        if roe > 0.15:
            earnings_details.append(f"Strong return on equity of **{roe*100:.1f}%** shows the company generates excellent returns on shareholder capital. ROE above 15% typically indicates a high-quality business with strong competitive advantages.")
        elif roe > 0:
            earnings_details.append(f"Moderate return on equity of **{roe*100:.1f}%** indicates the company generates positive but unremarkable returns on equity. There may be opportunities to improve capital efficiency.")
        else:
            earnings_details.append(f"Negative return on equity of **{roe*100:.1f}%** shows the company is destroying shareholder value. This is a critical issue requiring immediate management attention.")
    else:
        earnings_details.append("Return on equity data unavailable. ROE measures how effectively the company uses shareholder capital and is a key indicator of management quality.")
    
    return earnings_score, earnings_details

def analyze_technical(data):
    technical_score = 0
    technical_details = []
    
    current_rsi = data['RSI'].iloc[-1] if 'RSI' in data.columns and pd.notna(data['RSI'].iloc[-1]) else None
    current_macd = data['MACD'].iloc[-1] if 'MACD' in data.columns and pd.notna(data['MACD'].iloc[-1]) else None
    current_signal = data['Signal'].iloc[-1] if 'Signal' in data.columns and pd.notna(data['Signal'].iloc[-1]) else None
    
    # RSI Analysis
    if current_rsi is not None:
        if current_rsi < 30:
            technical_score += 2
            technical_details.append(f"RSI at **{current_rsi:.1f}** indicates oversold conditions. Historically, RSI readings below 30 precede price reversals as selling pressure becomes exhausted. This often represents a tactical buying opportunity, though further downside is possible before reversal occurs.")
        elif current_rsi > 70:
            technical_score -= 2
            technical_details.append(f"RSI at **{current_rsi:.1f}** signals overbought conditions. When RSI exceeds 70, stocks typically experience pullbacks or consolidation as buyers become exhausted. Consider taking profits or waiting for healthier entry points.")
        elif 45 < current_rsi < 55:
            technical_details.append(f"RSI at **{current_rsi:.1f}** is neutral, indicating balanced buying and selling pressure. The stock is neither overextended nor oversold, suggesting a consolidation phase with no immediate directional catalyst.")
        elif current_rsi < 45:
            technical_details.append(f"RSI at **{current_rsi:.1f}** shows mild bearish pressure. While not oversold, the indicator suggests sellers have slight control. Watch for a break below 30 for stronger oversold signals.")
        else:
            technical_details.append(f"RSI at **{current_rsi:.1f}** shows mild bullish pressure. The indicator suggests buyers have slight control but momentum isn't extreme. Watch for continuation above 70 or reversal below 50.")
    else:
        technical_details.append("RSI data unavailable. The Relative Strength Index measures momentum on a 0-100 scale and identifies overbought/oversold conditions that often precede price reversals.")
    
    # MACD Analysis
    if current_macd is not None and current_signal is not None:
        macd_diff = current_macd - current_signal
        if current_macd > current_signal:
            if macd_diff > 0.5:
                technical_score += 1
                technical_details.append(f"MACD strongly bullish at **{current_macd:.2f}** (signal: **{current_signal:.2f}**). The MACD line is significantly above the signal line, indicating strong upward momentum. This configuration typically persists until trend exhaustion.")
            else:
                technical_details.append(f"MACD mildly bullish at **{current_macd:.2f}** (signal: **{current_signal:.2f}**). The MACD is above the signal line but the margin is narrow, suggesting early-stage or weakening bullish momentum.")
        else:
            if macd_diff < -0.5:
                technical_score -= 1
                technical_details.append(f"MACD strongly bearish at **{current_macd:.2f}** (signal: **{current_signal:.2f}**). The MACD line is significantly below the signal line, indicating strong downward momentum. This suggests continued selling pressure.")
            else:
                technical_details.append(f"MACD mildly bearish at **{current_macd:.2f}** (signal: **{current_signal:.2f}**). The MACD is below the signal line but the margin is narrow, suggesting early-stage bearish momentum or potential reversal ahead.")
    else:
        technical_details.append("MACD data unavailable. The Moving Average Convergence Divergence indicator identifies trend changes and momentum shifts, making it valuable for timing entries and exits.")
    
    # Volatility assessment
    daily_returns = data['Close'].pct_change()
    volatility = daily_returns.std() * 100
    
    if volatility > 3:
        technical_details.append(f"High volatility of **{volatility:.2f}%** daily indicates significant price swings. This creates both opportunity and risk, requiring careful position sizing and stop-loss management. High volatility often occurs during trend changes or news events.")
    elif volatility < 1:
        technical_details.append(f"Low volatility of **{volatility:.2f}%** daily suggests stable, range-bound trading. Low volatility often precedes significant moves as markets tend to alternate between calm and volatile periods. Be prepared for eventual volatility expansion.")
    else:
        technical_details.append(f"Normal volatility of **{volatility:.2f}%** daily indicates typical price movement for this stock. This suggests standard risk levels without extreme swings that would require special risk management.")
    
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

# STOCK ANALYSIS PAGE
if st.session_state.page == 'analysis':
    st.markdown("""
    <div class='brbas-header'>
        <h1 class='brbas-title'>BRBAS</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Search bar - all aligned
    col1, col2, col3 = st.columns([4, 2, 2])
    
    with col1:
        ticker_input = st.text_input("Search", value="AAPL", placeholder="Enter ticker or company name", label_visibility="collapsed", key="ticker_search")
        ticker = search_ticker(ticker_input)
    
    with col2:
        period = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3, key="period_select", label_visibility="collapsed")
    
    with col3:
        analysis_depth = st.selectbox("Depth", ["Standard", "Detailed", "Advanced"], index=1, key="depth_select", label_visibility="collapsed")
    
    # Load data
    with st.spinner(f"Analyzing {ticker}..."):
        data, info, error = get_stock_data(ticker, period)
    
    if error:
        st.error(f"Error: {error}")
        st.stop()
    
    if data is None or data.empty:
        st.error(f"No data available for {ticker}")
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
    advice = generate_detailed_advice(confidence, recommendation, ticker, info, valuation_score, momentum_score, earnings_score, technical_score)
    
    # Add to portfolio
    if ticker not in st.session_state.portfolio:
        if st.button("Add to Portfolio"):
            st.session_state.portfolio.append(ticker)
            st.success(f"Added {ticker} to portfolio!")
    
    # Company Header - Truncated description
    business_summary = info.get('longBusinessSummary', 'No description available.')
    truncated_summary = truncate_description(business_summary, 300)
    
    st.markdown(f"""
    <div class='company-header'>
        <div class='company-name'>{info.get('longName', ticker)}</div>
        <div style='font-size: 1.2rem; opacity: 0.9; font-weight: 600; margin-bottom: 1rem;'>{ticker} | {info.get('exchange', 'N/A')}</div>
        <div class='company-description'>{truncated_summary}</div>
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
                <div style='font-size: 0.9rem; color: #64748b; text-transform: uppercase; letter-spacing: 2px; font-weight: 600; margin-top: 0.5rem;'>Confidence Score</div>
                <div class='recommendation-badge {rec_class}' style='margin-top: 1.5rem;'>{recommendation}</div>
            </div>
            <div>
                <div class='advice-text'>{advice}</div>
                <div style='margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #e2e8f0;'>
                    <small style='color: #64748b;'><strong>Analysis Breakdown:</strong> Valuation ({valuation_score+6}/12) | Momentum ({momentum_score+6}/12) | Earnings ({earnings_score+6}/12) | Technical ({technical_score+6}/12)</small>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Price Chart
    st.markdown("<h2 class='section-header'>Price Performance</h2>", unsafe_allow_html=True)
    
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
    
    # ANALYSIS MODELS - THE CENTERPIECE
    st.markdown("<h2 class='section-header'>Investment Analysis Models</h2>", unsafe_allow_html=True)
    
    # Valuation Model
    st.markdown(f"""
    <div class='model-card'>
        <div class='model-header'>Valuation Model</div>
        <span class='model-score'>Score: {valuation_score+6}/12</span>
        <p style='color: #64748b; margin: 1rem 0;'>Analyzes whether the stock is over or undervalued relative to its fundamentals using PEG ratio, P/E trends, and price-to-book metrics.</p>
    </div>
    """, unsafe_allow_html=True)
    
    for detail in valuation_details:
        st.markdown(f"<div class='model-detail'>{detail}</div>", unsafe_allow_html=True)
    
    # Momentum Model
    st.markdown(f"""
    <div class='model-card'>
        <div class='model-header'>Momentum Model</div>
        <span class='model-score'>Score: {momentum_score+6}/12</span>
        <p style='color: #64748b; margin: 1rem 0;'>Evaluates trend strength using moving average crossovers, price positioning, and volume analysis to identify sustained directional movements.</p>
    </div>
    """, unsafe_allow_html=True)
    
    for detail in momentum_details:
        st.markdown(f"<div class='model-detail'>{detail}</div>", unsafe_allow_html=True)
    
    # Earnings Model
    st.markdown(f"""
    <div class='model-card'>
        <div class='model-header'>Earnings & Growth Model</div>
        <span class='model-score'>Score: {earnings_score+6}/12</span>
        <p style='color: #64748b; margin: 1rem 0;'>Assesses business health through earnings growth, revenue trends, profitability margins, and return on equity to gauge fundamental strength.</p>
    </div>
    """, unsafe_allow_html=True)
    
    for detail in earnings_details:
        st.markdown(f"<div class='model-detail'>{detail}</div>", unsafe_allow_html=True)
    
    # Technical Model
    st.markdown(f"""
    <div class='model-card'>
        <div class='model-header'>Technical Analysis Model</div>
        <span class='model-score'>Score: {technical_score+6}/12</span>
        <p style='color: #64748b; margin: 1rem 0;'>Uses RSI, MACD, and volatility indicators to identify overbought/oversold conditions and potential reversal points for tactical timing.</p>
    </div>
    """, unsafe_allow_html=True)
    
    for detail in technical_details:
        st.markdown(f"<div class='model-detail'>{detail}</div>", unsafe_allow_html=True)
    
    # Company Information Grid
    st.markdown("<h2 class='section-header'>Company Fundamentals</h2>", unsafe_allow_html=True)
    
    st.markdown("<div class='info-grid'>", unsafe_allow_html=True)
    
    info_data = [
        ("Sector", info.get('sector', 'N/A')),
        ("Industry", info.get('industry', 'N/A')),
        ("Employees", f"{info.get('fullTimeEmployees', 0):,}" if info.get('fullTimeEmployees') else 'N/A'),
        ("Market Cap", f"${info.get('marketCap', 0)/1e9:.2f}B" if info.get('marketCap', 0) > 1e9 else 'N/A'),
        ("Revenue (TTM)", f"${info.get('totalRevenue', 0)/1e9:.2f}B" if info.get('totalRevenue') else 'N/A'),
        ("Profit Margin", f"{info.get('profitMargins', 0)*100:.2f}%" if info.get('profitMargins') else 'N/A'),
        ("Operating Margin", f"{info.get('operatingMargins', 0)*100:.2f}%" if info.get('operatingMargins') else 'N/A'),
        ("ROE", f"{info.get('returnOnEquity', 0)*100:.2f}%" if info.get('returnOnEquity') else 'N/A'),
        ("ROA", f"{info.get('returnOnAssets', 0)*100:.2f}%" if info.get('returnOnAssets') else 'N/A'),
        ("Debt/Equity", f"{info.get('debtToEquity', 0):.2f}" if info.get('debtToEquity') else 'N/A'),
        ("Current Ratio", f"{info.get('currentRatio', 0):.2f}" if info.get('currentRatio') else 'N/A'),
        ("Beta", f"{info.get('beta', 0):.2f}" if info.get('beta') else 'N/A'),
        ("Dividend Yield", f"{info.get('dividendYield', 0)*100:.2f}%" if info.get('dividendYield') else 'N/A'),
        ("Payout Ratio", f"{info.get('payoutRatio', 0)*100:.2f}%" if info.get('payoutRatio') else 'N/A'),
    ]
    
    for label, value in info_data:
        st.markdown(f"""
        <div class='info-row'>
            <span class='info-label'>{label}</span>
            <span class='info-value'>{value}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# COMPARE STOCKS PAGE
elif st.session_state.page == 'compare':
    st.markdown("""
    <div class='brbas-header'>
        <h1 class='brbas-title'>BRBAS</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 class='section-header'>Compare Stocks</h2>", unsafe_allow_html=True)
    
    comp_col1, comp_col2, comp_col3, comp_col4 = st.columns([3, 3, 3, 2])
    
    with comp_col1:
        ticker1 = st.text_input("Stock 1", value="AAPL", key="comp1").upper()
    with comp_col2:
        ticker2 = st.text_input("Stock 2", value="MSFT", key="comp2").upper()
    with comp_col3:
        ticker3 = st.text_input("Stock 3 (optional)", value="", key="comp3").upper()
    with comp_col4:
        comp_period = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y"], index=2)
    
    if st.button("Compare Stocks", type="primary"):
        tickers_to_compare = [t for t in [ticker1, ticker2, ticker3] if t]
        
        if len(tickers_to_compare) < 2:
            st.warning("Please enter at least 2 stocks")
        else:
            comparison_data = []
            
            for ticker_comp in tickers_to_compare:
                with st.spinner(f"Analyzing {ticker_comp}..."):
                    data_comp, info_comp, error_comp = get_stock_data(ticker_comp, comp_period)
                    
                    if error_comp or data_comp is None or data_comp.empty:
                        st.error(f"Could not load {ticker_comp}")
                        continue
                    
                    for ma_period in [20, 50, 100, 200]:
                        data_comp[f'MA{ma_period}'] = data_comp['Close'].rolling(window=ma_period).mean()
                    
                    data_comp = calculate_ema(data_comp, [8, 21, 50])
                    data_comp['RSI'] = calculate_rsi(data_comp)
                    data_comp['MACD'], data_comp['Signal'], data_comp['Histogram'] = calculate_macd(data_comp)
                    
                    val_score, val_details = analyze_valuation(info_comp)
                    mom_score, mom_details = analyze_momentum(data_comp)
                    earn_score, earn_details = analyze_earnings(info_comp)
                    tech_score, tech_details = analyze_technical(data_comp)
                    
                    conf = calculate_confidence_score(info_comp, data_comp, val_score, mom_score, earn_score, tech_score)
                    rec, rec_class = get_recommendation_from_confidence(conf)
                    
                    current_price_comp = data_comp['Close'].iloc[-1]
                    price_change_comp = data_comp['Close'].iloc[-1] - data_comp['Close'].iloc[0]
                    pct_change_comp = (price_change_comp / data_comp['Close'].iloc[0]) * 100
                    
                    comparison_data.append({
                        'Ticker': ticker_comp,
                        'Company': info_comp.get('longName', ticker_comp),
                        'Price': current_price_comp,
                        'Change': pct_change_comp,
                        'Confidence': conf,
                        'Recommendation': rec,
                        'rec_class': rec_class,
                        'Valuation': f"{val_score+6}/12",
                        'Momentum': f"{mom_score+6}/12",
                        'Earnings': f"{earn_score+6}/12",
                        'Technical': f"{tech_score+6}/12",
                        'Market Cap': f"${info_comp.get('marketCap', 0)/1e9:.1f}B" if info_comp.get('marketCap', 0) > 1e9 else "N/A",
                        'P/E': f"{info_comp.get('trailingPE', 0):.2f}" if info_comp.get('trailingPE') else "N/A",
                        'Sector': info_comp.get('sector', 'N/A')
                    })
            
            if comparison_data:
                st.markdown("### Comparison Results")
                
                cols = st.columns(len(comparison_data))
                
                for idx, stock_data in enumerate(comparison_data):
                    with cols[idx]:
                        if 'BUY' in stock_data['Recommendation']:
                            card_color = '#10b981'
                        elif 'SELL' in stock_data['Recommendation']:
                            card_color = '#ef4444'
                        else:
                            card_color = '#f59e0b'
                        
                        st.markdown(f"""
                        <div style='background: white; padding: 1.5rem; border-radius: 12px; 
                                    border-left: 4px solid {card_color}; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                            <h3 style='margin: 0; color: #1e293b;'>{stock_data['Ticker']}</h3>
                            <p style='color: #64748b; font-size: 0.9rem;'>{stock_data['Company'][:30]}</p>
                            <div style='margin: 1rem 0;'>
                                <div style='font-size: 1.5rem; font-weight: 700; color: #1e293b;'>${stock_data['Price']:.2f}</div>
                                <div style='color: {"#10b981" if stock_data["Change"] > 0 else "#ef4444"}; font-weight: 600;'>{stock_data['Change']:+.2f}%</div>
                            </div>
                            <div style='background: {card_color}; color: white; padding: 0.5rem; 
                                        border-radius: 8px; text-align: center; font-weight: 700;'>
                                {stock_data['Recommendation']}
                            </div>
                            <div style='font-size: 1.2rem; font-weight: 700; text-align: center; margin-top: 1rem; color: #1e293b;'>
                                {stock_data['Confidence']}%
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("**Scores:**")
                        st.write(f"Valuation: {stock_data['Valuation']}")
                        st.write(f"Momentum: {stock_data['Momentum']}")
                        st.write(f"Earnings: {stock_data['Earnings']}")
                        st.write(f"Technical: {stock_data['Technical']}")
                
                st.markdown("---")
                st.dataframe(pd.DataFrame(comparison_data).drop('rec_class', axis=1), use_container_width=True, hide_index=True)

# PORTFOLIO PAGE
elif st.session_state.page == 'portfolio':
    st.markdown("""
    <div class='brbas-header'>
        <h1 class='brbas-title'>BRBAS</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 class='section-header'>My Portfolio</h2>", unsafe_allow_html=True)
    
    if not st.session_state.portfolio:
        st.info("Your portfolio is empty. Add stocks from the Stock Analysis page.")
    else:
        st.markdown(f"### Tracking {len(st.session_state.portfolio)} stocks")
        
        for ticker_port in st.session_state.portfolio:
            data_port, info_port, error_port = get_stock_data(ticker_port, "1mo")
            
            if not error_port and data_port is not None and not data_port.empty:
                current_price = data_port['Close'].iloc[-1]
                price_change = data_port['Close'].iloc[-1] - data_port['Close'].iloc[0]
                pct_change = (price_change / data_port['Close'].iloc[0]) * 100
                change_color = "#10b981" if pct_change > 0 else "#ef4444"
                
                col_main, col_actions = st.columns([4, 1])
                
                with col_main:
                    st.markdown(f"""
                    <div class='portfolio-card'>
                        <div class='portfolio-info'>
                            <h3 style='margin: 0; color: #1e293b;'>{ticker_port}</h3>
                            <p style='color: #64748b; font-size: 0.9rem; margin: 0.25rem 0;'>{info_port.get('longName', ticker_port)[:40]}</p>
                            <div style='font-size: 1.8rem; font-weight: 700; color: #1e293b; margin-top: 0.5rem;'>${current_price:.2f}</div>
                            <div style='color: {change_color}; font-weight: 600; font-size: 1.1rem;'>{pct_change:+.2f}%</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_actions:
                    if st.button("Analyze", key=f"analyze_{ticker_port}", use_container_width=True):
                        st.session_state.page = 'analysis'
                        st.rerun()
                    if st.button("Remove", key=f"remove_{ticker_port}", use_container_width=True):
                        st.session_state.portfolio.remove(ticker_port)
                        st.rerun()
        
        if st.button("Clear Portfolio", type="secondary"):
            st.session_state.portfolio = []
            st.rerun()

# TOP STOCKS PAGE
elif st.session_state.page == 'top_stocks':
    st.markdown("""
    <div class='brbas-header'>
        <h1 class='brbas-title'>BRBAS</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 class='section-header'>Top Stocks by Sector</h2>", unsafe_allow_html=True)
    st.markdown("### Highest confidence stocks across major sectors")
    
    # Top sectors and representative stocks
    sectors = {
        'Technology': ['AAPL', 'MSFT', 'GOOGL', 'META', 'NVDA'],
        'Healthcare': ['JNJ', 'UNH', 'PFE', 'ABBV', 'TMO'],
        'Financial': ['JPM', 'BAC', 'WFC', 'GS', 'MS'],
        'Consumer': ['AMZN', 'TSLA', 'HD', 'MCD', 'NKE'],
        'Energy': ['XOM', 'CVX', 'COP', 'SLB', 'EOG'],
        'Industrial': ['BA', 'CAT', 'GE', 'HON', 'UPS'],
        'Materials': ['LIN', 'APD', 'SHW', 'NEM', 'FCX'],
        'Utilities': ['NEE', 'DUK', 'SO', 'D', 'AEP'],
        'Real Estate': ['AMT', 'PLD', 'CCI', 'EQIX', 'PSA'],
        'Communication': ['GOOGL', 'META', 'DIS', 'NFLX', 'CMCSA']
    }
    
    with st.spinner("Analyzing top stocks across sectors..."):
        sector_results = {}
        
        for sector, tickers in sectors.items():
            best_stock = None
            best_confidence = 0
            
            for ticker in tickers[:3]:  # Analyze top 3 per sector
                data_top, info_top, error_top = get_stock_data(ticker, "3mo")
                
                if error_top or data_top is None or data_top.empty:
                    continue
                
                for ma_period in [20, 50, 100, 200]:
                    data_top[f'MA{ma_period}'] = data_top['Close'].rolling(window=ma_period).mean()
                
                data_top = calculate_ema(data_top, [8, 21, 50])
                data_top['RSI'] = calculate_rsi(data_top)
                data_top['MACD'], data_top['Signal'], data_top['Histogram'] = calculate_macd(data_top)
                
                val_s, _ = analyze_valuation(info_top)
                mom_s, _ = analyze_momentum(data_top)
                earn_s, _ = analyze_earnings(info_top)
                tech_s, _ = analyze_technical(data_top)
                
                conf = calculate_confidence_score(info_top, data_top, val_s, mom_s, earn_s, tech_s)
                
                if conf > best_confidence:
                    best_confidence = conf
                    rec, rec_class = get_recommendation_from_confidence(conf)
                    best_stock = {
                        'ticker': ticker,
                        'company': info_top.get('longName', ticker),
                        'price': data_top['Close'].iloc[-1],
                        'confidence': conf,
                        'recommendation': rec,
                        'rec_class': rec_class
                    }
            
            if best_stock:
                sector_results[sector] = best_stock
    
    # Display results
    cols = st.columns(2)
    
    for idx, (sector, stock) in enumerate(sector_results.items()):
        with cols[idx % 2]:
            if 'BUY' in stock['recommendation']:
                card_color = '#10b981'
            elif 'SELL' in stock['recommendation']:
                card_color = '#ef4444'
            else:
                card_color = '#f59e0b'
            
            st.markdown(f"""
            <div style='background: white; padding: 1.5rem; border-radius: 12px; 
                        border-left: 4px solid {card_color}; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 1rem;'>
                <div style='font-size: 0.85rem; color: #64748b; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;'>{sector}</div>
                <h3 style='margin: 0.5rem 0; color: #1e293b;'>{stock['ticker']}</h3>
                <p style='color: #64748b; font-size: 0.9rem;'>{stock['company'][:35]}</p>
                <div style='font-size: 1.5rem; font-weight: 700; color: #1e293b; margin-top: 0.5rem;'>${stock['price']:.2f}</div>
                <div style='background: {card_color}; color: white; padding: 0.4rem 1rem; 
                            border-radius: 20px; text-align: center; font-weight: 600; margin-top: 1rem; display: inline-block;'>
                    {stock['recommendation']}
                </div>
                <div style='font-size: 1.3rem; font-weight: 700; color: #1e293b; margin-top: 1rem;'>
                    Confidence: {stock['confidence']}%
                </div>
            </div>
            """, unsafe_allow_html=True)
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
        line-height: 1.8;
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
        font-size: 2rem;
        font-weight: 700;
        color: #1e293b;
        margin: 3rem 0 1.5rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 3px solid #3b82f6;
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
        font-size: 1.5rem;
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
    
    .model-detail {
        padding: 1rem;
        margin: 0.75rem 0;
        background: #f8fafc;
        border-left: 3px solid #3b82f6;
        border-radius: 4px;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    .info-grid {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
        margin: 2rem 0;
    }
    
    .info-row {
        display: flex;
        justify-content: space-between;
        padding: 1rem 0;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .info-label {
        font-weight: 600;
        color: #64748b;
        font-size: 1.1rem;
    }
    
    .info-value {
        font-weight: 700;
        color: #1e293b;
        font-size: 1.2rem;
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
        transition: all 0.2s;
    }
    
    [data-testid="stSidebar"] button:hover {
        background: rgba(255, 255, 255, 0.2);
        border-color: rgba(255, 255, 255, 0.4);
        transform: translateX(5px);
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
    
    .portfolio-info {
        flex: 1;
    }
    
    .portfolio-actions {
        display: flex;
        gap: 0.5rem;
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .company-header, .confidence-card, .model-card {
        animation: fadeInUp 0.6s ease-out;
    }
    
    .stMetric:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .model-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
        transition: all 0.3s ease;
    }
    
    /* Align search inputs */
    .row-widget.stSelectbox, .row-widget.stTextInput {
        display: flex;
        align-items: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'analysis'
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []

# Sidebar Navigation
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
    
    st.markdown("---")
    st.markdown("<p style='color: rgba(255,255,255,0.7); font-size: 1rem; text-align: center;'>Professional Stock Analysis Platform</p>", unsafe_allow_html=True)

# Helper functions
def search_ticker(query):
    mapping = {
        'apple': 'AAPL', 'microsoft': 'MSFT', 'google': 'GOOGL', 'amazon': 'AMZN',
        'tesla': 'TSLA', 'meta': 'META', 'nvidia': 'NVDA', 'netflix': 'NFLX',
        'disney': 'DIS', 'walmart': 'WMT', 'coca cola': 'KO', 'pepsi': 'PEP'
    }
    
    query_lower = query.lower()
    if query_lower in mapping:
        return mapping[query_lower]
    return query.upper()

def truncate_description(text, max_length=300):
    """Truncate description properly without cutting mid-sentence"""
    if len(text) <= max_length:
        return text
    
    truncated = text[:max_length]
    last_period = truncated.rfind('.')
    
    if last_period > max_length * 0.7:
        return truncated[:last_period + 1]
    else:
        last_space = truncated.rfind(' ')
        return truncated[:last_space] + '.'

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

def generate_detailed_advice(confidence, recommendation, ticker, info, valuation_score, momentum_score, earnings_score, technical_score):
    company_name = info.get('longName', ticker)
    
    if confidence >= 75:
        base = f"Considering {company_name}'s strong fundamentals, positive momentum indicators, and robust earnings trajectory, I recommend **accumulating a position** in {ticker}. The data suggests significant upside potential with manageable risk."
    elif confidence >= 60:
        base = f"Based on {company_name}'s favorable valuation metrics and positive technical indicators, I recommend **initiating or adding to a position** in {ticker}. Monitor for any changes in market conditions."
    elif confidence >= 40:
        base = f"Given {company_name}'s mixed signals across valuation, momentum, and earnings metrics, I recommend **holding existing positions** in {ticker} and waiting for clearer directional signals before making additional moves."
    elif confidence >= 25:
        base = f"Considering {company_name}'s deteriorating fundamentals and weak technical indicators, I recommend **reducing exposure** to {ticker}. Consider reallocating capital to stronger opportunities."
    else:
        base = f"Given {company_name}'s significant headwinds across multiple analysis dimensions, I recommend **exiting positions** in {ticker}. The risk-reward profile is currently unfavorable."
    
    analysis = f"\n\n**Detailed Analysis:**\n\n"
    
    analysis += f"**Valuation ({valuation_score+6}/12):** "
    peg = info.get('pegRatio', None)
    pe = info.get('trailingPE', None)
    
    if valuation_score >= 2:
        analysis += f"The stock appears undervalued. "
        if peg and peg < 1:
            analysis += f"The PEG ratio of {peg:.2f} indicates the stock is trading below its growth rate, suggesting a compelling value opportunity. "
        if pe and pe < 20:
            analysis += f"With a P/E ratio of {pe:.1f}, the stock is reasonably priced relative to earnings. "
    elif valuation_score <= -2:
        analysis += f"Valuation metrics raise concerns. "
        if peg and peg > 2:
            analysis += f"The PEG ratio of {peg:.2f} suggests the stock is expensive relative to its growth prospects. "
        if pe and pe > 30:
            analysis += f"The elevated P/E ratio of {pe:.1f} indicates premium pricing that may not be justified. "
    else:
        analysis += f"Valuation appears fair. "
    
    analysis += f"\n\n**Momentum ({momentum_score+6}/12):** "
    if momentum_score >= 2:
        analysis += f"Strong bullish momentum is evident with the 50-day moving average crossing above the 200-day MA, a classically bullish technical signal suggesting institutional accumulation. "
    elif momentum_score <= -2:
        analysis += f"Momentum indicators are concerning with a death cross formation signaling potential further downside. "
    
    analysis += f"\n\n**Earnings & Growth ({earnings_score+6}/12):** "
    earnings_growth = info.get('earningsQuarterlyGrowth', None)
    
    if earnings_score >= 2:
        analysis += f"The company demonstrates strong fundamental health. "
        if earnings_growth and earnings_growth > 0.15:
            analysis += f"Quarterly earnings growth of {earnings_growth*100:.1f}% significantly exceeds market averages. "
    elif earnings_score <= -2:
        analysis += f"Fundamental performance is weak. "
        if earnings_growth and earnings_growth < 0:
            analysis += f"Negative earnings growth of {earnings_growth*100:.1f}% signals operational challenges. "
    
    beta = info.get('beta', None)
    if beta:
        if beta > 1.5:
            analysis += f"\n\n**Risk Assessment:** High volatility (Beta: {beta:.2f}) suggests this stock experiences larger price swings than the broader market."
        elif beta < 0.5:
            analysis += f"\n\n**Risk Assessment:** Low volatility (Beta: {beta:.2f}) indicates relative stability."
    
    return base + analysis

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
    pe = info.get('trailingPE', None)
    forward_pe = info.get('forwardPE', None)
    pb = info.get('priceToBook', None)
    
    # PEG Analysis
    if peg and peg > 0:
        if peg < 1:
            valuation_score += 2
            valuation_details.append(f"PEG Ratio of **{peg:.2f}** indicates the stock is undervalued relative to its growth rate. Stocks with PEG ratios below 1.0 are typically considered attractive investments, as you're paying less per unit of earnings growth than the market average.")
        elif peg < 1.5:
            valuation_score += 1
            valuation_details.append(f"PEG Ratio of **{peg:.2f}** suggests fair valuation. The stock is priced reasonably relative to its expected growth, though not at a significant discount.")
        elif peg < 2:
            valuation_score -= 1
            valuation_details.append(f"PEG Ratio of **{peg:.2f}** indicates slight overvaluation. Investors are paying a premium for growth that may not justify the current price level.")
        else:
            valuation_score -= 2
            valuation_details.append(f"PEG Ratio of **{peg:.2f}** signals significant overvaluation. The stock's price is substantially elevated relative to its growth prospects, suggesting limited upside potential at current levels.")
    else:
        valuation_details.append("PEG Ratio data unavailable. This metric compares the P/E ratio to earnings growth rate and is crucial for assessing whether a stock's valuation is justified by its growth trajectory.")
    
    # P/E Trend Analysis
    if pe and forward_pe and pe > 0 and forward_pe > 0:
        pe_change = ((forward_pe - pe) / pe) * 100
        if forward_pe < pe * 0.9:
            valuation_score += 1
            valuation_details.append(f"P/E ratio improving from **{pe:.1f}** to **{forward_pe:.1f}** (a {abs(pe_change):.1f}% improvement). This forward-looking improvement suggests the market expects stronger earnings growth, which could drive price appreciation.")
        elif forward_pe > pe * 1.1:
            valuation_score -= 1
            valuation_details.append(f"P/E ratio deteriorating from **{pe:.1f}** to **{forward_pe:.1f}** (a {abs(pe_change):.1f}% increase). Rising P/E with flat prices suggests weakening earnings expectations, which is a bearish indicator.")
        else:
            valuation_details.append(f"P/E ratio stable at **{pe:.1f}** (forward: **{forward_pe:.1f}**). Earnings expectations are consistent, indicating steady business performance without major growth or contraction anticipated.")
    elif pe and pe > 0:
        if pe < 15:
            valuation_score += 1
            valuation_details.append(f"P/E Ratio of **{pe:.1f}** is below market average (typically 15-20), suggesting the stock may be undervalued or the market has concerns about future growth.")
        elif pe > 30:
            valuation_score -= 1
            valuation_details.append(f"P/E Ratio of **{pe:.1f}** exceeds market norms, indicating investors are paying a premium. This is justified only if growth expectations are exceptionally high.")
        else:
            valuation_details.append(f"P/E Ratio of **{pe:.1f}** is within normal market range (15-25), suggesting standard valuation without extreme over or underpricing.")
    else:
        valuation_details.append("P/E Ratio data unavailable. This fundamental metric shows how much investors pay per dollar of earnings and is essential for value assessment.")
    
    # P/B Analysis
    if pb and pb > 0:
        if pb < 1:
            valuation_score += 1
            valuation_details.append(f"Price-to-Book ratio of **{pb:.2f}** means the stock trades below its book value. This could indicate a value opportunity, though it may also suggest the market doubts the quality of assets or future profitability.")
        elif pb > 5:
            valuation_score -= 1
            valuation_details.append(f"Price-to-Book ratio of **{pb:.2f}** represents a significant premium to book value. This is common for high-growth companies but may indicate excessive optimism if growth doesn't materialize.")
        else:
            valuation_details.append(f"Price-to-Book ratio of **{pb:.2f}** is reasonable. The stock trades at a moderate premium to book value, typical for established companies with solid profitability.")
    else:
        valuation_details.append("Price-to-Book ratio unavailable. This metric compares market value to accounting book value and helps identify potentially undervalued assets.")
    
    return valuation_score, valuation_details

def analyze_momentum(data):
    momentum_score = 0
    momentum_details = []
    
    current_price = data['Close'].iloc[-1]
    
    # Golden Cross / Death Cross
    if 'MA50' in data.columns and 'MA200' in data.columns:
        ma50 = data['MA50'].iloc[-1]
        ma200 = data['MA200'].iloc[-1]
        
        if pd.notna(ma50) and pd.notna(ma200):
            if ma50 > ma200 and current_price > ma50:
                momentum_score += 2
                momentum_details.append(f"**Golden Cross Active**: The 50-day moving average (**${ma50:.2f}**) is above the 200-day MA (**${ma200:.2f}**), and price (**${current_price:.2f}**) is above both. This is one of the most reliable bullish technical signals, indicating sustained upward momentum and suggesting institutional buying pressure. Historically, golden crosses precede extended rallies.")
            elif ma50 < ma200 and current_price < ma50:
                momentum_score -= 2
                momentum_details.append(f"**Death Cross Active**: The 50-day moving average (**${ma50:.2f}**) is below the 200-day MA (**${ma200:.2f}**), and price (**${current_price:.2f}**) is below both. This bearish configuration suggests sustained downward pressure and typically precedes extended periods of underperformance. Consider this a major warning signal.")
            elif current_price > ma50 and current_price > ma200:
                momentum_score += 1
                momentum_details.append(f"Price (**${current_price:.2f}**) is above both the 50-day (**${ma50:.2f}**) and 200-day (**${ma200:.2f}**) moving averages, indicating bullish momentum even though moving averages haven't crossed yet. This suggests buyer strength.")
            elif current_price < ma50 and current_price < ma200:
                momentum_score -= 1
                momentum_details.append(f"Price (**${current_price:.2f}**) is below both the 50-day (**${ma50:.2f}**) and 200-day (**${ma200:.2f}**) moving averages, indicating bearish momentum. This suggests sellers are in control.")
            else:
                momentum_details.append(f"Mixed signals with price (**${current_price:.2f}**) between the 50-day (**${ma50:.2f}**) and 200-day (**${ma200:.2f}**) moving averages. The stock is in a transition phase with unclear directional bias.")
        else:
            momentum_details.append("Insufficient data for 50-day and 200-day moving average analysis. These long-term trend indicators require extended price history.")
    else:
        momentum_details.append("Moving average data unavailable. These indicators smooth out price action to reveal the underlying trend and are fundamental to momentum analysis.")
    
    # Short-term momentum
    if 'MA20' in data.columns:
        ma20 = data['MA20'].iloc[-1]
        if pd.notna(ma20):
            deviation = ((current_price / ma20) - 1) * 100
            if current_price > ma20 * 1.03:
                momentum_score += 1
                momentum_details.append(f"Strong short-term momentum with price **{deviation:.1f}%** above the 20-day MA (**${ma20:.2f}**). This substantial deviation indicates powerful buying pressure and suggests the recent trend is likely to continue in the near term.")
            elif current_price < ma20 * 0.97:
                momentum_score -= 1
                momentum_details.append(f"Weak short-term momentum with price **{deviation:.1f}%** below the 20-day MA (**${ma20:.2f}**). This indicates selling pressure and suggests the recent downtrend may continue until support levels are established.")
            else:
                momentum_details.append(f"Price is **{abs(deviation):.1f}%** {'above' if deviation > 0 else 'below'} the 20-day MA (**${ma20:.2f}**), indicating neutral short-term momentum. The stock is consolidating without strong directional bias.")
        else:
            momentum_details.append("Insufficient data for 20-day moving average. This short-term indicator helps identify immediate trend strength and potential reversal points.")
    else:
        momentum_details.append("20-day moving average unavailable. This short-term momentum indicator is valuable for timing entries and exits.")
    
    # Volume analysis
    avg_volume = data['Volume'].tail(20).mean()
    current_volume = data['Volume'].iloc[-1]
    volume_ratio = (current_volume / avg_volume)
    
    if volume_ratio > 1.5:
        volume_change = ((volume_ratio - 1) * 100)
        momentum_details.append(f"Significant volume surge of **{volume_change:.0f}%** above the 20-day average. Current volume of **{current_volume:,.0f}** compared to average of **{avg_volume:,.0f}** suggests institutional activity. High volume confirms the strength of the current price movement, whether up or down.")
    elif volume_ratio < 0.7:
        momentum_details.append(f"Below-average volume at **{(volume_ratio * 100):.0f}%** of the 20-day average suggests low conviction in the current price level. Light volume moves are less reliable and more easily reversed.")
    else:
        momentum_details.append(
