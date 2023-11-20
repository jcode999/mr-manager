import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import calendar
from datetime import datetime
import altair as alt
import seaborn as sns
today_date = datetime.now()
today_day_name = today_date.strftime('%A')
today_day_name.lower()
today_day_name[0].upper()


day_mapping = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
def get_key_by_value(value, mapping):
    return next(key for key, val in mapping.items() if val == value)

day_literal = get_key_by_value(today_day_name,day_mapping)

def calculate_time_difference(group):
    start_time = group[0]
    end_time = group[-1]
    return (end_time - start_time).total_seconds()


def count_weekdays(year, month, day):
    _, days_in_month = calendar.monthrange(year, month)

    count = 0
    for day_in_month in range(1, days_in_month + 1):
        if calendar.weekday(year, month, day_in_month) == day:
            count += 1

    return count

@st.cache_data
def get_data():
    sales_file = '/Users/jigme/Desktop/data/sales.xlsx'
    df = pd.read_excel(sales_file,header=0)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Department'] = df['Department'].replace({'GAS PUMP #1': 'GAS', 'GAS PUMP #2': 'GAS', 'GAS PUMP #3': 'GAS','GAS PUMP #4': 'GAS'})
    return df


def get_transactional_data():
    df = get_data()
    st.write(df)
    df_grpd = df.groupby(['Tran ID']).aggregate({'Date':list})
    df_grpd['TimeDifference'] = df_grpd['Date'].apply(calculate_time_difference)
    df_grpd.reset_index(inplace=True)
    return df_grpd


@st.cache_data
def get_daily_data():
    df = get_data()
    df['Date'] = pd.to_datetime(df['Date'])
    df['year'] = df['Date'].dt.year
    df['month'] = df['Date'].dt.month
    df['day'] = df['Date'].dt.day_of_week
    
    df['day'] = df['day'].map(day_mapping)
    df['hour'] = df['Date'].dt.hour
    df['minute'] = df['Date'].dt.minute
    df.drop(columns=['Unnamed: 0','Description','Profit','Margin','POS Cost','POS Retail','Promo ID','Date'],inplace=True)

    new_colums = ['year','month','day','hour','minute','Scan Code','Department','Qty','Retail at Sale','Tran ID','Register']
    rearranged_df = df.loc[:,new_colums]
    return rearranged_df



def show_overall():
    dailly_df = get_daily_data()
    
    st.title("Business Throught The Day")


    attributes = st.multiselect(
            "Choose Attributes", dailly_df.columns.to_list(),['day','hour']
        )
    
    if not attributes:
        st.error("Please select at least one attribute.")
    else:
        
        
        agg_data = dailly_df.groupby(attributes).agg({'Qty':"sum"})
        
        dailly_df.sort_index(inplace=True)

        days =  st.multiselect(
                "Day", ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'],[today_day_name]
            )

        if not days:
            st.write("Please select a day")
            

        else:
            for j in range(0,len(days)):
                records = agg_data.loc[(days[j])]
                day_literal = get_key_by_value(days[j],day_mapping)
                num_apperances = count_weekdays(2023,9,day_literal)
                num_apperances = num_apperances + count_weekdays(2023,10,day_literal)
                records['Average Qty'] = records['Qty']/num_apperances
                st.title("Average numbers of items rung in last two months.")
                st.write("Day: ",days[j])
                # st.write(records)
                records.reset_index(inplace=True)
                st.bar_chart(data=records, x='hour', y=['Average Qty'], color=['#ffaa00'], width=1000, height=200, use_container_width=True)

                

