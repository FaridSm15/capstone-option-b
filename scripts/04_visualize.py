"""Generate the 5 executive-report charts from the clean LatAm finance dataset."""

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import pandas as pd

SOURCE_NOTE = "Source: Encuesta de Bienestar Financiero LatAm 2025, Futuro Digital LatAm"

# Reference palette (dataviz skill) -----------------------------------------
INK_PRIMARY = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#898781"
GRIDLINE = "#e1e0d9"
BASELINE = "#c3c2b7"
SURFACE = "#fcfcfb"

COUNTRY_COLORS = {
    "Argentina": "#2a78d6",  # blue
    "Brasil": "#1baf7a",     # aqua
    "Chile": "#eda100",      # yellow
    "Colombia": "#008300",   # green
    "México": "#4a3aa7",     # violet
    "Perú": "#e34948",       # red
}

STATUS_GOOD = "#0ca30c"
STATUS_CRITICAL = "#d03b3b"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Segoe UI", "DejaVu Sans", "Arial"],
    "axes.edgecolor": BASELINE,
    "axes.labelcolor": INK_SECONDARY,
    "text.color": INK_PRIMARY,
    "xtick.color": INK_MUTED,
    "ytick.color": INK_MUTED,
    "axes.grid": True,
    "grid.color": GRIDLINE,
    "grid.linewidth": 0.8,
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
})


def add_source_note(fig):
    fig.text(0.01, 0.01, SOURCE_NOTE, fontsize=8, color=INK_MUTED, ha="left")


def style_axes(ax):
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color(BASELINE)
    ax.tick_params(length=0)


df = pd.read_csv("data/latam_finanzas_clean.csv")

# ----------------------------------------------------------------------------
# Chart 1: Income distribution by country (horizontal box plot, sorted by median)
# ----------------------------------------------------------------------------
order = (
    df.groupby("pais")["ingreso_mensual_usd"]
    .median()
    .sort_values(ascending=True)  # ascending so highest ends up on top after boxplot draw order
    .index.tolist()
)

fig, ax = plt.subplots(figsize=(9, 5.5))
data = [df.loc[df["pais"] == c, "ingreso_mensual_usd"] for c in order]
box = ax.boxplot(
    data,
    orientation="horizontal",
    patch_artist=True,
    tick_labels=order,
    widths=0.6,
    medianprops={"color": INK_PRIMARY, "linewidth": 1.5},
    whiskerprops={"color": BASELINE},
    capprops={"color": BASELINE},
    flierprops={"markeredgecolor": INK_MUTED, "markersize": 4},
)
for patch, country in zip(box["boxes"], order):
    patch.set_facecolor(COUNTRY_COLORS[country])
    patch.set_alpha(0.75)
    patch.set_edgecolor(COUNTRY_COLORS[country])

ax.set_xlabel("Monthly income (USD)")
ax.set_ylabel("Country")
ax.set_title("Monthly Income Distribution by Country", fontsize=14, fontweight="bold", pad=14)
style_axes(ax)
ax.grid(axis="x")
ax.grid(axis="y", visible=False)
add_source_note(fig)
fig.tight_layout(rect=(0, 0.04, 1, 1))
fig.savefig("charts/01_income_by_country.png", dpi=200)
plt.close(fig)

# ----------------------------------------------------------------------------
# Chart 2: Age vs. monthly savings scatter, colored by country, with trend line
# ----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 6))
for country, color in COUNTRY_COLORS.items():
    sub = df[df["pais"] == country]
    ax.scatter(
        sub["edad"], sub["ahorro_mensual_usd"],
        s=28, color=color, alpha=0.75, edgecolor="none", label=country,
    )

slope, intercept = np.polyfit(df["edad"], df["ahorro_mensual_usd"], 1)
x_line = np.array([df["edad"].min(), df["edad"].max()])
ax.plot(x_line, slope * x_line + intercept, color=INK_PRIMARY, linewidth=2, linestyle="--", label="Trend (linear fit)")

ax.set_xlabel("Age (years)")
ax.set_ylabel("Monthly savings (USD)")
ax.set_title("Age vs. Monthly Savings by Country", fontsize=14, fontweight="bold", pad=14)
style_axes(ax)
ax.legend(frameon=False, fontsize=9, loc="upper left", bbox_to_anchor=(1.01, 1.0))
add_source_note(fig)
fig.tight_layout(rect=(0, 0.04, 0.86, 1))
fig.savefig("charts/02_age_vs_savings.png", dpi=200)
plt.close(fig)

