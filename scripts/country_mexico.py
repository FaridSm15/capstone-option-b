"""
Country profile script: Mexico
Filters the cleaned LatAm financial wellness survey data for pais == "Mexico"
(with accent) and computes summary statistics used in the executive report.
"""
import pandas as pd

CLEAN_DATA_PATH = "data/latam_finanzas_clean.csv"

def main():
    df = pd.read_csv(CLEAN_DATA_PATH, encoding="utf-8")

    country = "México"  # Mexico
    df_mx = df[df["pais"] == country].copy()

    # 1. Sample size and age range
    n = len(df_mx)
    age_min = df_mx["edad"].min()
    age_max = df_mx["edad"].max()

    # 2. Income stats (USD)
    income = df_mx["ingreso_mensual_usd"]
    income_median = income.median()
    income_mean = income.mean()
    income_min = income.min()
    income_max = income.max()
    income_std = income.std()

    # 3. Housing burden: avg gasto_vivienda_usd as % of ingreso_mensual_usd
    housing_pct_per_row = df_mx["gasto_vivienda_usd"] / df_mx["ingreso_mensual_usd"] * 100
    housing_pct_avg = housing_pct_per_row.mean()

    # 4. Spending breakdown: avg % of income for each gasto_* column
    gasto_cols = [
        "gasto_vivienda_usd",
        "gasto_alimentacion_usd",
        "gasto_transporte_usd",
        "gasto_entretenimiento_usd",
        "gasto_educacion_usd",
        "gasto_salud_usd",
    ]
    spending_breakdown = {}
    for col in gasto_cols:
        pct_per_row = df_mx[col] / df_mx["ingreso_mensual_usd"] * 100
        spending_breakdown[col] = pct_per_row.mean()

    # 5. Savings
    ahorro_mean = df_mx["ahorro_mensual_usd"].mean()
    pct_negative_savings = df_mx["ahorro_negativo"].mean() * 100

    # 6. AI tools & satisfaction
    ia_hours_avg = df_mx["horas_herramientas_ia_semana"].mean()
    satisfaction_avg = df_mx["satisfaccion_financiera"].mean()

    # Print results
    print("=== Country Profile: Mexico ===")
    print(f"Sample size: {n}")
    print(f"Age range: {age_min} - {age_max}")
    print()
    print("Income (USD):")
    print(f"  Median: {income_median:.2f}")
    print(f"  Mean: {income_mean:.2f}")
    print(f"  Min: {income_min:.2f}")
    print(f"  Max: {income_max:.2f}")
    print(f"  Std Dev: {income_std:.2f}")
    print()
    print(f"Housing burden (avg gasto_vivienda as % of income): {housing_pct_avg:.2f}%")
    print()
    print("Spending breakdown (avg % of income):")
    for col, val in spending_breakdown.items():
        print(f"  {col}: {val:.2f}%")
    print()
    print(f"Avg monthly savings (USD): {ahorro_mean:.2f}")
    print(f"% respondents with negative savings: {pct_negative_savings:.2f}%")
    print()
    print(f"Avg hours/week using AI tools: {ia_hours_avg:.2f}")
    print(f"Avg financial satisfaction: {satisfaction_avg:.2f}")


if __name__ == "__main__":
    main()
