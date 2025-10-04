# simple_streamlit_app.py
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Amazon Sales Visuals", layout="wide")

st.title("📊 Amazon Sales Visualizations")

# ---- Load data ----
uploaded = st.file_uploader("Upload your cleaned dataset", type=["csv", "xlsx"])
if uploaded:
    if uploaded.name.endswith(".csv"):
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_excel(uploaded)
else:
    st.warning("Please upload your cleaned dataset to continue.")
    st.stop()

# ---- Tabs for different charts ----
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Price Distribution", 
    "Rating Distribution", 
    "Correlation Heatmap", 
    "Top Products", 
    "Top Categories"
])

# ---- Tab 1: Price Distribution ----
with tab1:
    st.subheader("Discounted Price Distribution")
    if "discounted_price" in df.columns:
        fig, ax = plt.subplots(figsize=(8,5))
        sns.histplot(df["discounted_price"], bins=50, kde=True, ax=ax, color="skyblue")
        st.pyplot(fig)

# ---- Tab 2: Rating Distribution ----
with tab2:
    st.subheader("Rating Distribution")
    if "rating" in df.columns:
        fig, ax = plt.subplots(figsize=(8,5))
        sns.histplot(df["rating"], bins=20, kde=False, ax=ax, color="orange")
        st.pyplot(fig)

# ---- Tab 3: Correlation Heatmap ----
with tab3:
    st.subheader("Correlation Heatmap")
    num_cols = df.select_dtypes(include="number").columns
    if len(num_cols) > 1:
        corr = df[num_cols].corr()
        fig, ax = plt.subplots(figsize=(8,6))
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)

# ---- Tab 4: Top Products ----
with tab4:
    st.subheader("Top 10 Products by Rating Count")
    if "rating_count" in df.columns:
        df["rating_count"] = pd.to_numeric(df["rating_count"], errors="coerce")
        top_products = df.nlargest(10, "rating_count")
        fig = px.bar(top_products, x="product_name", y="rating_count", title="Top 10 Reviewed Products", color="rating_count")
        st.plotly_chart(fig, use_container_width=True)

# ---- Tab 5: Top Categories ----
with tab5:
    st.subheader("Top 10 Categories by Revenue (Discounted Price × Rating Count)")
    if {"discounted_price", "rating_count", "category"}.issubset(df.columns):
        df["rating_count"] = pd.to_numeric(df["rating_count"], errors="coerce").fillna(0)
        df["revenue"] = df["discounted_price"] * df["rating_count"]
        top_cat = df.groupby("category")["revenue"].sum().reset_index().sort_values("revenue", ascending=False).head(10)
        fig = px.bar(top_cat, x="category", y="revenue", title="Top 10 Categories by Revenue", color="revenue")
        st.plotly_chart(fig, use_container_width=True)
```
