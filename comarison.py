import pandas as pd

# Load CSV 1 into dataframe
df1 = pd.read_csv("doc1.csv")

# Load CSV 2 into dataframe
df2 = pd.read_csv("doc2.csv")

# Merge dataframes on 'id' column
merged_df = pd.merge(df1, df2, on='id')
print(merged_df)

# Compare 'Speed' and 'Velocity' columns
comparison_result = merged_df['Speed'] > merged_df['Velocity']

# Iterate over each row in the comparison_result Series
for index, result in comparison_result.items():
    if result:
        print(f"ID: {merged_df.at[index, 'id']}, Date: {merged_df.at[index, 'Date']}, Speed: {merged_df.at[index, 'Speed']}, Velocity: {merged_df.at[index, 'Velocity']}")
