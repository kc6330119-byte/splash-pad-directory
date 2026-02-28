import pandas as pd

existing = pd.read_excel("Outscraper-Clean-Descriptions.xlsx")
print(f"Existing rows: {len(existing)}")

new_raw = pd.read_excel(
    "Outscraper-20260228034825m97_water_park.xlsx",
    usecols=["name", "phone", "website", "company_insights.description"]
)
print(f"New file rows: {len(new_raw)}")

col = "company_insights.description"
new_raw = new_raw[new_raw[col].notna() & (new_raw[col].str.strip() != "")]
print(f"New rows with descriptions: {len(new_raw)}")

combined = pd.concat([existing, new_raw], ignore_index=True)
combined = combined.drop_duplicates(subset="website", keep="first")
print(f"Combined unique rows: {len(combined)}")

combined.to_excel("Outscraper-Clean-Descriptions.xlsx", index=False)
print("Saved: Outscraper-Clean-Descriptions.xlsx")
