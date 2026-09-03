# ApexPlanet Internship Task-4

Python Data Analytics Internship Project

## Data Storytelling & Statistical Validation

Author: Anish Raj.R

Internship: ApexPlanet Software Pvt. Ltd.

---

> This project demonstrates an end-to-end data analytics workflow using business performance analysis, data quality validation, AOV comparison, hypothesis testing, statistical validation, data visualization and evidence-based business recommendations.

## Project Objective

The objective of Task-4 is to synthesize sales analysis into a concise stakeholder story, validate a business hypothesis statistically, interpret the evidence, and recommend evidence-based business actions.

The project uses Python, Pandas, Excel, SciPy, Matplotlib and Python-based data analysis and visualization.

## Project Links

- GitHub Repository: https://github.com/anishraj-builds/ApexPlanet_Task_4
  
- Final Presentation: `presentation/Task_4_Data_Storytelling_Deck.pptx`
  
- Stakeholder Video: `presentation/apexplanet_task4_stakeholder_presentation.mp4`

---

## Project Overview

The analysis uses the ApexPlanet sales dataset containing 1,000 source records.

The workflow covers:

- Data loading and validation
- Data quality auditing
- Business performance analysis
- Monthly revenue analysis
- City revenue analysis
- Category revenue analysis
- Order-level AOV calculation
- Electronics versus Other-category AOV comparison
- Hypothesis formulation
- Welch two-sample t-test
- Mann-Whitney U sensitivity testing
- Confidence interval analysis
- Effect-size analysis using Cohen's d
- Statistical decision-making
- Business interpretation
- Evidence-based recommendations
- Stakeholder presentation development

The final project converts the analytical findings into a concise business story supported by statistical evidence.

---

## Project Workflow

ApexPlanet Sales Dataset
↓
Data Quality Validation
↓
Validated Sales Data
↓
Business Performance Analysis
↓
Order-Level AOV Analysis
↓
Electronics vs Other-category Comparison
↓
Hypothesis Formulation
↓
Welch Two-Sample t-Test
↓
Confidence Interval and Effect Size
↓
Mann-Whitney U Sensitivity Test
↓
Statistical Decision
↓
Business Interpretation
↓
Business Recommendations
↓
Stakeholder Presentation

---

## Technologies Used

- Python
- Pandas
- NumPy
- SciPy
- Excel
- OpenPyXL
- Matplotlib
- Python-pptx

---

## Project Structure

```text
ApexPlanet_Task_4/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── ApexPlanet_DataAnalytics_Dataset.xlsx
│   └── Task_4_Analysis_Workbook.xlsx
│
├── analysis/
│   └── task4_analysis.py
│
├── documentation/
│   ├── Data_Dictionary.md
│   └── Task_4_Hypothesis_Testing_Summary.md
│
├── outputs/
│   ├── analysis_summary.md
│   ├── hypothesis_test_results.md
│   ├── hypothesis_test_results.csv
│   ├── data_quality_audit.csv
│   ├── monthly_revenue.csv
│   ├── city_revenue.csv
│   ├── category_analysis.csv
│   ├── order_level_sales.csv
│   ├── validated_sales.csv
│   ├── hypothesis_test_sample.csv
│   ├── mixed_category_orders.csv
│   │
│   └── charts/
│       ├── monthly_revenue.png
│       ├── city_revenue.png
│       ├── category_revenue.png
│       ├── aov_boxplot.png
│       └── aov_confidence_interval.png
│
└── presentation/
    ├── Task_4_Data_Storytelling_Deck.pptx
    └── apexplanet_task4_stakeholder_presentation.mp4
```

---

## Features

- Data quality validation
- Missing-value validation
- Source-record and exclusion tracking
- Revenue analysis by month
- Revenue analysis by city
- Revenue analysis by category
- Order-level AOV calculation
- Electronics versus Other-category AOV comparison
- Two-sided hypothesis testing
- Welch two-sample t-test
- 95% confidence interval
- Cohen's d effect-size measurement
- Mann-Whitney U sensitivity test
- Statistical decision based on α = 0.05
- Business interpretation of statistical evidence
- Evidence-based business recommendations
- Reproducible CSV and Markdown outputs
- Supporting statistical charts
- Final stakeholder presentation deck
- Final stakeholder presentation video

