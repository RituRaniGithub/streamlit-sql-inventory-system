import pandas as pd
import streamlit as st
from invenfunctions import (
    connection, output, table_output,
    get_categories, get_suppliers,
    AddNewProduct, get_product_history,
    get_all_products, place_reorder,
    get_pending_reorders, mark_reorder_as_received
)

# ------------------ HEADER ------------------
st.title("Inventory Operations Dashboard")
st.caption("Inventory analytics & operational controls")

db = connection()
cursor = db.cursor(dictionary=True)

# ------------------ MAIN SECTIONS ------------------
section = st.selectbox(
    "Choose Section",
    ["Analytics", "Operations"]
)

# =================================================
# ================= ANALYTICS =====================
# =================================================
if section == "Analytics":
    st.subheader("Inventory Summary")

    data = output(cursor)
    keys = list(data.keys())

    col1, col2, col3 = st.columns(3)
    col1.metric(keys[0], data[keys[0]])
    col2.metric(keys[1], data[keys[1]])
    col3.metric(keys[2], data[keys[2]])

    col4, col5, col6 = st.columns(3)
    col4.metric(keys[3], data[keys[3]])
    col5.metric(keys[4], data[keys[4]])
    col6.metric(keys[5], data[keys[5]])

    st.divider()

    tables = table_output(cursor)
    for label, rows in tables.items():
        st.subheader(label)
        st.dataframe(pd.DataFrame(rows))
        st.divider()

# =================================================
# ================= OPERATIONS ====================
# =================================================
if section == "Operations":
    st.subheader("⚙️ Inventory Operations")

    task = st.selectbox(
        "Select Operation",
        ["Add Product", "Product History", "Place Reorder", "Receive Reorder"]
    )

    # ---------------- ADD PRODUCT ----------------
    if task == "Add Product":
        category = get_categories(cursor)
        suppliers = get_suppliers(cursor)

        st.markdown("### Add New Product")

        with st.form("add_product_form"):
            product_name = st.text_input("Product Name")
            product_category = st.selectbox("Category", category)
            product_price = st.number_input("Price", min_value=0.0)
            product_stock = st.number_input("Stock", min_value=0, step=1)
            product_reorder = st.number_input("Reorder Level", min_value=0, step=1)

            supplier_ids = [s["supplier_id"] for s in suppliers]
            supplier_names = [s["supplier_name"] for s in suppliers]

            supplier_selection = st.selectbox(
                "Supplier",
                options=supplier_ids,
                format_func=lambda x: supplier_names[supplier_ids.index(x)]
            )

            submitted = st.form_submit_button("Add Product")

        if submitted:
            try:
                AddNewProduct(
                    cursor, db,
                    product_name, product_category,
                    product_price, product_stock,
                    product_reorder, supplier_selection
                )
                st.success("Product added successfully 🎉")
            except Exception as e:
                st.error(f"Error: {e}")

    # ---------------- PRODUCT HISTORY ----------------
    if task == "Product History":
        st.markdown("### Product Inventory History")

        products = get_all_products(cursor)
        product_names = [p["product_name"] for p in products]
        product_ids = [p["product_id"] for p in products]

        selected_product = st.selectbox("Select Product", product_names)

        if selected_product:
            pid = product_ids[product_names.index(selected_product)]
            history = get_product_history(cursor, pid)

            if history:
                st.dataframe(pd.DataFrame(history))
            else:
                st.info("No history available for this product.")

    # ---------------- PLACE REORDER ----------------
    if task == "Place Reorder":
        st.markdown("### Place Reorder")

        products = get_all_products(cursor)
        product_names = [p["product_name"] for p in products]
        product_ids = [p["product_id"] for p in products]

        selected_product = st.selectbox("Select Product", product_names)
        reorder_qty = st.number_input("Reorder Quantity", min_value=1, step=1)

        if st.button("Place Reorder"):
            try:
                pid = product_ids[product_names.index(selected_product)]
                place_reorder(cursor, db, pid, reorder_qty)
                st.success("Reorder placed successfully")
            except Exception as e:
                st.error(f"Error: {e}")

    # ---------------- RECEIVE REORDER ----------------
    if task == "Receive Reorder":
        st.markdown("### Receive Reorder")

        pending = get_pending_reorders(cursor)

        if not pending:
            st.info("No pending reorders.")
        else:
            reorder_labels = [
                f"ID {r['reorder_id']} - {r['product_name']}"
                for r in pending
            ]
            reorder_ids = [r["reorder_id"] for r in pending]

            selected = st.selectbox("Select Reorder", reorder_labels)

            if st.button("Mark as Received"):
                try:
                    rid = reorder_ids[reorder_labels.index(selected)]
                    mark_reorder_as_received(cursor, db, rid)
                    st.success("Reorder received and stock updated")
                except Exception as e:
                    st.error(f"Error: {e}")

