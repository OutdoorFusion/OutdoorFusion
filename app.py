import pandas as pd
from flask import Flask, render_template, jsonify, request
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

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
    


# Load CSV file
@app.route('/chartQuantityByCategory')
def chart_quantity_by_category():
    OrderDetailsData = pd.read_csv("C://Users//3dvec//OneDrive - De Haagse Hogeschool//Sem4\OneDrive - De Haagse Hogeschool//OutdoorFusionDashboard//OutdoorFusion//OrderDetailsPerCategorie.csv")
    category_quantity = OrderDetailsData.groupby('CategoryName')['Quantity'].sum().reset_index()

    # Sort by 'Quantity' in descending order
    category_quantity = category_quantity.sort_values('Quantity', ascending=False)

    # Create bar graph data
    chart_data = go.Bar(
        x=category_quantity['CategoryName'],
        y=category_quantity['Quantity']
    )

    # Create bar graph layout
    chart_layout = go.Layout(
        title='Welke producten worden het meest verkocht',
        xaxis={'title': 'Category'},
        yaxis={'title': 'Quantity'}
    )

    # Create figure
    figure = go.Figure(data=[chart_data], layout=chart_layout)

    return figure.to_json()


@app.route('/chartOmzetByCategory')
def chart_omzet_by_category():
    dfOmzet = pd.read_csv("C://Users//3dvec//OneDrive - De Haagse Hogeschool//Sem4//OneDrive - De Haagse Hogeschool//OutdoorFusionDashboard//OutdoorFusion//OmzetPerCategorie.csv")
    # Group by 'CategoryName' and calculate the total 'Omzet'
    category_omzet = dfOmzet.groupby('CategoryName')['Omzet'].sum().reset_index()

    # Sort by 'Omzet' in descending order
    category_omzet = category_omzet.sort_values('Omzet', ascending=False)

    # Create bar graph data
    chart_data = go.Bar(
        x=category_omzet['CategoryName'],
        y=category_omzet['Omzet']
    )

    # Create bar graph layout
    chart_layout = go.Layout(
        title='Welke categorieën leveren de meeste omzet',
        xaxis={'title': 'Category'},
        yaxis={'title': 'Omzet'}
    )

    # Create figure
    figure = go.Figure(data=[chart_data], layout=chart_layout)

    return figure.to_json()




#Categories.CategoryName


# @app.route('/chartOmzetByCategory')
# def chart_omzet_by_category():
#     df = pd.read_csv("C://Users//3dvec//OneDrive - De Haagse Hogeschool//Sem4//OneDrive - De Haagse Hogeschool//OutdoorFusionDashboard//OutdoorFusion//NWSNewCSV.csv")

#     # Group by 'Category.CategoryName' and calculate the total 'Omzet'
#     category_omzet = df.groupby('Categories.CategoryName')['Omzet'].sum().reset_index()

#     # Sort by 'Omzet' in descending order and select the top 10 categories
#     top_10_categories = category_omzet.nlargest(10, 'Omzet')

#     # Create chart data
#     chart_data = go.Bar(
#         x=top_10_categories['Categories.CategoryName'],
#         y=top_10_categories['Omzet']
#     )

#     # Create chart layout
#     chart_layout = go.Layout(
#         title='Top 10 Product Categories by Total Sales',
#         xaxis={'title': 'Category'},
#         yaxis={'title': 'Total Sales'}
#     )

#     # Create figure
#     figure = go.Figure(data=[chart_data], layout=chart_layout)

#     return figure.to_json()







# @app.route('/profit_per_product')
# def profit_per_product():
#     # Perform necessary calculations to obtain the profit per product
#     data['Profit'] = data['Order Details.1.Quantity'] * data['UnitPrice']
#     profit_per_product = data.groupby('ProductName')['Profit'].sum().reset_index()

#     # Create a bar chart using Plotly Express
#     fig = px.bar(profit_per_product, x='ProductName', y='Profit', labels={'ProductName': 'Product', 'Profit': 'Profit'})

#     # Convert the figure to JSON format
#     graphJSON = fig.to_json()

#     return graphJSON



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
    
