
%%write as app.py
import pandas as pd
import json
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

with open("grid_search_results.json", "r") as file:
    grid_results = json.load(file)

dataframes = []

# Loop through each model's results
for model_name, results in grid_results.items():
    
    cv_results = results["cv_results"]

    df = pd.DataFrame(cv_results)
    
    columns_to_drop = ["mean_fit_time", "std_fit_time", "mean_score_time", "std_score_time","params",
                       "split0_test_score",	"split1_test_score",	"split2_test_score",
                       "split3_test_score",	"split4_test_score"]
    df = df.drop(columns=columns_to_drop)

    df["model_name"] = model_name

    dataframes.append(df)

# Concatenate all dataframes into a single dataframe
combined_df = pd.concat(dataframes, ignore_index=True)

#SVM results
df = dataframes[0]
C=pd.DataFrame({
    'C': df.loc[df['param_svm__kernel']=='linear','param_svm__C'],
    'Linear accuracy': df.loc[df['param_svm__kernel']=='linear','mean_test_score'],
    'rbf accuracy': df.loc[df['param_svm__kernel']=='rbf','mean_test_score']
})

# Plotting the data
st.line_chart(C.set_index('C'))

#Naive-Bayes results
df= dataframes[1]


Alpha = pd.DataFrame({
    'Alpha': df.loc[df['param_nb__fit_prior'] == True, 'param_nb__alpha'].values,
    'fit prior accuracy': df.loc[df['param_nb__fit_prior'] == True, 'mean_test_score'].values,
    'no fit prior accuracy': df.loc[df['param_nb__fit_prior'] == False, 'mean_test_score'].values
})


# Plotting the data
st.line_chart(Alpha.set_index('Alpha'))

#K-neighbors results
df=dataframes[2]

# Filter data for 'uniform' and 'distance' weights
df_distance = df[df['weights'] == 'distance']
df_uniform = df[df['weights'] == 'uniform']

# Create scatter plot for 'weights=distance'
fig, ax1 = plt.subplots()
scatter1 = ax1.scatter(df_distance['n_neighbors'], df_distance['p'], c=df_distance['accuracy'], cmap='viridis', s=100)
ax1.set_xlabel('n_neighbors')
ax1.set_ylabel('p')
ax1.set_title('K-Nearest Neighbors with Weights: Distance')
fig.colorbar(scatter1, ax=ax1, label='Accuracy')

# Display the plot for 'weights=distance'
st.pyplot(fig)

# Create scatter plot for 'weights=uniform'
fig, ax2 = plt.subplots()
scatter2 = ax2.scatter(df_uniform['n_neighbors'], df_uniform['p'], c=df_uniform['accuracy'], cmap='viridis', s=100)
ax2.set_xlabel('n_neighbors')
ax2.set_ylabel('p')
ax2.set_title('K-Nearest Neighbors with Weights: Uniform')
fig.colorbar(scatter2, ax=ax2, label='Accuracy')

# Display the plot for 'weights=uniform'
st.pyplot(fig)

#Random forest results
df=dataframes[3]

# Create scatter plot
fig, ax = plt.subplots()
scatter = ax.scatter(df['param_rf__max_depth'], df['param_rf__n_estimators'], c=df['mean_test_score'], cmap='viridis', s=100)
ax.set_xlabel('Max Depth')
ax.set_ylabel('Number of Estimators')
ax.set_title('Random Forest: Max Depth vs. Number of Estimators')
fig.colorbar(scatter, ax=ax, label='Mean Test Score')

# Display the plot
st.pyplot(fig)

#Linear Regression results
df=dataframes[4]

# Filter data for liblinear and lbfgs solvers
df_liblinear = df[df['param_lr__solver'] == 'liblinear']
df_lbfgs = df[df['param_lr__solver'] == 'lbfgs']

# Create the plot
fig, ax = plt.subplots()
ax.plot(df_liblinear['param_lr__C'], df_liblinear['mean_test_score'], label='liblinear', marker='o')
ax.plot(df_lbfgs['param_lr__C'], df_lbfgs['mean_test_score'], label='lbfgs', marker='o')

ax.set_xlabel('C')
ax.set_ylabel('Mean Accuracy')
ax.set_title('Logistic Regression: C vs Mean Accuracy')
ax.legend()

# Display the plot
st.pyplot(fig)

'''
! pip install streamlit -q
!wget -q -O - ipv4.icanhazip.com
! streamlit run app.py & npx localtunnel --port 8501
'''