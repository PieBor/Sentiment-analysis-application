import streamlit as st
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV

# Load the Iris dataset
iris = load_iris()
X = iris.data
y = iris.target

# Create a Streamlit dashboard
st.title('Decision Tree Grid Search Dashboard')

# Define parameter grid for GridSearchCV
param_grid = {
    'criterion': ['gini', 'entropy'],
    'max_depth': [None, 5, 10, 15, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# Create a Decision Tree Classifier
dt_classifier = DecisionTreeClassifier()

# Perform Grid Search with cross-validation
grid_search = GridSearchCV(estimator=dt_classifier, param_grid=param_grid, cv=5, scoring='accuracy')
grid_search.fit(X, y)

# Get the results and convert to DataFrame
cv_results = pd.DataFrame(grid_search.cv_results_)

# Display the results in the Streamlit app
st.subheader('Grid Search Results:')
st.write(cv_results[['params', 'mean_test_score', 'std_test_score', 'rank_test_score']])

# Plot the mean test scores
st.subheader('Mean Test Scores:')
st.line_chart(cv_results['mean_test_score'])

# Show the best parameters and score
best_params = grid_search.best_params_
best_score = grid_search.best_score_

st.subheader('Best Parameters:')
st.write(best_params)

st.subheader('Best Score:')
st.write(best_score)
