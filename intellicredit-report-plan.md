# IntelliCredit — Capstone Final Report Plan
### Business Analytics (23CSE452) · Units 1, 2 & 3

> **Modelled on:** *IndieGuard: Indie Game Launch Analytics* capstone format (15-page report).  
> **Our project:** IntelliCredit — Alternative credit scoring & risk analytics for thin-file / gig-economy borrowers.

---

## Document Structure (mirror of the reference report)

```
Cover Page
Declaration & Acknowledgement          (½ page)
Abstract                               (1 page)
Executive Summary                      (1 page)
Table of Contents
List of Figures / List of Tables
Abbreviations
─────────────────────────────────────────────────
1. Introduction, Business Objectives & Literature Review    (1.5 pages)
2. Dataset Description, Validation & Preparation            (1.5 pages)
3. Exploratory Data Analysis & Visualisation (Unit 1)       (1 page)
4. Feature Engineering & Predictive Modelling (Unit 2)      (2 pages)
5. Advanced Analytics (Unit 3): Two Selected Methods        (2 pages)
   5.1 Method 1 — Time-Series Forecasting (SARIMAX)
   5.2 Method 2 — Association Rule Mining (Apriori/FP-Growth)
6. Combined Business Insights & Impact Scenarios            (1 page)
7. Interactive Dashboard, Figure Index & Reproducibility    (0.5 page)
8. Reflections & Limitations                                (0.5 page)
References                                                  (0.5 page)
─────────────────────────────────────────────────
Appendix A. Additional Figures
Appendix B. Model Comparison Tables (full)
Appendix C. Implementation Details & Dashboard User Guide
Appendix D. Project Board, Contributions & AI Declaration
```

---

## Section-by-Section Plan

---

### Cover Page
| Field | Content |
|---|---|
| Report title | CAPSTONE PROJECT: FINAL REPORT |
| Project name | **IntelliCredit: Alternative Credit Scoring & Risk Analytics Engine** |
| Subtitle | *Predicting default risk, detecting delinquency patterns, and forecasting portfolio losses for India's thin-file and gig-economy borrowers* |
| Course | 23CSE452 Business Analytics (Units 1, 2 and 3) |
| Programme / section | [fill] |
| Team number | [fill] |
| Guide | [fill] |
| Academic year | 2026–2027 |
| Repository | github.com/Goldmauler/intellicredit-review2 |
| Dashboard | streamlit run dashboard/app.py |
| Team members | Darun R G · goldmauler · Abhinav Juturu · Gowtham Reddy · Adithya |

---

### Declaration & Acknowledgement
- Standard originality declaration, AI-use disclosure pointer to Appendix D (Table — Tools, Tasks, Content, Verification)
- Acknowledgement of guide and faculty

---

### Abstract (~250 words)

**What to cover:**

1. **Context** — Over 1.4 billion thin-file individuals and gig-economy workers in India lack traditional CIBIL scores; lenders either exclude them or lend blind.
2. **Data** — 30,000 synthetic borrower profiles + 360,000 monthly transactions (programmatically generated, validated against real Indian benchmarks: MFIN Micrometer, PLFS, CGAP, NPCI) + live macroeconomic series from FRED and World Bank APIs.
3. **What we did** — Unit 1 & 2: data cleaning (8 rules), EDA (38 charts, hypothesis tests), feature engineering (14 derived features, WoE/IV, PCA, SMOTE), and four model families with grid-search tuning; Unit 3 Method 1: SARIMAX with live macro drivers; Method 3 Method 2: Apriori / FP-Growth delinquency pattern mining.
4. **Main results** — Best model (Calibrated LightGBM): test AUC-ROC 0.741; top-decile defaults at 23% (2.9× lift). SARIMAX hold-out MAE 0.054 pp; every macro driver is significant with expected sign. 93 validated delinquency warning rules, all holding on unseen borrowers.
5. **Application** — A 5-tab Streamlit underwriter dashboard integrating all three units.
6. **Limitation** — Borrowers and transactions are synthetic; all results are associations in observational data.

