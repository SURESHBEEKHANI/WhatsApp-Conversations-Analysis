# Import necessary libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt  # type: ignore
from src.preprocessor import parse_whatsapp_chat
from src.helper import (
    fetch_stats,
    top_active_users,
    create_wordcloud,
    most_common_word,
)

# Application Title
st.title("📊 WhatsApp Chat Analyzer")

# Sidebar: File Uploader
st.sidebar.header("Upload Chat File")
uploaded_file = st.sidebar.file_uploader(
    "Upload a WhatsApp chat file (.txt format)", type=["txt"]
)

if uploaded_file:
    try:
        # Load and parse the uploaded file
        file_data = uploaded_file.getvalue().decode("utf-8")
        df = parse_whatsapp_chat(file_data)
        
        st.success("✅ Chat Data Loaded Successfully!")
        st.dataframe(df.head())  # Preview a few rows of the parsed data
        
        # User Selection for Analysis
        unique_users = sorted(
            user for user in df["User"].unique() if user != "group_notification"
        )
        unique_users.insert(0, "Overall")  # Add an option for overall analysis
        selected_user = st.sidebar.selectbox("Select User for Analysis", unique_users)
        
        # Analysis Section
        if st.sidebar.button("Show Analysis"):
            # Fetch basic statistics
            num_messages, words, num_media_messages, num_links = fetch_stats(
                df, selected_user
            )
            
            # Display Statistics
            st.subheader("📈 Key Chat Statistics")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Messages", num_messages)
            col2.metric("Total Words", words)
            col3.metric("Media Shared", num_media_messages)
            col4.metric("Links Shared", num_links)
            
            # Most Active Users Analysis (only for "Overall" selection)
            if selected_user == "Overall":
                st.subheader("📊 Most Active Users 🏆")
                top_users, user_percentages = top_active_users(df)
                
                # Visualizations for Active Users
                col1, col2 = st.columns(2)
                
                with col1:
                    # Bar Chart for User Activity
                    fig, ax = plt.subplots()
                    colors = ['#4C72B0', '#55A868', '#F1A340', '#C44E52', '#8172B2']
                    ax.bar(
                        top_users.index,
                        top_users.values,
                        color=[colors[i % len(colors)] for i in range(len(top_users))],
                    )
                    plt.xticks(rotation="vertical")
                    st.pyplot(fig)
                
                with col2:
                    # Data Table for User Percentages
                    st.dataframe(user_percentages)
            
            # Word Cloud Visualization
            st.subheader("🌟 Word Cloud 🌟")
            wordcloud = create_wordcloud(selected_user, df)
            
            fig, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation="bilinear")
            ax.axis("off")  # Hide axes for a cleaner display
            st.pyplot(fig)
            
            # Most Common Words
            st.subheader("📋Most Common Words📋")
            common_words = most_common_word(selected_user, df)
            
            # Bar Chart for Most Common Words
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(
                common_words[0], common_words[1], color="skyblue", edgecolor="black"
            )
            ax.set_title("Most Common Words", fontsize=16)
            ax.set_xlabel("Words", fontsize=12)
            ax.set_ylabel("Frequency", fontsize=12)
            ax.tick_params(axis="x", rotation=45)
            st.pyplot(fig)
        
        # Additional Features (Placeholders)
        if st.sidebar.button("Show Sentiment"):
            st.info("🛠 Sentiment Analysis is under development. Stay tuned!")
        
        if st.sidebar.button("Show Summary"):
            st.info("📋Chat Summary feature coming soon!")
    
    except Exception as e:
        st.error(f"🚨 An error occurred while processing the file: {e}")
else:
    st.warning("⚠️ Please upload a WhatsApp chat file to begin.")
