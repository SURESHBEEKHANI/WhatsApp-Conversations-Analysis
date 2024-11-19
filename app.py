# Import necessary libraries
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt  # type: ignore
from src.preprocessor import parse_whatsapp_chat
from src.helper import (
    fetch_stats,
    top_active_users,
    create_wordcloud,
    most_common_word,
    emojis_analysis,
    monthly_timeline,
    daily_timeline,
    week_activity_map,
    month_activity_map,
    activity_heatmap
)

# Application Title
st.title("📊WhatsApp Chat Analyzer📊")

# Sidebar: File Uploader
st.sidebar.header("Upload Chat File")
uploaded_file = st.sidebar.file_uploader("Upload a WhatsApp chat file (.txt format)", type=["txt"])

# Check if a file is uploaded
if uploaded_file:
    try:
        # Decode and parse the uploaded file
        file_data = uploaded_file.getvalue().decode("utf-8")
        df = parse_whatsapp_chat(file_data)

        # Display success message and show a preview of the data
        st.success("✅Chat Data Loaded Successfully!✅")
        st.dataframe(df.head())  # Show the first few rows of the DataFrame

        # Sidebar: User selection for analysis
        unique_users = sorted([user for user in df["User"].unique() if user != "group_notification"])
        unique_users.insert(0, "Overall")  # Add "Overall" option for global stats
        selected_user = st.sidebar.selectbox("Select User for Analysis", unique_users)

        # Analysis Section: Triggered by button
        if st.sidebar.button("Show Analysis"):
            # Fetch and display basic statistics
            num_messages, words, num_media_messages, num_links = fetch_stats(df, selected_user)

            st.subheader("📈Key Chat Statistics📈")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Messages", num_messages)
            col2.metric("Total Words", words)
            col3.metric("Media Shared", num_media_messages)
            col4.metric("Links Shared", num_links)

            # Monthly Timeline Analysis
            st.subheader("📅Monthly Timeline📅")
            timeline = monthly_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(timeline["time"], timeline["Message"], color="green")
            ax.set_title("Message Trends Over Time (Monthly)")  # Plot title
            ax.set_xlabel("Time (Month-Year)")  # X-axis label
            ax.set_ylabel("Number of Messages")  # Y-axis label
            plt.xticks(rotation="vertical")
            plt.legend()  # Show the legend for better clarity
            plt.grid(True)
            st.pyplot(fig)

            # Daily Timeline
            st.subheader("📅Daily Timeline📅")
            daily_data = daily_timeline(selected_user, df)  # Get daily timeline data
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(daily_data['only_date'], daily_data['Message'], color='blue')  # Line chart
            ax.set_title("Message Trends Over Time (Daily)")  # Title for the plot
            ax.set_xlabel("Date (Day-Month-Year)")  # Label for x-axis
            ax.set_ylabel("Number of Messages")  # Label for y-axis
            plt.xticks(rotation=80)  # Rotate x-axis labels for better visibility
            st.pyplot(fig)

            # Activity Map
            st.subheader("📅Activity Map📅")
            col1, col2 = st.columns(2)

            with col1:
                st.header("Most Busy Day")
                busy_day = week_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_day.index, busy_day.values, color='purple')
                ax.set_title("Weekly Activity: Most Busy Day")
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.header("Most Busy Month")
                busy_month = month_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values, color='orange')
                ax.set_title("Monthly Activity: Most Busy Month")
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            # Weekly Activity Heatmap
            st.title("📅Weekly Activity Map📅")
            user_heatmap = activity_heatmap(selected_user, df)
            fig, ax = plt.subplots()
            sns.heatmap(user_heatmap, ax=ax, cmap="coolwarm")
            ax.set_title("Heatmap of Weekly Activity")
            st.pyplot(fig)

            # Most Active Users (Overall Analysis only)
            if selected_user == "Overall":
                st.subheader("📊 Most Active Users 🏆")
                top_users, user_percentages = top_active_users(df)

                # Display bar chart and percentage table for active users
                col1, col2 = st.columns(2)

                with col1:
                    # Bar chart for user activity
                    fig, ax = plt.subplots()
                    colors = ['#4C72B0', '#55A868', '#F1A340', '#C44E52', '#8172B2']
                    ax.bar(
                        top_users.index,
                        top_users.values,
                        color=[colors[i % len(colors)] for i in range(len(top_users))],
                    )
                    ax.set_title("Top Active Users")
                    plt.xticks(rotation="vertical")
                    st.pyplot(fig)

                with col2:
                    # Table showing user activity percentages
                    st.dataframe(user_percentages)

            # Word Cloud Visualization
            st.subheader("🌟 Word Cloud 🌟")
            wordcloud = create_wordcloud(selected_user, df)
            fig, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation="bilinear")
            ax.axis("off")  # Hide axes for better visualization
            ax.set_title("Word Cloud Representation")
            st.pyplot(fig)

            # Most Common Words
            st.subheader("📋 Most Common Words 📋")
            common_words = most_common_word(selected_user, df)
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(common_words[0], common_words[1], color="skyblue", edgecolor="black")
            ax.set_title("Most Common Words Used")
            ax.set_xlabel("Words")
            ax.set_ylabel("Frequency")
            ax.tick_params(axis="x", rotation=45)
            st.pyplot(fig)

            # Emoji Analysis
            st.subheader("😊 Emoji Analysis 😊")
            emoji_df = emojis_analysis(selected_user, df)

            col1, col2 = st.columns(2)
            with col1:
                # Show emoji frequencies in a table
                st.dataframe(emoji_df)

            with col2:
                # Pie chart for top emojis
                fig, ax = plt.subplots()
                ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f%%")
                ax.set_title("Top Emojis Distribution")
                st.pyplot(fig)

        # Additional Features (Placeholders)
        if st.sidebar.button("Show Sentiment"):
            st.info("🛠 Sentiment Analysis is under development. Stay tuned!")

        if st.sidebar.button("Show Summary"):
            st.info("📋 Chat Summary feature coming soon!")

    except Exception as e:
        # Handle errors during file processing
        st.error(f"🚨 An error occurred while processing the file: {e}")
else:
    # Prompt user to upload a file if none is provided
    st.warning("⚠️ Please upload a WhatsApp chat file to begin.")
