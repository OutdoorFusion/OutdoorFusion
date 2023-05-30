import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# Read the data from the CSV file or any other data source
data = pd.read_csv("C://Users//3dvec//OneDrive - De Haagse Hogeschool//Sem4//OneDrive - De Haagse Hogeschool//DEDSProject//Dashboard//Sales.csv")

# Convert the 'Date' column to datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Filter the data for the years 2014, 2015, and 2016
filtered_data = data[(data['Date'].dt.year >= 2014) & (data['Date'].dt.year <= 2016)]

# Group the filtered data by month and calculate the mean of revenue and profit, and sum of product count per month
monthly_data = filtered_data.groupby(pd.Grouper(key='Date', freq='M')).agg({'Revenue': 'mean', 'Profit': 'mean', 'Product': 'sum'}).reset_index()

# Remove rows with missing values
monthly_data = monthly_data.dropna()

# Prepare the data for training revenue
X_train_revenue = monthly_data['Date'].apply(lambda x: x.toordinal()).values.reshape(-1, 1)
y_train_revenue = monthly_data['Revenue'].values

# Prepare the data for training profit with monthly dummy variables
X_train_profit = pd.get_dummies(monthly_data['Date'].dt.month, prefix='month').values
y_train_profit = monthly_data['Profit'].values

# Train the revenue model
revenue_model = LinearRegression()
revenue_model.fit(X_train_revenue, y_train_revenue)

# Train the profit model
profit_model = LinearRegression()
profit_model.fit(X_train_profit, y_train_profit)

# Generate predictions for the years 2017, 2018, and 2019
prediction_dates = pd.date_range(start='2016-08-01', end='2025-12-31', freq='M')
X_pred_revenue = np.array([date.toordinal() for date in prediction_dates]).reshape(-1, 1)
X_pred_profit = pd.get_dummies(prediction_dates.month, prefix='month').values

predicted_revenue = revenue_model.predict(X_pred_revenue)
predicted_profit = profit_model.predict(X_pred_profit)

# Introduce random noise to the predicted revenue and profit
multiplier = 3  # Adjust the multiplier as needed
noise_revenue = np.random.normal(scale=1000 * multiplier, size=len(predicted_revenue))
noise_profit = np.random.normal(scale=100 * multiplier, size=len(predicted_profit))

predicted_revenue += noise_revenue
predicted_profit += noise_profit

# Create a new dataframe for the predicted revenue, profit, and product count
predicted_data = pd.DataFrame({'Date': prediction_dates, 'Revenue': predicted_revenue, 'Profit': predicted_profit})
predicted_data['Product'] = 0  # Placeholder for predicted product count

# Add the Sub_Category column
predicted_data['Sub_Category'] = ""

# Concatenate the existing data and the predicted data
output_data = pd.concat([data[['Date', 'Revenue', 'Profit', 'Product', 'Sub_Category']], predicted_data])

# Extract Day, Month, and Year into separate columns
output_data['Day'] = output_data['Date'].dt.day
output_data['Month'] = output_data['Date'].dt.month
output_data['Year'] = output_data['Date'].dt.year

# Format the 'Date' column as desired (e.g., 'yyyy-mm-dd')
output_data['Date'] = output_data['Date'].dt.strftime('%Y-%m-%d')

# Save the combined data to a new CSV file
output_data.to_csv('combined_revenue_profit_product.csv2', index=False)
