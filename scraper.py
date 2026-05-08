import pandas as pd
from datetime import datetime

def clean_data(df):
    """डेटा साफ करना"""
    df = df.drop_duplicates(subset=['Tender_ID'])
    return df

def ai_priority_engine(df):
    """AI Priority Logic"""
    
    def priority(value):
        if value >= 1000000:
            return "HIGH"
        elif value >= 300000:
            return "MEDIUM"
        else:
            return "LOW"

    df['Priority_Score'] = df['Value'].apply(priority)
    return df

def run_production_scraper():
    print("🚀 Haryana Production Scraper Starting...")

    current_date = datetime.now().strftime("%Y-%m-%d")

    raw_data = [
        {
            "Tender_ID": "HR-2026-001",
            "Department": "Irrigation",
            "District": "Karnal",
            "Value": 1500000,
            "Work_Type": "Drain Cleaning",
            "Status": "LIVE",
            "Last_Date": "2026-05-25",
            "Date": current_date
        },
        {
            "Tender_ID": "HR-2026-002",
            "Department": "Police",
            "District": "Hisar",
            "Value": 800000,
            "Work_Type": "Bolero Hiring",
            "Status": "URGENT",
            "Last_Date": "2026-05-15",
            "Date": current_date
        }
    ]

    df = pd.DataFrame(raw_data)

    df = clean_data(df)

    df = ai_priority_engine(df)

    df.to_csv("haryana_tenders_master.csv", index=False)

    print("✅ Tender Data Saved Successfully!")

if __name__ == "__main__":
    run_production_scraper()
