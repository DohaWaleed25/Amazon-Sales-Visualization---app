# amazon_dashboard.py
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Amazon Sales Dashboard", layout="wide")

st.title("📊 Amazon Sales Dashboard")

# ---- Load Data from Excel ----
df = pd.read_excel("Amazon_Sales_Cleaned.xlsx")

# ---------------- Top Categories ----------------
st.header("Q1: What are the Top Categories with most products?")
top_categories = df['category'].value_counts().reset_index()
top_categories.columns = ['Category', 'Product Count']

fig1 = px.bar(top_categories.head(10), 
              x="Category", y="Product Count", 
              title="Top Categories by Number of Products",
              color="Product Count", color_continuous_scale="Blues",
              text="Product Count")
fig1.update_layout(width=900, height=500, xaxis_tickangle=45, margin=dict(l=50, r=50, t=50, b=50))
st.plotly_chart(fig1, use_container_width=True)

# ---------------- Distribution of Price Difference by Category ----------------
# Q2: Distribution of Price Difference by Category (Boxplot)
st.header("Q2: Distribution of Price Difference by Category")

# نعرض الأعمدة كلها عشان تختاري
numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
selected_col = st.selectbox("اختر العمود اللي عايزة تعملي عليه Boxplot:", numeric_cols)

if selected_col:
    fig, ax = plt.subplots(figsize=(12,6))
    sns.boxplot(data=df, x='main_category', y=selected_col, palette="Set2", ax=ax)

    ax.set_title(f"Distribution of {selected_col} by Category")
    ax.set_xlabel("Category")
    ax.set_ylabel(selected_col)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

    st.pyplot(fig)

# ---------------- Top 10 Most Reviewed Products ----------------
st.header("Q4: Top 10 Most Reviewed Products with Category")
df['rating_count'] = pd.to_numeric(df['rating_count'], errors="coerce").fillna(0).astype(int)
top10_reviews = df.sort_values("rating_count", ascending=False).head(10)

fig3 = px.bar(top10_reviews, x="product_name", y="rating_count", color="category",
              title="Top 10 Most Reviewed Products by Category", text="rating_count")
fig3.update_layout(width=900, height=500, xaxis_tickangle=45, margin=dict(l=50, r=50, t=50, b=50))
st.plotly_chart(fig3, use_container_width=True)

# ---------------- Top 5 Products with Highest Rating Counts ----------------
st.header("Q5: Top 5 Products with Highest Rating Counts")
top5 = df.sort_values("rating_count", ascending=False).head(5)

fig4, ax = plt.subplots(figsize=(8,8))   # 👈 هنا تحكم في حجم الـ Pie Chart
ax.pie(top5["rating_count"], labels=top5["product_name"], autopct="%.1f%%", startangle=140)
ax.set_title("Top 5 Products with Highest Rating Counts (Pie Chart)")
st.pyplot(fig4)




