import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Πεσματζού Business Plan", layout="wide", page_icon="📊")

st.title("📊 Πεσματζού Business Plan (36 Months)")

# --- Sidebar ---
st.sidebar.header("⚙️ Βασικές παράμετροι")
dev_cost = st.sidebar.number_input("Κόστος κατασκευής (€)", value=2800)
price_per_customer = st.sidebar.number_input("Τιμή ανά πελάτη (€)", value=28.15)
monthly_fixed_cost = st.sidebar.number_input("Σταθερά κόστη (€)", value=50)
marketing_expense = st.sidebar.number_input("Marketing (€)", value=100)

# --- Growth ---
st.subheader("Ανάπτυξη Πελατών")
col1, col2 = st.columns(2)
with col1:
    start_customers = st.number_input("Πελάτες Μήνα 1", value=2)
with col2:
    growth_per_month = st.number_input("Αύξηση ανά μήνα", value=1)

manual_mode = st.checkbox("Χειροκίνητη εισαγωγή πελατών")

if manual_mode:
    manual_df = pd.DataFrame({
        "Month": list(range(1, 37)),
        "Customers": [start_customers + i * growth_per_month for i in range(36)]
    })
    edited_df = st.data_editor(manual_df, num_rows="fixed", use_container_width=True)
    customers_data = edited_df["Customers"].tolist()
else:
    customers_data = [start_customers + i * growth_per_month for i in range(36)]

# --- Tabs ---
tab1, tab2 = st.tabs(["Scenario 1 (50-50 Deal)", "Scenario 2 (Tiered Cost)"])

# =========================
# ✅ SCENARIO 1
# =========================
with tab1:
    rows = []
    cumulative = -dev_cost

    for i, customers in enumerate(customers_data):
        month = i + 1

        revenue = customers * price_per_customer
        total_costs = monthly_fixed_cost + marketing_expense
        net_profit = revenue - total_costs

        your_profit = net_profit * 0.5
        yearly_cost = 600 if month % 12 == 0 else 0
        your_profit -= yearly_cost

        cumulative += your_profit

        rows.append({
            "Month": month,
            "Customers": customers,
            "Your Profit": round(your_profit, 2),
            "Cumulative Profit": round(cumulative, 2),
        })

    df1 = pd.DataFrame(rows)

    st.subheader("Scenario 1 Results")
    st.line_chart(df1.set_index("Month")["Cumulative Profit"])
    st.dataframe(df1)

# =========================
# ✅ SCENARIO 2 (NEW)
# =========================
with tab2:

    # Cost mapping based on your table
    def get_cost(customers):
        if customers <= 3:
            return 50
        elif customers <= 10:
            return 100
        elif customers <= 25:
            return 180
        elif customers <= 50:
            return 260
        else:
            return 450

    rows = []
    cumulative = -dev_cost

    for i, customers in enumerate(customers_data):
        month = i + 1

        revenue = customers * price_per_customer
        dynamic_cost = get_cost(customers)

        net_profit = revenue - dynamic_cost
        cumulative += net_profit

        rows.append({
            "Month": month,
            "Customers": customers,
            "Revenue": round(revenue, 2),
            "Cost": dynamic_cost,
            "Net Profit": round(net_profit, 2),
            "Cumulative Profit": round(cumulative, 2),
        })

    df2 = pd.DataFrame(rows)

    st.subheader("Scenario 2 Results")

    colA, colB = st.columns(2)

    with colA:
        fig1, ax1 = plt.subplots()
        ax1.bar(df2["Month"], df2["Net Profit"])
        ax1.set_title("Net Profit per Month")
        st.pyplot(fig1)

    with colB:
        fig2, ax2 = plt.subplots()
        ax2.plot(df2["Month"], df2["Cumulative Profit"])
        ax2.axhline(0, linestyle="--")
        ax2.set_title("Cumulative Profit")
        st.pyplot(fig2)

    st.dataframe(df2)
