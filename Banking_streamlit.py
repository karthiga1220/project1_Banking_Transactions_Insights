from datetime import datetime
import streamlit as st
import pandas as pd
import pymysql


# Reading csv files
customers_df = pd.read_csv(r'C:\Users\Dr.D Ravindran\Downloads\customers.csv')
accounts_df = pd.read_csv(r'C:\Users\Dr.D Ravindran\Downloads\accounts.csv')
transactions_df = pd.read_csv(r'C:\Users\Dr.D Ravindran\Downloads\transactions.csv')
loans_df = pd.read_csv(r'C:\Users\Dr.D Ravindran\Downloads\loans.csv')
branches_df = pd.read_csv(r'C:\Users\Dr.D Ravindran\Downloads\branches.csv')
support_tickets_df = pd.read_csv(r'C:\Users\Dr.D Ravindran\Downloads\support_tickets.csv')

#Fixing null values
support_tickets_df['Loan_ID'] = support_tickets_df['Loan_ID'].fillna('0')
support_tickets_df['Date_Closed'] = pd.to_datetime(support_tickets_df['Date_Closed'], errors='coerce')
support_tickets_df['Date_Closed'] = support_tickets_df['Date_Closed'].fillna(support_tickets_df['Date_Closed'].max())


#Python sql connection
@st.cache_resource
def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="customers_db"
    )

conn_pymysql = get_connection()
cursor_pymysql = conn_pymysql.cursor()


#Creating database customers_db
cursor_pymysql.execute("CREATE DATABASE IF NOT EXISTS customers_db;")
print("MySQL database 'customers_db' created successfully!")


#Creating 6 tables with columns
cursor_pymysql.execute("USE customers_db;") 
cursor_pymysql.execute("""
    CREATE TABLE IF NOT EXISTS customers_data (
        customer_id VARCHAR(5),
        name VARCHAR(50),
        gender VARCHAR(1),
        age INT,
        city VARCHAR(50),
        account_type VARCHAR(50),
        join_date Date
    );
""")
conn_pymysql.commit()
print("Table 'customers_data' created successfully in MySQL!")


cursor_pymysql.execute("USE customers_db;")  
cursor_pymysql.execute("""
    CREATE TABLE IF NOT EXISTS accounts_data (
        customer_id VARCHAR(5),
        account_balance VARCHAR(50),
        last_updated DATETIME
    );
""")
conn_pymysql.commit()
print("Table 'accounts_data' created successfully in MySQL!")


cursor_pymysql.execute("USE customers_db;") 
cursor_pymysql.execute("""
    CREATE TABLE IF NOT EXISTS transactions_data (
        txn_id VARCHAR(6),
        customer_id VARCHAR(5),
        txn_type VARCHAR(50),
        amount FLOAT,
        txn_time DATETIME,
        status VARCHAR(50)
    );
""")
conn_pymysql.commit()
print("Table 'transactions_data' created successfully in MySQL!")



cursor_pymysql.execute("USE customers_db;")  
cursor_pymysql.execute("""
    CREATE TABLE IF NOT EXISTS loan_amount_data (
        Loan_ID INT,
        Customer_ID VARCHAR(4),
        Account_ID  VARCHAR(4),
        Branch VARCHAR(100),
        Loan_Type VARCHAR(50),
        Loan_Amount INT,
        Interest_Rate FLOAT,
        Loan_Term_Months INT,
        Start_Date DATE,
        End_Date DATE,
        Loan_Status VARCHAR(50)
    );
""")
conn_pymysql.commit()
print("Table 'loan_amount_data' created successfully in MySQL!")


cursor_pymysql.execute("USE customers_db;")  
cursor_pymysql.execute("""
    CREATE TABLE IF NOT EXISTS branches_data (
        Branch_ID INT,
        Branch_Name VARCHAR(100),
        City  VARCHAR(50),
        Manager_Name VARCHAR(100),
        Total_Employees INT,
        Branch_Revenue FLOAT,
        Opening_Date DATE,
        Performance_Rating INT
    );
""")
conn_pymysql.commit()
print("Table 'branches_data' created successfully in MySQL!")

