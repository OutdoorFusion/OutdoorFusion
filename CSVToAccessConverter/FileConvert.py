import csv
import os
import pyodbc

# Define the folder path containing the CSV files
folder_path = 'C://Users//3dvec//OneDrive - De Haagse Hogeschool//Sem4//OneDrive - De Haagse Hogeschool//DEDSProject//AdventureWorks'

# Define the Access database path
access_db = 'C://Users//3dvec//OneDrive - De Haagse Hogeschool//Sem4//OneDrive - De Haagse Hogeschool//DEDSProject//Dashboard//AdventureWorks.accdb'

# Get the list of CSV files in the folder
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# Establish a connection to the Access database
conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + access_db)

# Create a cursor object
cursor = conn.cursor()

# Loop through the CSV files and convert them to Access tables
for file in csv_files:
    # Construct the full file path
    file_path = os.path.join(folder_path, file)

    # Extract the table name from the file name
    table_name = os.path.splitext(file)[0]

    # Create the table in the Access database
    try:
        with open(file_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            headers = next(csv_reader)
            cleaned_headers = [header.replace('.', '_') for header in headers]
            columns = [f"[{header.strip()}] TEXT" for header in cleaned_headers]
            create_table_query = f"CREATE TABLE [{table_name}] ({', '.join(columns)})"
            cursor.execute(create_table_query)
    except Exception as e:
        print(f"An error occurred while creating table '{table_name}': {str(e)}")
        continue
    
    # Insert data into the table
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            insert_query = f"INSERT INTO [{table_name}] VALUES ({', '.join(['?'] * len(row))})"
            cursor.execute(insert_query, row)

# Commit the changes and close the connection
conn.commit()
conn.close()