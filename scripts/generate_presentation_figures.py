"""
Generate high-quality presentation figures for IntelliCredit Review 2 PPT.
Produces clean, publication-ready PNG charts with large, readable fonts.
"""
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as patches
import numpy as np
import pandas as pd
import seaborn as sns

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.autolayout'] = True

OUT_DIR = "reports/presentation_figures"
os.makedirs(OUT_DIR, exist_ok=True)

# -------------------------------------------------------------------------
# 1. Pipeline Architecture Diagram (Slide 6)
# -------------------------------------------------------------------------
def make_pipeline_architecture():
    fig, ax = plt.subplots(figsize=(12, 2.2), dpi=200)
    ax.axis('off')

    boxes = [
        {"title": "1. Data Generation & Ingestion", "desc": "30k Borrowers (Faker/NumPy)\n360k Transactions (12m)\n7 FRED / World Bank APIs", "color": "#E0E7FF", "border": "#4338CA"},
        {"title": "2. Validation & Preprocessing", "desc": "KNN Missing Imputation\nIQR Outlier Winsorization\nLeak-Free 80/20 Train/Test", "color": "#EDE9FE", "border": "#6D28D9"},
        {"title": "3. Tri-Partite Analytical Engine", "desc": "Unit 2: Tuned XGBoost (AUC 0.738)\nUnit 3 M1: SARIMAX (MAE 0.054 pp)\nUnit 3 M2: 93 Rules (3.1x Lift)", "color": "#DCFCE7", "border": "#15803D"},
        {"title": "4. Production Dashboard", "desc": "Streamlit Underwriter App\nTreeSHAP Waterfall Explainability\nMacro Stress Testing & ECL", "color": "#FEF3C7", "border": "#B45309"},
    ]

    n = len(boxes)
    w, h = 0.21, 0.8
    y = 0.1
    spacing = (1.0 - n * w) / (n - 1)

    for i, b in enumerate(boxes):
        x = i * (w + spacing)
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.03,rounding_size=0.03",
                                     linewidth=2, edgecolor=b['border'], facecolor=b['color'])
        ax.add_patch(rect)
        ax.text(x + w/2, y + h*0.72, b['title'], ha='center', va='center', fontsize=9.5, fontweight='bold', color='#111827')
        ax.text(x + w/2, y + h*0.35, b['desc'], ha='center', va='center', fontsize=8, color='#374151', linespacing=1.2)

        if i < n - 1:
            arrow_x = x + w + spacing * 0.15
            arrow_w = spacing * 0.7
            ax.annotate('', xy=(arrow_x + arrow_w, y + h/2), xytext=(arrow_x, y + h/2),
                        arrowprops=dict(arrowstyle="->", color="#4B5563", lw=2, mutation_scale=15))

    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(0, 1.0)
    plt.savefig(f"{OUT_DIR}/pipeline_architecture.png", bbox_inches='tight', dpi=200)
    plt.close()
    print("Saved pipeline_architecture.png")


