# Datos que Hablan: Bienestar Financiero de Jóvenes Profesionales en América Latina
## Informe Ejecutivo — Futuro Digital LatAm, 2025

### 1. Resumen Ejecutivo

This report analyzes a survey of **500 young professionals** (ages 18–32) across six Latin American countries to inform the design of Futuro Digital LatAm's financial literacy programme. Three findings stand out. First, monthly income varies enormously by country — from a median of **$1,458** in Brazil to just **$798** in Argentina, an 83% gap — meaning a one-size-fits-all curriculum will misjudge relevance in at least some markets. Second, savings behavior is heavily age-dependent: the average savings rate nearly triples, from **5.7% of income** among 18–22 year-olds to **15.5%** among 29–32 year-olds, identifying the first years of a career as the highest-risk window for weak savings habits. Third, housing (28.5% of income) and food (23.8%) together consume over half of the average participant's budget, far outweighing discretionary categories like entertainment (8.7%) — so generic "spend less on fun" advice targets the wrong problem.

Two recommendations follow directly: (1) segment programme content by national income level, prioritizing budgeting and emergency-savings modules in Argentina and Peru and investment/long-term planning modules in Brazil and Chile; and (2) build a dedicated "first savings habits" module for 18–25 year-olds, using small, automated savings goals to compensate for lower relative income before financial routines calcify.

### 2. Metodología

- **Dataset:** Encuesta de Bienestar Financiero 2025
- **Sample:** 500 respondents across 6 countries (Argentina, Brazil, Chile, Colombia, Mexico, Peru), ages 18–32
- **Data collection and processing approach:** The raw survey export (`data/latam_finanzas_2025.csv`, 500 rows × 21 columns) was first profiled for structure, missing values, and category consistency (`scripts/01_explore.py`), then cleaned into an analysis-ready dataset (`data/latam_finanzas_clean.csv`) via `scripts/02_clean.py`. Cross-cutting statistical analyses (income, age, spending, credit card usage, AI tool usage, housing burden) were run in `scripts/03_analysis.py`, per-country profiles were generated via a dedicated country-profiler agent, five summary charts were produced in `scripts/04_visualize.py`, and each finding was interpreted and published to the Notion "Findings Tracker" database.

**Data quality issues found and how they were resolved:**

| Issue | Detail | Resolution |
|---|---|---|
| Inconsistent industry labels | The `industria` field contained **13 raw spelling/casing variants** across 10 real categories (e.g., `"tech"`, `"Tecnologia"`, `"TECNOLOGÍA"`, and `"Tecnología"` all referring to the same industry) | Mapped all variants to a single canonical label per industry (e.g., all four Tecnología variants collapsed into one), preserving all 10 true categories |
| Missing values | `gasto_salud_usd` (healthcare spending) had **33 missing values (6.6%** of rows); all other numeric columns were complete | Filled with the column median to preserve sample size, rather than dropping rows and losing data from every other analysis |
| Negative savings | **74 respondents (14.8%)** had negative `ahorro_mensual_usd`, meaning reported spending exceeded reported income | Kept as valid — overspending is a real and relevant financial-wellness signal, not a data error — and flagged with a new boolean column, `ahorro_negativo`, for downstream analysis. No rows were removed or values altered. |

No rows were dropped at any stage; all 500 respondents are represented in every analysis below.

### 3. Perfil de la Muestra

The sample comprises 500 respondents across six countries, unevenly distributed, with Mexico contributing the largest share:

| Country | Respondents | % of sample |
|---|---:|---:|
| Mexico | 150 | 30.0% |
| Colombia | 80 | 16.0% |
| Argentina | 70 | 14.0% |
| Chile | 70 | 14.0% |
| Brazil | 65 | 13.0% |
| Peru | 65 | 13.0% |

**Age:** Respondents range from 18 to 32 years old (mean **24.96**, median 25), distributed across four age bands with the youngest cohort being the largest:

