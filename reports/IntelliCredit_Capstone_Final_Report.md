# CAPSTONE PROJECT: FINAL REPORT

# IntelliCredit: Alternative Credit Scoring & Risk Analytics Engine
### Predicting default risk, detecting delinquency patterns, and forecasting portfolio losses for India's thin-file and gig-economy borrowers

**Course:** 23CSE452 Business Analytics (Units 1, 2 and 3)  
**Academic Year:** 2026–2027  
**Repository:** [github.com/Goldmauler/intellicredit-review2](https://github.com/Goldmauler/intellicredit-review2)  
**Research Prototype:** Streamlit Decision Engine (`streamlit run dashboard/app.py`)  

| Team Member | Register Number | Role & Focus Area |
|---|---|---|
| **Darun R G** | CB.SC.U4CSE23215 | Data Architecture, Synthetic Generator, Feature Engineering & Validation |
| **goldmauler** | CB.SC.U4CSE23118 | Lead: Time-Series Forecasting (SARIMAX) & Association Rule Mining (ARM) |
| **Abhinav Juturu** | CB.SC.U4CSE23146 | Portfolio Risk Modeller, EDA, Macro Panel Simulation & Hypothesis Testing |
| **Gowtham Reddy** | CB.SC.U4CSE23232 | Interactive Dashboard Architecture, Data Preprocessing & Web Deployment |
| **Adithya** | CB.SC.U4CSE23752 | Model Evaluation, TreeSHAP Explainability, Combined Insights & Reporting |

---

## Declaration and Acknowledgement

We declare that this report and the capstone project it describes represent our original work as a team, with artificial intelligence assistance transparently disclosed in Section 8.3 and Appendix D (Table 20). The transaction dataset was programmatically generated using parameterized statistical distributions and empirical conditional dependencies, while all macroeconomic indicators were harvested directly from institutional APIs (Federal Reserve FRED and the World Bank). No pre-built commercial credit dataset was used for primary training, though the pipeline's methodology was benchmarked against the real-world UCI Credit Card Default dataset (Section 5.3). Prior research studies, theoretical algorithms, and software packages are systematically cited in the references. Generative-AI tools assisted with iterative code debugging, documentation formatting, and visual refactoring; all analytical methodologies, data architectures, model tuning choices, empirical findings, and policy recommendations were designed, verified, and audited by the team.

We express our sincere gratitude to our project guide for constructive advice, technical scrutiny, and continuous feedback throughout Review 1 and Review 2. We also thank the course faculty for providing the structured rubric and rigorous evaluation framework that shaped this research.

---

## Abstract

Over 1.4 billion thin-file individuals and informal gig-economy workers globally—including over 77 million platform workers in India—lack conventional credit bureau documentation (CIBIL/FICO scores). Traditional commercial lenders either exclude them entirely or lend unhedged, incurring severe default losses. **IntelliCredit** addresses this challenge through an end-to-end, multi-tier credit risk analytics research prototype integrating **Unit 1 & 2** (exploratory analytics and calibrated probability of default modelling), **Unit 3 Method 1** (macro-conditioned portfolio default forecasting), and **Unit 3 Method 2** (behavioural association rule mining of delinquency patterns). 

We engineered a dual-stream dataset: 30,000 synthetic borrower profiles with 360,000 longitudinal monthly transactions calibrated against empirical benchmarks (PLFS 2022–23, MFIN Micrometer, NPCI, and CGAP India diaries), combined with 108 continuous monthly institutional macro series (2016–2024) harvested live from FRED and World Bank APIs. On a strictly isolated 20% hold-out test set (6,000 borrowers, 472 defaults, 7.87% default rate), tree-based predictive classifiers demonstrated robust discrimination: **Tuned XGBoost** achieved **AUC-ROC = 0.738** [95% CI: 0.712, 0.764] and **PR-AUC = 0.204**, while **Calibrated LightGBM** delivered **AUC-ROC = 0.741** [95% CI: 0.715, 0.767] with calibrated probabilities (Brier score 0.0612). DeLong's test confirmed these two models are statistically indistinguishable ($p = 0.661$). In an Oracle test, augmenting Logistic Regression with the generator's non-linear thresholds elevated its AUC from 0.728 to 0.748, confirming that the tree models succeed primarily by capturing these clipped behavioral steps.

In Unit 3, a **SARIMAX** model conditioning on leading macro drivers (unemployment, CPI, call-money rate) outperformed four univariate and machine learning benchmarks on 2024 hold-out forecasting (**MAE = 0.054 pp**, **MAPE = 16.36%**) and over a 40-origin expanding-window backtest (Diebold-Mariano $DM = 2.84, p < 0.01$). Concurrently, association rule mining via Apriori and FP-Growth isolated **93 non-redundant delinquency warning rules**, with **100% remaining consistent out-of-sample** (test lift $\ge 1.30\times$). Crucially, warning rules detect default clusters that the machine learning score misses: in the prime rating band (Band A, $\text{PD} < 4\%$), borrowers triggering $\ge 6$ warning rules default at **5.6%** versus **1.8%** with clean patterns ($3.1\times$ risk spread). Testing under a second data-generating process (DGP-2) and on the real-world UCI Credit Card Default dataset (AUC = 0.7806, calibration 22.20% vs 22.12%) verified pipeline generalizability. The framework is demonstrated via a 5-tab **Streamlit** research prototype supporting loan underwriting, TreeSHAP explainability, and macro scenario stress-testing.

---

## Executive Summary

Traditional retail lending relies heavily on historical repayment track records, formal tax returns, and fixed salary slips. For gig workers whose earnings fluctuate weekly across digital platforms, this dependency creates an insurmountable credit barrier. Lenders must balance financial inclusion with solvency: how can an underwriter accurately score an applicant with zero bureau history, recognize hidden behavioural distress before 90-day delinquency occurs, and dynamically adjust loss provisions for macroeconomic shocks?

IntelliCredit answers these challenges by unifying cross-sectional machine learning, macroeconomic time-series forecasting, and behavioural association rule mining into an integrated decision-support platform. Every result reported has been strictly evaluated on unseen hold-out splits (24,000 training borrowers, 6,000 test borrowers; 60 training months, 12 hold-out months).

![Workflow Architecture](presentation_figures/pipeline_architecture.png)
*Figure 1. End-to-end IntelliCredit analytics architecture spanning Units 1, 2, and 3.*

### Key Empirical Findings

- **Gig Platform Tenure and Income Trajectory Dominate Default Risk:** Gig workers with under 6 months on a digital platform default at **18.4%**, compared to only **4.1%** for workers with over 36 months of tenure ($4.5\times$ risk multiple), holding monthly income constant. TreeSHAP feature attributions confirm that tenure and income trend slope exert the strongest marginal influence on default log-odds.
- **Alternative Behavioural Flags Exhibit Non-Linear Distress Thresholds:** Utility payment punctuality and Buy-Now-Pay-Later (BNPL) debt burdens do not scale linearly. Missing 1 to 2 bills per year produces modest risk elevation (+1.2 pp), whereas missing 3 or more bills triggers an exponential risk escalation (+8.7 pp default rate). Similarly, BNPL-to-income ratios above 25% sharply separate solvent workers from distressed over-indebted borrowers.
- **Machine Learning Differences Are Within Statistical Uncertainty:** Tuned XGBoost (AUC-ROC 0.738 [0.712, 0.764]) and Calibrated LightGBM (AUC-ROC 0.741 [0.715, 0.767]) perform comparably under DeLong's test ($p = 0.661$). An Oracle test demonstrates that augmenting linear Logistic Regression with the generator's non-linear clipped terms lifts its AUC to **0.748**, closing 37.5% of the distance to the theoretical ceiling of 0.781.
- **Exogenous Macroeconomic Drivers Substantially Reduce Forecast Errors:** On 12 months of unseen 2024 portfolio performance, SARIMAX conditioning on institutional FRED and World Bank macro indicators achieved an **MAE of 0.054 percentage points** and a **MAPE of 16.36%**, cutting forecast errors by **38.6%** compared to univariate SARIMA (0.088 pp). A 40-origin backtest and Diebold-Mariano testing confirm this advantage is statistically significant ($DM = 2.84, p = 0.007$).
- **Association Warning Rules Provide a Vital "Second Opinion" to the ML Model:** In the prime risk band (Band A, model $\text{PD} < 4\%$), applicants triggering 6 or more behavioural warning rules exhibit an observed default rate of **5.6%** versus **1.8%** for applicants with 0 rules. Warning rules capture structured qualitative combinations that high-dimensional gradient boosting trees smooth over.
- **Macroeconomic Stress Selectively Amplifies Cash-Flow Volatility:** Stress testing under adverse and severe scenarios reveals that economic downturns do not impact all gig workers equally: workers with high income volatility suffer an additional **+4.5 pp** default increase during downturns, whereas workers with stable low incomes show no incremental default surge.
- **Demographic Proxies Can Be Safely Removed:** An algorithmic fairness ablation test reveals that dropping `location_type` and `education_level` yields identical test discrimination (**AUC = 0.7406** vs 0.7406, $\Delta \text{AUC} = 0.0000$), while reducing Rural False Negative Rates from 60.6% to 57.6%.

### Recommended Underwriting Actions

1. **Implement Two-Tier Dual-Key Underwriting:** Automatically approve applicants in Risk Bands A and B who trigger fewer than 3 warning rules. Route applicants in Band C or those triggering 3 to 5 warning rules to conditional approval (mandating weekly micro-amortisation or a 25% lower credit ticket). Automatically decline Band E or $\ge 15$ rule triggers.
2. **Eliminate Socioeconomic Proxy Variables:** Remove location tier and education level from the scorecard. Our ablation test confirms they contribute zero marginal predictive gain over transaction metrics while introducing undesirable demographic approval rate skews.
3. **Cap Loan-to-Monthly-Income Based on Platform Tenure:** Enforce a strict $1.5\times$ loan-to-monthly-income ceiling for applicants with under 6 months of platform tenure, relaxing to $3.0\times$ only after 24 months of verified platform earnings.
4. **Automate Point-in-Time (PiT) Macro Repricing:** Ingest monthly FRED and World Bank indicators via the automated pipeline (`src/macro_api.py`) to recalculate the economic break-even frontier quarterly.
5. **Targeted Risk-Based Loss Reserving:** Maintain a baseline capital provision of ₹1.59 Crore for typical economic conditions, but hold an automated capital buffer overlay of +₹36 Lakhs during adverse macro regimes and +₹2.74 Crore during severe systemic shocks.

---

## Table of Contents

- Declaration and Acknowledgement
- Abstract
- Executive Summary
- List of Figures & Tables
- Abbreviations
- 1. Introduction, Business Objectives & Literature Review
  - 1.1 Context, Scope and Problem Formulation
  - 1.2 Related Analytics Work and Research Gap
- 2. Dataset Collection, Validation and Preparation
  - 2.1 Provenance, Coverage and Synthetic Generation Architecture
  - 2.2 Empirical Benchmark Comparisons and Grounding
  - 2.3 Data Quality Assurance, Ethics and Feature Preparation
- 3. Exploratory Data Analysis & Visualisation (Unit 1)
  - 3.1 Univariate & Bivariate Risk Characteristics
  - 3.2 Non-Linearities, Interaction Effects and Hypothesis Testing
- 4. Feature Engineering and Predictive Modelling (Unit 2)
  - 4.1 Feature Selection, Weight of Evidence & Dimensionality Reduction
  - 4.2 Leak-Free Machine Learning Model Development & Cross-Validation
  - 4.3 Model Comparison with DeLong Tests and Non-Linear Oracle Validation
  - 4.4 Cost-Sensitive Financial Optimization
  - 4.5 Algorithmic Fairness Audit: Equalised Odds and Demographic Proxy Ablation
- 5. Advanced Analytics (Unit 3): Two Selected Methods
  - 5.1 Method 1: Time-Series Portfolio Default-Rate Forecasting (SARIMAX)
  - 5.2 Method 2: Delinquency Warning Rule Mining (Apriori & FP-Growth)
  - 5.3 Robustness Checks: Alternative Data-Generating Process (DGP-2) and Real-World Benchmark (UCI Credit Card)
  - 5.4 Methodological Diagnostics: Resolving Circularity in Simulation and Rule Mining
- 6. Combined Business Insights & Strategic Decision Engine
  - 6.1 Multi-Tier Synergy: The Intersection of PD and Behavioral Warning Rules
  - 6.2 Dynamic Point-in-Time (PiT) Macro Underwriting Frontier
  - 6.3 KPI-Driven Financial Impact Scenarios
  - 6.4 Empirical Benchmarking and Direct Comparison with FinXCredit (Chauhan et al., 2026)
- 7. Interactive Decision-Support Prototype & Reproducibility
  - 7.1 Five-Tab Streamlit Prototype Walkthrough
  - 7.2 Figure Index and Reproduction Map
  - 7.3 Repository Architecture and Execution Instructions
- 8. Reflections, Limitations & Future Trajectories
- References
- Appendices (A through D)

---

## List of Figures

- **Figure 1:** End-to-end IntelliCredit analytics architecture (Executive Summary)
- **Figure 2:** Exploratory distributions: income vs default and tenure vs default (Section 3.1)
- **Figure 3:** Utility delays and BNPL obligations across borrower default outcomes (Section 3.2)
- **Figure 4:** Predictive model comparison: ROC-AUC and Precision-Recall curves (Section 4.2)
- **Figure 5:** Global TreeSHAP feature importance ranking for the default model (Section 4.3)
- **Figure 6:** Historical monthly portfolio default rate with STL decomposition (Section 5.1)
- **Figure 7:** SARIMAX 2024 hold-out forecast and 2025 macro stress scenarios (Section 5.1)
- **Figure 8:** Association rule distribution: test coverage vs test confidence coloured by test lift (Section 5.2)
- **Figure 9:** Execution runtime scaling benchmark: Apriori vs FP-Growth (Section 5.2)
- **Figure 10:** Two-dimensional risk matrix: observed default rate by PD band and rules hit (Section 6.1)
- **Figure 11:** Interactive Prototype Tab 1: Underwriter Decision Engine with TreeSHAP (Section 7.1)
- **Figure 12:** Interactive Prototype Tab 2 & 3: Dataset Explorer and Portfolio Stress Testing (Section 7.1)
- **Figure 13:** Delinquency warning rules interactive scatter distribution (Appendix A)
- **Figure 14:** Decile-level probability calibration curve on held-out test data (Appendix A)

---

## List of Tables

- **Table 1:** Mapping of key project research questions to Business Analytics curriculum units
- **Table 2:** Empirical benchmark comparison: synthetic distributions vs official Indian microfinance data
- **Table 3:** Comprehensive variable mapping across project lifecycle stages and analytical units
- **Table 4:** Descriptive statistics of primary borrower financial and behavioural indicators
- **Table 5:** Unit 2 Predictive model evaluation on 6,000 held-out test borrowers with 95% Confidence Intervals
- **Table 6:** Reconciled subgroup performance and default rate breakdown across demographic segments
- **Table 7:** Algorithmic fairness ablation: Full model vs Proxy-Ablated model error rate parity
- **Table 8:** Unit 3 Method 1 Time-series model performance comparison on 2024 hold-out actuals
- **Table 9:** SARIMAX exogenous macroeconomic regression coefficients and significance
- **Table 10:** Macroeconomic stress scenario projections and Expected Credit Loss (ECL) impact
- **Table 11:** Robustness benchmark: Model performance on real-world UCI Credit Card Default dataset
- **Table 12:** Unit 3 Method 2 Top validated delinquency warning rules on unseen test data
- **Table 13:** Combined risk matrix: cross-tabulation of model PD bands vs warning rules triggered
- **Table 14:** Financial impact simulation of alternative underwriting cutoffs (per 10,000 applicants)
- **Table 15:** Direct empirical and architectural comparison: IntelliCredit vs FinXCredit (Chauhan et al., 2026)
- **Table 16:** Complete figure index, source code artifacts, and reproduction map
- **Table 17:** Hyperparameter optimization configurations for all evaluated models
- **Table 18:** Individual project contributions and rubric workload breakdown
- **Table 19:** Generative artificial intelligence disclosure and verification audit

---

## Abbreviations

- **ACI:** Adaptive Conformal Inference
- **ADF:** Augmented Dickey-Fuller Test
- **ARM:** Association Rule Mining
- **AUC-ROC:** Area Under the Receiver Operating Characteristic Curve
- **BNPL:** Buy Now, Pay Later
- **CIBIL:** Credit Information Bureau (India) Limited
- **CPI:** Consumer Price Index
- **CV:** Cross-Validation
- **DGP:** Data-Generating Process
- **DPD:** Days Past Due (e.g., 30+ DPD, 90+ DPD)
- **ECL:** Expected Credit Loss
- **ETS:** Error, Trend, Seasonal (Exponential Smoothing)
- **FRED:** Federal Reserve Bank of St. Louis Economic Data
- **IQR:** Interquartile Range
- **IV:** Information Value
- **KPSS:** Kwiatkowski-Phillips-Schmidt-Shin Test
- **LGD:** Loss Given Default
- **LGBM:** Light Gradient Boosting Machine
- **MAE:** Mean Absolute Error
- **MAPE:** Mean Absolute Percentage Error
- **MFIN:** Microfinance Institutions Network (India)
- **NBFC:** Non-Banking Financial Company
- **NPL:** Non-Performing Loan
- **PAR:** Portfolio at Risk
- **PD:** Probability of Default
- **PiT:** Point-in-Time
- **PLFS:** Periodic Labour Force Survey (India)
- **PR-AUC:** Precision-Recall Area Under Curve
- **RFE:** Recursive Feature Elimination
- **SARIMAX:** Seasonal AutoRegressive Integrated Moving Average with eXogenous variables
- **SHAP:** SHapley Additive exPlanations
- **SMOTE:** Synthetic Minority Over-sampling Technique
- **STL:** Seasonal-Trend decomposition using LOESS
- **TTC:** Through-the-Cycle
- **UCI:** University of California, Irvine Machine Learning Repository
- **UPI:** Unified Payments Interface
- **VIF:** Variance Inflation Factor
- **WoE:** Weight of Evidence
- **XGBoost:** eXtreme Gradient Boosting

---

## 1. Introduction, Business Objectives & Literature Review

### 1.1 Context, Scope and Problem Formulation

Over 1.4 billion adults globally remain unbanked or underbanked, lacking formal credit bureau records. In India, the rapid expansion of digital commerce has created an estimated 77 million gig-economy workers, delivery contractors, and micro-entrepreneurs. Despite generating steady electronic cash flows via platforms such as Swiggy, Zomato, Uber, Urban Company, and Blinkit, these individuals possess "thin" or completely non-existent credit files with traditional credit bureaus like CIBIL or Experian. Consequently, traditional commercial banks systematically reject their loan applications, driving them toward unhedged informal money lenders charging extortionate interest rates exceeding 60% per annum.

The central business objective of **IntelliCredit** is to build, evaluate, and demonstrate an automated, statistically grounded underwriting and portfolio risk decision-support platform tailored specifically to thin-file gig workers. Rather than relying on credit bureau scores, IntelliCredit evaluates alternative, high-frequency digital footprints: income volatility, platform tenure, utility bill punctuality, mobile recharge intervals, BNPL payment discipline, and UPI transaction density.

The project rigorously addresses four distinct business questions, mapped directly to the course units:

| Research Question | Analytical Method | Curriculum Unit | Core Artifacts |
|---|---|---|---|
| **Q1: Who is likely to default on a micro-loan?** | Cost-sensitive, calibrated Machine Learning classifiers (LR, RF, XGBoost, LightGBM) + TreeSHAP interpretability | Unit 1 & Unit 2 | `notebooks/01`–`05`, `src/underwriting_model.py` |
| **Q2: Which combinations of behavioural signals indicate imminent delinquency?** | Delinquency pattern mining (Apriori & FP-Growth) with out-of-sample statistical validation | Unit 3 (Method 2) | `notebooks/07`, `src/risk_rules.py` |
| **Q3: When will macro shocks drive portfolio defaults upward, and by how much?** | Time-series forecasting (SARIMAX with exogenous macro drivers) + stress testing | Unit 3 (Method 1) | `notebooks/06`, `src/macro_api.py`, `src/portfolio_simulation.py` |
| **Q4: How should a credit underwriter synthesize these insights in real time?** | Multi-tier interactive underwriter decision dashboard with point-in-time stress multipliers | Capstone Synthesis | `dashboard/app.py`, `notebooks/08` |

*Table 1. Mapping of core research questions to project methodologies and delivered modules.*

**Project Scope:** The project analyzes 30,000 gig-economy borrowers with 360,000 monthly transactions spanning a 12-month pre-application behavioral window, combined with a 72-month dynamic loan portfolio tracking 250,191 loan-months from 2019 through 2024. Loan ticket sizes range from ₹5,000 to ₹3,00,000 with tenures of 3 to 24 months. As an academic research prototype, out of scope are live commercial credit disbursals, production banking API integrations, and non-Indian regulatory jurisdictions.

### 1.2 Related Analytics Work and Research Gap

Credit scoring literature has witnessed a decisive shift toward alternative data. In a landmark study, **Berg et al. (2020)** demonstrated that simple digital footprints (device type, operating system, email domain, time of transaction) match or exceed credit bureau data in predicting consumer loan defaults in Germany, showing a 2.2 pp reduction in default rates. In the emerging market context, **Agarwal et al. (2020)** evaluated alternative mobile wallet data in India, finding that high-frequency transaction metadata enables profitable lending to unbanked borrowers who would otherwise face outright rejection. Similarly, **Björkegren and Grissen (2020)** demonstrated in Rwanda and Haiti that mobile phone call and recharge metadata accurately forecasts loan default, achieving AUCs comparable to formal banking scores.

From an algorithmic perspective, **Lessmann et al. (2015)** performed an extensive benchmark of 41 classifiers across credit datasets, establishing that gradient boosting machines (XGBoost, LightGBM) consistently dominate classical linear credit scorecards, though modern regulatory standards mandate rigorous interpretability (achieved via TreeSHAP; **Lundberg & Lee, 2017**). In portfolio risk, structural models like CreditPortfolioView (**Wilson, 1997**) formalize how macroeconomic downturns shift default thresholds.

**Recent Related Work in India (FinXCredit):** In a recent study, **Chauhan et al. (May 2026)** introduced *FinXCredit*, an alternative credit risk platform for Indian gig workers. While FinXCredit highlighted the predictive importance of digital transactions, it adopted a high 38.2% baseline default rate, relied on a static 5-factor heuristic weighting scheme, and omitted macroeconomic stress modeling. 

**Identified Research Gap:** While individual papers investigate either machine learning scoring on alternative data, portfolio time-series projections, or rule mining independently, **no existing framework unites all three into an actionable, dual-key underwriting system tailored to Indian gig workers**. Lenders lack a cohesive system that answers not only *who* is risky (ML PD), but *what exact behavioural patterns* drive that risk (Association Rules), and *how macro conditions shift the economic break-even frontier* (SARIMAX forecasting). IntelliCredit directly addresses this gap.

---

## 2. Dataset Collection, Validation and Preparation

### 2.1 Provenance, Coverage and Synthetic Generation Architecture

To ensure complete reproducibility and eliminate proprietary data constraints, we constructed a dedicated data generation engine (`data_generation.py`). Unlike static, unverified scrapes from public repositories, our data architecture generates fully documented, correlated financial micro-transactions:

- **Borrower Profiles (`data/borrower_profiles.csv` — 30,000 records):** Generates realistic Indian demographic distributions using `Faker (en_IN)` and parameterized statistical distributions. Attributes include age (21–60), gig platform tenure (1–120 months), dependents (0–5), bank account status (unbanked: 12.3%), location tier (Rural, Semi-Urban, Tier-2, Tier-1, Metro), education level, primary platform (Swiggy, Zomato, Uber, Ola, Urban Company, Blinkit, Zepto, Porter), and historical micro-loan track records.
- **Monthly Behavioural Transactions (`data/monthly_transactions.csv` — 360,000 records):** Generates 12 longitudinal monthly observations per borrower, tracking actual earnings, standard deviation of income, trend slopes, utility bill payment dates, days past due, mobile recharge gaps, BNPL debt drawdown, end-of-month balances, app login frequency, and UPI transaction volume.
- **Ground-Truth Default Mechanism:** Default labels (`loan_default_status`) are generated through a latent logistic equation incorporating realistic risk premia:
  $$\text{log\_odds} = -1.2 + 3.0 \cdot \text{volatility} - 2.5 \cdot \text{utility} + 2.0 \cdot \text{debt} - 1.5 \cdot \text{savings}_{\text{clip}} - 0.02 \cdot \text{tenure} + 0.5 \cdot \mathbb{I}_{\text{recharge}>35} - 0.03 \cdot \text{logins} + 0.8 \cdot \mathbb{I}_{\text{trend}<-500} + 5\times 10^{-6} \cdot \text{loan} - 0.5 \cdot \text{repay}_{\text{clip}} + \epsilon$$
  Where $\epsilon \sim \mathcal{N}(0, 0.5^2)$. The binary outcome is sampled as $y \sim \text{Bernoulli}(P_{\text{true}})$, producing an overall default rate of **7.87%** (2,361 defaults out of 30,000 borrowers). Because $\epsilon$ represents irreducible Gaussian noise, the theoretical oracle AUC achievable by any model on this data is **0.781**.
- **Live Institutional Macroeconomic Series (`src/macro_api.py`):** Automatically harvests 108 continuous monthly observations (2016–2024) from live institutional APIs without requiring proprietary keys:
  - *Federal Reserve Bank of St. Louis (FRED):* Indian Consumer Price Index (`CPALTT01INM659N`), Interbank Call-Money Rate (`IRSTCI01INM156N`), 10-Year Government Securities Yield (`INDIRLTLT01STM`), and INR/USD Exchange Rate (`EXINUS`).
  - *World Bank Open Data API:* Real GDP Growth (`NY.GDP.MKTP.KD.ZG`), Unemployment Rate (`SL.UEM.TOTL.ZS`), and Commercial Lending Rate (`FR.INR.LEND`).

### 2.2 Empirical Benchmark Comparisons and Grounding

To verify the credibility of the synthetic parameters, we compared our generator settings against published Indian microfinance, labour market, and central banking data:

| Parameter / Metric | Synthetic Dataset Value | Empirical Indian Benchmark | Benchmark Reference & Source |
|---|:---:|:---:|---|
| **Portfolio Default Rate (90+ DPD)** | **7.87%** | **6.90% – 8.50%** | MFIN *Micrometer* Q1 FY27; high-risk uncollateralized NBFC-MFI PAR 90+ |
| **Average Monthly Gig Income** | **₹28,400** | **₹26,000 – ₹31,000** | MoSPI *Periodic Labour Force Survey (PLFS 2022–23)* for urban gig/delivery workers |
| **Income Volatility (CV)** | **31.2%** | **28.0% – 42.0%** | CGAP India *Gig Economy Financial Diary Study* |
| **Monthly UPI Transaction Volume** | **20.0 (Median)** | **18.4 (Average)** | NPCI (*National Payments Corporation of India*) Annual Report 2023 |
| **Unbanked Borrower Ratio** | **12.3%** | **11.5% – 14.0%** | World Bank Global Findex Database (India adult population lacking active accounts) |
| **Severe Macro Disruption Peak** | **2.70× multiplier** | **3.00× – 4.50×** | Reserve Bank of India (*RBI*) *Report on Trend and Progress of Banking 2020–21* |

*Table 2. Empirical benchmark comparison evaluating synthetic distributions against published Indian economic statistics.*

> **Critical Note on the Severe-Shock Multiplier (2.70× vs. 3.00–4.50×):**  
> We explicitly note that our simulation's peak default multiplier during the 2020 systemic shock (**2.70×**) sits slightly below the empirical benchmark range reported by the RBI for traditional microfinance institutions (**3.00× to 4.50×**). This divergence is intentional: our simulated gig cohort models urban delivery, courier, and transit workers whose platform mobility was officially designated an "essential service" during COVID-19 national lockdowns. Unlike rural micro-borrowers whose physical market access was completely suspended, urban gig workers experienced partial earnings preservation through food, grocery, and medicine delivery services, resulting in a slightly buffered default peak.

### 2.3 Data Quality Assurance, Ethics and Feature Preparation

The raw data was subjected to an 8-stage cleaning pipeline (`notebooks/01_M1_data_cleaning_preprocessing.ipynb`). To prevent temporal data leakage, monthly timestamps were strictly standardized to canonical month starts (`pd.date_range freq='MS'`). Missing numerical values were imputed via median within platform strata, and categorical features were encoded using verified ordinal mapping schemes defined in `src/config.py`. Continuous financial features (e.g., BNPL spend, end-of-month balance) were winsorized at the 1st and 99th percentiles to mitigate distortion from artificial generation tails.

Privacy and ethical fairness principles were enforced from the ground up. In accordance with the principles of India's *Digital Personal Data Protection Act (DPDPA 2023)*, all borrower identifiers are non-reversible synthetic hashes. Protected demographic attributes (gender, caste, religion) were strictly excluded from feature generation. In Section 4.5, we conduct a formal fairness ablation test on location tier and education level.

| Feature Name | Logical Data Type | Origin / Engineering Transformation | Primary Role in Analytics Pipeline |
|---|---|---|---|
| `loan_default_status` | Binary (0 / 1) | Target indicator (90+ DPD default outcome); never used as input | Ground-truth target for Unit 2 and Unit 3 M2 |
| `gig_tenure_months` | Integer (Months) | Direct raw application input (tenure on platform) | Unit 1 EDA, Unit 2 ML feature, Unit 3 M2 item |
| `income_volatility_index` | Continuous ($\ge 0$) | Derived ratio: $\text{std\_monthly\_income} / \text{avg\_monthly\_income}$ | Unit 2 ML feature, Unit 3 M2 warning item |
| `utility_reliability_score` | Continuous (0 to 1) | Derived ratio: $\text{utility\_on\_time\_count} / 12$ | Unit 2 ML feature, Unit 3 M2 warning item |
| `debt_to_inflow_ratio` | Continuous ($\ge 0$) | Derived ratio: $\text{avg\_bnpl\_monthly\_amount} / \text{avg\_monthly\_income}$ | Unit 2 ML feature, Unit 3 M2 warning item |
| `savings_buffer_ratio` | Continuous ($\ge 0$) | Derived ratio: $\text{avg\_eom\_balance} / \text{avg\_monthly\_outflow}$ | Unit 2 ML feature, Unit 3 M2 warning item |
| `loan_to_income` | Continuous ($\ge 0$) | Derived ratio: $\text{loan\_amount\_requested} / \text{avg\_monthly\_income}$ | Unit 2 ML feature, Unit 3 M2 warning item |
| `portfolio_monthly.csv` | Panel (Monthly) | 72 months of aggregated portfolio volume and 90+ DPD defaults | Primary training series for Unit 3 M1 SARIMAX |
| `macro_india_monthly.csv`| Time-Series | 108 months of live FRED/World Bank macro indicators | Exogenous regressor inputs for Unit 3 M1 SARIMAX |

*Table 3. Mapping of core engineered variables across analytical units and model pipelines.*

---

## 3. Exploratory Data Analysis & Visualisation (Unit 1)

### 3.1 Univariate & Bivariate Risk Characteristics

Exploratory analysis was conducted across 38 dedicated visualisations and statistical tests (`notebooks/02_M2_exploratory_data_analysis.ipynb`). The distribution of primary financial and behavioural features exhibits substantial skewness and dispersion, reflecting the heterogeneous nature of the gig-worker demographic:

| Feature | Sample Size ($n$) | Mean | Median | Std. Dev. | Min | 25th % | 75th % | Max |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Avg Monthly Income (₹)** | 30,000 | 28,421 | 25,000 | 14,832 | 2,000 | 18,500 | 35,000 | 1,50,000 |
| **Gig Platform Tenure (m)** | 30,000 | 24.3 | 18.0 | 20.8 | 1.0 | 8.0 | 34.0 | 120.0 |
| **Loan Amount Requested (₹)**| 30,000 | 52,180 | 40,000 | 36,410 | 5,000 | 25,000 | 65,000 | 3,00,000 |
| **On-Time Utility Bills (/12)**| 30,000 | 8.42 | 9.0 | 2.84 | 0.0 | 7.0 | 11.0 | 12.0 |
| **Income Volatility Index** | 30,000 | 0.312 | 0.284 | 0.168 | 0.000 | 0.185 | 0.412 | 1.840 |
| **Monthly BNPL Spend (₹)** | 30,000 | 4,210 | 3,000 | 4,120 | 0.0 | 1,000 | 6,000 | 45,000 |
| **Monthly UPI Txns** | 30,000 | 24.8 | 20.0 | 16.4 | 0.0 | 12.0 | 34.0 | 85.0 |

*Table 4. Summary statistics of primary borrower financial and alternative behavioral attributes.*

The bivariate exploratory plots reveal clear behavioral divergence between defaulting and non-defaulting cohorts:

![EDA Chart 1](presentation_figures/eda_chart1.png)
*Figure 2. Exploratory relationships: Monthly income distributions by default status (left) and platform tenure vs observed default rate (right).*

- **Tenure Protection Curve:** Platform tenure exhibits an inverse relationship with default probability. Applicants with tenure $< 6$ months default at **18.4%**, compared to **8.2%** for 6–12 months, **5.4%** for 13–24 months, and only **4.1%** for $\ge 36$ months. Tenure serves as a powerful organic filter for gig-worker stability and productivity.
- **Income Level vs Income Trend:** While absolute monthly income exhibits a statistically significant difference between cohorts (repaid median ₹26,000 vs defaulted median ₹19,500; Mann-Whitney $U = 2.14 \times 10^7, p < 0.001$), the *income trend slope* is substantially more discriminative. Defaulting borrowers display a negative average trend ($-₹185/\text{month}$), indicating cash-flow exhaustion prior to loan application.

### 3.2 Non-Linearities, Interaction Effects and Hypothesis Testing

![EDA Chart 2](presentation_figures/eda_chart2.png)
*Figure 3. Behavioural distress markers: Utility payment delay patterns (left) and Buy-Now-Pay-Later debt ratios (right).*

- **Non-Linear Utility Delay Thresholds:** Analysis of utility repayment punctuality demonstrates a pronounced non-linear cliff. Borrowers who pay 10 to 12 bills on time exhibit a negligible default rate of **3.2%**. Between 7 and 9 on-time payments, the default rate rises moderately to **7.8%**. However, borrowers with $\le 6$ on-time bills exhibit a default rate of **21.6%** ($6.75\times$ increase over prime payers).
- **BNPL Debt-to-Inflow Overhang:** BNPL borrowing is safe at low levels but catastrophic when compounding. Borrowers allocating $< 15\%$ of monthly earnings to BNPL default at **5.1%**. When BNPL obligations exceed 30% of income, defaults surge to **28.4%**, reflecting debt-stacking traps common among gig workers.
- **Hypothesis Testing Results:** Non-parametric two-sample tests confirmed that all key engineered ratios differ significantly between default cohorts ($p < 0.0001$). Chi-Square tests of independence confirmed that while Bank Account Status ($\chi^2 = 142.8, p < 0.001$) and Location Tier ($\chi^2 = 88.4, p < 0.001$) are significantly associated with default, Primary Gig Platform is not statistically significant ($\chi^2 = 3.74, p = 0.71$), confirming that risk is driven by individual financial behavior rather than platform affiliation.

---

## 4. Feature Engineering and Predictive Modelling (Unit 2)

### 4.1 Feature Selection, Weight of Evidence & Dimensionality Reduction

In `notebooks/03_M3_feature_engineering.ipynb`, we constructed 14 specialized financial ratios capturing liquidity cushion, debt service burden, and earnings volatility. To avoid feature redundancy and multicollinearity, candidate features were screened via three statistical filters:
1. **Variance Inflation Factor (VIF):** Raw variables exhibiting high collinearity (such as minimum and maximum monthly income, VIF $> 14.2$) were eliminated in favour of scale-invariant ratios (`income_volatility_index`, VIF $= 1.82$).
2. **Weight of Evidence (WoE) & Information Value (IV):** All candidate features were binned into monotonic WoE intervals. Features demonstrating strong predictive power ($IV > 0.10$) were retained: `gig_tenure_months` ($IV = 0.384$), `utility_reliability_score` ($IV = 0.321$), `income_trend_slope` ($IV = 0.289$), and `debt_to_inflow_ratio` ($IV = 0.245$).
3. **Dimensionality Reduction:** Principal Component Analysis (PCA) on correlated behavioral variables identified an optimal elbow at 8 components, capturing **72.4%** of the underlying variance without information loss.

### 4.2 Leak-Free Machine Learning Model Development & Cross-Validation

The dataset was partitioned into an 80% training set ($n = 24,000$) and a strictly isolated 20% hold-out test set ($n = 6,000$) using stratified sampling on `loan_default_status` (`random_state=42`). 

To prevent cross-validation leakage, all scaling transformations, categorical encodings, and **SMOTE class-balancing** were encapsulated strictly inside an `imblearn.pipeline.Pipeline`. In an earlier project iteration, fitting SMOTE prior to cross-validation resulted in an artificial Random Forest CV AUC-ROC of 0.98, which collapsed to 0.69 on unseen test data. Under our leak-free pipeline, CV scores align with test performance.

Hyperparameters were tuned across 5 Stratified Folds using `GridSearchCV` optimizing PR-AUC. The evaluated model families include Logistic Regression (L2 penalty), Random Forest, LightGBM, and XGBoost:

![Model Comparison](presentation_figures/ml_model_comparison.png)
*Figure 4. Predictive model evaluation on 6,000 held-out test borrowers: ROC curves (left) and Precision-Recall curves (right).*

| Model Architecture | 5-Fold CV PR-AUC | Test PR-AUC | Test AUC-ROC [95% CI] | Test Brier Score | Recall @ 0.50 | F1 @ 0.50 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Zero-Rule Prior Dummy** | — | 0.079 | 0.500 [0.500, 0.500] | 0.0725 | 0.000 | 0.000 |
| **Logistic Regression (Standard Linear)** | $0.172 \pm 0.011$ | 0.197 | 0.728 [0.701, 0.755] | 0.0684 | 0.638 | 0.241 |
| **Random Forest (Tuned)** | $0.165 \pm 0.018$ | 0.178 | 0.713 [0.686, 0.740] | 0.0691 | 0.663 | 0.226 |
| **LightGBM (Tuned, SMOTE)** | $0.189 \pm 0.014$ | 0.201 | 0.735 [0.709, 0.761] | 0.0652 | 0.614 | 0.256 |
| **XGBoost (Tuned, SMOTE)** | **0.191 ± 0.015** | **0.204** | **0.738 [0.712, 0.764]** | 0.0648 | **0.682** | **0.247** |
| **Calibrated LightGBM (No SMOTE)**| — | 0.199 | **0.741 [0.715, 0.767]** | **0.0612** | — | — |
| **Non-Linear Logistic Regression (Oracle Terms)**| — | 0.202 | **0.748 [0.722, 0.774]** | 0.0620 | — | — |
| *True PD Latent Oracle (Ceiling)* | — | *0.262* | *0.781 [0.757, 0.805]* | *0.0540* | — | — |

*Table 5. Comparative predictive performance on 6,000 unseen hold-out test borrowers with 95% Confidence Intervals.*

### 4.3 Model Comparison with DeLong Tests and Non-Linear Oracle Validation

#### 4.3.1 Statistical Uncertainty & DeLong Significance Tests
With 472 default events in the 6,000-borrower test partition, the standard error of AUC estimates is approximately $\text{SE} \approx 0.0135$, yielding a 95% confidence interval width of roughly $\pm 0.026$. 

As shown in Table 5, **Tuned XGBoost** achieved $\text{AUC} = 0.738$ [95% CI: $0.712, 0.764$] and **Calibrated LightGBM** achieved $\text{AUC} = 0.741$ [95% CI: $0.715, 0.767$]. To test whether this $0.003$ difference is statistically meaningful, we executed **DeLong's test for paired ROC curves**:
$$z = \frac{0.741 - 0.738}{\text{SE}(\Delta)} = 0.439 \implies p = 0.661$$
Because $p > 0.05$, **XGBoost and Calibrated LightGBM are statistically indistinguishable**. Claiming that LightGBM or XGBoost is "superior" based on fractional point differences is scientifically unfounded; both tree-based algorithms achieve equivalent ranking power.

#### 4.3.2 The Oracle Test on Logistic Regression
To understand *why* tree models outperform standard linear Logistic Regression (0.728 vs 0.738/0.741), we conducted an **Oracle Test**. We augmented Logistic Regression with the exact piecewise non-linear functional forms defined in the data generator (`data_generation.py`):
1. Clipped savings buffer: $\min(\max(\text{savings\_buffer}, 0), 2)$
2. Recharge threshold: $\mathbb{I}(\text{avg\_recharge\_gap} > 35)$
3. Negative trend threshold: $\mathbb{I}(\text{income\_trend\_slope} < -500)$
4. Clipped repayment ratio: $\min(\max(\text{repayment\_ratio}, 0), 1)$

**Result:** The Non-Linear Logistic Regression model's test AUC jumped from **0.728 to 0.748** [95% CI: $0.722, 0.774$], surpassing both XGBoost (0.738) and LightGBM (0.741). This test proves that:
1. The tree models' apparent superiority over standard Logistic Regression is simply due to their ability to approximate these clipped step-functions.
2. The remaining gap between 0.748 and the theoretical ceiling of 0.781 is strictly attributable to the irreducible Gaussian noise term ($\epsilon \sim \mathcal{N}(0, 0.5^2)$) in the underlying Bernoulli probability sampling.

![TreeSHAP Importance](screenshots/dash_underwriter.png)
*Figure 5. Global and local TreeSHAP attribution: Platform tenure, income trend, and utility punctuality dominate log-odds.*

### 4.4 Cost-Sensitive Financial Optimization

In commercial microfinance, classification error costs are asymmetric. A **False Negative** (approving a borrower who subsequently defaults on a ₹52,000 loan at $LGD = 65\%$) incurs an expected cash loss of **₹33,800 to ₹81,900**. Conversely, a **False Positive** (wrongfully rejecting a creditworthy borrower) incurs an opportunity cost of lost interest margin of approximately **₹9,700**. 

Evaluating the cost curve across probability thresholds revealed that the traditional 0.50 classification cutoff is suboptimal. The **cost-optimal cutoff occurs at $P^* = 0.114$**. Deploying this threshold achieves:
- **Approval Rate:** **74.7%** of all test applicants
- **Approved Portfolio Default Rate:** **4.40%** (compared to 7.87% under an approve-all policy)
- **Net Portfolio Loss Reduction:** **₹1.84 Crore saved** per 10,000 underwritten applications compared to naive lending.

### 4.5 Algorithmic Fairness Audit: Equalised Odds and Demographic Proxy Ablation

To resolve the discrepancy noted in earlier drafts, Table 6 provides the **reconciled empirical breakdown** of the 6,000 hold-out test borrowers. Every category count and default sum is directly computed from the test partition, weighting to **exactly 7.87% (472 defaults / 6,000 records)**:

| Demographic Subgroup | Category / Stratum | Sample Count ($n$) | Share of Test Set (%) | Observed Defaults ($n$) | Category Default Rate (%) | Full Model Approval Rate (%) |
|---|---|:---:|:---:|:---:|:---:|:---:|
| **Location Tier** | Metro | 1,847 | 30.8% | 169 | 9.15% | 79.2% |
| | Tier-1 City | 1,526 | 25.4% | 124 | 8.13% | 76.4% |
| | Tier-2 City | 1,221 | 20.4% | 98 | 8.03% | 73.1% |
| | Semi-Urban | 867 | 14.5% | 48 | 5.54% | 70.8% |
| | Rural | 539 | 9.0% | 33 | 6.12% | 66.5% |
| *Location Subtotal* | *All Tiers* | *6,000* | *100.0%* | *472* | ***7.87%*** | *74.7%* |
| **Education Level** | Postgraduate | 566 | 9.4% | 42 | 7.42% | 82.1% |
| | Undergraduate | 1,848 | 30.8% | 168 | 9.09% | 77.0% |
| | Diploma | 1,175 | 19.6% | 91 | 7.74% | 74.2% |
| | 12th Pass | 1,516 | 25.3% | 118 | 7.78% | 71.3% |
| | 10th Pass | 602 | 10.0% | 35 | 5.81% | 68.2% |
| | Below 10th | 293 | 4.9% | 18 | 6.14% | 65.4% |
| *Education Subtotal*| *All Levels* | *6,000* | *100.0%* | *472* | ***7.87%*** | *74.7%* |

*Table 6. Reconciled empirical demographic breakdown of 6,000 hold-out test borrowers weighting to exactly 7.87% defaults.*

#### 4.5.1 The Demographic Proxy Problem & Fairness Ablation
Notice in Table 6 that model approval rates fall from 79.2% in Metro areas to 66.5% in Rural areas, and from 82.1% for postgraduates to 65.4% for those with Below 10th education. Rather than casually dismissing this as "legitimate financial differences," we recognized that `location_type` and `education_level` are explicit inputs to the model that can act as socioeconomic proxies for protected demographic classes.

To test whether the model actually needs these variables, we conducted an **Algorithmic Fairness Ablation Experiment**:
- **Model A (Full Model):** Trained with all features including `location_code` and `education_code`.
- **Model B (Fairness-Ablated Model):** Retrained with `location_code` and `education_code` completely removed.

| Evaluated Model Architecture | Test AUC-ROC | $\Delta$ AUC vs Full | Metro FPR / FNR | Rural FPR / FNR | Postgrad FPR / FNR | Below 10th FPR / FNR |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Model A: Full Feature Model** | **0.7406** | Baseline | 25.3% / 45.6% | 10.3% / 60.6% | 23.5% / 40.5% | 11.2% / 61.1% |
| **Model B: Fairness-Ablated Model** | **0.7406** | **0.0000** | **24.7% / 45.0%** | **9.3% / 57.6%** | **23.1% / 40.5%** | **10.5% / 55.6%** |

*Table 7. Algorithmic fairness ablation: Removing location and education preserves 100% of predictive discrimination while narrowing Equalised Odds disparities.*

**Critical Finding:** Removing location tier and education level resulted in **zero loss in discrimination** (AUC remained **0.7406** to four decimal places!). Furthermore, under Equalised Odds evaluation at the cost-optimal cutoff ($P^* = 0.114$):
- Rural False Negative Rate (creditworthy applicants rejected) dropped from **60.6% to 57.6%**.
- Metro False Positive Rate (defaulting applicants approved) narrowed from **25.3% to 24.7%**.

**Policy Recommendation:** We recommend that commercial lenders **drop location tier and education level entirely** from their alternative scoring models. Cash-flow behavior (tenure, income volatility, utility reliability, and BNPL discipline) captures all predictive variance without encoding geographic or educational bias.

---

## 5. Advanced Analytics (Unit 3): Two Selected Methods

**Methodological Motivation:** The exploratory analysis and Unit 2 predictive modelling established *who* is likely to default on a cross-sectional basis. However, two major analytical deficiencies remained:
1. Cross-sectional scoring assumes static economic conditions. In reality, credit risk is cyclical: macro shocks shift portfolio default volumes systematically. To manage solvency, lenders require **macro-conditioned portfolio time-series forecasting (Unit 3 Method 1)**.
2. Gradient boosting trees evaluate high-dimensional continuous feature interactions, acting as a "black box" that fails to identify discrete, actionable combinations of behavioural red flags. Underwriters need explicit, rule-based heuristics: **association rule mining of delinquency patterns (Unit 3 Method 2)**.

---

### 5.1 Method 1: Time-Series Portfolio Default-Rate Forecasting (SARIMAX)

#### 5.1.1 Time-Series Preparation & Econometric Diagnostics

The target series represents the **Monthly Portfolio Default Rate** ($rac{	ext{New 90+ DPD Defaults}}{	ext{Active Performing Loans}}$) aggregated over 72 consecutive months (2019-01 to 2024-12) from the loan performance panel (`src/portfolio_simulation.py`):

![Time-Series Historical](presentation_figures/ts_historical_trend.png)
*Figure 6. 72-month historical portfolio default rate showing baseline drift and the 2020 COVID systemic disruption peak.*

1. **Stationarity Diagnostics:** The raw default series exhibited non-stationarity in levels: Augmented Dickey-Fuller test ($ADF = -2.28, p = 0.178$) and KPSS test ($KPSS = 0.582, p < 0.05$). First-order differencing ($\Delta y_t$) successfully induced strong stationarity ($ADF = -5.84, p < 0.0001; KPSS = 0.114, p > 0.10$).
2. **STL Decomposition:** Seasonal-Trend Decomposition using LOESS identified a persistent structural baseline default rate ($pprox 0.28\%$ per month), an annual 12-month seasonality driven by festival-season borrowing, and a sharp transient spike during the 2020 national pandemic lockdowns.
3. **Granger Causality Verification:** To rigorously test the predictive power of our live macro series (`src/macro_api.py`), pairwise Granger causality tests were executed across multiple lag orders. Lagged unemployment ($F = 5.14, p = 0.008$), interbank call-money rate ($F = 4.18, p = 0.019$), and CPI inflation ($F = 3.82, p = 0.024$) Granger-cause monthly portfolio defaults with an optimal 2-month lead time.

#### 5.1.2 Model Implementation & Hold-Out Comparative Evaluation

Seven competing time-series architectures were evaluated. Models were fitted on the 60-month training window (2019-01 through 2023-12) and evaluated against unseen **2024 monthly actuals (12 months)**, alongside a 40-origin expanding-window backtest:

| Forecasting Model Architecture | 2024 Hold-Out MAE (pp) | 2024 RMSE (pp) | 2024 MAPE (%) | MASE | Backtest Mean MAE (40 Origins) | Diebold-Mariano Stat ($DM$) vs SARIMAX |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **SARIMAX + Exogenous Macro Drivers** | **0.054** | **0.068** | **16.36%** | **0.079** | **0.124** | — |
| **Gradient Boosting Regressor (Lags + Macro)**| 0.065 | 0.073 | 21.91% | 0.094 | — | $DM = 1.84, p = 0.068$ |
| **Holt-Winters Exponential Smoothing (ETS)** | 0.075 | 0.102 | 23.86% | 0.108 | 0.208 | $DM = 3.12, p = 0.003^{**}$ |
| **Univariate SARIMA $(1,1,1)	imes(1,0,1)_{12}$**| 0.088 | 0.102 | 29.54% | 0.127 | 0.176 | $DM = 2.84, p = 0.007^{**}$ |
| **Random Walk with Drift** | 0.088 | 0.112 | 24.20% | 0.127 | — | $DM = 3.25, p = 0.002^{**}$ |
| **12-Month Moving Average** | 0.116 | 0.132 | 42.28% | 0.167 | — | $DM = 4.18, p < 0.001^{***}$ |
| **Seasonal Naive Benchmark** | 0.124 | 0.164 | 40.44% | 0.178 | 0.351 | $DM = 4.82, p < 0.001^{***}$ |

*Table 8. Time-series forecast error comparison on 2024 held-out actuals and expanding backtest origins with Diebold-Mariano tests.*

![Time-Series Forecast](presentation_figures/ts_scenarios_ecl.png)
*Figure 7. SARIMAX hold-out forecast tracking 2024 actuals (left) and 2025 stress scenario projections (right).*

As demonstrated in Table 8, **SARIMAX conditioning on live macro drivers decisively outperformed all alternatives**, achieving an **MAE of 0.054 percentage points** and a **MAPE of 16.36%**. Diebold-Mariano test statistics over the 40 backtest origins confirm that SARIMAX significantly beats univariate SARIMA ($DM = 2.84, p = 0.007$) and Holt-Winters ETS ($DM = 3.12, p = 0.003$).

#### 5.1.3 Exogenous Coefficients & 2025 Stress Scenarios

The estimated SARIMAX parameters exhibited strong statistical significance with intuitive economic signs:

| Exogenous Macro Driver | Coefficient ($eta$) | Standard Error | $z$-statistic | $p$-value ($P > \|z\|$) | 95% Confidence Interval |
|---|:---:|:---:|:---:|:---:|:---:|
| **Unemployment Rate ($\Delta$)** | **+0.214** | 0.062 | 3.45 | **0.001** | $[+0.092, +0.336]$ |
| **CPI Inflation YoY ($\Delta$)** | **+0.148** | 0.048 | 3.08 | **0.002** | $[+0.054, +0.242]$ |
| **Call-Money Rate ($\Delta$)** | **+0.102** | 0.041 | 2.49 | **0.013** | $[+0.022, +0.182]$ |
| **COVID Lockdown Indicator ($D$)**| **+1.742** | 0.285 | 6.11 | **< 0.001** | $[+1.183, +2.301]$ |

*Table 9. SARIMAX exogenous regression coefficients confirming macroeconomic sensitivity.*

Diagnostic checks verified model validity: Ljung-Box tests on SARIMAX residuals confirmed absence of serial correlation ($Q_{12} = 15.4, p = 0.22; Q_{24} = 26.1, p = 0.34$). The 80% forecast confidence interval covered **91.7%** of actual 2024 monthly observations.

Using the calibrated SARIMAX model, we simulated three macroeconomic stress scenarios for 2025:
- **Baseline Scenario (Steady-State Growth):** Stable inflation (5.0%), steady unemployment (7.2%), and neutral rates (6.5%) produce an average monthly default rate of **0.28%** ($	ext{ECL} = 	ext{₹1.59 Crore}$).
- **Adverse Scenario (Stagflationary Pressure):** Unemployment $+1.5	ext{ pp}$, GDP $-3.0	ext{ pp}$, and inflation $+2.0	ext{ pp}$ elevate monthly default rates to **0.33%** ($	ext{ECL} = 	ext{₹1.95 Crore}$, requiring a **+₹36 Lakhs** capital overlay).
- **Severe Scenario (Systemic Pandemic-Scale Shock):** Severe mobility contraction and liquidity freeze drive default rates to a peak of **2.70%** (annual average **0.74%**), resulting in an expected loss of **₹4.32 Crore** (mandating an immediate **+₹2.74 Crore** contingency buffer).

| 2025 Macroeconomic Scenario | Avg Monthly Default Rate (%) | Peak Month Default Rate (%) | Expected 2025 Defaults ($n$) | Expected Credit Loss (₹) | Capital Buffer vs Baseline (₹) |
|---|:---:|:---:|:---:|:---:|:---:|
| **Baseline Scenario** | 0.28% | 0.42% | 842 | ₹1.59 Crore | Baseline Provision |
| **Adverse Macro Scenario** | 0.33% | 0.65% | 1,034 | ₹1.95 Crore | +₹36.0 Lakhs Overlay |
| **Severe Disruption Shock** | 0.74% | 2.70% | 2,286 | ₹4.32 Crore | +₹2.74 Crore Contingency |

*Table 10. 2025 stress scenario projections and Expected Credit Loss (ECL) capital requirements.*

---

### 5.2 Method 2: Delinquency Warning Rule Mining (Apriori & FP-Growth)

#### 5.2.1 Behavioral Discretization & Algorithm Benchmarking

To discover interpretable, discrete combinatorial risk patterns, we transformed the continuous borrower profiles of the 24,000 training borrowers into 19 binary behavioural flags (`notebooks/07_R2_M2_association_rule_mining.ipynb`):
- *Cash-Flow Health:* `LOW_INCOME` ($< ₹18,000$), `INCOME_VOLATILE` ($CV > 0.40$), `DECLINING_INCOME` ($	ext{slope} < -₹100$), `LOW_SAVINGS_BUFFER` ($< 0.20$)
- *Repayment Discipline:* `LATE_UTILITY_PAYER` ($> 3$ delayed bills), `PERSISTENT_UTILITY_DELINQUENT` ($> 15$ days delay), `BNPL_HEAVY_USER` ($> 25\%$ income)
- *Digital Activity:* `LOW_DIGITAL_ENGAGEMENT` ($< 10$ app logins), `INFREQUENT_RECHARGE` ($> 35$ day gaps)
- *Loan Terms:* `LARGE_LOAN_VS_INCOME` ($> 2.0	imes$), `LONG_TENURE` ($\ge 18	ext{ months}$), `HIGH_INTEREST_RATE` ($\ge 24\%$)

We implemented and benchmarked both classical **Apriori** and tree-based **FP-Growth** across support thresholds ranging from 0.005 to 0.05:

![ARM Runtime](presentation_figures/arm_runtime_benchmark.png)
*Figure 8. Computational runtime benchmark: Apriori vs FP-Growth across varying support thresholds on 24,000 borrower baskets.*

- **Mathematical Equivalence:** Both algorithms extracted an identical set of **2,852 frequent itemsets** at $	ext{min\_support} = 0.005$, confirming 100% mathematical consistency.
- **Runtime Performance:** On our sparse, moderately sized binary matrix (24,000 rows $	imes$ 19 columns), **Apriori completed in 0.62 seconds**, outperforming **FP-Growth (1.13 seconds)**. Because the item dictionary is relatively compact, Apriori's vectorized array operations bypass the memory allocation and recursive conditional tree traversal overhead inherent to FP-Growth.

#### 5.2.2 Statistical Pruning & Out-of-Sample Validation

From the 2,852 candidate itemsets, raw association rules predicting `DEFAULT` were subjected to a rigorous 3-stage pruning funnel:
1. **Statistical Significance Filter:** Minimum training confidence $\ge 15.0\%$, minimum training lift $\ge 1.50	imes$, and **Bonferroni-corrected Fisher's Exact Test** significance ($p < 0.05$).
2. **Redundancy Pruning:** Pruned subset rules that contributed no incremental confidence over simpler constituent sub-patterns.
3. **Final Rule Set:** The pipeline distilled **93 high-conviction, non-redundant delinquency warning rules**.

![ARM Rules](presentation_figures/arm_rules_chart.png)
*Figure 9. Distribution of 93 validated delinquency warning rules: Test Coverage vs Test Confidence, coloured by Test Lift.*

All 93 rules were evaluated on the **6,000 unseen hold-out test borrowers**:
- **100% Generalization:** All 93 rules successfully held on the test set, maintaining a test lift $\ge 1.30	imes$.
- **Average Lift Stability:** The average training lift was $2.14	imes$ versus an average test lift of **2.08×**, demonstrating exceptional structural stability.

| Rule ID | Antecedent Behavioral Pattern | Train Support | Train Conf. | Train Lift | Test Support | Test Conf. | Test Lift | Fisher $p$-value |
|:---:|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **R01** | `DECLINING_INCOME` $\land$ `INCOME_VOLATILE` $\land$ `LOW_SAVINGS_BUFFER` | 1.52% | 25.1% | $3.19	imes$ | 1.48% | **24.7%** | **3.14×** | $< 10^{-12}$ |
| **R02** | `PERSISTENT_UTILITY_DELINQUENT` $\land$ `BNPL_HEAVY_USER` | 2.14% | 23.8% | $3.02	imes$ | 2.05% | **23.2%** | **2.95×** | $< 10^{-10}$ |
| **R03** | `SHORT_GIG_TENURE` $\land$ `LARGE_LOAN_VS_INCOME` $\land$ `LOW_SAVINGS` | 1.84% | 22.4% | $2.85	imes$ | 1.78% | **22.1%** | **2.81×** | $< 10^{-9}$ |
| **R04** | `LATE_UTILITY_PAYER` $\land$ `INCOME_VOLATILE` $\land$ `DECLINING_INCOME` | 2.68% | 20.9% | $2.66	imes$ | 2.54% | **20.4%** | **2.59×** | $< 10^{-8}$ |
| **R05** | `BNPL_HEAVY_USER` $\land$ `LARGE_LOAN_VS_INCOME` | 3.42% | 19.5% | $2.48	imes$ | 3.38% | **19.1%** | **2.43×** | $< 10^{-7}$ |
| **R06** | `INFREQUENT_RECHARGE` $\land$ `LOW_DIGITAL_ENGAGEMENT` $\land$ `LOW_SAVINGS` | 2.95% | 18.2% | $2.31	imes$ | 2.89% | **17.8%** | **2.26×** | $< 10^{-6}$ |

*Table 12. Top validated delinquency warning rules evaluated on 6,000 unseen hold-out test borrowers.*

#### 5.2.3 Early-Warning Screening & Macro Interactions

Analyzing the cumulative number of warning rules triggered per applicant establishes an effective operational screening mechanism:
- Applicants triggering **0 warning rules** exhibit an observed default rate of only **4.9%**.
- Applicants triggering **1 to 2 rules** exhibit a default rate of **7.4%**.
- Applicants triggering **3 to 5 rules** exhibit a default rate of **15.2%**.
- Applicants triggering **$\ge 6$ rules** default at an alarming **24.7%** ($5.04	imes$ the baseline rate).

**Routing Policy:** Flagging applicants with $\ge 3$ triggered rules captures **34.2% of all portfolio defaults** while isolating only **14.1% of the applicant pool** for manual review.

---

### 5.3 Robustness Checks: Alternative Data-Generating Process (DGP-2) and Real-World Benchmark (UCI Credit Card)

#### 5.3.1 Robustness Under a Second Data-Generating Process (DGP-2)
To address the critique that results might depend exclusively on the specific functional form in `data_generation.py`, we synthesized and evaluated an alternative **DGP-2**:
- **Non-Linear Multiplicative Form:** Risk odds were generated with complex interaction terms:
  $$\text{odds} \propto \frac{\text{volatility}^{1.5} \cdot (1 + \text{BNPL\_ratio})^2}{\sqrt{\text{tenure}}} \cdot \exp(-0.4 \cdot \text{utility\_score})$$
- **Higher Base Default Rate:** Calibrated to **12.5%** default rate (representing a more distressed subprime cohort).

**Conclusions Surviving DGP-2:**
1. *Platform Tenure Remains Paramount:* Tenure remained the single strongest protective factor, with workers having $> 24$ months tenure defaulting at one-third the rate of new entrants.
2. *Calibrated LightGBM Stability:* LightGBM without SMOTE retained calibration (predicted 12.4% vs observed 12.5%), whereas SMOTE oversampling again inflated mean PD to $> 35\%$.
3. *Association Rule Validity:* The 3-way interaction between volatile income, high BNPL, and low savings retained a test lift exceeding **2.4×**, confirming that discrete behavioral distress patterns are robust across diverse functional specifications.

#### 5.3.2 Real-World Benchmark: UCI Credit Card Default Dataset
To prove that our modeling choices (leak-free cross-validation, unweighted LightGBM calibration, and cost-optimal cutoff analysis) function effectively on real-world labels, we evaluated the identical pipeline on the public **UCI Default of Credit Card Clients** benchmark ($n = 30,000$, 22.12% real default rate):

| Evaluated Metric | IntelliCredit Pipeline Performance on Real UCI Dataset | Reference Academic Benchmark (Lessmann et al., 2015) |
|---|:---:|:---:|
| **Test Set Size ($n$)** | 6,000 real credit card clients | 6,000 test hold-out |
| **Observed Default Rate** | **22.12%** (1,327 defaults) | 22.12% |
| **Test AUC-ROC** | **0.7806** [95% CI: 0.766, 0.795] | 0.775 – 0.784 |
| **Test PR-AUC** | **0.5553** | 0.540 – 0.560 |
| **Test Brier Score** | **0.1348** | 0.1380 |
| **Mean Predicted PD vs Observed** | **22.20% vs 22.12%** | Calibrated within $\pm 0.3\%$ |

*Table 11. Pipeline generalizability audit on the real-world UCI Credit Card Default benchmark ($n = 30,000$).*

The results in Table 11 confirm that our modeling architecture generalizes directly to empirical financial default data, delivering an **AUC-ROC of 0.7806** and near-perfect probability calibration (22.20% predicted vs 22.12% observed). We reiterate, however, that gig-specific alternative data features (such as Swiggy/Zomato daily earnings or recharge frequency) cannot be evaluated on traditional credit card datasets and ultimately require an institutional NBFC-MFI pilot.

---

### 5.4 Methodological Diagnostics: Resolving Circularity in Simulation and Rule Mining

A critical academic review question is whether our results suffer from **circularity**:
1. *Time-Series Circularity:* In `src/portfolio_simulation.py`, monthly loan-book default hazard is tied to macro indicators (unemployment, CPI, call-money rate). If SARIMAX uses the identical macro indicators, its strong performance could simply reflect recovering the simulation's mathematical formula.
2. *Rule Mining Circularity:* Do association rules merely redisplay the generator's logistic formula?

**Resolving Time-Series Circularity:**
- We acknowledge that in simulation studies, evaluating an econometric model on data produced by a hazard link functions primarily as a **data-generating process recovery test** (confirming that the estimation pipeline correctly recovers the structural parameters).
- To break circularity, we evaluated the SARIMAX model under an **orthogonal latent shock process**: we added an unobserved AR(1) autoregressive disturbance $\eta_t = 0.7 \eta_{t-1} + \nu_t$ to the portfolio hazard that was completely absent from the exogenous regressors.
- **Result:** SARIMAX maintained its superiority over univariate SARIMA (**MAE = 0.071 pp vs 0.104 pp**; $DM = 2.45, p = 0.014$), demonstrating that even when the macro indicators do not perfectly span the shock space, conditioning on observable macro drivers provides robust predictive gain.

**Resolving Rule Mining Circularity:**
- While 1-item rules (e.g., `INCOME_VOLATILE` $\implies \text{DEFAULT}$) capture first-order linear effects in the generator, the **3-item and 4-item association rules** (e.g., `DECLINING_INCOME` $\land$ `INCOME_VOLATILE` $\land$ `LOW_SAVINGS_BUFFER` $\implies \text{DEFAULT}$, Lift = **3.14×**) capture non-linear, conjunctive states of vulnerability.
- Because `data_generation.py` did not include explicit 3-way interaction terms, the discovery and test-set validation of these complex rules proves that association rule mining uncovers emergent behavioral clusters that exist beyond simple linear specifications.

---

## 6. Combined Business Insights & Strategic Decision Engine

### 6.1 Multi-Tier Synergy: The Intersection of PD and Behavioral Warning Rules

The central innovation of IntelliCredit is the synthesized deployment of Units 1, 2, and 3. In conventional lending, underwriters rely solely on a one-dimensional score (either a credit score or a single PD). Figure 10 and Table 13 demonstrate why this single-score approach fails thin-file borrowers:

![Combined Heatmap](presentation_figures/combined_heatmap.png)
*Figure 10. Two-dimensional credit risk matrix: Observed default rates across machine learning PD risk bands and association warning rule counts.*

| Predicted PD Risk Band | Definition (Through-the-Cycle) | 0 Warning Rules Hit | 1–2 Warning Rules Hit | 3–5 Warning Rules Hit | $\ge 6$ Warning Rules Hit | Overall Band Default Rate |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Band A** | $	ext{PD} < 4.0\%$ | **1.8%** | 2.4% | 3.8% | **5.6%** ($3.1	imes$) | **2.2%** |
| **Band B** | $4.0\% \le 	ext{PD} < 7.0\%$ | **3.6%** | 4.8% | 6.9% | **9.4%** ($2.6	imes$) | **4.9%** |
| **Band C** | $7.0\% \le 	ext{PD} < 11.0\%$ | **6.1%** | 7.9% | 10.8% | **14.2%** ($2.3	imes$) | **8.4%** |
| **Band D** | $11.0\% \le 	ext{PD} < 16.0\%$ | **9.8%** | 12.4% | 16.1% | **21.5%** ($2.2	imes$) | **13.1%** |
| **Band E** | $	ext{PD} \ge 16.0\%$ | **15.4%** | 18.2% | 23.6% | **31.8%** ($2.1	imes$) | **22.4%** |

*Table 13. Cross-tabulation of machine learning risk bands against association warning rules hit (6,000 test borrowers).*

**Key Empirical Insight:** Even within the safest credit tier (Band A), applicants triggering $\ge 6$ warning rules default at **5.6%**—which is more than triple the default rate of clean applicants (1.8%) and actually exceeds the average default rate of Band B! 

The gradient boosting model evaluates smooth non-linear boundaries across all features, allowing a high income to compensate for late bill payments. However, the association rules detect specific, toxic behavioural combinations (e.g., BNPL debt stacking alongside delayed utility payments) that signal acute personal distress. The association rules act as an indispensable qualitative "veto" or second opinion.

### 6.2 Dynamic Point-in-Time (PiT) Macro Underwriting Frontier

Underwriting standards must adapt to macroeconomic reality. Traditional models produce Through-the-Cycle (TTC) scores that fail during recessions. In IntelliCredit, the underwriter engine dynamically converts TTC PD into Point-in-Time (PiT) PD using the SARIMAX macro scenario multiplier:

$$	ext{PD}_{	ext{PiT}} = \min\left(	ext{PD}_{	ext{TTC}} 	imes M_{	ext{macro}}, 0.99
ight)$$

The economic decision rule automatically declines any applicant whose $	ext{PD}_{	ext{PiT}}$ exceeds the break-even threshold $	ext{PD}^*$, defined by loan economics:

$$	ext{PD}^* = rac{	ext{Margin}}{	ext{Margin} + 	ext{LGD}} = rac{(	ext{Rate} - 	ext{Cost of Funds}) 	imes rac{	ext{Tenure}}{12}}{(	ext{Rate} - 	ext{Cost of Funds}) 	imes rac{	ext{Tenure}}{12} + 	ext{LGD}}$$

Where $	ext{Cost of Funds} = 9.0\%$ and $LGD = 65.0\%$. Under this rigorous economic frontier, approval policies adjust automatically:
- **Benign Economy (Baseline Multiplier = 0.88×):** Approval rate expands safely to **75.1%**, maintaining an approved default rate of **4.38%**.
- **Neutral Economy (TTC Multiplier = 1.00×):** Approval rate is **60.3%**, with an approved default rate of **3.82%**.
- **Severe Downturn (Stress Multiplier = 1.45×):** Approval rate contracts automatically to **47.8%**, curtailing losses and keeping approved defaults at **3.12%**.

### 6.3 KPI-Driven Financial Impact Scenarios

To quantify the commercial value of IntelliCredit, we simulated underwriting 10,000 loan applications under alternative operational policies:

| Policy Underwriting Strategy | Approval Rate (%) | Approvals ($n$) | Approved Defaults ($n$) | Portfolio Default Rate (%) | Gross Interest Income (₹) | Total Default Loss (₹) | Net Financial Margin (₹) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Naive Baseline (Approve All)** | 100.0% | 10,000 | 787 | 7.87% | ₹4.80 Crore | ₹2.66 Crore | +₹2.14 Crore |
| **Strict Traditional Bureau Proxy** | 42.0% | 4,200 | 142 | 3.38% | ₹2.01 Crore | ₹0.48 Crore | +₹1.53 Crore |
| **ML Score Alone (Cost-Optimal)** | 74.7% | 7,470 | 329 | 4.40% | ₹3.58 Crore | ₹1.11 Crore | +₹2.47 Crore |
| **IntelliCredit Dual-Key Engine** | **71.2%** | **7,120** | **242** | **3.40%** | **₹3.42 Crore** | **₹0.82 Crore** | **+₹2.60 Crore** |

*Table 14. Simulated financial outcomes per 10,000 applicants comparing baseline and IntelliCredit strategies.*

**Financial Bottom Line:** Compared to the naive approve-all strategy, the IntelliCredit Dual-Key Engine delivers a **₹46 Lakhs net profit expansion (+21.5%)** per 10,000 applications while eliminating **₹1.84 Crore in credit defaults**. Compared to strict traditional bureau scoring that rejects unbanked workers, IntelliCredit expands financial inclusion by **+2,920 creditworthy borrowers (+69.5%)** while maintaining an institutional-grade default rate of **3.40%**.

---

### 6.4 Empirical Benchmarking and Direct Comparison with FinXCredit (Chauhan et al., 2026)

A closely related study on Indian gig-worker credit scoring was published by **Chauhan et al. (IJSREM, May 2026)**, titled *FinXCredit: An AI-Powered Alternative Credit Risk Assessment System for India's Gig Economy Workers*. To rigorously position IntelliCredit within the scientific literature, Table 15 provides a comprehensive, side-by-side empirical and architectural comparison:

| Technical Dimension | FinXCredit (Chauhan et al., May 2026) | IntelliCredit (Our System) | Scientific Evaluation & Comparison |
|---|---|---|---|
| **Underlying Default Rate** | **38.2%** (Freelancers 43.1%, Salaried 29.1%) | **7.87%** (Calibrated to uncollateralized MFI sector) | FinXCredit's 38.2% default rate reflects an extreme subprime environment. IntelliCredit grounds its baseline in MFIN *Micrometer* (6.9–8.5%). |
| **Primary Scoring Architecture** | Static 5-Factor Heuristic Engine (arbitrary weights) | Calibrated LightGBM ML + 93 Mined Association Warning Rules | FinXCredit's heuristic assumes linear factor additivity. IntelliCredit captures complex non-linear interactions. |
| **Empirical Test on Our Data** | **AUC = 0.6508** (Heuristic) / **0.5816** (Linear Formula) | **AUC = 0.7410** [95% CI: 0.715, 0.767] | When FinXCredit's 5-factor scoring engine is evaluated on our realistic dataset, its performance collapses to 0.651. |
| **Transaction Activity Weight** | 35% weight (claimed 2.3× weight on transaction activity) | Dynamic continuous feature (`avg_upi_transactions`, $IV = 0.21$) | FinXCredit over-weights raw transaction frequency, ignoring platform tenure ($IV = 0.384$) and negative income trend. |
| **Macroeconomic Cyclicality** | Completely omitted (assumes static macro conditions) | **SARIMAX + Exogenous FRED/World Bank Institutional APIs** | FinXCredit cannot adjust risk during recessions. IntelliCredit provides dynamic Point-in-Time scenario multipliers. |
| **Delinquency Pattern Mining** | None (pure tree-based prediction) | **93 Validated Association Rules (Apriori & FP-Growth)** | IntelliCredit provides a qualitative "second opinion" detecting 3.1× risk elevation in the prime ML rating band. |
| **Algorithmic Fairness** | Subgroup audits omitted; uses city tier as explicit input | **Formal fairness ablation; proved demographic proxies drop cleanly** | IntelliCredit demonstrates that location and education can be eliminated without losing predictive accuracy ($\Delta 	ext{AUC} = 0.0000$). |

*Table 15. Direct empirical and architectural benchmark comparing IntelliCredit with FinXCredit (Chauhan et al., 2026).*

#### 6.4.1 Empirical Evaluation of FinXCredit's Formula
To empirically evaluate the claims in Chauhan et al., we implemented their 5-factor scoring engine (Transaction Activity 35%, Savings Ratio 20%, Income Stability 15%, Spending Behavior 15%, Financial Discipline 15%) on our test dataset:
- FinXCredit's 5-factor composite score achieved an **AUC of only 0.6508**.
- FinXCredit's published linear logistic risk equation:
  $$\text{base\_risk} = 2.5 \cdot \text{loan\_to\_income} - 3.5 \cdot \text{savings\_ratio} + 2.0 \cdot \text{volatility} - 1.0 \cdot \text{digital\_ratio}$$
  achieved an **AUC of only 0.5816** on our dataset.

**Scientific Explanation:** FinXCredit's heuristic places heavy emphasis (35%) on raw transaction frequency. However, in our realistic microfinance distribution, a food delivery partner receiving 200 micro-payments of ₹40 per month does not automatically represent lower risk if their income trend is negative and their platform tenure is under 3 months. By omitting platform tenure (the #1 predictive factor in India's gig economy, $IV = 0.384$) and non-linear utility delay cliffs, FinXCredit's heuristic fails to discriminate risk in realistic microfinance portfolios.

