import mysql.connector

def connection():
    return mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="inventory"
)

def output(cursor):
    queries = {
    "Total Suppliers":"SELECT COUNT(*) as Total_Suppliers FROM suppliers;",
    "Total Products": "SELECT COUNT(*) as Total_Products FROM products;",
    "Total Categories":"SELECT COUNT(DISTINCT category) as Total_Categories fROM products;",
    "Total Sales in last 3 months": """select round(sum(p.price*abs(se.change_quantity)),2) as Total_Sales from stock_entries as se 
        join
        products as p on p.product_id = se.product_id
        where change_type = "Sale"
        and
        se.entry_date>=
        (Select date_sub(max(entry_date),interval 3 month) from stock_entries);""",
    "Total Restock in last 3 months": """select round(sum(p.price*abs(se.change_quantity)),2) as Total_Restocks from stock_entries as se 
        join
        products as p on p.product_id = se.product_id
        where change_type = "Restock"
        and
        se.entry_date>=
        (Select date_sub(max(entry_date),interval 3 month) from stock_entries);""",
    "Below Reorder and No pending Order": """select count(*) from products as p where p.stock_quantity<p.reorder_level and product_id not in
        (select distinct(product_id) from reorders
        where status = "Pending");"""}
    row = {}
    for label, query in queries.items():
        cursor.execute(query)
        result = cursor.fetchone()
        row[label] = list(result.values())[0]
    return row

def table_output(cursor):
    queries = {
        "Suppliers Information": """
            SELECT supplier_name, contact_name, email, phone 
            FROM suppliers;
        """,

        "Product and Supplier Information": """
            SELECT 
                p.product_name,
                p.category,
                p.stock_quantity,
                p.reorder_level,
                s.supplier_name
            FROM products p
            JOIN suppliers s 
                ON p.supplier_id = s.supplier_id
            ORDER BY p.product_name ASC;
        """,

        "Product Reorder Information": """
            SELECT 
                product_id,
                product_name,
                stock_quantity,
                reorder_level 
            FROM products 
            WHERE stock_quantity <= reorder_level;
        """
    }

    result = {}

    for label, query in queries.items():
        cursor.execute(query)
        result[label] = cursor.fetchall()

    return result

def get_categories(cursor):
    cursor.execute("SELECT DISTINCT category FROM products ORDER BY category ASC;")
    rows = cursor.fetchall()
    return [row["category"] for row in rows] 

def get_suppliers(cursor):
    cursor.execute("SELECT supplier_id, supplier_name FROM suppliers ORDER BY supplier_name ASC;")
    return cursor.fetchall()

def AddNewProduct(cursor,db,p_name,p_category,p_price,p_stock_quantity,p_reorder_level,p_supplier_id):
    prod_call = "Call AddProduct(%s,%s,%s,%s,%s,%s)"
    params = (p_name,p_category,p_price,p_stock_quantity,p_reorder_level,p_supplier_id)
    cursor.execute(prod_call,params)
    db.commit()

def get_all_products(cursor):
    cursor.execute("select product_id, product_name from products order by  product_name")
    return cursor.fetchall()

def get_product_history(cursor, product_id):
    query ="select * from product_inventory_history where product_id= %s order by record_date Desc"
    cursor.execute(query , (product_id,))
    return cursor.fetchall()

def place_reorder(cursor, db, product_id , reorder_quantity):
    query= """
         insert into reorders (reorder_id,product_id ,reorder_quantity,reorder_date ,status)
         select 
         max(reorder_id)+1,
         %s,
         %s,
         curdate(),
         "Ordered"
         from reorders;
         """
    cursor.execute(query,(product_id, reorder_quantity))
    db.commit()

def get_pending_reorders(cursor):
    cursor.execute("""
    select r.reorder_id , p.product_name
    from reorders as r join products as p 
    on r.product_id= p.product_id
    """)
    return cursor.fetchall()

def mark_reorder_as_received(cursor, db, reorder_id):
    cursor.callproc("MarkReorderAsReceived",[reorder_id])
    db.commit()
    
