from urlextract import URLExtract
from collections import Counter
import emoji
from wordcloud import WordCloud

# Create an object that will help in extracting URLs
extract = URLExtract()

# Create an object that will help in extracting URLs
extract = URLExtract()
class Helper:
    def __init__(self, df):
        self.df = df

    def fetch_stats(self, selected_user):
        """
        Fetch basic statistics for a selected user or for all users if 'Overall' is selected.

        Parameters:
            selected_user (str): The user to fetch stats for, or 'Overall' for aggregate stats.

        Returns:
            tuple: A tuple containing the number of messages, number of words, 
                   number of media messages, and number of links shared.
        """
        # Ensure selected_user is a string (in case it's a pandas Series)
        if not isinstance(selected_user, str):
            raise ValueError("selected_user should be a string")

        # If the selected user is not 'Overall', filter the data for that specific user
        if selected_user != 'Overall':
            df_filtered = self.df[self.df['User'] == selected_user]
        else:
            df_filtered = self.df  # Use entire DataFrame for 'Overall' stats

        # Count how many messages the selected user has sent
        num_messages = df_filtered.shape[0]

        # Create a list to hold all words from the messages
        words = []
        for message in df_filtered['Message']:
            words.extend(message.split())

        # Count how many media messages (like images or videos) the user sent
        num_media_messages = df_filtered[df_filtered['Message'] == '<Media omitted>'].shape[0]

        # Create a list to hold all the links shared by the user
        links = []
        for message in df_filtered['Message']:
            links.extend(extract.find_urls(message))

        return num_messages, len(words), num_media_messages, len(links)