---

## 7. Interactive Decision-Support Prototype & Reproducibility

### 7.1 Five-Tab Streamlit Prototype Walkthrough

The operational decision-support prototype of IntelliCredit is implemented as a responsive **Streamlit** application (`dashboard/app.py`):

![Dashboard Tab 1](screenshots/dash_underwriter.png)
*Figure 11. Tab 1 Underwriter Decision Engine: 8 streamlined input fields, TreeSHAP waterfall, and delinquency rule badges.*

1. **Tab 1: Underwriter Decision Engine:** Streamlined to **8 visible applicant inputs** (Age, Platform Tenure, Location, Education, Monthly Income, Utility Bills Paid on Time, Loan Amount, and Tenure) with all secondary parameters housed within a collapsible Advanced Expander. Includes one-click loading of three archetypal profiles:
   - *Customer 1 (Prime Gig Worker):* 36m tenure, 12/12 utility punctuality $\implies$ **Auto-Approved** ($	ext{PD} = 2.1\%$, Band A, Suggested Rate 14.0%).
   - *Customer 2 (Stressed Marginal Worker):* 8m tenure, declining trend, 8/12 bills $\implies$ **Approved with Conditions** ($	ext{PD} = 7.4\%$, Band C, triggers 4 warning rules).
   - *Customer 3 (Delinquent Worker):* 2m tenure, unbanked, 4/12 bills $\implies$ **Auto-Declined** ($	ext{PD} = 28.4\%$, Band E, triggers 75 warning rules).
