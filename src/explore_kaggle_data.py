"""
Explore Kaggle Credit Risk Dataset
Understand the structure and map to MSME context
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')


def load_kaggle_data():
    """Load the Kaggle credit risk dataset"""
    
    try:
        df = pd.read_csv('data/raw/credit_risk_dataset.csv')
        print("✅ Kaggle dataset loaded successfully!")
        return df
    except FileNotFoundError:
        print("❌ Error: credit_risk_dataset.csv not found in data/raw/")
        print("\n📥 Please download from:")
        print("   https://www.kaggle.com/datasets/laotse/credit-risk-dataset")
        print("\n📂 Save it to: data/raw/credit_risk_dataset.csv")
        return None


def explore_dataset(df):
    """Explore the Kaggle dataset structure"""
    
    if df is None:
        return
    
    print("\n" + "="*70)
    print("📊 KAGGLE CREDIT RISK DATASET - ANALYSIS")
    print("="*70)
    
    # Basic info
    print("\n1️⃣ DATASET SHAPE")
    print(f"   Rows: {df.shape[0]:,}")
    print(f"   Columns: {df.shape[1]}")
    
    # Column names and types
    print("\n2️⃣ COLUMN NAMES & DATA TYPES")
    print("-" * 70)
    for col in df.columns:
        dtype = df[col].dtype
        non_null = df[col].notna().sum()
        null_pct = (df[col].isna().sum() / len(df)) * 100
        print(f"   {col:25s} | {str(dtype):10s} | Non-null: {non_null:6,} | Null: {null_pct:5.2f}%")
    
    # First few rows
    print("\n3️⃣ FIRST 5 ROWS")
    print("-" * 70)
    print(df.head())
    
    # Statistical summary
    print("\n4️⃣ STATISTICAL SUMMARY (Numerical Columns)")
    print("-" * 70)
    print(df.describe())
    
    # Categorical columns
    print("\n5️⃣ CATEGORICAL COLUMNS - UNIQUE VALUES")
    print("-" * 70)
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        unique_count = df[col].nunique()
        print(f"\n   {col}: {unique_count} unique values")
        if unique_count <= 10:
            print(f"   Values: {df[col].value_counts().to_dict()}")
    
    # Target variable (if exists)
    print("\n6️⃣ TARGET VARIABLE ANALYSIS")
    print("-" * 70)
    
    # Common target column names in credit datasets
    possible_targets = ['loan_status', 'default', 'cb_person_default_on_file', 
                       'loan_grade', 'target', 'status']
    
    target_found = False
    for col in possible_targets:
        if col in df.columns:
            print(f"\n   Found target column: '{col}'")
            print(f"   Distribution:")
            print(df[col].value_counts())
            target_found = True
            break
    
    if not target_found:
        print("   No standard target column found.")
        print("   Columns available:", list(df.columns))
    
    return df


def map_to_msme_context(df):
    """
    Suggest mapping between Kaggle dataset columns and MSME features
    """
    
    if df is None:
        return
    
    print("\n" + "="*70)
    print("🔄 MAPPING TO MSME CONTEXT")
    print("="*70)
    
    print("\n📋 SUGGESTED COLUMN MAPPING:\n")
    
    # Common mappings
    mappings = {
        "person_age": "business_age_years (proxy)",
        "person_income": "avg_monthly_turnover",
        "person_emp_length": "business_age_years",
        "loan_amnt": "loan_amount_requested",
        "loan_int_rate": "interest_rate_offered",
        "loan_percent_income": "loan_to_turnover_ratio",
        "cb_person_cred_hist_length": "credit_history_years",
        "person_home_ownership": "collateral_available (map: OWN/MORTGAGE -> True)",
        "loan_intent": "loan_purpose",
        "loan_grade": "credit_label (A/B/C -> Approve/Review/Reject)",
        "cb_person_default_on_file": "existing_loans (Y -> True)"
    }
    
    available_mappings = []
    missing_columns = []
    
    for kaggle_col, msme_feature in mappings.items():
        if kaggle_col in df.columns:
            available_mappings.append((kaggle_col, msme_feature))
            print(f"✅ {kaggle_col:30s} → {msme_feature}")
        else:
            missing_columns.append(kaggle_col)
    
    if missing_columns:
        print(f"\n⚠️  Columns not found in dataset:")
        for col in missing_columns:
            print(f"   - {col}")
    
    print("\n" + "="*70)
    print("💡 RECOMMENDATION:")
    print("="*70)
    print("""
    Use this Kaggle dataset as:
    
    1. BASELINE COMPARISON
       - Compare our synthetic MSME data distribution with real credit data
       - Validate if our synthetic data patterns are realistic
    
    2. FEATURE ENGINEERING IDEAS
       - See what features are important in real credit datasets
       - Adopt similar feature engineering techniques
    
    3. MODEL BENCHMARKING
       - Train models on Kaggle data first
       - Then apply same techniques to our MSME data
       - Compare performance metrics
    
    4. ENSEMBLE APPROACH (Advanced)
       - Combine Kaggle data with synthetic MSME data
       - Use transfer learning concepts
    """)
    
    return available_mappings


def compare_with_synthetic(kaggle_df, synthetic_df_path='data/raw/msme_data.csv'):
    """
    Compare Kaggle data distribution with our synthetic MSME data
    """
    
    if kaggle_df is None:
        return
    
    try:
        msme_df = pd.read_csv(synthetic_df_path)
    except FileNotFoundError:
        print(f"\n⚠️  Synthetic MSME data not found at {synthetic_df_path}")
        return
    
    print("\n" + "="*70)
    print("⚖️  COMPARISON: Kaggle vs Synthetic MSME Data")
    print("="*70)
    
    print(f"\nKaggle Dataset:        {kaggle_df.shape[0]:6,} rows × {kaggle_df.shape[1]:2} columns")
    print(f"Synthetic MSME Data:   {msme_df.shape[0]:6,} rows × {msme_df.shape[1]:2} columns")
    
    # Compare loan amounts if available
    if 'loan_amnt' in kaggle_df.columns and 'loan_amount_requested' in msme_df.columns:
        print("\n📊 LOAN AMOUNT COMPARISON:")
        print(f"   Kaggle - Mean: ₹{kaggle_df['loan_amnt'].mean():,.2f} | Median: ₹{kaggle_df['loan_amnt'].median():,.2f}")
        print(f"   MSME   - Mean: ₹{msme_df['loan_amount_requested'].mean():,.2f} | Median: ₹{msme_df['loan_amount_requested'].median():,.2f}")


def main():
    """Main execution"""
    
    print("="*70)
    print("🔍 KAGGLE CREDIT RISK DATASET EXPLORER")
    print("="*70)
    
    # Load data
    df = load_kaggle_data()
    
    if df is not None:
        # Explore
        df = explore_dataset(df)
        
        # Map to MSME context
        map_to_msme_context(df)
        
        # Compare with synthetic data
        compare_with_synthetic(df)
    
    print("\n" + "="*70)
    print("✅ ANALYSIS COMPLETE!")
    print("="*70)


if __name__ == "__main__":
    main()