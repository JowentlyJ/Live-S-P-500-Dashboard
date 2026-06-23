# Live S&P 500 Dashboard

### Live Demo:https://live-s-p-500-dashboard-affcjvlg5dncfy2nxcwe8i.streamlit.app/
A Python-based stock market dashboard that displays live S&P 500 market data using the Alpha Vantage API. The project is designed to provide a simple and clear overview of stock market information, making it easier to track financial data in one place.

## Features

* Fetches live stock market data from Alpha Vantage
* Displays S&P 500-related market information
* Clean project structure with separated service logic
* Easy to configure with an API key
* Suitable as a learning project for Python, APIs, and financial dashboards

## Tech Stack

* Python
* Alpha Vantage API
* Git / GitHub

## Project Structure

```text
Live-S-P-500-Dashboard/
│
├── services/
│   ├── __init__.py
│   └── alpha_vantage.py
│
├── .gitignore
├── README.md
└── main.py
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/JowentlyJ/Live-S-P-500-Dashboard.git
```

Then go into the project folder:

```bash
cd Live-S-P-500-Dashboard
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

For macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

If the project has a `requirements.txt` file, run:

```bash
pip install -r requirements.txt
```

If not, install the required packages manually depending on what the project uses.

Example:

```bash
pip install requests python-dotenv
```

### 4. Set up your Alpha Vantage API key

Create a `.env` file in the root of the project:

```text
ALPHA_VANTAGE_API_KEY=your_api_key_here
```

You can get an API key from Alpha Vantage.

### 5. Run the project

```bash
python main.py
```

## Environment Variables

| Variable | Description |
| -------- | ----------- |
| `ALPHA_VANTAGE_API_KEY` | Your personal Alpha Vantage API key for stock and ETF data |
| `COINGECKO_API_KEY` | Your CoinGecko API key for cryptocurrency price and history data |
| `FINNHUB_API_KEY` | Your Finnhub API key for market news |

## Notes

* Do not commit your `.env` file to GitHub.
* Make sure `.env` is included in your `.gitignore`.
* Alpha Vantage has request limits depending on your API plan.

## Future Improvements


## Author

Created by [JowentlyJ](https://github.com/JowentlyJ)

## License

This project is open source and available under the MIT License.