---

## Core KPI Results

| KPI | Result |
|---|---:|
| Source Records | 1,000 |
| Valid Descriptive Records | 987 |
| Excluded Records | 13 |
| Exclusion Rate | 1.30% |
| Distinct Cleaned Orders | 980 |
| Unique Customers | 936 |
| Total Revenue | ₹137,858,822.11 |
| Overall Order-Level AOV | ₹140,672.27 |
| Analysis Period | 2025-01-01 to 2026-01-01 |

The analysis uses validated descriptive records and aggregates Total_Sales by Order_ID for order-level AOV analysis.

---

## Data Quality

The dataset contains 1,000 source records.

13 records are excluded from validated descriptive analysis because required fields are missing, leaving 987 valid descriptive records.

Order_ID `ORD100050` is a mixed-category anomalous order with inconsistent order-level attributes. The order is retained for descriptive row-level revenue analysis and excluded from the two-group AOV hypothesis test to avoid category-classification bias.

The analysis therefore uses:

- 987 valid descriptive records
- 980 distinct cleaned orders
- 979 orders for the hypothesis test
- 347 Electronics orders in the hypothesis test
- 632 Other-category orders in the hypothesis test

This approach preserves the source data while making the data-quality limitation explicit.

---

## AOV Comparison

The primary business comparison evaluates order-level Average Order Value between Electronics and all other categories.

| Metric | Result |
|---|---:|
| Electronics AOV | ₹145,037.74 |
| Other-category AOV | ₹136,232.75 |
| Observed Difference | ₹8,804.99 |
| Relative Difference | 6.46% |

Electronics has the higher observed order-level AOV in the validated hypothesis-test sample.

The observed difference alone does not establish a statistically significant difference.

---

## Hypothesis Testing Methodology

### Business Question

Do Electronics orders have a different average order value from orders in all other categories?

### Null Hypothesis

H0: Mean Electronics order value = Mean Other-category order value.

### Alternative Hypothesis

H1: Mean Electronics order value ≠ Mean Other-category order value.

### Primary Statistical Test

Welch two-sample t-test, two-sided, with α = 0.05.

Welch's test is used for the two-group comparison without assuming equal population variances.

### Sensitivity Test

A two-sided Mann-Whitney U test is also performed as a non-parametric sensitivity check.

### Analysis Unit

The analysis is performed at the order level. Total_Sales is aggregated by Order_ID before comparing the two groups.

---

## Statistical Results

| Statistical Measure | Result |
|---|---:|
| Electronics Orders | 347 |
| Other-category Orders | 632 |
| t-statistic | 1.1403 |
| p-value | 0.2546 |
| Welch Degrees of Freedom | 675.04 |
| 95% Confidence Interval | ₹-6,356.95 to ₹23,966.94 |
| Cohen's d | 0.0776 |
| Effect Size | Negligible |
| Mann-Whitney U p-value | 0.3598 |
| Decision | Fail to reject H0 |

The p-value of 0.2546 is above the significance level of 0.05.

The 95% confidence interval includes zero.

Cohen's d of 0.0776 indicates a negligible standardized effect.

The Mann-Whitney U sensitivity test also gives a non-significant result with p = 0.3598.

---

## Statistical Decision

Decision: Fail to reject H0.

The analysis does not provide sufficient statistical evidence to conclude that Electronics orders have a different mean order value from Other-category orders at the 5% significance level.

The observed Electronics AOV is higher by ₹8,804.99, or 6.46%, but the available evidence does not establish a statistically significant difference.

A non-significant result does not prove identical group means and does not establish causation.

---

## Business Insights

### Electronics AOV

Electronics has an observed order-level AOV of ₹145,037.74 compared with ₹136,232.75 for Other-category orders.

### Revenue Performance

- Peak revenue month: March 2025, ₹12,973,502.90
- Top city: Patna, ₹19,285,966.89
- Second-highest city: Kolkata, ₹18,884,349.57
- Top category: Electronics, ₹50,362,716.23

### Statistical Evidence

The Electronics AOV difference should be treated as a monitoring signal rather than a proven performance advantage.

