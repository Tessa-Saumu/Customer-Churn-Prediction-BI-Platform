# Customer Churn Prediction BI Platform

## Joyce's Project Documentation

**Role:** Business Intelligence & Power BI Developer  
**Project:** Customer Churn Prediction & BI Platform  
**Primary Tool:** Microsoft Power BI  
**Data Source:** SQLite / ODBC  
**Repository:** Customer-Churn-Prediction-BI-Platform  
**GitHub:** joyce-ai4health

---

## 1. Project Overview

The Customer Churn Prediction BI Platform was a collaborative end-to-end analytics project designed to help a telecommunications business identify customers who are likely to churn and turn analytical results into actionable business insights.

The complete project combined:

- Data ingestion and cleaning
- SQLite database development
- SQL analysis
- Feature engineering
- Machine learning model training and evaluation
- FastAPI prediction services
- Power BI business intelligence
- Business reporting
- Testing and validation

My primary contribution was the **Business Intelligence and Power BI dashboard development**.

---

## 2. My Role

I worked primarily on the **Power BI and Business Intelligence component** of the project.

My responsibilities included:

- Connecting Power BI to the project SQLite database through ODBC.
- Working with SQL views created by the SQL team.
- Building the five required Power BI dashboard pages.
- Creating DAX measures for dashboard KPIs.
- Connecting model evaluation results to the Model Predictions page.
- Developing business-focused visualizations.
- Writing dashboard insights and recommendations.
- Testing and validating dashboard results.
- Addressing issues identified during project review.
- Maintaining my GitHub branch and submitting the completed work through a Pull Request.

My assigned project task was **Issue #12 — Power BI Dashboard – 5 Pages via ODBC Connection – Joyce**.

---

## 3. Power BI Dashboard Development

I developed five dashboard pages:

### 3.1 Executive Overview

This page provides a high-level view of customer churn.

Key elements include:

- Total customers
- Overall churn rate
- Customer churn KPIs
- High-level business indicators
- Visual summaries of the customer base

### 3.2 Customer Demographics

This page examines churn across customer demographic groups.

The analysis includes:

- Gender
- Senior citizen status
- Partner status
- Dependents
- Other available demographic attributes

The purpose was to identify customer groups with noticeably different churn patterns.

### 3.3 Churn Drivers

This page investigates the major factors associated with customer churn.

The analysis includes:

- Contract type
- Tenure
- Internet service
- Technology support
- Online security
- Payment method
- Other relevant churn indicators

The dashboard showed particularly high churn among month-to-month customers and customers in their early tenure period.

### 3.4 Revenue Impact

This page connects customer churn to financial impact.

The analysis includes:

- Monthly charges
- Total charges
- Revenue associated with churned customers
- Comparison of churned and retained customers

This helped move the analysis from simply asking:

> "Who is churning?"

to:

> "What is the financial impact of that churn?"

### 3.5 Model Predictions

This page presents the performance of the machine learning models.

The dashboard compares:

- Logistic Regression
- LightGBM
- XGBoost
- Random Forest
- Decision Tree

Metrics include:

- Accuracy
- Precision
- Recall
- ROC AUC

The page also contains a model performance comparison and confusion-matrix information.

---

## 4. Technical Implementation

### SQLite + ODBC

The dashboard was connected to the project's SQLite database through an ODBC connection.

The workflow was:

