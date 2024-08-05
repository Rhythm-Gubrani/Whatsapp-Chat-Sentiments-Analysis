# import re
# import pandas as pd

# def preprocess(data):
#     pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
#     messages = re.split(pattern, data)[1:]
#     dates = re.findall(pattern, data)
#     from datetime import datetime
#     # dividing the dataset into two columns messages and date
#     df = pd.DataFrame({'user_message': messages, 'message_date': dates})

#     # converting the message date data type
#     def parse_date(date_str):
#         for fmt in ('%d/%m/%Y, %H:%M - ', '%m/%d/%y, %H:%M - '):
#             try:
#                 return datetime.strptime(date_str, fmt)
#             except ValueError:
#                 continue
#         raise ValueError(f"Date format not recognized: {date_str}")

#     df['message_date'] = df['message_date'].apply(parse_date)
#     df.rename(columns={'message_date': 'date'}, inplace=True)

#     users = []
#     messages = []
#     for message in df['user_message']:
#         entry = re.split(r'([\w\W]*?):\s', message)
#         if entry[1:]:  # user name
#             users.append(entry[1])
#             messages.append(" ".join(entry[2:]))
#         else:
#             users.append('group_notification')
#             messages.append(entry[0])

#     df['users'] = users
#     df['message'] = messages
#     df1 = df.drop(columns=['user_message'], inplace=True)
    
#     df['only_date'] = df['date'].dt.date
#     df['year'] = df['date'].dt.year
#     df['month_num'] = df['date'].dt.month
#     df['month'] = df['date'].dt.month_name()
#     df['day'] = df['date'].dt.day
#     df['day_name'] = df['date'].dt.day_name()
#     df['hour'] = df['date'].dt.hour
#     df['minute'] = df['date'].dt.minute
    
#     period = []
#     for hour in df[['day_name','hour']]['hour']:
#         if hour == 23:
#             period.append(str(hour) + "-" + str('00'))
#         elif hour == 0:
#             period.append(str('00') + "-" + str(hour+1))
#         else:
#             period.append(str(hour) + "-" + str(hour+1))

#     df['period'] = period
#     return df


import re
import pandas as pd
from datetime import datetime

def preprocess(data):
    # Pattern to match the date and time in both 12-hour and 24-hour formats
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?[APMampm]{0,2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Convert the message date data type
    def parse_date(date_str):
        # Try parsing in multiple formats to accommodate different time representations
        for fmt in ('%d/%m/%Y, %I:%M %p - ', '%d/%m/%Y, %H:%M - ', '%m/%d/%y, %I:%M %p - ', '%m/%d/%y, %H:%M - '):
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        raise ValueError(f"Date format not recognized: {date_str}")

    # Create dataframe
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Apply the date parsing
    df['message_date'] = df['message_date'].apply(parse_date)
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Extract users and messages
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'([\w\W]*?):\s', message)
        if entry[1:]:  # User name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['users'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Extract additional date and time information
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Define periods for activity heatmap
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    return df

