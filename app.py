import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Πεσματζού Business Plan", layout="wide", page_icon="📊")

# --- Custom CSS ---
st.markdown("""
<style>
    .metric-card { background: #1e293b; border-radius: 12px; padding: 20px; color: white; border: 1px solid #334155; }
    .value { font-size: 24px; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

st.title("📊 Πεσματζού Business Plan (36 Months)")

# --- Sidebar ---
st.sidebar.header("⚙️ Βασικές παράμετροι")
dev_cost = st.sidebar.number_input("Κόστος κατασκευής του app (€)", value=2800, step=100)
price_per_customer = st.sidebar.number_input("Μηνιαία τιμή ανά πελάτη (€)", value=28.15, step=0.5)

st.sidebar.divider()
st.sidebar.header("📈 Ρύθμιση Ανάπτυξης")
start_customers = st.sidebar.number_input("Πελάτες Μήνα 1", min_value=0, value=2)
growth_per_month = st.sidebar.number_input("Μηνιαία Αύξηση Πελατών", min_value=0, value=1)
monthly_fixed_cost = st.sidebar.number_input("Μηνιαία σταθερά κόστη (Σενάριο 1)", value=50, step=10)
marketing_expense = st.sidebar.number_input("Marketing Expense (Σενάριο 1)", value=100, step=10)

# --- Logic για Tiered Cost (Σενάριο 2) ---
def get_tiered_cost(customers):
    if customers <= 3: return 50
    elif 4 <= customers <= 10: return 100
    elif 11 <= customers <= 25: return 180
    elif 26 <= customers <= 50: return 260
    else: return 450

# --- Υπολογισμός Πελατών ---
customers_data = [start_customers + (i * growth_per_month) for i in range(36)]

# --- Tabs ---
tab1, tab2 = st.tabs(["Σενάριο 1: 50/50 Split", "Σενάριο 2: Tiered Costs"])

# --- Υπολογισμοί Σενάριο 1 ---
rows_s1 = []
cumulative_s1 = -dev_cost
for i, customers in enumerate(customers_data):
    month = i + 1
    revenue = customers * price_per_customer
    total_costs = monthly_fixed_cost + marketing_expense
    net_profit = revenue - total_costs
    your_profit = (net_profit * 0.5) - (600 if month % 12 == 0 else 0)
    cumulative_s1 += your_profit
    rows_s1.append({"Month": month, "Customers": customers, "Revenue": revenue, "Your Profit": round(your_profit, 2), "Cumulative Profit": round(cumulative_s1, 2)})

# --- Υπολογισμοί Σενάριο 2 ---
rows_s2 = []
cumulative_s2 = -dev_cost
for i, customers in enumerate(customers_data):
    month = i + 1
    revenue = customers * price_per_customer
    tiered_cost = get_tiered_cost(customers)
    net_profit_s2 = revenue - tiered_cost
    cumulative_s2 += net_profit_s2
    rows_s2.append({"Month": month, "Customers": customers, "Revenue": revenue, "Net Profit": round(net_profit_s2, 2), "Cumulative Profit": round(cumulative_s2, 2)})

# --- Εμφάνιση Tabs ---
with tab1:
    st.subheader("Σενάριο 1: 50/50 Split & 600€ Ετήσιο Κόστος")
    df_s1 = pd.DataFrame(rows_s1)
    st.dataframe(df_s1, use_container_width=True)
    fig1, ax1 = plt.subplots()
    ax1.plot(df_s1["Month"], df_s1["Cumulative Profit"], color="#34d399")
    st.pyplot(fig1)

with tab2:
    st.subheader("Σενάριο 2: Tiered Cost & Full Profit")
    df_s2 = pd.DataFrame(rows_s2)
    st.dataframe(df_s2, use_container_width=True)
    fig2, ax2 = plt.subplots()
    ax2.plot(df_s2["Month"], df_s2["Cumulative Profit"], color="#f59e0b")
    st.pyplot(fig2)
