import streamlit as st
import pandas as pd

cycle_start_day = 'Monday'
cycle_period = 7


@st.cache_data
def get_data():
    df = pd.read_excel('/Users/jigme/Desktop/data/sales.xlsx',dtype={'Scan Code':str})
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day_of_week
    print('Year(s) : ',df['Year'].unique())
    print('Months(s) : ',df['Month'].unique())
    print('start date: ',df['Date'][0])
    print('end date: ',df['Date'][len(df)-1])
    return df

def monthly_report(df:pd.DataFrame):
    pass





df = get_data()


##accounting only for cigarretes
filtered_df = df[(df['Department'] == 'Cigarettes') | (df['Department'] == 'MARLBORO')]
items = filtered_df['Scan Code'].unique()
daily = filtered_df.groupby(['Month','Day','Scan Code','Description','Department']).agg({'Qty':'sum'})
print(type(daily.loc[(9,0,'012300000932'),'Qty']))
    
    




