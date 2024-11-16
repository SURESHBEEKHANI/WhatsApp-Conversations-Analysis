import matplotlib.pyplot as plt
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter


# Initialize URL extractor globally
url_extractor = URLExtract()

def fetch_stats(df: pd.DataFrame, selected_user: str):
    """
    Fetch basic statistics (message count, word count, media count, and link count)
    for a selected user or aggregate statistics if 'Overall' is selected.

    Parameters:
        df (pd.DataFrame): DataFrame containing the chat data.
        selected_user (str): The user to fetch stats for, or 'Overall' for aggregate stats.

    Returns:
        tuple: A tuple containing:
            - num_messages: Total number of messages.
            - num_words: Total number of words.
            - num_media_messages: Number of media messages.
            - num_links: Number of links shared.
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

    Parameters:
        df (pd.DataFrame): DataFrame containing the chat data.
        top_n (int): Number of top users to display (default is 5).

    Returns:
        tuple: A tuple containing:
            - top_users: A Series of the top users and their message counts.
            - user_percentage: A DataFrame of the top users and their percentage of total messages.
    """
    # Calculate message counts for all users
    top_users = df['User'].value_counts().head(top_n)
    user_percentage = (df['User'].value_counts(normalize=True) * 100).round(2).reset_index()
    user_percentage.columns = ['User', 'Percentage']

    return top_users, user_percentage

def create_wordcloud(selected_user: str, df: pd.DataFrame):
    """
    Generate a word cloud from the selected user's messages.

    Parameters:
        selected_user (str): The user to generate the word cloud for, or 'Overall' for all users.
        df (pd.DataFrame): DataFrame containing the chat data.

    Returns:
        WordCloud: A WordCloud object generated from the messages.
    """
    # Load stop words
    with open('stop_hinglish.txt', 'r') as file:
        stop_words = set(file.read().split())

    # Filter messages for the selected user
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    # Exclude group notifications and media messages
    filtered_messages = df[(df['User'] != 'group_notification') & (df['Message'] != '<Media omitted>')]

    # Remove stop words from messages
    filtered_messages['Message'] = filtered_messages['Message'].apply(
        lambda msg: " ".join(word for word in msg.lower().split() if word not in stop_words)
    )

    # Generate the word cloud
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    wordcloud = wc.generate(filtered_messages['Message'].str.cat(sep=" "))

    return wordcloud

def most_common_word(selected_user: str, df: pd.DataFrame):
    """
    Get the most common words used by the selected user, excluding stop words.

    Parameters:
        selected_user (str): The user to analyze, or 'Overall' for all users.
        df (pd.DataFrame): DataFrame containing the chat data.

    Returns:
        pd.DataFrame: A DataFrame of the top 20 most common words and their frequencies.
    """
    # Load stop words
    with open('stop_hinglish.txt', 'r') as file:
        stop_words = set(file.read().split())

    # Filter messages for the selected user
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    # Exclude group notifications and media messages
    filtered_messages = df[df['User'] != 'group_notification']
    filtered_messages = filtered_messages[filtered_messages['Message'] != '<Media omitted>']

    # Collect all words excluding stop words
    words = [
        word
        for message in filtered_messages['Message']
        for word in message.lower().split()
        if word not in stop_words
    ]

    # Count the most common words
    word_counts = pd.DataFrame(Counter(words).most_common(20), columns=['Word', 'Frequency'])

    return word_counts
