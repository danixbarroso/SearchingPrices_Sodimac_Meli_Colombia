import pandas as pd
import matplotlib.pyplot as plt

# Load the uploaded MasterPrice file
master_price_df = pd.read_csv('S:/PT/ac-la/AC_MKB/7. TP ON/E-dealers/01_EspejoDePrecios/v2/Colombia/SearchingPrices_Sodimac_Meli_Colombia/Masterprice_Colombia.csv')

# Load the MasterColombia file
master_colombia_df = pd.read_excel('S:/PT/ac-la/AC_MKB/7. TP ON/E-dealers/01_EspejoDePrecios/v2/Colombia/SearchingPrices_Sodimac_Meli_Colombia/SearchTerms/MasterData_Consolidado.xlsx')
print(master_colombia_df.head)


# Rename columns for easier access and consistency
master_colombia_df.rename(columns={
    "PMCódigo del objeto (SKU)": "SKU",
    "PMNúmero de EAN o código de barras (13 dígitos)": "EAN"
}, inplace=True)

# Convert 'EAN' and 'SKU' columns in master_colombia_df and 'query' column in master_price_df to strings for consistent merging
master_colombia_df['EAN'] = master_colombia_df['EAN'].astype(str)
master_colombia_df['SKU'] = master_colombia_df['SKU'].astype(str)
master_price_df['query'] = master_price_df['query'].astype(str)

# Cleaning up the 'EAN' column in both dfs to remove decimals and make it comparable
master_colombia_df['EAN'] = master_colombia_df['EAN'].str.split('.').str[0]
master_price_df['query'] = master_price_df['query'].str.split('.').str[0]


# Strip whitespace and remove leading zeros for consistent comparison
master_colombia_df['SKU'] = master_colombia_df['SKU'].str.strip().str.lstrip('0')
master_price_df['query'] = master_price_df['query'].str.strip().str.lstrip('0')

# Separate the MasterPrice dataframe based on 'source'
meli_data = master_price_df[master_price_df['source'] == 'Meli']
sodimac_data = master_price_df[master_price_df['source'] == 'Sodimac']

# Debugging: Check the number of rows in each dataframe
print(f"Total de linhas em meli_data: {len(meli_data)}")
print(f"Total de linhas em sodimac_data: {len(sodimac_data)}")

# Debugging: Inspect unique values from 'query' and 'SKU' columns
print("Exemplos de valores em sodimac_data['query']:")
print(sodimac_data['query'].unique()[:10])
print("Exemplos de valores em master_colombia_df['SKU']:")
print(master_colombia_df['EAN'].unique()[:10])

# Merge based on the conditional relationships

# 1. Merge Meli data on 'EAN'
merged_meli = pd.merge(meli_data, master_colombia_df, left_on="query", right_on="EAN", how="inner")
print(f"Total de linhas em merged_meli: {len(merged_meli)}")

# 2. Merge Sodimac data on 'SKU'
merged_sodimac = pd.merge(sodimac_data, master_colombia_df, left_on="query", right_on="EAN", how="inner")
print(f"Total de linhas em merged_sodimac: {len(merged_sodimac)}")

# Concatenate the two merged DataFrames to create the final unified table
final_merged_df = pd.concat([merged_meli, merged_sodimac], ignore_index=True)
print(f"Total de linhas no dataframe final_merged_df: {len(final_merged_df)}")

# Export the final merged DataFrame to a CSV file
output_path = 'S:/PT/ac-la/AC_MKB/7. TP ON/E-dealers/01_EspejoDePrecios/v2/Colombia/SearchingPrices_Sodimac_Meli_Colombia/final_merged_master.csv'
final_merged_df.to_csv(output_path, index=False)

# Indicate that the file has been saved successfully
print(f"Arquivo salvo em: {output_path}")

# Plotting average price per date for Meli and Sodimac
final_merged_df['dateSearch'] = pd.to_datetime(final_merged_df['dateSearch'])
# Calculate average prices
df_avg_price = final_merged_df.groupby(['dateSearch', 'source'])['price'].mean().reset_index()

# Plotting
plt.figure(figsize=(10, 6))
for source in df_avg_price['source'].unique():
    source_data = df_avg_price[df_avg_price['source'] == source]
    plt.plot(source_data['dateSearch'], source_data['price'], label=source) 

plt.xlabel('Data')
plt.ylabel('Média do Preço')
plt.title('Média do Preço por Data para Meli e Sodimac')
plt.legend(title='Fonte')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