2. **Tab 2: Dataset Explorer & Drilldown:** Interactive multi-attribute browser for 6,000 held-out test borrowers. Features dynamic filters (Risk Band, Location, Gig Platform, Outcome) that instantly recalculate exposure metrics, default distributions, and applicant drilldowns with zero crash vulnerability on empty selections.
3. **Tab 3: Portfolio Outlook & Scenarios:** Visualizes historical loan-book defaults alongside live SARIMAX forecasts, 30+ DPD early-warning roll rates, 2025 ECL stress scenario tables, and institutional FRED/World Bank macro indicator plots.
4. **Tab 4: Delinquency Warning Rules:** Interactive Plotly scatter plot mapping all 93 validated warning rules across coverage, confidence, and lift, complete with dynamic item filtering.
5. **Tab 5: Model Card & Provenance:** Full governance report displaying decile calibration plots, AUC/Brier metrics, economic break-even equations, and complete API endpoint provenance.

![Dashboard Tab 2 & 3](screenshots/dash_portfolio.png)
*Figure 12. Tab 3 Portfolio Outlook: Dynamic macro scenario toggles and Expected Credit Loss projections.*

### 7.2 Figure Index and Reproduction Map

| Figure No. | Caption and Visual Content | Source Notebook / Generator Script | Output Artifact Path |
|---|---|---|---|
| **Figure 1** | End-to-end IntelliCredit analytics architecture | `reports/build_full_deck.py` | `reports/presentation_figures/pipeline_architecture.png` |
| **Figure 2** | Exploratory distributions: income and tenure vs default | `notebooks/02_M2_exploratory_data_analysis.ipynb` | `reports/presentation_figures/eda_chart1.png` |
| **Figure 3** | Utility delays and BNPL obligations vs default | `notebooks/02_M2_exploratory_data_analysis.ipynb` | `reports/presentation_figures/eda_chart2.png` |
| **Figure 4** | Predictive model comparison: ROC and PR curves | `notebooks/04_M4_predictive_modeling.ipynb` | `reports/presentation_figures/ml_model_comparison.png` |
| **Figure 5** | TreeSHAP feature importance ranking | `notebooks/05_M5_evaluation_interpretation.ipynb` | `reports/screenshots/dash_underwriter.png` |
| **Figure 6** | 72-month portfolio default rate and STL decomposition | `notebooks/06_R2_M1_time_series_forecasting.ipynb`| `reports/presentation_figures/ts_historical_trend.png` |
| **Figure 7** | SARIMAX 2024 forecast and 2025 stress scenarios | `notebooks/06_R2_M1_time_series_forecasting.ipynb`| `reports/presentation_figures/ts_scenarios_ecl.png` |
| **Figure 8** | ARM rule distribution: coverage vs confidence vs lift | `notebooks/07_R2_M2_association_rule_mining.ipynb`| `reports/presentation_figures/arm_rules_chart.png` |
| **Figure 9** | Execution runtime benchmark: Apriori vs FP-Growth | `notebooks/07_R2_M2_association_rule_mining.ipynb`| `reports/presentation_figures/arm_runtime_benchmark.png` |
| **Figure 10**| Two-dimensional risk matrix: PD band vs rules hit | `notebooks/08_R2_combined_insights_dashboard.ipynb`| `reports/presentation_figures/combined_heatmap.png` |
| **Figure 11**| Dashboard Tab 1 Underwriter Decision Engine | `dashboard/app.py` | `reports/screenshots/dash_underwriter.png` |
| **Figure 12**| Dashboard Tab 3 Portfolio Outlook & Stress Testing | `dashboard/app.py` | `reports/screenshots/dash_portfolio.png` |
| **Figure 13**| Delinquency warning rules interactive scatter distribution | `dashboard/app.py` | `reports/screenshots/dash_warning.png` |
| **Figure 14**| Decile-level probability calibration curve | `dashboard/app.py` | `reports/screenshots/dash_model.png` |

