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
        margin-bottom: 16px;
    }
    .metric-label {
        font-size: 14px;
        color: #94a3b8;
        margin-bottom: 6px;
    }
    .value { 
        font-size: 28px; 
        font-weight: 700; 
    }
    div[data-testid="stDataEditor"] div[role="gridcell"] {
        justify-content: center !important;
        text-align: center !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 Πεσματζού Business Plan (36 Months)")

# ─────────────────────────────────────────────
# SIDEBAR — all parameters including customers
# ─────────────────────────────────────────────
st.sidebar.header("⚙️ Βασικές Παράμετροι")

dev_cost = st.sidebar.number_input("Κόστος κατασκευής του app (€)", value=2800, step=100)
price_per_customer = st.sidebar.number_input("Μηνιαία τιμή ανά πελάτη (€)", value=28.15, step=0.5)
monthly_fixed_cost = st.sidebar.number_input("Μηνιαία σταθερά κόστη (€)", value=50, step=10)
marketing_expense = st.sidebar.number_input("Μηνιαία έξοδα Marketing (€)", value=100, step=10)

st.sidebar.markdown("---")
st.sidebar.subheader("👥 Ανάπτυξη Πελατών")

start_customers = st.sidebar.number_input("Πελάτες Μήνα 1", min_value=0, value=2)
growth_per_month = st.sidebar.number_input("Μηνιαία Αύξηση Πελατών", min_value=0, value=1)

manual_mode = st.sidebar.checkbox("Χειροκίνητη εισαγωγή πελατών ανά μήνα")

if manual_mode:
    st.sidebar.markdown("*Επεξεργάσου τον παρακάτω πίνακα:*")
    manual_df = pd.DataFrame({
        "Month": list(range(1, 37)),
        "Customers": [start_customers + i * growth_per_month for i in range(36)]
    })
    edited_df = st.sidebar.data_editor(manual_df, num_rows="fixed", use_container_width=True, height=300)
    customers_data = edited_df["Customers"].tolist()
else:
    customers_data = [start_customers + i * growth_per_month for i in range(36)]

# ─────────────────────────────────────────────
# HELPER: Tiered monthly cost (Scenario 2)
# ─────────────────────────────────────────────
def get_tiered_cost(customers):
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

# ─────────────────────────────────────────────
# MAIN BODY — two scenario tabs
# ─────────────────────────────────────────────
tab1, tab2 = st.tabs(["📐 Σενάριο 1 — 50/50 Split με Developer", "📦 Σενάριο 2 — Tiered Monthly Cost"])

# ── SCENARIO 1 ─────────────────────────────
with tab1:
    st.markdown(
        "**Λογική:** Καθαρό κέρδος = Έσοδα − Σταθερά Κόστη − Marketing. "
        "Το μισό πηγαίνει στον developer, το άλλο μισό σε σένα. "
        "Κάθε 12 μήνες αφαιρείται επιπλέον €600 από το δικό σου μερίδιο."
    )

    rows = []
    cumulative = -dev_cost  # you pay full dev cost upfront

    for i, customers in enumerate(customers_data):
        month = i + 1
        revenue = customers * price_per_customer
        total_costs = monthly_fixed_cost + marketing_expense
        net_profit = revenue - total_costs

        your_profit = net_profit * 0.5
        developer_profit = net_profit * 0.5

        yearly_cost = 600 if month % 12 == 0 else 0
        your_profit_after_cost = your_profit - yearly_cost

        cumulative += your_profit_after_cost

        rows.append({
            "Month": month,
            "Customers": customers,
            "Revenue (€)": round(revenue, 2),
            "Total Costs (€)": round(total_costs, 2),
            "Net Profit (€)": round(net_profit, 2),
            "Your Profit (€)": round(your_profit_after_cost, 2),
            "Dev Profit (€)": round(developer_profit, 2),
            "Extra Yearly Cost (€)": yearly_cost,
            "Cumulative Profit (€)": round(cumulative, 2),
        })

    df = pd.DataFrame(rows)

    # KPIs
    break_even_month = next((r["Month"] for r in rows if r["Cumulative Profit (€)"] >= 0), None)
    total_your_profit = df["Your Profit (€)"].sum()

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">Συνολικό κέρδος σου (36 μήνες)</div>'
            f'<div class="value">€ {total_your_profit:,.2f}</div></div>',
            unsafe_allow_html=True
        )
    with c2:
        bep = f"Μήνας {break_even_month}" if break_even_month else "Δεν επιτυγχάνεται"
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">Break-even</div>'
            f'<div class="value">{bep}</div></div>',
            unsafe_allow_html=True
        )
    with c3:
        total_dev = df["Dev Profit (€)"].sum()
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">Συνολικό κέρδος Developer (36 μήνες)</div>'
            f'<div class="value">€ {total_dev:,.2f}</div></div>',
            unsafe_allow_html=True
        )

    # Charts
    col_a, col_b = st.columns(2)
    with col_a:
        fig1, ax1 = plt.subplots(figsize=(7, 4))
        colors = ["#ef4444" if v < 0 else "#3b82f6" for v in df["Your Profit (€)"]]
        ax1.bar(df["Month"], df["Your Profit (€)"], color=colors)
        ax1.set_xlabel("Μήνας", fontsize=11)
        ax1.set_ylabel("Κέρδος (€)", fontsize=11)
        ax1.set_title("Μηνιαίο κέρδος σου (μετά split & κόστη)", fontsize=12)
        ax1.axhline(0, color="black", linewidth=0.8, linestyle="--")
        fig1.tight_layout()
        st.pyplot(fig1)

    with col_b:
        fig2, ax2 = plt.subplots(figsize=(7, 4))
        ax2.plot(df["Month"], df["Cumulative Profit (€)"], linewidth=2.5, color="#3b82f6")
        ax2.axhline(0, linestyle="--", color="gray", linewidth=1)
        ax2.fill_between(df["Month"], df["Cumulative Profit (€)"], 0,
                         where=[v >= 0 for v in df["Cumulative Profit (€)"]],
                         alpha=0.15, color="#3b82f6", label="Κέρδος")
        ax2.fill_between(df["Month"], df["Cumulative Profit (€)"], 0,
                         where=[v < 0 for v in df["Cumulative Profit (€)"]],
                         alpha=0.15, color="#ef4444", label="Ζημιά")
        ax2.set_xlabel("Μήνας", fontsize=11)
        ax2.set_ylabel("Συσσωρευμένο κέρδος (€)", fontsize=11)
        ax2.set_title("Συσσωρευμένο κέρδος σου", fontsize=12)
        ax2.legend()
        fig2.tight_layout()
        st.pyplot(fig2)

    with st.expander("🔍 Αναλυτικά δεδομένα — Σενάριο 1"):
        st.dataframe(df, use_container_width=True)

