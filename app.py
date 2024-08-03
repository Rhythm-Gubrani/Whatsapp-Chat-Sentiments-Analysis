import streamlit as st
import preprocessor,helper

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib import font_manager
import seaborn as sns



# Load the Noto Emoji font
emoji_font_path = "C:/Users/sunil/Desktop/RHYTHM DOCS/WhatsApp Chat Analysis/Whatsapp-Chat-Sentiments-Analysis/Noto_Emoji/NotoEmoji-VariableFont_wght.ttf"
emoji_font = FontProperties(fname=emoji_font_path)

st.sidebar.title("Whatsapp Chat Sentiments Analysis")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    
    df = preprocessor.preprocess(data)
    # st.dataframe(df)
    
    # fetch unique users
    user_list = df['users'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    
    selected_users = st.sidebar.selectbox("Show Analysis wrt",user_list)
    
    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_messages,links,num_emoticons = helper.fetch_stats(selected_users,df)
        # creating 4 columns
        col1, col2, col3, col4, col5 = st.columns(5)
        
        st.title("Top Statistics")
        # creating the first column to view total messages
        with col1:
            st.header("Total Messages")
            st.subheader(num_messages)
        # creating the seconnd column to view the total words
        with col2:
            st.header("Total Words")
            st.subheader(words)
        # creating the third column to view the number of media shared
        with col3:
            st.header("Media Shared")
            st.subheader(num_media_messages)
        # creating the forth column to view the number of links
        with col4:
            st.header("Links Shared")
            st.subheader(links)
        # creating the fifth column to view the number of emoticons
        with col5:
            st.header("Emoticons Shared")
            st.subheader(num_emoticons)
        
        # monthly timeline
        st.title("MOnthly Timeline")
        timeline = helper.monthly_timeline(selected_users,df)
        fig,ax = plt.subplots()
        plt.plot(timeline['time'],timeline['message'],color="green")
        plt.xticks(rotation = "vertical")
        st.pyplot(fig)
        
        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_users,df)
        fig,ax = plt.subplots()
        plt.plot(daily_timeline['only_date'],daily_timeline['message'],color="black")
        plt.xticks(rotation = "vertical")
        st.pyplot(fig)
        
        # activity maps
        st.title("Activity Map")
        col1,col2 = st.columns(2)
        
        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_analysis(selected_users,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation = "vertical")
            st.pyplot(fig)
        
        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_analysis(selected_users,df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color="orange")
            plt.xticks(rotation = "vertical")
            st.pyplot(fig)
            
        # heatmap
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_users,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)
            
        # finding the busiest users in the group(Group Level)
        if selected_users == 'Overall':
            st.title("Most Busy User")
            x,new_df = helper.most_busy_users(df )
            fig, ax = plt.subplots()
            
            col1,col2   = st.columns(2)
            
            with col1:
                ax.bar(x.index,x.values,color="red")
                plt.xticks(rotation = "vertical")
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        
        # WordCloud
        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_users,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
    
        # Most Common words
        st.title("Most Common Words")
        most_common_df = helper.most_common_words(selected_users,df)
        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation="vertical")
        st.pyplot(fig)
        
        # Emoji Analysis
        st.title("Emoji Analysis")
        emoji_df = helper.emojis_analysis(selected_users,df)
        col1,col2 = st.columns(2)
        
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots(figsize=(10,6))
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(),autopct=lambda pct: f'{int(pct)}', textprops={'fontproperties': emoji_font})
            st.pyplot(fig)
            
            

  
    
    
        
                
       
    
    
        
            
    
    

        
        
    