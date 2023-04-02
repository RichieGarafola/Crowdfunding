import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read in the dataset
df = pd.read_csv("./Resources/CrowdfundingData.csv")

# Wrangle the data
df['launched_at'] = pd.to_datetime(df['launched_at'], unit='s')
df['deadline'] = pd.to_datetime(df['deadline'], unit='s')
df['duration'] = (df['deadline'] - df['launched_at']).dt.days
df['success'] = df['outcome'] == 'successful'
df['main_category'] = df['category'].apply(lambda x: x.split('/')[0])

st.title("Crowdfunding Analysis")

# Create a sidebar with options for the user to select the analysis they want to view.
analysis = st.sidebar.selectbox(
    "Select an analysis:",
    ("Success Rate by Category", "Distribution of Funding Goals by Category", "Distribution of Pledged Amounts by Category", 
     "Backers Count vs. Pledged Amount", "Amount Pledged vs. Backers Count", "Amount Pledged by Outcome", 
     "Distribution of Campaign Durations", "Campaign Goal vs. Amount Pledged", "Average Funding Goals by Category", "Top 10 Most Successful Projects",  "Top 10 Most Backed Projects", "Success Rate by Month", "Number of Projects Launched by Month", "Top 10 Most Popular Categories")
)

st.set_option('deprecation.showPyplotGlobalUse', False)

# Display the appropriate chart based on the user's selection.
if analysis == "Success Rate by Category":
    plt.figure(figsize=(12, 6))
    sns.countplot(x='category', hue='success', data=df)
    plt.xticks(rotation=90)
    plt.title('Success Rate by Category')
    plt.xlabel('Category')
    plt.ylabel('Count')
    plt.legend(title='Success', loc='upper right')
    st.pyplot()

elif analysis == "Distribution of Funding Goals by Category":
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='category', y='goal', data=df)
    plt.xticks(rotation=90)
    plt.title('Distribution of Funding Goals by Category')
    plt.xlabel('Category')
    plt.ylabel('Funding Goal')
    st.pyplot()

elif analysis == "Distribution of Pledged Amounts by Category":
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='category', y='pledged', data=df)
    plt.xticks(rotation=90)
    plt.title('Distribution of Pledged Amounts by Category')
    plt.xlabel('Category')
    plt.ylabel('Pledged Amount')
    st.pyplot()

elif analysis == "Backers Count vs. Pledged Amount":
    plt.figure(figsize=(10, 8))
    sns.scatterplot(x='backers_count', y='pledged', hue='success', data=df, alpha=0.5)
    plt.xscale('log')
    plt.yscale('log')
    plt.title('Backers Count vs. Pledged Amount')
    plt.xlabel('Number of Backers')
    plt.ylabel('Pledged Amount')
    st.pyplot()

elif analysis == "Amount Pledged vs. Backers Count":
    plt.figure(figsize=(10, 8))
    sns.scatterplot(x='backers_count', y='pledged', hue='main_category', data=df, alpha=0.5)
    plt.xscale('log')
    plt.yscale('log')
    plt.title('Amount Pledged vs. Backers Count')
    plt.xlabel('Number of Backers')
    plt.ylabel('Pledged Amount')
    st.pyplot()

elif analysis == "Amount Pledged by Outcome":
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='outcome', y='pledged', data=df)
    plt.title('Amount Pledged by Outcome')
    plt.xlabel('Outcome')
    plt.ylabel('Pledged Amount')
    st.pyplot()

elif analysis == "Distribution of Campaign Durations":
    plt.figure(figsize=(10, 6))
    sns.histplot(df['duration'], kde=False)
    plt.title('Distribution of Campaign Durations')
    plt.xlabel('Duration (Days)')
    plt.ylabel('Count')
    st.pyplot()

elif analysis == "Campaign Goal vs. Amount Pledged":
    plt.figure(figsize=(10, 8))
    sns.scatterplot(x='goal', y='pledged', hue='success', data=df, alpha=0.5)
    plt.xscale('log')
    plt.yscale('log')
    plt.title('Campaign Goal vs. Amount Pledged')
    plt.xlabel('Campaign Goal')
    plt.ylabel('Pledged Amount')
    st.pyplot()

elif analysis == "Average Funding Goals by Category":
    category_mean = df.groupby('main_category')['goal'].mean().sort_values(ascending=False)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=category_mean.index, y=category_mean.values)
    plt.xticks(rotation=90)
    plt.title('Average Funding Goals by Category')
    plt.xlabel('Category')
    plt.ylabel('Average Funding Goal')
    st.pyplot()

elif analysis == "Top 10 Most Successful Projects":
    top_10_success = df[df['success']].sort_values('pledged', ascending=False).head(10)
    plt.figure(figsize=(12, 6))
    sns.barplot(x='name', y='pledged', data=top_10_success)
    plt.xticks(rotation=45, ha='right')
    plt.title('Top 10 Most Successful Projects')
    plt.xlabel('Project Title')
    plt.ylabel('Pledged Amount')
    st.pyplot()

elif analysis == "Top 10 Most Backed Projects":
    top_10_backed = df.sort_values('backers_count', ascending=False).head(10)
    plt.figure(figsize=(12, 6))
    sns.barplot(x='name', y='backers_count', data=top_10_backed)
    plt.xticks(rotation=45, ha='right')
    plt.title('Top 10 Most Backed Projects')
    plt.xlabel('Project Title')
    plt.ylabel('Number of Backers')
    st.pyplot()

elif analysis == "Success Rate by Month":
    df['launched_month'] = df['launched_at'].dt.month
    month_success_rate = df.groupby('launched_month')['success'].mean()
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=month_success_rate.index, y=month_success_rate.values)
    plt.title('Success Rate by Month')
    plt.xlabel('Month')
    plt.ylabel('Success Rate')
    st.pyplot()

elif analysis == "Number of Projects Launched by Month":
    df['launched_month'] = df['launched_at'].dt.month
    month_project_count = df.groupby('launched_month')['id'].count()
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=month_project_count.index, y=month_project_count.values)
    plt.title('Number of Projects Launched by Month')
    plt.xlabel('Month')
    plt.ylabel('Number of Projects')
    st.pyplot()

elif analysis == "Top 10 Most Popular Categories":
    top_10_categories = df['main_category'].value_counts().head(10)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_10_categories.index, y=top_10_categories.values)
    plt.xticks(rotation=90)
    plt.title('Top 10 Most Popular Categories')
    plt.xlabel('Category')
    plt.ylabel('Number of Projects')
    st.pyplot()



