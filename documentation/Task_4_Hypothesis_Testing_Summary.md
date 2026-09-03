# Task-4 Hypothesis Testing Summary

## Business Question

Do Electronics orders have a different average order value from orders in all other categories?

## Analysis Unit

Order-level analysis. Total_Sales is aggregated by Order_ID before group comparison.

## Data Handling

ORD100050 is a mixed-category anomalous order with inconsistent order-level attributes. It is retained for descriptive analysis and excluded from the two-group AOV hypothesis test.

## Hypotheses

H0: Mean Electronics order value = Mean Other-category order value.

H1: Mean Electronics order value ≠ Mean Other-category order value.

## Primary Test

Welch two-sample t-test, two-sided, α = 0.05.

## Sensitivity Test

Two-sided Mann-Whitney U test.

## Results

- Electronics orders: 347
- Other-category orders: 632
- Electronics order-level AOV: ₹145,037.74
- Other-category order-level AOV: ₹136,232.75
- Observed difference: ₹8,804.99, 6.46%
- t-statistic: 1.1403
- p-value: 0.2546
- 95% confidence interval: ₹-6,356.95 to ₹23,966.94
- Cohen's d: 0.0776
- Effect size interpretation: Negligible
- Mann-Whitney U p-value: 0.3598
- Decision: Fail to reject H0

## Interpretation

Electronics has a higher observed order-level AOV, but the p-value is above 0.05 and the confidence interval includes zero.

Cohen's d of 0.0776 indicates a negligible standardized effect.

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