cursor_pymysql.execute("USE customers_db;")  
cursor_pymysql.execute("""
    CREATE TABLE IF NOT EXISTS support_tickets_data (
        Ticket_ID VARCHAR(50),
        Customer_ID VARCHAR(50),
        Account_ID  VARCHAR(50),
        Loan_ID VARCHAR(50),
        Branch_Name VARCHAR(100),
        Issue_Category VARCHAR(100),
        Description VARCHAR(200),
        Date_Opened DATE,
        Date_Closed DATE,
        Priority VARCHAR(100),
        Status VARCHAR(50),
        Resolution_Remarks VARCHAR(200),
        Support_Agent VARCHAR(100),
        Channel VARCHAR(50),
        Customer_Rating INT    
                       
    );
""")
conn_pymysql.commit()
print("Table 'support_tickets_data' created successfully in MySQL!")


#Inserting values to tables

data_list1 = customers_df[['customer_id','name','gender','age','city','account_type','join_date']].values.tolist()

query = """
INSERT IGNORE INTO customers_data
(customer_id, name, gender, age, city, account_type, join_date)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

cursor_pymysql.executemany(query, data_list1)
conn_pymysql.commit()


print("✅ Insert  to customers_data table completed successfully")




data_list2 = accounts_df[['customer_id','account_balance','last_updated']].values.tolist()

query = """
INSERT IGNORE INTO accounts_data
(customer_id, account_balance, last_updated)
VALUES (%s, %s, %s)
"""

cursor_pymysql.executemany(query, data_list2)
conn_pymysql.commit()


print("✅ Insert to accounts_data table completed successfully")



data_list3 = transactions_df[['txn_id','customer_id','txn_type','amount','txn_time','status']].values.tolist()

query = """
INSERT IGNORE INTO transactions_data
(txn_id, customer_id, txn_type, amount, txn_time, status)
VALUES (%s, %s, %s, %s, %s, %s)
"""

cursor_pymysql.executemany(query, data_list3)
conn_pymysql.commit()

print("✅ Insert to transactions_data table completed successfully")




data_list4 = loans_df[['Loan_ID','Customer_ID','Account_ID','Branch','Loan_Type','Loan_Amount',
                  'Interest_Rate','Loan_Term_Months','Start_Date','End_Date','Loan_Status']].values.tolist()

query = """
INSERT IGNORE INTO loan_amount_data
(Loan_ID, Customer_ID, Account_ID, Branch, Loan_Type, Loan_Amount,
 Interest_Rate, Loan_Term_Months, Start_Date, End_Date, Loan_Status)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

cursor_pymysql.executemany(query, data_list4)
conn_pymysql.commit()

print("✅ Insert to loan_amount_data table completed successfully")



data_list5 = branches_df[['Branch_ID','Branch_Name','City','Manager_Name','Total_Employees','Branch_Revenue',
                  'Opening_Date','Performance_Rating']].values.tolist()

query = """
INSERT IGNORE INTO branches_data
(Branch_ID, Branch_Name, City, Manager_Name, Total_Employees, Branch_Revenue,
 Opening_Date, Performance_Rating)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

cursor_pymysql.executemany(query, data_list5)
conn_pymysql.commit()

print("✅ Insert to branches_data table completed successfully")



data_list6 = support_tickets_df[['Ticket_ID','Customer_ID','Account_ID','Loan_ID','Branch_Name','Issue_Category',
                  'Description','Date_Opened','Date_Closed','Priority','Status','Resolution_Remarks','Support_Agent','Channel','Customer_Rating']].values.tolist()

query = """
INSERT IGNORE INTO support_tickets_data
(Ticket_ID,Customer_ID,Account_ID,Loan_ID,Branch_Name,Issue_Category,
 Description,Date_Opened,Date_Closed,Priority,Status,Resolution_Remarks,Support_Agent,Channel,Customer_Rating)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
