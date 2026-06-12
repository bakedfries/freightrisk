
# FreightRisk Final V2 Outputs

This folder contains final exported results from the FreightRisk capstone modeling notebook.

## Folder Structure

- tables/
  - final model comparison tables
  - ensemble comparison tables
  - risk band summary
  - scored test-set orders
  - threshold tuning results

- figures/
  - model comparison visuals
  - ensemble comparison visual
  - final candidate comparison visual
  - risk band visuals

- models/
  - exported final fitted model objects using joblib

## Final Model Decision

Primary final model:
Gradient Boosting at threshold 0.40

Best ensemble:
Stacking Ensemble at threshold 0.35

High-recall backup:
Random Forest at threshold 0.30

## Main Modeling Conclusion

Gradient Boosting had the strongest held-out test F1 score and the lowest total error count.
Stacking was the strongest ensemble and performed almost as well as Gradient Boosting.
Random Forest had the strongest recall and the fewest false negatives.

## Use Case

FreightRisk is a constraint-aware freight risk decision-support system.
It scores orders by predicted freight infeasibility and converts probabilities into Low, Medium, High, and Critical risk bands.
