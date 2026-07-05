"""Clean the LatAm financial wellness survey dataset."""
import pandas as pd

RAW_PATH = "data/latam_finanzas_2025.csv"
CLEAN_PATH = "data/latam_finanzas_clean.csv"

# All observed spelling/casing/abbreviation variants of "industria" values,
# mapped to a single canonical label per industry.
INDUSTRIA_MAP = {
    "Finanzas": "Finanzas",
    "Ingeniería": "Ingeniería",
    "Ventas": "Ventas",
    "Salud": "Salud",
    "Marketing": "Marketing",
    "Tecnología": "Tecnología",
    "Tecnologia": "Tecnología",
    "tech": "Tecnología",
    "TECNOLOGÍA": "Tecnología",
    "Educación": "Educación",
    "Diseño": "Diseño",
    "Recursos Humanos": "Recursos Humanos",
    "Retail": "Retail",
}


def main():
    df = pd.read_csv(RAW_PATH)
    rows_before = len(df)

    print("=" * 80)
    print("1. STANDARDIZE 'industria'")
    print("=" * 80)
    print("Unique values BEFORE:")
    print(sorted(df["industria"].unique()))

    df["industria"] = df["industria"].str.strip().map(INDUSTRIA_MAP).fillna(df["industria"])

    print("\nUnique values AFTER:")
    print(sorted(df["industria"].unique()))

    print("\n" + "=" * 80)
    print("2. MISSING VALUES IN NUMERIC COLUMNS")
    print("=" * 80)
    numeric_cols = df.select_dtypes(include="number").columns
    pct_missing = (df[numeric_cols].isna().mean() * 100).sort_values(ascending=False)
    print(pct_missing.to_string())

    filled_columns = {}
    for col in numeric_cols:
        pct = pct_missing[col]
        if pct == 0:
            continue
        # Under ~10% missing: fill with median to preserve sample size for
        # every other analysis, rather than dropping otherwise-complete rows.
        median_val = df[col].median()
        n_filled = df[col].isna().sum()
        df[col] = df[col].fillna(median_val)
        filled_columns[col] = (n_filled, median_val)
        print(f"\n-> '{col}': {pct:.1f}% missing ({n_filled} rows). "
              f"Filled with median ({median_val:.2f}).")

    print("\n" + "=" * 80)
    print("3. NEGATIVE VALUES IN 'ahorro_mensual_usd'")
    print("=" * 80)
    n_negative = (df["ahorro_mensual_usd"] < 0).sum()
    print(f"Found {n_negative} rows with negative ahorro_mensual_usd (spending > income).")
    print("These are valid and are kept as-is; flagging with 'ahorro_negativo'.")
    df["ahorro_negativo"] = df["ahorro_mensual_usd"] < 0

    df.to_csv(CLEAN_PATH, index=False)
    rows_after = len(df)

    print("\n" + "=" * 80)
    print("4. SUMMARY")
    print("=" * 80)
    print(f"Rows before: {rows_before}")
    print(f"Rows after:  {rows_after}")
    print("Changes made:")
    print(f"  - Standardized 'industria': collapsed "
          f"{len(set(INDUSTRIA_MAP.keys()))} spelling/casing variants into "
          f"{len(set(INDUSTRIA_MAP.values()))} canonical categories.")
    for col, (n_filled, median_val) in filled_columns.items():
        print(f"  - Filled {n_filled} missing values in '{col}' with median "
              f"({median_val:.2f}).")
    print(f"  - Added 'ahorro_negativo' boolean column "
          f"({n_negative} rows flagged True). No rows removed or values altered.")
    print(f"Saved clean dataset to: {CLEAN_PATH}")


if __name__ == "__main__":
    main()
