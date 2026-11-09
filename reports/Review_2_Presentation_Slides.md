# IntelliCredit: FinTech Micro-Lending Risk Engine
## Review 2 Final Panel Presentation Deck & Defense Guide
**Duration: 15 Minutes | Total Marks: 20 | 18 Comprehensive Defense Slides**

---

### 5-Member Defense Timing Breakdown (15 Minutes)
| Member | Name & Roll No. | Slides | Topic / Focus Area | Timing |
|:---:|---|:---:|---|:---:|
| **1** | **Gowtham Reddy** (CB.SC.U4CSE23119) | **Slides 1 – 4** | Title, Problem Context, Literature Review & Complete Workflow | 0:00 – 3:00 (3:00 min) |
| **2** | **Abhinav Juturu** (CB.SC.U4CSE23103) | **Slides 5 – 8** | Dataset Architecture, Key Variables, QA/Validation & Unit 1 EDA | 3:00 – 5:45 (2:45 min) |
| **3** | **Adithya** (CB.SC.U4CSE23101) | **Slides 9 – 10** | Unit 2 ML Predictive Modeling, TreeSHAP Drivers & Unit 3 Method Selection | 5:45 – 8:00 (2:15 min) |
| **4** | **Vimalharihar S K** (CB.SC.U4CSE23120) | **Slides 11 – 14** | Unit 3 Method 1 (SARIMAX + ECL Scenarios) & Method 2 (ARM Delinquency Rules) | 8:00 – 11:30 (3:30 min) |
| **5** | **Darun R G** (CB.SC.U4CSE23114) | **Slides 15 – 18** | Combined Business Insights, Mandatory Live Dashboard Demo, Contributions & Conclusion | 11:30 – 15:00 (3:30 min) |
| **All** | **All Team Members** | **All** | Panel Defense Q&A & Rubric Justification | Post-Presentation |

---

## Slide 1: Title & Presentation Header (0:30 min)
- **Title**: IntelliCredit: FinTech Micro-Lending Risk & Alternative Credit Scoring Engine
- **Subtitle**: Capstone Project Review 2: Advanced Analytics & Underwriter Decision Cockpit
- **Course & Institution**: 23CSE452 Business Analytics | Department of Computer Science & Engineering, Amrita Vishwa Vidyapeetham
- **Faculty Guide**: Rohini S | **Presentation Date**: November 2026
- **Team Members**:
  - Darun R G (CB.SC.U4CSE23114)
  - Vimalharihar S K (CB.SC.U4CSE23120)
  - Abhinav Juturu (CB.SC.U4CSE23103)
  - Gowtham Reddy (CB.SC.U4CSE23119)
  - Adithya (CB.SC.U4CSE23101)

---

## Slide 2: Project Overview — Business Problem & Objectives (1:00 min)
- **Business Problem**: Over 1.4 billion gig-economy workers and thin-file individuals lack traditional credit scores (CIBIL/FICO). Lenders either exclude them unfairly or lend blind, resulting in prohibitive delinquency and high default rates.
- **Objectives**:
  1. *ML Default Prediction*: Develop interpretable ML classifiers beating baseline models (AUC > 0.70) on held-out test applicants with TreeSHAP explainability.
  2. *Advanced Analytics*: Forecast monthly portfolio default rates under macroeconomic shocks (SARIMAX) and uncover conjunctive delinquency traps (Association Rules).
- **Business Decision**: Enable underwriter decision automation (auto-approve, manual conditional review, or auto-decline) and dynamically calibrate credit limits and capital loss reserves (ECL in ₹ Crore) as macroeconomic cycles turn.
- **Expected Output**: Production-grade underwriting decision cockpit: calibrated applicant default probability, 93 behavioral warning badges, dynamic Point-in-Time stress multiplier, and a live Streamlit dashboard.
- **Takeaway**: *IntelliCredit replaces blunt credit bureau exclusion with an interpretable, macro-aware risk analytics engine.*

---

