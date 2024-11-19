# 📊 WhatsApp Chat Analyzer

WhatsApp Chat Analyzer is a Streamlit-based web application that allows users to upload and analyze their WhatsApp chat history. The application provides insights into various aspects of the chat data, including user activity, message trends, word usage, and emoji analysis.

## 🚀 Features

### Core Features:
1. **Upload WhatsApp Chat Files**:
   - Upload `.txt` files exported directly from WhatsApp.
   - Automatic parsing and preprocessing of the uploaded chat data.

2. **Comprehensive Chat Statistics**:
   - Total messages, words, media shared, and links shared.
   - Statistics can be filtered for specific users or overall chat analysis.

3. **Timeline Analysis**:
   - **Monthly Trends**: Visualize message trends over months with clear line charts.
   - **Daily Trends**: Analyze daily activity patterns with precise visualizations.

4. **Activity Analysis**:
   - **Weekly Heatmap**: A heatmap that highlights the busiest days of the week and time slots.
   - **Most Busy Day and Month**: Bar charts showing the days and months with the highest activity.

5. **User Behavior Insights**:
   - **Most Active Users**: Identify top contributors to the chat, along with their activity percentages.
   - Supports individual and overall chat analysis.

6. **Text and Word Analysis**:
   - **Word Cloud**: Beautiful visual representation of the most frequently used words.
   - **Most Common Words**: A bar chart showing the top words used in the chat.

7. **Emoji Analysis**:
   - Detailed breakdown of the most frequently used emojis.
   - Pie charts showing the distribution of top emojis.

### Advanced Features (Planned):
- **Sentiment Analysis**: Detect the overall sentiment of conversations.
- **Chat Summary**: Automated generation of chat summaries.

---

## 🛠️ How to Use

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/SURESHBEEKHANI/WhatsApp-Conversations-Analysis.git
   cd whatsapp-chat-analyzer



### Install Dependencies
Install the required Python libraries by running the following command:


pip install -r requirements.txt

### Run the Application: Launch the Streamlit application
streamlit run app.py

### Upload Chat File:
Upload Chat File
Export a .txt file from WhatsApp.
Upload it through the app's interface to start the analysis.

### 🔍 Key Visualizations:

📈 Chat Statistics
Analyze total messages, words, media shared, and links.
📅 Monthly and Daily Timeline
Visualize message trends over time using monthly and daily charts.
🌟 Word Cloud
Explore the most frequently used words in your chats through a dynamic word cloud.

### 🤖 Technical Details

Programming Language: Python
Framework: Streamlit for the web interface.
Visualization: Matplotlib, Seaborn
Text Analysis: Custom preprocessing logic for WhatsApp data.

#### Project Structure
bash

📂 src/
   ├── preprocessor.py      # Parsing and cleaning WhatsApp chat data
   ├── helper.py            # Core helper functions for analysis
📂 assets/
   ├── example_image_1.png  # Example visualizations
📂 app.py                   # Main Streamlit app file
📂 README.md                # Project documentation

#### requirements.txt            # Dependencies

Python Version: 3.7+
Libraries:
Streamlit
Matplotlib
Seaborn
Pandas
NumPy


### 🛡️ License

This project is licensed under the MIT License.

###  Contact

For questions or feedback, feel free to reach out:

Email: SURESHBEEKHANI26@gmail.com
GitHub: https://github.com/SURESHBEEKHANI
Enjoy analyzing your chats! 🎉
