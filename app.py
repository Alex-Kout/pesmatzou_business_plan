import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Πεσματζού Business Plan", layout="wide", page_icon="📊")

# --- Custom CSS ---
st.markdown("""
<style>
    .metric-card { 
        background: #1e293b; 
        border-radius: 12px; 
        padding: 20px; 
        color: white; 
        border: 1px solid #334155; 
    }
    .value { 
        font-size: 24px; 
        font-weight: 700; 
    }

    /* Center align numbers inside data_editor */
    div[data-testid="stDataEditor"] div[role="gridcell"] {
        justify-content: center !important;
        text-align: center !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 Πεσματζού Business Plan (36 Months)")

# --- Sidebar ---
st.sidebar.header("⚙️ Συμπλήρωσε τις βασικές παραμέτρους")
dev_cost = st.sidebar.number_input("Κόστος κατασκευής του app (€)", value=2800, step=100)
price_per_customer = st.sidebar.number_input("Μηνιαία τιμή ανά πελάτη (€)", value=28.15, step=0.5)
monthly_fixed_cost = st.sidebar.number_input("Μηνιαία σταθερά κόστη (€)", value=50, step=10)
marketing_expense = st.sidebar.number_input("Μηνιαία έξοδα Marketing (€)", value=100, step=10)

# --- Growth ---
st.subheader("Ρύθμιση Ανάπτυξης Πελατών")
col1, col2 = st.columns(2)
with col1:
    start_customers = st.number_input("Πελάτες Μήνα 1", min_value=0, value=2)
with col2:
    growth_per_month = st.number_input("Μηνιαία Αύξηση Πελατών", min_value=0, value=1)

# --- Manual Override ---
manual_mode = st.checkbox("Θέλω να ορίσω χειροκίνητα πελάτες ανά μήνα")

if manual_mode:
    st.subheader("Χειροκίνητη εισαγωγή πελατών ανά μήνα")
    manual_df = pd.DataFrame({
        "Month": list(range(1, 37)),
        "Customers": [start_customers + i * growth_per_month for i in range(36)]
    })
    edited_df = st.data_editor(manual_df, num_rows="fixed", use_container_width=True)
    customers_data = edited_df["Customers"].tolist()
else:
    customers_data = [start_customers + (i * growth_per_month) for i in range(36)]

# --- Logic για Tiered Cost (Σενάριο 2) ---
def get_tiered_cost(customers):
    if customers <= 3: return 50
    elif customers <= 10: return 100
    elif customers <= 25: return 180
    elif customers <= 50: return 260
    else: return 450

# --- Δημιουργία Tabs ---
tab1, tab2 = st.tabs(["Σενάριο 1 (50/50 Split)", "Σενάριο 2 (Tiered Costs)"])

with tab1:
    # --- Calculations ---
    rows = []
    cumulative = -dev_cost  # YOU pay full dev upfront

    for i, customers in enumerate(customers_data):
        month = i + 1

        revenue = customers * price_per_customer
        total_costs = monthly_fixed_cost + marketing_expense

        net_profit = revenue - total_costs

        # 50-50 split
        your_profit = net_profit * 0.5
        developer_profit = net_profit * 0.5

        # yearly extra cost from YOUR side
        yearly_cost = 600 if month % 12 == 0 else 0
        your_profit_after_cost = your_profit - yearly_cost

        cumulative += your_profit_after_cost

        rows.append({
            "Month": month,
            "Customers": customers,
            "Revenue": round(revenue, 2),
            "Total Costs": round(total_costs, 2),
            "Net Profit": round(net_profit, 2),
            "Your Profit": round(your_profit_after_cost, 2),
            "Dev Profit": round(developer_profit, 2),
            "Extra Yearly Cost": yearly_cost,
            "Cumulative Profit": round(cumulative, 2),
        })

    df = pd.DataFrame(rows)

    # --- KPIs ---
    total_net = df["Your Profit"].sum() - dev_cost
    break_even_month = next((r["Month"] for r in rows if r["Cumulative Profit"] >= 0), None)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="metric-card">Your Net Profit (36mo): <div class="value">€ {total_net:,.2f}</div></div>',
                    unsafe_allow_html=True)
    with c2:
        bep = f"Month {break_even_month}" if break_even_month else "Not reached"
        st.markdown(f'<div class="metric-card">Break-even Month: <div class="value">{bep}</div></div>',
                    unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Charts ---
    col_a, col_b = st.columns(2)
    with col_a:
        fig1, ax1 = plt.subplots()
        ax1.bar(df["Month"], df["Your Profit"])
        ax1.set_xlabel("Μήνες")
        ax1.set_ylabel("Δικό σου κέρδος")
        ax1.set_title("Μηνιαίο κέρδος (μετά split & κόστη)")
        st.pyplot(fig1)

    with col_b:
        fig2, ax2 = plt.subplots()
        ax2.plot(df["Month"], df["Cumulative Profit"], linewidth=2)
        ax2.axhline(0, linestyle="--")
        ax2.set_xlabel("Μήνες")
        ax2.set_ylabel("Συσσωρευμένο κέρδος")
        ax2.set_title("Συσσωρευμένο δικό σου κέρδος")
        st.pyplot(fig2)

    # --- Table ---
    with st.expander("Δείτε αναλυτικά τα δεδομένα"):
        st.dataframe(df, use_container_width=True)

with tab2:
    # --- Calculations Σενάριο 2 ---
    rows_s2 = []
    cumulative_s2 = -dev_cost
    
    for i, customers in enumerate(customers_data):
        month = i + 1
        revenue = customers * price_per_customer
        
        # Tiered cost calculation
        tier_cost = get_tiered_cost(customers)
        
        # Scenario 2: No split, just revenue - tier_cost
        net_profit_s2 = revenue - tier_cost
        cumulative_s2 += net_profit_s2
        
        rows_s2.append({
            "Month": month,
            "Customers": customers,
            "Revenue": round(revenue, 2),
            "Tiered Monthly Cost": tier_cost,
            "Net Profit": round(net_profit_s2, 2),
            "Cumulative Profit": round(cumulative_s2, 2),
        })
    
    df_s2 = pd.DataFrame(rows_s2)
    
    # --- KPIs S2 ---
    total_net_s2 = df_s2["Net Profit"].sum() - dev_cost
    bep_s2 = next((r["Month"] for r in rows_s2 if r["Cumulative Profit"] >= 0), None)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="metric-card">Net Profit S2 (36mo): <div class="value">€ {total_net_s2:,.2f}</div></div>',
                    unsafe_allow_html=True)
    with c2:
        bep_txt = f"Month {bep_s2}" if bep_s2 else "Not reached"
        st.markdown(f'<div class="metric-card">Break-even Month: <div class="value">{bep_txt}</div></div>',
                    unsafe_allow_html=True)
    
    # --- Charts S2 ---
    col_a, col_b = st.columns(2)
    with col_a:
        fig1, ax1 = plt.subplots()
        ax1.bar(df_s2["Month"], df_s2["Net Profit"], color="orange")
        ax1.set_xlabel("Μήνες")
        ax1.set_ylabel("Κέρδος")
        ax1.set_title("Μηνιαίο κέρδος (Tiered)")
        st.pyplot(fig1)

    with col_b:
        fig2, ax2 = plt.subplots()
        ax2.plot(df_s2["Month"], df_s2["Cumulative Profit"], color="orange", linewidth=2)
        ax2.axhline(0, linestyle="--")
        ax2.set_xlabel("Μήνες")
        ax2.set_ylabel("Συσσωρευμένο κέρδος")
        ax2.set_title("Συσσωρευμένο κέρδος (Tiered)")
        st.pyplot(fig2)

    with st.expander("Δείτε αναλυτικά τα δεδομένα"):
        st.dataframe(df_s2, use_container_width=True)
