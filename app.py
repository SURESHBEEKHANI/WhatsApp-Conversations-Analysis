import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt  # type: ignore
from src.preprocessor import parse_whatsapp_chat
from src.helper import fetch_stats, top_active_users


# Main Title
st.title("WhatsApp Chat Analyzer 📊")

# Sidebar: File Uploader
uploaded_file = st.sidebar.file_uploader("Upload a WhatsApp chat file (.txt format)", type=["txt"])

if uploaded_file:
    try:
        # Parse and load the uploaded chat file
        file_data = uploaded_file.getvalue().decode("utf-8")
        df = parse_whatsapp_chat(file_data)
        
        st.success("Chat Data Loaded Successfully!")
        st.dataframe(df.head())  # Preview the data
        
        # User Selection for Analysis
        unique_users = df['User'].unique().tolist()
        if 'group_notification' in unique_users:
            unique_users.remove('group_notification')
        unique_users.sort()
        unique_users.insert(0, "Overall")
        
        selected_user = st.sidebar.selectbox("Select User for Analysis", unique_users)

        # Analysis Button
        if st.sidebar.button("Show Analysis"):
            num_messages, words, num_media_messages, num_links = fetch_stats(df, selected_user)

            # Display Top Statistics
            st.subheader("📈 Top Statistics 📈")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Messages", num_messages)
            col2.metric("Total Words", words)
            col3.metric("Media Shared", num_media_messages)
            col4.metric("Links Shared", num_links)

            # Busy Users Analysis (if "Overall" selected)
            if selected_user == "Overall":
                st.subheader("📊 Most Busy Users 🏆")
                x, new_df = top_active_users(df)

                # Visualization
                fig, ax = plt.subplots()
                col1, col2 = st.columns(2)
                colors = ['#1f77b4', '#2ca02c', '#ff7f0e'] 

                with col1:
                    ax.bar(x.index, x.values, color=[colors[i % 3] for i in range(len(x))])  # Apply the colors in a cycle
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
                
                with col2:
                    st.dataframe(new_df)

        # Sentiment Analysis Placeholder
        if st.sidebar.button("Show Sentiment"):
            st.info("Sentiment Analysis is currently under development. Stay tuned!")

        # Chat Summary Placeholder
        if st.sidebar.button("Show Summary"):
            st.info("Chat Summary feature is coming soon!")

    except Exception as e:
        st.error(f"An error occurred while processing the file: {str(e)}")
else:
    st.warning("Please upload a WhatsApp chat file to begin.")