## Slide 3: Literature Review & Comparative Study (1:00 min)
- **Literature Foundations & Research Gaps Addressed**:
  - *Alternative Credit Scoring*: Khandani et al. (2010), Lessmann et al. (2015), and Óskarsdóttir et al. (2019) demonstrated that high-frequency transactional and behavioral cash flows predict consumer delinquency, but prior studies relied on commercial bank statements and operated in static macroeconomic regimes without dynamic stress testing.
  - *Macro Stress Testing & Credit Risk*: Pesaran et al. (2006) and Basel / IFRS 9 ECL regulatory frameworks established top-down portfolio default sensitivity to macroeconomic cycles (unemployment, GDP, interest rates), but remained disconnected from frontline borrower onboarding and underwriting.
  - *IntelliCredit Research Contribution*: IntelliCredit bridges these silos by fusing granular alternative cash flows (ML default probability), live FRED/World Bank macro regressors (SARIMAX portfolio forecasting), and 93 conjunctive warning rules into an operational underwriter cockpit.
- **Comparative Study Matrix**:
  | Evaluation Dimension | Traditional Bureaus (CIBIL / FICO) | Standard ML Credit Models | IntelliCredit (Our Proposed Engine) |
  |---|---|---|---|
  | **Data Modality & Ingestion** | Formal bureau trade-lines, credit card histories, salaried bank slips. Excludes non-traditional signals. | Static cross-sectional loan application tables (LendingClub, Kaggle Home Credit). Offline snapshots. | **High-frequency cash-flow volatility, utility discipline, UPI, savings buffer + Live FRED & World Bank macro APIs.** |
  | **Target Population & Inclusion** | Prime & salaried formal borrowers. Completely excludes 1.4B unbanked / gig workers lacking bureau files. | Formally banked credit applicants. Struggles on thin-file applicants with irregular, volatile income streams. | **Engineered specifically for thin-file & gig workers (₹14k–₹48k/mo); unlocks safe, automated financial inclusion.** |
  | **Macro Stress Awareness** | Static Through-The-Cycle (TTC) scores; insensitive to live inflation, rates, or macro recessions. | Static offline risk distribution; assumes macro stability. Zero real-time stress testing linkage. | **Dynamic Point-in-Time (PiT) SARIMAX forecasting; adjusts approval cutoffs and ₹ Crore ECL buffers.** |
  | **Interpretability & Underwriting** | Opaque empirical 300–900 score; proprietary scoring matrices without granular causal feedback. | Black-box ensembles (GBM / Deep Net); global feature importances lack applicant-level actionability. | **Dual explainability: local applicant TreeSHAP waterfalls + 93 Fisher-pruned rules (100% test generalization).** |
  | **Operational Deployment** | Rigid binary cutoffs or manual paper underwriting. Disconnected from dynamic portfolio provisioning. | Standalone probability predictions; disconnected from underwriter policy and live stress scenarios. | **Production Streamlit decision cockpit: live scoring, dynamic PiT multiplier, warning badges, and ECL simulation.** |
- **Takeaway**: *IntelliCredit bridges alternative behavioral signals, live macroeconomic stress testing, and granular explainability into one unified engine.*

---

## Slide 4: Units 1 to 3 Complete Project Workflow (1:00 min)
- **Workflow Implementation Across Units**:
  - *Unit 1*: Programmatic data generation (30,000 borrowers, 360,000 transactions); KNN missing imputation, IQR outlier winsorization; 38 EDA visualisations with chi-square & Mann-Whitney tests; 14 engineered alternative behavioral features, VIF, WoE/IV, PCA, SMOTE.
  - *Unit 2*: 5 baseline + 4 tuned ML algorithms (LR, RF, LightGBM, Tuned XGBoost); voting & stacking ensembles; leak-free 5-fold CV with SMOTE pipeline; ROC/PR curves, KS test, TreeSHAP waterfall explainability; INR cost-optimal threshold (₹81.9k vs ₹9.7k).
  - *Unit 3*: Method 1: Time-series portfolio default forecasting (SARIMAX with live FRED/World Bank macro regressors, 40-origin backtest, 3 stress scenarios) and Method 2: Association rule mining (Apriori vs FP-Growth, 93 warning rules, 100% test generalization).
  - *Final Application*: Production Streamlit underwriter dashboard (`dashboard/app.py`): 5 interactive tabs including Dataset Explorer, Real-time Scoring with TreeSHAP, Active Warning Badges, Portfolio Forecasts, and Macro Stress Testing. Plus standalone HTML report.
