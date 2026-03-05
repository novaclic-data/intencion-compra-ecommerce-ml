# =================================================================
# PROJECT: RETAIL CUSTOMER SEGMENTATION (RFM ANALYSIS)
# GOAL: Categorize customers by Recency, Frequency, and Monetary value.
# =================================================================

import pandas as pd
import matplotlib.pyplot as plt
import joblib

# --- STEP 1: DATA INGESTION AND QUALITY CONTROL ---
# Loading retail dataset with 'latin1' encoding to avoid Unicode errors
df = pd.read_csv(r"C:\Users\PC\OneDrive\Documentos\ia_ml\datos\retail_ventas.csv", encoding='latin1')
print(f"--- DATASET LOADED: {len(df)} transactions found ---")

# Data Cleansing: Removing nulls in CustomerID and handling returns
df = df.dropna(subset=['CustomerID'])
df['CustomerID'] = df['CustomerID'].astype(int)
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['TotalSum'] = df['Quantity'] * df['UnitPrice']
df = df[df['Quantity'] > 0] # Removing negative quantities (returns)

print(f"✅ Data Cleansing Completed. Clean records: {len(df)}")

# --- STEP 2: RFM MODEL CALCULATION ---
# Setting snapshot date for Recency calculation (Last date + 1 day)
snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)

# Grouping by Customer to calculate R, F, and M
rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days, # Recency
    'InvoiceNo': 'count',                                   # Frequency
    'TotalSum': 'sum'                                       # Monetary
})

rfm.rename(columns={
    'InvoiceDate': 'Recency',
    'InvoiceNo': 'Frequency',
    'TotalSum': 'MonetaryValue'
}, inplace=True)

print("--- RFM TABLE GENERATED ---")
print(rfm.head())

# --- STEP 3: CUSTOMER SCORING (RANKING 1 TO 4) ---
# 1 is the best (Champions), 4 is the lowest
r_labels = range(1, 5)
f_labels = range(4, 0, -1)
m_labels = range(4, 0, -1)

rfm['R'] = pd.qcut(rfm['Recency'], q=4, labels=r_labels)
rfm['F'] = pd.qcut(rfm['Frequency'], q=4, labels=f_labels)
rfm['M'] = pd.qcut(rfm['MonetaryValue'], q=4, labels=m_labels)

# Creating the RFM Score (e.g., '111' is a perfect customer)
rfm['RFM_Score'] = rfm['R'].astype(str) + rfm['F'].astype(str) + rfm['M'].astype(str)

# --- STEP 4: DATA VISUALIZATION (EXECUTIVE INSIGHTS) ---

# 1. Chart: Top 10 Segments by Average Spending
plt.figure(figsize=(10, 6))
rfm.groupby('RFM_Score')['MonetaryValue'].mean().sort_values(ascending=False).head(10).plot(kind='bar', color='#f1c40f')
plt.title('Top 10 Customer Segments by Average Spending', fontsize=14)
plt.xlabel('RFM Score (111 = Champions)')
plt.ylabel('Average Monetary Value ($)')
plt.tight_layout()
plt.savefig("01_customer_segments_spending.png")
plt.close()

# 2. Chart: Customer Behavior Heatmap (Recency vs Frequency)
plt.figure(figsize=(12, 7))
scatter = plt.scatter(rfm['Recency'], rfm['Frequency'], 
            c=rfm['MonetaryValue'], 
            cmap='plasma', s=60, alpha=0.6, edgecolors='white', linewidth=0.5)

plt.xlim(-20, 450) 
plt.ylim(-10, 600) 
plt.title('Customer Segmentation: Behavioral Patterns and Value', fontsize=16, fontweight='bold')
plt.xlabel('Days since last purchase (Recency)')
plt.ylabel('Number of transactions (Frequency)')

cbar = plt.colorbar(scatter)
cbar.set_label('Total Monetary Value ($)', labelpad=15)
plt.grid(True, linestyle='--', alpha=0.3)
plt.tight_layout()
plt.savefig("02_customer_behavior_heatmap.png")
plt.close()

# Exporting Segmented Data
rfm.to_csv("customer_segmentation_results.csv")
print("\n✅ RFM ANALYSIS COMPLETED: Metrics and visualizations exported.")