```text
SQLite Database
      ↓
ODBC Connection
      ↓
Power BI
      ↓
SQL Views / Tables
      ↓
DAX Measures
      ↓
Dashboard Visualizations
````

This allowed the dashboard to use project data rather than manually entering final dashboard values.

---

## 5. DAX Development

One important part of the dashboard development was replacing hardcoded dashboard values with dynamic DAX logic.

For example, the Best Model was initially hardcoded as:

```DAX
Best Model = 
"Logistic Regression"
```

This was later changed to a dynamic calculation that identifies the model with the highest ROC AUC:

```DAX
Best Model = 
CALCULATE(
    SELECTEDVALUE(model_comparison[Model]),
    TOPN(
        1,
        model_comparison,
        model_comparison[ROC_AUC],
        DESC
    )
)
```

This means the dashboard can determine the best-performing model from the data rather than relying on a manually entered model name.

I also created dynamic measures for the model evaluation summary and confusion matrix summary.

---

## 6. Dashboard Validation

I validated the dashboard by checking that:

* The dashboard opened successfully.
* All five pages were present.
* Dashboard visuals displayed correctly.
* Model comparison metrics matched the evaluation data.
* DAX measures returned the expected values.
* The selected model updated dynamically.
* Model evaluation information responded to visual filtering.
* The dashboard did not rely on manually entered final metric values.

I also tested the dashboard after the reviewed changes were applied.

---

## 7. Challenges and Problem Solving

One of the important parts of the project was dealing with issues that appeared during development and review.

### ODBC / Power BI Data-Type Issue

Some SQL view values were returned through the SQLite ODBC connection as text rather than numeric values.

This affected the churn-rate fields.

I resolved the issue by converting the affected values to numeric data types in Power Query before using them in DAX.

### Model Evaluation Updates

The selected model changed during the project as the machine-learning evaluation was updated.

Instead of leaving the dashboard dependent on a hardcoded model name, I updated the Model Predictions page to use dynamic DAX logic.

### Dashboard Review

The dashboard went through a review process.

I implemented the requested corrections and verified the updated dashboard before committing the final Power BI file.

---

## 8. GitHub Collaboration

I used GitHub throughout the project to manage and document my work.

My workflow included:

1. Working on my assigned dashboard branch.
2. Pulling the latest project changes.
3. Updating the Power BI dashboard.
4. Testing the dashboard locally.
5. Committing changes with descriptive commit messages.
6. Pushing the changes to GitHub.
7. Submitting the work through the project Pull Request.
8. Applying review feedback.
9. Committing the final reviewed dashboard.

The completed dashboard was submitted through the project's Power BI Pull Request.

---

## 9. Business Insights

The dashboard analysis identified several important churn patterns.

### Month-to-Month Customers

Month-to-month customers showed substantially higher churn than customers on longer-term contracts.

This suggests that contract upgrades and retention incentives could be useful strategies.

### Early-Tenure Customers

Customers within their first year showed considerably higher churn.

This suggests that the first 12 months are an important period for customer retention activities.

### Technology Support and Security

Customers without technology support or online security showed higher churn rates.

These services could therefore be considered as part of customer onboarding and retention strategies.

### Fiber Optic Customers

Fiber optic customers showed higher churn than DSL customers.

This suggests that the business should investigate potential issues around service quality, pricing, customer expectations, or competition.

---

## 10. Business Recommendations

Based on the dashboard analysis, I identified several possible actions:

1. Encourage month-to-month customers to move to longer-term contracts.
2. Strengthen retention activities during the customer's first year.
3. Consider bundling technology support and online security with customer onboarding.
4. Investigate fiber-optic service quality and pricing.
5. Use model predictions to prioritize high-risk customers for retention campaigns.

---

## 11. Final Deliverables

My main deliverables were:

* Power BI dashboard
* Five completed dashboard pages
* DAX measures
* Model comparison visualizations
* Business insights
* Business recommendations
* Dashboard documentation
* GitHub commits and Pull Request
* Final reviewed Power BI `.pbix` file

---

## 12. What I Learned

This project gave me practical experience beyond simply creating Power BI charts.

I learned how to:

* Connect Power BI to a SQLite database through ODBC.
* Work with SQL views created by another team member.
* Transform and clean data before visualization.
* Create DAX measures.
* Build a multi-page business dashboard.
* Translate machine-learning evaluation metrics into business language.
* Validate dashboard results against source data.
* Troubleshoot data-type and visualization problems.
* Work with Git and GitHub in a collaborative project.
* Respond to technical review feedback.
* Document my contribution to a larger data project.

---

## 13. Project Outcome

The final result was an interactive five-page Power BI dashboard that brought together customer churn analysis, demographic insights, churn drivers, revenue impact, and machine-learning model evaluation.

My contribution focused on transforming the project's underlying data and analytical outputs into a business-facing BI solution that could be used to understand churn and support retention decisions.

---

## 14. Supporting Evidence

Detailed evidence of my contribution can be found through:

* GitHub project repository
* Issue #12
* Power BI dashboard
* Pull Request #28
* GitHub commit history
* Dashboard screenshots
* Business report
* Model evaluation outputs

```