- **Completion Status**: 100% implementation delivered and verified across all 3 analytical units, 8 notebooks, dashboard, and technical report.
- **Takeaway**: *Every analytical unit is integrated end-to-end: one validated dataset, one leak-free chronological split, and one unified dashboard.*

---

## Slide 5: Overall Dataset Description Across Units 1 to 3 (1:00 min)
- **Source & Collection**: Programmatic statistical generation (NumPy distributions + Faker `en_IN`) for 30,000 borrowers and 360,000 transactions. Live institutional macroeconomic APIs from FRED (CPI inflation, call-money rate, 10y G-sec, INR/USD) and World Bank (unemployment, real GDP growth, lending rate). No pre-built Kaggle/UCI datasets used.
- **Final Dataset Size**: 30,000 borrower profiles × 39 demographic/behavioral variables; 360,000 monthly transactions across 12 months; 108 monthly macro observations (2017–2025); 30,000 originated loans × 250,191 loan-months over 72 months (2019–2024).
- **Coverage**: Indian gig-economy and thin-file cohort; monthly income ₹14k–₹48k; gig platforms Swiggy, Zomato, Ola, Uber, Urban Company; 7 institutional macroeconomic series; COVID lockdown and second-wave disruption event dummies included.
- **Unit Mapping**: Units 1–2 use borrower profiles & 12-month transactions (default prediction). Unit 3 Method 1 uses monthly portfolio default rate panel & macro indicators (time-series). Unit 3 Method 2 uses 19 discretized behavioral flags on 24k training borrowers (ARM).
- **Takeaway**: *An original, frozen, and reproducible data architecture linking micro borrower transactions to macroeconomic cycles.*

---

## Slide 6: Sample Dataset and Key Variables (1:00 min)
- **Sample Records**: Showcases contrasting borrower profiles (Swiggy vs. Zomato vs. high-risk Ola borrower defaulting due to 0.48 income volatility and 42% utility reliability).
- **Key Variables**: `loan_default_status` (binary target, 7.87% baseline rate); `avg_monthly_income` (₹ continuous); `income_volatility_index` (std/mean income); `utility_reliability_score` (ratio of on-time utility payments); `savings_buffer_ratio` (end-of-month balance / monthly outflow); `gig_tenure_months` (platform stability).
- **Linked Datasets**: `monthly_transactions.csv` (12-month transaction logs); `macro_india_monthly.csv` (7 live FRED/World Bank macro indicators); `portfolio/loan_book.csv` & `loan_performance.csv` (macro-linked loan repayment panel for time-series). Samples in `data/sample/`.
- **Takeaway**: *Multi-attribute feature vectors capture both willingness-to-pay (utility discipline) and cash-flow capacity (income volatility).*

---

## Slide 7: Dataset Validation and Preparation (1:00 min)
- **Comprehensive Quality Assurance**:
  - *Missing Values & Duplicates*: 0 duplicate borrower IDs; 6,319 missing ages in transactions; structural nulls in `default_month`. Handled via KNN imputation for missing ages; structural nulls verified. Retained 30k unique borrowers.
  - *Types, Ranges & Consistency*: Income outliers detected via IQR; month_label had duplicates; unmapped ordinals. Handled via IQR winsorization; fixed dates with `pd.date_range`; corrected ordinal maps in config.
  - *Suitability Across Units*: Units require borrower features (1-2), 72-month portfolio panel (M1), 19 binary flags (M2). Leak-free 80/20 split; SMOTE applied only within CV folds; fitted on train only. 21 checks pass.
  - *Synthetic Realism Checks*: Borrowers/txns synthetic. All 7 macro indicators 100% real from FRED & World Bank APIs. Validated against MFIN Micrometer (7.87% default), PLFS 2022-23 (₹14k-48k income), CGAP reports.
