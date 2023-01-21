from get_historical import get_historical
import pandas as pd
historical_obj = get_historical("3045", "ONE_MINUTE", "2021-02-08 09:00", "2021-02-08 09:45")
df = historical_obj.get_data()
print(df)