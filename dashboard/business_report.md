\# Customer Churn Dashboard Business Report



\## Project Overview



This report summarizes the key findings from the Customer Churn Power BI Dashboard developed as part of the Customer Churn Prediction BI Platform project.



The dashboard connects to the project's SQLite database (`churn.db`) through an ODBC connection and provides interactive insights into customer demographics, churn behavior, revenue impact, and machine learning model performance.



The dashboard contains five pages:



1\. Executive Overview

2\. Customer Demographics

3\. Churn Drivers

4\. Revenue Impact

5\. Model Predictions



\---



\# Executive Summary



The analysis shows that customer churn remains a significant business challenge.



Out of \*\*7,043 customers\*\*, \*\*1,869 customers\*\* have churned, resulting in an overall \*\*churn rate of 26.54%\*\*.



The dashboard identifies the customer groups most likely to churn, highlights the financial impact of churn, and presents a predictive machine learning model that can help identify customers at risk before they leave.



\---



\# Dashboard Findings



\## 1. Executive Overview



The Executive Overview page provides a high-level summary of customer churn.



\### Key Metrics



\- Total Customers: \*\*7,043\*\*

\- Active Customers: \*\*5,174\*\*

\- Churned Customers: \*\*1,869\*\*

\- Overall Churn Rate: \*\*26.54%\*\*



\### Key Insights



\- Approximately one in every four customers has churned.

\- Month-to-Month contracts experience substantially higher churn than One-Year and Two-Year contracts.

\- Customers with shorter tenure are significantly more likely to churn.

\- The dashboard highlights the Top 5 churn reasons to support targeted retention initiatives.



\---



\## 2. Customer Demographics



This page explores how customer characteristics relate to churn.



\### Key Insights



\- Senior citizens experience a higher churn rate than non-senior customers.

\- Customers without partners or dependents are more likely to churn.

\- Churn differs across gender and demographic groups.

\- Internet service adoption and phone service usage vary across the customer base.



Understanding these demographic patterns enables more targeted customer retention strategies.



\---



\## 3. Churn Drivers



The Churn Drivers page identifies the factors most strongly associated with customer churn.



\### Key Insights



\- Month-to-Month contract customers are the highest-risk customer segment.

\- Customers with shorter tenure exhibit the greatest likelihood of churning.

\- Internet service type influences churn behavior.

\- Payment method also affects customer retention.

\- The Top 5 churn reasons provide actionable insight into customer dissatisfaction.



These findings help identify where retention efforts will have the greatest impact.



\---



\## 4. Revenue Impact



Customer churn has a measurable financial impact on the business.



The dashboard compares:



\- Revenue from Active Customers

\- Revenue from Churned Customers

\- Average Monthly Charges

\- Average Total Charges

\- Average Customer Lifetime Value (CLTV)



\### Key Insights



\- Churned customers represent a substantial loss in recurring revenue.

\- Higher-value customers contribute significantly to revenue and should be prioritised for retention.

\- CLTV provides an effective measure for identifying customers deserving proactive engagement.



\---



\## 5. Model Predictions



Five machine learning models were evaluated for customer churn prediction.



\### Models Evaluated



\- Logistic Regression

\- Decision Tree

\- Random Forest

\- XGBoost

\- LightGBM



Following the latest model evaluation, \*\*Logistic Regression\*\* was selected as the production model.



\### Selected Model Performance



| Metric | Value |

|---------|------:|

| Accuracy | \*\*91.77%\*\* |

| Precision | \*\*83.77%\*\* |

| Recall | \*\*85.56%\*\* |

| ROC AUC | \*\*97.43%\*\* |



The selected model demonstrates strong predictive performance and can assist the business in identifying customers who are likely to churn before cancellation occurs.



\---



\# Business Recommendations



\## Recommendation 1



Develop targeted retention campaigns for customers on Month-to-Month contracts by offering incentives to migrate to longer-term contracts.



\---



\## Recommendation 2



Use the Logistic Regression model to identify high-risk customers and proactively engage them before they churn.



\---



\## Recommendation 3



Prioritize customers with high Customer Lifetime Value (CLTV) by offering personalized retention strategies and loyalty incentives.



\---



\## Recommendation 4



Address the leading churn reasons identified in the dashboard through improvements in pricing, customer support, and service quality.



\---



\## Recommendation 5



Monitor customer churn continuously using the Power BI dashboard to evaluate the effectiveness of retention initiatives and support data-driven decision-making.



\---



\# Conclusion



The Customer Churn Dashboard provides a comprehensive view of customer behavior, churn trends, revenue impact, and predictive analytics.



By combining descriptive analytics with machine learning insights, the dashboard enables stakeholders to identify at-risk customers, understand the primary causes of churn, and implement effective retention strategies that improve customer satisfaction and long-term business performance.