- **Pipeline Architecture**: Visual diagram showing raw generation $\to$ cleaning/imputation $\to$ feature engineering $\to$ chronological train/test split.
- **Takeaway**: *Audited and leak-free: zero pipeline leakage, fixed timestamps, and benchmarked against real Indian financial data.*

---

## Slide 8: Unit 1 Exploratory Analysis and Preprocessing (1:00 min)
- **Visuals**: Two high-density EDA charts (`eda_chart1.png` - Gig Platform Default Rates & Tenure Trends; `eda_chart2.png` - Income Volatility Deciles vs Delinquency).
- **Key Findings**: (1) Gig tenure < 12 months displays a 2.3× higher default rate than tenure > 36 months. (2) Income volatility index > 0.4 correlates strongly with delinquency (Mann-Whitney p < 0.001); the top risk decile defaults at 23% (2.9× lift over baseline).
- **Preprocessing Pipeline**: KNN imputation for missing ages; IQR winsorization on skewed financial values; ordinal encoding (education, location); one-hot encoding (gig platform); 14 engineered features (income volatility, utility reliability, savings buffer, trend slope); VIF < 5; WoE/IV screen.
- **Takeaway**: *Alternative cash-flow stability and utility discipline carry significant predictive power for thin-file applicants.*

---

## Slide 9: Unit 2 Predictive Modelling and Final Evaluation (1:00 min)
- **Model Comparison Table & Graphic**:
  - Tuned XGBoost [BEST]: AUC-ROC = **0.738** (85.3% of theoretical ceiling 0.781), PR-AUC = **0.204**, Recall = 0.682, F1 = 0.247.
  - Tuned LightGBM: AUC-ROC = 0.735, PR-AUC = 0.201.
  - Tuned Logistic Regression: AUC-ROC = 0.728, PR-AUC = 0.197.
- **Evaluation Setup**: Target = `loan_default_status` (7.87% positive class). Chronological 80/20 train/test split (24,000 train / 6,000 held-out test). SMOTE applied inside imblearn pipeline during 5-fold stratified CV only to prevent synthetic leakage.
- **Selected Cutoff & TreeSHAP Drivers**: At INR cost-optimal threshold (missed default cost ₹81.9k vs wrong rejection ₹9.7k): 74.7% approved with an approved default rate of only 4.4% (vs 7.87% baseline). Top SHAP drivers: gig tenure, income trend, utility reliability.
- **Takeaway**: *Tuned XGBoost captures 85% of theoretical discrimination; cost-optimal cutoff slashes approved default rates by 44%.*

---

## Slide 10: Unit 3 Selected Advanced Analytics Methods (1:00 min)
- **Method 1: Time-Series Portfolio Forecasting**:
  - *Business Question*: When will portfolio defaults rise, and by how much under macroeconomic stress scenarios?
  - *Data Subsets*: 72 monthly portfolio default rates (2019–2024) + 7 live macro indicators from FRED & World Bank APIs (108 monthly observations).
- **Method 2: Association Rule Mining**:
  - *Business Question*: Which specific combinations of alternative borrower behaviors signal severe delinquency risk?
  - *Data Subsets*: 19 discretized behavioral flags across 24,000 training borrowers (cash-flow trend, volatility, utility delays, savings buffer).
- **Methodology Rationale**: Method 1 provides top-down portfolio loss forecasting to quantify capital buffers; Method 2 provides bottom-up conjunctive warning patterns that catch localized risk that ML gradients smooth over. Both methods directly feed the underwriter dashboard.
- **Takeaway**: *Two complementary advanced methods: macro portfolio risk horizon (Method 1) combined with granular behavioral traps (Method 2).*