*Table 16. Complete figure index and reproduction map linking visuals to underlying codebase scripts.*

### 7.3 Repository Architecture and Execution Instructions

The repository is structured to adhere to production software standards:

```text
intellicredit-review2/
├── README.md                           # Project documentation, rubric mapping, and execution guide
├── requirements.txt                    # Pinned library dependencies
├── data_generation.py                  # Synthetic borrower and transaction generation engine
├── dashboard/
│   └── app.py                          # Streamlit decision-support application
├── src/
│   ├── config.py                       # Global paths, categorical mappings, and fixed seeds
│   ├── macro_api.py                    # Institutional FRED and World Bank API collector
│   ├── portfolio_simulation.py         # 72-month macro-linked loan performance panel
│   ├── underwriting_model.py           # Calibrated LightGBM model training and serialization
│   └── risk_rules.py                   # Mined association rule application and scoring
├── data/
│   ├── borrower_profiles.csv           # 30,000 raw borrower records
│   ├── monthly_transactions.csv        # 360,000 transaction records
│   ├── processed/                      # Cleaned splits, feature matrices, and SMOTE frames
│   ├── external/                       # Harvested institutional macro time-series data
│   └── portfolio/                      # Loan-level and portfolio-level monthly panel data
├── notebooks/
│   ├── 01_M1_data_cleaning_preprocessing.ipynb
│   ├── 02_M2_exploratory_data_analysis.ipynb
│   ├── 03_M3_feature_engineering.ipynb
│   ├── 04_M4_predictive_modeling.ipynb
│   ├── 05_M5_evaluation_interpretation.ipynb
│   ├── 06_R2_M1_time_series_forecasting.ipynb      # Unit 3 Method 1 (Time-Series)
│   ├── 07_R2_M2_association_rule_mining.ipynb      # Unit 3 Method 2 (Rule Mining)
│   └── 08_R2_combined_insights_dashboard.ipynb     # Capstone synthesis
└── models/                             # Serialized models, rule sets, and scenario projections
```

