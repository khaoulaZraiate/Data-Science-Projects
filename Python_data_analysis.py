



import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
from itertools import repeat



# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[3]:


# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[4]:


def get_list_of_university_towns():
    df=pd.read_csv("university_towns.txt", sep='delimiter', header=None)
    list_state= df[df[0].str.contains("edit")]
    list_state_new=[]
    
    index_difference=list_state.index
    list_state=list_state.reset_index()
    del list_state['index']
    list_state=list_state[0].tolist()
    
    for i in range(1,len(index_difference)):
        times=index_difference[i]-index_difference[i-1]-1
        
        
        list_state_new.extend(repeat(list_state[i-1], times))
        
    list_state_new.append(list_state[-1])
    state=list_state_new

    df=df.drop(df.index[index_difference])
    df=df.reset_index()
    regionName=df[0].tolist()
    del df['index']
    
    zippedList =list(zip(list_state_new, regionName))
            
    df_finale=pd.DataFrame(zippedList, columns = ['State' , 'RegionName'])
    
    for ind in df_finale['State']:
        df_finale=df_finale.replace(ind,ind[:-6])
        
    for ind in df_finale['RegionName']:
        if "(" in ind :
            df_finale=df_finale.replace(ind,ind[:(ind.index("(")-1)])
    
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
   
    return df_finale
get_list_of_university_towns()


# In[5]:


def get_recession_start():
    GDP=pd.read_excel('gdplev.xls')
    
    GDP=GDP.rename(columns={'Unnamed: 1':'GDP in billions of current dollars(Annual)','Unnamed: 2':'GDP in billions of chained 2009 dollars','Unnamed: 4':'(Seasonally adjusted annual rates) Quarterly','Unnamed: 5':'GDP in billions of current dollars','Unnamed: 6':'GDP in billions of chained 2009 dollars1'})
    GDP=GDP.drop(['Unnamed: 3','Current-Dollar and "Real" Gross Domestic Product','GDP in billions of current dollars(Annual)'],axis=1)
    GDP=GDP.drop(GDP.columns[-1],axis=1).drop(GDP.columns[0],axis=1)
    GDP=GDP[219:].reset_index().drop(GDP.columns[-2],axis=1)
    
    GDP=GDP.drop(GDP.columns[0],axis=1)
    
    for ind in range(len(GDP)-4):
        if (GDP['GDP in billions of chained 2009 dollars1'][ind])<GDP['GDP in billions of chained 2009 dollars1'][ind+1]:
            if (GDP['GDP in billions of chained 2009 dollars1'][ind+1])>GDP['GDP in billions of chained 2009 dollars1'][ind+2]:
                if (GDP['GDP in billions of chained 2009 dollars1'][ind+2])>GDP['GDP in billions of chained 2009 dollars1'][ind+3]:
                    result=GDP['(Seasonally adjusted annual rates) Quarterly'][ind+2]
            
        
    
    
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    
    return result
get_recession_start()


# In[6]:


def get_recession_end():
    

    
    GDP=pd.read_excel('gdplev.xls')
    
    GDP=GDP.rename(columns={'Unnamed: 1':'GDP in billions of current dollars(Annual)','Unnamed: 2':'GDP in billions of chained 2009 dollars','Unnamed: 4':'(Seasonally adjusted annual rates) Quarterly','Unnamed: 5':'GDP in billions of current dollars','Unnamed: 6':'GDP in billions of chained 2009 dollars1'})
    GDP=GDP.drop(['Unnamed: 3','Current-Dollar and "Real" Gross Domestic Product','GDP in billions of current dollars(Annual)'],axis=1)
    GDP=GDP.drop(GDP.columns[-1],axis=1).drop(GDP.columns[0],axis=1)
    GDP=GDP[219:].reset_index().drop(GDP.columns[-2],axis=1)
    
    GDP=GDP.drop(GDP.columns[0],axis=1)
    
    for ind in range(1,len(GDP)-5):
        if(GDP['GDP in billions of chained 2009 dollars1'][ind-1])>GDP['GDP in billions of chained 2009 dollars1'][ind]:
            if (GDP['GDP in billions of chained 2009 dollars1'][ind])>GDP['GDP in billions of chained 2009 dollars1'][ind+1]:
                if (GDP['GDP in billions of chained 2009 dollars1'][ind+1])<GDP['GDP in billions of chained 2009 dollars1'][ind+2]:
                    if (GDP['GDP in billions of chained 2009 dollars1'][ind+2])<GDP['GDP in billions of chained 2009 dollars1'][ind+3]:
                        if(GDP['GDP in billions of chained 2009 dollars1'][ind+3])<GDP['GDP in billions of chained 2009 dollars1'][ind+4]:
                            result=GDP['(Seasonally adjusted annual rates) Quarterly'][ind+3]
    
    
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    
    
    
       
    return result
get_recession_end()


# In[7]:


