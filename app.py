import pandas as pd
from flask import Flask, render_template, jsonify, request
import plotly.express as px
import numpy as np


# Load CSV file
data = pd.read_csv("C://Users//3dvec//OneDrive - De Haagse Hogeschool//Sem4//OneDrive - De Haagse Hogeschool//DEDSProject//Dashboard//Sales.csv")
# data = pd.read_csv("C://Users//Vincent//OneDrive - De Haagse Hogeschool//DEDSProject//Dashboard//Sales.csv")

# Create Flask app
app = Flask(__name__)

# Create a route for the dashboard
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# Create a route for the scatter plot
@app.route('/plot')
def plot():
    field_a = request.args.get('field_a')
    field_b = request.args.get('field_b')
    
    fig = None
    if field_a and field_b:
        fig = px.scatter(data, x=field_a, y=field_b)
    
    if fig:
        graphJSON = fig.to_json()
        return graphJSON
    else:
        return jsonify(error='Invalid fields A and B')


# Create a route for customer data
@app.route('/customer_data')
def customer_data():
    field_a = request.args.get('field_a')
    field_b = request.args.get('field_b')
    
    if field_a == 'customer_age':
        value_a = data['Customer_Age'].mean()
    elif field_a == 'country':
        value_a = data['Country'].value_counts().idxmax()
    else:
        return jsonify(error='Invalid field A')
    
    if field_b == 'customer_age':
        value_b = data['Customer_Age'].mean()
    elif field_b == 'country':
        value_b = data['Country'].value_counts().idxmax()
    else:
        return jsonify(error='Invalid field B')
    
    return jsonify(value_a=value_a, value_b=value_b)

@app.route('/chartVerkoopPrestaties') 
def chartVerkoopPrestaties():
    selected_product = request.args.get('product')

    # Filter the data based on the selected product
    product_data = data[data['Product'] == selected_product]

    # Check if product data exists
    if product_data.empty:
        return jsonify(error='Selected product not found')

    # Prepare the data for the bar chart
    variables = ['Unit_Cost', 'Unit_Price', 'winst', 'Profit', 'Order_Quantity', 'Revenue']
    labels = ['Unit Cost', 'Unit Price', 'Unit Price / Unit Cost', 'Profit', 'Order Quantity', 'Revenue']
    values = product_data[variables].iloc[0].tolist()

    # Create a bar chart using Plotly Express
    fig = px.bar(x=labels, y=values, labels={'x': 'Variable', 'y': 'Value'}, title=f'Product Data for {selected_product}')

    # Convert the figure to JSON format
    graphJSON = fig.to_json()

    return graphJSON    

# Create a route for generating different types of charts
@app.route('/chart')
def chart():
    chart_type = request.args.get('type')
    field_a = request.args.get('field_a')
    
    fig = None
    if chart_type == 'pie':
        if field_a == 'index':
            df = data[field_a].value_counts().reset_index()
            fig = px.pie(df, values=field_a, names='index')
        else:
            df = data.groupby(field_a)['Revenue'].sum().reset_index()
            fig = px.pie(df, values='Revenue', names=field_a)
    elif chart_type == 'bar':
        df = data.groupby(field_a)['Revenue'].sum().reset_index()
        fig = px.bar(df, x=field_a, y='Revenue')
    
    if fig:
        graphJSON = fig.to_json()
        return graphJSON
    else:
        return jsonify(error='Invalid chart type or field A')

# Create a route to retrieve table options


@app.route('/chartMonthlyPerformance')
def chartMonthlyPerformance():
    selected_product = request.args.get('product')

    # Filter the data based on the selected product
    product_data = data[data['Product'] == selected_product]

    # Check if product data exists
    if product_data.empty:
        return jsonify(error='Selected product not found')

    # Prepare the data for the line graph
    variables = ['Unit_Cost', 'Unit_Price', 'Profit', 'Order_Quantity', 'Revenue']
    chart_data = []

    for variable in variables:
        changes = product_data.groupby('Month')[variable].diff().fillna(0).tolist()
        months = product_data['Month'].tolist()
        chart_item = {
            'variable': variable,
            'months': months,
            'changes': changes
        }
        chart_data.append(chart_item)

    return jsonify(chartData=chart_data)



@app.route('/tablesVerkoopPrestaties') #table van verkoop prestaties is anders dan die van dashboard
def tablesVerkoopPrestaties():
    table_optionsVerkoopPrestatietables = data['Product'].unique().tolist()  # Get unique products from "Product" column
    
    return jsonify(tablesVerkoopPrestatie=table_optionsVerkoopPrestatietables)


@app.route('/tables') #table van dashboard. Anders dan die van VerkoopPrestaties
def tables():
    table_options = data.columns.tolist()  # Assuming each column represents a table
    
    return jsonify(tables=table_options)



@app.route('/adventureworks')
def adventureworks():
    return render_template('adventureworks.html')

@app.route('/verkoopprestaties')
def verkoopprestaties():
    return render_template('verkoopprestaties.html')

@app.route('/product_data')
def product_data():
    selected_product = request.args.get('product')

    # Filter the data based on the selected product
    product_data = data[data['Product'] == selected_product]

    # Prepare the data for the selected product
    product_info = {
        'unitCost': int(product_data['Unit_Cost'].iloc[0]),
        'unitPrice': int(product_data['Unit_Price'].iloc[0]),
        'winst': float(product_data['Unit_Price'].iloc[0]) / float(product_data['Unit_Cost'].iloc[0]),
        'profit': int(product_data['Profit'].iloc[0]),
        'quantity': int(product_data['Order_Quantity'].iloc[0]),
        'revenue': int(product_data['Revenue'].iloc[0])
    }



    # Prepare the response data
    response_data = {
        'productInfo': product_info
    }

    return jsonify(response_data)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)