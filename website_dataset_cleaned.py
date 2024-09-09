#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[21]:


# The raw data string
raw_data = "website_dataset.csv"


# In[26]:


# Read the data into a pandas DataFrame
df = pd.read_csv((raw_data), sep=';')


# In[27]:


df.head


# In[28]:


# Clean and format the data
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)  # Remove leading/trailing whitespace
df = df.apply(lambda x: x.str.capitalize() if x.dtype == "object" else x)  # Capitalize first letter


# In[29]:


# Specific column cleaning
df['main_country'] = df['main_country'].str.capitalize()
df['main_region'] = df['main_region'].str.title()
df['site_name'] = df['site_name'].str.title()
df['s_category'] = df['s_category'].str.title()


# In[31]:


# Format phone numbers (assuming they should all be 11 digits)
df['phone'] = df['phone'].apply(lambda x: f"+{x}" if pd.notnull(x) and len(str(x)) == 11 else x)


# In[33]:


print(df.head())
print("\nData has been cleaned and saved to 'website_dataset_cleaned.csv'")


# In[34]:


# Save the cleaned data to a CSV file
df.to_csv('website_dataset_cleaned.csv', index=False)


# In[ ]:




