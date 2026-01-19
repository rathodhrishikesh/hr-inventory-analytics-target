import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from scipy import stats

from models.eoq import calculate_eoq
from models.rop import calculate_rop
from models.newsvendor import newsvendor_optimal_q


def show_inventory_models(ts, filtered):
    """Display Inventory Models tab content (EOQ, ROP, Newsvendor)"""
    
    st.subheader("📦 EOQ + ROP")
    
    col_param1, col_param2 = st.columns(2)
    with col_param1:
        D = ts.sum()
        S = st.slider("Order Cost ($)", 50, 500, 100, key="order_cost")
        H = st.slider("Holding Cost ($)", 1, 20, 5, key="holding_cost")
    
    with col_param2:
        lead = st.slider("Lead Time (days)", 1, 30, 7)
        std = ts.std()
        service = st.slider("Service Level Z", 1.28, 2.33, 1.65, key="service_level")
    
    eoq = calculate_eoq(D, S, H)
    rop = calculate_rop(ts.mean(), lead, std, service)
    
    # Display results in columns
    col_eoq, col_rop = st.columns(2)
    with col_eoq:
        st.metric("Economic Order Quantity (EOQ)", f"{int(eoq)} units", delta=f"Annual Cost: ${int((2 * S * D / eoq * H)):,}")
    with col_rop:
        st.metric("Reorder Point (ROP)", f"{int(rop)} units", delta=f"Lead Time: {lead} days")
    
    # Visualization: EOQ cost curve
    quantities = np.linspace(max(1, eoq * 0.3), eoq * 2, 200)
    holding_costs = (quantities / 2) * H
    ordering_costs = (D / quantities) * S
    total_costs = holding_costs + ordering_costs
    
    # Create DataFrame for better legend labels
    eoq_data = pd.DataFrame({
        'Order Quantity': quantities,
        'Holding Cost (H/2 × Q)': holding_costs,
        'Ordering Cost (D/Q × S)': ordering_costs,
        'Total Cost (H + O)': total_costs
    })
    
    fig_eoq = px.line(
        eoq_data,
        x='Order Quantity',
        y=['Holding Cost (H/2 × Q)', 'Ordering Cost (D/Q × S)', 'Total Cost (H + O)'],
        labels={"x": "Order Quantity (units)", "value": "Annual Cost ($)"},
        title="EOQ Cost Analysis",
        line_shape="spline"
    )
    
    # Update colors for better visualization
    colors_eoq = ['#FF6B6B', '#4ECDC4', '#2C3E50']
    for i, trace in enumerate(fig_eoq.data):
        trace.line.color = colors_eoq[i]
    
    fig_eoq.add_vline(x=eoq, line_dash="dash", line_color="red", annotation_text=f"EOQ: {int(eoq)} units")
    fig_eoq.update_layout(template="plotly_white", hovermode="x unified", height=450)
    st.plotly_chart(fig_eoq, use_container_width=True)
    
    # Visualization: ROP with demand distribution
    demand_range = np.linspace(0, ts.mean() + 3 * std, 100)
    demand_dist = stats.norm.pdf(demand_range, ts.mean(), std)
    
    fig_rop = px.area(
        x=demand_range,
        y=demand_dist,
        labels={"x": "Demand during Lead Time", "y": "Probability Density"},
        title="ROP & Service Level Visualization"
    )
    fig_rop.add_vline(x=rop, line_dash="dash", line_color="green", annotation_text=f"ROP: {int(rop)} units")
    st.plotly_chart(fig_rop, use_container_width=True)
    
    st.divider()
    st.subheader("💰 Newsvendor Model")
    
    col_nv1, col_nv2 = st.columns(2)
    with col_nv1:
        mu, sigma = ts.mean(), std
        cu = st.slider("Understock Cost ($)", 1, 50, 10, key="understock")
    
    with col_nv2:
        co = st.slider("Overstock Cost ($)", 1, 50, 5, key="overstock")
    
    q_opt = newsvendor_optimal_q(mu, sigma, cu, co)
    
    st.metric("Optimal Order Quantity", f"{int(q_opt)} units", delta=f"Critical Ratio: {cu/(cu+co):.2%}")
    
    # Visualization: Profit function
    quantities_nv = np.linspace(mu - 3*sigma, mu + 3*sigma, 200)
    profits = []
    for q in quantities_nv:
        sold = np.minimum(q, mu)
        leftover = np.maximum(q - mu, 0)
        profit = sold * (1) - leftover * co - (q - sold) * cu if q > sold else sold * (1)
        profits.append(profit)
    
    fig_nv = px.line(
        x=quantities_nv,
        y=profits,
        labels={"x": "Order Quantity (units)", "y": "Expected Profit ($)"},
        title="Newsvendor Profit Function",
        line_shape="spline"
    )
    fig_nv.add_vline(x=q_opt, line_dash="dash", line_color="orange", annotation_text=f"Optimal Q: {int(q_opt)} units")
    st.plotly_chart(fig_nv, use_container_width=True)
