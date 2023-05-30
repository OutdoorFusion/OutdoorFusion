import pandas as pd
from flask import Flask, render_template, jsonify, request
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import json


data = pd.read_csv("C://Users//3dvec//OneDrive - De Haagse Hogeschool//Sem4//OneDrive - De Haagse Hogeschool//DEDSProject//Dashboard//Sales.csv")
# data = pd.read_csv("C://Users//Vincent//OneDrive - De Haagse Hogeschool//DEDSProject//Dashboard//Sales.csv")
app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

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
    


@app.route('/chartQuantityByCategory')
def chart_quantity_by_category():
    OrderDetailsData = pd.read_csv("C://Users//3dvec//OneDrive - De Haagse Hogeschool//Sem4\OneDrive - De Haagse Hogeschool//OutdoorFusionDashboard//OutdoorFusion//OrderDetailsPerCategorie.csv")
    # OrderDetailsData = pd.read_csv("C://Users//Vincent//OneDrive - De Haagse Hogeschool//OutdoorFusionDashboard//OutdoorFusion//OrderDetailsPerCategorie.csv")
    category_quantity = OrderDetailsData.groupby('CategoryName')['Quantity'].sum().reset_index()

    category_quantity = category_quantity.sort_values('Quantity', ascending=False)

    chart_data = go.Bar(
        x=category_quantity['CategoryName'],
        y=category_quantity['Quantity']
    )

    chart_layout = go.Layout(
        title='Welke producten worden het meest verkocht',
        xaxis={'title': 'Category'},
        yaxis={'title': 'Quantity'}
    )

    figure = go.Figure(data=[chart_data], layout=chart_layout)

    return figure.to_json()


@app.route('/chartOmzetByCategory')
def chart_omzet_by_category():
    dfOmzet = pd.read_csv("C://Users//3dvec//OneDrive - De Haagse Hogeschool//Sem4//OneDrive - De Haagse Hogeschool//OutdoorFusionDashboard//OutdoorFusion//OmzetPerCategorie.csv")
    # dfOmzet = pd.read_csv("C://Users//Vincent//OneDrive - De Haagse Hogeschool//OutdoorFusionDashboard//OutdoorFusion//OmzetPerCategorie.csv")
    category_omzet = dfOmzet.groupby('CategoryName')['Omzet'].sum().reset_index()

    category_omzet = category_omzet.sort_values('Omzet', ascending=False)

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

    product_data = data[data['Product'] == selected_product]

    if product_data.empty:
        return jsonify(error='Selected product not found')

    variables = ['Unit_Cost', 'Unit_Price', 'winst', 'Profit', 'Order_Quantity', 'Revenue']
    labels = ['Unit Cost', 'Unit Price', 'Unit Price / Unit Cost', 'Profit', 'Order Quantity', 'Revenue']
    values = product_data[variables].iloc[0].tolist()

    fig = px.bar(x=labels, y=values, labels={'x': 'Variable', 'y': 'Value'}, title=f'Product Data for {selected_product}')

    graphJSON = fig.to_json()

    return graphJSON    

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
    





import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import json

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import json

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import json

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.express as px



import pandas as pd
import plotly.express as px

# Read the data from the combined_revenue_profit_product.csv file
data = pd.read_csv("C://Users//3dvec//OneDrive - De Haagse Hogeschool//Sem4//OneDrive - De Haagse Hogeschool//OutdoorFusionDashboard//OutdoorFusion//combined_revenue_profit_product.csv")
data['Date'] = pd.to_datetime(data['Date'])

@app.route('/chartOriginal')
def chartOriginal():
    chart_type = request.args.get('type')
    field_a = request.args.get('field_a')

    if chart_type == 'bar':
        if field_a == 'product':
            df = data.groupby('Product')['Profit'].sum().reset_index()
            fig = px.bar(df, x='Product', y='Profit', title='Profit per Product',
                         labels={'Product': 'Product', 'Profit': 'Profit'})
        else:
            df = data.groupby(field_a)['Revenue'].sum().reset_index()
            fig = px.bar(df, x=field_a, y='Revenue')
    elif chart_type == 'pie':
        if field_a == 'index':
            df = data[field_a].value_counts().reset_index()
            fig = px.pie(df, values=field_a, names='index')
        else:
            df = data.groupby(field_a)['Revenue'].sum().reset_index()
            fig = px.pie(df, values='Revenue', names=field_a)
    else:
        return jsonify(error='Invalid chart type')

    if fig:
        graphJSON = fig.to_json()
        return graphJSON
    else:
        return jsonify(error='Invalid chart type or field A')




