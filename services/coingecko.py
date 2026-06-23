import requests
import pandas as pd
import streamlit as st


@st.cache_data(ttl=300)
def get_crypto_price(coin_id, api_key=None):
    """
    Fetch current crypto price data from CoinGecko.

    Example coin_id values:
    - bitcoin
    - ethereum
    - solana
    - ripple
    - cardano
    """

    url = "https://api.coingecko.com/api/v3/simple/price"

    headers = {}
    if api_key:
        headers["x-cg-demo-api-key"] = api_key

    params = {
        "ids": coin_id,
        "vs_currencies": "usd",
        "include_market_cap": "true",
        "include_24hr_vol": "true",
        "include_24hr_change": "true"
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

    except requests.exceptions.RequestException as error:
        return None, {"error": str(error)}

    if coin_id not in data:
        return None, data

    coin = data[coin_id]

    price = coin.get("usd")

    if price is None:
        return None, {"error": f"Price data unavailable for {coin_id}. Try again shortly."}

    return {
        "id": coin_id,
        "symbol": coin_id.upper(),
        "asset_type": "Crypto",
        "price": price,
        "market_cap": coin.get("usd_market_cap") or 0.0,
        "volume_24h": coin.get("usd_24h_vol") or 0.0,
        "change_24h": coin.get("usd_24h_change") or 0.0
    }, None


@st.cache_data(ttl=3600)
def get_crypto_history(coin_id, days=30, api_key=None):
    """
    Fetch historical crypto price data from CoinGecko.

    The returned history is used for line charts.
    """

    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"

    headers = {}
    if api_key:
        headers["x-cg-demo-api-key"] = api_key

    params = {
        "vs_currency": "usd",
        "days": days
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

    except requests.exceptions.RequestException as error:
        return None, {"error": str(error)}

    if "prices" not in data:
        return None, data

    history = []

    for timestamp, price in data["prices"]:
        history.append({
            "date": pd.to_datetime(timestamp, unit="ms"),
            "price": float(price)
        })

    return history, None