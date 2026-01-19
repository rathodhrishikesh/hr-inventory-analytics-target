# def detect_bottlenecks(df):
    # df = df.copy()
    # df["Stockout_Risk"] = df["Units_Sold"] / df["Units_Sold"].mean()
    # return df.sort_values("Stockout_Risk", ascending=False).head(20)

def detect_bottlenecks(df):
    import pandas as pd
    import numpy as np

    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])

    # 1. Aggregate daily demand at Store–Product level
    daily = (
        df.groupby(["Store", "Product", "Date"], as_index=False)
          .agg({"Units_Sold": "sum"})
    )

    # 2. Rolling demand (sales velocity)
    daily["Rolling_Mean"] = (
        daily.groupby(["Store", "Product"])["Units_Sold"]
        .transform(lambda x: x.rolling(14, min_periods=3).mean())
    )

    # 3. Demand volatility
    daily["Rolling_Std"] = (
        daily.groupby(["Store", "Product"])["Units_Sold"]
        .transform(lambda x: x.rolling(14, min_periods=3).std())
    )

    # 4. Recent demand acceleration
    daily["Demand_Trend"] = (
        daily.groupby(["Store", "Product"])["Rolling_Mean"]
        .pct_change(fill_method=None)
    )

    # 5. Clean NaNs / inf
    daily[["Rolling_Mean", "Rolling_Std", "Demand_Trend"]] = (
        daily[["Rolling_Mean", "Rolling_Std", "Demand_Trend"]]
        .replace([np.inf, -np.inf], 0)
        .fillna(0)
    )

    # 6. Normalize components
    daily["Norm_Demand"] = daily["Rolling_Mean"] / max(daily["Rolling_Mean"].mean(), 1)
    daily["Norm_Volatility"] = daily["Rolling_Std"] / max(daily["Rolling_Std"].mean(), 1)
    daily["Norm_Trend"] = daily["Demand_Trend"].clip(lower=0)

    # 7. Composite Stockout Risk score
    daily["Stockout_Risk"] = (
        0.5 * daily["Norm_Demand"] +
        0.3 * daily["Norm_Volatility"] +
        0.2 * daily["Norm_Trend"]
    )

    # 8. Keep most recent record per Store–Product
    latest = (
        daily.sort_values("Date")
             .groupby(["Store", "Product"])
             .tail(1)
    )

    result = (
        latest.sort_values("Stockout_Risk", ascending=False)
              .head(20)
              .reset_index(drop=True)
    )
    
    # Reorder columns: Units_Sold followed by Stockout_Risk
    cols = result.columns.tolist()
    cols.remove("Stockout_Risk")
    units_sold_idx = cols.index("Units_Sold")
    cols.insert(units_sold_idx + 1, "Stockout_Risk")
    
    return result[cols]
