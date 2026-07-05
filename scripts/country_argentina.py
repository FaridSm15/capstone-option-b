"""
Country profile: Argentina
Reads the cleaned LATAM financial wellness dataset, filters to Argentina,
and prints summary statistics used to build the executive report section.
"""

import pandas as pd

DATA_PATH = "data/latam_finanzas_clean.csv"
COUNTRY = "Argentina"

GASTO_COLS = [
    "gasto_vivienda_usd",
    "gasto_alimentacion_usd",
    "gasto_transporte_usd",
    "gasto_entretenimiento_usd",
    "gasto_educacion_usd",
    "gasto_salud_usd",
]


def main():
    df = pd.read_csv(DATA_PATH)
    sub = df[df["pais"] == COUNTRY].copy()

    n = len(sub)
    age_min = sub["edad"].min()
    age_max = sub["edad"].max()

    income = sub["ingreso_mensual_usd"]
    income_median = income.median()
    income_mean = income.mean()
    income_min = income.min()
    income_max = income.max()
    income_std = income.std()

    housing_pct_of_income = (sub["gasto_vivienda_usd"] / sub["ingreso_mensual_usd"]) * 100
    housing_avg_pct = housing_pct_of_income.mean()

    spending_pct = {}
    for col in GASTO_COLS:
        pct = (sub[col] / sub["ingreso_mensual_usd"]) * 100
        spending_pct[col] = pct.mean()

    avg_savings = sub["ahorro_mensual_usd"].mean()

    # ahorro_negativo may be boolean or string "True"/"False"
    neg_savings = sub["ahorro_negativo"]
    if neg_savings.dtype == object:
        neg_savings_bool = neg_savings.astype(str).str.strip().str.lower() == "true"
    else:
        neg_savings_bool = neg_savings.astype(bool)
    pct_negative_savings = neg_savings_bool.mean() * 100

    avg_ia_hours = sub["horas_herramientas_ia_semana"].mean()
    avg_satisfaction = sub["satisfaccion_financiera"].mean()

    print(f"Country: {COUNTRY}")
    print(f"Sample size (n): {n}")
    print(f"Age range: {age_min} - {age_max}")
    print()
    print("Income (USD):")
    print(f"  Median: {income_median:.2f}")
    print(f"  Mean: {income_mean:.2f}")
    print(f"  Min: {income_min:.2f}")
    print(f"  Max: {income_max:.2f}")
    print(f"  Std Dev: {income_std:.2f}")
    print()
    print(f"Housing burden (avg gasto_vivienda_usd as % of income): {housing_avg_pct:.2f}%")
    print()
    print("Spending breakdown (avg % of income):")
    for col, val in spending_pct.items():
        print(f"  {col}: {val:.2f}%")
    print()
    print(f"Average monthly savings (ahorro_mensual_usd): {avg_savings:.2f}")
    print(f"% respondents with negative savings: {pct_negative_savings:.2f}%")
    print()
    print(f"Average hours/week using AI tools (horas_herramientas_ia_semana): {avg_ia_hours:.2f}")
    print(f"Average financial satisfaction (satisfaccion_financiera): {avg_satisfaction:.2f}")


if __name__ == "__main__":
    main()