---

## Slide 11: Unit 3 Method 1 Implementation: SARIMAX with Macro Drivers (1:00 min)
- **Method & Target**: Time-Series Forecasting using SARIMAX with exogenous macroeconomic regressors to forecast portfolio default rates and quantify Expected Credit Loss (ECL) under stress.
- **Input & Preparation**: 72 monthly default rates (2019–2024). ADF and KPSS tests confirmed non-stationarity in levels; stationary after first-order differencing ($d=1$, $p < 0.001$). STL decomposition isolated 12-month seasonality & COVID disruption. Granger causality verified unemployment ($p=0.008$), call money ($p=0.019$), and CPI ($p=0.024$) lead defaults by 2 months.
- **Implementation**: $\text{SARIMAX}(1,1,1)(1,1,1)_{12}$ with 4 macro regressors (unemployment rate, CPI inflation, call-money rate, COVID lockdown dummy). Benchmarked against 6 alternatives (Gradient Boosting, Holt-Winters, SARIMA, Seasonal Naive, STL+ETS, STL+ARIMA) across 40-origin expanding-window backtests.
- **Output**: SARIMAX achieves lowest hold-out error (MAE 0.054 pp, MAPE 16%). Macro effects: unemployment +1 pp $\to$ +21% defaults; CPI +1 pp $\to$ +15%; COVID lockdown $\to$ 5.7× default surge. Residuals are white noise (Ljung-Box $p=0.12$).
- **Takeaway**: *First-order differencing and Granger-causal macro regressors deliver stationary, lead-indicator forecasting power.*

---

## Slide 12: Unit 3 Method 1 Evaluation and Macro Stress Scenarios (1:00 min)
- **Model Architecture Benchmark**:
  | Model Architecture | Hold-out MAE | MAPE % | Backtest MAE |
  |---|:---:|:---:|:---:|
  | **SARIMAX + Macro [BEST]** | **0.054 pp** | **16.4%** | **0.124 pp** |
  | Gradient Boosting / Holt-Winters | 0.063 / 0.075 | 21.2% / 23.9% | — / 0.208 |
- **Validation**: 60 training months (2019–2023), 12 held-out test months (2024). 40-origin expanding-window backtest validates stability across regimes. Ljung-Box test confirms white-noise residuals ($p = 0.12$). 80% prediction interval covers 91.7% of actual 2024 observations.
- **Translating Forecasts into Capital (ECL in ₹)**:
  - *Baseline Scenario* (0.28% avg monthly default rate) $\to$ **₹1.59 Crore ECL**.
  - *Adverse Scenario* (Unemployment +1.5 pp, GDP -3 pp) $\to$ **₹1.95 Crore ECL** (+₹36 Lakhs capital overlay).
  - *Severe Scenario* (COVID-scale shock) $\to$ **₹4.32 Crore ECL** (+₹2.74 Crore capital buffer).
- **Takeaway**: *SARIMAX with live macro APIs beats all baselines; stress scenarios translate rates into actionable capital buffers in ₹ Crore.*

---

## Slide 13: Unit 3 Method 2 Implementation: Delinquency Rule Mining (1:00 min)
- **Method & Target**: Association Rule Mining (Apriori vs FP-Growth) to discover specific conjunctive combinations of borrower behaviors (income volatility, utility delays, low savings) that signal high delinquency risk, complementing the ML default probability.
- **Input & Preparation**: 19 behavioral flags discretized across 24,000 training borrowers (`DECLINING_INCOME`, `INCOME_VOLATILE`, `LOW_SAVINGS_BUFFER`, `HIGH_BNPL_USAGE`, `UTILITY_DELAY_HIGH`, `LOW_DIGITAL_ACTIVITY`, `RURAL_LOCATION`, `NEW_GIG_TENURE`). Structured as dense binary itemsets.
- **Implementation & Pruning**: Apriori vs FP-Growth (mlxtend) with min_support = 0.5%. Both algorithms discover identical 2,852 frequent itemsets. Apriori executed faster (0.62s vs 1.13s) due to low array overhead on dense binary structures. Multi-stage pruning: Confidence $\ge 15\%$, Lift $\ge 1.50$, Bonferroni-corrected Fisher exact $p < 0.05$, and subset redundancy removal $\to$ **93 high-conviction warning rules**.
- **Output**: 93 validated delinquency rules. Top rule: $\text{DECLINING\_INCOME} \land \text{INCOME\_VOLATILE} \land \text{LOW\_SAVINGS\_BUFFER} \to \text{DEFAULT}$ (24.7% default rate, 3.14× lift). Routing applicants with $\ge 3$ rules to manual review flags 14% of volume and catches 34% of all portfolio defaults.
- **Takeaway**: *Rigorous statistical pruning and held-out validation eliminate spurious rules and prevent false alarms.*

