import re
import pandas as pd

def parse_whatsapp_chat(data):
    # Regex pattern to match the chat log format
    pattern = r"(\d{2}/\d{2}/\d{4}),\s(\d{1,2}:\d{2}\s?[ap]m)\s-\s(\+\d{2}\s\d{3}\s\d{7}):\s(.*)"

    # Find all matches using regex
    matches = re.findall(pattern, data)

    # Create a DataFrame from the extracted matches
    df = pd.DataFrame(matches, columns=['Date', 'Time', 'User', 'Message'])

    # Split the 'Date' column into 'Day', 'Month', 'Year'
    df[['Day', 'Month', 'Year']] = df['Date'].str.split('/', expand=True)

    # Convert 'Date' to datetime format to extract the day name and month name
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

    # Extract the Day name (e.g., Monday, Tuesday)
    df['Day'] = df['Date'].dt.strftime('%A')  # Get the day name (e.g., "Monday")

    # Extract the Month name (e.g., January, February)
    df['Month'] = df['Date'].dt.strftime('%B')  # Get the full month name (e.g., "July")

    # Clean up and split the 'Time' column into 'Hour', 'Minute', and 'AMPM'
    df['Time'] = df['Time'].str.replace('\u202f', ' ')  # Remove non-breaking spaces

    # Split the cleaned 'Time' column into 'Hour:Minute' and 'AMPM'
    df[['Hour_Minute', 'AMPM']] = df['Time'].str.extract(r'(\d{1,2}:\d{2})\s?(am|pm)', expand=True)

    # Split the 'Hour_Minute' into 'Hour' and 'Minute'
    df[['Hour', 'Minute']] = df['Hour_Minute'].str.split(':', expand=True)

    # Drop the original 'Date' and 'Time' columns if you don't need them anymore
    df = df.drop(columns=['Date', 'Time', 'Hour_Minute'])

    # Return the DataFrame
    return df
