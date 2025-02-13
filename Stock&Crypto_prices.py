{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "6c704537-4bf6-434b-be1a-574ff728dc04",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Server running at: http://127.0.0.1:8080/data\n",
      "Or access from LAN: http://192.168.100.105:8080/data\n",
      " * Serving Flask app '__main__'\n",
      " * Debug mode: off\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.\n",
      " * Running on all addresses (0.0.0.0)\n",
      " * Running on http://127.0.0.1:8080\n",
      " * Running on http://192.168.100.105:8080\n",
      "Press CTRL+C to quit\n"
     ]
    }
   ],
   "source": [
    "from flask import Flask, jsonify  # Import Flask for creating a web server\n",
    "import yfinance as yf  # Import yfinance to get stock and crypto prices\n",
    "import pandas as pd  # Import pandas for handling data\n",
    "\n",
    "# Create a Flask web application\n",
    "app = Flask(__name__)\n",
    "\n",
    "# ✅ List of assets (stocks, crypto, ETFs) that we want to track\n",
    "TICKERS = [\n",
    "    \"BTC-USD\", \"ETH-USD\", \"TRUMP-OFFICIAL-USD\", \"IBIT\", \"MSTR\",  # Cryptocurrencies & Stocks\n",
    "    \"VOO\", \"QQQ\", \"XLV\", \"IAU\", \"VXF\", \"SLV\",  # ETFs (Exchange-Traded Funds)\n",
    "    \"KO\", \"MSFT\", \"TSLA\", \"PLTR\", \"FRHC\", \"NVDA\", \"OKLO\"  # Individual company stocks\n",
    "]\n",
    "\n",
    "def get_market_data():\n",
    "    \"\"\"Fetch real-time market values from Yahoo Finance and handle NaN values.\"\"\"\n",
    "    market_data = {}  # Dictionary to store asset prices\n",
    "\n",
    "    try:\n",
    "        # ✅ Fetch all ticker prices in one request for efficiency\n",
    "        data = yf.download(TICKERS, period=\"1d\", progress=False)[\"Close\"]\n",
    "\n",
    "        # ✅ Process each asset to extract the latest price\n",
    "        for ticker in TICKERS:\n",
    "            try:\n",
    "                # ✅ Get the last available closing price\n",
    "                price = data[ticker].iloc[-1] if ticker in data else None\n",
    "                \n",
    "                # ✅ If the price is missing, fetch it individually as a backup\n",
    "                if pd.isna(price):\n",
    "                    price = yf.Ticker(ticker).history(period=\"1d\")[\"Close\"].iloc[-1]\n",
    "                \n",
    "                # ✅ Store price in dictionary (rounded to 4 decimal places)\n",
    "                market_data[ticker] = round(price, 4) if price else \"No Data\"\n",
    "            except Exception:\n",
    "                # ✅ If an error occurs, mark the asset as \"No Data\"\n",
    "                market_data[ticker] = \"No Data\"\n",
    "\n",
    "        # ✅ Add a fake \"CASH\" asset with a fixed value of 1.00\n",
    "        market_data[\"$$CASH\"] = 1.00\n",
    "\n",
    "    except Exception as e:\n",
    "        # ✅ If an error happens, return the error message\n",
    "        return {\"error\": str(e)}\n",
    "\n",
    "    return market_data  # ✅ Return the dictionary with asset prices\n",
    "\n",
    "# ✅ Homepage Route: Displays a simple message when visiting \"/\"\n",
    "@app.route('/')\n",
    "def home():\n",
    "    return jsonify({\"message\": \"Use /data to get market data\"})\n",
    "\n",
    "# ✅ Data Route: Returns real-time market prices in JSON format\n",
    "@app.route('/data', methods=['GET'])\n",
    "def serve_data():\n",
    "    \"\"\"Serve real-time market data as JSON.\"\"\"\n",
    "    market_data = get_market_data()  # ✅ Fetch the latest market data\n",
    "    return jsonify(market_data)  # ✅ Convert data to JSON and return\n",
    "\n",
    "# ✅ Start the server when the script is run\n",
    "if __name__ == '__main__':\n",
    "    host = \"0.0.0.0\"  # ✅ Allows the server to be accessed from any device on the network\n",
    "    port = 8080  # ✅ Port number to run the server\n",
    "\n",
    "    print(f\"Server running at: http://127.0.0.1:{port}/data\")  # ✅ Local access\n",
    "    print(f\"Or access from LAN: http://192.168.100.105:{port}/data\")  # ✅ Update with your local IP\n",
    "    \n",
    "    try:\n",
    "        app.run(host=host, port=port, debug=False)  # ✅ Start the Flask server\n",
    "    except Exception as e:\n",
    "        print(f\"Server failed to start: {e}\")  # ✅ Print error if the server fails"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:base] *",
   "language": "python",
   "name": "conda-base-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
