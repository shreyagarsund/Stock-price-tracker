# =============================================================
#   STOCKS — Stock Price Tracker
#   stocks.py  |  Single-file application
#   Run:  python stocks.py
#   Requires: pip install yfinance matplotlib pandas numpy openpyxl
# =============================================================

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.gridspec as gridspec
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import threading
import os

try:
    import openpyxl
    EXCEL_AVAILABLE = True
except ImportError:
    EXCEL_AVAILABLE = False

# =============================================================
# =============================================================
#  SYMBOL DIRECTORY  (used for autocomplete in frontend)
# =============================================================

# Comprehensive list of popular symbols: NSE India (.NS), NYSE, NASDAQ, BSE (.BO)
SYMBOL_LIST = [
    # ── US — NASDAQ ───────────────────────────────────────────
    ("AAPL",   "Apple Inc."),
    ("MSFT",   "Microsoft Corporation"),
    ("GOOGL",  "Alphabet Inc. (Class A)"),
    ("GOOG",   "Alphabet Inc. (Class C)"),
    ("AMZN",   "Amazon.com Inc."),
    ("META",   "Meta Platforms Inc."),
    ("NVDA",   "NVIDIA Corporation"),
    ("TSLA",   "Tesla Inc."),
    ("NFLX",   "Netflix Inc."),
    ("ADBE",   "Adobe Inc."),
    ("AMD",    "Advanced Micro Devices"),
    ("INTC",   "Intel Corporation"),
    ("CSCO",   "Cisco Systems"),
    ("QCOM",   "Qualcomm Inc."),
    ("AVGO",   "Broadcom Inc."),
    ("TXN",    "Texas Instruments"),
    ("AMAT",   "Applied Materials"),
    ("MU",     "Micron Technology"),
    ("LRCX",   "Lam Research"),
    ("KLAC",   "KLA Corporation"),
    ("ASML",   "ASML Holding"),
    ("MRVL",   "Marvell Technology"),
    ("SNPS",   "Synopsys Inc."),
    ("CDNS",   "Cadence Design"),
    ("PANW",   "Palo Alto Networks"),
    ("CRWD",   "CrowdStrike Holdings"),
    ("ZS",     "Zscaler Inc."),
    ("OKTA",   "Okta Inc."),
    ("NET",    "Cloudflare Inc."),
    ("DDOG",   "Datadog Inc."),
    ("SNOW",   "Snowflake Inc."),
    ("PLTR",   "Palantir Technologies"),
    ("PATH",   "UiPath Inc."),
    ("AI",     "C3.ai Inc."),
    ("COIN",   "Coinbase Global"),
    ("PYPL",   "PayPal Holdings"),
    ("SQ",     "Block Inc."),
    ("SHOP",   "Shopify Inc."),
    ("UBER",   "Uber Technologies"),
    ("LYFT",   "Lyft Inc."),
    ("ABNB",   "Airbnb Inc."),
    ("DASH",   "DoorDash Inc."),
    ("RBLX",   "Roblox Corporation"),
    ("SPOT",   "Spotify Technology"),
    ("PINS",   "Pinterest Inc."),
    ("SNAP",   "Snap Inc."),
    ("TWTR",   "Twitter / X"),
    ("ZOOM",   "Zoom Video"),
    ("ZM",     "Zoom Video Comm."),
    ("DOCU",   "DocuSign Inc."),
    ("TEAM",   "Atlassian Corporation"),
    ("WDAY",   "Workday Inc."),
    ("CRM",    "Salesforce Inc."),
    ("NOW",    "ServiceNow Inc."),
    ("ORCL",   "Oracle Corporation"),
    ("IBM",    "IBM Corporation"),
    ("HPQ",    "HP Inc."),
    ("HPE",    "Hewlett Packard Enterprise"),
    ("DELL",   "Dell Technologies"),
    ("ACN",    "Accenture PLC"),
    # ── US — NYSE ─────────────────────────────────────────────
    ("JPM",    "JPMorgan Chase"),
    ("BAC",    "Bank of America"),
    ("WFC",    "Wells Fargo"),
    ("C",      "Citigroup Inc."),
    ("GS",     "Goldman Sachs"),
    ("MS",     "Morgan Stanley"),
    ("BLK",    "BlackRock Inc."),
    ("AXP",    "American Express"),
    ("V",      "Visa Inc."),
    ("MA",     "Mastercard Inc."),
    ("BRK-B",  "Berkshire Hathaway B"),
    ("BRK-A",  "Berkshire Hathaway A"),
    ("UNH",    "UnitedHealth Group"),
    ("JNJ",    "Johnson & Johnson"),
    ("PFE",    "Pfizer Inc."),
    ("MRK",    "Merck & Co."),
    ("ABBV",   "AbbVie Inc."),
    ("LLY",    "Eli Lilly"),
    ("BMY",    "Bristol-Myers Squibb"),
    ("AMGN",   "Amgen Inc."),
    ("GILD",   "Gilead Sciences"),
    ("CVS",    "CVS Health"),
    ("MCK",    "McKesson Corporation"),
    ("ABT",    "Abbott Laboratories"),
    ("MDT",    "Medtronic PLC"),
    ("SYK",    "Stryker Corporation"),
    ("BSX",    "Boston Scientific"),
    ("ELV",    "Elevance Health"),
    ("CI",     "Cigna Group"),
    ("HUM",    "Humana Inc."),
    ("XOM",    "ExxonMobil"),
    ("CVX",    "Chevron Corporation"),
    ("COP",    "ConocoPhillips"),
    ("EOG",    "EOG Resources"),
    ("SLB",    "SLB (Schlumberger)"),
    ("HAL",    "Halliburton"),
    ("KO",     "Coca-Cola Co."),
    ("PEP",    "PepsiCo Inc."),
    ("MCD",    "McDonald's Corp."),
    ("SBUX",   "Starbucks Corp."),
    ("YUM",    "Yum! Brands"),
    ("CMG",    "Chipotle Mexican Grill"),
    ("DPZ",    "Domino's Pizza"),
    ("WMT",    "Walmart Inc."),
    ("TGT",    "Target Corporation"),
    ("COST",   "Costco Wholesale"),
    ("HD",     "Home Depot"),
    ("LOW",    "Lowe's Companies"),
    ("NKE",    "Nike Inc."),
    ("PG",     "Procter & Gamble"),
    ("CL",     "Colgate-Palmolive"),
    ("GE",     "GE Aerospace"),
    ("HON",    "Honeywell International"),
    ("MMM",    "3M Company"),
    ("CAT",    "Caterpillar Inc."),
    ("DE",     "Deere & Company"),
    ("BA",     "Boeing Company"),
    ("RTX",    "RTX Corporation"),
    ("LMT",    "Lockheed Martin"),
    ("NOC",    "Northrop Grumman"),
    ("GD",     "General Dynamics"),
    ("UPS",    "United Parcel Service"),
    ("FDX",    "FedEx Corporation"),
    ("DAL",    "Delta Air Lines"),
    ("UAL",    "United Airlines"),
    ("AAL",    "American Airlines"),
    ("LUV",    "Southwest Airlines"),
    ("T",      "AT&T Inc."),
    ("VZ",     "Verizon Communications"),
    ("TMUS",   "T-Mobile US"),
    ("NEE",    "NextEra Energy"),
    ("DUK",    "Duke Energy"),
    ("SO",     "Southern Company"),
    ("D",      "Dominion Energy"),
    ("AMT",    "American Tower"),
    ("PLD",    "Prologis Inc."),
    ("SPG",    "Simon Property Group"),
    ("O",      "Realty Income"),
    ("DIS",    "Walt Disney Co."),
    ("CMCSA",  "Comcast Corporation"),
    ("CHTR",   "Charter Communications"),
    ("WBD",    "Warner Bros. Discovery"),
    ("PARA",   "Paramount Global"),
    ("F",      "Ford Motor Company"),
    ("GM",     "General Motors"),
    # ── India — NSE (.NS) ─────────────────────────────────────
    ("TCS.NS",       "Tata Consultancy Services"),
    ("INFY.NS",      "Infosys Limited"),
    ("WIPRO.NS",     "Wipro Limited"),
    ("HCLTECH.NS",   "HCL Technologies"),
    ("TECHM.NS",     "Tech Mahindra"),
    ("MPHASIS.NS",   "Mphasis Limited"),
    ("LTIM.NS",      "LTIMindtree"),
    ("PERSISTENT.NS","Persistent Systems"),
    ("COFORGE.NS",   "Coforge Limited"),
    ("KPITTECH.NS",  "KPIT Technologies"),
    ("RELIANCE.NS",  "Reliance Industries"),
    ("HDFCBANK.NS",  "HDFC Bank"),
    ("ICICIBANK.NS", "ICICI Bank"),
    ("SBIN.NS",      "State Bank of India"),
    ("AXISBANK.NS",  "Axis Bank"),
    ("KOTAKBANK.NS", "Kotak Mahindra Bank"),
    ("BAJFINANCE.NS","Bajaj Finance"),
    ("BAJAJFINSV.NS","Bajaj Finserv"),
    ("INDUSINDBK.NS","IndusInd Bank"),
    ("BANDHANBNK.NS","Bandhan Bank"),
    ("HINDUNILVR.NS","Hindustan Unilever"),
    ("ITC.NS",       "ITC Limited"),
    ("NESTLEIND.NS", "Nestle India"),
    ("BRITANNIA.NS", "Britannia Industries"),
    ("DABUR.NS",     "Dabur India"),
    ("MARICO.NS",    "Marico Limited"),
    ("COLPAL.NS",    "Colgate-Palmolive India"),
    ("GODREJCP.NS",  "Godrej Consumer Products"),
    ("EMAMILTD.NS",  "Emami Limited"),
    ("TATACONSUM.NS","Tata Consumer Products"),
    ("TATAMOTORS.NS","Tata Motors"),
    ("MARUTI.NS",    "Maruti Suzuki India"),
    ("M&M.NS",       "Mahindra & Mahindra"),
    ("BAJAJ-AUTO.NS","Bajaj Auto"),
    ("HEROMOTOCO.NS","Hero MotoCorp"),
    ("EICHERMOT.NS", "Eicher Motors"),
    ("TVSMOTOR.NS",  "TVS Motor Company"),
    ("ASHOKLEY.NS",  "Ashok Leyland"),
    ("TATASTEEL.NS", "Tata Steel"),
    ("JSWSTEEL.NS",  "JSW Steel"),
    ("HINDALCO.NS",  "Hindalco Industries"),
    ("VEDL.NS",      "Vedanta Limited"),
    ("COALINDIA.NS", "Coal India"),
    ("NTPC.NS",      "NTPC Limited"),
    ("POWERGRID.NS", "Power Grid Corporation"),
    ("ADANIPORTS.NS","Adani Ports"),
    ("ADANIENT.NS",  "Adani Enterprises"),
    ("ADANIGREEN.NS","Adani Green Energy"),
    ("ADANIPOWER.NS","Adani Power"),
    ("ONGC.NS",      "Oil & Natural Gas Corp."),
    ("BPCL.NS",      "Bharat Petroleum"),
    ("IOC.NS",       "Indian Oil Corporation"),
    ("GAIL.NS",      "GAIL India"),
    ("SUNPHARMA.NS", "Sun Pharmaceutical"),
    ("DRREDDY.NS",   "Dr. Reddy's Laboratories"),
    ("CIPLA.NS",     "Cipla Limited"),
    ("DIVISLAB.NS",  "Divi's Laboratories"),
    ("APOLLOHOSP.NS","Apollo Hospitals"),
    ("MAXHEALTH.NS", "Max Healthcare"),
    ("FORTIS.NS",    "Fortis Healthcare"),
    ("NAUKRI.NS",    "Info Edge India"),
    ("ZOMATO.NS",    "Zomato Limited"),
    ("PAYTM.NS",     "One97 Communications"),
    ("POLICYBZR.NS", "PB Fintech"),
    ("DELHIVERY.NS", "Delhivery Limited"),
    ("IRCTC.NS",     "Indian Railway Catering"),
    ("INDIGO.NS",    "InterGlobe Aviation"),
    ("SPICEJET.NS",  "SpiceJet Limited"),
    ("ULTRACEMCO.NS","UltraTech Cement"),
    ("SHREECEM.NS",  "Shree Cement"),
    ("AMBUJACEM.NS", "Ambuja Cements"),
    ("ACC.NS",       "ACC Limited"),
    ("ASIANPAINT.NS","Asian Paints"),
    ("BERGERINT.NS", "Berger Paints"),
    ("PIDILITIND.NS","Pidilite Industries"),
    ("TITAN.NS",     "Titan Company"),
    ("TRENT.NS",     "Trent Limited"),
    ("DMART.NS",     "Avenue Supermarts"),
    ("HAVELLS.NS",   "Havells India"),
    ("VOLTAS.NS",    "Voltas Limited"),
    ("WHIRLPOOL.NS", "Whirlpool of India"),
    ("LTTS.NS",      "L&T Technology Services"),
    ("LT.NS",        "Larsen & Toubro"),
    ("SIEMENS.NS",   "Siemens India"),
    ("ABB.NS",       "ABB India"),
    ("CUMMINSIND.NS","Cummins India"),
    ("MOTHERSON.NS", "Samvardhana Motherson"),
    ("BHARTIARTL.NS","Bharti Airtel"),
    ("IDEA.NS",      "Vodafone Idea"),
    # ── Global ETFs & Indices ──────────────────────────────────
    ("SPY",    "SPDR S&P 500 ETF"),
    ("QQQ",    "Invesco QQQ (NASDAQ-100)"),
    ("DIA",    "SPDR Dow Jones ETF"),
    ("IWM",    "iShares Russell 2000"),
    ("VTI",    "Vanguard Total Market"),
    ("VOO",    "Vanguard S&P 500 ETF"),
    ("GLD",    "SPDR Gold Shares"),
    ("SLV",    "iShares Silver Trust"),
    ("USO",    "US Oil Fund"),
    ("TLT",    "iShares 20+ Year Treasury"),
    ("^NSEI",  "Nifty 50 Index"),
    ("^BSESN", "BSE Sensex Index"),
    ("^GSPC",  "S&P 500 Index"),
    ("^DJI",   "Dow Jones Industrial Avg"),
    ("^IXIC",  "NASDAQ Composite"),
    ("^RUT",   "Russell 2000 Index"),
    ("^VIX",   "CBOE Volatility Index"),
    # ── Crypto ────────────────────────────────────────────────
    ("BTC-USD", "Bitcoin USD"),
    ("ETH-USD", "Ethereum USD"),
    ("BNB-USD", "BNB USD"),
    ("XRP-USD", "XRP USD"),
    ("SOL-USD", "Solana USD"),
    ("ADA-USD", "Cardano USD"),
    ("DOGE-USD","Dogecoin USD"),
]


