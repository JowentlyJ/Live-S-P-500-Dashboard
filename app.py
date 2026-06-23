import os
import re
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from dotenv import load_dotenv

from services.alpha_vantage import get_stock_data
from services.coingecko import get_crypto_price, get_crypto_history
from services.finnhub import get_market_news


# ==============================
# Page config
# ==============================
st.set_page_config(
    page_title="Personal Market Dashboard",
    page_icon="📈",
    layout="wide"
)


#=================

st.markdown(
    """
    <style>
    section[data-testid="stSidebar"] div.stButton > button {
        width: 100%;
        height: 48px;
        justify-content: flex-start;
        text-align: left;
        border-radius: 6px;
        border: 1px solid #2f3b52;
        background-color: #262936;
        color: white;
        font-weight: 600;
    }

    section[data-testid="stSidebar"] div.stButton > button:hover {
        border: 1px solid #3b82f6;
        background-color: #1f2a44;
        color: white;
    }

    section[data-testid="stSidebar"] div.stButton > button:focus {
        border: 1px solid #3b82f6;
        background-color: #1e3a8a;
        color: white;
        box-shadow: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==============================
# Load environment variables
# ==============================
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

ALPHA_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
COINGECKO_KEY = os.getenv("COINGECKO_API_KEY")
FINNHUB_KEY = os.getenv("FINNHUB_API_KEY")


# ==============================
# Helper functions
# ==============================
def show_plotly_line_chart(
    dataframe,
    x_column,
    y_column,
    title,
    x_label,
    y_label,
    text_column=None
):
    fig = px.line(
        dataframe,
        x=x_column,
        y=y_column,
        text=text_column,
        markers=True,
        title=title
    )

    fig.update_traces(
        textposition="bottom right"
    )

    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label,
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)


def show_plotly_bar_chart(
    dataframe,
    x_column,
    y_column,
    title,
    x_label,
    y_label
):
    fig = px.bar(
        dataframe,
        x=x_column,
        y=y_column,
        title=title,
        text_auto=True
    )

    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label,
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)


def show_plotly_scatter_chart(
    dataframe,
    x_column,
    y_column,
    title,
    x_label,
    y_label,
    trendline=True
):
    fig = px.scatter(
        dataframe,
        x=x_column,
        y=y_column,
        title=title,
        trendline="ols" if trendline else None
    )

    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label,
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)


def show_plotly_heatmap(dataframe, title):
    numeric_df = dataframe.select_dtypes(include="number")
    correlation = numeric_df.corr()

    fig = px.imshow(
        correlation,
        text_auto=True,
        aspect="auto",
        title=title
    )

    fig.update_layout(
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

def clean_html(raw_text):
    if not raw_text:
        return ""

    clean_text = re.sub(r"<.*?>", "", raw_text)
    clean_text = clean_text.replace("&amp;", "&")
    clean_text = clean_text.replace("&quot;", '"')
    clean_text = clean_text.replace("&#39;", "'")
    clean_text = clean_text.replace("&lt;", "<")
    clean_text = clean_text.replace("&gt;", ">")

    return clean_text.strip()


# ==============================
# Main page
# ==============================
st.title("📈 Personal Market Dashboard")

st.write(
    "This dashboard combines multiple APIs to provide a personalized market overview. "
    "Alpha Vantage is used for stock and ETF data, CoinGecko is used for cryptocurrency data, "
    "and Finnhub is used for market news. Plotly is used for all charts and visual analysis."
)

# ==============================
# Sidebar button navigation
# ==============================
st.sidebar.markdown("### Market Views")

if "page" not in st.session_state:
    st.session_state.page = "Stocks / ETFs"

if st.sidebar.button("📈 Stocks & ETFs", use_container_width=True):
    st.session_state.page = "Stocks / ETFs"

if st.sidebar.button("🪙 Crypto", use_container_width=True):
    st.session_state.page = "Crypto"

if st.sidebar.button("📰 Latest Market News", use_container_width=True):
    st.session_state.page = "Latest Market News"

page = st.session_state.page

# ==============================
# Stocks / ETFs Section
# ==============================
if page == "Stocks / ETFs":

    if not ALPHA_KEY:
        st.error("Alpha Vantage API key is missing. Add it to your .env file.")
        st.stop()

    symbol = st.sidebar.selectbox(
        "Choose stock or ETF",
        ["SPY", "QQQ", "DIA", "NVDA", "AAPL", "MSFT", "TSLA"]
    )

    asset, error = get_stock_data(symbol, ALPHA_KEY)

    if error:
        st.error("Could not fetch stock data.")
        st.write(error)
        st.stop()

    st.subheader(f"{asset['symbol']} — {asset.get('asset_type', 'Stock / ETF')}")
    st.caption(f"Latest completed trading day: {asset['date']}")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Price", f"${asset['price']:.2f}")
    col2.metric("Open", f"${asset['open']:.2f}")
    col3.metric("High", f"${asset['high']:.2f}")
    col4.metric("Low", f"${asset['low']:.2f}")

    st.metric("Volume", f"{asset['volume']:,} shares traded")

    history_df = pd.DataFrame(asset["history"])
    history_df["date"] = pd.to_datetime(history_df["date"])
    history_df = history_df.sort_values("date")

    history_df["daily_change"] = history_df["close"] - history_df["open"]
    history_df["daily_change_percent"] = (
        (history_df["close"] - history_df["open"]) / history_df["open"]
    ) * 100
    history_df["price_range"] = history_df["high"] - history_df["low"]

    # ==============================
    # Candlestick chart
    # ==============================
    st.subheader("Candlestick Price Chart")

    candle_fig = go.Figure(
        data=[
            go.Candlestick(
                x=history_df["date"],
                open=history_df["open"],
                high=history_df["high"],
                low=history_df["low"],
                close=history_df["close"],
                name=asset["symbol"]
            )
        ]
    )

    candle_fig.update_layout(
        title=f"{asset['symbol']} Price Movement",
        xaxis_title="Date",
        yaxis_title="Price in USD",
        height=600,
        xaxis_rangeslider_visible=False
    )

    st.plotly_chart(candle_fig, use_container_width=True)

    # ==============================
    # Analysis section
    # ==============================
    st.subheader("Market Data Analysis")

    chart_choice = st.selectbox(
        "Choose analysis chart",
        [
            "Trend analysis",
            "Volume comparison",
            "Volume vs price movement",
            "Correlation heatmap"
        ]
    )

    if chart_choice == "Trend analysis":
        trend_df = history_df.tail(30).copy()
        trend_df["label"] = trend_df["date"].dt.strftime("%b %d")

        show_plotly_line_chart(
            dataframe=trend_df,
            x_column="date",
            y_column="close",
            title=f"{asset['symbol']} Closing Price Trend — Last 30 Trading Days",
            x_label="Date",
            y_label="Close Price in USD",
            text_column="label"
        )

        st.info(
            "This Plotly line chart shows the closing price trend over time. "
            "It helps reveal whether the selected stock or ETF is moving upward, downward, or sideways."
        )

    elif chart_choice == "Volume comparison":
        recent_volume_df = history_df.tail(20).copy()
        recent_volume_df["date_label"] = recent_volume_df["date"].dt.strftime("%b %d")

        show_plotly_bar_chart(
            dataframe=recent_volume_df,
            x_column="date_label",
            y_column="volume",
            title=f"{asset['symbol']} Trading Volume — Last 20 Trading Days",
            x_label="Date",
            y_label="Trading Volume"
        )

        st.info(
            "This Plotly bar chart compares recent trading volume. Higher volume can indicate "
            "stronger market attention or increased buying and selling activity."
        )

    elif chart_choice == "Volume vs price movement":
        clean_df = history_df.dropna().copy()

        show_plotly_scatter_chart(
            dataframe=clean_df,
            x_column="volume",
            y_column="daily_change_percent",
            title=f"{asset['symbol']} Volume vs Daily Price Change %",
            x_label="Trading Volume",
            y_label="Daily Change %"
        )

        correlation = clean_df["volume"].corr(clean_df["daily_change_percent"])

        st.metric(
            "Correlation between volume and daily change %",
            f"{correlation:.2f}"
        )

        st.info(
            "This Plotly scatter plot compares trading volume with daily price movement. "
            "The trendline helps show whether higher volume is related to stronger positive or negative price changes."
        )

    elif chart_choice == "Correlation heatmap":
        correlation_df = history_df[
            [
                "open",
                "high",
                "low",
                "close",
                "volume",
                "daily_change",
                "daily_change_percent",
                "price_range"
            ]
        ].dropna()

        show_plotly_heatmap(
            dataframe=correlation_df,
            title=f"{asset['symbol']} Correlation Heatmap"
        )

        st.info(
            "This Plotly heatmap shows how strongly different numerical market values relate to each other. "
            "Values close to 1 mean a strong positive relationship, values close to -1 mean a strong negative relationship, "
            "and values near 0 mean weak or no relationship."
        )

    with st.expander("View historical stock / ETF data"):
        st.dataframe(
            history_df.sort_values("date", ascending=False),
            use_container_width=True,
            hide_index=True
        )


# ==============================
# Crypto Section
# ==============================
elif page == "Crypto":

    coin_id = st.sidebar.selectbox(
        "Choose crypto",
        ["bitcoin", "ethereum", "solana", "ripple", "cardano"]
    )

    crypto, error = get_crypto_price(coin_id, COINGECKO_KEY)

    if error:
        st.error("Could not fetch crypto data.")
        st.write(error)
        st.stop()

    crypto_history, history_error = get_crypto_history(
        coin_id,
        days=30,
        api_key=COINGECKO_KEY
    )

    st.subheader(f"{crypto['symbol']} — {crypto['asset_type']}")

    st.info(
        "Crypto markets trade 24/7, unlike stocks and ETFs, which follow market opening hours."
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Price", f"${crypto['price']:,.2f}")
    col2.metric("24h Change", f"{crypto['change_24h']:.2f}%")
    col3.metric("24h Volume", f"${crypto['volume_24h']:,.0f}")

    if crypto_history:
        history_df = pd.DataFrame(crypto_history)
        history_df["date"] = pd.to_datetime(history_df["date"])
        history_df = history_df.sort_values("date")

        history_df["price_change"] = history_df["price"].diff()
        history_df["price_change_percent"] = history_df["price"].pct_change() * 100
        history_df["rolling_average"] = history_df["price"].rolling(window=7).mean()

        st.subheader("Crypto Analysis")

        crypto_chart_choice = st.selectbox(
            "Choose crypto analysis chart",
            [
                "Trend analysis",
                "Price change comparison",
                "Price vs daily change",
                "Correlation heatmap"
            ]
        )

        if crypto_chart_choice == "Trend analysis":
            trend_df = history_df.copy()

            trend_fig = px.line(
                trend_df,
                x="date",
                y=["price", "rolling_average"],
                markers=True,
                title=f"{crypto['symbol']} Price Trend",
                labels={
                    "date": "Date",
                    "value": "Price in USD",
                    "variable": "Metric"
                }
            )

            trend_fig.update_layout(
                height=500
            )

            st.plotly_chart(trend_fig, use_container_width=True)

            st.info(
                "This Plotly line chart shows the crypto price trend together with a 7-period rolling average. "
                "The rolling average smooths short-term movement and makes the trend easier to understand."
            )

        elif crypto_chart_choice == "Price change comparison":
            recent_crypto_df = history_df.tail(20).copy()
            recent_crypto_df["date_label"] = recent_crypto_df["date"].dt.strftime("%b %d")

            show_plotly_bar_chart(
                dataframe=recent_crypto_df,
                x_column="date_label",
                y_column="price_change_percent",
                title=f"{crypto['symbol']} Price Change % — Recent Data Points",
                x_label="Date",
                y_label="Price Change %"
            )

            st.info(
                "This Plotly bar chart compares recent percentage changes in price. "
                "It helps identify which days had the strongest movement."
            )

        elif crypto_chart_choice == "Price vs daily change":
            clean_df = history_df.dropna().copy()

            show_plotly_scatter_chart(
                dataframe=clean_df,
                x_column="price",
                y_column="price_change_percent",
                title=f"{crypto['symbol']} Price vs Price Change %",
                x_label="Price in USD",
                y_label="Price Change %"
            )

            correlation = clean_df["price"].corr(clean_df["price_change_percent"])

            st.metric(
                "Correlation between price and price change %",
                f"{correlation:.2f}"
            )

            st.info(
                "This Plotly scatter plot compares the crypto price level with percentage price movement. "
                "It helps show whether larger movements happen more often at certain price levels."
            )

        elif crypto_chart_choice == "Correlation heatmap":
            correlation_df = history_df[
                [
                    "price",
                    "price_change",
                    "price_change_percent",
                    "rolling_average"
                ]
            ].dropna()

            show_plotly_heatmap(
                dataframe=correlation_df,
                title=f"{crypto['symbol']} Correlation Heatmap"
            )

            st.info(
                "This Plotly heatmap shows how crypto price, price changes, and rolling averages relate to each other."
            )

        with st.expander("View historical crypto data"):
            st.dataframe(
                history_df.sort_values("date", ascending=False),
                use_container_width=True,
                hide_index=True
            )

    elif history_error:
        st.error("Could not fetch crypto history.")
        st.write(history_error)


# ==============================
# Market News Section
# ==============================
elif page == "Latest Market News":

    st.subheader("Latest Market News")

    if not FINNHUB_KEY:
        st.warning(
            "Finnhub API key is missing. Add FINNHUB_API_KEY to your .env file to show market news."
        )

    else:
        news_category = st.selectbox(
            "News category",
            ["general", "forex", "crypto", "merger"],
            index=0
        )

        news_items, news_error = get_market_news(FINNHUB_KEY, news_category)

        if news_error:
            st.error("Could not fetch market news.")
            st.write(news_error)

        elif news_items:
            for article in news_items[:5]:
                st.markdown(f"### {clean_html(article.get('headline', 'No headline available'))}")

                source = article.get("source", "Unknown source")
                timestamp = article.get("datetime")

                if timestamp:
                    published = datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%b %d, %Y · %H:%M UTC")
                    st.caption(f"Source: {source}  ·  Published: {published}")
                else:
                    st.caption(f"Source: {source}")

                summary = clean_html(article.get("summary", ""))

                if summary:
                    st.write(summary)

                if article.get("url"):
                    st.markdown(f"[Read full article]({article['url']})")

                st.divider()

        else:
            st.info("No market news available.")