import yfinance as yf


def get_financial_stock_assets():
    """
    Returns:
        stocks (list of str): List of stock ticker symbols
        correlation_matrix (np.ndarray): Correlation matrix of daily percentage returns
        stock_pairs
    """
    # Define the date range for historical data
    start_date = "2024-01-01"
    end_date = "2025-01-01"

    # List of stock ticker symbols to analyze
    stocks = ["AAPL", "MSFT", "TSLA", "JPM", "XOM", 
               "GOOGL", "NFLX", "NVDA", "PFE", "AMZN"]

    # Download daily closing price data for the selected stocks
    price_data = yf.download(stocks, start=start_date, end=end_date)["Close"]

    # Calculate daily percentage returns and remove missing values
    daily_returns = price_data.pct_change().dropna()

    # Compute the correlation matrix of the daily returns and convert to NumPy array
    correlation_matrix = daily_returns.corr().values

    # Calculate all stock pairs
    stock_pairs = {
        (i, j) for i in range(len(stocks)) for j in range(i + 1, len(stocks))
    }

    return stocks, correlation_matrix, stock_pairs