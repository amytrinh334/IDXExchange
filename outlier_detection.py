#!/usr/bin/env python
# coding: utf-8

# In[19]:


import pandas as pd
import numpy as np


# In[20]:


listings = pd.read_csv('cleaned_listings.csv')
sold = pd.read_csv('cleaned_sold.csv')


# In[21]:


cols = ['ClosePrice', 'LivingArea', 'DaysOnMarket']
for col in cols:
    q1_listings = listings[col].quantile(0.25) 
    q3_listings = listings[col].quantile(0.75) 
    iqr_listings = q3_listings - q1_listings
    lower_listings = q1_listings - 1.5 * iqr_listings
    upper_listings = q3_listings + 1.5 * iqr_listings
    listings[f'{col.lower()}_outlier_flag'] = (listings[col] < lower_listings) | (listings[col] > upper_listings)

    q1_sold = sold[col].quantile(0.25) 
    q3_sold = sold[col].quantile(0.75) 
    iqr_sold = q3_sold - q1_sold
    lower_sold = q1_sold - 1.5 * iqr_sold
    upper_sold = q3_sold + 1.5 * iqr_sold
    sold[f'{col.lower()}_outlier_flag'] = (sold[col] < lower_sold) | (sold[col] > upper_sold)


# In[22]:


print("Number of Listings: " + str(len(listings)))

print("Outlier Count: ")
listings[['closeprice_outlier_flag', 'livingarea_outlier_flag', 'daysonmarket_outlier_flag']].sum()


# In[23]:


print("Number of Sold: " + str(len(sold)))

print("Outlier Count: ")
sold[['closeprice_outlier_flag', 'livingarea_outlier_flag', 'daysonmarket_outlier_flag']].sum()


# In[25]:


listings.to_csv('outlier_flagged_listings.csv', index=False)
sold.to_csv('outlier_flagged_sold.csv', index=False)


# In[27]:


outlier_listings = listings.copy()
outlier_sold = sold.copy()

outlier_listings = outlier_listings[~(outlier_listings['closeprice_outlier_flag'] | outlier_listings['livingarea_outlier_flag'] | outlier_listings['daysonmarket_outlier_flag'])]
outlier_sold = outlier_sold[~(outlier_sold['closeprice_outlier_flag'] | outlier_sold['livingarea_outlier_flag'] | outlier_sold['daysonmarket_outlier_flag'])]


# In[33]:


print("Listings Dataset: ")
print("Number of Rows Before Outlier Removal: " + str(len(listings)))
print("Number of Rows After Outlier Removal: " + str(len(outlier_listings)))
print("Number of Rows Removed: " + str(len(listings) - len(outlier_listings)))

print("\nMean Close Price Before Outlier Removal: " + str(listings['ClosePrice'].mean()))
print("Mean Close Price After Outlier Removal: " + str(outlier_listings['ClosePrice'].mean()))
print("Difference in Mean Close Price: " + str(outlier_listings['ClosePrice'].mean() - listings['ClosePrice'].mean()))

print("\nMean Living Area Before Outlier Removal: " + str(listings['LivingArea'].mean()))
print("Mean Living Area After Outlier Removal: " + str(outlier_listings['LivingArea'].mean()))
print("Difference in Mean Living Area: " + str(outlier_listings['LivingArea'].mean() - listings['LivingArea'].mean()))

print("\n------------------------------\n")

print("Sold Dataset: ")
print("Number of Rows Before Outlier Removal: " + str(len(sold)))
print("Number of Rows After Outlier Removal: " + str(len(outlier_sold)))
print("Number of Rows Removed: " + str(len(sold) - len(outlier_sold)))

print("\nMean Close Price Before Outlier Removal: " + str(sold['ClosePrice'].mean()))
print("Mean Close Price After Outlier Removal: " + str(outlier_sold['ClosePrice'].mean()))
print("Difference in Mean Close Price: " + str(outlier_sold['ClosePrice'].mean() - sold['ClosePrice'].mean()))

print("\nMean Living Area Before Outlier Removal: " + str(sold['LivingArea'].mean()))
print("Mean Living Area After Outlier Removal: " + str(outlier_sold['LivingArea'].mean()))
print("Difference in Mean Living Area: " + str(outlier_sold['LivingArea'].mean() - sold['LivingArea'].mean()))


# In[34]:


outlier_listings.to_csv('final_cleaned_listings.csv', index=False)
sold.to_csv('final_cleaned_sold.csv', index=False)