---

## Slide 14: Unit 3 Method 2 Evaluation and Delinquency Patterns (1:00 min)
- **Top Validated Delinquency Rules**:
  | Top Validated Delinquency Rules (Antecedents $\to$ Default) | Confidence | Train Lift | Test Lift (Held-out) |
  |---|:---:|:---:|:---:|
  | `DECLINING_INCOME + INCOME_VOLATILE + LOW_SAVINGS_BUFFER` | 24.7% | 3.14× | **3.14× [100% Generalization]** |
  | `INCOME_VOLATILE + LOW_SAVINGS_BUFFER + NEW_GIG_TENURE` | 24.5% | 3.11× | **3.11× [100% Generalization]** |
- **Generalization & Risk Spread**: 100% of the 93 rules generalize on 6,000 unseen test borrowers (Test Lift $\ge 1.30\times$). Triggered rules create a 5× risk spread (0 rules $\to$ 4.9% default; $\ge 6$ rules $\to$ 24.7% default).
- **Visuals**: Bubble scatter plot of Lift vs Confidence (`arm_rules_chart.png`).
- **Takeaway**: *All 93 rules hold on unseen test borrowers; triggering 6+ rules signals a 5x surge in delinquency probability.*

---

## Slide 15: Business Outcomes and Combined Insights (1:00 min)
- **Combined Synergies**:
  - *Rules detect risk ML PD misses*: In Band A (<3%), $\ge 6$ rules defaults at 5.6% vs 1.8% with 0 rules (3.1× spread).
  - *Recommended Underwriting Action*: Two-tier underwriting: Auto-approve Bands A–B (<3 rules); conditional review for $\ge 3$ rules; decline Bands D–E.
  - *Expected Financial Benefit*: Reduces approved defaults from 7.87% to 4.4%. Route 14% to manual review to catch 34% of defaults.
  - *Dynamic Macro Policy*: SARIMAX forecasts default surges under macro stress. Point-in-Time multiplier converts TTC PD to macro state. Auto-contract approvals from 75% (baseline) to 48% (severe) under same break-even rule. Avoids catastrophic wave; protects ₹2.74 Cr in severe shocks while maintaining lending in benign cycles.
- **Visuals**: Interactive Heatmap (`combined_heatmap.png`) showing delinquency rates cross-tabulated by ML Risk Band and Active Warning Rule count.
- **Takeaway**: *Synthesizing ML PD, warning rules, and macro multipliers yields an automated, macro-resilient credit underwriting engine.*

---

## Slide 16: Mandatory Live Demonstration (2:00 min)
- **Tech Stack**: Production Streamlit Dashboard (`dashboard/app.py`) & Standalone Plotly HTML (`reports/interactive_dashboard.html`).
- **Application & Live Demo Flow**:
  - Select applicant or adjust sliders (income, platform, volatility).
  - Inspect real-time TreeSHAP waterfall explaining positive/negative risk contributors.
  - Review active delinquency warning badges triggered by Association Rules.
  - Toggle macroeconomic scenarios (Baseline, Adverse, Severe) to view dynamic Point-in-Time approval adjustments.