# Read the data from the combined_revenue_profit_product.csv file
data = pd.read_csv("C://Users//3dvec//OneDrive - De Haagse Hogeschool//Sem4//OneDrive - De Haagse Hogeschool//OutdoorFusionDashboard//OutdoorFusion//combined_revenue_profit_product.csv2")
data['Date'] = pd.to_datetime(data['Date'])


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
            df = data.groupby(field_a)['Profit'].sum().reset_index()
            fig = px.pie(df, values='Profit', names=field_a)
    elif chart_type == 'bar':
        if field_a == 'product':
            product_data = data.groupby(['Product', pd.Grouper(key='Date', freq='M')]).agg({'Profit': 'mean'}).reset_index()

            # Prepare the training data for all products
            X_train_product = product_data[product_data['Date'] < '2016-08-01']['Date'].apply(lambda x: x.toordinal()).values.reshape(-1, 1)
            y_train_product = product_data[product_data['Date'] < '2016-08-01']['Profit'].values

            # Train the linear regression model for all products
            model_product = LinearRegression()
            model_product.fit(X_train_product, y_train_product)

            # Generate predictions for all products
            prediction_dates = pd.date_range(start='2016-08-01', end='2025-12-31', freq='M')
            X_pred_product = np.array([date.toordinal() for date in prediction_dates]).reshape(-1, 1)
            predicted_profits_product = model_product.predict(X_pred_product)

            # Create a dataframe to store the predicted profits
            predicted_data = pd.DataFrame({'Date': prediction_dates, 'Profit': predicted_profits_product})

            # Update the bar chart with the predicted data
            fig = px.bar(predicted_data, x='Date', y='Profit', title='Average Profit per Month',
                         labels={'Date': 'Date', 'Profit': 'Average Profit'})
            fig.update_layout(barmode='stack')
        else:
            df = data.groupby(field_a)['Profit'].sum().reset_index()
            fig = px.bar(df, x=field_a, y='Profit')
    else:
        return jsonify(error='Invalid chart type')

    if fig:
        graphJSON = fig.to_json()
        return graphJSON
    else:
        return jsonify(error='Invalid chart type or field A')


#PREDICTED REVENUE
# @app.route('/chartProductRevenue')
# def chartProductRevenue():
#     chart_type = request.args.get('type')
#     field_a = request.args.get('field_a')

#     fig = None
#     if chart_type == 'pie':
#         if field_a == 'index':
#             df = data[field_a].value_counts().reset_index()
#             fig = px.pie(df, values=field_a, names='index')
#         else:
#             df = data.groupby(field_a)['Revenue'].sum().reset_index()
#             fig = px.pie(df, values='Revenue', names=field_a)
#     elif chart_type == 'bar':
#         if field_a == 'product':
#             product_data = data.groupby(['Product', pd.Grouper(key='Date', freq='M')]).agg({'Revenue': 'mean'}).reset_index()

#             # Prepare the training data for all products
#             X_train_product = product_data[product_data['Date'] < '2016-08-01']['Date'].apply(lambda x: x.toordinal()).values.reshape(-1, 1)
#             y_train_product = product_data[product_data['Date'] < '2016-08-01']['Revenue'].values

#             # Train the linear regression model for all products
#             model_product = LinearRegression()
#             model_product.fit(X_train_product, y_train_product)

#             # Generate predictions for all products
#             prediction_dates = pd.date_range(start='2016-08-01', end='2025-12-31', freq='M')
#             X_pred_product = np.array([date.toordinal() for date in prediction_dates]).reshape(-1, 1)
#             predicted_revenue_product = model_product.predict(X_pred_product)

#             # Create a dataframe to store the predicted revenues
#             predicted_data = pd.DataFrame({'Date': prediction_dates, 'Revenue': predicted_revenue_product})

#             # Update the bar chart with the predicted data
#             fig = px.bar(predicted_data, x='Date', y='Revenue', title='Average Revenue per Month',
#                          labels={'Date': 'Date', 'Revenue': 'Average Revenue'})
#             fig.update_layout(barmode='stack')
#         else:
#             df = data.groupby(field_a)['Revenue'].sum().reset_index()
#             fig = px.bar(df, x=field_a, y='Revenue')
#     else:
#         return jsonify(error='Invalid chart type')

#     if fig:
#         graphJSON = fig.to_json()
#         return graphJSON
#     else:
#         return jsonify(error='Invalid chart type or field A')




    


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

    return fig.to_json()





@app.route('/tablesVerkoopPrestaties') #table van verkoop prestaties is anders dan die van dashboard
def tablesVerkoopPrestaties():
    table_optionsVerkoopPrestatietables = data['Product'].unique().tolist()  # Get unique products from "Product" column
    
    return jsonify(tablesVerkoopPrestatie=table_optionsVerkoopPrestatietables)


@app.route('/tables') #table van dashboard. Anders dan die van VerkoopPrestaties
def tables():
    table_options = data.columns.tolist()  
    
    return jsonify(tables=table_options)



@app.route('/adventureworks')
def adventureworks():
    return render_template('adventureworks.html')

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

    product_data = data[data['Product'] == selected_product]

    product_info = {
    'unitCost': int(product_data['Unit_Cost'].iloc[0]),
    'unitPrice': int(product_data['Unit_Price'].iloc[0]),
    'winst': float(product_data['Unit_Price'].iloc[0]) / float(product_data['Unit_Cost'].iloc[0]),
    'profit': int(product_data['Profit'].iloc[0]),
    'quantity': int(product_data['Order_Quantity'].iloc[0]),
    # 'Sub_Category': int(product_data['Sub_Category'].iloc[0]),
    'Sub_Category': product_data['Sub_Category'].iloc[0],
    'revenue': int(product_data['Revenue'].iloc[0]),

    # 'date': product_data['Date'].iloc[0].strftime('%Y-%m-%d'),  #TODO sloopt op dit moment de 'Productinzien' pagina
    # 'Product_Category': product_data['Product_Category'].iloc[0]
}
    response_data = {
        'productInfo': product_info
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)