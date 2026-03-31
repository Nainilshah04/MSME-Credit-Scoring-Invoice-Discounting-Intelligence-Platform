"""
Load CSV data into SQLite database
Loads MSME, Invoice, and Kaggle datasets
"""

import sqlite3
import pandas as pd
import os
from datetime import datetime

class DatabaseLoader:
    """Load CSV data into SQLite database"""
    
    def __init__(self, db_path='data/msme_credit.db'):
        self.db_path = db_path
        self.conn = None
        
    def connect(self):
        """Connect to SQLite database"""
        self.conn = sqlite3.connect(self.db_path)
        print(f"✅ Connected to database: {self.db_path}")
        return self.conn
    
    def create_schema(self):
        """Execute schema.sql to create tables"""
        
        schema_path = 'sql/schema.sql'
        
        if not os.path.exists(schema_path):
            print(f"❌ Error: {schema_path} not found!")
            return False
        
        print(f"📋 Reading schema from {schema_path}...")
        
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        try:
            cursor = self.conn.cursor()
            cursor.executescript(schema_sql)
            self.conn.commit()
            print("✅ Database schema created successfully!")
            return True
        except sqlite3.Error as e:
            print(f"❌ Error creating schema: {e}")
            return False
    
    def load_msme_data(self, csv_path='data/raw/msme_data.csv'):
        """Load MSME data from CSV to database"""
        
        if not os.path.exists(csv_path):
            print(f"❌ Error: {csv_path} not found!")
            return False
        
        print(f"\n📊 Loading MSME data from {csv_path}...")
        
        try:
            # Read CSV
            df = pd.read_csv(csv_path)
            print(f"   Rows in CSV: {len(df)}")
            
            # Convert boolean columns
            bool_columns = ['udyam_registered', 'existing_loans', 'collateral_available']
            for col in bool_columns:
                if col in df.columns:
                    df[col] = df[col].astype(int)
            
            # Load to database
            df.to_sql('msme_profiles', self.conn, if_exists='append', index=False)
            
            print(f"✅ Loaded {len(df)} MSME records successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error loading MSME data: {e}")
            return False
    
    def load_invoice_data(self, csv_path='data/raw/invoice_data.csv'):
        """Load Invoice data from CSV to database"""
        
        if not os.path.exists(csv_path):
            print(f"❌ Error: {csv_path} not found!")
            return False
        
        print(f"\n📄 Loading Invoice data from {csv_path}...")
        
        try:
            # Read CSV
            df = pd.read_csv(csv_path)
            print(f"   Rows in CSV: {len(df)}")
            
            # Convert date columns
            date_columns = ['invoice_date', 'due_date']
            for col in date_columns:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col]).dt.strftime('%Y-%m-%d')
            
            # Load to database
            df.to_sql('invoice_records', self.conn, if_exists='append', index=False)
            
            print(f"✅ Loaded {len(df)} invoice records successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error loading Invoice data: {e}")
            return False
    
    def load_kaggle_data(self, csv_path='data/raw/credit_risk_dataset.csv'):
        """Load Kaggle credit data from CSV to database"""
        
        if not os.path.exists(csv_path):
            print(f"⚠️  Warning: {csv_path} not found! Skipping Kaggle data...")
            return False
        
        print(f"\n🔍 Loading Kaggle data from {csv_path}...")
        
        try:
            # Read CSV
            df = pd.read_csv(csv_path)
            print(f"   Rows in CSV: {len(df)}")
            
            # Load to database
            df.to_sql('kaggle_credit_data', self.conn, if_exists='append', index=False)
            
            print(f"✅ Loaded {len(df)} Kaggle records successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error loading Kaggle data: {e}")
            return False
    
    def verify_data(self):
        """Verify loaded data with statistics"""
        
        print("\n" + "="*60)
        print("📊 DATABASE VERIFICATION")
        print("="*60)
        
        queries = {
            "MSME Profiles": "SELECT COUNT(*) FROM msme_profiles",
            "Invoice Records": "SELECT COUNT(*) FROM invoice_records",
            "Kaggle Data": "SELECT COUNT(*) FROM kaggle_credit_data",
        }
        
        for name, query in queries.items():
            try:
                cursor = self.conn.cursor()
                cursor.execute(query)
                count = cursor.fetchone()[0]
                print(f"✅ {name:20s}: {count:6,} records")
            except sqlite3.Error as e:
                print(f"⚠️  {name:20s}: Table not found or empty")
        
        # Credit label distribution
        print("\n📈 Credit Label Distribution:")
        try:
            df = pd.read_sql_query(
                "SELECT credit_label, COUNT(*) as count FROM msme_profiles GROUP BY credit_label",
                self.conn
            )
            for _, row in df.iterrows():
                print(f"   {row['credit_label']:10s}: {row['count']:5,}")
        except:
            pass
        
        # Payment status distribution
        print("\n💳 Payment Status Distribution:")
        try:
            df = pd.read_sql_query(
                "SELECT payment_status, COUNT(*) as count FROM invoice_records GROUP BY payment_status",
                self.conn
            )
            for _, row in df.iterrows():
                print(f"   {row['payment_status']:15s}: {row['count']:5,}")
        except:
            pass
        
        print("\n" + "="*60)
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("\n✅ Database connection closed")


def main():
    """Main execution function"""
    
    print("="*60)
    print("🚀 MSME CREDIT SCORING - DATABASE LOADER")
    print("="*60)
    
    # Initialize loader
    loader = DatabaseLoader()
    
    # Connect to database
    loader.connect()
    
    # Create schema
    if not loader.create_schema():
        print("❌ Failed to create schema. Exiting...")
        return
    
    # Load data
    loader.load_msme_data()
    loader.load_invoice_data()
    loader.load_kaggle_data()
    
    # Verify
    loader.verify_data()
    
    # Close connection
    loader.close()
    
    print("\n" + "="*60)
    print("✅ DATABASE SETUP COMPLETE!")
    print("="*60)
    print(f"\n📁 Database file: data/msme_credit.db")
    print(f"💡 You can now query the database using SQL or pandas")


if __name__ == "__main__":
    main()