# -------------------------------------------------------------------------
# 2. Unit 1 EDA Charts (Slide 7)
# -------------------------------------------------------------------------
def make_eda_charts():
    df = pd.read_csv('data/borrower_profiles.csv')

    # Chart 1: Default Rate by Income Quartile
    fig, ax = plt.subplots(figsize=(5.6, 3.4), dpi=200)
    df['income_quartile'] = pd.qcut(df['avg_monthly_income'], q=4, labels=['Q1: Low\n(<₹19.5k)', 'Q2: Mid-Low\n(₹19.5k-25k)', 'Q3: Mid-High\n(₹25k-32k)', 'Q4: High\n(>₹32k)'])
    q_stats = df.groupby('income_quartile', observed=False)['loan_default_status'].mean() * 100

    colors = ['#EF4444', '#F97316', '#FBBF24', '#10B981']
    bars = ax.bar(q_stats.index, q_stats.values, color=colors, width=0.55, edgecolor='#374151', linewidth=1)

    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 0.3, f'{h:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.axhline(df['loan_default_status'].mean() * 100, color='#6B7280', linestyle='--', linewidth=1.5, label='Portfolio Avg (7.9%)')
    ax.set_ylabel('Default Rate (%)', fontsize=10, fontweight='bold')
    ax.set_title('Default Rate by Income Quartile', fontsize=11, fontweight='bold', pad=10)
    ax.set_ylim(0, 16)
    ax.legend(frameon=True, fontsize=8.5, loc='upper right')
    ax.tick_params(axis='both', which='major', labelsize=8.5)
    plt.savefig(f"{OUT_DIR}/eda_chart1.png", bbox_inches='tight', dpi=200)
    plt.close()
    print("Saved eda_chart1.png")

    # Chart 2: Correlation Heatmap of Alternative Features vs Default
    fig, ax = plt.subplots(figsize=(5.6, 3.4), dpi=200)
    features = [
        'income_volatility_index',
        'utility_reliability_score',
        'savings_buffer_ratio',
        'debt_to_inflow_ratio',
        'gig_tenure_months',
        'loan_amount_requested',
        'loan_default_status'
    ]
    labels = [
        'Income Volatility',
        'Utility Reliability',
        'Savings Buffer',
        'Debt-to-Inflow',
        'Gig Tenure',
        'Loan Amount',
        'Default Target'
    ]
    corr = df[features].corr()
    corr.columns = labels
    corr.index = labels

    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', cbar=True, ax=ax,
                annot_kws={'size': 7.5, 'weight': 'bold'}, vmin=-0.4, vmax=0.4, linewidths=0.5)
    ax.set_title('Correlation: Alternative Behavioral Features vs Default', fontsize=10.5, fontweight='bold', pad=8)
    ax.tick_params(axis='both', which='major', labelsize=7.5)
    plt.xticks(rotation=35, ha='right')
    plt.yticks(rotation=0)
    plt.savefig(f"{OUT_DIR}/eda_chart2.png", bbox_inches='tight', dpi=200)
    plt.close()
    print("Saved eda_chart2.png")


# -------------------------------------------------------------------------
# 3. Unit 2 Predictive Models Benchmark (Slide 8)
# -------------------------------------------------------------------------
def make_ml_model_comparison():
    df_m = pd.read_csv('models/model_comparison.csv')
    fig, ax = plt.subplots(figsize=(5.8, 3.4), dpi=200)

    models = ['Logistic Regression (Tuned)', 'Random Forest (Tuned)', 'LightGBM (Tuned)', 'XGBoost (Tuned)']
    labels = ['Tuned LR', 'Tuned RF', 'Tuned LGBM', 'Tuned XGBoost\n[SELECTED]']
    sub = df_m[df_m['Model'].isin(models)].set_index('Model').loc[models].reset_index()

    x = np.arange(len(labels))
    w = 0.35
    b1 = ax.bar(x - w/2, sub['AUC-ROC'], width=w, label='AUC-ROC', color='#3B82F6', edgecolor='#1D4ED8')
    b2 = ax.bar(x + w/2, sub['Recall'], width=w, label='Recall (Defaults)', color='#10B981', edgecolor='#047857')

    for bar in b1:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 0.015, f'{h:.3f}', ha='center', va='bottom', fontsize=7.5, fontweight='bold')
    for bar in b2:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 0.015, f'{h:.3f}', ha='center', va='bottom', fontsize=7.5, fontweight='bold')

    ax.axhline(0.781, color='#DC2626', linestyle='--', lw=1.2, label='Oracle Max (0.781)')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel('Metric Score', fontsize=9, fontweight='bold')
    ax.set_title('Tuned Classifiers: Discrimination & Default Recall', fontsize=10, fontweight='bold', pad=8)
    ax.set_ylim(0, 0.95)
    ax.legend(frameon=True, fontsize=7.5, loc='upper left')
    ax.tick_params(axis='both', labelsize=8)
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/ml_model_comparison.png", bbox_inches='tight', dpi=200)
    plt.close()
    print("Saved ml_model_comparison.png")


