"""
Country profile: Peru
Filters the cleaned LatAm financial wellness dataset for pais == "Perú"
and prints summary statistics used to build the executive report section.
"""
import pandas as pd

df = pd.read_csv("data/latam_finanzas_clean.csv")

peru = df[df["pais"] == "Perú"].copy()

gasto_cols = [
    "gasto_vivienda_usd",
    "gasto_alimentacion_usd",
    "gasto_transporte_usd",
    "gasto_entretenimiento_usd",
    "gasto_educacion_usd",
    "gasto_salud_usd",
]

print("=== Sample size and age range ===")
print(f"n = {len(peru)}")
print(f"age min = {peru['edad'].min()}, age max = {peru['edad'].max()}")

print("\n=== Income (ingreso_mensual_usd) ===")
print(f"median = {peru['ingreso_mensual_usd'].median():.2f}")
print(f"mean = {peru['ingreso_mensual_usd'].mean():.2f}")
print(f"min = {peru['ingreso_mensual_usd'].min():.2f}")
print(f"max = {peru['ingreso_mensual_usd'].max():.2f}")
print(f"std = {peru['ingreso_mensual_usd'].std():.2f}")

print("\n=== Housing burden ===")
housing_pct = (peru["gasto_vivienda_usd"] / peru["ingreso_mensual_usd"]) * 100
print(f"avg housing % of income = {housing_pct.mean():.2f}")

print("\n=== Spending breakdown (% of income) ===")
for col in gasto_cols:
    pct = (peru[col] / peru["ingreso_mensual_usd"]) * 100
    print(f"{col} = {pct.mean():.2f}")

print("\n=== Savings ===")
print(f"avg ahorro_mensual_usd = {peru['ahorro_mensual_usd'].mean():.2f}")
neg_pct = (peru["ahorro_negativo"].astype(str).str.lower() == "true").mean() * 100
print(f"% ahorro_negativo = {neg_pct:.2f}")

print("\n=== AI tools & satisfaction ===")
print(f"avg horas_herramientas_ia_semana = {peru['horas_herramientas_ia_semana'].mean():.2f}")
print(f"avg satisfaccion_financiera = {peru['satisfaccion_financiera'].mean():.2f}")