def get_recession_bottom():
    GDP=pd.read_excel('gdplev.xls')
    
    GDP=GDP.rename(columns={'Unnamed: 1':'GDP in billions of current dollars(Annual)','Unnamed: 2':'GDP in billions of chained 2009 dollars','Unnamed: 4':'(Seasonally adjusted annual rates) Quarterly','Unnamed: 5':'GDP in billions of current dollars','Unnamed: 6':'GDP in billions of chained 2009 dollars1'})
    GDP=GDP.drop(['Unnamed: 3','Current-Dollar and "Real" Gross Domestic Product','GDP in billions of current dollars(Annual)'],axis=1)
    GDP=GDP.drop(GDP.columns[-1],axis=1).drop(GDP.columns[0],axis=1)
    GDP=GDP[219:].reset_index().drop(GDP.columns[-2],axis=1)
    GDP=GDP.drop(GDP.columns[0],axis=1)
    for ind in range(1,len(GDP)-4):
        if(GDP['GDP in billions of chained 2009 dollars1'][ind-1])>GDP['GDP in billions of chained 2009 dollars1'][ind]:
            if (GDP['GDP in billions of chained 2009 dollars1'][ind])>GDP['GDP in billions of chained 2009 dollars1'][ind+1]:
                if (GDP['GDP in billions of chained 2009 dollars1'][ind+1])<GDP['GDP in billions of chained 2009 dollars1'][ind+2]:
                    if (GDP['GDP in billions of chained 2009 dollars1'][ind+2])<GDP['GDP in billions of chained 2009 dollars1'][ind+3]:
                        if(GDP['GDP in billions of chained 2009 dollars1'][ind+3])<GDP['GDP in billions of chained 2009 dollars1'][ind+4]:
                            result=GDP['(Seasonally adjusted annual rates) Quarterly'][ind+1]
    
    
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    
    return result
get_recession_bottom()


# In[8]:


def convert_housing_data_to_quarters():
    housing_data=pd.read_csv('City_Zhvi_AllHomes.csv')
    
    working_data=housing_data.iloc[:,51:]
    for i in range (0,len(working_data.columns),3):
        if working_data.columns[i][-2:]=='01':
            working_data[str(working_data.columns[i][:4])+'q1']=working_data[working_data.columns[i:i+3]].mean(axis=1)
        if working_data.columns[i][-2:]=='04':
            working_data[str(working_data.columns[i][:4])+'q2']=working_data[working_data.columns[i:i+3]].mean(axis=1)
        if working_data.columns[i][-2:]=='07':
            working_data[str(working_data.columns[i][:4])+'q3']=working_data[working_data.columns[i:i+3]].mean(axis=1) 
        if working_data.columns[i][-2:]=='10':
            working_data[str(working_data.columns[i][:4])+'q4']=working_data[working_data.columns[i:i+3]].mean(axis=1)
            
            
        
    working_data=working_data.iloc[:,200:]
   
    thisss=pd.DataFrame([states]).T.reset_index()
    thisss=thisss.rename(columns={'index':'State',0:'SateNew'})
   
    housing_data=housing_data.iloc[:,:3]
    housing_data=pd.merge(housing_data,thisss,on='State',how='left')
    housing_data=housing_data.drop(housing_data.columns[2],axis=1)
    housing_data=housing_data.rename(columns={'SateNew':'State'})
    working_data=pd.merge(housing_data,working_data, left_index=True, right_index=True,how='inner')
    working_data=working_data.drop(working_data.columns[0],axis=1)
    working_data=working_data.set_index(['State','RegionName'])
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    
    return working_data

convert_housing_data_to_quarters()


# In[22]:



def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    
    df = convert_housing_data_to_quarters()
    
   
    before_rec = (df.columns.get_loc(get_recession_start())-1)
    rec_bottom = df.columns.get_loc(get_recession_bottom())
    
    uni = get_list_of_university_towns().set_index(['State', 'RegionName'])
    
    # Turn the divided values into a DataFrame!
    df = np.divide(df.ix[:,before_rec],df.ix[:,rec_bottom]).to_frame().dropna()
    
    # Merge university and GDP data.
    uni_df = df.merge(uni, right_index=True, left_index=True, how='inner')
    
    # Drop the indices of uni towns to get data only for non uni towns.
    nonuni_df = df.drop(uni_df.index)
    
    # A t-test is commonly used to determine whether the mean of a population significantly
    # differs from a specific value (called the hypothesized mean) or from the mean of another population.
    p_value = ttest_ind(uni_df.values, nonuni_df.values).pvalue
    if p_value < 0.01:
        different=True
    else:
        different=False
        
    # Better depending on which one is LOWER! Remember prices go up during a recession so lower is better.
    if uni_df.mean().values < nonuni_df.mean().values:
        better='university town'
    else:
        better='non-university town'

    return (different, p_value[0], better)
    
run_ttest()