- **Underwriting Business Scenario**:
  - Delivery worker earning ₹18,000/mo (8 mos tenure, 3 warning rules) applies for ₹50,000 loan.
  - Baseline economy: Approved conditionally with micro-ticket.
  - Adverse shock: Automatically declined as macro multiplier pushes PiT PD past break-even threshold.
- **Takeaway**: *A fully operational loan underwriting cockpit enabling real-time, explainable, and macro-aware credit decisions.*

---

## Slide 17: 100% Project Implementation & Contributions (1:00 min)
- **Team Responsibilities & Scope**:
  - **Darun R G (CB.SC.U4CSE23114)**: Data architecture, synthetic data generator (30k borrowers), feature engineering (14 features, WoE/IV), ARM data prep, dataset validation summary & benchmarks. (`data_generation.py`, `notebooks/01-05`, `DATASET_VALIDATION_SUMMARY.md`; Tasks #2, #3, #6, #13, #18).
  - **Vimalharihar S K (CB.SC.U4CSE23120)**: Lead — Method 1 SARIMAX forecasting (7 models, backtesting, macro APIs) & Method 2 Association Rule Mining (Apriori/FP-Growth, 93 rules, Fisher pruning). Predictive model tuning. (`notebooks/06_R2_M1`, `07_R2_M2`, `src/macro_api.py`, `models/arm_model_comparison.csv`; Tasks #7, #11-#15).
  - **Abhinav Juturu (CB.SC.U4CSE23103)**: Portfolio simulation engine, 72-month DPD migration panel, 38 exploratory data analysis charts, statistical hypothesis testing, scenario loss quantification. (`src/portfolio_simulation.py`, `notebooks/02_M2`, `data/portfolio/`; Tasks #5, #11).
  - **Gowtham Reddy (CB.SC.U4CSE23119)**: Interactive Streamlit 5-tab application (`dashboard/app.py`), TreeSHAP waterfall integration, data cleaning/preprocessing, standalone Plotly HTML report. (`dashboard/app.py`, `notebooks/01_M1`, `reports/interactive_dashboard.html`; Tasks #4, #16, #17).
  - **Adithya (CB.SC.U4CSE23101)**: Model evaluation & TreeSHAP explainability, combined business insights synthesis, quality assurance audit, technical report & 15-min panel presentation slides. (`notebooks/05_M5`, `08_R2`, `Review_2_Final_Report.md`, `Review_2_Presentation_Slides.md`; Tasks #8, #15, #17, #19).
- **Governance**: Project Board: `github.com/Darun1017/credit-scoring-engine` (19 tracked tasks) | Repositories: `Darun1017/credit-scoring-engine` & `Goldmauler/intellicredit-review2`.

---

## Slide 18: Final Project Outcome, Conclusions & Limitations (0:30 min)
- **Main Outcome**: 100% end-to-end implementation delivered across Units 1, 2, and 3: interpretable ML default prediction (AUC 0.738), macro-driven portfolio forecasting (SARIMAX, MAE 0.054 pp), 93 validated delinquency warning rules, and a 5-tab live decision dashboard.
- **Business Value**: Enables lenders to safely score thin-file borrowers (74.7% approved at 4.4% default rate), provision capital under macro stress (₹1.59 Cr baseline to ₹4.32 Cr severe), and flag high-risk combinations invisible to ML alone ($\ge 6$ rules $\to$ 5× default rate).
- **Honest Limitations**: Borrowers and transactions are synthetic (validated against MFIN, PLFS, RBI benchmarks); FRED CPI ends March 2025; rules are associative, not causal; SMOTE models overstate raw PD (dashboard resolves this via separately calibrated model).
- **Future Scope**: Ingest live UPI transaction streams, connect to RBI CRILC / Account Aggregator framework, calibrate PiT multipliers against empirical economic cycles, and deploy on cloud microservices.
- **Takeaway**: *IntelliCredit proves that alternative behavioral data and macroeconomic intelligence can safely expand credit inclusion.*
