import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_tsla_data():
    # The URL for TSLA historical data
    url = "https://finance.yahoo.com/quote/TSLA/history?period1=1277856000&period2=1699833600&interval=1mo&filter=history&frequency=1mo&includeAdjustedClose=true"
    
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Proceed only if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find the table headers
        headers = [header.text for header in soup.find_all('th')]
        
        # Extracting table rows
        rows_data = []
        for row in soup.find_all('tr'):
            cells = row.find_all('td')
            row_data = [cell.text.strip() for cell in cells]
            if row_data:
                rows_data.append(row_data)
        
        # Create the DataFrame
        df = pd.DataFrame(rows_data, columns=headers)
        
        # Drop the "Volume" column
        df.drop(["Volume"], axis=1, inplace=True)
        
        # Remove rows with stock splits
        df = df[~df['Open'].str.contains("Split")]
        
        # Set the "Date" column as the index
        df.set_index("Date", inplace=True)
        
        # Save the DataFrame to a CSV file
        df.to_csv("TSLA.csv")
    else:
        print(f"Failed to retrieve web page, status code: {response.status_code}")

# Call the function to extract data
extract_tsla_data()
