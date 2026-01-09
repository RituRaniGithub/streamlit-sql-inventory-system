> Streamlit SQL Inventory System
<img width="967" height="801" alt="dashboard" src="https://github.com/user-attachments/assets/6f02e566-1f1e-473d-a5cb-a4822248de4e" />

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

## Snapshots
<img width="967" height="801" alt="dashboard" src="https://github.com/user-attachments/assets/374413e4-dcd7-4bc9-af12-b5706285fce0" />
<img width="692" height="871" alt="overview_dash" src="https://github.com/user-attachments/assets/7a884755-3b5b-4d0c-9e51-1c1deaeb0498" />
<img width="673" height="847" alt="operations1" src="https://github.com/user-attachments/assets/e60bcdcc-bc2e-4fbb-b320-88bdfa6cd60c" />
<img width="721" height="582" alt="operations_reorder" src="https://github.com/user-attachments/assets/4946340d-42f5-48bd-ac51-1543fde70511" />
<img width="727" height="500" alt="receive_reorder" src="https://github.com/user-attachments/assets/80574af4-3960-415d-a4b6-6ed57b69a40f" />





