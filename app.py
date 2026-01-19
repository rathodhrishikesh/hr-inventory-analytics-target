import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

from tabs.inventory_models import show_inventory_models
from models.abc import abc_classification
from models.forecasting import moving_average_forecast
from models.bottleneck import detect_bottlenecks

st.set_page_config(page_title="Inventory Analytics Simulator", layout="wide")

# Title with logo on the right
col_title, col_logo = st.columns([4, 1])
with col_title:
    st.title("📦 Inventory Analytics – Target")
with col_logo:
    st.image("images/target_logo.png", width=80)

@st.cache_data
def load_data():
    data_path = os.path.join(os.path.dirname(__file__), "data", "sales_data.csv")
    return pd.read_csv(data_path, parse_dates=["Date"])

df = load_data()

# store = st.sidebar.selectbox("Select Store", df["Store"].unique())
# category = st.sidebar.selectbox("Select Category", df["Category"].unique())
# product = st.sidebar.selectbox("Select Product", df["Product"].unique())

# filtered = df[(df["Store"]==store) & (df["Category"]==category) & (df["Product"]==product)]

stores = st.sidebar.multiselect("Select Store(s)", df["Store"].unique(), df["Store"].unique())
categories = st.sidebar.multiselect("Select Category(s)", df["Category"].unique(), df["Category"].unique())
products = st.sidebar.multiselect("Select Product(s)", df["Product"].unique(), df["Product"].unique())

# Date range filter
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df["Date"].min().date(), df["Date"].max().date()),
    min_value=df["Date"].min().date(),
    max_value=df["Date"].max().date()
)

filtered = df[
    (df["Store"].isin(stores)) &
    (df["Category"].isin(categories)) &
    (df["Product"].isin(products)) &
    (df["Date"].dt.date >= date_range[0]) &
    (df["Date"].dt.date <= date_range[1])
]

st.subheader("📊 KPI Dashboard")
col1,col2,col3,col4 = st.columns(4)
col1.metric("Revenue", f"${filtered['Revenue'].sum():,.0f}")
col2.metric("Units Sold", int(filtered["Units_Sold"].sum()))
col3.metric("Avg Price", f"${filtered['Price'].mean():.2f}")
col4.metric("Margin", f"${(filtered['Price']-filtered['Cost']).mean():.2f}")

st.subheader("📈 Demand Forecasting")
ts = filtered.groupby("Date")["Units_Sold"].sum()
forecast = moving_average_forecast(ts,7)

# Create DataFrame for proper visualization
forecast_df = pd.DataFrame({
    'Date': ts.index,
    'Actual Demand': ts.values,
    'Forecast (7-day MA)': forecast.values
})

fig = px.line(
    forecast_df,
    x='Date',
    y=['Actual Demand', 'Forecast (7-day MA)'],
    labels={"value": "Units", "Date": "Date"},
    title="Actual vs Forecast Demand",
    line_shape="spline"
)

fig.update_traces(
    line=dict(width=2.5),
    hovertemplate='<b>%{x|%b %d}</b><br>%{y:,.0f} units<extra></extra>'
)

# Color scheme
colors = ['#1f77b4', '#ff7f0e']
for i, trace in enumerate(fig.data):
    trace.line.color = colors[i]

fig.update_layout(
    template="plotly_white",
    hovermode="x unified",
    height=400,
    margin=dict(l=50, r=50, t=50, b=50),
    font=dict(size=11),
    xaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray'),
    yaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray'),
    plot_bgcolor='rgba(250,250,250,0.5)'
)

st.plotly_chart(fig, use_container_width=True)

# Create tabs for modeling and analysis
tab1, tab2, tab3 = st.tabs(["📊 ABC Classification", "🚨 Bottleneck Detection", "📦 Inventory Models"])

with tab3:
    show_inventory_models(ts, filtered)

with tab1:
    st.subheader("📊 ABC Classification")
    abc = abc_classification(filtered)
    st.dataframe(abc)
    
    st.divider()
    st.subheader("Legend")
    
    legend_data = {
        "Class": ["🔴 A", "🟡 B", "🟢 C"],
        "Priority": ["High Priority", "Medium Priority", "Low Priority"],
        "Description": ["0-50% of value", "50-75% of value", "75-100% of value"]
    }
    
    legend_df = pd.DataFrame(legend_data)
    st.dataframe(legend_df, hide_index=True, use_container_width=True)

with tab2:
    st.subheader("🚨 Bottleneck Detection")
    
    # Display bottleneck data
    st.markdown("#### Top 20 High-Risk Products")
    bottlenecks = detect_bottlenecks(filtered)
    st.dataframe(bottlenecks, use_container_width=True)

    # Display Stockout Risk formula
    st.markdown("#### Stockout Risk Formula")
    st.latex(r"Stockout\_Risk = 0.5 \times Demand + 0.3 \times Volatility + 0.2 \times Trend")
    st.info("📌 Higher risk = More likely to stockout")
    
    st.divider()
    
    # Display methodology
    with st.expander("📖 Formula Components", expanded=True):
        formula_components = {
            "Component": ["Demand (50%)", "Volatility (30%)", "Trend (20%)"],
            "Description": [
                "Rolling 14-day average demand (normalized)",
                "Rolling 14-day demand standard deviation (normalized)",
                "Recent demand growth acceleration (% change in demand)"
            ]
        }
        st.dataframe(pd.DataFrame(formula_components), hide_index=True, use_container_width=True)