# ── SCENARIO 2 ─────────────────────────────
with tab2:
    st.markdown(
        "**Λογική:** Δεν υπάρχει split. Το μηνιαίο κόστος κλιμακώνεται ανάλογα με τον αριθμό πελατών "
        "(tiered pricing). Κέρδος = Έσοδα − Tiered κόστος."
    )

    # Tiered cost legend
    with st.expander("📋 Tiered κόστος ανά αριθμό πελατών"):
        tier_info = pd.DataFrame({
            "Πελάτες": ["1–3", "4–10", "11–25", "26–50", "51+"],
            "Μηνιαίο Κόστος (€)": [50, 100, 180, 260, 450],
        })
        st.table(tier_info)

    rows_s2 = []
    cumulative_s2 = -dev_cost

    for i, customers in enumerate(customers_data):
        month = i + 1
        revenue = customers * price_per_customer
        tier_cost = get_tiered_cost(customers)
        net_profit_s2 = revenue - tier_cost
        cumulative_s2 += net_profit_s2

        rows_s2.append({
            "Month": month,
            "Customers": customers,
            "Revenue (€)": round(revenue, 2),
            "Tiered Cost (€)": tier_cost,
            "Net Profit (€)": round(net_profit_s2, 2),
            "Cumulative Profit (€)": round(cumulative_s2, 2),
        })

    df_s2 = pd.DataFrame(rows_s2)

    # KPIs
    total_net_s2 = df_s2["Net Profit (€)"].sum()
    bep_s2 = next((r["Month"] for r in rows_s2 if r["Cumulative Profit (€)"] >= 0), None)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">Συνολικό κέρδος (36 μήνες)</div>'
            f'<div class="value">€ {total_net_s2:,.2f}</div></div>',
            unsafe_allow_html=True
        )
    with c2:
        bep_txt = f"Μήνας {bep_s2}" if bep_s2 else "Δεν επιτυγχάνεται"
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">Break-even</div>'
            f'<div class="value">{bep_txt}</div></div>',
            unsafe_allow_html=True
        )

    # Charts
    col_a, col_b = st.columns(2)
    with col_a:
        fig3, ax3 = plt.subplots(figsize=(7, 4))
        colors_s2 = ["#ef4444" if v < 0 else "#f97316" for v in df_s2["Net Profit (€)"]]
        ax3.bar(df_s2["Month"], df_s2["Net Profit (€)"], color=colors_s2)
        ax3.axhline(0, color="black", linewidth=0.8, linestyle="--")
        ax3.set_xlabel("Μήνας", fontsize=11)
        ax3.set_ylabel("Κέρδος (€)", fontsize=11)
        ax3.set_title("Μηνιαίο κέρδος (Tiered κόστος)", fontsize=12)
        fig3.tight_layout()
        st.pyplot(fig3)

    with col_b:
        fig4, ax4 = plt.subplots(figsize=(7, 4))
        ax4.plot(df_s2["Month"], df_s2["Cumulative Profit (€)"], color="#f97316", linewidth=2.5)
        ax4.axhline(0, linestyle="--", color="gray", linewidth=1)
        ax4.fill_between(df_s2["Month"], df_s2["Cumulative Profit (€)"], 0,
                         where=[v >= 0 for v in df_s2["Cumulative Profit (€)"]],
                         alpha=0.15, color="#f97316", label="Κέρδος")
        ax4.fill_between(df_s2["Month"], df_s2["Cumulative Profit (€)"], 0,
                         where=[v < 0 for v in df_s2["Cumulative Profit (€)"]],
                         alpha=0.15, color="#ef4444", label="Ζημιά")
        ax4.set_xlabel("Μήνας", fontsize=11)
        ax4.set_ylabel("Συσσωρευμένο κέρδος (€)", fontsize=11)
        ax4.set_title("Συσσωρευμένο κέρδος (Tiered κόστος)", fontsize=12)
        ax4.legend()
        fig4.tight_layout()
        st.pyplot(fig4)

    with st.expander("🔍 Αναλυτικά δεδομένα — Σενάριο 2"):
        st.dataframe(df_s2, use_container_width=True)