@app.route('/chartProductProfit')
def chartProductProfit():
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
        if field_a == 'product':
            data['Date'] = pd.to_datetime(data['Date'])
            product_data = data.groupby(['Product', pd.Grouper(key='Date', freq='M')])['Profit'].mean().reset_index()

            fig = px.bar(product_data, x='Date', y='Profit', color='Product',
                         title='Average Profit per Month for Each Product',
                         labels={'Date': 'Date', 'Profit': 'Average Profit', 'Product': 'Product'})
            fig.update_layout(barmode='stack')
    else:
        df = data.groupby(field_a)['Revenue'].sum().reset_index()
        fig = px.bar(df, x=field_a, y='Revenue')

    if fig:
        graphJSON = fig.to_json()
        return graphJSON
    else:
        return jsonify(error='Invalid chart type or field A')
    


@app.route('/top10Products')
def top10Products():
    df = data.groupby('Product')['Revenue'].sum().reset_index()
    df = df.nlargest(10, 'Revenue')

    fig = px.bar(df, x='Product', y='Revenue',
                 title='Top 10 producten kwa opbrengsten',
                 labels={'Product': 'Product', 'Revenue': 'Total Revenue'})

    graphJSON = fig.to_json()
    return graphJSON

@app.route('/top10ProductCategories')
def top10ProductCategories():
    df = data.groupby('Sub_Category')['Revenue'].sum().reset_index()
    df = df.nlargest(10, 'Revenue')

    fig = px.pie(df, values='Revenue', names='Sub_Category',
                 title='Top 10 Product Categories by Revenue')

    graphJSON = fig.to_json()
    return graphJSON



@app.route('/chartProductProfitLine') #TODO verwerk Purchasing.PurchaseOrderHeader hier ook in vanuit Adventureworks. AenC bevat alleen maar unit_price en quantity dat is te weinig
def chartProductProfitLine():         #TODO Verwerk ook Northwind. 
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
        if field_a == 'product':
            product_data = data.groupby(['Product', 'Month'])['Profit'].sum().reset_index()

            fig = px.bar(product_data, x='Month', y='Profit', color='Product',
                         title='Profit per Month for Each Product',
                         labels={'Month': 'Month', 'Profit': 'Profit', 'Product': 'Product'})
            fig.update_layout(barmode='stack')
    elif chart_type == 'line':  # Add a new condition for line graph
        if field_a == 'product':
            product_data = data.groupby(['Product', pd.Grouper(key='Date', freq='M')])['Profit'].sum().reset_index()

            fig = px.line(product_data, x='Date', y='Profit', color='Product',
                          title='Totale winst over alle producten per maand',
                          labels={'Date': 'Date', 'Profit': 'Profit', 'Product': 'Product'})
    else:
        df = data.groupby(field_a)['Revenue'].sum().reset_index()
        fig = px.bar(df, x=field_a, y='Revenue')

    # Return the figure as JSON
    return fig.to_json()





@app.route('/tablesVerkoopPrestaties') #table van verkoop prestaties is anders dan die van dashboard
def tablesVerkoopPrestaties():
    table_optionsVerkoopPrestatietables = data['Product'].unique().tolist()  # Get unique products from "Product" column
    
    return jsonify(tablesVerkoopPrestatie=table_optionsVerkoopPrestatietables)


@app.route('/tables') #table van dashboard. Anders dan die van VerkoopPrestaties
def tables():
    table_options = data.columns.tolist()  # Assuming each column represents a table
    
    return jsonify(tables=table_options)



# Create a route for the adventureworks page
@app.route('/adventureworks')
def adventureworks():
    return render_template('adventureworks.html')

# Create a route for the verkoopprestaties page
@app.route('/verkoopprestaties')
def verkoopprestaties():
    return render_template('verkoopprestaties.html')

@app.route('/productprofit')
def productprofit():
    return render_template('productprofit.html')

@app.route('/productinzien')
def productinzien():
    return render_template('productinzien.html')

@app.route('/northwindprestaties')
def northwindprestaties():
    return render_template('northwindprestaties.html')

@app.route('/bikestoreprestaties')
def bikestoreprestaties():
    return render_template('bikestoreprestaties.html')
           



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
    'Sub_Category': int(product_data['Sub_Category'].iloc[0]),
    'revenue': int(product_data['Revenue'].iloc[0]),

    # 'date': product_data['Date'].iloc[0].strftime('%Y-%m-%d'),  #TODO sloopt op dit moment de 'Productinzien' pagina
    # 'Product_Category': product_data['Product_Category'].iloc[0]
}
    # Prepare the response data
    response_data = {
        'productInfo': product_info
    }

    return jsonify(response_data)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)