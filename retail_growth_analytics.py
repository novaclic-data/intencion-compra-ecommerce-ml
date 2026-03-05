# =================================================================
# PROJECT: E-COMMERCE CONVERSION & CONSUMER BEHAVIOR ANALYTICS
# GOAL: Predict purchase intent and optimize sales conversion (ROI).
# =================================================================

import pandas as pd
import matplotlib.pyplot as plt
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# --- STEP 1: DATA INGESTION AND QUALITY ASSURANCE ---
# Loading the online shoppers intention dataset
df = pd.read_csv(r"C:\Users\PC\OneDrive\Documentos\ia_ml\datos\intencion_compra.csv")
print(f"--- DATASET LOADED: {len(df)} web sessions found ---")

# Data Cleaning: Removing nulls and duplicates for a clean "Store"
df = df.dropna()
df = df.drop_duplicates()
print(f"✅ Clean Data: {len(df)} unique sessions ready for analysis.")

# --- STEP 2: BUSINESS KPI ANALYSIS (REVENUE & CONVERSION) ---
# True = Purchase Completed | False = Cart Abandonment
conversion_rate = df['Revenue'].value_counts(normalize=True) * 100
print("\n--- GLOBAL CONVERSION RATE (%) ---")
print(conversion_rate)

# Seasonality Analysis: Best months for sales
monthly_conversion = pd.crosstab(df['Month'], df['Revenue'], normalize='index') * 100
print("\n--- PURCHASE PROBABILITY BY MONTH (RANKING) ---")
print(monthly_conversion[True].sort_values(ascending=False))

# --- STEP 3: VISITOR LOYALTY & BEHAVIORAL INSIGHTS ---
# Comparing Returning vs New Visitors
visitor_impact = pd.crosstab(df['VisitorType'], df['Revenue'], normalize='index') * 100
print("\n--- CONVERSION BY VISITOR TYPE ---")
print(visitor_impact[True].sort_values(ascending=False))

# Exit Rates: Analyzing who leaves the site faster
exit_behavior = df.groupby('Revenue')['ExitRates'].mean()
print("\n--- AVERAGE EXIT RATES (PURCHASE VS ABANDONMENT) ---")
print(exit_behavior)

# --- STEP 4: DATA VISUALIZATION (STRATEGIC DASHBOARD) ---

# 1. Chart: Monthly Sales Seasonality
plt.figure(figsize=(12, 6))
monthly_conversion[True].sort_values(ascending=False).plot(kind='bar', color='#f39c12')
plt.title('E-commerce Seasonality: Highest Conversion Months', fontsize=14)
plt.xlabel('Month')
plt.ylabel('Conversion Rate (%)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("01_monthly_conversion_ranking.png")
plt.close()

# 2. Chart: Page Value Impact (The "Buy" Signal)
# Comparing the browsing value of buyers vs non-buyers
page_values = df.groupby('Revenue')['PageValues'].mean()
page_values.plot(kind='bar', color=['#e74c3c', '#2ecc71'], figsize=(8, 6))
plt.title('Average Page Value: Buyers vs Non-Buyers', fontsize=14)
plt.ylabel('Page Value Score')
plt.xticks([0, 1], ['Abandoned', 'Purchased'], rotation=0)
plt.tight_layout()
plt.savefig("02_page_value_impact.png")
plt.close()

# --- STEP 4.5: RFM SEGMENTATION (CUSTOMER LOYALTY) ---
# High Score (111) = Champions | Low Score (333) = At Risk
# We simulate the RFM visualization based on PageValues and VisitorType
plt.figure(figsize=(10, 6))
# Usamos una paleta de colores profesional (azul para VIP, naranja para Riesgo)
colors = ['#2980b9', '#3498db', '#f39c12', '#e67e22', '#e74c3c']
df.groupby('VisitorType')['PageValues'].mean().plot(kind='bar', color=colors)

plt.title('Customer Loyalty Segment: Page Value by Visitor Type', fontsize=14)
plt.xlabel('Customer Segment (Loyalty Group)')
plt.ylabel('Average Engagement Score (RFM)')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("04_rfm_customer_segments.png")
plt.close()

print("✅ RFM Loyalty Chart recovered successfully!")

# --- STEP 5: PREDICTIVE MODELING (PURCHASE INTENT AI) ---
features = ['Administrative', 'Informational', 'ProductRelated', 
            'ExitRates', 'PageValues', 'Month', 'VisitorType']
X = pd.get_dummies(df[features], drop_first=True)
y = df['Revenue']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Training the "Virtual Salesman" using Random Forest
# We use class_weight='balanced' to handle the minority purchase class
conversion_model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
conversion_model.fit(X_train, y_train)

# --- STEP 6: EVALUATION AND FEATURE IMPORTANCE ---
print("\n--- SALES PREDICTION PERFORMANCE REPORT ---")
predictions = conversion_model.predict(X_test)
print(classification_report(y_test, predictions))

# Exporting top indicators of purchase intent
importance = pd.Series(conversion_model.feature_importances_, index=X.columns)
plt.figure(figsize=(10, 6))
importance.sort_values(ascending=True).tail(10).plot(kind='barh', color='#2ecc71')
plt.title('Key Indicators of Purchase Intent', fontsize=14)
plt.xlabel('Impact Level on Conversion')
plt.tight_layout()
plt.savefig("03_purchase_intent_features.png")
plt.close()

# Exporting the trained AI model
joblib.dump(conversion_model, 'ecommerce_intent_model.pkl')
print("\n✅ RETAIL ANALYTICS PIPELINE COMPLETED.")