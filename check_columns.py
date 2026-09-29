import pandas as pd
import os

files = ['Sales.csv', 'Product.csv', 'Region.csv', 'Reseller.csv', 'Salesperson.csv', 'Targets.csv']

for file in files:
    if os.path.exists(file):
        print(f"\n🔍 Checking: {file}")
        # Try different separators to find the one that works
        for sep in [',', ';', '\t']:
            try:
                # Read just the first 2 rows to check the structure
                df = pd.read_csv(file, sep=sep, nrows=2)
                print(f"   ✅ Delimiter: '{sep}'")
                print(f"   📋 Columns: {list(df.columns)}")
                break # Stop trying once we find the right separator
            except Exception:
                continue
    else:
        print(f"\n❌ File not found: {file}")

print("\n✅ Done! Copy the output above and paste it here.")