---

### Executive Summary (~400 words)

**Structure (follow IndieGuard's bullets + recommendation format):**

**Opening:** Lenders serving gig workers have no CIBIL score to fall back on. We ask: who is likely to default, which behavioural combinations signal delinquency, and when will portfolio defaults rise? We built our own dataset, checked every result on a held-out 20% test set, and deployed a unified decision dashboard.

**Key findings (bullet-point style like the reference):**

- 🔴 **Gig tenure and income trend dominate default risk.** A borrower with <6 months on a platform is 3.1× more likely to default than one with 3+ years, even at the same income level.
- 🔴 **Delinquency patterns cluster together.** 93 validated rules, all holding on unseen borrowers. The top rule (declining income + volatile income + low savings buffer) predicts a 24.7% default rate (3.1× lift).
- 🔴 **Rules add information the PD model misses.** Within the same lowest-risk PD band, applicants with 6+ triggered rules default 3× more (5.6% vs 1.8%).
- 🟡 **Macro shocks dramatically change approvals.** Under the same break-even rule, approval rates move from 75% (benign 2025) to 48% (severe macro stress).
- 🟢 **The model is well-calibrated.** Mean predicted PD 7.8% vs observed 7.9% on 6,000 test borrowers.

**Recommendations (numbered, as in IndieGuard):** Provide 4–5 concrete actions for a lender to test, in priority order.

**Dashboard pointer:** "The live dashboard (streamlit run dashboard/app.py) integrates all three units and lets an underwriter score an applicant, explore the portfolio outlook, and browse the delinquency warning rules."

---

### 1. Introduction, Business Objectives & Literature Review (1.5 pages)

#### 1.1 Context and Scope
- India's gig economy (~77 million workers, PLFS 2022–23); thin-file problem
- Four research questions mapped to Units 1, 2, 3 (reproduce the README table)
- Scope: 30,000 borrowers, 12-month behavioural window, 72-month portfolio simulation, INR micro-loans of ₹5,000–₹3,00,000
- Out of scope: real borrower PII, live loan book, causal claims

#### 1.2 Related Analytics Work & Research Gap
Cite 4–6 papers and state the gap honestly:

| Prior study | Method | Dataset | Gap filled by us |
|---|---|---|---|
| Berg et al. (2020) | ML on digital footprints | German fintech | India gig-economy + alternative behavioural signals |
| Agarwal et al. (2020) | Alt-data credit India | Real Indian borrowers | Integrates time-series and ARM; full pipeline |
| Björkegren & Grissen (2020) | Mobile phone + repayment | Rwanda, Haiti | India-specific: UPI, BNPL, recharge signals |
| Lessmann et al. (2015) | Credit scoring benchmark | UCI / benchmark sets | Combines ARM warning patterns with PD model |
| MFIN Micrometer (2026) | Industry report | Real India NBFC | Validates our synthetic statistics |

**Gap:** No end-to-end open pipeline combining interpretable PD + ARM warning patterns + macro-scenario portfolio forecasting for Indian gig workers with a live underwriter dashboard.

---

### 2. Dataset Description, Validation & Preparation (1.5 pages)

#### 2.1 Provenance, Coverage and Challenges

| Dataset | Rows | Source | Generated by |
|---|---|---|---|
| `borrower_profiles.csv` | 30,000 | Synthetic (NumPy + Faker en_IN + logistic label) | `data_generation.py` |
| `monthly_transactions.csv` | 360,000 | Synthetic (12 months per borrower) | `data_generation.py` |
| `macro_india_monthly.csv` | 108 months (2016–2024) | **Live APIs** — FRED + World Bank | `src/macro_api.py` |
| `portfolio/portfolio_monthly.csv` | 72 months × 30k loans | Macro-driven simulation | `src/portfolio_simulation.py` |

**Challenges:** Class imbalance (7.87% default rate; always-negative baseline scores 92% accuracy), annual World Bank series interpolated to monthly, CPI on FRED carried forward past March 2025.

**Validation against real-world benchmarks (key differentiator):**

| Synthetic statistic | Our value | Real benchmark | Source |
|---|---|---|---|
| Default rate | 7.87% | 6.9–8.5% (MFI borrowers) | MFIN Micrometer Q1 FY27 |
| Avg monthly income | ₹28,400 | ₹26,000–31,000 | PLFS 2022–23 |
| UPI transactions/month | 20 median | 18.4 average | NPCI Annual Report 2023 |
| Utility delay 15+ days (high-risk) | 22% | 18–25% | CGAP India survey |

#### 2.2 Data Quality, Privacy & Ethics
- 8 cleaning rules (documented in notebook 01): missing value imputation (median / mode), IQR winsorisation, ordinal encoding via `src/config.ORDINAL_MAPS`
- No real borrower PII; borrower names from Faker are pseudonymous and never stored in model features
- Synthetic data means no DPDPA consent obligation; explicitly stated

**Known biases:** Urban-skewed platform distribution; loan amounts may not reflect full NBFC range; World Bank annual series have interpolation error.

#### 2.3 Transformations and Usable Dataset
- 80/20 stratified split (seed 42), 5 CV folds inside training
- 14 engineered features (from notebook 03): `income_volatility_index`, `debt_to_inflow_ratio`, `savings_buffer_ratio`, `loan_to_income`, `repayment_ratio`, `utility_reliability_score`, `income_trend_slope`, ordinal encodings
- SMOTE applied **inside** each training fold only (no leakage)
- 21 automated leakage checks pass (reference in Appendix C)

> [!IMPORTANT]
> Map each key field to the unit it feeds — reproduce as a table (like Table 3 in IndieGuard).

**Table X. Mapping of key fields to units and methods.**

| Variable | Type | Preparation | Used in |
|---|---|---|---|
| `loan_default_status` | binary target | Stratified split; never a feature | U2, U3 M2 |
| `avg_monthly_income` | continuous | Winsorised; `income_volatility_index` derived | U1, U2, U3 |
| `utility_on_time_count` | count (0–12) | `utility_reliability_score = /12` | U1, U2, U3 M2 |
| `avg_bnpl_monthly_amount` | continuous | `debt_to_inflow_ratio` derived | U1, U2, U3 M2 |
| `gig_tenure_months` | continuous | Ordinal grouping for EDA | U1, U2, U3 M2 |
| `portfolio_monthly.csv` | panel | Macro-driven hazard model output | U3 M1 |
| `macro_india_monthly.csv` | time series | FRED/World Bank; COVID dummy | U3 M1 |

---

### 3. Exploratory Data Analysis & Visualisation — Unit 1 (1 page)

**Guiding questions (map to your 4 research questions):**

- Q1: Who defaults? (demographics, platform, education, location)
- Q2: Which behavioural signals co-vary with default?
- Q3: Does macro environment correlate with portfolio default rate?
- Q4: Are warning flags clustered or independent?

**Key descriptive statistics table** (like IndieGuard Table 4):

| Variable | n | Mean | Median | Min | Max |
|---|---|---|---|---|---|
| Avg monthly income (INR) | 30,000 | 28,400 | 25,000 | 2,000 | 1,50,000 |
| Gig tenure (months) | 30,000 | 24.3 | 18 | 1 | 120 |
| Loan amount (INR) | 30,000 | 52,000 | 40,000 | 5,000 | 3,00,000 |
| Utility bills on time (of 12) | 30,000 | 8.4 | 9 | 0 | 12 |
| Income volatility index | 30,000 | 0.31 | 0.28 | 0.00 | 2.00 |

**Key EDA findings to highlight (with figure references):**

1. **Gig tenure vs default** — Borrowers with <6 months tenure default at 18.4% vs 4.1% for 3+ years (Figure 2).
2. **Income volatility** — High volatility (>0.5 CV) correlates with 2× higher default rate (Figure 3).
3. **Utility reliability** — Every missed bill adds ~1.8 pp to default rate; above 3 misses the effect accelerates (Figure 4).
4. **BNPL-to-income ratio** — Non-linear: minimal effect until ratio >0.3, then sharply higher risk (Figure 5).
5. **Location** — Rural borrowers default at 11.2% vs Metro at 5.7% (Figure 6).
6. **Hypothesis tests** — Mann-Whitney U for income (p<0.001), chi-square for education level (p<0.001), chi-square for bank account status (p<0.001).

**Note on methodology choice:** With 7.87% default rate, accuracy rewards ignoring the minority class; we use PR-AUC and macro-F1 as primary metrics. Borrowers on the same gig platform share behavioural vocabulary, so random split would over-state performance; we use stratified split.

---

### 4. Feature Engineering & Predictive Modelling — Unit 2 (2 pages)

#### 4.1 Feature Engineering
- 14 engineered features (describe each briefly)
- VIF analysis (remove multicollinear raw features)
- Weight of Evidence / Information Value screen (selected features with IV > 0.1)
- PCA on correlated behavioural clusters — elbow at 8 components (keeping 72% variance)
- t-SNE visualisation showing default cluster separation

#### 4.2 Model Development & Evaluation

> Same structure as IndieGuard Table 5 — produce a clean comparison table.

**Model comparison on the shared held-out test set (6,000 borrowers; guessing PR-AUC ≈ 0.08, baseline AUC 0.5).**

| Model | CV PR-AUC | Test PR-AUC | Test AUC-ROC | Recall (defaults) |
|---|---|---|---|---|
| Dummy (prior) | — | 0.079 | 0.500 | 0.00 |
| Logistic Regression (tuned) | 0.172 ± 0.011 | 0.197 | 0.728 | 0.638 |
| Random Forest (tuned) | 0.165 ± 0.018 | 0.178 | 0.713 | 0.663 |
| **LightGBM (tuned)** | **0.189 ± 0.014** | **0.201** | **0.735** | 0.614 |
| XGBoost (tuned) | 0.191 ± 0.015 | 0.204 | 0.738 | 0.682 |
| **Calibrated LightGBM (dashboard)** | — | 0.199 | **0.741** | — |

- **Selection:** Calibrated LightGBM for the dashboard (needs calibrated probabilities for expected-loss pricing); XGBoost for ranking comparisons.
- **Leakage audit:** outcome column excluded; SMOTE inside pipeline; all scalers/imputers fitted inside each training fold; 21 automated checks pass.
- **SHAP top drivers:** Gig tenure (months), income trend slope, utility reliability score, loan-to-income ratio, income volatility index (Figure X).

#### 4.3 Subgroup Performance Check
Slice test predictions by: location type, education level, gig platform, loan tenure bucket. Report where the model is weaker (Early-tenure applicants, Rural location) and state that those segments deserve more caution.

**Cost-optimal threshold:**
- Missed default cost ≈ ₹81,900 (LGD × median loan)
- Wrong rejection cost ≈ ₹9,700 (lost net interest over tenure)
- At optimal threshold: 74.7% approved, 4.4% approved-default rate vs 7.9% if everyone were approved.

---

### 5. Advanced Analytics (Unit 3): Two Selected Methods (2 pages)

**Motivation bridge** (like IndieGuard's Section 5 intro): The EDA and Unit 2 models raised two further questions. First, PD tells us *who* will default but not *what combination of signals* triggers that — so we chose association rule mining. Second, individual-level PD ignores macro cycles — so we chose time-series forecasting of the portfolio default rate. *(Time series was not substituted for a third ML model; each method answers a distinct question.)*

---

#### 5.1 Method 1 — Time-Series Forecasting (SARIMAX + Live Macro Drivers)

**Data:** Monthly portfolio default rate (72 months, 2019–2024) from `portfolio_monthly.csv`. Macro drivers: unemployment rate, GDP growth, CPI inflation, call-money rate, 10y G-sec yield, INR/USD — from FRED and World Bank APIs.

**Pipeline:**
1. Stationarity — ADF and KPSS tests; differencing if needed
2. STL decomposition — trend, seasonal (annual), residual
3. Granger causality — test which macro series lead the default rate (handle statsmodels ≥0.15 `verbose` removal)
4. SARIMAX — BIC-selected order; macro drivers as exogenous regressors; COVID lockdown dummy
5. Comparison vs: SARIMA (no macro), Holt-Winters ETS, Gradient Boosting (lags + macro), Seasonal Naive

**Model comparison (hold-out 2024 — 12 months, never seen in fitting):**

| Model | MAE (pp) | MAPE | Backtest MAE (40 origins) |
|---|---|---|---|
| **SARIMAX + macro** | **0.054** | **16%** | **0.124** |
| Gradient Boosting | 0.065 | 22% | — |
| Holt-Winters ETS | 0.075 | 24% | 0.208 |
| SARIMA | 0.088 | 30% | 0.176 |
| Seasonal Naive | 0.124 | 40% | 0.351 |

**Driver significance (expected signs, all p < 0.05):**
- Unemployment +1 pp → +21% defaults
- CPI +1 pp → +15%
- Call-money rate +1 pp → +10%
- COVID lockdown month → ×5.7

**2025 Stress Scenarios:**

| Scenario | Avg monthly default rate | Expected Credit Loss | vs Baseline |
|---|---|---|---|
| Baseline | 0.28% | ₹1.59 crore | — |
| Adverse (+1.5pp unemployment, −3pp GDP) | 0.33% | ₹1.95 crore | +₹36 lakh |
| Severe (COVID-style) | 0.74% (peak 2.7%) | ₹4.32 crore | +₹2.74 crore |

---

#### 5.2 Method 2 — Delinquency Warning Rules (Apriori / FP-Growth)

**Data:** 24,000 training borrowers encoded into 19 binary behavioural flags (e.g., `high_volatility`, `low_savings_buffer`, `utility_miss_3plus`, `high_bnpl_ratio`, `declining_income`, `short_gig_tenure`).

**Pipeline:**
1. Item definition — 19 flags with thresholds justified from EDA
2. Apriori vs FP-Growth — both on same support range; compare rule counts, speed, identical rules at same threshold (Table in Appendix B)
3. Filter: lift ≥ 1.5, support ≥ 0.5%, Bonferroni-corrected Fisher p < 0.05
4. Redundancy pruning — remove rules whose consequent is covered by a strict subset antecedent with higher lift
5. Validate on 6,000 unseen test borrowers

**Results:**
- 2,852 frequent itemsets → 93 rules after filtering and pruning
- **All 93 hold on unseen borrowers** (test lift ≥ 1.3)
- Top rule: *declining income + volatile income + low savings buffer → 24.7% default rate (3.1× test lift)*
- Routing applicants with ≥3 rules to manual review flags 14% of applicants but catches 34% of all defaults

**Macro interaction (novel finding):**
Under macro stress, `volatile_income` adds +4.5 extra default points, while `low_income` and `rural_location` add nothing extra — suggesting behavioural instability (not just poverty) is the stress amplifier.

---

### 6. Combined Business Insights & Impact Scenarios (1 page)

#### 6.1 Combined Decision Rule
The dashboard's underwriting decision integrates three layers:

| Layer | Model | Trigger |
|---|---|---|
| PD check | Calibrated LightGBM | Decline if PD > Break-even PD |
| Stress overlay | SARIMAX multiplier | Point-in-time PD = PD × macro multiplier |
| Behavioural flag | 93 ARM rules | ≥3 rules → Approve with Conditions |

**Key combined insight:** Within the same lowest-risk PD band (Band A, PD < 4%), applicants with 6+ triggered warning rules default 3× more (5.6% vs 1.8%). The PD model and the ARM rules are **complementary, not redundant**.

#### 6.2 KPI-Based Business Impact Scenarios

*(Structured like IndieGuard Table 10 — illustrative, not forecasts)*

**Scenario: Routing ≥3-rule applicants to manual review (extra ₹500 cost per file)**

| Scenario | Applicants routed | Defaults caught | Cost per caught default |
|---|---|---|---|
| No filter (approve all) | 0 | 0 | — |
| ≥3 rules → review | 14% | 34% of all defaults | ₹500 / ₹81,900 LGD (6× ROI) |
| ≥6 rules → decline | 4% | 12% of all defaults | ₹0 upfront |

**Assumptions stated:** All numbers assume the model's test-set performance holds on future borrowers; macro multipliers are point estimates; LGD is assumed constant at 65%.

#### 6.3 Literature Comparison
*(Like IndieGuard's comparison table)* — compare our accuracy against Berg et al. (2020) fintech study, Agarwal et al. (2020) India study, Lessmann et al. (2015) benchmark.

---

### 7. Interactive Dashboard, Figure Index & Reproducibility (0.5 page)

#### 7.1 Mandatory Dashboard
The dashboard runs with `streamlit run dashboard/app.py` from the repository root.

**Five tabs:**
1. **Underwriter Decision Engine** — Score an applicant (8 visible inputs + Advanced expander); SHAP waterfall; delinquency rules triggered
2. **Dataset Explorer & Drilldown** — Filter 6,000 test borrowers by risk band, location, platform; dynamic KPIs and charts
3. **Portfolio Outlook & Scenarios** — SARIMAX forecast vs historical actual; scenario toggle; ECL impact table; macro driver charts
4. **Delinquency Warning Rules** — Interactive scatter of all 93 rules by lift and coverage; filter by flag must-contain
5. **Model Card & Provenance** — Calibration by decile; model metadata; macro data provenance table

#### 7.2 Figure Index & Reproduction Map
*(Table with Figure number, content, source notebook/script — like IndieGuard Table 11)*

#### 7.3 Code and Environment
- Repository: `github.com/Goldmauler/intellicredit-review2`
- Python 3.10, all packages pinned in `requirements.txt`
- Reproduce: `python data_generation.py` → `python -m src.macro_api` → `python -m src.portfolio_simulation` → notebooks 01–08 → `streamlit run dashboard/app.py`
- All randomness seeded (42 for data/models, 2026 for portfolio simulation)

---

### 8. Reflections & Limitations (0.5 page)

**Limitations (be honest, like IndieGuard):**
- Borrowers and transactions are synthetic; all results are associations, not causal estimates of real borrower behaviour
- World Bank annual series interpolated to monthly — interpolation error at turning points
- 93 ARM rules validated on a held-out split from the same synthetic distribution; real generalisation unknown
- The macro multiplier is a linear overlay; it assumes the PD model's rank ordering is stable under stress
- The dashboard SHAP values are log-odds contributions; lay users may misread them as probabilities
- Thin-file borrowers with 0 prior micro-loans produce a `repayment_ratio` of −1 (sentinel); this segment's model performance is unvalidated

**What worked well:** Live API integration (FRED + World Bank) with graceful fallback; ARM rules generalising perfectly to held-out test set; calibrated LightGBM PD aligning closely with observed default rate.

**What we would do next:** Real borrower pilot; model monitoring with distribution shift alerts; Platt-scaling recalibration quarterly as macro regime changes.

---

### References (~15–20 entries, ACM/IEEE style)

Must include:
1. Berg et al. (2020) — digital footprints and credit scoring
2. Björkegren & Grissen (2020) — mobile phone data and repayment
3. Agarwal, Alok, Ghosh, Gupta (2020) — alternative credit India
4. Lessmann et al. (2015) — benchmarking credit scoring models
5. Lundberg & Lee (2017) — SHAP values (TreeSHAP)
6. MFIN Micrometer Q1 FY27 — microfinance India benchmark
7. NITI Aayog (2022) — gig economy policy brief
8. Agrawal & Srikant (1994) — Apriori algorithm
9. FCA (2024/2025) — synthetic data for financial services
10. NPCI Annual Report (UPI transaction statistics)
11. PLFS 2022–23 (income benchmarks)
12. Pandas, Streamlit, LightGBM, scikit-learn — software citations

---

## Appendices

### Appendix A. Additional Figures
- Full SHAP summary plot (all features)
- Calibration curve (10 deciles)
- STL decomposition of portfolio default rate
- Granger causality test results table
- ARM scatter: test coverage vs test confidence (all 93 rules)
- Confusion matrix at cost-optimal threshold

### Appendix B. Full Model Comparison Tables
- Review 1: all five models — 5-fold CV + test AUC-ROC, PR-AUC, F1, KS, recall
- Review 2 M1: Apriori vs FP-Growth — itemset counts, rule counts, runtime (identical rules at same thresholds → confirmed)
- Review 2 M2: SARIMAX vs all baselines — full metrics table

### Appendix C. Implementation Details & Dashboard User Guide
**Requirements:** Python 3.10, `pip install -r requirements.txt`

**Pipeline steps:**
```
python data_generation.py
python -m src.macro_api
python -m src.portfolio_simulation
python -m src.underwriting_model
# Then run notebooks 01–08 in order
streamlit run dashboard/app.py
```

**Dashboard user guide:** Tab-by-tab walkthrough (how to use each control, what the metrics mean, what SHAP log-odds contribution means in plain English)

### Appendix D. Project Board, Contributions & AI Declaration

**GitHub project board:** link (all 19 tasks completed)

**Table. Project-board cards by member** (like IndieGuard Table 19)

| Member | Register Number | Tasks (owner) | Rubric component |
|---|---|---|---|
| Darun R G | CB.SC.U4CSE23215 | Data architecture, generator, feature engineering, ARM data prep, dataset validation | Dataset + Unit 1 & 2 baseline |
| goldmauler | [fill] | Method 1 (Time-Series) & Method 2 (ARM), macro API, 93 warning rules | Method 1 (5 marks) + Method 2 (5 marks) |
| Abhinav Juturu | [fill] | EDA (38 charts), portfolio simulation, hypothesis tests | EDA + Method 1 data prep |
| Gowtham Reddy | [fill] | Dashboard (5-tab Streamlit), data cleaning, HTML report | Mandatory dashboard (5 marks) |
| Adithya | [fill] | Model evaluation, SHAP, combined insights, final report & slides | Combined insights + Presentation |

**Table. Generative-AI disclosure** (like IndieGuard Table 20)

| Tool | Tasks supported | Content / code affected | Human verification |
|---|---|---|---|
| Antigravity (AI coding assistant) | Dashboard code improvements, report plan generation | `dashboard/app.py` refactoring (fewer inputs, rate fix, ECL year), this report plan | All changes read, run, and tested; model outputs cross-checked against notebook results |
| ChatGPT / Claude | Ideation, debugging help | Small code snippets, documentation drafts | Team ran, checked and corrected all outputs; errors found and fixed |

---

> [!TIP]
> **Page budget guidance** (targeting ~15 pages like the reference report):
> - Abstract + Exec Summary: 2 pages
> - Sections 1–2: 3 pages
> - Sections 3–4: 3 pages
> - Section 5: 2 pages
> - Sections 6–8 + References: 3 pages
> - Cover, ToC, Abbreviations: 2 pages
> - **Total body: ~15 pages** (appendices are additional)

> [!NOTE]
> Every table and figure in the main text should reference its source notebook or script (e.g., "Python/Matplotlib; `notebooks/02_M2_exploratory_data_analysis.ipynb`") — the IndieGuard reference report does this consistently and it makes reproducibility obvious to the reviewer.
