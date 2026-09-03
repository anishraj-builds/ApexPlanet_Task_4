# ApexPlanet Task-4, Data Storytelling & Statistical Validation

## 1. Project Objective

Synthesize the sales analysis into a concise stakeholder story, validate a business hypothesis statistically, interpret the evidence, and recommend evidence-based actions.

## 2. Business Question

Do Electronics orders have a different average order value from orders in all other categories?

H0: Mean Electronics order value = Mean Other-category order value.

H1: Mean Electronics order value ≠ Mean Other-category order value.

## 3. Dataset and Validation

- Source records: 1,000
- Excluded records: 13, due to missing fields required for validated descriptive analysis
- Valid descriptive records: 987
- Exclusion rate: 1.30%
- Distinct cleaned orders: 980
- Unique customers: 936
- Total revenue: ₹137,858,822.11
- Overall order-level AOV: ₹140,672.27
- Analysis period: 2025-01-01 to 2026-01-01

ORD100050 is a mixed-category anomalous order. It is retained for descriptive row-level analysis and excluded from the two-group hypothesis test to avoid category-classification bias.

## 4. Key Business Findings

- Peak month: March 2025, ₹12,973,502.90
- Top city: Patna, ₹19,285,966.89
- Second city: Kolkata, ₹18,884,349.57
- Top category: Electronics, ₹50,362,716.23
- Electronics order-level AOV: ₹145,037.74
- Other-category order-level AOV: ₹136,232.75
- Observed difference: ₹8,804.99, 6.46%

## 5. Statistical Validation

Primary test: Welch two-sample t-test, two-sided, α = 0.05.

- Electronics orders: 347
- Other-category orders: 632
- t-statistic: 1.1403
- Welch degrees of freedom: 675.04
- p-value: 0.2546
- 95% CI: ₹-6,356.95 to ₹23,966.94
- Cohen's d: 0.0776, negligible
- Mann-Whitney U sensitivity p-value: 0.3598
- Decision: Fail to reject H0

## 6. Business Interpretation

Electronics has a higher observed order-level AOV, but the available evidence does not establish a statistically significant difference.

The confidence interval includes zero, so the direction of the population mean difference is uncertain. The result does not establish causation or prove identical group means.

## 7. Recommended Actions

- Monitor Electronics AOV over future observations.
- Segment AOV by product and city.
- Review demand drivers around March 2025.
- Prioritize Patna and Kolkata for commercial review.
- Use controlled pricing or promotion experiments before broad changes.
- Re-test with future observations.

## 8. Project Structure

```text
ApexPlanet_Task_4/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── ApexPlanet_DataAnalytics_Dataset.xlsx
│   └── Task_4_Analysis_Workbook.xlsx
├── analysis/
│   └── task4_analysis.py
├── documentation/
│   ├── Data_Dictionary.md
│   └── Task_4_Hypothesis_Testing_Summary.md
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
│   └── charts/
│       ├── monthly_revenue.png
│       ├── city_revenue.png
│       ├── category_revenue.png
│       ├── aov_boxplot.png
│       └── aov_confidence_interval.png
└── presentation/
    ├── Task_4_Data_Storytelling_Deck.pptx
    └── apexplanet_task4_stakeholder_presentation.mp4   

```

## 9. Reproducibility

From the project root:

```bash
pip install -r requirements.txt
python analysis/task4_analysis.py
```

The script regenerates the analytical CSV/Markdown outputs and all five supporting charts.

Core validation checks include:

- 1,000 source records
- 987 valid descriptive records
- 980 distinct cleaned orders
- 979 hypothesis-test orders
- 347 Electronics orders
- 632 Other-category orders
- p = 0.2546
- Cohen's d = 0.0776
- 95% CI = ₹-6,356.95 to ₹23,966.94
- Fail to reject H0

## 10. Final Presentation

The final stakeholder deck contains 10 concise slides:

1. Title
2. Business Performance Snapshot
3. Analysis Scope and Group Definition
4. Electronics Shows a Higher Observed AOV
5. Hypotheses and Statistical Test
6. Statistical Test Results
7. Confidence Interval Includes Zero
8. Statistical Interpretation and Next Test
9. Business Decision and Next Options
10. Tactical Action Plan for the Next Experiment

The deck is designed for a concise stakeholder presentation.

## 11. Limitations

- Historical observational sales data.
- No causal inference.
- One mixed-category anomalous order is excluded from the two-group AOV test.
- Product mix, pricing, quantity, city, and customer behavior influence order value.
- The two-group test does not control for all business drivers.
- A non-significant result does not prove identical group means.
- Very small effects require sufficient statistical power to detect reliably.

## 12. Deliverables

- Source dataset
- Analysis workbook
- Reproducible Python analysis
- Data-quality audit
- Statistical results
- Supporting CSV outputs
- Supporting charts
- Data dictionary
- Hypothesis-testing summary
- Final PowerPoint

The stakeholder video is included in the presentation folder.

## 13. Final Quality Control

The project uses one source dataset, one reproducible analysis script, one validated statistical methodology, and one final presentation. Numerical findings are regenerated from the source workbook and checked against the documented statistical results.

## 14. Author

Anish Raj.R

ApexPlanet Internship Task-4
Data Storytelling & Statistical Validation
