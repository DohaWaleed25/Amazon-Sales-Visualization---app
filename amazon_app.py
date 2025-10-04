import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Amazon Sales Dashboard", layout="wide")

st.title("📊 Amazon Sales Dashboard")

# ---------------------------------------------------
# هنا بنقرأ الداتا من Excel
# ---------------------------------------------------
df = pd.read_excel("Amazon_Sales_Cleaned.xlsx")  

# ---------------- Q1: Top Categories ----------------
st.header("Q1: What are the Top Categories with most products?")
top_categories = df['category'].value_counts().reset_index()
top_categories.columns = ['Category', 'Product Count']

fig1 = px.bar(top_categories.head(10), x="Category", y="Product Count", 
              title="Top Categories by Number of Products",
              color="Product Count", color_continuous_scale="Blues")
st.plotly_chart(fig1, use_container_width=True)

# ---------------- Q2: Actual vs Discount Price per Category ----------------
st.header("Q2: Difference between Actual Price and Discounted Price per Category")
df['price_diff'] = df['actual_price'] - df['discounted_price']
price_diff = df.groupby("category")[["actual_price","discounted_price","price_diff"]].mean().reset_index()

fig2 = px.bar(price_diff, x="category", y=["actual_price","discounted_price"], 
              barmode="group",
              title="Actual vs Discounted Price (Avg) per Category")
st.plotly_chart(fig2, use_container_width=True)

# ---------------- Q4: Top 10 Most Reviewed Products ----------------
st.header("Q4: Top 10 Most Reviewed Products with Category")
df['rating_count'] = pd.to_numeric(df['rating_count'], errors="coerce").fillna(0).astype(int)
top10_reviews = df.sort_values("rating_count", ascending=False).head(10)

fig3 = px.bar(top10_reviews, x="product_name", y="rating_count", color="category",
              title="Top 10 Most Reviewed Products by Category")
fig3.update_xaxes(tickangle=45)
st.plotly_chart(fig3, use_container_width=True)

# ---------------- Q5: Top 5 Products with Highest Rating Counts ----------------
st.header("Q5: Top 5 Products with Highest Rating Counts")
top5 = df.sort_values("rating_count", ascending=False).head(5)

fig4, ax = plt.subplots(figsize=(6,6))
ax.pie(top5["rating_count"], labels=top5["product_name"], autopct="%.1f%%", startangle=140)
ax.set_title("Top 5 Products with Highest Rating Counts (Pie Chart)")
st.pyplot(fig4)
