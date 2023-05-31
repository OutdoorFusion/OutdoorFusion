import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Read the data from the NorthwindNew2.csv file
data = pd.read_csv("C:/Users/3dvec/OneDrive - De Haagse Hogeschool/Sem4/OneDrive - De Haagse Hogeschool/OutdoorFusionDashboard/OutdoorFusion/NorthwindNew2.csv",
                   parse_dates=['OrderDate'], dayfirst=True)

# Define a custom function to remove commas and 'XDR' prefix
def clean_quantity(value):
    if isinstance(value, str):
        value = value.replace(',', '').replace('XDR', '')
    return value

# Apply the custom function to the 'Quantity' column
data['Quantity'] = data['Quantity'].apply(clean_quantity)

# Convert the 'Quantity' column to a numeric type
data['Quantity'] = pd.to_numeric(data['Quantity'], errors='coerce')

# Create an empty DataFrame to store the forecasted data
forecast_data = pd.DataFrame()

# Iterate over each unique category
for category in data['Categories.CategoryName'].unique():
    # Filter data for the current category
    category_data = data[data['Categories.CategoryName'] == category]

    # Group the data by month and calculate the sum of quantities
    monthly_data = category_data.groupby(pd.Grouper(key='OrderDate', freq='M'))['Quantity'].sum().reset_index()

    # Create a time series with the sum of quantities
    time_series = monthly_data.set_index('OrderDate')['Quantity']

    # Find the first non-null value in the time series
    first_valid_index = time_series.first_valid_index()

    # Subset the time series starting from the first non-null value
    time_series = time_series.loc[first_valid_index:]

    # Fit a SARIMA model to the time series
    model = SARIMAX(time_series, order=(1, 1, 1), seasonal_order=(0, 1, 1, 12))
    model_fit = model.fit()

    # Generate future dates for the current category starting from the first non-null value
    future_dates = pd.date_range(start=first_valid_index, end='2010-12-31', freq='M')

    # Predict for the future dates
    predictions = model_fit.predict(start=len(time_series), end=len(time_series) + len(future_dates) - 1)

    # # Add randomness to the predictions within three-month time periods
    # random_values = np.random.normal(loc=0, scale=5, size=len(predictions))
    # predictions = predictions + random_values

    # Create a DataFrame for the current category's forecasted data
    future_data = pd.DataFrame({'OrderDate': future_dates, 'Quantity': predictions})
    future_data['Categories.CategoryName'] = category

    # Append the current category's forecasted data to the overall forecasted data
    forecast_data = pd.concat([forecast_data, future_data], ignore_index=True)

# Concatenate the original data and the forecasted data
combined_data = pd.concat([data, forecast_data])

# Save the combined data as a CSV file
combined_data.to_csv("combined_data.csv", index=False)