def search_symbols(query: str, max_results: int = 10) -> list[tuple[str, str]]:
    """
    Return up to max_results symbols/names that contain `query` (case-insensitive).
    Prioritises entries where the SYMBOL starts with the query, then name matches.
    Returns list of (symbol, name) tuples.
    """
    q = query.upper().strip()
    if not q:
        return []
    starts_with = [(s, n) for s, n in SYMBOL_LIST if s.startswith(q)]
    contains    = [(s, n) for s, n in SYMBOL_LIST
                   if not s.startswith(q) and (q in s or q in n.upper())]
    return (starts_with + contains)[:max_results]


# =============================================================
#  DATA FETCHING
# =============================================================

def fetch_historical(symbol: str, days: int) -> pd.DataFrame | None:
    """
    Fetch OHLCV data for `symbol` over the last `days` calendar days.
    Returns a DataFrame or None if no data found.
    """
    end   = datetime.today()
    start = end - timedelta(days=days)
    df = yf.download(symbol, start=start, end=end,
                     progress=False, auto_adjust=True)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return None if df.empty else df


def fetch_live_price(symbol: str) -> float | None:
    """
    Fetch the most recent closing price for a single symbol.
    Returns a float or None on failure.
    """
    try:
        hist = yf.Ticker(symbol).history(period='2d')
        return hist['Close'].iloc[-1].item() if not hist.empty else None
    except Exception:
        return None