# ----------------------------------------------------------------------------
# Chart 3: Average spending breakdown by category (% of income)
# ----------------------------------------------------------------------------
categories = {
    "gasto_vivienda_usd": "Housing",
    "gasto_alimentacion_usd": "Food",
    "gasto_transporte_usd": "Transport",
    "gasto_entretenimiento_usd": "Entertainment",
    "gasto_educacion_usd": "Education",
    "gasto_salud_usd": "Health",
}
pct = pd.DataFrame({
    label: df[col] / df["ingreso_mensual_usd"] * 100
    for col, label in categories.items()
})
avg_pct = pct.mean().sort_values(ascending=True)  # ascending for barh so highest is on top

fig, ax = plt.subplots(figsize=(9, 5.5))
ax.barh(avg_pct.index, avg_pct.values, color="#2a78d6", height=0.6)
for i, v in enumerate(avg_pct.values):
    ax.text(v + 0.3, i, f"{v:.1f}%", va="center", fontsize=9, color=INK_SECONDARY)

ax.set_xlabel("Average share of monthly income (%)")
ax.set_ylabel("Expense category")
ax.set_title("Average Spending Breakdown by Category", fontsize=14, fontweight="bold", pad=14)
style_axes(ax)
ax.grid(axis="y", visible=False)
add_source_note(fig)
fig.tight_layout(rect=(0, 0.04, 1, 1))
fig.savefig("charts/03_spending_breakdown.png", dpi=200)
plt.close(fig)

# ----------------------------------------------------------------------------
# Chart 4: Financial satisfaction by AI tool usage tier (tercile bins)
# ----------------------------------------------------------------------------
tier_labels = ["Low", "Medium", "High"]
df["ai_usage_tier"] = pd.qcut(df["horas_herramientas_ia_semana"], q=3, labels=tier_labels)
tier_means = df.groupby("ai_usage_tier", observed=True)["satisfaccion_financiera"].mean().reindex(tier_labels)

tier_colors = {"Low": "#86b6ef", "Medium": "#2a78d6", "High": "#104281"}  # sequential blue ramp (light -> dark)

fig, ax = plt.subplots(figsize=(7.5, 5.5))
bars = ax.bar(tier_means.index, tier_means.values, color=[tier_colors[t] for t in tier_labels], width=0.55)
for bar, v in zip(bars, tier_means.values):
    ax.text(bar.get_x() + bar.get_width() / 2, v + 0.03, f"{v:.2f}", ha="center", fontsize=10, color=INK_SECONDARY)

ax.set_xlabel("AI tool usage (weekly hours, tercile)")
ax.set_ylabel("Average financial satisfaction score")
ax.set_title("Financial Satisfaction by AI Tool Usage", fontsize=14, fontweight="bold", pad=14)
ax.set_ylim(0, tier_means.max() * 1.25)
style_axes(ax)
ax.grid(axis="x", visible=False)
add_source_note(fig)
fig.tight_layout(rect=(0, 0.04, 1, 1))
fig.savefig("charts/04_satisfaction_by_ai_usage.png", dpi=200)
plt.close(fig)

# ----------------------------------------------------------------------------
# Chart 5: Housing burden by country (% of income spent on housing)
# ----------------------------------------------------------------------------
df["housing_pct"] = df["gasto_vivienda_usd"] / df["ingreso_mensual_usd"] * 100
burden = df.groupby("pais")["housing_pct"].mean().sort_values(ascending=False)

cmap = LinearSegmentedColormap.from_list("burden", [STATUS_GOOD, "#fab219", STATUS_CRITICAL])
norm = plt.Normalize(burden.values.min(), burden.values.max())
colors = [cmap(norm(v)) for v in burden.values]

fig, ax = plt.subplots(figsize=(9, 5.5))
ax.barh(burden.index[::-1], burden.values[::-1], color=colors[::-1], height=0.6)
for i, v in enumerate(burden.values[::-1]):
    ax.text(v + 0.3, i, f"{v:.1f}%", va="center", fontsize=9, color=INK_SECONDARY)

ax.set_xlabel("Average housing cost (% of monthly income)")
ax.set_ylabel("Country")
ax.set_title("Housing Cost Burden by Country", fontsize=14, fontweight="bold", pad=14)
style_axes(ax)
ax.grid(axis="y", visible=False)
add_source_note(fig)
fig.tight_layout(rect=(0, 0.04, 1, 1))
fig.savefig("charts/05_housing_burden_by_country.png", dpi=200)
plt.close(fig)

print("All 5 charts saved to charts/")
