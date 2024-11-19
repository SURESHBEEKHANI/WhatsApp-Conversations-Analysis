import re
import pandas as pd

def parse_whatsapp_chat(data):
    """
    Parses WhatsApp chat data and converts it into a structured pandas DataFrame.

    Args:
        data (str): The raw WhatsApp chat log as a string.

    Returns:
        pd.DataFrame: A DataFrame with columns for date, time, user, and message,
                      along with extracted components like day, month, year, hour, and period.
    """
    # Define regex pattern to extract date, time, user, and message
    pattern = r"(\d{2}/\d{2}/\d{4}),\s(\d{1,2}:\d{2}\s?[ap]m)\s-\s([\w\s+]+):\s(.*)"

    # Extract matches using the regex pattern
    matches = re.findall(pattern, data)

    # Create a DataFrame from matches
    df = pd.DataFrame(matches, columns=['Date', 'Time', 'User', 'Message'])

    # Convert 'Date' column to datetime
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    df['only_date'] = df['Date'].dt.date
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.strftime('%B')
    df['month_num'] = df['Date'].dt.month
    df['day_name'] = df['Date'].dt.strftime('%A')

    # Split 'Time' into 'Hour', 'Minute', and 'AM/PM'
    df[['Hour_Minute', 'AMPM']] = df['Time'].str.extract(r'(\d{1,2}:\d{2})\s?(am|pm)', expand=True)
    df[['Hour', 'Minute']] = df['Hour_Minute'].str.split(':', expand=True)
    df['Hour'] = df['Hour'].astype(int)

    # Add time periods in HH AM/PM - HH AM/PM format
    def format_period(hour, ampm):
        next_hour = (hour + 1) % 12 or 12
        next_ampm = 'pm' if hour == 11 and ampm == 'am' else \
                    'am' if hour == 11 and ampm == 'pm' else ampm
        return f"{hour} {ampm} - {next_hour} {next_ampm}"

    df['period'] = df.apply(lambda row: format_period(row['Hour'], row['AMPM']), axis=1)

    return df
