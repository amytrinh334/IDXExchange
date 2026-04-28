#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os


# In[2]:


sns.set_theme(style="whitegrid")

def validate_and_eda(input_csv, output_csv):
    df = pd.read_csv(input_csv)

    print(f"{'='*60}")
    print(f"ANALYZING: {input_csv}")
    print(f"{'='*60}")

    # Understand dataset structure
    print("\n--- DATASET STRUCTURE ---")
    print(f"Total Rows: {df.shape[0]}")
    print(f"Total Columns: {df.shape[1]}")
    print("\nColumn Data Types:")
    print(df.dtypes)

    # Analyze missing values
    print("\n--- MISSING VALUE ANALYSIS ---")
    null_counts = df.isnull().sum()
    null_pct = (df.isnull().sum() / len(df)) * 100
    null_report = pd.DataFrame({'Null Count': null_counts, 'Percentage (%)': null_pct})

    print("Null Summary Table:")
    print(null_report.sort_values(by='Percentage (%)', ascending=False).head(10))

    # Flag columns > 90% null
    high_null_cols = null_report[null_report['Percentage (%)'] > 90].index.tolist()
    print(f"\nFlagged columns (>90% null): {high_null_cols}")

    # Drop high-null columns unless they are key fields. 
    keep_fields = ['ClosePrice', 'ListPrice', 'OriginalListPrice', 'LivingArea', 'LotSizeAcres', 
                   'BedroomsTotal', 'BathroomsTotalInteger', 'DaysOnMarket', 'YearBuilt', 'CloseDate', 'PurchaseContractDate', 
                   'ListingContractDate', 'ContractStatusChangeDate', 'Latitude', 'Longitude', 'UnparsedAddress', 'StandardStatus', 
                   'PropertyType', 'PropertySubType', 'City', 'Country', 'ListAgentFullName', 'ListOfficeName', 'CountOrParish' 'StateOrProvince', 
                   'CoListOfficeName', 'BuilderName']
    key_fields = ['ClosePrice', 'ListPrice', 'OriginalListPrice', 'LivingArea', 
        'LotSizeAcres', 'BedroomsTotal', 'BathroomsTotalInteger', 
        'DaysOnMarket', 'YearBuilt']

    cols_to_drop = [c for c in high_null_cols if c not in keep_fields]
    df_cleaned = df.drop(columns=cols_to_drop)
    print(f"Dropped {len(cols_to_drop)} columns due to excessive null count")

    # --- optimized graphing loop by sampling ---
    for field in key_fields:
        if field in df.columns:
            # 1. Drop NaNs and get a SAMPLE for plotting
            # Plotting 20,000 rows looks identical to 300,000 but is 15x faster
            plot_data = df[field].dropna()
            if len(plot_data) > 20000:
                plot_sample = plot_data.sample(20000, random_state=42)
            else:
                plot_sample = plot_data

            fig, (ax_hist, ax_box) = plt.subplots(2, sharex=True, 
                                                 gridspec_kw={"height_ratios": (.85, .15)}, 
                                                 figsize=(10, 4))

            # 2. Use a fixed number of bins to prevent the engine from over-calculating
            sns.histplot(plot_sample, ax=ax_hist, bins=50, kde=True, color='teal')
            sns.boxplot(x=plot_sample, ax=ax_box, color='salmon')

            # 3. Calculate outliers on the FULL dataset (so numbers stay accurate)
            q1, q3 = plot_data.quantile(0.25), plot_data.quantile(0.75)
            iqr = q3 - q1
            outlier_count = ((plot_data < (q1 - 1.5 * iqr)) | (plot_data > (q3 + 1.5 * iqr))).sum()

            ax_hist.set_title(f'{field} Distribution | Full Data Outlier Count: {outlier_count}')
            plt.tight_layout()
            plt.show()

            # 4. Clear memory after each plot
        plt.close(fig)

    # 4. Specific Distribution Summary (Targeted Fields)
    target_summary_fields = ['ClosePrice', 'LivingArea', 'DaysOnMarket']
    summary_table = df[target_summary_fields].describe(percentiles=[.25, .5, .75, .90, .95, .99]).T

    # Cleaning up the summary table to include Median clearly
    summary_table = summary_table[['min', 'max', 'mean', '50%', '25%', '75%', '90%', '95%', '99%']]
    summary_table.rename(columns={'50%': 'median'}, inplace=True)

    print("\n--- NUMERIC DISTRIBUTION SUMMARY (ClosePrice, LivingArea, & DaysOnMarket) ---")
    print(summary_table)

    # Final Save (should keep null columns still)
    df.to_csv(output_csv, index=False)
    print(f"\nFiltered dataset saved as: {output_csv}")


# In[3]:


validate_and_eda('combined_listings_residential.csv', 'validated_listings_residential.csv')
validate_and_eda('combined_sold_residential.csv', 'validated_sold_residential.csv')

