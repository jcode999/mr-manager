
# import pandas as pd
# # df = pd.DataFrame({'Day':[1,1,1,3],
# #                    'Hour':[7,7,8,9],
# #                    'value':[1,1,1,2]})

# # grouped = df.groupby(['Day','Hour']).agg({'value':'sum'})
# # print(grouped)
# def calculate_time_difference(group):
#     start_time = group[0]
#     end_time = group[-1]
#     return (end_time - start_time).total_seconds()

# df = pd.DataFrame({'Date':['2023-09-01 07:11:01','2023-09-01 07:11:10','2023-09-01 07:12:57','2023-09-01 07:13:57'],
#                    'Tran ID':['123','123','124','124']})

# df['Date'] = pd.to_datetime(df['Date'])
# df_grpd = df.groupby(['Tran ID']).aggregate({'Date':list})

# # Apply the custom function to each group
# df_grpd['TimeDifference'] = df_grpd['Date'].apply(calculate_time_difference)

# # Reset the index for better presentation
# df_grpd.reset_index(inplace=True)

# print(df_grpd)

# import calendar

# def find_first_monday(year, month):
#     # Get the calendar for the given month and year
#     cal = calendar.monthcalendar(year, month)

#     # Find the first week that has a Monday
#     for week in cal:
#         if week[calendar.MONDAY] != 0:
#             # Return the date of the first Monday
#             return week[calendar.MONDAY]

# # Example: Find the first Monday of November 2023
# year = 2023
# month = 11
# first_monday = find_first_monday(year, 9)

# print(f"The first Monday of {year}-{month:02d} is on {first_monday}")

import pandas as pd

sales = [10,12,11,33]
df = pd.DataFrame(columns=['Week1','Week2','Week3','Week4'])
print(df)
