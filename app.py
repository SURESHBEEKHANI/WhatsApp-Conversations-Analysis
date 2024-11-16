import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt  # type: ignore
from src.preprocessor import parse_whatsapp_chat
from src.helper import fetch_stats, top_active_users, create_wordcloud, most_common_word

# Main Title
st.title("📊 WhatsApp Chat Analyzer")

# Sidebar: File Uploader
uploaded_file = st.sidebar.file_uploader("Upload a WhatsApp chat file (.txt format)", type=["txt"])

if uploaded_file:
    try:
        # Parse and load the uploaded chat file
        file_data = uploaded_file.getvalue().decode("utf-8")
        df = parse_whatsapp_chat(file_data)

        st.success("✅ Chat Data Loaded Successfully!")
        st.dataframe(df.head())  # Preview the data

        # User Selection for Analysis
        unique_users = sorted(user for user in df['User'].unique() if user != 'group_notification')
        unique_users.insert(0, "Overall")
        selected_user = st.sidebar.selectbox("Select User for Analysis", unique_users)

        # Analysis Section
        if st.sidebar.button("Show Analysis"):
            # Fetch statistics
            num_messages, words, num_media_messages, num_links = fetch_stats(df, selected_user)

            # Display Top Statistics
            st.subheader("📈 Top Statistics")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Messages", num_messages)
            col2.metric("Total Words", words)
            col3.metric("Media Shared", num_media_messages)
            col4.metric("Links Shared", num_links)

            # Busy Users Analysis (if "Overall" selected)
            if selected_user == "Overall":
                st.subheader("📊 Most Active Users 🏆")
                top_users, user_percentages = top_active_users(df)

                # Visualization
                col1, col2 = st.columns(2)
                with col1:
                    fig, ax = plt.subplots()
                    colors = ['#4C72B0', '#55A868', '#F1A340', '#C44E52', '#8172B2']
                    ax.bar(top_users.index, top_users.values, color=[colors[i % len(colors)] for i in range(len(top_users))])
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)

                with col2:
                    st.dataframe(user_percentages)

            # Word Cloud Section
            st.subheader("🌟 Word Cloud 🌟")
            wordcloud = create_wordcloud(selected_user, df)

            # Plot the word cloud
            fig, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation="bilinear")
            ax.axis("off")  # Hide the axes for better visualization
            st.pyplot(fig)

            # Most Common Words Section
            st.subheader("📋 Most Common Words")
            common_words = most_common_word(selected_user, df)
            st.dataframe(common_words)

        # Additional Features
        if st.sidebar.button("Show Sentiment"):
            st.info("Sentiment Analysis is currently under development. Stay tuned!")

        if st.sidebar.button("Show Summary"):
            st.info("Chat Summary feature is coming soon!")

    except Exception as e:
        st.error(f"🚨 An error occurred while processing the file: {e}")

else:
    st.warning("⚠️ Please upload a WhatsApp chat file to begin.")
