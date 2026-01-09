> Streamlit SQL Inventory System

Streamlit interface for executing and monitoring SQL inventory operations.

## Why does this project exist?
Inventory operations are often managed through spreadsheets or direct database access, which increases the risk of errors and inconsistent data updates. This project demonstrates how a Python library Streamlit can execute inventory workflows while preserving database integrity.

## What can this system do?
* Add new products with automatic stock initialization  
* Detect low-stock products based on reorder thresholds  
* Place and receive reorders using transactional SQL logic  
* Track recent sales and restock activity (rolling 3-month window)  
* View complete product-level inventory history in one place  

## How does it work?
- Streamlit provides the user interface for inventory operations  
- Python acts as the application layer to control database access  
- MySQL handles transactional consistency using views and stored procedures  
- All inventory changes are logged to maintain a full audit trail  

## Business impact
- Reduces manual database interaction and operational errors  
- Improves inventory visibility for operational planning  
- Demonstrates safe execution of business workflows on a SQL backend  

## Tech stack
Python · Streamlit · MySQL · Pandas · SQL
streamlit run app.py

