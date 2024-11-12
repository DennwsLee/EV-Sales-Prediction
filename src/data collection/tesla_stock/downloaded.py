import pandas as pd

def data_parser():
    df = pd.read_csv('vehicles.csv')
    
    # Combine 'make' and 'model' columns into a new 'Model' column and title-case it
    df['Model'] = df['make'].str.cat(df['model'], sep=' ').str.title()
    
    # Define the columns to keep, including the new 'Model' column
    columns_to_keep = ['Model', 'year', 'fuelType', 'city08', 'highway08', 'comb08', 'fuelCost08',
                        'barrels08', 'highwayE', 'cityE', 'combE', 'VClass', 'youSaveSpend', 'atvType']
    
    # Filter out columns to only keep the ones specified
    df = df[columns_to_keep]
    
    # Make the 'Model' column the first column in the dataframe
    cols = df.columns.tolist()
    cols.insert(0, cols.pop(cols.index('Model')))
    df = df[cols]
    


    # Filter the dataframe to only keep rows where 'year' is greater than or equal to 2000
    df = df[df['year'] >= 2000]

    # Remove rows where 'atvType' is 'Hybrid', 'Plug-in Hybrid', or 'Diesel'
    df = df[~df['atvType'].isin(['Hybrid', 'Plug-in Hybrid', 'Diesel'])]

    # Combining makes and models that have the same model, make, year, fuelType
    aggregation_functions = {
        'fuelType': 'first',
        'city08': 'mean',
        'highway08': 'mean',
        'comb08': 'mean',
        'fuelCost08': 'mean',
        'barrels08': 'mean',
        'highwayE': 'mean',
        'cityE':'mean',
        'combE' : 'mean',
        'VClass': 'first',
        'youSaveSpend': 'mean',
        'atvType': 'first'
    }
    
    df = df.groupby(['Model', 'year']).agg(aggregation_functions).reset_index()

    # Sort the DataFrame by 'Year' and 'Model'
    df = df.sort_values(by=['year', 'Model'])

    #Round Annual Consumption to 2 decimal places
    df['barrels08'] = df['barrels08'].round(4)
    df['fuelCost08'] = df['fuelCost08'].round(2)
    df['city08'] = df['city08'].round(2)
    df['highway08'] = df['highway08'].round(2)
    df['comb08'] = df['comb08'].round(2)
    df['youSaveSpend'] = df['youSaveSpend'].round(2)
    df['cityE'] = df['cityE'].round(2)
    df['highwayE'] = df['highwayE'].round(2)
    df['combE'] = df['combE'].round(2)
    


    # Rename columns as needed
    df.rename(columns={
        'barrels08' : 'Annual Consumption (Barrels)',
        'year': 'Year',
        'fuelType':'Fuel Type',
        'city08': 'City MPG',
        'highway08': 'Highway MPG',
        'comb08': 'Combined MPG',
        'fuelCost08': 'Annual Fuel Cost',
        'VClass': 'Vehicle Class',
        'youSaveSpend': 'YouSaveOrSpend',
        'atvType': 'AlternativeVehicleType',
        'cityE' : 'City Electricity Consumption',
        'highwayE' : 'Highway Electricity Consumption',
        'combE' : 'Combined Electricity Consumption',

    # Add any other columns you wish to rename
    }, inplace=True)

    df.to_csv('updatedVehicles.csv')
# Call the function
data_parser()
