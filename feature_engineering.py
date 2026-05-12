#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[ ]:


listings = pd.read_csv('cleaned_listings.csv').copy()
sold = pd.read_csv('cleaned_sold.csv').copy()


# In[3]:


listings["PriceRatio"] = listings['ClosePrice'] / listings['OriginalListPrice']
sold["PriceRatio"] = sold['ClosePrice'] / sold['OriginalListPrice']


# In[4]:


listings['PricePerSqFt'] = listings['ClosePrice'] / listings['LivingArea']
sold['PricePerSqFt'] = sold['ClosePrice'] / sold['LivingArea']


# In[19]:


listings["DaysOnMarket"] = (pd.to_datetime(listings['CloseDate']) - pd.to_datetime(listings['ListingContractDate'])).dt.days
sold["DaysOnMarket"] = (pd.to_datetime(sold['CloseDate']) - pd.to_datetime(sold['ListingContractDate'])).dt.days


# In[16]:


listings['CloseDate'] = pd.to_datetime(listings['CloseDate'])
listings = listings.assign(
    Year=listings['CloseDate'].dt.year,
    Month=listings['CloseDate'].dt.month,
    YrMo=listings['CloseDate'].dt.year.astype(str) + '-' + listings['CloseDate'].dt.month.astype(str)
)

sold['CloseDate'] = pd.to_datetime(sold['CloseDate'])
sold = sold.assign(
    Year=sold['CloseDate'].dt.year,
    Month=sold['CloseDate'].dt.month,
    YrMo=sold['CloseDate'].dt.year.astype(str) + '-' + sold['CloseDate'].dt.month.astype(str)
)


# In[17]:


listings["CloseToOriginalRatio"] = listings['ClosePrice'] / listings['OriginalListPrice']
sold["CloseToOriginalRatio"] = sold['ClosePrice'] / sold['OriginalListPrice']


# In[20]:


listings["ListToContractDays"] = (pd.to_datetime(listings['PurchaseContractDate']) - pd.to_datetime(listings['ListingContractDate'])).dt.days
sold["ListToContractDays"] = (pd.to_datetime(sold['PurchaseContractDate']) - pd.to_datetime(sold['ListingContractDate'])).dt.days


# In[21]:


listings["ContractToCloseDays"] = (pd.to_datetime(listings['CloseDate']) - pd.to_datetime(listings['PurchaseContractDate'])).dt.days
sold["ContractToCloseDays"] = (pd.to_datetime(sold['CloseDate']) - pd.to_datetime(sold['PurchaseContractDate'])).dt.days


# In[29]:


listings[['PriceRatio', 'PricePerSqFt', 'DaysOnMarket', 'CloseToOriginalRatio', 'ListToContractDays', 'ContractToCloseDays']]


# In[30]:


sold[['PriceRatio', 'PricePerSqFt', 'DaysOnMarket', 'CloseToOriginalRatio', 'ListToContractDays', 'ContractToCloseDays']]


# In[40]:


#since listings is mostly nulls and sold has actual infomation, we can do the market metrics on that instead
propertysubtype_summary = sold.groupby('PropertySubType').agg({
    'PriceRatio': 'mean',
    'PricePerSqFt': 'mean',
    'DaysOnMarket': 'median',
    'CloseToOriginalRatio': 'mean',
    'ListToContractDays': 'median',
    'ContractToCloseDays': 'median',
    'ClosePrice': 'count' # number of sold properties in each subtype

})

propertysubtype_summary.sort_values(by='ClosePrice', ascending=False)


# In[39]:


competitive_summary = sold.groupby('ListOfficeName').agg({
    'PriceRatio': 'mean',
    'PricePerSqFt': 'mean',
    'DaysOnMarket': 'median',
    'CloseToOriginalRatio': 'mean',
    'ListToContractDays': 'median',
    'ContractToCloseDays': 'median',
    'ClosePrice': 'count' # number of sold properties in each subtype

})

competitive_summary.sort_values(by='ClosePrice', ascending=False).head(10)


# #would it be better to merge the listing and sold datasets now? keeping mainly the sold ones?
