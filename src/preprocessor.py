import re
import pandas as pd

def parse_whatsapp_chat(data):
    """
    Parses WhatsApp chat data and converts it into a structured pandas DataFrame.

    Args:
        data (str): The raw WhatsApp chat log as a string.

    Returns:
        pd.DataFrame: A DataFrame with columns for date, time, user, and message,
                      along with extracted components like day, month, year, hour, and minute.
    """
    # Define the regex pattern to extract details from the chat log
    pattern = r"(\d{2}/\d{2}/\d{4}),\s(\d{1,2}:\d{2}\s?[ap]m)\s-\s(\+\d{2}\s\d{3}\s\d{7}):\s(.*)"
    
    # Extract matches from the chat log using the regex pattern
    matches = re.findall(pattern, data)

    # Create a DataFrame from the extracted matches
    df = pd.DataFrame(matches, columns=['Date', 'Time', 'User', 'Message'])

    # Convert the 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    # Extract the Day name (e.g., Monday, Tuesday) and Month name
    df['Day'] = df['Date'].dt.strftime('%A')  # Full day name
    df['Month'] = df['Date'].dt.strftime('%B')  # Full month name
    df['Year'] = df['Date'].dt.year  # Year as a separate column
    df['month_num'] = df['Date'].dt.month
    # Clean and split the 'Time' column into components
    df[['Hour_Minute', 'AMPM']] = df['Time'].str.extract(r'(\d{1,2}:\d{2})\s?(am|pm)', expand=True)

    # Further split 'Hour_Minute' into 'Hour' and 'Minute'
    df[['Hour', 'Minute']] = df['Hour_Minute'].str.split(':', expand=True)

    # Drop unnecessary intermediate columns
    df = df.drop(columns=['Hour_Minute', 'Time'])

    # Return the final structured DataFrame
    return df
