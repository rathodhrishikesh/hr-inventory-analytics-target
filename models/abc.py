import pandas as pd

# def abc_classification(df):
    # df = df.copy()
    # df["Annual_Dollar"] = df["Units_Sold"] * df["Cost"]
    # df = df.groupby("Product").sum().sort_values("Annual_Dollar", ascending=False)
    # df["CumPct"] = df["Annual_Dollar"].cumsum() / df["Annual_Dollar"].sum()
    # df["Class"] = pd.cut(df["CumPct"], bins=[0,0.8,0.95,1], labels=["A","B","C"])
    # return df.reset_index()

def abc_classification(df):
    df = df.copy()
    df["Annual_Dollar"] = df["Units_Sold"] * df["Cost"]
    grouped = df.groupby("Product", as_index=False)["Annual_Dollar"].sum()
    grouped = grouped.sort_values("Annual_Dollar", ascending=False)
    grouped["CumPct"] = grouped["Annual_Dollar"].cumsum() / grouped["Annual_Dollar"].sum()

    grouped["Class"] = pd.cut(
        grouped["CumPct"],
        bins=[0, 0.5, 0.75, 1],
        labels=["🔴 A", "🟡 B", "🟢 C"]
    )

    return grouped