**Step-by-Step Reproduction Instructions:**

```bash
# 1. Environment Initialization
git clone https://github.com/Goldmauler/intellicredit-review2.git
cd intellicredit-review2
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
# source venv/bin/activate
pip install -r requirements.txt

# 2. Automated Data Pipeline Execution
python data_generation.py                 # Generates 30k borrowers and 360k transactions
python -m src.macro_api                   # Harvests live FRED and World Bank macro series
python -m src.portfolio_simulation        # Simulates 72-month macro loan performance
python -m src.underwriting_model          # Fits and saves calibrated LightGBM model

# 3. Interactive Web Application Launch
streamlit run dashboard/app.py
```

*Note on Determinism:* All stochastic processes enforce global seeds (`RANDOM_STATE = 42` for data and ML models; `SEED = 2026` for portfolio loan-level simulation), guaranteeing 100% exact numerical reproduction.

---

## 8. Reflections, Limitations & Future Trajectories

### 8.1 Critical Assessment of Project Limitations

In adhering to rigorous academic standards, we explicitly acknowledge the following project limitations:
1. **Academic Research Platform vs. Production Underwriter:** The deployed Streamlit dashboard functions as an interactive research prototype for decision support and scenario exploration. It is not an enterprise core-banking engine; production deployment requires integration with live Account Aggregator (AA) SDKs, core-banking APIs (e.g., Mambu, Finacle), and high-availability microservices.
2. **Synthetic Nature of Micro-Transactions:** While macroeconomic series are 100% real institutional data and borrower distributions are benchmarked against official Indian government data (PLFS, MFIN), applicant transactions were generated via statistical simulation. Real-world consumer behavior exhibits idiosyncratic fraud patterns and micro-shocks that synthetic distributions cannot fully capture.
3. **Temporal Interpolation of Annual Macro Indicators:** World Bank indicators (GDP growth, national unemployment) are published annually and were interpolated to monthly frequency via cubic splines. Consequently, rapid intra-year macroeconomic turning points may appear smoothed relative to actual monthly economic reality.
4. **Linear Macro Multiplier Assumption:** The Point-in-Time overlay converts through-the-cycle PD via a scalar multiplier. This assumes that macroeconomic stress inflates default risk proportionally across all borrowers, whereas empirical evidence suggests low-income segments experience non-linear risk escalation during extreme stagflation.
5. **Log-Odds SHAP Interpretation:** TreeSHAP values are computed in log-odds space. While mathematically exact, operational underwriters without quantitative training may misinterpret log-odds additivity as linear probability shifts.

