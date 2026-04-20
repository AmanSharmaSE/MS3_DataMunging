#### SER541: Machine Learning Evaluation

#### Mexico City Airbnb Price Prediction

#### Aman Sharma

#### 2026-04-20

## Evaluation Metrics

### Metric 1

**Name:** Root Mean Squared Error (RMSE)

**Choice Justification:** RMSE is appropriate for this project because the prediction target is listing price, which is a continuous numeric variable. RMSE measures the average size of prediction error in the same units as the target variable, so it is easy to interpret in the Airbnb pricing domain. A lower RMSE means the model’s predicted prices are closer to the actual listing prices.

**Interpretation:** RMSE tells us how far off the model’s predictions are from the true Airbnb prices on average. Since price is measured directly in currency units, this metric is useful for understanding practical prediction quality.

### Metric 2

**Name:** Coefficient of Determination (R²)

**Choice Justification:** R² is appropriate because it measures how much of the variation in Airbnb listing prices is explained by the model. Since listing price depends on several factors such as room type, number of bedrooms, and guest capacity, R² helps show how well the model captures those relationships.

**Interpretation:** A higher R² means the model explains more of the variation in listing prices. A low R² suggests that important price-related factors may still be missing from the selected features.

## Alternative Models

### Alternative 1

**Construction:** The baseline model was a simple Linear Regression model using only one feature, `accommodates`. This was chosen as a reasonable low-complexity competitor because guest capacity should affect listing price, but the model intentionally uses less information than the full models.

**Evaluation:** The baseline model produced an RMSE of 12255.9216 and an R² of 0.0178. This shows that using only guest capacity provides very limited explanatory power for predicting Airbnb prices.

### Alternative 2

**Construction:** A full Linear Regression model was trained using `accommodates`, `bedrooms`, `number_of_reviews`, and one-hot encoded `room_type`. This model used all selected project features and served as the main regression model.

**Evaluation:** The Linear Regression model produced an RMSE of 11822.4798 and an R² of 0.0860. It performed better than the baseline, which suggests that the additional features improved price prediction.

### Alternative 3

**Construction:** A Ridge Regression model was trained using the same full feature set as the linear regression model. Ridge regularization was added to control coefficient size and reduce possible overfitting.

**Evaluation:** The Ridge Regression model produced an RMSE of 11824.3082 and an R² of 0.0858. Its performance was nearly the same as standard linear regression, indicating that regularization did not significantly improve results for this feature set.

### Alternative 4

**Construction:** A Lasso Regression model was trained using the same full feature set. Lasso was used as another regularized alternative that can reduce less useful feature influence.

**Evaluation:** The Lasso Regression model produced an RMSE of 11822.5902 and an R² of 0.0860. Its performance was also very similar to standard linear regression, showing that sparse regularization did not materially change the model behavior here.

### Alternative 5

**Construction:** A Random Forest Regressor was trained using the same selected features. Unlike the linear models, Random Forest can capture non-linear interactions and more complex relationships between price and the listing features.

**Evaluation:** The Random Forest Regressor produced an RMSE of 11353.5753 and an R² of 0.1571. This was the best performance among all evaluated models, suggesting that Airbnb price depends on relationships that are not purely linear.

## Best Model

**Model:** Random Forest Regressor

The Random Forest model was the best-performing model because it achieved the lowest RMSE and the highest R² among all tested models. This indicates that it predicted listing prices more accurately than the baseline, linear regression, Ridge regression, and Lasso regression. The result is reasonable because Airbnb pricing is likely influenced by non-linear interactions between factors such as room type, bedrooms, and guest capacity.
