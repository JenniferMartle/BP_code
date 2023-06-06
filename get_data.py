import pandas as pd
from sodapy import Socrata

client = Socrata("data.seattle.gov", None)

results = client.get("tmmm-ytt6", limit='42249307',
                     where='usageclass like "Physical" and materialtype like "BOOK" and checkoutyear between 2019 and 2023')

results_df = pd.DataFrame.from_records(results)
results_df.to_csv('SPL_dataset.csv')
print(results_df)
