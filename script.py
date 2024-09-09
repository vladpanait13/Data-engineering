#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


# Load datasets
facebook_df = pd.read_csv('facebook_dataset.csv', error_bad_lines = False)
google_df = pd.read_csv('google_dataset.csv', error_bad_lines = False)
website_df = pd.read_csv('website_dataset_cleaned.csv')


# In[9]:


# Normalize and clean columns for consistency
def normalize_phone(phone):
    return phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '') if pd.notnull(phone) else phone

def normalize_name(name):
    return name.lower().strip() if pd.notnull(name) else name


# In[10]:


facebook_df['phone'] = facebook_df['phone'].apply(normalize_phone)
google_df['phone'] = google_df['phone'].apply(normalize_phone)
website_df['phone'] = website_df['phone'].apply(normalize_phone)


# In[11]:


facebook_df['name'] = facebook_df['name'].apply(normalize_name)
google_df['name'] = google_df['name'].apply(normalize_name)
website_df['site_name'] = website_df['site_name'].apply(normalize_name)


# In[16]:


# Join datasets on primary key `domain/root_domain`
merged_df = pd.merge(facebook_df, google_df, left_on='domain', right_on='domain', how='outer', suffixes=('_fb', '_gg'))
merged_df = pd.merge(merged_df, website_df, left_on='domain', right_on='root_domain', how='outer')


# In[17]:


# Resolve conflicts: Prioritize Google > Facebook > Website
def resolve_conflict(primary, secondary, tertiary):
    if pd.notnull(primary):
        return primary
    elif pd.notnull(secondary):
        return secondary
    else:
        return tertiary


# In[18]:


# Example: Resolving the 'name' field conflict
merged_df['final_name'] = merged_df.apply(lambda row: resolve_conflict(row['name_gg'], row['name_fb'], row['site_name']), axis=1)


# In[19]:


# Resolve conflicts for key columns
merged_df['final_category'] = merged_df.apply(lambda row: resolve_conflict(row['category'], row['categories'], row['s_category']), axis=1)
merged_df['final_phone'] = merged_df.apply(lambda row: resolve_conflict(row['phone_gg'], row['phone_fb'], row['phone']), axis=1)


# In[20]:


# Address resolution
def resolve_address(row):
    # Combine the address components, preferring Google, then Facebook, then Website
    country = resolve_conflict(row['country_name_gg'], row['country_name_fb'], row['main_country'])
    region = resolve_conflict(row['region_name_gg'], row['region_name_fb'], row['main_region'])
    city = resolve_conflict(row['city_gg'], row['city_fb'], row['main_city'])
    address = resolve_conflict(row['address_gg'], row['address_fb'], None)
    return f"{address}, {city}, {region}, {country}"


# In[21]:


merged_df['final_address'] = merged_df.apply(resolve_address, axis=1)


# In[22]:


# Select final columns to keep in the new dataset
final_df = merged_df[['domain', 'final_name', 'final_category', 'final_phone', 'final_address']]


# In[23]:


# Rename columns for clarity
final_df.columns = ['Domain', 'Company Name', 'Category', 'Phone', 'Address']


# In[24]:


# Save the final dataset
final_df.to_csv('combined_dataset.csv', index=False)


# In[26]:


print("Combined dataset created successfully and saved as 'combined_dataset.csv'")


# In[ ]:




