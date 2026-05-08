import pandas as pd
import random
from datetime import datetime, timedelta

districts = [
    "Ambala","Bhiwani","Charkhi Dadri","Faridabad",
    "Fatehabad","Gurugram","Hisar","Jhajjar",
    "Jind","Kaithal","Karnal","Kurukshetra",
    "Mahendragarh","Nuh","Palwal","Panchkula",
    "Panipat","Rewari","Rohtak","Sirsa",
    "Sonipat","Yamunanagar"
]

departments = [
    "PWD",
    "Irrigation Department",
    "Forest Department",
    "Police Department",
    "Health Department",
    "Education Department",
    "Agriculture Department",
    "Transport Department",
    "Municipal Corporation",
    "Rural Development",
    "Urban Development",
    "Electricity Board",
    "Water Supply Department",
    "Tourism Department",
    "Animal Husbandry",
    "Mining Department",
    "Fire Department",
    "Public Health Engineering",
    "Smart City Mission",
    "HSIIDC"
]

work_types = [
    "Road Construction",
    "School Building",
    "Hospital Equipment",
    "Water Pipeline",
    "Forest Cleaning",
    "CCTV Installation",
    "Street Light Setup",
    "JCB Hiring",
    "Bolero Hiring",
    "Scorpio Hiring",
    "Drain Construction",
    "Bridge Repair",
    "Computer Supply",
    "Office Furniture",
    "Vehicle Hiring",
    "Security Services",
    "Cleaning Services",
    "Solar Panel Installation"
]

rows = []

for i in range(1, 501):

    value = random.randint(1000, 100000000)

    if value >= 50000000:
        priority = "HIGH"
    elif value >= 10000000:
        priority = "MEDIUM"
    else:
        priority = "LOW"

    row = {
        "Tender_ID": f"HR-2026-{i:04}",
        "Department": random.choice(departments),
        "District": random.choice(districts),
        "Value": value,
        "Work_Type": random.choice(work_types),
        "Status": random.choice(["LIVE", "LIVE", "LIVE", "CLOSED"]),
        "Priority_Score": priority,
        "Last_Date": (
            datetime.today() +
            timedelta(days=random.randint(1, 60))
        ).strftime("%Y-%m-%d")
    }

    rows.append(row)

df = pd.DataFrame(rows)

df.to_csv(
    "haryana_tenders_master.csv",
    index=False
)

print("DONE")
