from datetime import datetime
import yfinance as yf

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

def get_stock_price(ticker:str) -> dict:
    """Retrieves current stock price and saves to session state."""
    print(f"--- Tool: get_stock_price, Ticker: {ticker} ---")

    try: 
        stock = yf.Ticker(ticker)
        current_price = stock.info['regularMarketPrice']

        if current_price is None:
            return {
                "status": "error",
                "message": f"Could not retrieve price for ticker '{ticker}'."
            }
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return {
            "status": "success",
            "ticker": ticker,
            "price": current_price,
            "time": current_time
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error fetching stock data: {str(e)}"
        }
    
    
stock_analyst = Agent(
    name="stock_analyst",
    model=LiteLlm(model="ollama_chat/qwen3:4b"),
    description="An agent that can look up stock prices and track them over time.",
    instruction="""
    You are a helpful stock market assistant that helps users track their stocks of interest.
    
    When asked about stock prices:
    1. Use the get_stock_price tool to fetch the latest price for the requested stock(s)
    2. Format the response to show each stock's current price and the time it was fetched
    3. If a stock price couldn't be fetched, mention this in your response
    
    Example response format:
    "Here are the current prices for your stocks:
    - GOOG: $175.34 (updated at 2024-04-21 16:30:00)
    - TSLA: $156.78 (updated at 2024-04-21 16:30:00)
    - META: $123.45 (updated at 2024-04-21 16:30:00)"

    If the user asked about anything else, delegate the task to the manager agent.
    """,
    tools=[get_stock_price],
)