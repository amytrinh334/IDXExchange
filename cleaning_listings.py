#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


listings = pd.read_csv('listings_with_rates.csv')
listings.columns


# In[3]:


print("Row Count Before Cleaning: " + str(len(listings)))


# In[4]:


#Remove unnecessary or redundant columns
keep_fields = ['ClosePrice', 'ListPrice', 'OriginalListPrice', 'LivingArea', 'LotSizeAcres', 
                   'BedroomsTotal', 'BathroomsTotalInteger', 'DaysOnMarket', 'YearBuilt', 'CloseDate', 'PurchaseContractDate', 
                   'ListingContractDate', 'ContractStatusChangeDate', 'Latitude', 'Longitude', 'UnparsedAddress', 'StandardStatus', 
                   'PropertyType', 'PropertySubType', 'City', 'Country', 'ListAgentFullName', 'ListOfficeName', 'CountyOrParish' 'StateOrProvince', 
                   'CoListOfficeName', 'BuilderName']
listings = listings.drop(columns=[col for col in listings.columns if col not in keep_fields])
listings.columns


# In[5]:


 #Convert date fields to datetime format
date_fields = ['CloseDate', 'PurchaseContractDate', 'ListingContractDate', 'ContractStatusChangeDate']
for field in date_fields:
    listings[field] = pd.to_datetime(listings[field], errors='coerce')
listings


# In[6]:


#Validate the logical order of date fields
listings['listing_after_close_flag'] = listings['ListingContractDate'] > listings['PurchaseContractDate'] #ListingContractDate should precede (<) PurchaseContractDate
listings['purchase_after_close_flag'] = listings['PurchaseContractDate'] > listings['CloseDate'] #PurchaseContractDate should precede (<) CloseDate
#df['negative_timeline_flag'] = what is negative timeline?
listings[['listing_after_close_flag', 'purchase_after_close_flag']].sum() 



# In[7]:


 # Analyze missing values
print("\n--- MISSING VALUE ANALYSIS ---")
null_counts = listings.isnull().sum()
null_pct = (listings.isnull().sum() / len(listings)) * 100
null_report = pd.DataFrame({'Null Count': null_counts, 'Percentage (%)': null_pct})

print("Null Summary Table:")
print(null_report.sort_values(by='Percentage (%)', ascending=False))


# In[8]:


#Remove unnesscary columns
listings = listings.drop(columns=['BuilderName', 'CoListOfficeName']) #too many null values to keep, not needed to feature engineering later
listings.columns


# In[9]:


#Handle missing values appropriately

#ClosePrice, CloseDate, and PurchaseContractDate nulls values don't need to be filled --> means that it just hasn't been sold yet so no data

#Flag records with missing coordinates (Latitude or Longitude is null)
listings['missing_coordinates_flag'] = (listings['Latitude'].isnull()) | (listings['Longitude'].isnull())

#Flag Latitude = 0 or Longitude = 0 (sentinel null values)
listings['sentinenl_null_flag'] = (listings['Latitude'] == 0) | (listings['Longitude'] == 0)

#Flag Longitude > 0 errors (California coordinates should be negative)
listings['wrong_longitude_flag'] = listings['Longitude'] > 0

#Flag out-of-state or implausible coordinates

#For CA
lat_bounds = (32, 42)
long_bounds = (-124, -114)

listings['out_of_state_flags'] = (~(listings['Latitude'].between(*lat_bounds))) | (\
                             ~(listings['Longitude'].between(*long_bounds)))

print(listings[['missing_coordinates_flag', 'sentinenl_null_flag', 'wrong_longitude_flag','out_of_state_flags']].sum())


# In[10]:


#Remove or flag invalid numeric values: ClosePrice <= 0, LivingArea <= 0, DaysOnMarket < 0, negative Bedrooms or Bathrooms
listings['neg_closeprice_flag'] = listings['ClosePrice'] <= 0
listings['neg_daysonmarket_flag'] = listings['DaysOnMarket'] < 0 
listings['neg_livingarea_flag'] = listings['LivingArea'] <= 0
listings['neg_bedbath_flag'] = (listings['BedroomsTotal'] < 0) | (listings['BathroomsTotalInteger'] < 0)

listings[['neg_closeprice_flag', 'neg_daysonmarket_flag','neg_livingarea_flag', 'neg_bedbath_flag']].sum()


# In[14]:


#remove rows 
listings = listings[~listings['neg_daysonmarket_flag']]
listings = listings[~listings['neg_livingarea_flag']]
listings[['neg_daysonmarket_flag','neg_livingarea_flag']].sum()


# In[ ]:





# In[ ]:





# In[ ]:





# In[15]:


 # Analyze missing values
print("\n--- MISSING VALUE ANALYSIS ---")
null_counts = listings.isnull().sum()
null_pct = (listings.isnull().sum() / len(listings)) * 100
null_report = pd.DataFrame({'Null Count': null_counts, 'Percentage (%)': null_pct})

print("Null Summary Table:")
print(null_report.sort_values(by='Percentage (%)', ascending=False))


# In[12]:


#Ensure numeric fields are properly typed


# In[ ]:




