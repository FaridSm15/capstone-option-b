"""
Country profile: Colombia
Analyzes data/latam_finanzas_clean.csv filtered to pais == "Colombia"
and prints a Markdown section with summary statistics.
"""

import pandas as pd

DATA_PATH = "data/latam_finanzas_clean.csv"
COUNTRY = "Colombia"

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
    country_df = df[df["pais"] == COUNTRY].copy()

    # 1. Sample size and age range
    n = len(country_df)
    age_min = country_df["edad"].min()
    age_max = country_df["edad"].max()

    # 2. Income stats
    income = country_df["ingreso_mensual_usd"]
    income_median = income.median()
    income_mean = income.mean()
    income_min = income.min()
    income_max = income.max()
    income_std = income.std()

    # 3. Housing burden: gasto_vivienda_usd as % of ingreso_mensual_usd
    housing_pct = (country_df["gasto_vivienda_usd"] / country_df["ingreso_mensual_usd"]) * 100
    housing_pct_avg = housing_pct.mean()

    # 4. Spending breakdown: average % of income for each gasto_* column
    spending_breakdown = {}
    for col in GASTO_COLS:
        pct = (country_df[col] / country_df["ingreso_mensual_usd"]) * 100
        spending_breakdown[col] = pct.mean()

    # 5. Savings
    ahorro_mean = country_df["ahorro_mensual_usd"].mean()
    pct_negative_savings = country_df["ahorro_negativo"].mean() * 100

    # 6. AI tools & satisfaction
    ia_hours_avg = country_df["horas_herramientas_ia_semana"].mean()
    satisfaccion_avg = country_df["satisfaccion_financiera"].mean()

    # ---- Build Markdown output ----
    lines = []
    lines.append(f"## País: {COUNTRY}")
    lines.append("")
    lines.append(f"**Sample size:** {n} respondents | **Age range:** {age_min}–{age_max} years")
    lines.append("")
    lines.append("**Income (USD, monthly):**")
    lines.append(f"- Median: ${income_median:.2f}")
    lines.append(f"- Mean: ${income_mean:.2f}")
    lines.append(f"- Min: ${income_min:.2f}")
    lines.append(f"- Max: ${income_max:.2f}")
    lines.append(f"- Standard deviation: ${income_std:.2f}")
    lines.append("")
    lines.append(f"**Housing burden:** Housing expenses average {housing_pct_avg:.2f}% of monthly income.")
    lines.append("")
    lines.append("**Spending breakdown (average % of monthly income):**")
    label_map = {
        "gasto_vivienda_usd": "Housing",
        "gasto_alimentacion_usd": "Food",
        "gasto_transporte_usd": "Transportation",
        "gasto_entretenimiento_usd": "Entertainment",
        "gasto_educacion_usd": "Education",
        "gasto_salud_usd": "Health",
    }
    for col in GASTO_COLS:
        lines.append(f"- {label_map[col]}: {spending_breakdown[col]:.2f}%")
    lines.append("")
    lines.append("**Savings:**")
    lines.append(f"- Average monthly savings: ${ahorro_mean:.2f}")
    lines.append(f"- Respondents with negative savings: {pct_negative_savings:.2f}%")
    lines.append("")
    lines.append("**AI tools & financial satisfaction:**")
    lines.append(f"- Average hours/week using AI financial tools: {ia_hours_avg:.2f}")
    lines.append(f"- Average financial satisfaction score: {satisfaccion_avg:.2f}")

    output = "\n".join(lines)
    print(output)


if __name__ == "__main__":
    main()
