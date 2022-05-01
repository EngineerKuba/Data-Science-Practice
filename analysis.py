#%% Import libraries
import os
import pandas as pd
import re

# %% Merge all data to one file 

data_path = "./Sales_Data/"

filepaths = [data_path + f for f in os.listdir(data_path) if f.endswith('.csv')]
df = pd.concat(map(pd.read_csv, filepaths))

df.to_csv("merged_data.csv", index=False)

#%% Besst month for sales + amount
## Data cleanup
merged_data = pd.read_csv("merged_data.csv")

# drop nan
merged_data.dropna(how="all", inplace=True)

# delete duplicate headers made while merging files
merged_data = merged_data[merged_data.Product != "Product"]

# add month column as int
merged_data["Month"] = merged_data["Order Date"].str[0:2].astype('int')

# add a sales column
merged_data["Sales"] = merged_data["Price Each"].astype('float') * merged_data["Quantity Ordered"].astype('int')

# rearranging the columns
cols = list(merged_data.columns)
merged_data = merged_data[cols[0:4] + [cols[-1]] + cols[4:7]]

# find month with best sales 
sales_result = merged_data.groupby("Month").sum().sort_values("Sales", ascending=False)
best_sale = sales_result.head(1)
print(f"Best sale result was\n {best_sale}")

# %% Plot sales per month
import matplotlib.pyplot as plt

sales_result.sort_values("Month", inplace=True)
sales_result.reset_index(inplace=True)
sales_result.plot(x ='Month', y='Sales', kind = 'line')
plt.ylabel("Sales in m$")
plt.show()

# %% What city had highest No of sales
