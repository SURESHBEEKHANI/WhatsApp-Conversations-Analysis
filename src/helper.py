import matplotlib.pyplot as plt  # type: ignore
from urlextract import URLExtract
from wordcloud import WordCloud


# Initialize URL extractor globally
url_extractor = URLExtract()

def fetch_stats(df, selected_user):
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
    if selected_user != 'Overall':
        df_filtered = df[df['User'] == selected_user]
    else:
        df_filtered = df

    # Calculate statistics
    num_messages = df_filtered.shape[0]
    words = [word for message in df_filtered['Message'] for word in message.split()]
    num_media_messages = df_filtered[df_filtered['Message'] == '<Media omitted>'].shape[0]
    links = [link for message in df_filtered['Message'] for link in url_extractor.find_urls(message)]

    return num_messages, len(words), num_media_messages, len(links)
def top_active_users(df):
    """
    Calculates the top N most active users based on their message count.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the chat data.
        top_n (int): The number of top users to display (default is 5).

    Returns:
        tuple: A tuple containing:
               - A Series of the top users and their message counts
               - A DataFrame of the top users and their percentage of total messages
    """
    # Get the top N users by message count
    x = df['User'].value_counts().head()
    
    # Calculate the percentage of total messages for these top users
    df = round((df['User'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'name', 'User': 'percent'})

    return x, df

def create_wordcloud(selected_user,df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    temp = df[df['User'] != 'group_notification']
    temp = temp[temp['Message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['Message'] = temp['Message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['Message'].str.cat(sep=" "))
    return df_wc