import requests
import streamlit as st
import matplotlib.pyplot as plt
import random

api_key = '6XCFUOW5JB5B23H2'

def get_realtime_stock_data(symbol):
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}'
    try:
        response = requests.get(url)
        data = response.json()
        if 'Global Quote' in data:
            stock_info = data['Global Quote']
            st.subheader("Real-Time Stock Data")
            st.write(f"Symbol: {stock_info['01. symbol']}")
            st.write(f"Open: {stock_info['02. open']}")
            st.write(f"High: {stock_info['03. high']}")
            st.write(f"Low: {stock_info['04. low']}")
            st.write(f"Price: {stock_info['05. price']}")
            st.write(f"Volume: {stock_info['06. volume']}")
            st.write(f"Last Trading Day: {stock_info['07. latest trading day']}")
            st.write(f"Previous Close: {stock_info['08. previous close']}")
            st.write(f"Change: {stock_info['09. change']}")
            st.write(f"Change Percent: {stock_info['10. change percent']}")
                 
            close_price = float(stock_info['08. previous close'])
            current_price = float(stock_info['05. price'])
            average_price = (close_price + current_price) / 2

            st.write(f"Closing Price Average: {average_price}")
            # Plot the real-time price using matplotlib
            prices = [float(stock_info['02. open']), float(stock_info['03. high']), float(stock_info['04. low']), float(stock_info['05. price'])]
            labels = ['Open', 'High', 'Low', 'Price']

            fig, ax = plt.subplots()
            ax.bar(labels, prices)
            ax.set_xlabel('Price Type')
            ax.set_ylabel('Price')
            ax.set_title(f"{symbol} Real-Time Stock Prices")
            plt.tight_layout()

            # Display the graph
            st.pyplot(fig)

            # Plot a pie chart of price type distribution
            fig2, ax2 = plt.subplots()
            types = ['Open', 'High', 'Low', 'Price']
            ax2.pie(prices, labels=types, autopct='%1.1f%%')
            ax2.set_title(f"{symbol} Price Type Distribution")
            plt.tight_layout()

            # Display the pie chart
            st.pyplot(fig2)

            # Track the symbol
            track_symbol(symbol)

        else:
            st.warning("No real-time stock data found for the symbol.")
    except requests.exceptions.RequestException as e:
        st.error(str(e))

def get_historical_stock_data(symbol):
    # Add your code to retrieve historical stock data here
    pass

def track_symbol(symbol):
    tracked_symbols = st.session_state.get('tracked_symbols', [])
    tracked_symbols.append(symbol)
    st.session_state['tracked_symbols'] = tracked_symbols

def main():
    st.title("Stock Market Data App")
    option = st.radio("Data Type", ("Real-Time", "Historical"))

    if option == "Real-Time":
        symbol = st.text_input("Enter Stock Symbol:").upper()
        if symbol:
            get_realtime_stock_data(symbol)
    elif option == "Historical":
        symbol = st.text_input("Enter Stock Symbol:").upper()
        if symbol:
            get_historical_stock_data(symbol)
            if st.button("Show Graph"):
                get_historical_stock_data(symbol)
                # Track the symbol
                track_symbol(symbol)

    # Display the tracked symbols
    tracked_symbols = st.session_state.get('tracked_symbols', [])
    if tracked_symbols:
        st.subheader("Tracked Symbols")
        for symbol in tracked_symbols:
            unique_key = f"track_{symbol}_{random.randint(0, 1000000)}"
            if st.button(symbol, key=unique_key):
                pass

if __name__ == '__main__':
    main()
