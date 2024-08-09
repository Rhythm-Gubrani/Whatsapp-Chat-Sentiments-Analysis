# import re
# import pandas as pd
# from datetime import datetime

# def preprocess(data):
#     # Pattern to match the date and time in both 12-hour and 24-hour formats
#     pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?[APMampm]{0,2}\s-\s'
#     messages = re.split(pattern, data)[1:]
#     dates = re.findall(pattern, data)

  
#     from dateutil import parser

#     def parse_date(date_str):
#         try:
#             # Attempt to parse date assuming it's in a recognized format
#             return parser.parse(date_str.split(' - ')[0])
#         except (parser.ParserError, ValueError):
#             raise ValueError(f"Date format not recognized: {date_str}")

#     # Create dataframe
#     df = pd.DataFrame({'user_message': messages, 'message_date': dates})

#     # Apply the date parsing
#     df['message_date'] = df['message_date'].apply(parse_date)
#     df.rename(columns={'message_date': 'date'}, inplace=True)

#     # Extract users and messages
#     users = []
#     messages = []
#     for message in df['user_message']:
#         entry = re.split(r'([\w\W]*?):\s', message)
#         if entry[1:]:  # User name
#             users.append(entry[1])
#             messages.append(" ".join(entry[2:]))
#         else:
#             users.append('group_notification')
#             messages.append(entry[0])

#     df['users'] = users
#     df['message'] = messages
#     df.drop(columns=['user_message'], inplace=True)

#     # Extract additional date and time information
#     df['only_date'] = df['date'].dt.date
#     df['year'] = df['date'].dt.year
#     df['month_num'] = df['date'].dt.month
#     df['month'] = df['date'].dt.month_name()
#     df['day'] = df['date'].dt.day
#     df['day_name'] = df['date'].dt.day_name()
#     df['hour'] = df['date'].dt.hour
#     df['minute'] = df['date'].dt.minute

#     # Define periods for activity heatmap
#     period = []
#     for hour in df[['day_name', 'hour']]['hour']:
#         if hour == 23:
#             period.append(str(hour) + "-" + str('00'))
#         elif hour == 0:
#             period.append(str('00') + "-" + str(hour + 1))
#         else:
#             period.append(str(hour) + "-" + str(hour + 1))

#     df['period'] = period
#     return df

import re
import pandas as pd
from dateutil import parser

def preprocess(data):
    # Patterns to match the date and time in both 12-hour and 24-hour formats
    # pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?[APMampm]{0,2}\s-\s|\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?[APMampm]{0,2}\]|[0-9]{2}/[0-9]{2}/[0-9]{2,4},\s\d{1,2}:\d{2}\s?[APMampm]{0,2}|\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}'
    # pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(:\d{2})?\s?[APMampm]{0,2}\s-\s|'r'\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(:\d{2})?\s?[APMampm]{0,2}\]|'r'[0-9]{2}/[0-9]{2}/[0-9]{2,4},\s\d{1,2}:\d{2}(:\d{2})?\s?[APMampm]{0,2}|'r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}(:\d{2})?\s?[APMampm]{0,2}'
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?[APMampm]{0,2}\s-\s|\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\s?[APMampm]{0,2}\]|[0-9]{2}/[0-9]{2}/[0-9]{2,4},\s\d{1,2}:\d{2}\s?[APMampm]{0,2}|\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    def parse_date(date_str):
        date_str = re.sub(r'[\[\]]', '', date_str)  # Remove square brackets if present
        try:
            return parser.parse(date_str.split(' - ')[0])
        except (parser.ParserError, ValueError):
            raise ValueError(f"Date format not recognized: {date_str}")

    # Create DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Apply date parsing
    df['message_date'] = df['message_date'].apply(parse_date)
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Extract users and messages
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'([\w\W]*?):\s', message)
        if entry[1:]:  # User name exists
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
    for hour in df['hour']:
        if hour == 23:
            period.append(f"{hour}-00")
        elif hour == 0:
            period.append("00-1")
        else:
            period.append(f"{hour}-{hour + 1}")

    df['period'] = period
    return df