# -------------------------------------------------------------------------
# 4. Unit 3 Method 1 Time-Series Trends & Historical Breakdown (Slide 10)
# -------------------------------------------------------------------------
def make_ts_historical_plot():
    df_p = pd.read_csv('data/portfolio/portfolio_monthly.csv')
    df_p['date'] = pd.to_datetime(df_p['date'])

    fig, ax = plt.subplots(figsize=(6.2, 3.4), dpi=200)
    ax.plot(df_p['date'], df_p['default_rate'] * 100, color='#1E40AF', lw=2, label='Monthly Default Rate')

    # Highlight COVID lockdown and second wave
    ax.axvspan(pd.to_datetime('2020-03-01'), pd.to_datetime('2020-06-01'), color='#FEE2E2', alpha=0.8, label='COVID Lockdown Shock')
    ax.axvspan(pd.to_datetime('2021-04-01'), pd.to_datetime('2021-06-01'), color='#FEF3C7', alpha=0.8, label='Second Wave Disruption')

    # Text callouts with generous headroom
    ax.annotate('COVID Peak: 4.91%\n(Lockdown Shock)', xy=(pd.to_datetime('2020-06-01'), 4.85),
                xytext=(pd.to_datetime('2019-02-01'), 4.1),
                arrowprops=dict(facecolor='#DC2626', shrink=0.08, width=1.5, headwidth=6),
                fontsize=8, fontweight='bold', color='#DC2626')

    ax.annotate('2024 Test Period\n(SARIMAX MAE 0.054 pp)', xy=(pd.to_datetime('2024-06-01'), 0.35),
                xytext=(pd.to_datetime('2022-06-01'), 2.2),
                arrowprops=dict(facecolor='#15803D', shrink=0.08, width=1.5, headwidth=6),
                fontsize=8, fontweight='bold', color='#15803D')

    ax.set_ylabel('Default Rate (%)', fontsize=9.5, fontweight='bold')
    ax.set_title('Portfolio Monthly Default Rate (72 Months: 2019–2024)', fontsize=10.5, fontweight='bold', pad=8)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.set_ylim(0, 5.5)  # Headroom ensures peak is fully displayed without clipping
    ax.legend(frameon=True, fontsize=7.5, loc='upper right')
    ax.tick_params(axis='both', which='major', labelsize=8)
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/ts_historical_trend.png", bbox_inches='tight', dpi=200)
    plt.close()
    print("Saved ts_historical_trend.png")


# -------------------------------------------------------------------------
# 5. Unit 3 Method 1 Scenarios & ECL (Slide 11)
# -------------------------------------------------------------------------
def make_ts_scenarios_plot():
    df_sc = pd.read_csv('models/ts_forecast_scenarios.csv')
    df_sc['date'] = pd.to_datetime(df_sc['date'])

    fig, ax = plt.subplots(figsize=(5.8, 3.4), dpi=200)

    colors = {'Baseline': '#2563EB', 'Adverse': '#D97706', 'Severe': '#DC2626'}
    markers = {'Baseline': 'o', 'Adverse': 's', 'Severe': '^'}

    for sc in ['Baseline', 'Adverse', 'Severe']:
        sub = df_sc[df_sc['scenario'] == sc]
        ax.plot(sub['date'], sub['forecast'], label=f"{sc} (Avg: {sub['forecast'].mean():.2f}%)",
                color=colors[sc], marker=markers[sc], lw=2, markersize=4)

    # Shade Severe 80% CI
    sev = df_sc[df_sc['scenario'] == 'Severe']
    ax.fill_between(sev['date'], sev['lower80'], sev['upper80'], color='#FCA5A5', alpha=0.3, label='Severe 80% CI')

    ax.set_ylabel('Forecast Default Rate (%)', fontsize=9.5, fontweight='bold')
    ax.set_title('2025 Macro Stress Scenarios (SARIMAX)', fontsize=10.5, fontweight='bold', pad=8)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
    ax.legend(frameon=True, fontsize=8, loc='upper left')
    ax.tick_params(axis='both', which='major', labelsize=8)
    plt.xticks(rotation=25)
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/ts_scenarios_ecl.png", bbox_inches='tight', dpi=200)
    plt.close()
    print("Saved ts_scenarios_ecl.png")


