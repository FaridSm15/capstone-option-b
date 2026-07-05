"""
Analysis script: cross-cutting analyses over the full cleaned sample.
Covers: age vs. savings, spending breakdown, credit card holders vs.
non-holders, and AI tool usage vs. financial satisfaction.
"""
import pandas as pd
from scipy import stats

CLEAN_DATA_PATH = "data/latam_finanzas_clean.csv"

# Country profile figures (scripts/country_profiles.md) for analyses 1 and 6
INCOME_BY_COUNTRY = {
    "Brazil": {"median": 1458.03, "mean": 1387.97, "min": 300.00, "max": 2874.49, "std": 592.18},
    "Chile": {"median": 1246.01, "mean": 1245.29, "min": 575.20, "max": 1861.10, "std": 289.66},
    "Mexico": {"median": 1066.99, "mean": 1042.05, "min": 300.00, "max": 1693.16, "std": 286.61},
    "Colombia": {"median": 856.62, "mean": 848.78, "min": 405.15, "max": 1362.79, "std": 188.70},
    "Peru": {"median": 821.59, "mean": 817.76, "min": 361.89, "max": 1341.50, "std": 207.91},
    "Argentina": {"median": 798.49, "mean": 766.38, "min": 372.85, "max": 1342.56, "std": 203.94},
}

HOUSING_BURDEN_BY_COUNTRY = {
    "Argentina": 34.09,
    "Chile": 32.55,
    "Mexico": 28.15,
    "Brazil": 26.90,
    "Colombia": 25.41,
    "Peru": 24.63,
}


def age_vs_savings(df):
    bins = [18, 23, 26, 29, 33]
    labels = ["18-22", "23-25", "26-28", "29-32"]
    df = df.copy()
    df["age_group"] = pd.cut(df["edad"], bins=bins, labels=labels, right=False)

    df["savings_rate"] = df["ahorro_mensual_usd"] / df["ingreso_mensual_usd"] * 100

    result = df.groupby("age_group", observed=True).agg(
        avg_monthly_savings=("ahorro_mensual_usd", "mean"),
        avg_savings_rate=("savings_rate", "mean"),
    )
    return result.reindex(labels)


def spending_breakdown(df):
    gasto_cols = {
        "gasto_vivienda_usd": "Housing",
        "gasto_alimentacion_usd": "Food",
        "gasto_transporte_usd": "Transport",
        "gasto_entretenimiento_usd": "Entertainment",
        "gasto_educacion_usd": "Education",
        "gasto_salud_usd": "Healthcare",
    }
    rows = {}
    for col, label in gasto_cols.items():
        rows[label] = (df[col] / df["ingreso_mensual_usd"] * 100).mean()
    result = pd.Series(rows, name="avg_pct_of_income").sort_values(ascending=False)
    return result


def credit_card_comparison(df):
    metrics = {
        "avg_income": "ingreso_mensual_usd",
        "avg_food_spending": "gasto_alimentacion_usd",
        "avg_entertainment_spending": "gasto_entretenimiento_usd",
        "avg_savings": "ahorro_mensual_usd",
    }
    holders = df[df["tiene_tarjeta_credito"] == "Sí"]
    non_holders = df[df["tiene_tarjeta_credito"] == "No"]

    rows = []
    for label, col in metrics.items():
        h = holders[col].mean()
        nh = non_holders[col].mean()
        pct_diff = (h - nh) / nh * 100
        rows.append({"metric": label, "holders": h, "non_holders": nh, "pct_diff": pct_diff})
    return pd.DataFrame(rows).set_index("metric")


def ai_usage_vs_satisfaction(df):
    bins = [0, 4, 11, df["horas_herramientas_ia_semana"].max() + 1]
    labels = ["Low (0-3 hrs/week)", "Medium (4-10 hrs/week)", "High (11+ hrs/week)"]
    df = df.copy()
    df["ia_usage_group"] = pd.cut(
        df["horas_herramientas_ia_semana"], bins=bins, labels=labels, right=False
    )
    result = df.groupby("ia_usage_group", observed=True).agg(
        n=("satisfaccion_financiera", "size"),
        avg_satisfaction=("satisfaccion_financiera", "mean"),
        avg_income=("ingreso_mensual_usd", "mean"),
    )
    return result.reindex(labels)


def ai_usage_satisfaction_correlation(df):
    r, p = stats.pearsonr(df["horas_herramientas_ia_semana"], df["satisfaccion_financiera"])
    return r, p


def income_by_country():
    result = pd.DataFrame(INCOME_BY_COUNTRY).T
    result = result[["median", "mean", "min", "max", "std"]]
    return result.sort_values("median", ascending=False)


def housing_burden_by_country():
    result = pd.Series(HOUSING_BURDEN_BY_COUNTRY, name="avg_housing_pct_of_income")
    return result.sort_values(ascending=False)


def main():
    df = pd.read_csv(CLEAN_DATA_PATH, encoding="utf-8")

    print("=== 1. Income by Country ===")
    print(income_by_country().round(2))
    print()

    print("=== 2. Age vs. Savings ===")
    print(age_vs_savings(df).round(2))
    print()

    print("=== 3. Spending Breakdown (full sample) ===")
    print(spending_breakdown(df).round(2))
    print()

    print("=== 4. Credit Card Holders vs. Non-Holders ===")
    print(credit_card_comparison(df).round(2))
    print()

    print("=== 5. AI Tool Usage vs. Financial Satisfaction ===")
    print(ai_usage_vs_satisfaction(df).round(2))
    print()
    r, p = ai_usage_satisfaction_correlation(df)
    print(f"Pearson correlation (hours/week AI use vs. financial satisfaction): r = {r:.4f}, p = {p:.6g}")
    print()

    print("=== 6. Housing Burden by Country ===")
    print(housing_burden_by_country().round(2))


if __name__ == "__main__":
    main()