| Age group | Respondents | % of sample |
|---|---:|---:|
| 18–22 | 162 | 32.4% |
| 23–25 | 123 | 24.6% |
| 26–28 | 87 | 17.4% |
| 29–32 | 128 | 25.6% |

**Industries:** Respondents span 10 industries, led by Finance (**66**, 13.2%), Technology (57, 11.4%), and Engineering (53, 10.6%), down to Retail (41, 8.2%) — a fairly even spread with no single industry dominating the sample.

**Occupations:** The most common roles are Graphic Designer (56), Engineer (55), Community Manager (52), Project Manager (51), Accountant (50), and Financial Analyst (50), reflecting the sample's cross-industry composition rather than concentration in a single professional track.

**Financial profile of the sample:**
- **284 respondents (56.8%)** hold a credit card; 216 (43.2%) do not.
- **362 respondents (72.4%)** hold a savings account; 138 (27.6%) do not.
- **234 respondents (46.8%)** report having debt.
- The most common financial goal is paying off debt (81 respondents), followed by investing in the stock market (75) and saving for retirement (68).
- **74 respondents (14.8%)** report negative monthly savings (spending exceeds income).

### 4. Hallazgos

#### 4.1 Income differences across Latin American countries

Median monthly income varies by nearly two-fold across the six countries in the sample, from **$1,458** in Brazil to **$798** in Argentina, with Chile ($1,246), Mexico ($1,067), Colombia ($857), and Peru ($822) in an intermediate range.

This gap means a uniform financial literacy programme will not be equally relevant in every market: in Argentina and Peru, where median income is lowest, financial-wellness priorities (saving, debt management, essential spending) carry a different weight than in Brazil or Chile. Programme content should be segmented by national income level, prioritizing budgeting and emergency-savings modules for Argentina and Peru, and investment or long-term planning modules for Brazil and Chile. See **Figure 1** (`charts/01_income_by_country.png`).

![Monthly Income Distribution by Country](charts/01_income_by_country.png)

#### 4.2 The relationship between age and savings behavior

The average savings rate rises steadily with age, from **5.7%** of income in the 18–22 age group to **15.5%** in the 29–32 group — nearly tripling across the sampled age range.

This identifies 18–25 year-olds (with rates of 5.7% and 8.3%) as the segment with the weakest saving capacity or habit, likely driven by lower starting income and less experience with financial planning rather than an unwillingness to save. Futuro Digital LatAm should design a dedicated "first savings habits" module for users aged 18–25, built around small, automated savings goals that offset their comparatively lower income. See **Figure 2** (`charts/02_age_vs_savings.png`).

![Age vs. Monthly Savings by Country](charts/02_age_vs_savings.png)

#### 4.3 Where the biggest expense categories are

Across the full sample, housing (**28.5%** of income) and food (**23.8%**) together account for more than half of average monthly spending, while healthcare (4.9%) and education (8.5%) receive the smallest shares — well below transport (10.1%) and entertainment (8.7%).

This matters for programme design because it shows regional households have very little budgetary room left for preventive healthcare or additional financial education once essential housing and food costs are covered. The programme should include a module on optimizing housing and food spending (rent negotiation, smart shopping) to free up budgetary room for health and education. See **Figure 3** (`charts/03_spending_breakdown.png`).

![Average Spending Breakdown by Category](charts/03_spending_breakdown.png)

#### 4.4 How credit card holders differ from non-holders

With nearly identical income (+1.5%), credit card holders spend **17.2% more on entertainment** and **16.1% more on food** than non-holders, while also saving **6.7% more** on average.

This suggests that credit access in the Futuro Digital LatAm population is associated with higher discretionary spending that isn't backed by additional income — a risk pattern especially relevant for young holders who are new to their first card. A "responsible credit use" module should be added to help holders distinguish discretionary, credit-financed spending from their real savings capacity. (Not visualized in the five summary charts; see `scripts/03_analysis.py`, `credit_card_comparison()`.)

#### 4.5 The relationship between AI tool usage and financial satisfaction