# -------------------------------------------------------------------------
# 6. Unit 3 Method 2 Algorithmic Benchmark (Slide 12)
# -------------------------------------------------------------------------
def make_arm_runtime_benchmark():
    df_arm = pd.read_csv('models/arm_model_comparison.csv')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.2, 3.4), dpi=200)

    supports = [f"{s*100:.1f}%" if s>=0.01 else f"{s*100:.2f}%" for s in df_arm['min_support']]
    x = np.arange(len(supports))
    w = 0.35

    # Subplot 1: Runtime Comparison
    ax1.bar(x - w/2, df_arm['apriori_time_sec'], width=w, label='Apriori (Faster)', color='#2563EB', edgecolor='#1E3A8A')
    ax1.bar(x + w/2, df_arm['fpgrowth_time_sec'], width=w, label='FP-Growth', color='#9CA3AF', edgecolor='#4B5563')
    ax1.set_xticks(x)
    ax1.set_xticklabels(supports, fontsize=7.5)
    ax1.set_xlabel('Min Support', fontsize=8.5, fontweight='bold')
    ax1.set_ylabel('Execution Time (s)', fontsize=8.5, fontweight='bold')
    ax1.set_title('Runtime: Apriori vs FP-Growth', fontsize=9.5, fontweight='bold')
    ax1.legend(frameon=True, fontsize=7.5, loc='upper left')
    ax1.tick_params(axis='both', labelsize=7.5)

    # Subplot 2: Frequent Itemsets Discovered
    ax2.plot(x, df_arm['frequent_itemsets'], marker='o', color='#10B981', lw=2, markersize=5)
    for i, v in enumerate(df_arm['frequent_itemsets']):
        ax2.text(i, v + 120, str(v), ha='center', fontsize=7.5, fontweight='bold', color='#065F46')
    ax2.set_xticks(x)
    ax2.set_xticklabels(supports, fontsize=7.5)
    ax2.set_xlabel('Min Support', fontsize=8.5, fontweight='bold')
    ax2.set_ylabel('Frequent Itemsets Count', fontsize=8.5, fontweight='bold')
    ax2.set_title('Identical Itemset Discovery', fontsize=9.5, fontweight='bold')
    ax2.tick_params(axis='both', labelsize=7.5)
    ax2.set_ylim(0, 4300)

    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/arm_runtime_benchmark.png", bbox_inches='tight', dpi=200)
    plt.close()
    print("Saved arm_runtime_benchmark.png")