### 8.2 What Worked Well & Methodological Innovations

- **The Power of the Dual-Key Underwriting Framework:** Demonstrating that association rules isolate high-risk default clusters within the prime machine learning risk band (Band A default spread: 1.8% vs 5.6%) is a substantial empirical finding that provides immediate operational value to lenders.
- **Fairness through Proxy Ablation:** Proving that dropping `location_type` and `education_level` incurs zero loss in predictive power ($\Delta 	ext{AUC} = 0.0000$) provides commercial lenders with a practical, legally sound path to eliminate socioeconomic proxies.
- **Resilient Multi-Tier API Architecture:** Constructing an automated collector with graceful three-tier caching (Live API $	o$ Local JSON Cache $	o$ Offline Synthetic Baseline) ensures that the analytics pipeline remains fully functional in offline environments without external failure points.
- **Zero-Data-Leakage Discipline:** Enforcing strict pipeline encapsulation of all preprocessing, WoE transformations, and SMOTE balancing eliminated optimistic performance bias, establishing reliable generalization across all 6,000 hold-out test borrowers.

### 8.3 Future Research Trajectories

For future production evolution, we propose three technical extensions:
1. **Pilot Deployment with an Indian NBFC-MFI:** Partner with a licensed microfinance institution to shadow-score actual loan applications using live Account Aggregator (AA) and UPI consent APIs.
2. **Dynamic Conformal Prediction Intervals:** Incorporate Adaptive Conformal Inference (ACI) into the time-series forecasting engine to guarantee distribution-free, finite-sample coverage intervals for loan loss reserves.
3. **Automated Algorithmic Recourse Generation:** Enhance the underwriter engine with counterfactual optimisation algorithms (e.g., DiCE) to provide declined applicants with actionable, personalized paths to approval (e.g., "Increasing platform tenure by 3 months and reducing BNPL spend by ₹1,500 moves your application into Risk Band B").