There is a strong, statistically significant positive correlation (**r = 0.57, p ≈ 1.2e-44**) between weekly hours of AI tool usage and financial satisfaction, which rises from **2.11** in the low-usage group (0–3 hrs/week, n=150) to **3.53** in the high-usage group (11+ hrs/week, n=15).

This is especially relevant for the low-usage segment, which represents 150 people with both the lowest average income ($776) and the lowest financial satisfaction in the sample — suggesting that low adoption of digital financial-management tools coincides with worse perceived financial wellness. Futuro Digital LatAm should introduce an entry-level AI-tools-for-personal-finance module targeted at the low-usage segment to close this adoption gap, while continuing to monitor the usage–satisfaction relationship longitudinally to rule out reverse causality (higher income driving both greater AI usage and higher satisfaction), given the small size (n=15) of the high-usage group. See **Figure 4** (`charts/04_satisfaction_by_ai_usage.png`).

![Financial Satisfaction by AI Tool Usage](charts/04_satisfaction_by_ai_usage.png)

#### 4.6 Housing burden differences by country

The share of income spent on housing varies markedly by country, from **34.1%** in Argentina and **32.6%** in Chile down to **24.6%** in Peru, with Mexico (28.2%), Brazil (26.9%), and Colombia (25.4%) in between.

This is especially relevant for participants in Argentina and Chile, where a housing burden above 32% of income leaves significantly less room for savings, debt repayment, or emergencies than in a country like Peru. Argentina and Chile should be prioritized for a dedicated housing-cost module (rent renegotiation, shared-housing options), using Peru and Colombia's lower housing burden as a comparative benchmark in educational content. See **Figure 5** (`charts/05_housing_burden_by_country.png`).

![Housing Cost Burden by Country](charts/05_housing_burden_by_country.png)

### 5. Recomendaciones

1. **Segment programme content by national income level, prioritizing Argentina and Peru first.** With median income ranging 83% between Brazil and Argentina (Finding 4.1), prioritize budgeting and emergency-savings modules for Argentina and Peru, and investment or long-term planning modules for Brazil and Chile, rather than a single regional curriculum.

2. **Launch a "first savings habits" module for 18–25 year-olds.** Since the average savings rate nearly triples between the 18–22 and 29–32 age bands (Finding 4.2), prioritize a dedicated module for the youngest cohort built around small, automated savings goals, rather than assuming savings education matters equally across all age groups.

3. **Shift curriculum emphasis from discretionary cuts to housing- and food-cost optimization.** Because housing and food alone consume over half of average income while entertainment accounts for under 9% (Finding 4.3), replace generic "spend less" advice with rent negotiation, shared-housing, and smart-shopping strategies that free up budget for health and education.

4. **Introduce a responsible credit-use module for cardholders.** Credit card holders spend 16–17% more on food and entertainment than non-holders despite near-identical income (Finding 4.4), so a module distinguishing discretionary, credit-financed spending from real savings capacity should be introduced for new and prospective cardholders.

5. **Prioritize Argentina and Chile for a housing-cost module, and offer AI tools as a supplementary resource for low-usage users.** Housing consumes 32–34% of income in these two countries (Finding 4.6), warranting a dedicated module on rent negotiation and shared housing. Separately, since low AI-tool usage coincides with both lower income and lower financial satisfaction (Finding 4.5), introduce an entry-level AI-tools module for the low-usage segment — framed as a complement to core training, not a replacement, and monitored longitudinally given the small high-usage sample (n=15) underlying that correlation.

### 6. Conclusión

This data paints a picture of financial wellness shaped less by individual discipline than by structural cost pressures: income varies nearly two-fold across countries, housing and food absorb over half of the average budget, and the years right after entering the workforce are when savings habits are most fragile. Encouragingly, savings behavior improves substantially with age, and neither credit access nor AI tool adoption appears to undermine financial outcomes — suggesting that targeted, localized interventions in the earliest career years, focused on fixed costs rather than discretionary spending, offer the clearest path to improving financial wellness among young Latin American professionals.
