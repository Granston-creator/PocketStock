import streamlit as st
import streamlit as st
import yfinance as yf
import pandas_ta as ta
from google import genai
from st_paywall import add_auth  # <-- 1. Import the Cashier


add_auth(required=True)
API_KEY = st.secrets["GEMINI_KEY"]
client = genai.Client(api_key=API_KEY)


st.title("🤖 AI Stock Analyst (Premium Edition)")

# --- USER INPUT ---
ticker = st.sidebar.text_input("Stock Ticker:", "TSLA").upper()

if ticker:
    # --- GET MATH DATA ---
    data = yf.Ticker(ticker).history(period="6mo")
    if not data.empty:
        data['RSI'] = ta.rsi(data['Close'], length=14)
        current_price = float(data['Close'].dropna().iloc[-1])
        current_rsi = float(data['RSI'].dropna().iloc[-1])

        # --- SHOW THE CHART ---
        st.subheader(f"{ticker} Performance")
        st.line_chart(data['Close'])

        # --- THE AI CHAT BOX ---
        st.subheader("AI Financial Analysis")
        with st.spinner("AI is searching news and analyzing..."):
            prompt = f"Analyze {ticker} at ${current_price:.2f} with an RSI of {current_rsi:.2f}. Search for the latest news and tell me if it's a Buy, Sell, or Hold."
            
            response = client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=prompt,
                config={"tools": [{"google_search": {}}]}
            )
            
            st.chat_message("assistant").write(response.text)
    else:
        st.error("Ticker not found.")