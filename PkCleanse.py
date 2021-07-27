#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype


# In[2]:


def ExceptionMsg(field,reason):
    return "Exception for "+field+' - '+reason
    


# In[3]:



df = pd.read_csv ('Pakistan Largest Ecommerce Dataset.csv')
dfAllExceptions = pd.DataFrame()
df.head()


# In[4]:


#Understanding the file/data structure
df.info()


# In[5]:


df.isnull().sum()


# In[34]:


#analyse to have a better the categorical columns
cat_col = df.select_dtypes(include=['object'])
values = cat_col.nunique()
print(values)


# In[44]:


#Showing the unique values in the column if there are within a certain viewable # e.g. 30
for column in cat_col:
    if df[column].nunique() < 30:
        print('Feature: ', column)
        print('Feature Values: ', df[column].unique())
    else:
        print('Feature: ', column)
        print('Feature with too many unique values, displaying Counts only: ', df[column].nunique())
    print('---------------------------')
        
        


# In[6]:



#Cleansing starts here
#Removing the empty columns with no headers
df.drop(df.filter(regex="Unname"),axis=1, inplace=True)


# In[7]:


df.head()
print("Before Cleansing # of rows ",df.shape)


# In[8]:


#Remove empty rows at the end of the file
df=df.dropna(how='all')
print("After Cleansing empty # rows at the end of the file ",df.shape)


# In[9]:


#Dropping those with empty category_name_1
filter = df["category_name_1"].isnull() 
dfexception_cat_name = pd.DataFrame()
dfexception_cat_name = df[filter].copy()
dfexception_cat_name["Exception"] = ExceptionMsg("category_name_1","Empty Field") 


# In[10]:


df=df.dropna(subset=["category_name_1"])
print("After Cleansing category_name_1 which are empty ",df.shape)


# In[11]:


#Dropping those with empty Customer ID
filter = df["Customer ID"].isnull() 
dfexception_cust_id = pd.DataFrame()
dfexception_cust_id = df[filter].copy()
dfexception_cust_id["Exception"] = ExceptionMsg("Customer ID","Empty Field") 


# In[12]:


df=df.dropna(subset=["Customer ID"])
print("After Cleansing Customer ID which are empty ",df.shape)


# In[13]:


#Dropping those with empty status
filter = df["status"].isnull() 
dfexception_status = df[filter].copy()
dfexception_status["Exception"] = ExceptionMsg("status","Empty Field")


# In[14]:


#Dropping those with empty status
df=df.dropna(subset=["status"])
print("After Cleansing status which are empty ",df.shape)


# In[15]:


#Filter category_name_1!="/N" 
keep = df["category_name_1"] != "\\N" 
filter = df["category_name_1"] == "\\N" 
dfexception_cat_name_2 = df[filter].copy()
dfexception_cat_name_2["Exception"] = ExceptionMsg("category_name_1","Invalid Content \\N")
#print(dfexception_cat_name_2.shape)  


# In[16]:


df= df[keep]
print("After Cleansing category_name_1 which='\\N' rows ",df.shape)


# In[17]:


#Filter BI Status == #REF! 
keep = df["BI Status"] != "#REF!"
filter = df["BI Status"] == "#REF!"
dfexception_bi_status = df[filter].copy()
dfexception_bi_status["Exception"] = ExceptionMsg("BI Status","Invalid Content #REF!")
#print(dfexception_bi_status.shape)  


# In[18]:


df= df[keep]
print("After Cleansing BI Status= #REF! rows ",df.shape)


# In[19]:


#print(df.columns)


# In[20]:


#Filter MV =" -   " 
keep = df[" MV "] != " -   "
filter = df[" MV "] == " -   "
dfexception_mv = df[filter].copy()
dfexception_mv["Exception"] = ExceptionMsg("MV","Invalid Content - ")
#print(dfexception_mv.shape)  


# In[21]:


df= df[keep]
print("After Cleansing MV = - rows ",df.shape)


# In[22]:


is_numeric_dtype(df[" MV "])
df["MV"]=df[" MV "]
#df.drop(" MV ")
#print(df)


# In[23]:


#df[df.MV.apply(lambda x: x.isnumeric())]
#print("After Cleansing MV = - rows ",df.shape)
#print(df.columns)


# In[24]:


#Cleansing the empty spaces and removing the thousand separators
df["MV"]=df["MV"].str.strip()
df["MV"]=df["MV"].str.replace(",","")


# In[25]:


#print("After Cleansing MV = - rows ",df.shape)


# In[26]:


#Conversion to integer
df["MV"] = df["MV"].apply(lambda x: int(x))


# In[27]:


#Reconciliation of MV Value columns
df["calculated_grandtotal"]= df.apply(lambda x: x['MV'] - x['discount_amount'], axis=1)
df["recon_grandtotal"]=df.apply(lambda x: x["grand_total"] - x["calculated_grandtotal"], axis=1)


# In[28]:


print("These are all that is left after the cleansing ",df.shape)


# In[29]:



#these might be potential fraud cases, hence we may not want to destroy or cleanse these
filtermismatch=df["recon_grandtotal"] != 0
print("These are mismatches between MV-discount and grand_total, but they should not be omitted as it might be potential bugs or fraud cases: ",df[filtermismatch].shape)

#Export MV mismatch report File to drive
df[filtermismatch].to_csv('data_mv_mismatch_report.csv',sep=",",index=False)

#these are the cases that match
filtermatch=df["recon_grandtotal"] == 0
print("These are matches between MV-discount and grand_total: ",df[filtermatch].shape)




# In[30]:


#Export Cleanse File to drive
print("Before export this is all that's left after the cleansing ",df.shape)
df.to_csv('data_cleansed.csv',sep=",",index=False)


# In[31]:


#Preparing Exception Report
frames = [dfexception_cat_name,dfexception_cust_id,dfexception_status,dfexception_cat_name_2,dfexception_bi_status,dfexception_mv]
dfAllExceptions=pd.concat(frames)


# In[32]:


print("Compiling Exceptions, Total Exceptions ",dfAllExceptions.shape)
dfAllExceptions.to_csv('Exception_Report.csv',sep=",",index=False)
dfAllExceptions.head()

