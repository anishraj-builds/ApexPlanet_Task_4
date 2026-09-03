# Task-4 Analysis Summary

## Dataset

- Original sales records: 1,000
- Excluded records: 13
- Valid descriptive records: 987
- Exclusion rate: 1.30%
- Date range: 2025-01-01 to 2026-01-01
- Distinct cleaned Order_ID values: 980
- Unique Customer_ID values: 936
- Total revenue: ₹137,858,822.11
- Average row-level sales value: ₹139,674.59
- Overall order-level AOV: ₹140,672.27

## Key Findings

- Peak revenue month: Mar 2025, ₹12,973,502.90
- Top city: Patna, ₹19,285,966.89, 13.99% of total revenue
- Second-highest city: Kolkata, ₹18,884,349.57, 13.70% of total revenue
- Top category: Electronics, ₹50,362,716.23, 36.53% of total revenue

## Statistical Validation

- Electronics order-level AOV: ₹145,037.74
- Other-category order-level AOV: ₹136,232.75
- Observed difference: ₹8,804.99
- Relative difference: 6.46%
- t-statistic: 1.1403
- p-value: 0.2546
- 95% CI: ₹-6,356.95 to ₹23,966.94
- Cohen's d: 0.0776
- Mann-Whitney U p-value: 0.3598
- Decision: Fail to reject H0

## Business Conclusion

Electronics has a higher observed order-level AOV, but the available evidence does not establish a statistically significant difference.

Monitor the metric, investigate drivers, and use controlled testing for future pricing or promotion decisions.
