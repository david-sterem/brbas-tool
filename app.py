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

st.set_page_config(page_title="SternCurve", layout="wide", page_icon="📊")

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
            stock['position'] = "Oversold" if current_k < 20 else "Overbought" if current_k > 80 else "Neutral"
            stock['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M")
            return False
    
    st.session_state.portfolio.append({
        'ticker': ticker,
        'stoch_k': current_k,
        'stoch_d': current_d,
        'momentum': k_momentum,
        'trend': trend,
        'position': "Oversold" if current_k < 20 else "Overbought" if current_k > 80 else "Neutral",
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
    
    if 'financial' in sector or 'bank' in industry or 'insurance' in industry or 'credit' in industry:
        return 'Financial Services'
    elif 'technology' in sector or 'software' in industry or 'semiconductor' in industry or 'information technology' in sector:
        return 'Technology'
    elif 'industrial' in sector or 'aerospace' in industry or 'defense' in industry or 'machinery' in industry or 'construction' in industry:
        return 'Industrial'
    elif 'energy' in sector or 'oil' in industry or 'gas' in industry or 'petroleum' in industry:
        return 'Energy'
    elif 'real estate' in sector or 'reit' in industry:
        return 'Real Estate'
    elif 'consumer cyclical' in sector or 'retail' in industry or 'automotive' in industry or 'apparel' in industry or 'travel' in industry:
        return 'Consumer Cyclical'
    elif 'consumer defensive' in sector or 'consumer staples' in sector or 'food' in industry or 'beverage' in industry or 'household' in industry:
        return 'Consumer Defensive'
    elif 'communication' in sector or 'media' in industry or 'telecom' in industry or 'entertainment' in industry:
        return 'Communication Services'
    elif 'basic materials' in sector or 'materials' in sector or 'chemical' in industry or 'metal' in industry or 'mining' in industry:
        return 'Basic Materials'
    elif 'utilities' in sector or 'utility' in industry or 'electric' in industry:
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
        'drivers': [],
        'what_to_look_for': [],
        'peer_examples': []
    }
    
    pe_ratio = info.get('trailingPE', info.get('forwardPE'))
    
    if sector == 'Financial Services':
        analysis['drivers'] = ['Interest rates', 'Loan growth', 'Credit quality', 'Regulation']
        analysis['peer_examples'] = ['JPM', 'BAC', 'GS', 'WFC', 'BRK-B']
        analysis['what_to_look_for'] = ['Growing deposits', 'Stable loan portfolio', 'Good risk management']
        
        roe = info.get('returnOnEquity', 0) * 100 if info.get('returnOnEquity') else None
        book_value = info.get('bookValue')
        pb_ratio = info.get('priceToBook')
        
        analysis['metrics'] = {
            'P/E Ratio': f"{pe_ratio:.2f}" if pe_ratio else 'N/A',
            'ROE (Return on Equity)': f"{roe:.1f}%" if roe else 'N/A',
            'Price-to-Book (P/B)': f"{pb_ratio:.2f}" if pb_ratio else 'N/A',
            'Book Value per Share': f"${book_value:.2f}" if book_value else 'N/A'
        }
        
        score = 50
        if roe:
            if roe > 15:
                analysis['strengths'].append(f"Strong ROE of {roe:.1f}% - Efficient use of capital")
                score += 20
            elif roe > 10:
                analysis['strengths'].append(f"Adequate ROE of {roe:.1f}%")
                score += 10
            elif roe < 8:
                analysis['weaknesses'].append(f"Low ROE of {roe:.1f}% - Inefficient capital deployment")
                score -= 15
        
        if pb_ratio:
            if pb_ratio < 1.0:
                analysis['strengths'].append(f"Attractive P/B of {pb_ratio:.2f} - Trading below book value")
                score += 15
            elif pb_ratio < 1.5:
                analysis['strengths'].append(f"Reasonable P/B of {pb_ratio:.2f}")
                score += 10
            elif pb_ratio > 3:
                analysis['weaknesses'].append(f"High P/B of {pb_ratio:.2f} - May be overvalued")
                score -= 15
        
        if pe_ratio:
            if pe_ratio < 12:
                analysis['strengths'].append(f"Low P/E of {pe_ratio:.2f} - Potential value")
                score += 5
            elif pe_ratio > 20:
                analysis['weaknesses'].append(f"High P/E of {pe_ratio:.2f} - May be expensive")
                score -= 5
        
        analysis['rating'] = max(0, min(100, score))
        
    elif sector == 'Technology':
        analysis['drivers'] = ['Innovation cycles', 'AI growth', 'Cloud adoption', 'Consumer demand']
        analysis['peer_examples'] = ['AAPL', 'NVDA', 'MSFT', 'AMD', 'ADBE']
        analysis['what_to_look_for'] = ['Scalable software models', 'High customer retention', 'IP moats and competitive advantages']
        
        revenue_growth = info.get('revenueGrowth', 0) * 100 if info.get('revenueGrowth') else None
        gross_margin = info.get('grossMargins', 0) * 100 if info.get('grossMargins') else None
        free_cash_flow = info.get('freeCashflow', 0)
        
        analysis['metrics'] = {
            'P/E Ratio': f"{pe_ratio:.2f}" if pe_ratio else 'N/A',
            'Revenue Growth (YoY)': f"{revenue_growth:.1f}%" if revenue_growth else 'N/A',
            'Gross Margin': f"{gross_margin:.1f}%" if gross_margin else 'N/A',
            'Free Cash Flow': f"${free_cash_flow/1e9:.2f}B" if free_cash_flow else 'N/A'
        }
        
        score = 50
        if revenue_growth:
            if revenue_growth > 20:
                analysis['strengths'].append(f"Exceptional revenue growth of {revenue_growth:.1f}%")
                score += 25
            elif revenue_growth > 15:
                analysis['strengths'].append(f"Strong revenue growth of {revenue_growth:.1f}%")
                score += 20
            elif revenue_growth > 10:
                analysis['strengths'].append(f"Solid revenue growth of {revenue_growth:.1f}%")
                score += 10
            elif revenue_growth < 5:
                analysis['weaknesses'].append(f"Slow revenue growth of {revenue_growth:.1f}%")
                score -= 20
        
        if gross_margin:
            if gross_margin > 70:
                analysis['strengths'].append(f"Excellent gross margin of {gross_margin:.1f}% - Strong competitive advantage")
                score += 20
            elif gross_margin > 60:
                analysis['strengths'].append(f"High gross margin of {gross_margin:.1f}%")
                score += 15
            elif gross_margin < 40:
                analysis['weaknesses'].append(f"Low gross margin of {gross_margin:.1f}% - Limited pricing power")
                score -= 15
        
        if free_cash_flow:
            if free_cash_flow > 5e9:
                analysis['strengths'].append("Strong free cash flow generation")
                score += 15
            elif free_cash_flow > 0:
                analysis['strengths'].append("Positive free cash flow")
                score += 10
            else:
                analysis['weaknesses'].append("Negative free cash flow")
                score -= 10
        
        analysis['rating'] = max(0, min(100, score))
        
    elif sector == 'Industrial':
        analysis['drivers'] = ['Economic growth', 'Infrastructure spending', 'Supply chain health']
        analysis['peer_examples'] = ['BA', 'CAT', 'GE', 'HON', 'RTX']
        analysis['what_to_look_for'] = ['Operational efficiency', 'Diversified client base', 'Government contracts']
        
        operating_margin = info.get('operatingMargins', 0) * 100 if info.get('operatingMargins') else None
        debt_to_equity = info.get('debtToEquity')
        free_cash_flow = info.get('freeCashflow', 0)
        
        analysis['metrics'] = {
            'Operating Margin': f"{operating_margin:.1f}%" if operating_margin else 'N/A',
            'Debt-to-Equity': f"{debt_to_equity:.2f}" if debt_to_equity else 'N/A',
            'Free Cash Flow': f"${free_cash_flow/1e9:.2f}B" if free_cash_flow else 'N/A',
            'P/E Ratio': f"{pe_ratio:.2f}" if pe_ratio else 'N/A'
        }
        
        score = 50
        if operating_margin:
            if operating_margin > 15:
                analysis['strengths'].append(f"Strong operating margin of {operating_margin:.1f}%")
                score += 20
            elif operating_margin > 10:
                analysis['strengths'].append(f"Healthy operating margin of {operating_margin:.1f}%")
                score += 10
            elif operating_margin < 5:
                analysis['weaknesses'].append(f"Low operating margin of {operating_margin:.1f}%")
                score -= 15
        
        if debt_to_equity:
            if debt_to_equity < 50:
                analysis['strengths'].append(f"Low debt-to-equity of {debt_to_equity:.2f} - Strong balance sheet")
                score += 15
            elif debt_to_equity > 150:
                analysis['weaknesses'].append(f"High debt-to-equity of {debt_to_equity:.2f} - Leverage risk")
                score -= 20
        
        if free_cash_flow and free_cash_flow > 0:
            analysis['strengths'].append("Positive free cash flow - Financial stability")
            score += 15
        
        analysis['rating'] = max(0, min(100, score))
        
    elif sector == 'Energy':
        analysis['drivers'] = ['Commodity prices (oil, natural gas)', 'Geopolitical factors', 'OPEC decisions']
        analysis['peer_examples'] = ['XOM', 'CVX', 'COP', 'SLB', 'NEE']
        analysis['what_to_look_for'] = ['Low-cost producers', 'Strong reserves', 'Diversification into renewables']
        
        pb_ratio = info.get('priceToBook')
        debt_to_equity = info.get('debtToEquity')
        free_cash_flow = info.get('freeCashflow', 0)
        
        analysis['metrics'] = {
            'Price-to-Book (P/B)': f"{pb_ratio:.2f}" if pb_ratio else 'N/A',
            'Debt-to-Equity': f"{debt_to_equity:.2f}" if debt_to_equity else 'N/A',
            'Free Cash Flow': f"${free_cash_flow/1e9:.2f}B" if free_cash_flow else 'N/A',
            'P/E Ratio': f"{pe_ratio:.2f}" if pe_ratio else 'N/A'
        }
        
        score = 50
        if pb_ratio:
            if pb_ratio < 1.5:
                analysis['strengths'].append(f"Attractive P/B of {pb_ratio:.2f}")
                score += 15
            elif pb_ratio > 3:
                analysis['weaknesses'].append(f"High P/B of {pb_ratio:.2f}")
                score -= 10
        
        if debt_to_equity:
            if debt_to_equity < 40:
                analysis['strengths'].append(f"Low debt-to-equity of {debt_to_equity:.2f}")
                score += 20
            elif debt_to_equity > 100:
                analysis['weaknesses'].append(f"High debt-to-equity of {debt_to_equity:.2f}")
                score -= 15
        
        if free_cash_flow and free_cash_flow > 2e9:
            analysis['strengths'].append("Strong free cash flow coverage")
            score += 15
        
        analysis['rating'] = max(0, min(100, score))
        
    elif sector == 'Real Estate':
        analysis['drivers'] = ['Interest rates', 'Occupancy rates', 'Property values']
        analysis['peer_examples'] = ['PLD', 'O', 'SPG', 'AMT']
        analysis['what_to_look_for'] = ['Quality assets', 'Low leverage', 'Stable rental income']
        
        dividend_yield = info.get('dividendYield', 0) * 100 if info.get('dividendYield') else None
        payout_ratio = info.get('payoutRatio', 0) * 100 if info.get('payoutRatio') else None
        debt_to_equity = info.get('debtToEquity')
        
        analysis['metrics'] = {
            'Dividend Yield': f"{dividend_yield:.2f}%" if dividend_yield else 'N/A',
            'Payout Ratio': f"{payout_ratio:.1f}%" if payout_ratio else 'N/A',
            'Debt-to-Equity': f"{debt_to_equity:.2f}" if debt_to_equity else 'N/A',
            'P/E Ratio': f"{pe_ratio:.2f}" if pe_ratio else 'N/A'
        }
        
        score = 50
        if dividend_yield:
            if dividend_yield > 4:
                analysis['strengths'].append(f"Attractive dividend yield of {dividend_yield:.2f}%")
                score += 20
            elif dividend_yield > 3:
                analysis['strengths'].append(f"Solid dividend yield of {dividend_yield:.2f}%")
                score += 10
        
        if payout_ratio:
            if 50 < payout_ratio < 80:
                analysis['strengths'].append(f"Sustainable payout ratio of {payout_ratio:.1f}%")
                score += 15
            elif payout_ratio > 90:
                analysis['weaknesses'].append(f"High payout ratio of {payout_ratio:.1f}% - Dividend risk")
                score -= 15
        
        if debt_to_equity:
            if debt_to_equity < 100:
                analysis['strengths'].append(f"Manageable debt-to-equity of {debt_to_equity:.2f}")
                score += 15
            elif debt_to_equity > 200:
                analysis['weaknesses'].append(f"High debt-to-equity of {debt_to_equity:.2f}")
                score -= 20
        
        analysis['rating'] = max(0, min(100, score))
        
    elif sector == 'Consumer Cyclical':
        analysis['drivers'] = ['Consumer confidence', 'Disposable income', 'Inflation']
        analysis['peer_examples'] = ['AMZN', 'TSLA', 'NKE', 'MCD', 'DIS']
        analysis['what_to_look_for'] = ['Strong brands', 'Pricing power', 'Global presence']
        
        gross_margin = info.get('grossMargins', 0) * 100 if info.get('grossMargins') else None
        revenue_growth = info.get('revenueGrowth', 0) * 100 if info.get('revenueGrowth') else None
        
        analysis['metrics'] = {
            'P/E Ratio': f"{pe_ratio:.2f}" if pe_ratio else 'N/A',
            'Gross Margin': f"{gross_margin:.1f}%" if gross_margin else 'N/A',
            'Revenue Growth': f"{revenue_growth:.1f}%" if revenue_growth else 'N/A'
        }
        
        score = 50
        if gross_margin:
            if gross_margin > 40:
                analysis['strengths'].append(f"Strong gross margin of {gross_margin:.1f}% - Pricing power")
                score += 20
            elif gross_margin < 25:
                analysis['weaknesses'].append(f"Low gross margin of {gross_margin:.1f}%")
                score -= 15
        
        if revenue_growth:
            if revenue_growth > 10:
                analysis['strengths'].append(f"Solid revenue growth of {revenue_growth:.1f}%")
                score += 15
            elif revenue_growth < 0:
                analysis['weaknesses'].append(f"Negative revenue growth of {revenue_growth:.1f}%")
                score -= 20
        
        analysis['rating'] = max(0, min(100, score))
        
    elif sector == 'Consumer Defensive':
        analysis['drivers'] = ['Defensive sector - steady demand', 'Economic resilience', 'Brand loyalty']
        analysis['peer_examples'] = ['PG', 'KO', 'PEP', 'COST', 'WMT']
        analysis['what_to_look_for'] = ['Consistent earnings', 'Loyal customer base', 'Pricing resilience']
        
        revenue_growth = info.get('revenueGrowth', 0) * 100 if info.get('revenueGrowth') else None
        dividend_yield = info.get('dividendYield', 0) * 100 if info.get('dividendYield') else None
        operating_margin = info.get('operatingMargins', 0) * 100 if info.get('operatingMargins') else None
        
        analysis['metrics'] = {
            'Revenue Growth': f"{revenue_growth:.1f}%" if revenue_growth else 'N/A',
            'Dividend Yield': f"{dividend_yield:.2f}%" if dividend_yield else 'N/A',
            'Operating Margin': f"{operating_margin:.1f}%" if operating_margin else 'N/A',
            'P/E Ratio': f"{pe_ratio:.2f}" if pe_ratio else 'N/A'
        }
        
        score = 50
        if revenue_growth and revenue_growth > 3:
            analysis['strengths'].append(f"Stable revenue growth of {revenue_growth:.1f}%")
            score += 15
        
        if dividend_yield:
            if dividend_yield > 3:
                analysis['strengths'].append(f"Attractive dividend yield of {dividend_yield:.2f}%")
                score += 20
            elif dividend_yield > 2:
                analysis['strengths'].append(f"Solid dividend yield of {dividend_yield:.2f}%")
                score += 10
        
        if operating_margin and operating_margin > 15:
            analysis['strengths'].append(f"Strong operating margin of {operating_margin:.1f}%")
            score += 15
        
        analysis['rating'] = max(0, min(100, score))
        
    elif sector == 'Communication Services':
        analysis['drivers'] = ['Ad revenue', 'Subscriptions', 'Data usage', 'Competition']
        analysis['peer_examples'] = ['GOOGL', 'META', 'NFLX', 'VZ', 'T']
        analysis['what_to_look_for'] = ['Scale advantage', 'Diverse revenue streams', 'Global footprint']
        
        revenue_growth = info.get('revenueGrowth', 0) * 100 if info.get('revenueGrowth') else None
        operating_margin = info.get('operatingMargins', 0) * 100 if info.get('operatingMargins') else None
        
        analysis['metrics'] = {
            'Revenue Growth': f"{revenue_growth:.1f}%" if revenue_growth else 'N/A',
            'Operating Margin': f"{operating_margin:.1f}%" if operating_margin else 'N/A',
            'P/E Ratio': f"{pe_ratio:.2f}" if pe_ratio else 'N/A'
        }
        
        score = 50
        if revenue_growth:
            if revenue_growth > 15:
                analysis['strengths'].append(f"Strong revenue growth of {revenue_growth:.1f}%")
                score += 20
            elif revenue_growth < 5:
                analysis['weaknesses'].append(f"Slow revenue growth of {revenue_growth:.1f}%")
                score -= 15
        
        if operating_margin:
            if operating_margin > 25:
                analysis['strengths'].append(f"Excellent operating margin of {operating_margin:.1f}%")
                score += 20
            elif operating_margin < 10:
                analysis['weaknesses'].append(f"Low operating margin of {operating_margin:.1f}%")
                score -= 15
        
        analysis['rating'] = max(0, min(100, score))
        
    elif sector == 'Basic Materials':
        analysis['drivers'] = ['Commodity cycles', 'Construction demand', 'Inflation trends']
        analysis['peer_examples'] = ['DOW', 'DD', 'FCX', 'NUE', 'LIN']
        analysis['what_to_look_for'] = ['Cost leadership', 'Vertical integration', 'Low leverage']
        
        gross_margin = info.get('grossMargins', 0) * 100 if info.get('grossMargins') else None
        operating_cash_flow = info.get('operatingCashflow', 0)
        debt_to_equity = info.get('debtToEquity')
        
        analysis['metrics'] = {
            'Gross Margin': f"{gross_margin:.1f}%" if gross_margin else 'N/A',
            'Operating Cash Flow': f"${operating_cash_flow/1e9:.2f}B" if operating_cash_flow else 'N/A',
            'Debt-to-Equity': f"{debt_to_equity:.2f}" if debt_to_equity else 'N/A',
            'P/E Ratio': f"{pe_ratio:.2f}" if pe_ratio else 'N/A'
        }
        
        score = 50
        if gross_margin:
            if gross_margin > 30:
                analysis['strengths'].append(f"Strong gross margin of {gross_margin:.1f}%")
                score += 15
            elif gross_margin < 15:
                analysis['weaknesses'].append(f"Low gross margin of {gross_margin:.1f}% - Cyclical pressure")
                score -= 10
        
        if operating_cash_flow and operating_cash_flow > 1e9:
            analysis['strengths'].append("Solid operating cash flow generation")
            score += 15
        
        if debt_to_equity:
            if debt_to_equity < 50:
                analysis['strengths'].append(f"Low debt-to-equity of {debt_to_equity:.2f}")
                score += 20
            elif debt_to_equity > 100:
                analysis['weaknesses'].append(f"High debt-to-equity of {debt_to_equity:.2f}")
                score -= 15
        
        analysis['rating'] = max(0, min(100, score))
        
    elif sector == 'Utilities':
        analysis['drivers'] = ['Regulation', 'Energy demand', 'Rate adjustments']
        analysis['peer_examples'] = ['DUK', 'D', 'NEE', 'SO', 'AEP']
        analysis['what_to_look_for'] = ['Stable cash flow', 'Dividend reliability', 'Green transition initiatives']
        
        dividend_yield = info.get('dividendYield', 0) * 100 if info.get('dividendYield') else None
        payout_ratio = info.get('payoutRatio', 0) * 100 if info.get('payoutRatio') else None
        debt_to_equity = info.get('debtToEquity')
        
        analysis['metrics'] = {
            'Dividend Yield': f"{dividend_yield:.2f}%" if dividend_yield else 'N/A',
            'Payout Ratio': f"{payout_ratio:.1f}%" if payout_ratio else 'N/A',
            'Debt-to-Equity': f"{debt_to_equity:.2f}" if debt_to_equity else 'N/A',
            'P/E Ratio': f"{pe_ratio:.2f}" if pe_ratio else 'N/A'
        }
        
        score = 50
        if dividend_yield:
            if dividend_yield > 4:
                analysis['strengths'].append(f"Attractive dividend yield of {dividend_yield:.2f}%")
                score += 20
            elif dividend_yield > 3:
                analysis['strengths'].append(f"Solid dividend yield of {dividend_yield:.2f}%")
                score += 10
        
        if payout_ratio:
            if 50 < payout_ratio < 75:
                analysis['strengths'].append(f"Sustainable payout ratio of {payout_ratio:.1f}%")
                score += 15
            elif payout_ratio > 85:
                analysis['weaknesses'].append(f"High payout ratio of {payout_ratio:.1f}%")
                score -= 10
        
        if debt_to_equity:
            if debt_to_equity > 150:
                analysis['weaknesses'].append(f"High debt-to-equity of {debt_to_equity:.2f} - Capital intensive")
                score -= 5
        
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
    
    if analysis['rating'] >= 75:
        analysis['recommendation'] = "Strong Buy"
    elif analysis['rating'] >= 65:
        analysis['recommendation'] = "Buy"
    elif analysis['rating'] >= 50:
        analysis['recommendation'] = "Hold"
    elif analysis['rating'] >= 40:
        analysis['recommendation'] = "Underperform"
    else:
        analysis['recommendation'] = "Sell"
    
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
        "Magnificent 7 (Tech)": ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA'],
        "Finance": ['JPM', 'BAC', 'GS', 'WFC', 'V', 'MA', 'BRK-B'],
        "Healthcare Industry": ['JNJ', 'UNH', 'PFE', 'ABBV', 'TMO', 'ABT', 'MRK'],
        "Consumer Staples": ['WMT', 'HD', 'NKE', 'SBUX', 'MCD', 'DIS', 'COST'],
        "Energy": ['XOM', 'CVX', 'COP', 'SLB', 'EOG', 'MPC', 'PSX'],
        "Industrials": ['BA', 'CAT', 'GE', 'HON', 'UPS', 'MMM', 'DE']
    }

with st.sidebar:
    st.title("SternCurve")
    if st.button("Equities Analyzer"):
        st.session_state.page = 'analysis'
    if st.button("SternCurve Portfolio"):
        st.session_state.page = 'portfolio'
    if st.button("Discover Stocks"):
        st.session_state.page = 'discover'
    
    st.markdown("---")
    st.caption(f"Stocks in Portfolio: {len(st.session_state.portfolio)}")

if st.session_state.page == 'analysis':
    st.title("SternCurve Equities Analyzer")
    
    col1, col2 = st.columns([4, 2])
    with col1:
        default_ticker = st.session_state.get('selected_ticker', 'AAPL')
        ticker_input = st.text_input("Enter ticker", default_ticker, key="ticker_input")
        ticker = search_ticker(ticker_input)
        if 'selected_ticker' in st.session_state:
            del st.session_state.selected_ticker
    with col2:
        period = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y", "2y"], index=3)
    
    with st.spinner(f"Analyzing {ticker}..."):
        data, info, error = get_stock_data(ticker, period)
    
    if error or data is None or data.empty:
        st.error("Unable to fetch data")
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
                            name='%K'), row=2, col=1)
    
    fig.add_trace(go.Scatter(x=data.index, y=data['STOCH_D'], line=dict(color='black', width=2),
                            name='%D'), row=2, col=1)
    
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
    position = "Oversold" if current_k < 20 else "Overbought" if current_k > 80 else "Neutral"
    
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
    
    st.subheader("Current Market Position")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Stochastic %K", f"{current_k:.1f}", f"{k_momentum:+.1f}")
    col2.metric("Stochastic %D", f"{current_d:.1f}")
    col3.metric("Position", position)
    col4.metric("Combined Score", f"{combined_score:.0f}/100")
    
    st.markdown("---")
    
    st.subheader("Technical Analysis: Momentum & Trend")
    
    if position == "Oversold":
        st.error("Oversold Territory - High Priority Signal")
        st.write(f"What This Means: {ticker} is trading in oversold territory with a %K reading of {current_k:.1f}. This suggests the stock has experienced significant selling pressure and may be approaching a technical bottom.")
        st.write("")
        st.write("Investment Implications:")
        st.write("- The stock is potentially undervalued on a short-term technical basis")
        st.write("- Historical patterns suggest oversold conditions often precede rebounds")
        st.write("- Risk/reward ratio may favor buyers at this level")
        st.write("- However: Oversold can remain oversold - don't catch a falling knife")
        st.write("")
        st.write("Action Considerations:")
        st.write("- For aggressive traders: Consider scaling into a position")
        st.write("- For conservative investors: Wait for confirmation of reversal")
        st.write("- Set tight stop-losses if entering")
        st.write("- Monitor volume for signs of capitulation or accumulation")
        
    elif position == "Overbought":
        st.warning("Overbought Territory - Caution Advised")
        st.write(f"What This Means: {ticker} is trading in overbought territory with a %K reading of {current_k:.1f}. This indicates strong buying pressure but also suggests limited upside in the near term.")
        st.write("")
        st.write("Investment Implications:")
        st.write("- The rally may be overextended and due for consolidation or pullback")
        st.write("- Momentum is strong, but price may have run ahead of fundamentals")
        st.write("- Risk/reward ratio currently favors taking profits")
        st.write("- However: Strong trends can remain overbought for extended periods")
        st.write("")
        st.write("Action Considerations:")
        st.write("- For current holders: Consider taking partial profits")
        st.write("- For potential buyers: Wait for a pullback to more favorable entry levels")
        st.write("- Watch for bearish divergence")
        st.write("- Overbought + bearish crossover = strong sell signal")
        
    else:
        st.info("Neutral Range - Balanced Market Conditions")
        st.write(f"What This Means: {ticker} is trading in neutral territory with a %K reading of {current_k:.1f}. The stock is neither oversold nor overbought, suggesting balanced supply and demand.")
        st.write("")
        st.write("Investment Implications:")
        st.write("- No extreme technical signals at this time")
        st.write("- Market is in equilibrium - wait for clearer directional signals")
        st.write("- Risk/reward is unclear without additional confirmation")
        st.write("")
        st.write("Action Considerations:")
        st.write("- Wait for the stock to enter oversold or overbought territory")
        st.write("- Focus on crossover signals and momentum shifts")
        st.write("- Use this time to monitor fundamentals")
    
    st.markdown("---")
    
    st.write("Crossover Signals:")
    
    if bullish_cross:
        st.success("Bullish Crossover Detected - Buy Signal")
        st.write(f"The fast line (%K = {current_k:.1f}) crossed ABOVE the slow line (%D = {current_d:.1f})")
        signal_strength = 'Very Strong' if current_k < 30 else 'Strong' if current_k < 50 else 'Moderate'
        st.write(f"Signal Strength: {signal_strength}")
        st.write("Crossovers in oversold territory are most reliable")
    elif bearish_cross:
        st.error("Bearish Crossover Detected - Sell Signal")
        st.write(f"The fast line (%K = {current_k:.1f}) crossed BELOW the slow line (%D = {current_d:.1f})")
        signal_strength = 'Very Strong' if current_k > 70 else 'Strong' if current_k > 50 else 'Moderate'
        st.write(f"Signal Strength: {signal_strength}")
        st.write("Crossovers in overbought territory are most reliable")
    else:
        st.info("No Recent Crossover Detected")
        k_above = current_k > current_d
        st.write(f"%K is currently {'ABOVE' if k_above else 'BELOW'} %D")
    
    st.markdown("---")
    
    st.write("Momentum and Trend Analysis:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("5-Day Momentum:")
        if k_momentum > 10:
            st.success(f"+{k_momentum:.1f} - Strong Upward Momentum")
        elif k_momentum > 0:
            st.info(f"+{k_momentum:.1f} - Positive Momentum")
        elif k_momentum > -10:
            st.warning(f"{k_momentum:.1f} - Negative Momentum")
        else:
            st.error(f"{k_momentum:.1f} - Strong downward momentum")
    
    with col2:
        st.write("10-Day Trend:")
        if trend_direction == "bullish":
            st.success("Consistently Rising - Strong Uptrend")
        elif trend_direction == "bearish":
            st.error("Consistently Falling - Strong Downtrend")
        else:
            st.info("Mixed Signals - Choppy Action")
    
    st.markdown("---")
    
    st.subheader("Fundamental Investment Analysis")
    
    st.info(f"Sector Classification: **{sector}**")
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.write("**What Drives This Sector:**")
        for driver in fundamental_analysis['drivers']:
            st.write(f"• {driver}")
    
    with col2:
        if fundamental_analysis['peer_examples']:
            st.write("**Compare To (Peer Examples):**")
            st.write(", ".join(fundamental_analysis['peer_examples']))
    
    st.markdown("---")
    
    st.write("**Key Financial Metrics:**")
    
    metric_cols = st.columns(len(fundamental_analysis['metrics']))
    for idx, (metric_name, metric_value) in enumerate(fundamental_analysis['metrics'].items()):
        with metric_cols[idx]:
            st.metric(metric_name, metric_value)
    
    st.markdown("---")
    
    col_rating, col_rec = st.columns(2)
    with col_rating:
        st.metric("Fundamental Score", f"{fundamental_analysis['rating']:.0f}/100")
    with col_rec:
        if fundamental_analysis['rating'] >= 75:
            st.success(f"Rating: {fundamental_analysis['recommendation']}")
        elif fundamental_analysis['rating'] >= 65:
            st.success(f"Rating: {fundamental_analysis['recommendation']}")
        elif fundamental_analysis['rating'] >= 50:
            st.info(f"Rating: {fundamental_analysis['recommendation']}")
        elif fundamental_analysis['rating'] >= 40:
            st.warning(f"Rating: {fundamental_analysis['recommendation']}")
        else:
            st.error(f"Rating: {fundamental_analysis['recommendation']}")
    
    if fundamental_analysis['strengths']:
        st.write("**Fundamental Strengths:**")
        for strength in fundamental_analysis['strengths']:
            st.success(f"✓ {strength}")
    
    if fundamental_analysis['weaknesses']:
        st.write("**Fundamental Concerns:**")
        for weakness in fundamental_analysis['weaknesses']:
            st.warning(f"⚠ {weakness}")
    
    if fundamental_analysis['what_to_look_for']:
        st.write(f"**Investment Strategy for {sector}:**")
        st.write("Look for companies with:")
        for item in fundamental_analysis['what_to_look_for']:
            st.write(f"• {item}")
    
    st.markdown("---")
    
    st.write("Risk Assessment:")
    
    risk_factors = []
    risk_score = 0
    
    if current_k > 80:
        risk_factors.append("Overbought Condition Increases Pullback Risk")
        risk_score += 2
    if current_k < 20:
        risk_factors.append("Oversold Condition Suggests Potential Reversal")
        risk_score -= 1
    if bearish_cross:
        risk_factors.append("Recent Bearish Crossover Signals Downside")
        risk_score += 2
    if bullish_cross:
        risk_factors.append("Recent Bullish Crossover Signals Upside")
        risk_score -= 1
    
    if risk_score >= 3:
        st.error("High Risk - Multiple Warning Signals Present")
    elif risk_score >= 1:
        st.warning("Moderate Risk - Some Caution Warranted")
    else:
        st.success("Lower Risk - Technical Picture Appears Favorable")
    
    if risk_factors:
        st.write("Key Risk Factors:")
        for factor in risk_factors:
            st.write(f"- {factor}")
    
    st.markdown("---")
    st.header("Comprehensive Investment Analysis")
    
    tab1, tab2, tab3 = st.tabs(["Technical", "Fundamental", "Combined"])
    
    with tab1:
        st.subheader("Critical Technical Signal Analysis")
        
        if position == "Oversold":
            st.error("Oversold Territory - High Priority Signal")
            st.write(f"What This Means: {ticker} is trading in oversold territory with a %K reading of {current_k:.1f}. This suggests the stock has experienced significant selling pressure and may be approaching a technical bottom.")
            st.write("")
            st.write("Investment Implications:")
            st.write("- The stock is potentially undervalued on a short-term technical basis")
            st.write("- Historical patterns suggest oversold conditions often precede rebounds")
            st.write("- Risk/reward ratio may favor buyers at this level")
            st.write("- However: Oversold can remain oversold - don't catch a falling knife")
            st.write("")
            st.write("Action Considerations:")
            st.write("- For aggressive traders: Consider scaling into a position")
            st.write("- For conservative investors: Wait for confirmation of reversal")
            st.write("- Set tight stop-losses if entering")
            st.write("- Monitor volume for signs of capitulation or accumulation")
            
        elif position == "Overbought":
            st.warning("Overbought Territory - Caution Advised")
            st.write(f"What This Means: {ticker} is trading in overbought territory with a %K reading of {current_k:.1f}. This indicates strong buying pressure but also suggests limited upside in the near term.")
            st.write("")
            st.write("Investment Implications:")
            st.write("- The rally may be overextended and due for consolidation or pullback")
            st.write("- Momentum is strong, but price may have run ahead of fundamentals")
            st.write("- Risk/reward ratio currently favors taking profits")
            st.write("- However: Strong trends can remain overbought for extended periods")
            st.write("")
            st.write("Action Considerations:")
            st.write("- For current holders: Consider taking partial profits")
            st.write("- For potential buyers: Wait for a pullback to more favorable entry levels")
            st.write("- Watch for bearish divergence")
            st.write("- Overbought + bearish crossover = strong sell signal")
            
        else:
            st.info("Neutral Range - Balanced Market Conditions")
            st.write(f"What This Means: {ticker} is trading in neutral territory with a %K reading of {current_k:.1f}. The stock is neither oversold nor overbought, suggesting balanced supply and demand.")
            st.write("")
            st.write("Investment Implications:")
            st.write("- No extreme technical signals at this time")
            st.write("- Market is in equilibrium - wait for clearer directional signals")
            st.write("- Risk/reward is unclear without additional confirmation")
            st.write("")
            st.write("Action Considerations:")
            st.write("- Wait for the stock to enter oversold or overbought territory")
            st.write("- Focus on crossover signals and momentum shifts")
            st.write("- Use this time to monitor fundamentals")
        
        st.markdown("---")
        
        st.write("Crossover Signals:")
        
        if bullish_cross:
            st.success("Bullish Crossover Detected - Buy Signal")
            st.write(f"The fast line (%K = {current_k:.1f}) crossed ABOVE the slow line (%D = {current_d:.1f})")
            signal_strength = 'Very Strong' if current_k < 30 else 'Strong' if current_k < 50 else 'Moderate'
            st.write(f"Signal Strength: {signal_strength}")
            st.write("Crossovers in oversold territory are most reliable")
        elif bearish_cross:
            st.error("Bearish Crossover Detected - Sell Signal")
            st.write(f"The fast line (%K = {current_k:.1f}) crossed BELOW the slow line (%D = {current_d:.1f})")
            signal_strength = 'Very Strong' if current_k > 70 else 'Strong' if current_k > 50 else 'Moderate'
            st.write(f"Signal Strength: {signal_strength}")
            st.write("Crossovers in overbought territory are most reliable")
        else:
            st.info("No Recent Crossover Detected")
            k_above = current_k > current_d
            st.write(f"%K is currently {'ABOVE' if k_above else 'BELOW'} %D")
        
        st.markdown("---")
        
        st.write("Momentum and Trend Analysis:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("5-Day Momentum:")
            if k_momentum > 10:
                st.success(f"+{k_momentum:.1f} - Strong Upward Momentum")
            elif k_momentum > 0:
                st.info(f"+{k_momentum:.1f} - Positive Momentum")
            elif k_momentum > -10:
                st.warning(f"{k_momentum:.1f} - Negative Momentum")
            else:
                st.error(f"{k_momentum:.1f} - Strong downward momentum")
        
        with col2:
            st.write("10-Day Trend:")
            if trend_direction == "bullish":
                st.success("Consistently Rising - Strong Uptrend")
            elif trend_direction == "bearish":
                st.error("Consistently Falling - Strong Downtrend")
            else:
                st.info("Mixed Signals - Choppy Action")
        
        st.markdown("---")
        
        st.write("Risk Assessment:")
        
        risk_factors = []
        risk_score = 0
        
        if current_k > 80:
            risk_factors.append("Overbought Condition Increases Pullback Risk")
            risk_score += 2
        if current_k < 20:
            risk_factors.append("Oversold Condition Suggests Potential Reversal")
            risk_score -= 1
        if bearish_cross:
            risk_factors.append("Recent Bearish Crossover Signals Downside")
            risk_score += 2
        if bullish_cross:
            risk_factors.append("Recent Bullish Crossover Signals Upside")
            risk_score -= 1
        
        if risk_score >= 3:
            st.error("High Risk - Multiple Warning Signals Present")
        elif risk_score >= 1:
            st.warning("Moderate Risk - Some Caution Warranted")
        else:
            st.success("Lower Risk - Technical Picture Appears Favorable")
        
        if risk_factors:
            st.write("Key Risk Factors:")
            for factor in risk_factors:
                st.write(f"- {factor}")
    
    with tab2:
        st.subheader("Fundamental Valuation Analysis")
        st.info(f"Sector: {sector}")
        
        st.write("Key Financial Metrics:")
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
                st.success("Strong Fundamentals - Excellent Financial Health")
            elif fundamental_analysis['rating'] >= 60:
                st.success("Solid Fundamentals - Good Financial Metrics")
            elif fundamental_analysis['rating'] >= 50:
                st.info("Fair Fundamentals - Adequately Valued")
            elif fundamental_analysis['rating'] >= 40:
                st.warning("Weak Fundamentals - Some Concerns Present")
            else:
                st.error("Poor Fundamentals - Significant Weaknesses")
        
        st.markdown("---")
        
        if fundamental_analysis['strengths']:
            st.write("Fundamental Strengths:")
            for s in fundamental_analysis['strengths']:
                st.success(f"• {s}")
        
        if fundamental_analysis['weaknesses']:
            st.write("Fundamental Concerns:")
            for w in fundamental_analysis['weaknesses']:
                st.warning(f"• {w}")
        
        st.markdown("---")
        
        st.write("Sector-Specific Investment Considerations:")
        
        if sector == 'Financial Services':
            st.write("What Drives Financial Stocks:")
            st.write("- Interest rate environment")
            st.write("- Loan growth and credit quality")
            st.write("- Regulatory changes")
            st.write("")
            st.write("What to Look For:")
            st.write("- ROE > 15% indicates efficient capital deployment")
            st.write("- P/B ratio < 1.5 may signal undervaluation")
            st.write("- Strong risk management")
            
        elif sector == 'Technology':
            st.write("What Drives Technology Stocks:")
            st.write("- Innovation cycles and product launches")
            st.write("- Cloud adoption and AI growth")
            st.write("- Market share gains")
            st.write("")
            st.write("What to Look For:")
            st.write("- Revenue growth > 15% YoY")
            st.write("- Gross margins > 60%")
            st.write("- Positive free cash flow")
    
    with tab3:
        st.subheader("Combined Investment Recommendation")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Technical", f"{stoch_score:.0f}/100", help="Based on stochastic oscillator")
        col2.metric("Fundamental", f"{fundamental_analysis['rating']:.0f}/100", help="Based on financial metrics")
        col3.metric("Combined", f"{combined_score:.0f}/100", help="Equal weight average")
        
        st.markdown("---")
        
        st.write("Integrated Investment Thesis:")
        
        if stoch_score >= 60 and fundamental_analysis['rating'] >= 60:
            st.success("High Conviction Buy")
            st.write(f"{ticker} presents a rare alignment of both technical and fundamental factors.")
            st.write("")
            st.write("Technical Perspective: The stochastic oscillator shows favorable conditions for entry.")
            st.write("")
            st.write(f"Fundamental Perspective: The company demonstrates {fundamental_analysis['recommendation'].lower()} fundamentals with a score of {fundamental_analysis['rating']:.0f}/100.")
            st.write("")
            st.write("Combined View: When strong fundamentals align with favorable technical entry points, these setups historically produce above-average returns.")
            st.write("")
            st.write("Action: Consider this a high-probability opportunity for position sizing.")
            
        elif (stoch_score >= 60 and fundamental_analysis['rating'] >= 45) or (stoch_score >= 45 and fundamental_analysis['rating'] >= 60):
            st.info("Qualified Buy")
            
            if stoch_score > fundamental_analysis['rating']:
                st.write("Mixed Signals - Technical Leading:")
                st.write("")
                st.write("The technical setup is stronger than fundamentals.")
                st.write(f"Technical Strength: {ticker} shows favorable stochastic readings.")
                st.write(f"Fundamental Caution: Score of {fundamental_analysis['rating']:.0f}/100 suggests some concerns.")
                st.write("")
                st.write("Recommendation: Suitable for swing traders with 1-3 month holding period.")
            else:
                st.write("Mixed Signals - Fundamental Leading:")
                st.write("")
                st.write("The company quality exceeds the current technical setup.")
                st.write(f"Fundamental Strength: {ticker} demonstrates solid financial health.")
                st.write(f"Technical Caution: Current readings suggest {position.lower()} conditions.")
                st.write("")
                st.write("Recommendation: Appropriate for patient investors willing to average in.")
                
        elif stoch_score < 45 or fundamental_analysis['rating'] < 45:
            st.warning("Hold / Avoid")
            
            if stoch_score < 45 and fundamental_analysis['rating'] < 45:
                st.write("Dual Weakness Identified:")
                st.write(f"Both technical and fundamental analysis raise concerns about {ticker}.")
                st.write("")
                st.write("Recommendation: Avoid new positions. Better opportunities exist elsewhere.")
                
            elif stoch_score < 45:
                st.write("Technical Weakness Despite Strong Fundamentals:")
                st.write("")
                st.write(f"{ticker} presents a puzzle - good business, poor price action.")
                st.write("")
                st.write("Recommendation: Wait for technical confirmation before entering.")
                
            else:
                st.write("Fundamental Weakness Despite Technical Strength:")
                st.write("")
                st.write(f"{ticker} shows favorable technical setup but concerning fundamentals.")
                st.write("")
                st.write("Recommendation: Avoid unless experienced short-term trader.")
        
        else:
            st.info("Neutral / Hold")
            st.write("Signals are mixed. Consider waiting for clearer conviction.")
        
        st.markdown("---")
        
        st.write("Factor Comparison:")
        
        tech_signal = 'Bullish' if stoch_score >= 60 else 'Bearish' if stoch_score < 45 else 'Neutral'
        fund_health = 'Strong' if fundamental_analysis['rating'] >= 60 else 'Weak' if fundamental_analysis['rating'] < 45 else 'Fair'
        
        comparison_data = {
            'Factor': ['Technical Signal', 'Fundamental Health', 'Risk Level'],
            'Assessment': [
                f"{tech_signal} ({stoch_score:.0f}/100)",
                f"{fund_health} ({fundamental_analysis['rating']:.0f}/100)",
                f"{'Low' if combined_score >= 65 else 'High' if combined_score < 50 else 'Moderate'}"
            ]
        }
        
        st.table(comparison_data)
        
        st.markdown("---")
        
        st.write("Final Verdict:")
        
        if combined_score >= 70:
            st.success("Strong Buy - High Conviction")
            st.write(f"Combined score of {combined_score:.0f}/100 represents a high-quality opportunity.")
            st.write("Suggested allocation: 5-10% of portfolio for aggressive investors")
        elif combined_score >= 60:
            st.info("Buy - Moderate Conviction")
            st.write(f"Combined score of {combined_score:.0f}/100 indicates a good opportunity.")
            st.write("Suggested allocation: 2-5% of portfolio")
        elif combined_score >= 50:
            st.warning("Hold - Neutral")
            st.write(f"Combined score of {combined_score:.0f}/100 suggests no strong conviction.")
            st.write("Suggested action: Maintain existing positions")
        else:
            st.error("Avoid - Low Conviction")
            st.write(f"Combined score of {combined_score:.0f}/100 indicates significant concerns.")
            st.write("Suggested action: Avoid new positions")

elif st.session_state.page == 'portfolio':
    st.title("My Portfolio")
    
    if not st.session_state.portfolio:
        st.info("Portfolio empty")
        if st.button("Go to Analysis"):
            st.session_state.page = 'analysis'
            st.rerun()
    else:
        oversold = sum(1 for s in st.session_state.portfolio if s['position'] == 'Oversold')
        overbought = sum(1 for s in st.session_state.portfolio if s['position'] == 'Overbought')
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total", len(st.session_state.portfolio))
        col2.metric("Oversold", oversold)
        col3.metric("Overbought", overbought)
        
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
                    if st.button(f"Analyze", key=f"analyze_{stock['ticker']}"):
                        st.session_state.page = 'analysis'
                        st.session_state.selected_ticker = stock['ticker']
                        st.rerun()
                with btn2:
                    if st.button(f"Remove", key=f"remove_{stock['ticker']}"):
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
    
    if st.button(f"🔍 Analyze {selected_sector} Sector", use_container_width=True, type="primary"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        tickers = stock_categories[selected_sector]
        results = []
        
        for idx, ticker in enumerate(tickers):
            status_text.text(f"Analyzing {ticker}... ({idx + 1}/{len(tickers)})")
            progress_bar.progress((idx + 1) / len(tickers))
            
            try:
                time.sleep(0.3)
                
                stock = yf.Ticker(ticker)
                data = stock.history(period=analysis_period)
                
                if data is None or data.empty or len(data) < 14:
                    continue
                
                info = stock.info
                
                k_period = 14
                d_period = 3
                
                data['STOCH_K'], data['STOCH_D'] = calculate_stochastic(
                    data['High'], data['Low'], data['Close'], k_period, d_period
                )
                
                current_k = data['STOCH_K'].iloc[-1]
                current_d = data['STOCH_D'].iloc[-1]
                
                if pd.isna(current_k) or pd.isna(current_d):
                    continue
                
                k_momentum = current_k - data['STOCH_K'].iloc[-5] if len(data) >= 5 else 0
                recent_k = data['STOCH_K'].iloc[-10:] if len(data) >= 10 else data['STOCH_K']
                trend = "bullish" if recent_k.is_monotonic_increasing else "bearish" if recent_k.is_monotonic_decreasing else "mixed"
                
                price = data['Close'].iloc[-1]
                change = ((data['Close'].iloc[-1] / data['Close'].iloc[0]) - 1) * 100 if len(data) > 0 else 0
                
                position = "Oversold" if current_k < 20 else "Overbought" if current_k > 80 else "Neutral"
                score = calculate_stochastic_score(current_k, current_d, k_momentum, trend)
                
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
                    'bearish_cross': bearish_cross
                })
            except Exception as e:
                continue
        
        progress_bar.empty()
        status_text.empty()
        
        if results:
            st.session_state.discovery_results = results
            st.session_state.discovery_sector = selected_sector
            st.success(f"✅ Successfully analyzed {len(results)} out of {len(tickers)} stocks!")
            st.rerun()
        else:
            st.error(f"❌ Unable to fetch data for stocks in {selected_sector}.")
            st.write("Try waiting a moment and selecting a different sector.")
    
    if 'discovery_results' in st.session_state and st.session_state.discovery_results:
        results = st.session_state.discovery_results
        sector_name = st.session_state.get('discovery_sector', 'Selected Sector')
        
        st.markdown("---")
        
        st.subheader(f"📊 {sector_name} Sector Overview")
        
        oversold_count = sum(1 for r in results if r['position'] == 'Oversold')
        overbought_count = sum(1 for r in results if r['position'] == 'Overbought')
        bullish_cross_count = sum(1 for r in results if r['bullish_cross'])
        
        avg_score = sum(r['score'] for r in results) / len(results)
        avg_momentum = sum(r['momentum'] for r in results) / len(results)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Stocks Analyzed", len(results))
        col2.metric("Oversold 🟢", oversold_count)
        col3.metric("Overbought 🔴", overbought_count)
        col4.metric("Bullish Crosses", bullish_cross_count)
        col5.metric("Avg Score", f"{avg_score:.0f}/100")
        
        st.markdown("---")
        
        st.success("🌟 Top 3 Opportunities In This Sector")
        st.write("Ranked by highest stochastic score and momentum - these are the strongest signals!")
        
        top_opportunities = sorted(results, key=lambda x: (x['score'], x['momentum']), reverse=True)[:3]
        
        rank_emojis = ["🥇", "🥈", "🥉"]
        
        for idx, stock in enumerate(top_opportunities):
            strength = "Strong Buy" if stock['score'] >= 70 else "BUY" if stock['score'] >= 60 else "MODERATE BUY" if stock['score'] >= 50 else "HOLD"
            
            with st.expander(f"{rank_emojis[idx]} **#{idx+1} - {stock['ticker']}** ({stock['name']}) | Score: **{stock['score']}/100** | {strength}", expanded=True):
                col1, col2, col3, col4, col5 = st.columns(5)
                col1.metric("Price", f"${stock['price']:.2f}", f"{stock['change']:+.2f}%")
                col2.metric("Position", stock['position'])
                col3.metric("Stochastic %K", f"{stock['stoch_k']:.1f}")
                col4.metric("Momentum", f"{stock['momentum']:+.1f}")
                col5.metric("Trend", stock['trend'].title())
                
                st.markdown(f"**Why #{idx+1}:**")
                
                reasons = []
                
                if stock['score'] >= 70:
                    reasons.append(f"✅ **Exceptional Score ({stock['score']}/100)** - Among the highest in sector")
                elif stock['score'] >= 60:
                    reasons.append(f"✅ **Strong Score ({stock['score']}/100)** - Above average signals")
                else:
                    reasons.append(f"⚠️ **Moderate Score ({stock['score']}/100)** - Decent but not exceptional")
                
                if stock['position'] == 'Oversold':
                    reasons.append("✅ **Oversold Position** - Potential buying opportunity")
                elif stock['position'] == 'Overbought':
                    reasons.append("⚠️ **Overbought Position** - Caution advised")
                else:
                    reasons.append("ℹ️ **Neutral Position** - No extreme signals")
                
                if stock['momentum'] > 10:
                    reasons.append(f"✅ **Strong Positive Momentum (+{stock['momentum']:.1f})** - Accelerating upward")
                elif stock['momentum'] > 0:
                    reasons.append(f"✅ **Positive Momentum (+{stock['momentum']:.1f})**")
                else:
                    reasons.append(f"⚠️ **Negative Momentum ({stock['momentum']:.1f})**")
                
                if stock['trend'] == 'bullish':
                    reasons.append("✅ **Bullish Trend** - Consistently rising")
                elif stock['trend'] == 'bearish':
                    reasons.append("⚠️ **Bearish Trend** - Consistently falling")
                
                if stock['bullish_cross']:
                    reasons.append("🚀 **BULLISH CROSSOVER** - %K crossed above %D (buy signal!)")
                
                for reason in reasons:
                    st.markdown(f"- {reason}")
                
                st.markdown("**Investment Recommendation:**")
                
                if stock['score'] >= 70 and stock['position'] == 'Oversold':
                    st.success(f"🎯 **STRONG BUY CANDIDATE** - {stock['ticker']} shows exceptional technical strength with oversold positioning.")
                elif stock['score'] >= 60 and stock['position'] == 'Oversold':
                    st.success(f"✅ **BUY CANDIDATE** - {stock['ticker']} has strong signals and is oversold.")
                elif stock['score'] >= 60:
                    st.info(f"📊 **SOLID CHOICE** - {stock['ticker']} has good technical signals.")
                else:
                    st.info(f"⚖️ **MODERATE OPPORTUNITY** - {stock['ticker']} shows decent signals.")
                
                btn_col1, btn_col2 = st.columns(2)
                
                with btn_col1:
                    if st.button(f"📊 Full Analysis", key=f"analyze_top_{stock['ticker']}", use_container_width=True, type="primary"):
                        st.session_state.page = 'analysis'
                        st.session_state.selected_ticker = stock['ticker']
                        st.rerun()
                
                with btn_col2:
                    is_in_portfolio = any(s['ticker'] == stock['ticker'] for s in st.session_state.portfolio)
                    if not is_in_portfolio:
                        if st.button(f"⭐ Add to Portfolio", key=f"add_top_{stock['ticker']}", use_container_width=True):
                            add_to_portfolio(stock['ticker'], stock['stoch_k'], stock['stoch_d'], 
                                           stock['momentum'], stock['trend'])
                            st.success(f"Added {stock['ticker']}!")
                            st.rerun()
                    else:
                        st.success("✓ In Portfolio")
        
        st.markdown("---")
        
        st.subheader(f"📋 All Results ({len(results)} stocks)")
        
        sort_col1, sort_col2 = st.columns([2, 2])
        with sort_col1:
            sort_by = st.selectbox("Sort by", ["Score (High to Low)", "Score (Low to High)", "Momentum", "Position"], index=0)
        with sort_col2:
            position_filter = st.multiselect("Filter by Position", ["Oversold", "Neutral", "Overbought"], default=["Oversold", "Neutral", "Overbought"])
        
        filtered_results = [r for r in results if r['position'] in position_filter]
        
        if sort_by == "Score (High to Low)":
            filtered_results = sorted(filtered_results, key=lambda x: x['score'], reverse=True)
        elif sort_by == "Score (Low to High)":
            filtered_results = sorted(filtered_results, key=lambda x: x['score'])
        elif sort_by == "Momentum":
            filtered_results = sorted(filtered_results, key=lambda x: x['momentum'], reverse=True)
        elif sort_by == "Position":
            filtered_results = sorted(filtered_results, key=lambda x: x['position'])
        
        for stock in filtered_results:
            position_emoji = "🟢" if stock['position'] == 'Oversold' else "🔴" if stock['position'] == 'Overbought' else "⚪"
            
            with st.expander(f"{position_emoji} **{stock['ticker']}** - {stock['position']} | Score: {stock['score']}/100"):
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Price", f"${stock['price']:.2f}", f"{stock['change']:+.2f}%")
                col2.metric("%K", f"{stock['stoch_k']:.1f}")
                col3.metric("Momentum", f"{stock['momentum']:+.1f}")
                col4.metric("Trend", stock['trend'].title())
                
                if stock['position'] == 'Oversold':
                    st.success(f"💡 **Potential Buy:** {stock['ticker']} is oversold.")
                elif stock['position'] == 'Overbought':
                    st.warning(f"⚠️ **Caution:** {stock['ticker']} is overbought.")
                else:
                    st.info(f"ℹ️ {stock['ticker']} is in neutral territory.")
                
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
                            st.success(f"Added {stock['ticker']}!")
                            st.rerun()
                    else:
                        st.success("✓ In Portfolio")