def show_register_wise(df:pd.DataFrame):
    register_data  = df.groupby(['day','hour','Register']).agg({'Qty':'sum'})
    records = register_data.loc[(today_day_name)]
    day_literal = get_key_by_value(today_day_name,day_mapping)
    num_apperances = count_weekdays(2023,9,day_literal)
    num_apperances = num_apperances + count_weekdays(2023,10,day_literal)
    records['Average Qty'] = records['Qty']/num_apperances
    records.reset_index(inplace=True)
    records['hour'] = records['hour'].astype(str)

    # Create a complete set of data with zeros for missing values
    complete_data = pd.DataFrame([(str(hour), register) for hour in range(6, 25) for register in records['Register'].unique()], columns=['hour', 'Register'])
    complete_data = complete_data.merge(records, how='left', on=['hour', 'Register']).fillna(0)
    
    # Create a stacked bar chart using Altair
    chart = alt.Chart(complete_data).mark_bar().encode(
        x=alt.X('hour:O', title='Hour', scale=alt.Scale(domain=list(map(str, range(6, 25))))),
        y=alt.Y('Average Qty:Q', title='Average Qty'),
        color='Register:N',
        tooltip=['hour', 'Register', 'Average Qty']
    ).properties(
        width=1000,
        height=200
    )

    # Streamlit app
    st.title('Distribution of transactions among registers')
    st.altair_chart(chart, use_container_width=True)

@st.cache_data
def department_sales_overall(df:pd.DataFrame):
    departmet_grouped = df.groupby(['day','Department']).agg({'Qty':'sum'})
    todays_records = departmet_grouped.loc[(today_day_name)]
    num_apperances = count_weekdays(2023,9,day_literal)
    num_apperances = num_apperances + count_weekdays(2023,10,day_literal)
    todays_records['Average Qty'] = todays_records['Qty']/num_apperances
    todays_records.reset_index(inplace=True)
    return todays_records

def department_pie(df):
    df = department_sales_overall(df)
    st.write("Todays Departent Wise Sales",df)
    st.title('Average Transactions by Department - Pie Chart')
    df['Percentage'] = (df['Average Qty'] / df['Average Qty'].sum()) * 100

    # Create a pie chart using the 'Average' column
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(df['Percentage'], labels=df['Department'], startangle=140)
    # ax.set_title('Average Transactions by Department')
    # Set background color
    ax.set_facecolor('black')

    # Set text color for labels
    for text in ax.texts:
        text.set_color('white')
    
    # Display the pie chart using Streamlit
    st.pyplot(fig)

def show_departmental_data(df:pd.DataFrame):

    departmet_grouped = df.groupby(['day','hour','Department']).agg({'Qty':'sum'})
    todays_records = departmet_grouped.loc[(today_day_name)]
    num_apperances = count_weekdays(2023,9,day_literal)
    num_apperances = num_apperances + count_weekdays(2023,10,day_literal)
    todays_records['Average Qty'] = todays_records['Qty']/num_apperances
    todays_records.reset_index(inplace=True)
    
    todays_records['hour'] = todays_records['hour'].astype(str)
    #('Average Qty:Q', title='Average Qty'),
    chart = alt.Chart(todays_records).mark_bar().encode(
        x=alt.X('Average Qty:Q', title='Average Qty'),
        y=alt.Y('hour:O', title='Hour', scale=alt.Scale(domain=list(map(str, range(6, 25))))),
        color='Department:N',
        tooltip=['hour', 'Department', 'Average Qty']
    ).properties(
        width=1000,
        height=600
    )
    
    st.title('Distribution of Department Wise Sales Per Hour')
    st.altair_chart(chart, use_container_width=True)
    st.title('Department Sales Per Hour')
    selected_columns = [st.selectbox('Select Departments', todays_records['Department'].unique())]
    
    # Filter the DataFrame based on the selected columns
    filtered_data = todays_records[todays_records['Department'].isin(selected_columns)]
    filtered_data['hour'] = filtered_data['hour'].astype(int)
    # st.write(filtered_data)

    # Bar chart
    # st.bar_chart(data=filtered_data, x='hour', y=['Average Qty'], color=['#ffaa00'], width=1000, height=200, use_container_width=True)
    # st.write(filtered_data)
    st.line_chart(data = filtered_data, x='hour', y=['Average Qty'], color=['#ffaa00'], width=1000, height=200, use_container_width=True)


    


df = get_daily_data()
show_overall()
show_register_wise(df)
# department_pie(df)
show_departmental_data(df)

