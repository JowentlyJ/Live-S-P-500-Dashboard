import requests
import streamlit as st


@st.cache_data(ttl=3600)
def get_market_news(api_key, category="general"):
    """
    Fetch latest market news from Finnhub.

    Categories:
    - general
    - forex
    - crypto
    - merger
    """

    if not api_key:
        return None, {"error": "Finnhub API key is missing."}

    url = "https://finnhub.io/api/v1/news"

    params = {
        "category": category,
        "token": api_key
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

    except requests.exceptions.RequestException as error:
        return None, {"error": str(error)}

    if not isinstance(data, list):
        return None, data

    cleaned_news = []

    for article in data:
        cleaned_news.append({
            "headline": article.get("headline", "No headline available"),
            "summary": article.get("summary", "No summary available"),
            "source": article.get("source", "Unknown source"),
            "url": article.get("url"),
            "image": article.get("image"),
            "datetime": article.get("datetime"),
            "category": article.get("category", category)
        })

    return cleaned_news, None


@st.cache_data(ttl=3600)
def get_company_news(symbol, api_key, from_date, to_date):
    """
    Fetch company-specific news from Finnhub.

    Example:
    get_company_news("NVDA", FINNHUB_KEY, "2026-06-01", "2026-06-18")
    """

    if not api_key:
        return None, {"error": "Finnhub API key is missing."}

    url = "https://finnhub.io/api/v1/company-news"

    params = {
        "symbol": symbol,
        "from": from_date,
        "to": to_date,
        "token": api_key
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

    except requests.exceptions.RequestException as error:
        return None, {"error": str(error)}

    if not isinstance(data, list):
        return None, data

    cleaned_news = []

    for article in data:
        cleaned_news.append({
            "headline": article.get("headline", "No headline available"),
            "summary": article.get("summary", "No summary available"),
            "source": article.get("source", "Unknown source"),
            "url": article.get("url"),
            "image": article.get("image"),
            "datetime": article.get("datetime"),
            "related": article.get("related", symbol)
        })

    return cleaned_news, None


@st.cache_data(ttl=300)
def get_latest_quote(symbol, api_key):
    """
    Fetch latest quote data from Finnhub.

    Returned values:
    c  = current/latest price
    o  = open price
    h  = high price
    l  = low price
    pc = previous close
    """

    if not api_key:
        return None, {"error": "Finnhub API key is missing."}

    url = "https://finnhub.io/api/v1/quote"

    params = {
        "symbol": symbol,
        "token": api_key
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

    except requests.exceptions.RequestException as error:
        return None, {"error": str(error)}

    if not data or data.get("c", 0) == 0:
        return None, data

    quote = {
        "symbol": symbol,
        "price": data.get("c"),
        "open": data.get("o"),
        "high": data.get("h"),
        "low": data.get("l"),
        "previous_close": data.get("pc")
    }

    return quote, None