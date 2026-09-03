# Data Dictionary

| Field | Description |
|---|---|
| Order_ID | Identifier used for order-level aggregation. |
| Order_Date | Transaction date. |
| Customer_ID | Customer identifier. |
| Customer_Name | Customer name field. |
| Age | Customer age field. |
| Gender | Customer gender field. |
| City | Sales city. |
| Product | Product purchased. |
| Category | Product category. |
| Quantity | Quantity recorded for the row. |
| Unit_Price | Unit price recorded for the row. |
| Total_Sales | Sales value used for revenue and order-value calculations. |

Analysis rule:

Total_Sales is summed by Order_ID for order-level AOV analysis.

Data-quality rule:

Rows missing Order_Date, Total_Sales, Category, or City are excluded from the validated descriptive dataset. The original source workbook is preserved unchanged.