# =============================================================
#  INDICATOR CALCULATIONS
# =============================================================

def compute_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """Relative Strength Index (RSI) using EWM smoothing."""
    delta = series.diff()
    gain  = delta.clip(lower=0)
    loss  = -delta.clip(upper=0)
    avg_g = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_l = loss.ewm(com=period - 1, min_periods=period).mean()
    return 100 - (100 / (1 + avg_g / avg_l))


def compute_moving_averages(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds SMA20, SMA50, EMA12, EMA26 columns to a copy of df.
    Returns the enriched DataFrame.
    """
    out = df.copy()
    out['SMA20'] = out['Close'].rolling(20).mean()
    out['SMA50'] = out['Close'].rolling(50).mean()
    out['EMA12'] = out['Close'].ewm(span=12, adjust=False).mean()
    out['EMA26'] = out['Close'].ewm(span=26, adjust=False).mean()
    return out


def compute_bollinger_bands(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    """
    Adds BB_Mid, BB_Upper, BB_Lower columns.
    Returns enriched DataFrame.
    """
    out = df.copy()
    out['BB_Mid']   = out['Close'].rolling(window).mean()
    out['BB_Std']   = out['Close'].rolling(window).std()
    out['BB_Upper'] = out['BB_Mid'] + 2 * out['BB_Std']
    out['BB_Lower'] = out['BB_Mid'] - 2 * out['BB_Std']
    return out


def compute_signals(df: pd.DataFrame, short_window: int, long_window: int) -> pd.DataFrame:
    """
    MA crossover buy/sell signals.
    Adds: Short_MA, Long_MA, Signal, Position columns.
    Returns enriched DataFrame.
    """
    out = df.copy()
    out['Short_MA'] = out['Close'].rolling(short_window).mean()
    out['Long_MA']  = out['Close'].rolling(long_window).mean()
    out['Signal']   = np.where(out['Short_MA'] > out['Long_MA'], 1, 0)
    out['Position'] = out['Signal'].diff()
    return out


def compute_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies all indicators at once (used for export).
    Returns DataFrame with SMA20, SMA50, EMA12, RSI14, BB_Upper, BB_Lower.
    """
    out = df.copy()
    out['SMA20']    = out['Close'].rolling(20).mean()
    out['SMA50']    = out['Close'].rolling(50).mean()
    out['EMA12']    = out['Close'].ewm(span=12, adjust=False).mean()
    out['RSI14']    = compute_rsi(out['Close'])
    out['BB_Upper'] = out['Close'].rolling(20).mean() + 2 * out['Close'].rolling(20).std()
    out['BB_Lower'] = out['Close'].rolling(20).mean() - 2 * out['Close'].rolling(20).std()
    return out


# =============================================================
#  SUMMARY / ANALYTICS
# =============================================================

def get_dashboard_metrics(df: pd.DataFrame, symbol: str) -> dict:
    """
    Returns a plain dict of summary metrics for the dashboard cards.
    All values are already formatted strings — frontend just displays them.
    """
    close      = df['Close'].iloc[-1].item()
    prev_close = df['Close'].iloc[-2].item()
    pct_change = (close - prev_close) / prev_close * 100
    direction  = "▲" if pct_change >= 0 else "▼"

    return {
        "symbol":       symbol,
        "date":         df.index[-1].strftime("%d %b %Y"),
        "close":        round(close, 2),
        "prev_close":   round(prev_close, 2),
        "open":         round(df['Open'].iloc[-1].item(), 2),
        "high":         round(df['High'].iloc[-1].item(), 2),
        "low":          round(df['Low'].iloc[-1].item(), 2),
        "volume":       int(df['Volume'].iloc[-1].item()),
        "pct_change":   round(pct_change, 2),
        "direction":    direction,
        "period_high":  round(df['High'].max().item(), 2),
        "period_low":   round(df['Low'].min().item(), 2),
        "avg_volume":   int(df['Volume'].mean()),
        "is_up":        pct_change >= 0,
    }


def get_portfolio_data(holdings: dict) -> tuple[list, float]:
    """
    Given holdings = {symbol: shares}, fetches live prices
    and returns (results_list, total_value).

    results_list is a list of dicts:
      [{ symbol, shares, price, value, allocation }, ...]
    """
    raw     = []
    total   = 0.0

    for symbol, shares in holdings.items():
        price = fetch_live_price(symbol) or 0.0
        value = price * shares
        total += value
        raw.append({"symbol": symbol, "shares": shares,
                    "price": price, "value": value})

    results = []
    for r in raw:
        r["allocation"] = round(r["value"] / total * 100, 1) if total else 0.0
        r["price"]      = round(r["price"], 2)
        r["value"]      = round(r["value"], 2)
        results.append(r)

    return results, round(total, 2)


def get_normalized_comparison(symbols: list, days: int) -> list:
    """
    Fetches data for each symbol and normalizes to base 100.
    Returns list of (symbol, index_series, normalized_series) tuples.
    Only includes symbols where data was successfully fetched.
    """
    results = []
    for symbol in symbols:
        df = fetch_historical(symbol, days)
        if df is not None:
            norm = df['Close'] / df['Close'].iloc[0] * 100
            results.append((symbol, df.index, norm))
    return results


# =============================================================
#  EXPORT
# =============================================================

def export_to_csv(df: pd.DataFrame, symbol: str, days: int, folder: str) -> str:
    """
    Exports enriched DataFrame to CSV.
    Returns the saved file path.
    """
    path = os.path.join(folder, f"{symbol}_{days}d.csv")
    enriched = compute_all_indicators(df)
    enriched.to_csv(path)
    return path


def export_to_excel(df: pd.DataFrame, symbol: str, days: int, folder: str) -> str | None:
    """
    Exports enriched DataFrame to Excel with 2 sheets: Data + Summary.
    Returns the saved file path, or None if openpyxl is not installed.
    """
    if not EXCEL_AVAILABLE:
        return None

    enriched = compute_all_indicators(df)
    metrics  = get_dashboard_metrics(df, symbol)
    path     = os.path.join(folder, f"{symbol}_{days}d.xlsx")

    summary = pd.DataFrame({
        "Metric": ["Symbol", "Close", "Change %", "Period High",
                   "Period Low", "Avg Volume"],
        "Value":  [symbol,
                   f"{metrics['close']:.2f}",
                   f"{metrics['direction']} {abs(metrics['pct_change']):.2f}%",
                   f"{metrics['period_high']:.2f}",
                   f"{metrics['period_low']:.2f}",
                   f"{metrics['avg_volume']:,}"],
    })

    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        enriched.to_excel(writer, sheet_name="OHLCV + Indicators")
        summary.to_excel(writer, sheet_name="Summary", index=False)

    return path


# =============================================================
#  THEME & COLORS  (frontend concern only)
# =============================================================

BG_DARK  = "#1a1a2e"
BG_PANEL = "#16213e"
BG_CARD  = "#0f3460"
ACCENT   = "#e94560"
ACCENT2  = "#1D9E75"
TEXT_PRI = "#eaeaea"
TEXT_SEC = "#a0a0b0"
BORDER   = "#2a2a4a"

CHART_COLORS = ['#378ADD','#1D9E75','#D85A30','#7F77DD','#BA7517','#D4537E']

plt.rcParams.update({
    'figure.facecolor':  BG_PANEL,
    'axes.facecolor':    BG_DARK,
    'axes.edgecolor':    BORDER,
    'axes.labelcolor':   TEXT_SEC,
    'xtick.color':       TEXT_SEC,
    'ytick.color':       TEXT_SEC,
    'text.color':        TEXT_PRI,
    'grid.color':        BORDER,
    'grid.alpha':        0.5,
    'legend.facecolor':  BG_PANEL,
    'legend.edgecolor':  BORDER,
    'legend.labelcolor': TEXT_PRI,
})

# =============================================================
#  REUSABLE WIDGET HELPERS  (frontend only)
# =============================================================

def styled_label(parent, text, size=11, bold=False, color=TEXT_PRI, **kw):
    weight = "bold" if bold else "normal"
    return tk.Label(parent, text=text, font=("Segoe UI", size, weight),
                    fg=color, bg=parent.cget('bg'), **kw)

def styled_entry(parent, width=12, **kw):
    return tk.Entry(parent, width=width, font=("Segoe UI", 11),
                    bg=BG_DARK, fg=TEXT_PRI, insertbackground=TEXT_PRI,
                    relief="flat", highlightthickness=1,
                    highlightbackground=BORDER, highlightcolor=ACCENT, **kw)

def styled_button(parent, text, command, color=ACCENT, width=14, **kw):
    b = tk.Button(parent, text=text, command=command,
                  font=("Segoe UI", 10, "bold"),
                  bg=color, fg="white", activebackground=BG_CARD,
                  activeforeground="white", relief="flat",
                  padx=10, pady=6, cursor="hand2", width=width, **kw)
    b.bind("<Enter>", lambda e: b.config(bg=BG_CARD))
    b.bind("<Leave>", lambda e: b.config(bg=color))
    return b

def card_frame(parent, **kw):
    return tk.Frame(parent, bg=BG_CARD, bd=0, relief="flat", **kw)

def make_canvas(parent, fig):
    """Embed a matplotlib Figure inside a tkinter parent frame."""
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    tb_frame = tk.Frame(parent, bg=BG_PANEL)
    tb_frame.pack(fill="x")
    NavigationToolbar2Tk(canvas, tb_frame)
    canvas.get_tk_widget().pack(fill="both", expand=True)
    return canvas

def loading_label(parent):
    lbl = styled_label(parent, "Loading...", color=TEXT_SEC)
    lbl.pack(pady=20)
    return lbl



# =============================================================
#  AUTOCOMPLETE SYMBOL ENTRY WIDGET
# =============================================================

class AutocompleteEntry(tk.Frame):
    """
    A themed text entry that shows a live dropdown of matching stock
    symbols as the user types. Backed by backend.search_symbols().

    Usage:
        w = AutocompleteEntry(parent, default="AAPL")
        w.pack(side="left", padx=4)
        symbol = w.get()      # returns uppercased text
        w.set("TCS.NS")       # programmatically set value
    """

    DROPDOWN_MAX = 10
    ROW_HEIGHT   = 26
    DROPDOWN_W   = 300

    def __init__(self, parent, default="AAPL", width=12, **kw):
        super().__init__(parent, bg=parent.cget("bg"), **kw)
        self._var      = tk.StringVar(value=default)
        self._dropdown = None
        self._listbox  = None
        self._matches  = []
        self._suppress = False
        self._after_id = None

        self._entry = tk.Entry(
            self, textvariable=self._var, width=width,
            font=("Segoe UI", 11),
            bg=BG_DARK, fg=TEXT_PRI, insertbackground=TEXT_PRI,
            relief="flat", highlightthickness=1,
            highlightbackground=BORDER, highlightcolor=ACCENT,
        )
        self._entry.pack(ipady=4)

        self._var.trace_add("write", self._on_type)
        self._entry.bind("<Down>",     self._focus_list)
        self._entry.bind("<Escape>",   lambda e: self._close_dropdown())
        self._entry.bind("<FocusOut>", self._on_focus_out)
        self._entry.bind("<Return>",   lambda e: self._close_dropdown())

    # -- Public API --------------------------------------------

    def get(self) -> str:
        return self._var.get().upper().strip()

    def set(self, value: str):
        self._suppress = True
        self._var.set(value.upper().strip())
        self._suppress = False
        self._close_dropdown()

    def delete(self, a, b):
        """Mimic tk.Entry.delete so callers can clear the field."""
        self._entry.delete(a, b)

    # -- Internal ----------------------------------------------

    def _on_type(self, *_):
        if self._suppress:
            return
        if self._after_id:
            self.after_cancel(self._after_id)
        self._after_id = self.after(120, self._update_dropdown)

    def _update_dropdown(self):
        query   = self._var.get().strip()
        matches = search_symbols(query, self.DROPDOWN_MAX) if query else []
        if not matches:
            self._close_dropdown()
            return
        self._open_dropdown(matches)

    def _open_dropdown(self, matches):
        if self._dropdown is None or not self._dropdown.winfo_exists():
            self._dropdown = tk.Toplevel(self)
            self._dropdown.wm_overrideredirect(True)
            self._dropdown.configure(bg=BORDER)
            self._dropdown.attributes("-topmost", True)

            self._listbox = tk.Listbox(
                self._dropdown,
                font=("Segoe UI", 10),
                bg=BG_CARD, fg=TEXT_PRI,
                selectbackground=ACCENT, selectforeground="white",
                activestyle="none", relief="flat", bd=0,
                highlightthickness=0, cursor="hand2",
            )
            self._listbox.pack(fill="both", expand=True, padx=1, pady=1)
            self._listbox.bind("<<ListboxSelect>>", self._on_select)
            self._listbox.bind("<Return>",          self._on_select)
            self._listbox.bind("<Escape>",          lambda e: self._close_dropdown())
            self._listbox.bind("<FocusOut>",        self._on_focus_out)

        self.update_idletasks()
        x = self._entry.winfo_rootx()
        y = self._entry.winfo_rooty() + self._entry.winfo_height() + 2
        h = min(len(matches), self.DROPDOWN_MAX) * self.ROW_HEIGHT
        self._dropdown.geometry(f"{self.DROPDOWN_W}x{h}+{x}+{y}")

        self._listbox.delete(0, tk.END)
        self._matches = matches
        for sym, name in matches:
            self._listbox.insert(tk.END, f"  {sym:<16} {name}")

        self._dropdown.deiconify()

    def _close_dropdown(self):
        if self._dropdown and self._dropdown.winfo_exists():
            self._dropdown.withdraw()

    def _on_select(self, event=None):
        idx = self._listbox.curselection()
        if not idx:
            return
        sym, _ = self._matches[idx[0]]
        self.set(sym)
        self._entry.focus_set()
        self._entry.icursor(tk.END)

    def _focus_list(self, event=None):
        if self._listbox and self._dropdown.winfo_ismapped():
            self._listbox.focus_set()
            if self._listbox.size():
                self._listbox.selection_set(0)
                self._listbox.activate(0)

    def _on_focus_out(self, event=None):
        self.after(150, self._check_focus)

    def _check_focus(self):
        try:
            focused = self.focus_get()
            if focused not in (self._entry, self._listbox):
                self._close_dropdown()
        except Exception:
            pass

# =============================================================
#  MAIN APPLICATION WINDOW
# =============================================================

class StockTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("STOCKS — Stock Price Tracker")
        self.geometry("1280x780")
        self.minsize(1100, 650)
        self.configure(bg=BG_DARK)
        self.resizable(True, True)
        self._build_ui()

    # ── LAYOUT ───────────────────────────────────────────────

    def _build_ui(self):
        self._build_titlebar()
        body = tk.Frame(self, bg=BG_DARK)
        body.pack(fill="both", expand=True)
        self._build_sidebar(body)
        self.content = tk.Frame(body, bg=BG_DARK)
        self.content.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self._show_dashboard_view()

    def _build_titlebar(self):
        bar = tk.Frame(self, bg=BG_PANEL, height=52)
        bar.pack(fill="x", side="top")
        bar.pack_propagate(False)
        tk.Label(bar, text="📈  STOCKS", font=("Segoe UI", 15, "bold"),
                 fg=ACCENT, bg=BG_PANEL).pack(side="left", padx=18, pady=10)
        tk.Label(bar, text="Stock Price Tracker",
                 font=("Segoe UI", 10), fg=TEXT_SEC, bg=BG_PANEL).pack(side="left")
        self.clock_lbl = tk.Label(bar, font=("Segoe UI", 10), fg=TEXT_SEC, bg=BG_PANEL)
        self.clock_lbl.pack(side="right", padx=18)
        self._tick_clock()

    def _tick_clock(self):
        self.clock_lbl.config(text=datetime.now().strftime("%d %b %Y   %H:%M:%S"))
        self.after(1000, self._tick_clock)

    def _build_sidebar(self, parent):
        sb = tk.Frame(parent, bg=BG_PANEL, width=185)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)
        tk.Label(sb, text="MENU", font=("Segoe UI", 9, "bold"),
                 fg=TEXT_SEC, bg=BG_PANEL).pack(pady=(18, 6), padx=16, anchor="w")
        nav_items = [
            ("📊  Dashboard",        self._show_dashboard_view),
            ("📈  Price Plot",       self._show_plot_view),
            ("🕯  Candlestick",      self._show_candle_view),
            ("📉  Indicators",       self._show_indicators_view),
            ("⚡  Buy/Sell Signals", self._show_signals_view),
            ("🔀  Compare Stocks",   self._show_compare_view),
            ("💼  Portfolio",        self._show_portfolio_view),
            ("💾  Export Data",      self._show_export_view),
        ]
        for label, cmd in nav_items:
            b = tk.Button(sb, text=label, command=cmd,
                          font=("Segoe UI", 10), fg=TEXT_PRI, bg=BG_PANEL,
                          activebackground=BG_CARD, activeforeground=ACCENT,
                          relief="flat", anchor="w", padx=16, pady=8,
                          cursor="hand2", width=20)
            b.pack(fill="x", pady=1)
            b.bind("<Enter>", lambda e, b=b: b.config(bg=BG_CARD, fg=ACCENT))
            b.bind("<Leave>", lambda e, b=b: b.config(bg=BG_PANEL, fg=TEXT_PRI))

    def _clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    # ── SHARED INPUT HELPERS ──────────────────────────────────

    def _input_row(self, parent, days_default="90", default_sym="AAPL"):
        """Returns (row_frame, AutocompleteEntry, days_entry)."""
        row = tk.Frame(parent, bg=BG_PANEL, pady=10, padx=14)
        row.pack(fill="x", pady=(0, 8))
        styled_label(row, "Symbol:", color=TEXT_SEC).pack(side="left", padx=(0, 4))
        sym_e = AutocompleteEntry(row, default=default_sym, width=12)
        sym_e.pack(side="left", padx=(0, 14))
        styled_label(row, "Days:", color=TEXT_SEC).pack(side="left", padx=(0, 4))
        days_e = styled_entry(row, width=6)
        days_e.insert(0, days_default)
        days_e.pack(side="left", padx=(0, 14), ipady=4)
        return row, sym_e, days_e

    def _parse_sym_days(self, sym_e, days_e):
        """Validate and return (symbol, days) or (None, None) on error."""
        symbol = sym_e.get().upper().strip()
        if not symbol:
            messagebox.showerror("Input Error", "Please enter a stock symbol.")
            return None, None
        try:
            days = int(days_e.get())
            if days <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Enter a valid positive number of days.")
            return None, None
        return symbol, days

    def _fetch_bg(self, symbol, days, on_done):
        """Fetch historical data in a background thread, call on_done(df) on UI thread."""
        def worker():
            df = fetch_historical(symbol, days)
            self.after(0, lambda: on_done(df))
        threading.Thread(target=worker, daemon=True).start()

    def _clear_frame(self, frame):
        for w in frame.winfo_children():
            w.destroy()

    # =========================================================
    #  VIEW 1 — DASHBOARD
    # =========================================================

    def _show_dashboard_view(self):
        self._clear_content()
        styled_label(self.content, "Live Dashboard", size=14, bold=True).pack(anchor="w", pady=(4, 8))

        ctrl = tk.Frame(self.content, bg=BG_DARK)
        ctrl.pack(fill="x")
        row, sym_e, days_e = self._input_row(ctrl, days_default="30")

        self._dash_cards = tk.Frame(self.content, bg=BG_DARK)
        self._dash_cards.pack(fill="x", pady=6)
        self._dash_chart = tk.Frame(self.content, bg=BG_DARK)
        self._dash_chart.pack(fill="both", expand=True)

        def on_fetch():
            symbol, days = self._parse_sym_days(sym_e, days_e)
            if symbol is None: return
            self._clear_frame(self._dash_cards)
            self._clear_frame(self._dash_chart)
            loading_label(self._dash_cards)

            def on_done(df):
                self._clear_frame(self._dash_cards)
                if df is None:
                    messagebox.showerror("Error", f"No data found for '{symbol}'.")
                    return
                # ── backend gives us clean metrics dict ──
                m = get_dashboard_metrics(df, symbol)
                self._render_dashboard_cards(m)
                self._render_dashboard_chart(df, symbol, days, m)

            self._fetch_bg(symbol, days, on_done)

        styled_button(row, "Fetch", on_fetch, color=ACCENT2, width=8).pack(
            side="left", padx=6, pady=10)

    def _render_dashboard_cards(self, m):
        """Pure UI: draw metric cards from the metrics dict returned by backend."""
        pct_color = "#1D9E75" if m["is_up"] else "#D85A30"
        cards = [
            ("CLOSE",       f"{m['close']:.2f}",                                TEXT_PRI),
            ("CHANGE",      f"{m['direction']} {abs(m['pct_change']):.2f} %",   pct_color),
            ("OPEN",        f"{m['open']:.2f}",                                 TEXT_PRI),
            ("HIGH",        f"{m['high']:.2f}",                                 "#1D9E75"),
            ("LOW",         f"{m['low']:.2f}",                                  "#D85A30"),
            ("VOLUME",      f"{m['volume']:,}",                                  TEXT_PRI),
            ("PERIOD HIGH", f"{m['period_high']:.2f}",                          "#1D9E75"),
            ("PERIOD LOW",  f"{m['period_low']:.2f}",                           "#D85A30"),
        ]
        for i, (label, value, vc) in enumerate(cards):
            card = card_frame(self._dash_cards, padx=12, pady=8)
            card.grid(row=0, column=i, padx=5, pady=4, sticky="nsew")
            styled_label(card, label, size=8, color=TEXT_SEC).pack(anchor="w")
            styled_label(card, value, size=13, bold=True, color=vc).pack(anchor="w")
            self._dash_cards.columnconfigure(i, weight=1)

    def _render_dashboard_chart(self, df, symbol, days, m):
        """Pure UI: draw the closing price area chart."""
        self._clear_frame(self._dash_chart)
        fig = Figure(figsize=(10, 3.8), dpi=96)
        ax  = fig.add_subplot(111)
        ax.plot(df.index, df['Close'], color=ACCENT2, linewidth=2, label="Close")
        ax.fill_between(df.index, df['Close'], df['Close'].min(),
                        alpha=0.08, color=ACCENT2)
        ax.set_title(f"{symbol}  —  Closing Price  |  Last {days} Days",
                     fontsize=11, fontweight='bold', color=TEXT_PRI, pad=8)
        ax.set_xlabel("Date"); ax.set_ylabel("Price")
        ax.grid(True, linestyle='--', alpha=0.4); ax.legend()
        fig.tight_layout()
        make_canvas(self._dash_chart, fig)

    # =========================================================
    #  VIEW 2 — PRICE PLOT
    # =========================================================

    def _show_plot_view(self):
        self._clear_content()
        styled_label(self.content, "Price Plot", size=14, bold=True).pack(anchor="w", pady=(4, 8))

        ctrl = tk.Frame(self.content, bg=BG_PANEL, pady=10, padx=14)
        ctrl.pack(fill="x", pady=(0, 8))

        styled_label(ctrl, "Symbol:", color=TEXT_SEC).pack(side="left", padx=(0, 4))
        sym_e = AutocompleteEntry(ctrl, default="AAPL", width=12)
        sym_e.pack(side="left", padx=(0, 12))

        styled_label(ctrl, "Days:", color=TEXT_SEC).pack(side="left", padx=(0, 4))
        days_e = styled_entry(ctrl, width=6); days_e.insert(0, "90")
        days_e.pack(side="left", padx=(0, 12), ipady=4)

        styled_label(ctrl, "Price Type:", color=TEXT_SEC).pack(side="left", padx=(0, 4))
        price_var = tk.StringVar(value="Close")
        ttk.Combobox(ctrl, textvariable=price_var, width=8,
                     values=["Open","High","Low","Close","Volume"],
                     state="readonly").pack(side="left", padx=(0, 12))

        chart_f = tk.Frame(self.content, bg=BG_DARK)
        chart_f.pack(fill="both", expand=True)

        color_map = {"Open": CHART_COLORS[0], "High": CHART_COLORS[1],
                     "Low":  CHART_COLORS[2], "Close": CHART_COLORS[3],
                     "Volume": CHART_COLORS[4]}

        def on_plot():
            symbol, days = self._parse_sym_days(sym_e, days_e)
            if symbol is None: return
            col = price_var.get()
            self._clear_frame(chart_f); loading_label(chart_f)

            def on_done(df):
                self._clear_frame(chart_f)
                if df is None: messagebox.showerror("Error", f"No data for '{symbol}'."); return
                # ── pure UI drawing ──
                fig = Figure(figsize=(10, 5), dpi=96)
                ax  = fig.add_subplot(111)
                ax.plot(df.index, df[col], color=color_map[col], linewidth=2, label=col)
                ax.set_title(f"{symbol}  —  {col}  |  Last {days} Days",
                             fontsize=11, fontweight='bold', color=TEXT_PRI)
                ax.set_xlabel("Date"); ax.set_ylabel(col)
                ax.legend(); ax.grid(True, linestyle='--', alpha=0.4)
                fig.tight_layout()
                make_canvas(chart_f, fig)

            self._fetch_bg(symbol, days, on_done)

        styled_button(ctrl, "Plot", on_plot, color=ACCENT, width=8).pack(
            side="left", padx=4, ipady=2)

    # =========================================================
    #  VIEW 3 — CANDLESTICK
    # =========================================================

    def _show_candle_view(self):
        self._clear_content()
        styled_label(self.content, "Candlestick Chart", size=14, bold=True).pack(anchor="w", pady=(4, 8))

        row, sym_e, days_e = self._input_row(self.content, days_default="60")
        chart_f = tk.Frame(self.content, bg=BG_DARK)
        chart_f.pack(fill="both", expand=True)

        def on_draw():
            symbol, days = self._parse_sym_days(sym_e, days_e)
            if symbol is None: return
            self._clear_frame(chart_f); loading_label(chart_f)

            def on_done(df):
                self._clear_frame(chart_f)
                if df is None: messagebox.showerror("Error", f"No data for '{symbol}'."); return
                # ── pure UI drawing ──
                fig = Figure(figsize=(10, 6), dpi=96)
                gs  = gridspec.GridSpec(2, 1, height_ratios=[3, 1], hspace=0.05, figure=fig)
                ax1 = fig.add_subplot(gs[0])
                ax2 = fig.add_subplot(gs[1], sharex=ax1)

                up   = df[df['Close'] >= df['Open']]
                down = df[df['Close'] <  df['Open']]
                for sub, col, bot in [
                    (up,   "#1D9E75", up['Open']),
                    (down, "#D85A30", down['Close']),
                ]:
                    ax1.bar(sub.index, abs(sub['Close'] - sub['Open']),
                            0.6, bottom=bot, color=col, alpha=0.9)
                    ax1.bar(sub.index, sub['High'] - sub[['Open','Close']].max(axis=1),
                            0.1, bottom=sub[['Open','Close']].max(axis=1), color=col)
                    ax1.bar(sub.index, sub[['Open','Close']].min(axis=1) - sub['Low'],
                            0.1, bottom=sub['Low'], color=col)

                ax1.set_title(f"{symbol}  —  Candlestick  |  Last {days} Days",
                              fontsize=11, fontweight='bold', color=TEXT_PRI)
                ax1.set_ylabel("Price"); ax1.grid(True, linestyle='--', alpha=0.3)
                plt.setp(ax1.get_xticklabels(), visible=False)

                clrs = ['#1D9E75' if c >= o else '#D85A30'
                        for c, o in zip(df['Close'], df['Open'])]
                ax2.bar(df.index, df['Volume'], color=clrs, alpha=0.8)
                ax2.set_ylabel("Volume"); ax2.grid(True, linestyle='--', alpha=0.3)
                ax2.yaxis.set_major_formatter(
                    plt.FuncFormatter(lambda x, _: f'{int(x):,}'))
                fig.tight_layout()
                make_canvas(chart_f, fig)

            self._fetch_bg(symbol, days, on_done)

        styled_button(row, "Draw Chart", on_draw, color=ACCENT, width=12).pack(
            side="left", padx=6, pady=10)

    # =========================================================
    #  VIEW 4 — INDICATORS (MA + RSI + Bollinger)
    # =========================================================

    def _show_indicators_view(self):
        self._clear_content()
        styled_label(self.content, "Technical Indicators", size=14, bold=True).pack(anchor="w", pady=(4, 8))

        row, sym_e, days_e = self._input_row(self.content, days_default="200")

        opts_f = tk.Frame(self.content, bg=BG_PANEL, padx=14, pady=6)
        opts_f.pack(fill="x")
        indicator_flags = {}
        for label in ["SMA 20", "SMA 50", "EMA 12", "RSI", "Bollinger Bands"]:
            v = tk.BooleanVar(value=True)
            tk.Checkbutton(opts_f, text=label, variable=v,
                           font=("Segoe UI", 10), fg=TEXT_PRI, bg=BG_PANEL,
                           selectcolor=BG_DARK, activebackground=BG_PANEL,
                           activeforeground=ACCENT).pack(side="left", padx=10)
            indicator_flags[label] = v

        chart_f = tk.Frame(self.content, bg=BG_DARK)
        chart_f.pack(fill="both", expand=True)

        def on_load():
            symbol, days = self._parse_sym_days(sym_e, days_e)
            if symbol is None: return
            flags = {k: v.get() for k, v in indicator_flags.items()}
            self._clear_frame(chart_f); loading_label(chart_f)

            def on_done(df):
                self._clear_frame(chart_f)
                if df is None: messagebox.showerror("Error", f"No data for '{symbol}'."); return

                # ── backend calculations ──
                df_ma  = compute_moving_averages(df)
                df_bb  = compute_bollinger_bands(df)
                df['RSI14'] = compute_rsi(df['Close'])

                # ── pure UI drawing ──
                show_rsi = flags["RSI"]
                fig = Figure(figsize=(10, 6.5), dpi=96)
                gs  = gridspec.GridSpec(2 if show_rsi else 1, 1,
                                        height_ratios=[2.5, 1] if show_rsi else [1],
                                        hspace=0.08, figure=fig)
                ax1 = fig.add_subplot(gs[0])
                ax1.plot(df.index, df['Close'], color='#888780', linewidth=1.5,
                         label='Close', alpha=0.85)

                if flags["SMA 20"]:
                    ax1.plot(df_ma.index, df_ma['SMA20'], color=CHART_COLORS[0],
                             linewidth=1.5, label='SMA 20')
                if flags["SMA 50"]:
                    ax1.plot(df_ma.index, df_ma['SMA50'], color=CHART_COLORS[2],
                             linewidth=1.5, label='SMA 50')
                if flags["EMA 12"]:
                    ax1.plot(df_ma.index, df_ma['EMA12'], color=CHART_COLORS[1],
                             linewidth=1.3, linestyle='--', label='EMA 12')
                if flags["Bollinger Bands"]:
                    ax1.plot(df_bb.index, df_bb['BB_Upper'], color=CHART_COLORS[2],
                             linewidth=1, alpha=0.7, label='BB Upper')
                    ax1.plot(df_bb.index, df_bb['BB_Lower'], color=CHART_COLORS[1],
                             linewidth=1, alpha=0.7, label='BB Lower')
                    ax1.fill_between(df_bb.index, df_bb['BB_Upper'], df_bb['BB_Lower'],
                                     alpha=0.07, color=CHART_COLORS[0])

                ax1.set_title(f"{symbol}  —  Indicators  |  Last {days} Days",
                              fontsize=11, fontweight='bold', color=TEXT_PRI)
                ax1.set_ylabel("Price"); ax1.legend(fontsize=8)
                ax1.grid(True, linestyle='--', alpha=0.4)
                if show_rsi: plt.setp(ax1.get_xticklabels(), visible=False)

                if show_rsi:
                    ax2 = fig.add_subplot(gs[1], sharex=ax1)
                    ax2.plot(df.index, df['RSI14'], color=CHART_COLORS[4],
                             linewidth=1.5, label='RSI(14)')
                    ax2.axhline(70, color=CHART_COLORS[2], linestyle='--', linewidth=1)
                    ax2.axhline(30, color=CHART_COLORS[1], linestyle='--', linewidth=1)
                    ax2.fill_between(df.index, df['RSI14'], 70,
                                     where=(df['RSI14'] >= 70), alpha=0.15, color=CHART_COLORS[2])
                    ax2.fill_between(df.index, df['RSI14'], 30,
                                     where=(df['RSI14'] <= 30), alpha=0.15, color=CHART_COLORS[1])
                    ax2.set_ylim(0, 100); ax2.set_ylabel("RSI")
                    ax2.legend(fontsize=8); ax2.grid(True, linestyle='--', alpha=0.4)

                fig.tight_layout()
                make_canvas(chart_f, fig)

            self._fetch_bg(symbol, days, on_done)

        styled_button(row, "Load Indicators", on_load, color=ACCENT, width=14).pack(
            side="left", padx=6, pady=10)

    # =========================================================
    #  VIEW 5 — BUY/SELL SIGNALS
    # =========================================================

    def _show_signals_view(self):
        self._clear_content()
        styled_label(self.content, "Buy / Sell Signal Generator", size=14, bold=True).pack(
            anchor="w", pady=(4, 8))

        ctrl = tk.Frame(self.content, bg=BG_PANEL, pady=10, padx=14)
        ctrl.pack(fill="x", pady=(0, 8))

        def lbl(t): styled_label(ctrl, t, color=TEXT_SEC).pack(side="left", padx=(0, 4))
        def ent(w=7, default=""):
            e = styled_entry(ctrl, width=w); e.insert(0, default)
            e.pack(side="left", padx=(0, 12), ipady=4); return e

        lbl("Symbol:")
        sym_e = AutocompleteEntry(ctrl, default="AAPL", width=12)
        sym_e.pack(side="left", padx=(0, 12))
        lbl("Days:");   days_e = ent(6, "200")
        lbl("Short MA:"); sw_e = ent(5, "20")
        lbl("Long MA:");  lw_e = ent(5, "50")

        chart_f   = tk.Frame(self.content, bg=BG_DARK)
        chart_f.pack(fill="both", expand=True)
        stats_lbl = styled_label(self.content, "", color=TEXT_SEC, size=10)
        stats_lbl.pack(anchor="w", padx=10)

        def on_generate():
            symbol = sym_e.get().upper().strip()
            try:
                days = int(days_e.get()); sw = int(sw_e.get()); lw = int(lw_e.get())
                if sw >= lw: raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Long MA must be greater than Short MA."); return

            self._clear_frame(chart_f); loading_label(chart_f)

            def on_done(df):
                self._clear_frame(chart_f)
                if df is None: messagebox.showerror("Error", f"No data for '{symbol}'."); return

                # ── backend calculates signals ──
                df_sig = compute_signals(df, sw, lw)
                buys   = df_sig[df_sig['Position'] == 1]
                sells  = df_sig[df_sig['Position'] == -1]

                # ── pure UI drawing ──
                fig = Figure(figsize=(10, 5), dpi=96)
                ax  = fig.add_subplot(111)
                ax.plot(df_sig.index, df_sig['Close'],    color='#888780', linewidth=1.5, alpha=0.8, label='Close')
                ax.plot(df_sig.index, df_sig['Short_MA'], color=CHART_COLORS[0], linewidth=1.8, label=f'SMA {sw}')
                ax.plot(df_sig.index, df_sig['Long_MA'],  color=CHART_COLORS[2], linewidth=1.8, label=f'SMA {lw}')
                ax.scatter(buys.index,  buys['Close'],  marker='^', color='#1D9E75', s=90, zorder=5, label='Buy ▲')
                ax.scatter(sells.index, sells['Close'], marker='v', color='#D85A30', s=90, zorder=5, label='Sell ▼')
                ax.set_title(f"{symbol}  —  Crossover Signals  |  Last {days} Days",
                             fontsize=11, fontweight='bold', color=TEXT_PRI)
                ax.set_xlabel("Date"); ax.set_ylabel("Price")
                ax.legend(fontsize=9); ax.grid(True, linestyle='--', alpha=0.4)
                fig.tight_layout()
                make_canvas(chart_f, fig)
                stats_lbl.config(text=f"  Buy signals: {len(buys)}     Sell signals: {len(sells)}")

            self._fetch_bg(symbol, days, on_done)

        styled_button(ctrl, "Generate", on_generate, color=ACCENT, width=10).pack(
            side="left", padx=4, ipady=2)

    # =========================================================
    #  VIEW 6 — MULTI-STOCK COMPARISON
    # =========================================================

    def _show_compare_view(self):
        self._clear_content()
        styled_label(self.content, "Multi-Stock Comparison", size=14, bold=True).pack(
            anchor="w", pady=(4, 8))

        ctrl = tk.Frame(self.content, bg=BG_PANEL, pady=10, padx=14)
        ctrl.pack(fill="x", pady=(0, 8))

        styled_label(ctrl, "Symbols (comma-separated):", color=TEXT_SEC).pack(side="left", padx=(0, 4))
        sym_e = styled_entry(ctrl, width=24); sym_e.insert(0, "AAPL,MSFT,GOOGL")
        sym_e.pack(side="left", padx=(0, 12), ipady=4)
        styled_label(ctrl, "(e.g. TCS.NS, INFY.NS)", color=TEXT_SEC, size=9).pack(side="left", padx=(0,8))
        styled_label(ctrl, "Days:", color=TEXT_SEC).pack(side="left", padx=(0, 4))
        days_e = styled_entry(ctrl, width=6); days_e.insert(0, "180")
        days_e.pack(side="left", padx=(0, 12), ipady=4)

        chart_f = tk.Frame(self.content, bg=BG_DARK)
        chart_f.pack(fill="both", expand=True)

        def on_compare():
            syms = [s.strip().upper() for s in sym_e.get().split(',') if s.strip()]
            try: days = int(days_e.get())
            except: messagebox.showerror("Error", "Enter valid days."); return
            if not syms: messagebox.showerror("Error", "Enter at least one symbol."); return
            self._clear_frame(chart_f); loading_label(chart_f)

            def worker():
                # ── backend fetches + normalizes ──
                results = get_normalized_comparison(syms, days)
                self.after(0, lambda: render(results))

            def render(results):
                self._clear_frame(chart_f)
                if not results: messagebox.showerror("Error", "No data found."); return
                # ── pure UI drawing ──
                fig = Figure(figsize=(10, 5), dpi=96)
                ax  = fig.add_subplot(111)
                for i, (sym, idx, norm) in enumerate(results):
                    ax.plot(idx, norm, color=CHART_COLORS[i % len(CHART_COLORS)],
                            linewidth=2, label=sym)
                ax.axhline(100, color='#888780', linewidth=0.8, linestyle='--', alpha=0.6)
                ax.set_title(f"Normalized Comparison  |  Last {days} Days  (Base = 100)",
                             fontsize=11, fontweight='bold', color=TEXT_PRI)
                ax.set_xlabel("Date"); ax.set_ylabel("Normalized Price (Base 100)")
                ax.legend(); ax.grid(True, linestyle='--', alpha=0.4)
                fig.tight_layout()
                make_canvas(chart_f, fig)

            threading.Thread(target=worker, daemon=True).start()

        styled_button(ctrl, "Compare", on_compare, color=ACCENT, width=10).pack(
            side="left", padx=4, ipady=2)

    # =========================================================
    #  VIEW 7 — PORTFOLIO
    # =========================================================

    def _show_portfolio_view(self):
        self._clear_content()
        styled_label(self.content, "Portfolio Tracker", size=14, bold=True).pack(
            anchor="w", pady=(4, 8))

        self._portfolio_holdings = {}

        top = tk.Frame(self.content, bg=BG_DARK)
        top.pack(fill="both", expand=True)

        # ── Left: input panel ──
        left = tk.Frame(top, bg=BG_PANEL, width=280, padx=14, pady=12)
        left.pack(side="left", fill="y", padx=(0, 8))
        left.pack_propagate(False)

        styled_label(left, "Add Holdings", bold=True, size=11).pack(anchor="w", pady=(0, 10))
        styled_label(left, "Symbol:", color=TEXT_SEC).pack(anchor="w")
        sym_e = AutocompleteEntry(left, default="", width=16)
        sym_e.set("")
        sym_e.pack(fill="x", pady=(2, 8))
        styled_label(left, "Shares:", color=TEXT_SEC).pack(anchor="w")
        sh_e  = styled_entry(left, width=16); sh_e.pack(fill="x", pady=(2, 8), ipady=4)

        list_var = tk.StringVar()
        tk.Listbox(left, listvariable=list_var, font=("Segoe UI", 10),
                   bg=BG_DARK, fg=TEXT_PRI, selectbackground=BG_CARD,
                   relief="flat", height=8, bd=0).pack(fill="x", pady=6)

        def add_holding():
            sym = sym_e.get().upper().strip()
            try: sh = int(sh_e.get())
            except: messagebox.showerror("Error", "Enter valid share count."); return
            if not sym: return
            self._portfolio_holdings[sym] = sh
            list_var.set([f"{s}  ×  {n}" for s, n in self._portfolio_holdings.items()])
            sym_e.delete(0, tk.END); sh_e.delete(0, tk.END)

        styled_button(left, "Add",   add_holding,
                      color=ACCENT2, width=10).pack(fill="x", pady=3)
        styled_button(left, "Clear", lambda: (self._portfolio_holdings.clear(), list_var.set([])),
                      color="#555",  width=10).pack(fill="x", pady=3)

        # ── Right: results ──
        right   = tk.Frame(top, bg=BG_DARK)
        right.pack(side="left", fill="both", expand=True)
        result_f = tk.Frame(right, bg=BG_DARK)
        result_f.pack(fill="both", expand=True)

        def on_fetch():
            if not self._portfolio_holdings:
                messagebox.showinfo("Portfolio", "Add at least one holding."); return
            self._clear_frame(result_f); loading_label(result_f)

            def worker():
                # ── backend fetches prices + calculates ──
                results, total = get_portfolio_data(self._portfolio_holdings)
                self.after(0, lambda: render(results, total))

            def render(results, total):
                self._clear_frame(result_f)
                if not results: return

                # ── pure UI: table ──
                tbl = tk.Frame(result_f, bg=BG_PANEL, padx=10, pady=10)
                tbl.pack(fill="x", pady=(0, 10))
                for ci, h in enumerate(["Symbol","Shares","Price","Value","Allocation"]):
                    styled_label(tbl, h, color=TEXT_SEC, size=9, bold=True).grid(
                        row=0, column=ci, padx=10, pady=4, sticky="w")
                for ri, r in enumerate(results):
                    row_vals = [r['symbol'], str(r['shares']),
                                f"{r['price']:.2f}", f"{r['value']:,.2f}",
                                f"{r['allocation']:.1f}%"]
                    for ci, v in enumerate(row_vals):
                        styled_label(tbl, v, color=TEXT_PRI).grid(
                            row=ri+1, column=ci, padx=10, pady=3, sticky="w")
                tk.Frame(tbl, bg=BORDER, height=1).grid(
                    row=len(results)+1, column=0, columnspan=5, sticky="ew", pady=4)
                styled_label(tbl, f"TOTAL:  {total:,.2f}", bold=True, color=ACCENT2).grid(
                    row=len(results)+2, column=0, columnspan=5, sticky="w", padx=10)

                # ── pure UI: pie chart ──
                fig = Figure(figsize=(5, 4), dpi=96)
                ax  = fig.add_subplot(111)
                ax.pie([r['value'] for r in results],
                       labels=[r['symbol'] for r in results],
                       autopct='%1.1f%%',
                       colors=CHART_COLORS[:len(results)],
                       startangle=140)
                ax.set_title("Allocation", fontsize=10, fontweight='bold', color=TEXT_PRI)
                fig.tight_layout()
                make_canvas(result_f, fig)

            threading.Thread(target=worker, daemon=True).start()

        styled_button(left, "Fetch Prices", on_fetch, color=ACCENT, width=14).pack(
            fill="x", pady=(10, 0))

    # =========================================================
    #  VIEW 8 — EXPORT
    # =========================================================

    def _show_export_view(self):
        self._clear_content()
        styled_label(self.content, "Export Data", size=14, bold=True).pack(anchor="w", pady=(4, 8))

        panel = card_frame(self.content, padx=24, pady=20)
        panel.pack(fill="x", pady=10)

        styled_label(panel, "Symbol:", color=TEXT_SEC).grid(row=0, column=0, sticky="w", pady=6)
        sym_e = AutocompleteEntry(panel, default="AAPL", width=14)
        sym_e.grid(row=0, column=1, padx=10, pady=6)

        styled_label(panel, "Days:", color=TEXT_SEC).grid(row=1, column=0, sticky="w", pady=6)
        days_e = styled_entry(panel, width=12); days_e.insert(0, "365")
        days_e.grid(row=1, column=1, padx=10, pady=6, ipady=4)

        styled_label(panel, "Save folder:", color=TEXT_SEC).grid(row=2, column=0, sticky="w", pady=6)
        folder_e = styled_entry(panel, width=30)
        folder_e.insert(0, os.path.expanduser("~"))
        folder_e.grid(row=2, column=1, padx=10, pady=6, ipady=4)

        def browse():
            d = filedialog.askdirectory()
            if d: folder_e.delete(0, tk.END); folder_e.insert(0, d)

        styled_button(panel, "Browse", browse, color="#555", width=8).grid(
            row=2, column=2, padx=6)

        fmt_var = tk.StringVar(value="Both")
        styled_label(panel, "Format:", color=TEXT_SEC).grid(row=3, column=0, sticky="w", pady=6)
        for i, opt in enumerate(["CSV", "Excel", "Both"]):
            tk.Radiobutton(panel, text=opt, variable=fmt_var, value=opt,
                           font=("Segoe UI", 10), fg=TEXT_PRI, bg=BG_CARD,
                           selectcolor=BG_DARK, activebackground=BG_CARD).grid(
                               row=3, column=i+1, padx=4, sticky="w")

        status_lbl = styled_label(self.content, "", color=ACCENT2, size=10)
        status_lbl.pack(anchor="w", padx=10, pady=4)

        def on_export():
            symbol, days = self._parse_sym_days(sym_e, days_e)
            if symbol is None: return
            folder = folder_e.get().strip()
            fmt    = fmt_var.get()
            status_lbl.config(text="Fetching data...", fg=TEXT_SEC)

            def on_done(df):
                if df is None:
                    status_lbl.config(text=f"No data found for '{symbol}'.", fg="#D85A30")
                    return

                saved = []
                # ── backend handles all file I/O ──
                if fmt in ("CSV", "Both"):
                    path = export_to_csv(df, symbol, days, folder)
                    saved.append(path)

                if fmt in ("Excel", "Both"):
                    path = export_to_excel(df, symbol, days, folder)
                    if path:
                        saved.append(path)
                    else:
                        status_lbl.config(
                            text="Install openpyxl for Excel: pip install openpyxl",
                            fg="#D85A30")
                        return

                status_lbl.config(text=f"Saved: {',  '.join(saved)}", fg=ACCENT2)
                messagebox.showinfo("Export Complete", "Files saved:\n" + "\n".join(saved))

            self._fetch_bg(symbol, days, on_done)

        styled_button(self.content, "Export Now", on_export, color=ACCENT, width=14).pack(pady=10)


# =============================================================
#  ENTRY POINT
# =============================================================

if __name__ == "__main__":
    app = StockTrackerApp()
    app.mainloop()
