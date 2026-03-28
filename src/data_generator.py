"""
MSME Credit Scoring - Synthetic Data Generator
Generates realistic MSME profiles with credit features for ML modeling
"""

import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import warnings
import os
warnings.filterwarnings('ignore')

# Set random seed for reproducibility
np.random.seed(42)
fake = Faker('en_IN')  # Indian locale
Faker.seed(42)


class MSMEDataGenerator:
    """Generate synthetic MSME credit data with realistic patterns"""
    
    def __init__(self, n_samples=5000):
        self.n_samples = n_samples
        self.indian_states = [
            'Maharashtra', 'Karnataka', 'Tamil Nadu', 'Gujarat', 'Delhi',
            'Uttar Pradesh', 'West Bengal', 'Rajasthan', 'Telangana', 'Kerala',
            'Punjab', 'Haryana', 'Madhya Pradesh', 'Andhra Pradesh', 'Bihar'
        ]
        self.industries = [
            'Manufacturing', 'Retail', 'Services', 'Food & Beverage', 'Textile'
        ]
        self.loan_purposes = [
            'Working Capital', 'Machinery', 'Expansion', 'Inventory'
        ]
        
    def generate_msme_profiles(self):
        """Generate basic MSME profile information"""
        
        data = {
            'msme_id': [f'MSME{str(i).zfill(6)}' for i in range(1, self.n_samples + 1)],
            'business_name': [self._generate_business_name() for _ in range(self.n_samples)],
            'industry_type': np.random.choice(self.industries, self.n_samples),
            'business_age_years': np.random.randint(1, 21, self.n_samples),
            'state': np.random.choice(self.indian_states, self.n_samples),
            'udyam_registered': np.random.choice([True, False], self.n_samples, p=[0.65, 0.35])
        }
        
        return pd.DataFrame(data)
    
    def _generate_business_name(self):
        """Generate realistic Indian business names"""
        prefixes = ['Sri', 'Shri', 'Kumar', 'Singh', 'Patel', 'Sharma', 'Global']
        suffixes = ['Enterprises', 'Industries', 'Traders', 'Solutions', 'Corporation', 
                   'Manufacturing', 'Services', 'Exports']
        
        if np.random.random() > 0.3:
            return f"{np.random.choice(prefixes)} {fake.last_name()} {np.random.choice(suffixes)}"
        else:
            return f"{fake.company()}"
    
    def add_gst_features(self, df):
        """Add GST compliance and turnover features"""
        
        # GST filing months (better for older, registered businesses)
        base_filing = np.random.randint(6, 13, self.n_samples)
        df['gst_filing_months'] = np.where(
            df['udyam_registered'], 
            np.minimum(base_filing + 2, 12),
            base_filing
        )
        
        # Average monthly turnover - varies by industry
        turnover_base = np.random.lognormal(13, 1.2, self.n_samples)
        
        industry_multipliers = {
            'Manufacturing': 1.5,
            'Retail': 1.0,
            'Services': 1.2,
            'Food & Beverage': 0.9,
            'Textile': 1.3
        }
        
        df['avg_monthly_turnover'] = df['industry_type'].map(industry_multipliers) * turnover_base
        df['avg_monthly_turnover'] = df['avg_monthly_turnover'].round(2)
        
        # GST compliance score (0-100)
        df['gst_compliance_score'] = (
            (df['gst_filing_months'] / 12) * 50 +
            (df['business_age_years'] / 20) * 30 +
            np.random.uniform(0, 20, self.n_samples)
        ).clip(0, 100).round(2)
        
        # Turnover growth rate (%)
        age_factor = np.where(df['business_age_years'] < 5, 1.5, 1.0)
        df['turnover_growth_rate'] = (
            np.random.normal(15, 25, self.n_samples) * age_factor
        ).round(2)
        
        return df
    
    def add_upi_transaction_features(self, df):
        """Add UPI and digital transaction patterns"""
        
        # UPI inflow - correlated with turnover
        df['avg_monthly_upi_inflow'] = (
            df['avg_monthly_turnover'] * np.random.uniform(0.3, 0.8, self.n_samples)
        ).round(2)
        
        # Transaction consistency (0-1)
        base_consistency = np.random.beta(5, 2, self.n_samples)
        df['upi_transaction_consistency'] = (
            base_consistency * (1 + df['business_age_years'] / 40)
        ).clip(0, 1).round(3)
        
        # Number of unique buyers
        buyer_base = {
            'Manufacturing': np.random.randint(20, 150, self.n_samples),
            'Retail': np.random.randint(100, 500, self.n_samples),
            'Services': np.random.randint(10, 100, self.n_samples),
            'Food & Beverage': np.random.randint(50, 300, self.n_samples),
            'Textile': np.random.randint(30, 200, self.n_samples)
        }
        df['num_unique_buyers'] = df['industry_type'].map(
            lambda x: np.random.choice(buyer_base[x])
        )
        
        # Peak to off-peak ratio
        seasonal_industries = ['Food & Beverage', 'Retail', 'Textile']
        df['peak_to_offpeak_ratio'] = np.where(
            df['industry_type'].isin(seasonal_industries),
            np.random.uniform(2.0, 5.0, self.n_samples),
            np.random.uniform(1.1, 2.5, self.n_samples)
        ).round(2)
        
        return df
    
    def add_loan_features(self, df):
        """Add loan request and credit features"""
        
        # Loan amount requested
        industry_loan_multipliers = {
            'Manufacturing': 8,
            'Retail': 4,
            'Services': 5,
            'Food & Beverage': 4,
            'Textile': 6
        }
        
        df['loan_amount_requested'] = (
            df['industry_type'].map(industry_loan_multipliers) * 
            df['avg_monthly_turnover'] * 
            np.random.uniform(0.5, 2.0, self.n_samples)
        ).round(2)
        
        # Loan purpose
        df['loan_purpose'] = np.random.choice(
            self.loan_purposes, 
            self.n_samples,
            p=[0.4, 0.25, 0.2, 0.15]
        )
        
        # Existing loans
        existing_loan_prob = (df['business_age_years'] / 30).clip(0, 0.7)
        df['existing_loans'] = np.random.binomial(1, existing_loan_prob).astype(bool)
        
        # Collateral available
        collateral_base_prob = 0.4
        df['collateral_available'] = np.where(
            df['industry_type'] == 'Manufacturing',
            np.random.binomial(1, 0.6, self.n_samples),
            np.random.binomial(1, collateral_base_prob, self.n_samples)
        ).astype(bool)
        
        return df
    
    def generate_credit_labels(self, df):
        """Generate credit decision labels based on realistic business rules"""
        
        # Create scoring components
        compliance_score = (df['gst_compliance_score'] / 100) * 30
        filing_score = (df['gst_filing_months'] / 12) * 20
        age_score = (df['business_age_years'] / 20) * 20
        consistency_score = df['upi_transaction_consistency'] * 15
        
        # Bonus points
        udyam_bonus = np.where(df['udyam_registered'], 10, 0)
        collateral_bonus = np.where(df['collateral_available'], 5, 0)
        
        # Total credit score (0-100)
        credit_score = (
            compliance_score + filing_score + age_score + 
            consistency_score + udyam_bonus + collateral_bonus
        )
        
        # Add randomness
        credit_score = credit_score + np.random.normal(0, 5, self.n_samples)
        credit_score = credit_score.clip(0, 100)
        
        # Decision thresholds
        df['credit_score'] = credit_score.round(2)
        df['credit_label'] = pd.cut(
            credit_score,
            bins=[0, 45, 70, 100],
            labels=['Reject', 'Review', 'Approve']
        )
        
        return df
    
    def generate(self):
        """Main method to generate complete MSME dataset"""
        
        print("🏭 Generating MSME profiles...")
        df = self.generate_msme_profiles()
        
        print("📊 Adding GST features...")
        df = self.add_gst_features(df)
        
        print("💳 Adding UPI transaction features...")
        df = self.add_upi_transaction_features(df)
        
        print("💰 Adding loan features...")
        df = self.add_loan_features(df)
        
        print("✅ Generating credit labels...")
        df = self.generate_credit_labels(df)
        
        print(f"\n✨ Generated {len(df)} MSME records successfully!")
        
        return df