---

## References

1. Agarwal, S., Alok, S., Ghosh, P., & Gupta, S. (2020). *Financial Inclusion and Alternative Data: Evaluating Mobile Wallet Credit Scoring in India*. Journal of Financial Economics, 138(2), 412–435.
2. Agrawal, R., & Srikant, R. (1994). *Fast Algorithms for Mining Association Rules in Large Databases*. Proceedings of the 20th International Conference on Very Large Data Bases (VLDB '94), 487–499.
3. Berg, T., Burg, V., Gombović, A., & Puri, M. (2020). *On the Rise of the FinTechs—Credit Scoring Using Digital Footprints*. The Review of Financial Studies, 33(7), 2845–2897.
4. Björkegren, D., & Grissen, D. (2020). *Behavior Revealed in Mobile Phone Usage Predicts Credit Repayment*. The World Bank Economic Review, 34(3), 618–634.
5. Chauhan, V., Sawarkar, M., Nage, J., Mishra, P., & Soni, G. (2026). *FinXCredit: An AI-Powered Alternative Credit Risk Assessment System for India's Gig Economy Workers*. International Journal of Scientific Research in Engineering and Management (IJSREM), 10(5), 1–6. DOI: 10.55041/IJSREM62883.
6. Federal Reserve Bank of St. Louis (FRED). (2024). *Economic Data Series for India: Consumer Price Index, Interbank Rates, G-Sec Yields, and Currency Exchange*. Federal Reserve Data API.
7. Lessmann, S., Baesens, B., Seow, H. V., & Thomas, L. C. (2015). *Benchmarking State-of-the-Art Classification Algorithms for Credit Scoring: An Update of Research*. European Journal of Operational Research, 247(1), 124–136.
8. Lundberg, S. M., & Lee, S. I. (2017). *A Unified Approach to Interpreting Model Predictions*. Advances in Neural Information Processing Systems (NeurIPS 2017), 30, 4765–4774.
9. Microfinance Institutions Network (MFIN). (2024). *Micrometer: Comprehensive State of the Microfinance Industry in India (Quarterly Reports FY24–FY27)*. MFIN India Publications.
10. Ministry of Statistics and Programme Implementation (MoSPI). (2023). *Periodic Labour Force Survey (PLFS) Annual Report 2022–2023*. Government of India.
11. National Payments Corporation of India (NPCI). (2023). *UPI Product Statistics and Annual Transaction Volume Metrics*. NPCI Mumbai.
12. NITI Aayog. (2022). *Booster's Economy: The Potential and Challenges of the Gig and Platform Economy in India*. Government of India Policy Brief.
13. Reserve Bank of India (RBI). (2021). *Report on Trend and Progress of Banking in India 2020–21*. RBI Central Publications, Mumbai.
14. UK Financial Conduct Authority (FCA). (2024). *Synthetic Data for Financial Inclusion and Model Validation: Technical Guidance and Regulatory Principles*. FCA Research Paper Series.
15. Wilson, T. C. (1997). *Portfolio Credit Risk (Parts I & II)*. Risk Magazine, 10(9), 111–117; 10(10), 56–61.
16. World Bank. (2024). *World Development Indicators: Real GDP Growth, Unemployment Rate, and Lending Interest Rates for India*. World Bank Open Data API.

---

## Appendices

### Appendix A: Additional Diagnostic Figures & Sensitivity Plots

![Delinquency Rules Scatter](screenshots/dash_warning.png)
*Figure 13. Interactive Delinquency Warning Rule Explorer (Dashboard Tab 4) visualizing all 93 validated rules.*

![Model Calibration](screenshots/dash_model.png)
*Figure 14. Decile-level probability calibration curve (Dashboard Tab 5) demonstrating exact alignment between predicted PD and observed defaults.*

---

### Appendix B: Comprehensive Model Tuning & Benchmark Tables

| Model Type | Tuned Hyperparameter Configuration | Cross-Validation Tuning Space |
|---|---|---|
| **Logistic Regression** | `C=0.10`, `penalty='l2'`, `solver='lbfgs'`, `max_iter=1000` | $C \in [0.001, 0.01, 0.1, 1.0, 10.0]$ |
| **Random Forest** | `n_estimators=300`, `max_depth=8`, `min_samples_split=20`, `max_features='sqrt'` | `n_estimators` $\in [100, 300, 500]$, `max_depth` $\in [5, 8, 12]$ |
| **LightGBM** | `n_estimators=400`, `learning_rate=0.02`, `num_leaves=15`, `reg_lambda=2.0` | `num_leaves` $\in [15, 31, 63]$, `learning_rate` $\in [0.01, 0.02, 0.05]$ |
| **XGBoost** | `n_estimators=350`, `learning_rate=0.03`, `max_depth=4`, `colsample_bytree=0.8` | `max_depth` $\in [3, 4, 6]$, `subsample` $\in [0.7, 0.8, 1.0]$ |
| **SARIMAX** | $	ext{Order}=(1,1,1)$, $	ext{Seasonal}=(1,0,1)_{12}$, $	ext{Trend}='c'$, Exog: 4 variables | Grid search over $p, q \in [0, 2]$, $P, Q \in [0, 1]$, BIC selection |

*Table 17. Complete hyperparameter optimization settings for all evaluated predictive and time-series models.*

---

### Appendix C: Implementation Details & Underwriter User Guide

**System Requirements:** Python 3.10+, 8 GB RAM, modern web browser (Chrome, Edge, Firefox).

**Detailed Underwriting Dashboard Operational Guide:**
1. **Selecting Applicant Data:** Navigate to Tab 1. Use the horizontal radio control to load either pre-configured customer archetypes (**Customer 1: Prime**, **Customer 2: Stressed**, **Customer 3: Delinquent**) or choose **Custom Entry** to evaluate a novel applicant.
2. **Entering Core Application Fields:** Enter the 8 visible primary parameters (Age, Tenure, Location, Education, Monthly Income, Utility Bills on Time, Loan Amount, and Tenure). To modify secondary behavioral features (e.g., BNPL spend, app logins, recharge intervals), open the collapsible **Advanced Parameters** expander.
3. **Evaluating Decision Output:** Click **Score Applicant**. The engine computes:
   - *Through-the-Cycle (TTC) PD:* Unadjusted baseline probability of default.
   - *Point-in-Time (PiT) PD:* Macro-adjusted probability incorporating the scenario multiplier selected in the sidebar.
   - *Economic Decision Badge:* Displays **APPROVE** (green), **APPROVE WITH CONDITIONS** (amber), or **DECLINE / REFER** (red) alongside explicit economic justification.
   - *Suggested Interest Rate:* Recommends an actuarially sound interest rate reflecting the applicant's assigned risk band.
   - *TreeSHAP Attribution Chart:* Highlights the top 10 features raising (red) or lowering (green) borrower default log-odds.
   - *Delinquency Warning Badges:* Lists all validated behavioural association rules triggered by the applicant.
4. **Stress Testing the Loan Book:** Navigate to Tab 3. Toggle between **Baseline**, **Adverse**, and **Severe** macro scenarios in the sidebar. Observe how portfolio loss provisions and approval frontiers shift dynamically in response to macro shocks.

---

### Appendix D: Project Board Evidence, Individual Contributions & AI Disclosure

**Project Management & Version Control Governance:**  
The capstone project was tracked via GitHub Kanban boards and issue trackers across 19 discrete technical tasks (10 tasks for Review 1; 9 tasks for Review 2). All code changes, pull requests, and documentation drafts were reviewed and merged through automated CI/CD checks.

| Team Member | Official Register No. | Assigned Tasks & Deliverable Ownership | Curriculum Rubric Component (Marks) | Primary Verified Code Artifacts |
|---|:---:|---|---|---|
| **Darun R G** | CB.SC.U4CSE23215 | Data architecture, synthetic transaction generator, feature engineering, benchmark validation | Overall Dataset Description & Baseline ML (Unit 1 & 2) | `data_generation.py`, `notebooks/01-05`, `data/DATASET_VALIDATION_SUMMARY.md` |
| **goldmauler** | CB.SC.U4CSE23118 | Lead: Time-Series Forecasting (SARIMAX), institutional APIs, ARM mining (Apriori/FP-Growth) | Method 1 (5 Marks) + Method 2 (5 Marks) | `notebooks/06_R2_M1`, `notebooks/07_R2_M2`, `src/macro_api.py`, `models/association_rules.csv` |
| **Abhinav Juturu** | CB.SC.U4CSE23146 | Portfolio risk modelling, 38 EDA visualisations, dynamic loan book simulation, hypothesis testing | Method 1 Data Prep, EDA & Scenario Loss (2 Marks) | `src/portfolio_simulation.py`, `notebooks/02_M2`, `data/portfolio/` |
| **Gowtham Reddy** | CB.SC.U4CSE23232 | Full-stack interactive dashboard development, UI refactoring, data cleaning, HTML export | Mandatory Interactive Application (5 Marks) | `dashboard/app.py`, `notebooks/01_M1`, `reports/interactive_dashboard.html` |
| **Adithya** | CB.SC.U4CSE23752 | Model evaluation, TreeSHAP interpretability, combined insights synthesis, report authoring | Combined Business Insights (2 Marks) + Defense (3 Marks) | `notebooks/05_M5`, `notebooks/08_R2`, `reports/Review_2_Final_Report.md` |

*Table 18. Detailed individual workload allocation, rubric ownership, and code deliverable mapping.*

**Generative Artificial Intelligence Disclosure (Complete Audit):**

| AI Tool & Provider | Specific Tasks Supported | Affected Modules & Content | Human Verification, Auditing & Correction Procedures |
|---|---|---|---|
| **Antigravity (Coding Assistant)** | Dashboard UI refactoring, Word report script generation | `dashboard/app.py`, `scripts/build_final_word_report.py` | The team audited all code syntax, ran local unit tests, verified input derivation logic, and confirmed zero model degradation. |
| **Claude (Anthropic)** | Report structuring, formatting, and plan synthesis | `reports/Review_2_Final_Report.md`, Capstone Report Plan | The team verified all empirical numbers against notebook outputs, recalculated table metrics, corrected LaTeX formatting, and authored all strategic recommendations. |
| **ChatGPT (OpenAI)** | Initial conceptual brainstorming and literature search | Early project planning documentation | Ideas were reviewed by team members, checked against course guidelines and academic papers, and rewritten from scratch. |

*Table 19. Comprehensive generative artificial intelligence declaration and audit log.*

---
*End of Report — IntelliCredit Capstone Final Technical Report (2026–2027)*
