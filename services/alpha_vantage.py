import requests
import streamlit as st


@st.cache_data(ttl=3600)
def get_stock_data(symbol="SPY", api_key=None):
    url = "https://www.alphavantage.co/query"

    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": api_key
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

    except requests.exceptions.RequestException as error:
        return None, {"error": str(error)}

    time_series_key = "Time Series (Daily)"

    if time_series_key not in data:
        return None, data

    time_series = data[time_series_key]
    latest_date = list(time_series.keys())[0]
    latest_data = time_series[latest_date]

    history = []

    for date, values in time_series.items():
        history.append({
            "date": date,
            "open": float(values["1. open"]),
            "high": float(values["2. high"]),
            "low": float(values["3. low"]),
            "close": float(values["4. close"]),
            "volume": int(values["5. volume"])
        })

    stock_data = {
        "symbol": symbol,
        "asset_type": "Stock / ETF",
        "date": latest_date,
        "price": float(latest_data["4. close"]),
        "open": float(latest_data["1. open"]),
        "high": float(latest_data["2. high"]),
        "low": float(latest_data["3. low"]),
        "volume": int(latest_data["5. volume"]),
        "history": history
    }

    return stock_data, None