---

## Business Recommendations

- Monitor Electronics AOV over future observations.
- Segment AOV by product and city.
- Review demand drivers around March 2025.
- Prioritize Patna and Kolkata for commercial review.
- Use controlled pricing or promotion experiments before broad changes.
- Re-test the AOV comparison with future observations.

---

## Additional Commercial Findings

| Finding | Result |
|---|---:|
| Peak Revenue Month | March 2025 |
| Peak Monthly Revenue | ₹12,973,502.90 |
| Top City | Patna |
| Top City Revenue | ₹19,285,966.89 |
| Second-highest City | Kolkata |
| Second-highest City Revenue | ₹18,884,349.57 |
| Top Category | Electronics |
| Top Category Revenue | ₹50,362,716.23 |

---

## Supporting Charts

The project includes five reproducible supporting charts:

- `monthly_revenue.png`
- `city_revenue.png`
- `category_revenue.png`
- `aov_boxplot.png`
- `aov_confidence_interval.png`

These charts support the business performance analysis and statistical storytelling used in the final presentation.

---

## Video Demonstration

The final stakeholder presentation presents the business performance snapshot, analysis scope, AOV comparison, hypothesis testing, statistical results, business decision, interpretation and recommended actions.

### Video File

- `presentation/apexplanet_task4_stakeholder_presentation.mp4`

---

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Task-4 analysis

From the project root:

```bash
python analysis/task4_analysis.py
```

The script validates the source dataset, generates the descriptive analysis, performs the hypothesis test, creates the statistical outputs, and regenerates all five supporting charts.

Generated outputs include:

```text
outputs/analysis_summary.md
outputs/hypothesis_test_results.md
outputs/hypothesis_test_results.csv
outputs/data_quality_audit.csv
outputs/monthly_revenue.csv
outputs/city_revenue.csv
outputs/category_analysis.csv
outputs/order_level_sales.csv
outputs/validated_sales.csv
outputs/hypothesis_test_sample.csv
outputs/mixed_category_orders.csv
outputs/charts/
```

---

## Reproducibility and Validation

The Python analysis uses the source Excel dataset and applies the same validation rules, order-level aggregation, hypothesis definition and statistical methodology documented in the project.

Core validation checks include:

- 1,000 source records
- 987 valid descriptive records
- 980 distinct cleaned orders
- 979 hypothesis-test orders
- 347 Electronics orders
- 632 Other-category orders
- Electronics AOV = ₹145,037.74
- Other-category AOV = ₹136,232.75
- Observed difference = ₹8,804.99
- Relative difference = 6.46%
- t = 1.1403
- p = 0.2546
- 95% CI = ₹-6,356.95 to ₹23,966.94
- Cohen's d = 0.0776
- Mann-Whitney U p = 0.3598
- Decision = Fail to reject H0

The analysis script also contains reproducibility assertions for the core dataset and statistical results.

---

## Limitations

- The analysis uses historical observational sales data.
- The analysis does not establish causal relationships.
- One mixed-category anomalous Order_ID is excluded from the two-group AOV hypothesis test.
- Product mix, pricing, quantity, city and customer behavior influence order value.
- The two-group test does not control for all business drivers.
- A non-significant result does not prove identical group means.
- Very small effects require sufficient statistical power to detect reliably.

---

## Skills Demonstrated

- Python Programming
- Pandas
- NumPy
- Data Cleaning and Validation
- Excel Data Analysis
- KPI Analysis
- Business Performance Analysis
- AOV Analysis
- Hypothesis Testing
- Welch Two-Sample t-Test
- Mann-Whitney U Test
- Confidence Interval Analysis
- Effect Size Analysis
- Statistical Interpretation
- Data Visualization
- Business Storytelling
- Business Reporting
- Data-Driven Recommendations

---

## Project Status

Completed.

The project includes the source dataset, analysis workbook, reproducible Python analysis, data-quality audit, statistical results, supporting CSV outputs, supporting charts, data dictionary, hypothesis-testing summary, final PowerPoint deck and stakeholder presentation video.

---

## Author

Anish Raj.R

ApexPlanet Software Pvt. Ltd.

Internship Task-4: Data Storytelling & Statistical Validation