"""

cursor_pymysql.executemany(query, data_list6)
conn_pymysql.commit()


print("✅ Insert to support_tickets_data completed successfully")


# ---------- HELPERS ----------

@st.cache_data(ttl=300)
def run_query(query):
    """Run SQL query and return DataFrame.

    If the cached connection is closed or fails, try a fresh connection.
    """
    try:
        return pd.read_sql(query, conn_pymysql)
    except Exception:
        # fallback: create a new short-lived connection and retry
        tmp_conn = pymysql.connect(
            host="localhost",
            user="root",
            password="root",
            database="customers_db"
        )
        try:
            df = pd.read_sql(query, tmp_conn)
            return df
        finally:
            tmp_conn.close()

@st.cache_data(ttl=300)
def get_columns_with_types(table):
    df = pd.read_sql(f"DESCRIBE {table};", conn_pymysql)
    return dict(zip(df["Field"], df["Type"]))

@st.cache_data(ttl=300)
def get_distinct_values(table, column):
    df = pd.read_sql(f"SELECT DISTINCT {column} FROM {table} WHERE {column} IS NOT NULL ORDER BY {column};", conn_pymysql)
    return df[column].astype(str).tolist()

def cast_value(value, sql_type):
    sql_type = sql_type.lower()
    if "int" in sql_type:
        return int(value)
    if "float" in sql_type or "double" in sql_type or "decimal" in sql_type:
        return float(value)
    return value   # varchar, date, datetime

def cast_value1(value, sql_type):
    sql_type = sql_type.lower()
    if value == "" or value is None:
        return None
    if "int" in sql_type:
        return int(value)
    if "float" in sql_type or "double" in sql_type or "decimal" in sql_type:
        return float(value)
    return value   # varchar, date, datetime




# ----------------------------
# Page configuration
# ----------------------------
st.set_page_config(
    page_title="Banking Transaction Insights",
    layout="wide"
)

# ----------------------------
# Sidebar (Left Navigation)
# ----------------------------
st.sidebar.title("📊 Navigation")
menu = st.sidebar.radio(
    "Go to",
    ["Introduction", "View Tables", "Analytics","Filter operations", "CRUD Operations","Credit/Debit simulation", "Creator"]
)

# ----------------------------
# Main Title (Right Side)
# ----------------------------
if menu == "Introduction":
 st.title("🏦 Banking Transaction Insights")

 st.markdown("---")
 st.subheader("📌 Project Overview")
 st.markdown("""
 Banks process millions of transactions daily.  
 **Banking Transaction Insights** helps analyze customer behavior, transaction trends,
 and detect potential fraud through an interactive Streamlit dashboard.
 """)

 st.subheader("🎯 Project Objectives")
 st.markdown("""
 - Analyze customer demographics and transactions  
 - Identify trends across accounts and branches  
 - Detect high-risk or anomalous transactions  
 - Evaluate branch and account performance  
 - Enable interactive exploration with CRUD operations  
 """)
elif menu == "View Tables":
    st.subheader("📂 View Tables")

    table = st.selectbox(
        "Select a table to view",
        ["Customers", "Accounts", "Transactions", "Loans", "Support Tickets"]
    )

    if table == "Customers":
        st.dataframe(customers_df)

    elif table == "Accounts":
        st.dataframe(accounts_df)

    elif table == "Transactions":
        st.dataframe(transactions_df)

    elif table == "Loans":
        st.dataframe(loans_df)
    
    elif table == "Branches":
        st.dataframe(branches_df)

    elif table == "Support Tickets":
        st.dataframe(support_tickets_df)

elif menu == "Filter operations":
     
    tables = {
    "Customers Data": "customers_data",
    "Accounts Data": "accounts_data",
    "Transactions Data": "transactions_data",
    "Loans Data": "loan_amount_data",
    "Branches Data": "branches_data"
    }

    
    st.title("🎛️ Multi-Table Filter Dashboard")

    selected_table_label = st.selectbox("Select Table", list(tables.keys()))
    selected_table = tables[selected_table_label]

    columns_with_types = get_columns_with_types(selected_table)

    st.subheader("Filter Conditions")

    filters = {}

    for col, col_type in columns_with_types.items():
        values = get_distinct_values(selected_table, col)

        if not values:
            continue

        display_values = ["All"] + [str(v) for v in values]
        selected_display = st.selectbox(col, display_values)

        if selected_display == "All":
            filters[col] = "All"
        else:
            filters[col] = cast_value(selected_display, col_type)

# ------------------ APPLY FILTER ------------------
    if st.button("Apply Filter"):
        conditions = []
        params = []

        for col, val in filters.items():
            if val != "All":
                conditions.append(f"{col} = %s")
                params.append(val)

        query = f"SELECT DISTINCT * FROM {selected_table}"

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        df = pd.read_sql(query, conn_pymysql, params=params)

        if df.empty:
            st.info("No matching records found")
        else:
            st.success(f"{len(df)} record(s) found")
            st.dataframe(df, use_container_width=True)
elif menu == "Analytics":

    st.subheader("📊 Analytics Dashboard")

    question_dict = {
    "Q1: Customers per city & average account balance": """
        SELECT 
            c.city AS City,
            COUNT(DISTINCT c.customer_id) AS `Total Customers`,
            AVG(a.account_balance) AS `Average Account Balance`
        FROM customers_data c
        JOIN accounts_data a
            ON c.customer_id = a.customer_id
        GROUP BY c.city;
    """,
    "Q2:Which account type (Savings, Current, Loan, etc.) holds the highest total balance?":"""
       SELECT 
           c.account_type,
           SUM(a.account_balance) AS total_balance
        FROM customers_data c
        JOIN accounts_data a
             ON c.customer_id = a.customer_id
        GROUP BY c.account_type
        ORDER BY total_balance DESC
        LIMIT 1;
        """,
    "Q3:Who are the top 10 customers by total account balance across all account types?":"""
    SELECT 
        c.customer_id,
        c.name,
    SUM(a.account_balance) AS total_balance
    FROM customers_data c
    JOIN accounts_data a
        ON c.customer_id = a.customer_id
    GROUP BY c.customer_id, c.name
    ORDER BY total_balance DESC
    LIMIT 10;
    """,
    "Q4:Which customers opened accounts in 2023 with a balance above ₹1,00,000?":"""
    SELECT 
        c.customer_id,
        c.name,
        c.join_date,
    SUM(a.account_balance) AS total_balance
    FROM customers_data c
    JOIN accounts_data a
    ON c.customer_id = a.customer_id
    WHERE YEAR(c.join_date) = 2023
    GROUP BY c.customer_id, c.name, c.join_date
    HAVING SUM(a.account_balance) > 100000
    ORDER BY total_balance DESC;
    """,
    "Q5: What is the total transaction volume (sum of amounts) by transaction type?":"""
    SELECT
        txn_type,
        SUM(amount) AS total_transaction_volume
    FROM transactions_data
    GROUP BY txn_type
    ORDER BY total_transaction_volume DESC;
    """,
    "Q6:How many failed transactions occurred for each transaction type?":"""
    SELECT
        txn_type,
        COUNT(*) AS failed_transaction_count
    FROM transactions_data
    WHERE status = 'failed'
    GROUP BY txn_type
    ORDER BY failed_transaction_count DESC;
    """,
    "Q7:What is the total number of transactions per transaction type?":"""
    SELECT
        txn_type,
        COUNT(*) AS total_transactions
    FROM transactions_data
    GROUP BY txn_type
    ORDER BY total_transactions DESC;
    """,
    "Q8:Which accounts have 5 or more high-value transactions above ₹20,000?":"""
    SELECT
        txn_id,
        COUNT(*) AS high_value_transaction_count
    FROM transactions_data
    WHERE amount > 20000
    GROUP BY txn_id
    HAVING COUNT(*) >= 5
    ORDER BY high_value_transaction_count DESC;
    """,
    "Q9: What is the average loan amount and interest rate by loan type (Personal, Auto, Home, etc.)?":"""
    SELECT
        Loan_Type,
        AVG(Loan_Amount) AS Avg_Loan_Amount,
        AVG(Interest_Rate) AS Avg_Interest_Rate
    FROM loan_amount_data
    GROUP BY Loan_Type
    ORDER BY Avg_Loan_Amount DESC;
    """,
    "Q10:Which customers currently hold more than one active or approved loan?":"""
    SELECT
        customer_id,
        COUNT(loan_id) AS active_approved_loans
    FROM loan_amount_data
    WHERE LOWER(loan_status) IN ('active', 'approved')
    GROUP BY customer_id
    HAVING COUNT(loan_id) > 1
    ORDER BY active_approved_loans DESC;
    """,
    "Q11:Who are the top 5 customers with the highest outstanding (non-closed) loan amounts?":"""
    SELECT
        customer_id,
        SUM(loan_amount) AS outstanding_loan_amount
    FROM loan_amount_data
    WHERE LOWER(loan_status) IN ('active', 'approved')
    GROUP BY customer_id
    ORDER BY outstanding_loan_amount DESC
    LIMIT 5;
    """,
    "Q12:What is the average loan amount per branch?":"""
    SELECT
        Branch,
        AVG(loan_amount) AS Avg_loan_amount
    FROM loan_amount_data
    GROUP BY Branch
    ORDER BY Avg_loan_amount DESC;
    """,
    "Q13:How many customers exist in each age group (e.g., 18–25, 26–35, etc.)?":"""
    SELECT
        CASE
            WHEN age BETWEEN 18 AND 25 THEN '18–25'
            WHEN age BETWEEN 26 AND 35 THEN '26–35'
            WHEN age BETWEEN 36 AND 45 THEN '36–45'
            WHEN age BETWEEN 46 AND 55 THEN '46–55'
            WHEN age BETWEEN 56 AND 65 THEN '56–65'
            ELSE '66+'
            END AS age_group,
        COUNT(*) AS customer_count
        FROM customers_data
    GROUP BY age_group
    ORDER BY
        CASE age_group
            WHEN '18–25' THEN 1
            WHEN '26–35' THEN 2
            WHEN '36–45' THEN 3
            WHEN '46–55' THEN 4
            WHEN '56–65' THEN 5
            ELSE 6
        END;
    """,
    "Q14:Which issue categories have the longest average resolution time?":"""
    SELECT 
        Issue_Category,
        AVG(DATEDIFF(Date_Closed, Date_Opened)) AS avg_resolution_days
    FROM support_tickets_data
    WHERE Date_Closed IS NOT NULL
    GROUP BY Issue_Category
    ORDER BY avg_resolution_days DESC;
    """,
    "Q15:Which support agents have resolved the most critical tickets with high customer ratings (≥4)?":"""
    SELECT
        Support_Agent,
        COUNT(*) AS critical_high_rating_tickets
    FROM support_tickets_data
    WHERE Priority = 'Critical'
     AND Status = 'Closed'
     AND Customer_Rating >= 4
    GROUP BY Support_Agent
    ORDER BY critical_high_rating_tickets DESC;
    """
     }
    
# -------------------------------
# Question Selector
# -------------------------------
    selected_question = st.selectbox(
        "📌 Select a Question",
        list(question_dict.keys()),
        key="analytics_question"
    )
    # -------------------------------
# Run Query Button
# -------------------------------
    if st.button("▶ Run Query", key="run_analytics_button"):
        with st.spinner("⏳ Running query..."):
            df = run_query(question_dict[selected_question])
        st.dataframe(df, use_container_width=True)

        col1, col2 = st.columns([1, 5])
        with col1:
            st.download_button(
                "⬇ Download CSV",
                df.to_csv(index=False).encode("utf-8"),
                "query_result.csv",
                "text/csv"
            )

elif menu == 'CRUD Operations':
    st.header("🧾 CRUD Dashboard")
    tables = {
    "Customers Data": "customers_data",
    "Transactions Data": "transactions_data",
    "Loans Data": "loan_amount_data",
    "Branches Data": "branches_data"
    }

# ---------------- SELECT OPERATION ----------------
    crud_action = st.selectbox(
        "Select Operation",
        ["Create", "Read", "Update", "Delete"]
    )

    # ---------------- SELECT TABLE ----------------
    selected_table_label = st.selectbox(
        "Select Table",
        list(tables.keys())
    )
    table = tables[selected_table_label]

    # ---------------- GET COLUMNS (DICT) ----------------
    columns_dict = get_columns_with_types(table)



    # =========================
    # CREATE
    # =========================
    if crud_action == "Create":
        st.subheader("➕ Insert Record")

        input_values = {}
        for field, sql_type in columns_dict.items():
            input_values[field] = st.text_input(field)

        if st.button("Insert"):
            cols, params, placeholders = [], [], []

            for field, sql_type in columns_dict.items():
                val = input_values[field]
                if val != "":
                    cols.append(field)
                    params.append(cast_value1(val, sql_type))
                    placeholders.append("%s")

            query = f"""
            INSERT INTO {table} ({", ".join(cols)})
            VALUES ({", ".join(placeholders)})
            """

            cursor_pymysql.execute(query, params)
            conn_pymysql.commit()
            st.success("✅ Record inserted successfully")

    # =========================
    # READ
    # =========================
    elif crud_action == "Read":
        st.subheader("📄 View Records")

        df = pd.read_sql(f"SELECT * FROM {table}", conn_pymysql)
        st.dataframe(df, use_container_width=True)

    # =========================
    # UPDATE
    # =========================
    elif crud_action == "Update":
        st.subheader("✏️ Update Record")

        key_col = list(columns_dict.keys())[0]

        key_values = pd.read_sql(
            f"SELECT DISTINCT {key_col} FROM {table}",
            conn_pymysql
        )[key_col].astype(str).tolist()

        selected_key = st.selectbox(f"Select {key_col}", key_values)

        row_df = pd.read_sql(
            f"SELECT * FROM {table} WHERE {key_col} = %s",
            conn_pymysql,
            params=[selected_key]
        )

        if not row_df.empty:
            updated_values = {}
            for field, sql_type in columns_dict.items():
                updated_values[field] = st.text_input(
                    field,
                    str(row_df.iloc[0][field])
                )

            if st.button("Update"):
                updates, params = [], []

                for field, sql_type in columns_dict.items():
                    updates.append(f"{field} = %s")
                    params.append(cast_value1(updated_values[field], sql_type))

                params.append(selected_key)

                query = f"""
                UPDATE {table}
                SET {", ".join(updates)}
                WHERE {key_col} = %s
                """

                cursor_pymysql.execute(query, params)
                conn_pymysql.commit()
                st.success("✅ Record updated successfully")

    # =========================
    # DELETE
    # =========================
    elif crud_action == "Delete":
        st.subheader("🗑️ Delete Record")

        key_col = list(columns_dict.keys())[0]

        key_values = pd.read_sql(
            f"SELECT DISTINCT {key_col} FROM {table}",
            conn_pymysql
        )[key_col].astype(str).tolist()

        selected_key = st.selectbox(
            f"Select {key_col} to delete",
            key_values
        )

        if st.button("Delete"):
            cursor_pymysql.execute(
                f"DELETE FROM {table} WHERE {key_col} = %s",
                (selected_key,)
            )
            conn_pymysql.commit()
            st.success("✅ Record deleted successfully")


elif menu == "Credit/Debit simulation":

    st.header("💳 Credit / Debit Simulation")

    customers = pd.read_sql(
        "SELECT DISTINCT customer_id FROM customers_data WHERE customer_id IS NOT NULL ORDER BY customer_id;",
        conn_pymysql
    )["customer_id"].astype(str).tolist()

    with st.form("credit_debit_form"):
        selected_customer = st.selectbox(
            "Customer ID",
            customers
        )

        txn_type = st.selectbox(
            "Transaction Type",
            ["Deposit", "Withdraw"]
        )

        amount = st.number_input(
            "Amount",
            min_value=0.0,
            step=100.0
        )

        submitted = st.form_submit_button("Submit")

    if submitted:
        balance_df = pd.read_sql(
            "SELECT account_balance FROM accounts_data WHERE customer_id = %s",
            conn_pymysql,
            params=[selected_customer]
        )

        current_balance = float(balance_df.iloc[0][0])

        if txn_type == "Withdraw" and amount > current_balance:
            st.error("❌ Insufficient balance")
        else:
            new_balance = (
                current_balance + amount
                if txn_type == "Deposit"
                else current_balance - amount
            )

            with conn_pymysql.cursor() as cursor:
                cursor_pymysql.execute(
                    """
                    UPDATE accounts_data
                    SET account_balance=%s, last_updated=%s
                    WHERE customer_id=%s
                    """,
                    (new_balance, datetime.now(), selected_customer)
                )
                conn_pymysql.commit()

            st.success(f"💰 Updated Balance: ₹ {new_balance:,.2f}")

elif menu == "Creator":

    st.header("👤 Creator")

    # Static creator display (no input)
    st.subheader("MuthuKarthiga Devi")
    st.write("**Role:** Frontend Developer")
