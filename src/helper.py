import matplotlib.pyplot as plt  # type: ignore
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd

# Initialize URL extractor globally
url_extractor = URLExtract()

def fetch_stats(df: pd.DataFrame, selected_user: str):
    """
    Fetch basic statistics for a selected user or for all users if 'Overall' is selected.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the chat data.
        selected_user (str): The user to fetch stats for, or 'Overall' for aggregate stats.

    Returns:
        tuple: A tuple containing:
               - Number of messages
               - Number of words
               - Number of media messages
               - Number of links shared
    """
    # Filter the DataFrame based on the selected user
    df_filtered = df if selected_user == 'Overall' else df[df['User'] == selected_user]

    # Calculate statistics
    num_messages = df_filtered.shape[0]
    num_words = sum(len(message.split()) for message in df_filtered['Message'])
    num_media_messages = df_filtered[df_filtered['Message'] == '<Media omitted>'].shape[0]
    num_links = sum(len(url_extractor.find_urls(message)) for message in df_filtered['Message'])

    return num_messages, num_words, num_media_messages, num_links

def top_active_users(df: pd.DataFrame, top_n: int = 5):
    """
    Calculate the top N most active users based on their message count.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the chat data.
        top_n (int): The number of top users to display (default is 5).

    Returns:
        tuple: A tuple containing:
               - A Series of the top users and their message counts
               - A DataFrame of the top users and their percentage of total messages
    """
    # Calculate message counts for all users
    top_users = df['User'].value_counts().head(top_n)
    user_percentage = (df['User'].value_counts(normalize=True) * 100).round(2).reset_index()
    user_percentage.columns = ['name', 'percent']

    return top_users, user_percentage

def create_wordcloud(selected_user: str, df: pd.DataFrame):
    """
    Generate a word cloud for the selected user's messages.

    Parameters:
        selected_user (str): The user to generate the word cloud for, or 'Overall' for all users.
        df (pd.DataFrame): The DataFrame containing the chat data.

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
    temp = df[(df['User'] != 'group_notification') & (df['Message'] != '<Media omitted>\n')]

    # Remove stop words from messages
    def remove_stop_words(message):
        return " ".join(word for word in message.lower().split() if word not in stop_words)

    temp['Message'] = temp['Message'].apply(remove_stop_words)

    # Generate the word cloud
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    wordcloud = wc.generate(temp['Message'].str.cat(sep=" "))

    return wordcloud
