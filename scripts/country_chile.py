"""
Country profile: Chile
Reads the cleaned LatAm financial wellness survey data and computes
summary statistics for respondents in Chile.
"""

import pandas as pd

CLEAN_DATA_PATH = "data/latam_finanzas_clean.csv"
COUNTRY = "Chile"

GASTO_COLS = [
    "gasto_vivienda_usd",
    "gasto_alimentacion_usd",
    "gasto_transporte_usd",
    "gasto_entretenimiento_usd",
    "gasto_educacion_usd",
    "gasto_salud_usd",
]


def main():
    df = pd.read_csv(CLEAN_DATA_PATH)
    country_df = df[df["pais"] == COUNTRY].copy()

    n = len(country_df)
    age_min = country_df["edad"].min()
    age_max = country_df["edad"].max()

    income = country_df["ingreso_mensual_usd"]
    income_median = income.median()
    income_mean = income.mean()
    income_min = income.min()
    income_max = income.max()
    income_std = income.std()

    housing_pct_of_income = (
        country_df["gasto_vivienda_usd"] / country_df["ingreso_mensual_usd"]
    ) * 100
    housing_pct_avg = housing_pct_of_income.mean()

    spending_breakdown = {}
    for col in GASTO_COLS:
        pct = (country_df[col] / country_df["ingreso_mensual_usd"]) * 100
        spending_breakdown[col] = pct.mean()

    savings_avg = country_df["ahorro_mensual_usd"].mean()
    negative_savings_pct = country_df["ahorro_negativo"].mean() * 100

    ai_hours_avg = country_df["horas_herramientas_ia_semana"].mean()
    satisfaction_avg = country_df["satisfaccion_financiera"].mean()

    print(f"## País: {COUNTRY}\n")

    print("### 1. Sample")
    print(f"- Sample size: {n}")
    print(f"- Age range: {age_min}-{age_max}\n")

    print("### 2. Income (USD)")
    print(f"- Median: {income_median:.2f}")
    print(f"- Mean: {income_mean:.2f}")
    print(f"- Min: {income_min:.2f}")
    print(f"- Max: {income_max:.2f}")
    print(f"- Std Dev: {income_std:.2f}\n")

    print("### 3. Housing Burden")
    print(f"- Average housing spend as % of income: {housing_pct_avg:.2f}%\n")

    print("### 4. Spending Breakdown (avg % of income)")
    for col, val in spending_breakdown.items():
        print(f"- {col}: {val:.2f}%")
    print()

    print("### 5. Savings")
    print(f"- Average monthly savings (USD): {savings_avg:.2f}")
    print(f"- % of respondents with negative savings: {negative_savings_pct:.2f}%\n")

    print("### 6. AI Tools & Satisfaction")
    print(f"- Average hours/week using AI tools: {ai_hours_avg:.2f}")
    print(f"- Average financial satisfaction: {satisfaction_avg:.2f}")


if __name__ == "__main__":
    main()
