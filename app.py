

# import pandas as pd
# from flask import Flask, render_template, jsonify
# import plotly.express as px

# # Load CSV file
# data = pd.read_csv("C://Users//3dvec//OneDrive - De Haagse Hogeschool//Sem4//OneDrive - De Haagse Hogeschool//DEDSProject//Dashboard//Sales.csv")
# # data = pd.read_csv("C://Users//Vincent//OneDrive - De Haagse Hogeschool//DEDSProject//Dashboard//Sales.csv")

# # Create Flask app
# app = Flask(__name__)

# # Create a route for the dashboard
# @app.route('/')
# def dashboard():
#     return render_template('dashboard.html')

# # Create a route for the scatter plot
# @app.route('/plot')
# def plot():
#     fig = px.scatter(data, x='Year', y='Revenue')
#     graphJSON = fig.to_json()
#     return graphJSON

# # Create a route for customer data
# @app.route('/customer_data')
# def customer_data():
#     customer_age = data['Customer_Age'].mean()
#     country = data['Country'].value_counts().idxmax()
#     return jsonify(customer_age=customer_age, country=country)

# @app.route('/pie')
# def pie():
#     df = data.groupby('Year')['Revenue'].sum().reset_index()
#     fig = px.pie(df, values='Revenue', names='Year')
#     graphJSON = fig.to_json()
#     return graphJSON

# @app.route('/adventureworks')
# def subpage():
#     return render_template('adventureworks.html')

# # Run the app
# if __name__ == '__main__':
#     app.run(debug=True)


import pandas as pd
from flask import Flask, render_template, jsonify, request
import plotly.express as px

# Load CSV file
# data = pd.read_csv("C://Users//3dvec//OneDrive - De Haagse Hogeschool//Sem4//OneDrive - De Haagse Hogeschool//DEDSProject//Dashboard//Sales.csv")
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
@app.route('/tables')
def tables():
    table_options = data.columns.tolist()  # Assuming each column represents a table
    
    return jsonify(tables=table_options)


@app.route('/adventureworks')
def subpage():
    return render_template('adventureworks.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