class InvoiceDataGenerator:
    """Generate synthetic invoice data for invoice discounting model"""
    
    def __init__(self, msme_df, n_invoices=3000):
        self.msme_df = msme_df
        self.n_invoices = n_invoices
        self.buyer_types = ['Large Corporate', 'Government', 'SME', 'Retail']
        self.buyer_industries = [
            'Manufacturing', 'Retail', 'IT Services', 'Healthcare', 
            'Government', 'Automotive', 'FMCG', 'Real Estate'
        ]
        
    def generate(self):
        """Generate invoice dataset"""
        
        print("\n📄 Generating invoice records...")
        
        # Random MSME IDs
        msme_ids = np.random.choice(
            self.msme_df['msme_id'].values, 
            self.n_invoices,
            replace=True
        )
        
        data = {
            'invoice_id': [f'INV{str(i).zfill(7)}' for i in range(1, self.n_invoices + 1)],
            'msme_id': msme_ids,
        }
        
        df = pd.DataFrame(data)
        
        # Merge with MSME data
        df = df.merge(
            self.msme_df[['msme_id', 'credit_score', 'industry_type', 'avg_monthly_turnover']], 
            on='msme_id', 
            how='left'
        )
        
        # Invoice amount (10K to 50L)
        df['invoice_amount'] = np.random.uniform(10000, 5000000, self.n_invoices).round(2)
        
        # Buyer type
        df['buyer_type'] = np.random.choice(self.buyer_types, self.n_invoices)
        df['buyer_industry'] = np.random.choice(self.buyer_industries, self.n_invoices)
        
        # Invoice dates (last 6 months)
        start_date = datetime.now() - timedelta(days=180)
        df['invoice_date'] = [
            start_date + timedelta(days=np.random.randint(0, 180)) 
            for _ in range(self.n_invoices)
        ]
        
        # Due date (30/60/90 days)
        payment_terms = np.random.choice([30, 60, 90], self.n_invoices, p=[0.5, 0.3, 0.2])
        df['due_date'] = df['invoice_date'] + pd.to_timedelta(payment_terms, unit='D')
        df['payment_term_days'] = payment_terms
        
        # Historical payment delay
        buyer_delay_map = {}
        for buyer_type in self.buyer_types:
            if buyer_type == 'Government':
                buyer_delay_map[buyer_type] = np.random.randint(30, 90)
            elif buyer_type == 'Large Corporate':
                buyer_delay_map[buyer_type] = np.random.randint(0, 30)
            elif buyer_type == 'SME':
                buyer_delay_map[buyer_type] = np.random.randint(10, 60)
            else:  # Retail
                buyer_delay_map[buyer_type] = np.random.randint(5, 45)
        
        df['historical_payment_delay_days'] = df['buyer_type'].map(
            lambda x: buyer_delay_map[x] + np.random.randint(-10, 20)
        ).clip(0)
        
        # Seller credit score
        df['seller_credit_score'] = df['credit_score']
        
        # Invoice frequency
        invoice_counts = df['msme_id'].value_counts()
        df['invoice_frequency'] = df['msme_id'].map(invoice_counts)
        
        # Generate payment status and risk labels
        df = self._generate_payment_labels(df)
        
        # Clean up
        df = df.drop(['credit_score', 'industry_type', 'avg_monthly_turnover'], axis=1)
        
        print(f"✨ Generated {len(df)} invoice records successfully!")
        
        return df
    
    def _generate_payment_labels(self, df):
        """Generate payment status and risk labels based on features"""
        
        # Risk factors
        seller_risk = (100 - df['seller_credit_score']) / 100
        buyer_delay_risk = (df['historical_payment_delay_days'] / 90).clip(0, 1)
        amount_risk = (df['invoice_amount'] / df['invoice_amount'].max()).clip(0, 1)
        
        buyer_type_risk = df['buyer_type'].map({
            'Large Corporate': 0.2,
            'Government': 0.3,
            'SME': 0.6,
            'Retail': 0.7
        })
        
        # Composite risk score
        risk_score = (
            seller_risk * 0.3 + 
            buyer_delay_risk * 0.3 + 
            buyer_type_risk * 0.25 + 
            amount_risk * 0.15
        )
        
        # Add randomness
        risk_score = risk_score + np.random.normal(0, 0.1, len(df))
        risk_score = risk_score.clip(0, 1)
        
        # Payment status
        payment_outcomes = []
        for risk in risk_score:
            if risk < 0.35:
                outcome = np.random.choice(
                    ['Paid_OnTime', 'Paid_Late', 'Defaulted'],
                    p=[0.85, 0.12, 0.03]
                )
            elif risk < 0.65:
                outcome = np.random.choice(
                    ['Paid_OnTime', 'Paid_Late', 'Defaulted'],
                    p=[0.50, 0.40, 0.10]
                )
            else:
                outcome = np.random.choice(
                    ['Paid_OnTime', 'Paid_Late', 'Defaulted'],
                    p=[0.30, 0.45, 0.25]
                )
            payment_outcomes.append(outcome)
        
        df['payment_status'] = payment_outcomes
        
        # Risk label
        df['risk_label'] = pd.cut(
            risk_score,
            bins=[0, 0.35, 0.65, 1.0],
            labels=['Low', 'Medium', 'High']
        )
        
        df['risk_score'] = (risk_score * 100).round(2)
        
        return df


