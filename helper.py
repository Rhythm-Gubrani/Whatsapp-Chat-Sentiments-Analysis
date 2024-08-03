# def fetch_stats(selected_user,df):
#     if selected_user == 'Overall':
#         # 1.fetch number of messages
#         num_messages =  df.shape[0]
#         # 2.fetch number of words
#         words = []
#         for message in df['message']:
#             words.extend(message.split())
#         return num_messages,len(words)
#     else:
#         new_df = df[df['users'] == selected_user]
#         num_messages = new_df.shape[0]
#         words = []
#         for message in new_df['message']:
#             words.extend(message.split())
#         return num_messages,len(words)

# for fetching the URLs
import re
import pandas as pd
import emoji
from collections import Counter
from urlextract import URLExtract
from wordcloud import WordCloud
extractor = URLExtract()

def count_emoticons(messages):
    emoticon_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "]+", flags=re.UNICODE)
    
    num_emoticons = sum(len(emoticon_pattern.findall(message)) for message in messages)
    return num_emoticons

def fetch_stats(selected_user,df):
    if selected_user != 'Overall': 
        df = df[df['users']==selected_user]
    # 1.fetch number of messages
    num_messages = df.shape[0]
    # 2.fetch number of words
    words = []
    for message in df['message']:
        words.extend(message.split())
    # 3.fetch number of media messages
    num_media_messages = df[df['message']=='<Media omitted>\n'].shape[0]
    # 4.fetch number of links 
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))
    # 5.fetch number of emoticons
    num_emoticons = count_emoticons(df['message'])
    
    
    
    return num_messages,len(words),num_media_messages,len(links),num_emoticons

def most_busy_users(df):
    x = df['users'].value_counts().head()
    df = round((df['users'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'users':'Name','count':'Percent'})
    return x,df

# creating the wordcloud
def create_wordcloud(selected_user,df):
    
    f = open('stop_hinglish.txt','r')
    stop_words = f.read() 
    
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]
        
    temp = df[df['users'] != "group_notification"]
    temp = temp[temp['message'] != '<Media omitted>\n']
    
    # removing the stop words from the chats 
    # that were matched with the words in the txt file
    def remove_stop_words(message):
        words = []
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
        return " ".join(words)
        
    wc = WordCloud(width = 500,height = 500,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc 

# bar chart to plot the most common words
def most_common_words(selected_user,df):
    
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "]+", flags=re.UNICODE)
    
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]
    # filtering out the messages 
    temp = df[df['users'] != "group_notification"]
    temp = temp[temp['message'] != '<Media omitted>\n']
    
    phone_pattern = re.compile(r'@\d{10,}')  # regex pattern to match phone numbers
    
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words and not emoji_pattern.search(word) and not phone_pattern.match(word):
                words.append(word)
    
    
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

# analysing the emojis
def emojis_analysis(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

# Initialize an empty list to hold the emojis
    emojis = []

# Function to check if a character is an emoji
    def is_emoji(character):
        return character in emoji.EMOJI_DATA

# Iterate over each message in the dataframe
    for message in df['message']:
    # Extract emojis from each message
       emojis.extend([c for c in message if is_emoji(c)])

# Count the occurrences of each emoji
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df
    
# monthly timeline
def monthly_timeline(selected_user,df):
    if selected_user != "Overall":
        df[df['users']==selected_user]
    
    # grouping the data on the basis of year and month
    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()
   
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))
    timeline['time'] = time
    return timeline 

# daily timeline
def daily_timeline(selected_user,df):
    if selected_user != "Overall":
        df[df['users'] == selected_user]
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    
    return daily_timeline

# week activity analysis
def week_activity_analysis(selected_user,df):
    if selected_user !="Overall":
        df[df['users'] ==selected_user]
    return df['day_name'].value_counts()

# month activity analysis
def month_activity_analysis(selected_user,df):
    if selected_user != "Overall":
        df[df["users"] == selected_user]
    
    return df['month'].value_counts()

# heat map 
def activity_heatmap(selected_user,df):
    if selected_user != "Overall":
        df[df["users"] == selected_user]
    user_heatmap = df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)
    return user_heatmap
         
        