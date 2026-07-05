"""
Country profile: Brasil
Analyzes financial wellness survey data for Brasil respondents.
Reads data/latam_finanzas_clean.csv (relative to repo root).
"""

import pandas as pd

df = pd.read_csv("data/latam_finanzas_clean.csv")

country = "Brasil"
sub = df[df["pais"] == country].copy()

# 1. Sample size and age range
n = len(sub)
age_min = sub["edad"].min()
age_max = sub["edad"].max()

# 2. Income stats
income = sub["ingreso_mensual_usd"]
income_median = income.median()
income_mean = income.mean()
income_min = income.min()
income_max = income.max()
income_std = income.std()

# 3. Housing burden: average gasto_vivienda_usd as % of ingreso_mensual_usd
housing_pct = (sub["gasto_vivienda_usd"] / sub["ingreso_mensual_usd"] * 100).mean()

# 4. Spending breakdown: average % of income for each gasto_* column
gasto_cols = [
    "gasto_vivienda_usd",
    "gasto_alimentacion_usd",
    "gasto_transporte_usd",
    "gasto_entretenimiento_usd",
    "gasto_educacion_usd",
    "gasto_salud_usd",
]
spending_pct = {}
for col in gasto_cols:
    spending_pct[col] = (sub[col] / sub["ingreso_mensual_usd"] * 100).mean()

# 5. Savings
ahorro_mean = sub["ahorro_mensual_usd"].mean()
neg_savings_pct = sub["ahorro_negativo"].mean() * 100

# 6. AI tools
ia_hours_mean = sub["horas_herramientas_ia_semana"].mean()
satisfaccion_mean = sub["satisfaccion_financiera"].mean()

# Print results
print(f"Sample size: {n}")
print(f"Age range: {age_min} - {age_max}")
print()
print(f"Income median: {income_median:.2f}")
print(f"Income mean: {income_mean:.2f}")
print(f"Income min: {income_min:.2f}")
print(f"Income max: {income_max:.2f}")
print(f"Income std: {income_std:.2f}")
print()
print(f"Housing burden (% of income): {housing_pct:.2f}")
print()
print("Spending breakdown (% of income):")
for col, val in spending_pct.items():
    print(f"  {col}: {val:.2f}")
print()
print(f"Average monthly savings (USD): {ahorro_mean:.2f}")
print(f"% respondents with negative savings: {neg_savings_pct:.2f}")
print()
print(f"Average AI tool hours/week: {ia_hours_mean:.2f}")
print(f"Average financial satisfaction: {satisfaccion_mean:.2f}")
