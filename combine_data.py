#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd
import numpy as np
import glob
import os


# In[6]:


def combine_data(input_folder, output_filename):
    all_files = glob.glob(os.path.join(input_folder, "*.csv"))

    if not all_files:
        print(f"No CSV files found in {input_folder}")
        return

    dataframes = []

    print(f"{'='*60}")
    print(f"PROCESSING DATA: {input_folder}")
    print(f"{'='*60}")

    # 1. Row count for each file
    print("--- Individual File Row Counts ---")
    total_expected = 0
    for file in sorted(all_files):
        df = pd.read_csv(file)
        count = len(df)
        total_expected += count
        print(f"{os.path.basename(file)}: {count} rows")
        dataframes.append(df)

    # 2. Row count of the combined dataset after concatenation
    combined_df = pd.concat(dataframes, axis=0, ignore_index=True)
    print(f"\n--- Concatenation Summary ---")
    print(f"Combined dataset row count: {len(combined_df)}")

    # 3. Frequency table of PropertyType before filtering
    print(f"\n--- PropertyType Frequency (Before Filter) ---")
    print(combined_df['PropertyType'].value_counts())

    # 4. Row count after applying PropertyType == 'Residential'
    residential_df = combined_df[combined_df['PropertyType'] == 'Residential'].copy()
    print(f"\n--- Filtering Summary ---")
    print(f"Rows after 'Residential' filter: {len(residential_df)}")

    # 5. Frequency table of PropertyType after filtering
    print(f"\n--- PropertyType Frequency (After Filter) ---")
    print(residential_df['PropertyType'].value_counts())

    # Save new csv output
    residential_df.to_csv(output_filename, index=False)
    print(f"\nFile saved as: {output_filename}\n")


# In[7]:


combine_data('CRMLS Listing Files', 'combined_listings_residential.csv')
combine_data('CRMLS Sold Files', 'combined_sold_residential.csv')


# In[ ]:




