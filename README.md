# 📦 Inventory Analytics - Target

A comprehensive Streamlit application for inventory optimization and demand forecasting, designed to help analyze and optimize supply chain operations using advanced inventory management models.

## 🚀 Live Demo

**Try the deployed application:**

🔗 **Visit:** https://hr-inventory-analytics-target.streamlit.app/

## 🎯 Features

### 1. **KPI Dashboard**
- Real-time revenue metrics
- Units sold tracking
- Average pricing analysis
- Profit margin calculations

### 2. **Demand Forecasting**
- 7-day moving average forecasting
- Actual vs. Forecast comparison visualization
- Clean, interactive time-series charts

### 3. **ABC Classification** (Tab 1)
- Automated product classification based on value contribution
- **Class A**: 0-50% of revenue (High Priority)
- **Class B**: 50-75% of revenue (Medium Priority)
- **Class C**: 75-100% of revenue (Low Priority)
- Visual legend with priority indicators

### 4. **Bottleneck Detection** (Tab 2)
- Identify high-risk products prone to stockouts
- **Stockout Risk Formula**: 0.5×Demand + 0.3×Volatility + 0.2×Trend
- Components:
  - Demand: 14-day rolling average (normalized)
  - Volatility: 14-day rolling standard deviation
  - Trend: Recent demand growth acceleration
- Top 20 high-risk products ranking

### 5. **Inventory Optimization Models** (Tab 3)

#### **EOQ + ROP Model**
- Economic Order Quantity calculation
- Reorder Point determination with service level adjustment
- Cost analysis visualization showing:
  - Holding costs
  - Ordering costs
  - Total inventory costs
- ROP distribution visualization with service level

#### **Newsvendor Model**
- Dynamic order quantity optimization
- Understock and overstock cost configuration
- Critical ratio calculation
- Profit function visualization

## 📊 Filters & Customization

**Sidebar Controls:**
- Select one or multiple stores
- Filter by product categories
- Choose specific products
- Select date range
- All metrics and models update dynamically

## 📁 Project Structure

```
inventory_simulator/
├── app.py                          # Main Streamlit application
├── data/
│   └── sales_data.csv             # Input data
├── models/
│   ├── eoq.py                     # Economic Order Quantity model
│   ├── rop.py                     # Reorder Point model
│   ├── newsvendor.py              # Newsvendor optimization model
│   ├── abc.py                     # ABC classification
│   ├── forecasting.py             # Demand forecasting
│   └── bottleneck.py              # Bottleneck detection
├── tabs/
│   └── inventory_models.py        # Inventory models tab module
├── images/
│   └── target_logo.png            # Target logo (80x80)
└── README.md                       # This file
```

## 📈 Mathematical Models

### **Economic Order Quantity (EOQ)**
$$EOQ = \sqrt{\frac{2DS}{H}}$$

Where:
- D = Annual demand
- S = Ordering cost per order
- H = Holding cost per unit per year

### **Reorder Point (ROP)**
$$ROP = \mu L + Z \times \sigma \times \sqrt{L}$$

Where:
- μ = Mean demand
- L = Lead time
- σ = Demand standard deviation
- Z = Service level factor

### **Stockout Risk Score**
$$Risk = 0.5 \times Demand_{norm} + 0.3 \times Volatility_{norm} + 0.2 \times Trend$$

## 📊 Data Format

**Required CSV columns:**
- `Date`: Transaction date
- `Store`: Store identifier
- `Product`: Product name/ID
- `Category`: Product category
- `Units_Sold`: Units sold in transaction
- `Price`: Sale price
- `Cost`: Cost to acquire
- `Revenue`: Sale revenue

## 💡 Use Cases

1. **Inventory Planning**: Determine optimal order quantities and reorder points
2. **Product Classification**: Identify critical products requiring close monitoring
3. **Risk Assessment**: Detect products at high stockout risk
4. **Demand Analysis**: Visualize actual vs. forecasted demand patterns
5. **Cost Optimization**: Analyze holding vs. ordering cost trade-offs