# Customer Churn Model Comparison

| model_name          |   accuracy |   precision |   recall |   roc_auc | confusion_matrix       |
|:--------------------|-----------:|------------:|---------:|----------:|:-----------------------|
| Logistic Regression |   0.917672 |    0.837696 | 0.855615 |  0.974275 | [[973, 62], [54, 320]] |
| Decision Tree       |   0.908446 |    0.819843 | 0.839572 |  0.886453 | [[966, 69], [60, 314]] |
| Random Forest       |   0.927608 |    0.867568 | 0.858289 |  0.966707 | [[986, 49], [53, 321]] |
| XGBoost             |   0.92335  |    0.853723 | 0.858289 |  0.979212 | [[980, 55], [53, 321]] |
| LightGBM            |   0.930447 |    0.863158 | 0.877005 |  0.981767 | [[983, 52], [46, 328]] |

## Selected Model

**LightGBM**

### Performance

- Accuracy: 0.9304
- Precision: 0.8632
- Recall: 0.8770
- ROC AUC: 0.9818
- Confusion Matrix: [[983, 52], [46, 328]]

## Why this model was selected

LightGBM was selected because it achieved the highest ROC AUC (0.9818), which was the primary model selection criterion. It also demonstrated strong overall performance across accuracy, precision, and recall, making it the best balance of predictive performance among the evaluated models.