from flask import Flask, jsonify
import yfinance as yf

app = Flask(__name__)

symbols = {
    "ES": "ES=F",
    "NQ": "NQ=F",
    "YM": "YM=F",
    "CL": "CL=F",
    "GC": "GC=F",
    "VIX": "^VIX"
}

@app.route("/")
def home():
    return "TEA Futures API Running"

@app.route("/markets")
def markets():

    data = {}

    for key, ticker in symbols.items():
        try:
            t = yf.Ticker(ticker)
            hist = t.history(period="1d")

            if not hist.empty:
                last = hist["Close"].iloc[-1]
                open_price = hist["Open"].iloc[0]

                change = last - open_price
                pct = (change / open_price) * 100

                data[key] = {
                    "price": round(float(last),2),
                    "change": round(float(change),2),
                    "pct": round(float(pct),2)
                }

        except Exception as e:
            data[key] = {"error": "data unavailable"}

    return jsonify(data)

if __name__ == "__main__":
    app.run()
