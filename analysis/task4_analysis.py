from pathlib import Path
import math
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data" / "ApexPlanet_DataAnalytics_Dataset.xlsx"
OUT = BASE / "outputs"
CHARTS = OUT / "charts"
OUT.mkdir(exist_ok=True)
CHARTS.mkdir(exist_ok=True)

ALPHA = 0.05


def load_data():
    """Load and standardize the source Excel dataset."""
    df = pd.read_excel(DATA)
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    df["Total_Sales"] = pd.to_numeric(df["Total_Sales"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["Unit_Price"] = pd.to_numeric(df["Unit_Price"], errors="coerce")
    return df


def validate_data(df):
    """Keep rows with fields required for descriptive analysis."""
    required = ["Order_ID", "Order_Date", "Total_Sales", "Category", "City"]
    return df.dropna(subset=required).copy()


def build_order_level(clean):
    """Aggregate valid sales rows to one row per Order_ID."""
    order_level = clean.groupby("Order_ID", as_index=False).agg(
        Order_Date=("Order_Date", "min"),
        Customer_ID=("Customer_ID", "first"),
        City=("City", "first"),
        Order_Value=("Total_Sales", "sum"),
        Category_Count=("Category", "nunique"),
        Row_Count=("Order_ID", "size"),
    )
    category_map = clean.groupby("Order_ID")["Category"].first()
    order_level["Category"] = order_level["Order_ID"].map(category_map)
    return order_level


def create_quality_audit(df, clean, order_level, mixed_ids, hypothesis_sample):
    rows = [
        ("Original records", len(df)),
        ("Excluded records", len(df) - len(clean)),
        ("Valid records", len(clean)),
        ("Exclusion rate", f"{(len(df) - len(clean)) / len(df) * 100:.2f}%"),
        ("Missing Order_Date", int(df["Order_Date"].isna().sum())),
        ("Missing Total_Sales", int(df["Total_Sales"].isna().sum())),
        ("Missing Category", int(df["Category"].isna().sum())),
        ("Missing City", int(df["City"].isna().sum())),
        ("Distinct Order_ID values after validation", clean["Order_ID"].nunique()),
        ("Unique Customer_ID values after validation", clean["Customer_ID"].nunique()),
        ("Order_IDs appearing more than once", int((clean["Order_ID"].value_counts() > 1).sum())),
        ("Mixed-category/anomalous Order_IDs", len(mixed_ids)),
        ("All valid orders", len(order_level)),
        ("Hypothesis-test orders", len(hypothesis_sample)),
    ]
    pd.DataFrame(rows, columns=["Metric", "Value"]).to_csv(OUT / "data_quality_audit.csv", index=False)


def create_descriptive_outputs(clean, order_level):
    working = clean.copy()
    working["Month"] = working["Order_Date"].dt.to_period("M").astype(str)

    monthly = working.groupby("Month", as_index=False)["Total_Sales"].sum().sort_values("Month")
    monthly["Month_Label"] = pd.to_datetime(monthly["Month"]).dt.strftime("%b %Y")
    monthly["MoM_Change_Percent"] = monthly["Total_Sales"].pct_change() * 100
    monthly.loc[monthly.index[0], "MoM_Change_Percent"] = float("nan")
    monthly[["Month_Label", "Total_Sales", "MoM_Change_Percent"]].to_csv(OUT / "monthly_revenue.csv", index=False)

    city = working.groupby("City", as_index=False)["Total_Sales"].sum().sort_values("Total_Sales", ascending=False)
    city["Revenue_Share_Percent"] = city["Total_Sales"] / working["Total_Sales"].sum() * 100
    city.to_csv(OUT / "city_revenue.csv", index=False)

    category = working.groupby("Category", as_index=False).agg(
        Revenue=("Total_Sales", "sum"), Records=("Total_Sales", "size")
    )
    category["Revenue_Share_Percent"] = category["Revenue"] / working["Total_Sales"].sum() * 100
    category["Row_Level_AOV"] = category["Revenue"] / category["Records"]
    category.sort_values("Revenue", ascending=False).to_csv(OUT / "category_analysis.csv", index=False)

    order_level.to_csv(OUT / "order_level_sales.csv", index=False)
    return monthly, city, category


def create_hypothesis_sample(clean, order_level):
    counts = clean.groupby("Order_ID")["Category"].nunique()
    mixed_ids = counts[counts > 1].index.tolist()
    clean[clean["Order_ID"].isin(mixed_ids)].to_csv(OUT / "mixed_category_orders.csv", index=False)
    sample = order_level[~order_level["Order_ID"].isin(mixed_ids)].copy()
    sample.to_csv(OUT / "hypothesis_test_sample.csv", index=False)
    return sample, mixed_ids


def run_hypothesis_test(sample, mixed_ids):
    electronics = sample.loc[
        sample["Category"].astype(str).str.strip().str.lower() == "electronics", "Order_Value"
    ]
    other = sample.loc[
        sample["Category"].astype(str).str.strip().str.lower() != "electronics", "Order_Value"
    ]

    t_stat, p_value = stats.ttest_ind(electronics, other, equal_var=False, alternative="two-sided")
    n1, n2 = len(electronics), len(other)
    m1, m2 = electronics.mean(), other.mean()
    difference = m1 - m2
    relative_difference = difference / m2 * 100
    v1, v2 = electronics.var(ddof=1), other.var(ddof=1)
    se = math.sqrt(v1 / n1 + v2 / n2)
    welch_df = (v1 / n1 + v2 / n2) ** 2 / (((v1 / n1) ** 2) / (n1 - 1) + ((v2 / n2) ** 2) / (n2 - 1))
    critical = stats.t.ppf(1 - ALPHA / 2, welch_df)
    ci_low, ci_high = difference - critical * se, difference + critical * se
    pooled_sd = math.sqrt(((n1 - 1) * v1 + (n2 - 1) * v2) / (n1 + n2 - 2))
    cohen_d = difference / pooled_sd
    u_stat, u_p = stats.mannwhitneyu(electronics, other, alternative="two-sided")

    effect = "Negligible" if abs(cohen_d) < 0.2 else ("Small" if abs(cohen_d) < 0.5 else ("Medium" if abs(cohen_d) < 0.8 else "Large"))
    results = pd.DataFrame([
        ("Analysis unit", "Order"),
        ("Mixed-category/anomalous orders excluded", len(mixed_ids)),
        ("All valid orders", len(sample) + len(mixed_ids)),
        ("Hypothesis-test orders", len(sample)),
        ("Electronics orders", n1),
        ("Other-category orders", n2),
        ("Electronics order-level AOV", round(m1, 2)),
        ("Other-category order-level AOV", round(m2, 2)),
        ("Electronics median order value", round(electronics.median(), 2)),
        ("Other-category median order value", round(other.median(), 2)),
        ("Electronics standard deviation", round(electronics.std(ddof=1), 2)),
        ("Other-category standard deviation", round(other.std(ddof=1), 2)),
        ("Observed difference", round(difference, 2)),
        ("Relative difference", round(relative_difference, 2)),
        ("t-statistic", round(t_stat, 4)),
        ("p-value", round(p_value, 4)),
        ("Welch degrees of freedom", round(welch_df, 2)),
        ("95% CI lower", round(ci_low, 2)),
        ("95% CI upper", round(ci_high, 2)),
        ("Cohen's d", round(cohen_d, 4)),
        ("Effect size interpretation", effect),
        ("Mann-Whitney U", round(u_stat, 4)),
        ("Mann-Whitney p-value", round(u_p, 4)),
        ("Decision", "Fail to reject H0" if p_value >= ALPHA else "Reject H0"),
    ], columns=["Metric", "Result"])
    results.to_csv(OUT / "hypothesis_test_results.csv", index=False)
    return {
        "electronics": electronics, "other": other, "t_stat": t_stat, "p_value": p_value,
        "difference": difference, "relative_difference": relative_difference,
        "ci_low": ci_low, "ci_high": ci_high, "welch_df": welch_df,
        "cohen_d": cohen_d, "u_stat": u_stat, "u_p": u_p, "effect": effect,
    }


def create_charts(monthly, city, category, test):
    """Regenerate all supporting charts so the project is fully reproducible."""
    # Monthly revenue
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(monthly["Month_Label"], monthly["Total_Sales"], marker="o")
    ax.set_title("Monthly Revenue")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue (₹)")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(CHARTS / "monthly_revenue.png", dpi=180)
    plt.close(fig)

    # City revenue
    top = city.sort_values("Total_Sales", ascending=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(top["City"], top["Total_Sales"])
    ax.set_title("Revenue by City")
    ax.set_xlabel("Revenue (₹)")
    fig.tight_layout()
    fig.savefig(CHARTS / "city_revenue.png", dpi=180)
    plt.close(fig)

    # Category revenue
    cat = category.sort_values("Revenue", ascending=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(cat["Category"], cat["Revenue"])
    ax.set_title("Revenue by Category")
    ax.set_xlabel("Revenue (₹)")
    fig.tight_layout()
    fig.savefig(CHARTS / "category_revenue.png", dpi=180)
    plt.close(fig)

    # AOV boxplot
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.boxplot([test["other"], test["electronics"]], tick_labels=["Other", "Electronics"], showmeans=True)
    ax.set_title("Order-Level AOV Distribution")
    ax.set_ylabel("Order Value (₹)")
    fig.tight_layout()
    fig.savefig(CHARTS / "aov_boxplot.png", dpi=180)
    plt.close(fig)

    # Confidence interval chart
    diff = test["difference"]
    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.errorbar([0], [diff], yerr=[[diff - test["ci_low"]], [test["ci_high"] - diff]], fmt="o", capsize=7)
    ax.axhline(0, linestyle="--")
    ax.set_xticks([0])
    ax.set_xticklabels(["Electronics − Other AOV"])
    ax.set_ylabel("Mean Difference (₹)")
    ax.set_title("95% Confidence Interval for Mean AOV Difference")
    fig.tight_layout()
    fig.savefig(CHARTS / "aov_confidence_interval.png", dpi=180)
    plt.close(fig)


def create_reports(df, clean, order_level, monthly, city, category, test):
    peak = monthly.loc[monthly["Total_Sales"].idxmax()]
    top_city, second_city = city.iloc[0], city.iloc[1]
    top_category = category.sort_values("Revenue", ascending=False).iloc[0]

    report = f"""# Task-4 Hypothesis Testing Summary

## Business Question

Do Electronics orders have a different average order value from orders in all other categories?

## Analysis Unit

Order-level analysis. Total_Sales is aggregated by Order_ID before group comparison.

## Data Handling Rule

Order_ID ORD100050 appears across multiple records with multiple categories and inconsistent order-level attributes. The anomalous Order_ID is retained for descriptive row-level revenue analysis but excluded from the two-group AOV hypothesis test.

## Hypotheses

H0: The mean order value for Electronics equals the mean order value for all other categories.

H1: The mean order value for Electronics differs from the mean order value for all other categories.

## Primary Test

Welch two-sample t-test, two-sided, alpha = 0.05.

## Sensitivity Test

Two-sided Mann-Whitney U test.

## Results

- Electronics orders: {len(test['electronics'])}
- Other-category orders: {len(test['other'])}
- Electronics order-level AOV: ₹{test['electronics'].mean():,.2f}
- Other-category order-level AOV: ₹{test['other'].mean():,.2f}
- Observed difference: ₹{test['difference']:,.2f}, or {test['relative_difference']:.2f}%
- t-statistic: {test['t_stat']:.4f}
- p-value: {test['p_value']:.4f}
- 95% confidence interval: ₹{test['ci_low']:,.2f} to ₹{test['ci_high']:,.2f}
- Cohen's d: {test['cohen_d']:.4f}
- Effect size interpretation: {test['effect']}
- Mann-Whitney U p-value: {test['u_p']:.4f}
- Decision: Fail to reject H0

## Interpretation

Electronics has a higher observed order-level AOV, but the p-value is above 0.05 and the confidence interval includes zero.

Cohen's d indicates a negligible standardized effect.

A non-significant result does not prove identical group means or establish causation.

## Business Conclusion

Treat the Electronics AOV difference as a monitoring signal rather than a proven performance advantage.

Segment the metric by product and city, then validate pricing or promotion decisions through controlled testing.

## Limitations

- Historical observational sales data.
- No causal inference.
- Product mix, customer behavior, city, quantity, and pricing influence order value.
- The two-group test does not control for all business drivers.
- Very small effects require sufficient statistical power to detect reliably.
"""
    (OUT / "hypothesis_test_results.md").write_text(report.strip() + "\n", encoding="utf-8")

    summary = f"""# Task-4 Analysis Summary

## Dataset

- Original sales records: {len(df):,}
- Excluded records: {len(df) - len(clean):,}
- Valid descriptive records: {len(clean):,}
- Exclusion rate: {(len(df) - len(clean)) / len(df) * 100:.2f}%
- Date range: {clean['Order_Date'].min().strftime('%Y-%m-%d')} to {clean['Order_Date'].max().strftime('%Y-%m-%d')}
- Distinct cleaned Order_ID values: {clean['Order_ID'].nunique():,}
- Unique Customer_ID values: {clean['Customer_ID'].nunique():,}
- Total revenue: ₹{clean['Total_Sales'].sum():,.2f}
- Average row-level sales value: ₹{clean['Total_Sales'].mean():,.2f}
- Overall order-level AOV: ₹{order_level['Order_Value'].mean():,.2f}

## Key Findings

- Peak revenue month: {peak['Month_Label']}, ₹{peak['Total_Sales']:,.2f}
- Top city: {top_city['City']}, ₹{top_city['Total_Sales']:,.2f}, {top_city['Revenue_Share_Percent']:.2f}% of total revenue
- Second-highest city: {second_city['City']}, ₹{second_city['Total_Sales']:,.2f}, {second_city['Revenue_Share_Percent']:.2f}% of total revenue
- Top category: {top_category['Category']}, ₹{top_category['Revenue']:,.2f}, {top_category['Revenue_Share_Percent']:.2f}% of total revenue

## Statistical Validation

- Electronics order-level AOV: ₹{test['electronics'].mean():,.2f}
- Other-category order-level AOV: ₹{test['other'].mean():,.2f}
- Observed difference: ₹{test['difference']:,.2f}
- Relative difference: {test['relative_difference']:.2f}%
- t-statistic: {test['t_stat']:.4f}
- p-value: {test['p_value']:.4f}
- 95% CI: ₹{test['ci_low']:,.2f} to ₹{test['ci_high']:,.2f}
- Cohen's d: {test['cohen_d']:.4f}
- Mann-Whitney U p-value: {test['u_p']:.4f}
- Decision: Fail to reject H0

## Business Conclusion

Electronics has a higher observed order-level AOV, but the available evidence does not establish a statistically significant difference.

Monitor the metric, investigate drivers, and use controlled testing for future pricing or promotion decisions.
"""
    (OUT / "analysis_summary.md").write_text(summary.strip() + "\n", encoding="utf-8")


def main():
    df = load_data()
    clean = validate_data(df)
    order_level = build_order_level(clean)
    hypothesis_sample, mixed_ids = create_hypothesis_sample(clean, order_level)

    clean_export = clean.copy()
    clean_export["Order_Date"] = clean_export["Order_Date"].dt.strftime("%Y-%m-%d")
    clean_export.to_csv(OUT / "validated_sales.csv", index=False)

    create_quality_audit(df, clean, order_level, mixed_ids, hypothesis_sample)
    monthly, city, category = create_descriptive_outputs(clean, order_level)
    test = run_hypothesis_test(hypothesis_sample, mixed_ids)
    create_reports(df, clean, order_level, monthly, city, category, test)
    create_charts(monthly, city, category, test)

    # Reproducibility checks.
    assert len(df) == 1000
    assert len(clean) == 987
    assert len(order_level) == 980
    assert len(hypothesis_sample) == 979
    assert len(test["electronics"]) == 347
    assert len(test["other"]) == 632
    assert round(test["p_value"], 4) == 0.2546
    assert round(test["cohen_d"], 4) == 0.0776
    assert round(test["ci_low"], 2) == -6356.95
    assert round(test["ci_high"], 2) == 23966.94

    print("Task-4 analysis completed successfully.")
    print("p-value:", round(test["p_value"], 4))
    print("Cohen's d:", round(test["cohen_d"], 4))
    print("Decision: Fail to reject H0")


if __name__ == "__main__":
    main()
