import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns
from PIL import Image


rcParams['font.family'] = 'Segoe UI Emoji'

st.sidebar.title("Whatsapp Chat Analyzer")

df = None  # initialize df to avoid NameError

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is None:
     st.markdown(
        """
        <div style="padding: 15px; background-color: #cce5ff; color: #004085; border-radius: 5px;">
            📄 Please upload a WhatsApp chat file to start analysis.
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)

 
if df is not None:
  user_list = df['user'].unique().tolist()
  if "group_notification" in user_list:
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

  selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

  if st.sidebar.button("show analysis"):
   
   num_messages , words , num_media_messages , num_links= helper.fetch_stats(selected_user,df)

  #stats

   st.title("Top Statistics")
   col1, col2, col3, col4 = st.columns(4)
   
   with col1:
    st.header("Total Messages")
    st.title(num_messages)
   with col2:
    st.header("Total Words")
    st.title(words)
   with col3:
    st.header("Media Shared")
    st.title(num_media_messages)
   with col4:
    st.header("Links Shared")
    st.title(num_links)


   #timeline(monthly)
   st.title("Montly Timeline")
   timeline = helper.monthly_timeline(selected_user,df)
   fig,ax = plt.subplots(figsize=(12, 5))
   ax.plot(timeline['time'] , timeline['message'] , color = 'green')
   plt.xticks(rotation = 'vertical')
   st.pyplot(fig)

   #daily
   st.title("Daily Timeline")
   daily_timeline = helper.daily_timeline(selected_user,df)
   fig,ax = plt.subplots(figsize=(12, 5))
   ax.plot(daily_timeline['only_date'] , daily_timeline['message'] , color = 'black')
   plt.xticks(rotation = 'vertical')
   st.pyplot(fig)

   #activity

   st.title("Activity Map")
   col1 ,col2 = st.columns(2)

   with col1 :
     st.header("Most Busy Day")
     busy_day = helper.week_activity_map(selected_user,df)
     fig ,ax = plt.subplots(figsize=(10, 4))
     ax.bar(busy_day.index , busy_day.values)
     plt.xticks(rotation = 'vertical')
     st.pyplot(fig)

   with col2 :
     st.header("Most Busy Month")
     busy_month = helper.month_activity_map(selected_user,df)
     fig ,ax = plt.subplots(figsize=(10, 4))
     ax.bar(busy_month.index , busy_month.values , color = 'orange')
     plt.xticks(rotation = 'vertical')
     st.pyplot(fig)
    
    #heatmap
   st.title('Weekly Activity Map')
   user_heatmap = helper.activity_heatmap(selected_user,df)
   fig,ax = plt.subplots(figsize=(12, 4))
   ax = sns.heatmap(user_heatmap)
   st.pyplot(fig)
     


#finding the busiest users in the group (Group level)

   if selected_user =='Overall':
     st.title("Most Busy Users")
     x,new_df = helper.most_busy_users(df)
     fig,ax = plt.subplots(figsize=(10, 4))
     col1 , col2 = st.columns(2)


     with col1:
       ax.bar(x.index,x.values, color='red')
       plt.xticks(rotation='vertical')
       st.pyplot(fig)
     with col2:
       st.dataframe(new_df, use_container_width=True, hide_index=True)
   
    #wordcloud

   st.title("WordCloud")
   df_wc = helper.create_wordcloud(selected_user, df)
  #  fig, ax = plt.subplots(figsize=(6, 3), dpi=80)
  #  ax.imshow(df_wc, interpolation='bilinear')
  #  ax.axis('off')  # hide axes for cleaner display
  #  st.pyplot(fig)
   wc_image = df_wc.to_image()

   new_width = 900       # keeps width same
   new_height = 600      # increase height
   wc_image = wc_image.resize((new_width, new_height))

   st.image(wc_image)



#most common words
   most_common_df = helper.most_common_words(selected_user,df)
   fig,ax = plt.subplots(figsize=(8, 4))

   ax.barh(most_common_df['Word'],most_common_df['Count'])
   plt.xticks(rotation='vertical')

   st.title('Most commmon words')
   st.pyplot(fig)
  #  st.dataframe(most_common_df , use_container_width=True, hide_index=True)


   emoji_df = helper.emoji_helper(selected_user,df)
   st.title("Emoji Analysis")
  
   col1,col2 = st.columns(2)
   

   with col1:
     st.dataframe(emoji_df,use_container_width=True, hide_index=True)
   with col2:
     fig,ax = plt.subplots(figsize=(6, 6))
     ax.pie(emoji_df['Count'].head(),labels=emoji_df['Emoji'].head(),autopct="%0.2f")
     st.pyplot(fig)


  
   