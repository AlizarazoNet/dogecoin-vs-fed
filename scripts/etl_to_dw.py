import pandas as pd
import yfinance as yf
from datetime import datetime
from fredapi import Fred
import os
# --- Settings ---
START_DATE = datetime(2020, 1, 1)
END_DATE = datetime.today()
FRED_API_KEY = "6768b112bc2c95e9b76ffc5ce067a455"

# --- Extract ---

def fetch_dogecoin_data(start, end):
    doge = yf.download('DOGE-USD', start=start, end=end)
    doge = doge[['Close']]
    doge_reset = doge.reset_index()
    # Flatten possible MultiIndex
    doge_reset.columns = ['Date', 'Dogecoin_Close']
    return doge_reset

def fetch_fed_rate_data(start, end, api_key):
    fred = Fred(api_key=api_key)
    fed_rate = fred.get_series('FEDFUNDS', observation_start=start, observation_end=end)
    fed_rate = fed_rate.rename("Fed_Funds_Rate").to_frame()
    fed_reset = fed_rate.reset_index()
    fed_reset.columns = ['Date', 'Fed_Funds_Rate']
    return fed_reset

# --- Transform and Merge ---

def merge_data(doge_df, fed_df):
    combined = pd.merge(doge_df, fed_df, on="Date", how="inner")
    combined.dropna(inplace=True)
    return combined

# --- Load ---

def save_to_csv(doge_df, fed_df, combined_df):
    # Make sure 'data' directory exists
    os.makedirs("data/prepared", exist_ok=True)
    
    doge_df.to_csv("data/prepared/dogecoin_data.csv", index=False)
    fed_df.to_csv("data/prepared/fed_funds_rate.csv", index=False)
    combined_df.to_csv("data/prepared/combined_doge_fed.csv", index=False)
    print("✅ All datasets saved to /data")



# --- Run ETL Pipeline ---

def run_etl():
    print("🚀 Running ETL pipeline...")
    doge_df = fetch_dogecoin_data(START_DATE, END_DATE)
    fed_df = fetch_fed_rate_data(START_DATE, END_DATE, FRED_API_KEY)
    combined_df = merge_data(doge_df, fed_df)
    save_to_csv(doge_df, fed_df, combined_df)

if __name__ == "__main__":
    run_etl()