def main():
    """Main execution function"""
    
    print("=" * 60)
    print("🚀 MSME Credit Scoring - Data Generation Pipeline")
    print("=" * 60)
    
    # Generate MSME data
    msme_generator = MSMEDataGenerator(n_samples=5000)
    msme_df = msme_generator.generate()
    
    # Generate Invoice data
    invoice_generator = InvoiceDataGenerator(msme_df, n_invoices=3000)
    invoice_df = invoice_generator.generate()
    
    # Create output directory
    os.makedirs('data/raw', exist_ok=True)
    
    # Save to CSV
    msme_output_path = 'data/raw/msme_data.csv'
    invoice_output_path = 'data/raw/invoice_data.csv'
    
    msme_df.to_csv(msme_output_path, index=False)
    invoice_df.to_csv(invoice_output_path, index=False)
    
    print("\n" + "=" * 60)
    print("✅ DATA GENERATION COMPLETE!")
    print("=" * 60)
    print(f"\n📁 Files saved:")
    print(f"   • {msme_output_path}")
    print(f"   • {invoice_output_path}")
    
    print(f"\n📊 Summary Statistics:")
    print(f"\n   MSME Data Shape: {msme_df.shape}")
    print(f"   Credit Label Distribution:")
    print(f"   {msme_df['credit_label'].value_counts()}")
    
    print(f"\n   Invoice Data Shape: {invoice_df.shape}")
    print(f"   Payment Status Distribution:")
    print(f"   {invoice_df['payment_status'].value_counts()}")
    
    print(f"\n   Risk Label Distribution:")
    print(f"   {invoice_df['risk_label'].value_counts()}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()