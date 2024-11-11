import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
import requests
import openai
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Title of the dashboard
st.title("AI Agent Dashboard")

# Step 1: File upload section
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
if uploaded_file:
    # Load the uploaded file as a DataFrame and display a preview
    df = pd.read_csv(uploaded_file)
    st.write("Preview of Uploaded Data:", df.head())

    # Step 2: Allow the user to select the main column
    main_column = st.selectbox("Select main column", df.columns)

    # Step 3: Input box for query template
    query_template = st.text_input("Enter your search query template", "Get the email of {company}")

    # Step 4: Button to start the search process
    if st.button("Start Search"):
        st.write("Processing data...")  # Placeholder for further code
        # Option to choose between CSV upload and Google Sheets
data_source = st.radio("Choose Data Source", ("CSV Upload", "Google Sheets"))

# If user chooses Google Sheets
if data_source == "Google Sheets":
    spreadsheet_id = st.text_input("Enter Google Sheet ID")
    range_name = st.text_input("Enter Data Range (e.g., 'Sheet1!A1:D10')")
    credentials = service_account.Credentials.from_service_account_file("credentials.json")
    service = build('sheets', 'v4', credentials=credentials)

    # Function to get data from Google Sheets
    def get_sheet_data(spreadsheet_id, range_name):
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        return pd.DataFrame(result.get('values', []))

    if st.button("Load Google Sheet"):
        df = get_sheet_data(spreadsheet_id, range_name)
        st.write("Preview of Google Sheets Data:", df.head())
        main_column = st.selectbox("Select main column", df.columns)
        query_template = st.text_input("Enter your search query template", "Get the email of {company}")

load_dotenv()  # Load environment variables
serpapi_key = os.getenv("SERPAPI_KEY")

# Function to search for each entity (replace with real API calls)
def search_entity(query):
    params = {
        "q": query,
        "api_key": serpapi_key
    }
    response = requests.get("https://serpapi.com/search", params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None
        if st.button("Start Search"):
            # Indented block starts here
            results = []
            for entity in df[main_column]:  # Loop over each entity in the selected column
                query = query_template.replace("{company}", entity)
                search_result = search_entity(query)
                results.append((entity, search_result))
            st.write("Search Results:", results)
openai.api_key = os.getenv("OPENAI_API_KEY")
def parse_search_results(results):
    prompt = f"Extract the information based on the results: {results}"
    response = openai.Completion.create(model="text-davinci-003", prompt=prompt, max_tokens=100)
    return response.choices[0].text.strip()
    if st.button("Download Results as CSV"):
       st.download_button("Download", data=extracted_df.to_csv(index=False), file_name="results.csv", mime="text/csv")

    
