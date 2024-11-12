from bs4 import BeautifulSoup
import pandas as pd

def extra_source1():
    # Load the HTML content from the given file path
    with open("TSLA1.html", 'r', encoding='utf-8') as file:
        content = file.read()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(content, "html.parser")

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

    # Drop the "Volume" column if it exists
    if "Volume" in df.columns:
        df.drop(["Volume"], axis=1, inplace=True)

    # Convert the 'Open' column to string type to handle None/NaN values
    df['Open'] = df['Open'].astype(str)

    # Remove rows with stock splits by filtering out rows where 'Open' column contains 'Split'
    df = df[~df['Open'].str.contains("Split")]

    # Set the "Date" column as the index if it exists
    if "Date" in df.columns:
        df.set_index("Date", inplace=True)

    # Save the DataFrame to the given CSV file path
    df.to_csv("TSLA.csv")

    print(df)

# Call the function to extract data and save it to a CSV file
extra_source1()
