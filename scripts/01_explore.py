"""Initial exploration of the LatAm financial wellness survey dataset."""
import pandas as pd

DATA_PATH = "data/latam_finanzas_2025.csv"

CATEGORICAL_COLUMNS = [
    "pais",
    "industria",
    "ocupacion",
    "meta_financiera",
    "tiene_tarjeta_credito",
    "tiene_cuenta_ahorro",
    "tiene_deuda",
]


def main():
    df = pd.read_csv(DATA_PATH)

    print("=" * 80)
    print("1. SHAPE")
    print("=" * 80)
    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

    print("\n" + "=" * 80)
    print("2. COLUMNS AND DATA TYPES")
    print("=" * 80)
    print(df.dtypes.to_string())

    print("\n" + "=" * 80)
    print("3. MISSING VALUES (sorted, most to least)")
    print("=" * 80)
    missing = df.isna().sum().sort_values(ascending=False)
    print(missing.to_string())

    print("\n" + "=" * 80)
    print("4. BASIC STATISTICS (numeric columns)")
    print("=" * 80)
    numeric_df = df.select_dtypes(include="number")
    stats = numeric_df.agg(["min", "max", "mean", "median", "std"]).T
    print(stats.to_string())

    print("\n" + "=" * 80)
    print("5. CATEGORICAL COLUMN VALUE COUNTS")
    print("=" * 80)
    for col in CATEGORICAL_COLUMNS:
        if col not in df.columns:
            print(f"\n--- {col} --- (column not found)")
            continue
        print(f"\n--- {col} ---")
        print(df[col].value_counts(dropna=False).to_string())


if __name__ == "__main__":
    main()
