#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


# Added verification??

import ssl
import certifi

ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())


# In[3]:


# Fetch mortgage data from FRED

url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"
mortgage = pd.read_csv(url, parse_dates=['observation_date'])
mortgage.columns = ['date', 'rate_30yr_fixed']


# In[4]:


# Resample weekly rates to monthly averages

mortgage['year_month'] = mortgage['date'].dt.to_period('M') 
mortgage_monthly = (
mortgage.groupby('year_month')['rate_30yr_fixed'].mean().reset_index() )


# In[5]:


# Create a matching year_month key on the MLS datasets

sold = pd.read_csv("validated_sold_residential.csv")
# Sold dataset — key off CloseDate
sold['year_month'] = pd.to_datetime(sold['CloseDate']).dt.to_period('M')

listings = pd.read_csv("validated_listings_residential.csv")
# Listings dataset — key off ListingContractDate
listings['year_month'] = pd.to_datetime(listings['ListingContractDate']).dt.to_period('M')


# In[6]:


# Merge datasets

sold_with_rates = sold.merge(mortgage_monthly, on='year_month', how='left')
listings_with_rates = listings.merge(mortgage_monthly, on='year_month', how='left')


# In[7]:


# Validate merge -- check for any unmatched rows (rate should not be null)

print(sold_with_rates['rate_30yr_fixed'].isnull().sum())
print(listings_with_rates['rate_30yr_fixed'].isnull().sum())


# In[8]:


print(
sold_with_rates[
['CloseDate', 'year_month', 'ClosePrice', 'rate_30yr_fixed']
].head()
)


# In[9]:


sold_with_rates.to_csv('sold_with_rates.csv', index=False)
listings_with_rates.to_csv('listings_with_rates.csv', index=False)

