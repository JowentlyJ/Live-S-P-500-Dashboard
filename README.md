# Personal Market Dashboard

A live, interactive financial dashboard built with Python and Streamlit. It combines three real-world APIs to display stock and ETF data, cryptocurrency prices, and the latest market news — all visualized with Plotly charts.

---

## Features

### Stocks & ETFs
- Live price metrics: current price, open, high, low, and trading volume
- Interactive candlestick price chart (Plotly)
- Four analysis views: trend, volume comparison, volume vs price movement (with OLS trendline), and correlation heatmap
- Expandable historical data table

### Crypto
- Live price, 24-hour change percentage, and 24-hour trading volume
- Four analysis views: price trend with 7-period rolling average, price change comparison, price vs daily change scatter, and correlation heatmap
- Expandable historical data table

### Latest Market News
- Real-time market news from Finnhub
- Filter by category: general, forex, crypto, or merger
- Each article shows headline, source, publish date and time, summary, and a link to the full article
- Raw HTML stripped from summaries for clean display

---

## APIs Used

| API | Purpose | Free Tier |
|---|---|---|
| [Alpha Vantage](https://www.alphavantage.co/) | Daily stock and ETF prices | 25 requests/day |
| [CoinGecko](https://www.coingecko.com/en/api) | Crypto prices and history | 30 calls/min (demo key) |
| [Finnhub](https://finnhub.io/) | Market news feed | 60 calls/min |

---

## How to Run Locally

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Mac / Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API keys

Create a `.env` file in the project root:

```
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
COINGECKO_API_KEY=your_coingecko_demo_key_here
FINNHUB_API_KEY=your_finnhub_key_here
```

Get free API keys here:
- Alpha Vantage: https://www.alphavantage.co/support/#api-key
- CoinGecko: https://www.coingecko.com/en/api/pricing (Demo plan)
- Finnhub: https://finnhub.io/register

### 5. Run the app

```bash
streamlit run app.py
```

The dashboard opens automatically in your browser at `http://localhost:8501`.

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `ALPHA_VANTAGE_API_KEY` | Yes | Used for stocks and ETF data |
| `COINGECKO_API_KEY` | No | CoinGecko works without a key, but a demo key raises the rate limit |
| `FINNHUB_API_KEY` | Yes | Required for the market news page |

**Note:** The `.env` file is listed in `.gitignore` and will never be committed.

---

## Project Structure

```
├── app.py                  # Main Streamlit dashboard
├── requirements.txt        # Python dependencies
├── .env                    # API keys (not committed)
├── .gitignore
└── services/
    ├── alpha_vantage.py    # Alpha Vantage API integration
    ├── coingecko.py        # CoinGecko API integration
    └── finnhub.py          # Finnhub API integration
```

---

## What I Learned

- **Multi-API integration:** Connecting three different REST APIs with different authentication methods, response formats, and rate limits inside a single application.
- **Streamlit session state:** Using `st.session_state` to build sidebar navigation that feels like a multi-page app without page reloads.
- **Plotly for financial charts:** Building candlestick charts, OLS scatter trendlines, and correlation heatmaps using `plotly.graph_objects` and `plotly.express`.
- **API response caching:** Using `@st.cache_data` with per-endpoint TTLs to avoid hitting rate limits and keep the dashboard responsive.
- **Defensive error handling:** Wrapping all API calls in `try/except` blocks so network failures and missing data never crash the UI — instead, they show user-friendly messages.
- **Data processing with Pandas:** Computing derived columns (daily change %, rolling averages, price range) for richer analysis views.
- **Environment variable security:** Keeping all API keys in `.env`, loading them with `python-dotenv`, and ensuring `.env` is excluded from version control.

---

## Future Improvements

- **Watchlist:** Let the user type in any stock ticker, not just the preset list
- **Company news:** Show Finnhub company-specific news alongside the selected stock chart
- **Live quote overlay:** Add real-time intraday price on top of the end-of-day candlestick chart
- **Moving average overlays:** Add 20-day and 50-day moving averages to the candlestick chart
- **Portfolio tracker:** Let the user input how many shares they own and calculate current portfolio value
- **Export to CSV:** Add a download button for historical data tables
- **Mock data fallback:** Show sample data when an API is unavailable or rate-limited
- **Daily market brief card:** An auto-generated text summary at the top of the page (biggest mover, volume spike alert)