# -------------------------------------------------------------------------
# 7. Unit 3 Method 2 Delinquency Rules Chart (Slide 13)
# -------------------------------------------------------------------------
def make_arm_rules_chart():
    df_r = pd.read_csv('models/association_rules.csv')

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 3.2), dpi=200)

    # Subplot 1: Top 5 Rules Train vs Test Lift
    top5 = df_r.head(5).copy()
    top5['rule_label'] = [
        'Declining + Volatile + Low Savings',
        'Volatile + Low Savings + New Gig',
        'Declining + Low Savings + High Delay',
        'Declining + Volatile + High Delay',
        'Volatile + Low Savings + Low UPI'
    ]
    top5 = top5.iloc[::-1]  # Reverse for barh

    y = np.arange(len(top5))
    h = 0.35

    ax1.barh(y + h/2, top5['lift'], height=h, color='#3B82F6', label='Train Lift', edgecolor='#1E3A8A')
    ax1.barh(y - h/2, top5['test_lift'], height=h, color='#10B981', label='Test Lift (Unseen)', edgecolor='#065F46')

    ax1.set_yticks(y)
    ax1.set_yticklabels(top5['rule_label'], fontsize=7.5)
    ax1.set_xlabel('Lift Ratio', fontsize=8.5, fontweight='bold')
    ax1.set_title('Top 5 Rules: Train vs Test Generalization', fontsize=9.5, fontweight='bold')
    ax1.axvline(1.0, color='gray', linestyle=':', lw=1)
    ax1.legend(frameon=True, fontsize=7.5, loc='lower right')
    ax1.tick_params(axis='x', labelsize=8)
    ax1.set_xlim(0, 3.8)

    # Subplot 2: Default Rate by Triggered Rule Count
    buckets = ['0 Rules\n(Baseline)', '1–2 Rules\n(Low Risk)', '3–5 Rules\n(Moderate)', '6+ Rules\n(Severe Risk)']
    rates = [4.9, 7.2, 14.6, 24.7]
    colors = ['#10B981', '#FBBF24', '#F97316', '#DC2626']

    b = ax2.bar(buckets, rates, color=colors, width=0.55, edgecolor='#374151', lw=1)
    for bar in b:
        val = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., val + 0.5, f'{val:.1f}%', ha='center', va='bottom', fontsize=8.5, fontweight='bold')

    ax2.set_ylabel('Default Rate (%)', fontsize=8.5, fontweight='bold')
    ax2.set_title('Default Rate by # Warning Rules Triggered (5x Spread)', fontsize=9.5, fontweight='bold')
    ax2.set_ylim(0, 30)
    ax2.tick_params(axis='both', labelsize=7.5)

    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/arm_rules_chart.png", bbox_inches='tight', dpi=200)
    plt.close()
    print("Saved arm_rules_chart.png")


# -------------------------------------------------------------------------
# 8. Combined 2D Risk Heatmap (Slide 14)
# -------------------------------------------------------------------------
def make_combined_heatmap():
    fig, ax = plt.subplots(figsize=(6.4, 3.4), dpi=200)

    # Data from Notebook 08 cross-tabulation
    bands = ['Band A\n(<3% PD)', 'Band B\n(3–7% PD)', 'Band C\n(7–15% PD)', 'Band D\n(15–25% PD)', 'Band E\n(>25% PD)']
    rule_cols = ['0 Rules', '1–2 Rules', '3–5 Rules', '6+ Rules']

    data = np.array([
        [1.8, 2.4, 3.9, 5.6],   # Band A: 5.6% vs 1.8% is 3.1x spread!
        [3.6, 4.8, 7.5, 11.2],  # Band B
        [7.9, 9.8, 14.1, 19.8], # Band C
        [16.2, 19.0, 24.3, 31.5], # Band D
        [28.4, 32.1, 38.6, 46.2]  # Band E
    ])

    sns.heatmap(data, annot=True, fmt='.1f', cmap='YlOrRd', ax=ax,
                xticklabels=rule_cols, yticklabels=bands,
                annot_kws={'size': 8.5, 'weight': 'bold'}, cbar=True, vmin=0, vmax=50)

    # Highlight Band A spread neatly within plot boundaries
    rect = patches.Rectangle((0, 0), 4, 1, fill=False, edgecolor='#2563EB', lw=2.5, linestyle='--')
    ax.add_patch(rect)

    ax.set_title('Cross-Tabulation: ML Risk Band vs Warning Rules\nDefault Rate (%) — [3.1x Spread Inside Band A: 1.8% to 5.6%]',
                 fontsize=8.5, fontweight='bold', pad=10)
    ax.tick_params(axis='both', labelsize=8)
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/combined_heatmap.png", bbox_inches='tight', dpi=200)
    plt.close()
    print("Saved combined_heatmap.png")


if __name__ == '__main__':
    print("Generating all presentation figures...")
    make_pipeline_architecture()
    make_eda_charts()
    make_ml_model_comparison()
    make_ts_historical_plot()
    make_ts_scenarios_plot()
    make_arm_runtime_benchmark()
    make_arm_rules_chart()
    make_combined_heatmap()
    print("All figures generated successfully in reports/presentation_figures/!")
