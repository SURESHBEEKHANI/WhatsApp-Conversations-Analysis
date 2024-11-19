import matplotlib.pyplot as plt
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

from textblob import TextBlob 

# Initialize URL extractor globally
url_extractor = URLExtract()

def fetch_stats(df: pd.DataFrame, selected_user: str):
    """
    Fetch basic statistics (message count, word count, media count, and link count)
    for a selected user or aggregate statistics if 'Overall' is selected.
    """
    # Filter the DataFrame based on the selected user
    df_filtered = df if selected_user == 'Overall' else df[df['User'] == selected_user]

    # Calculate statistics
    num_messages = df_filtered.shape[0]
    num_words = df_filtered['Message'].apply(lambda msg: len(msg.split())).sum()
    num_media_messages = df_filtered[df_filtered['Message'] == '<Media omitted>'].shape[0]
    num_links = df_filtered['Message'].apply(lambda msg: len(url_extractor.find_urls(msg))).sum()

    return num_messages, num_words, num_media_messages, num_links

def top_active_users(df: pd.DataFrame, top_n: int = 5):
    """
    Calculate the top N most active users based on their message count.
    """
    top_users = df['User'].value_counts().head(top_n)
    user_percentage = (df['User'].value_counts(normalize=True) * 100).round(2).reset_index()
    user_percentage.columns = ['User', 'Percentage']

    return top_users, user_percentage

def create_wordcloud(selected_user: str, df: pd.DataFrame):
    """
    Generate a word cloud from the selected user's messages.
    """
    with open('stop_hinglish.txt', 'r') as file:
        stop_words = set(file.read().split())

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    filtered_messages = df[(df['User'] != 'group_notification') & (df['Message'] != '<Media omitted>')]
    filtered_messages['Message'] = filtered_messages['Message'].apply(
        lambda msg: " ".join(word for word in msg.lower().split() if word not in stop_words)
    )

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    wordcloud = wc.generate(filtered_messages['Message'].str.cat(sep=" "))

    return wordcloud

def most_common_word(selected_user: str, df: pd.DataFrame):
    """
    Get the most common words used by the selected user, excluding stop words.
    """
    with open('stop_hinglish.txt', 'r') as file:
        stop_words = set(file.read().split())

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    filtered_messages = df[(df['User'] != 'group_notification') & (df['Message'] != '<Media omitted>')]
    words = [
        word
        for message in filtered_messages['Message']
        for word in message.lower().split()
        if word not in stop_words
    ]

    word_counts = pd.DataFrame(Counter(words).most_common(20))

    return word_counts

def emojis_analysis(selected_user: str, df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract and analyze emojis from messages for a specific user or overall.
    """
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    extracted_emojis = [
        char
        for message in df['Message'].dropna()
        for char in message
        if char in emoji.EMOJI_DATA
    ]

    emoji_counts = Counter(extracted_emojis)
    emoji_df = pd.DataFrame(emoji_counts.most_common())

    return emoji_df

def monthly_timeline(selected_user: str, df: pd.DataFrame):
    """
    Generate a timeline of message counts by month and year for the selected user.
    """
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    timeline = df.groupby(['Year', 'month_num', 'Month']).count()['Message'].reset_index()
    timeline['time'] = timeline.apply(lambda row: f"{row['Month']}-{row['Year']}", axis=1)

    return timeline

def daily_timeline(selected_user: str, df: pd.DataFrame):
    """
    Generate a daily timeline of messages for the selected user.
    """
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['Message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user: str, df: pd.DataFrame):
    """
    Generate a weekly activity map of messages for the selected user.
    """
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user: str, df: pd.DataFrame):
    """
    Generate a monthly activity map of messages for the selected user.
    """
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    return df['Month'].value_counts()

def activity_heatmap(selected_user: str, df: pd.DataFrame):
    """
    Generate a heatmap of user activity by day and period for the selected user.
    """
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='Message', aggfunc='count').fillna(0)

    return user_heatmap

# Function to perform sentiment analysis
def perform_sentiment_analysis(data, selected_user):
    """Analyze sentiment of messages."""
    if selected_user != "Overall":
        data = data[data["User"] == selected_user]

    # Calculate polarity and classify sentiment
    data["Polarity"] = data["Message"].apply(lambda x: TextBlob(x).sentiment.polarity)
    data["Sentiment"] = data["Polarity"].apply(
        lambda x: "Positive" if x > 0.1 else ("Negative" if x < -0.1 else "Neutral")
    )

    # Aggregate sentiment counts
    sentiment_counts = data["Sentiment"].value_counts()

    return sentiment_counts, data