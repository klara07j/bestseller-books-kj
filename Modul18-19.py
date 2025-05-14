import pandas as pd
import streamlit as st
import plotly.express as px

'''df = pd.DataFrame({
    'Name':['Lana','Goran','Timur'],
    'Age':[23,12,34],
    'City':['Mostar','Sarajevo','Konjic']
})
#print(df)
#df
st.write(df)
st.dataframe(df)'''

books_df = pd.read_csv('bestsellers_with_categories_2022_03_27.csv')
st.title("Bestselling Books Analysis")
st.write("This app analyzes the Amazon Top Selling books from 2009 to 2022")

#SIDEBAR: ADDING NEW DATA
st.sidebar.header("Add New Book Data")
with st.sidebar.form("book_form"):
    new_name = st.text_input("Enter New Book Name")
    new_author = st.text_input("Author")
    new_user_rating = st.slider("User's Rating", 0.0, 5.0, 0.0, 0.1)
    new_reviews = st.number_input("Reviews", min_value=0, step=1)
    new_price = st.number_input("Price", min_value=0, step=1)
    new_year = st.number_input("Year", min_value=2009, max_value=2022, step=1)
    new_genre = st.selectbox("Genre", books_df['Genre'].unique())
    btn = st.form_submit_button(label="Add Book")

if btn:
    new_data ={
        "Name": new_name,
        "Author":new_author,
        "User Rating":new_user_rating,
        "Reviews":new_reviews,
        "Price":new_price,
        "Year":new_year,
        "Genre":new_genre
    }
    #Add new data to the top of the DataFrame
    books_df = pd.concat([pd.DataFrame(new_data, index=[0]), books_df], ignore_index=True)
    books_df.to_csv("bestsellers_with_categories_2022_03_27.csv", index=False)
    st.sidebar.success("New Book Added successfully")

#SUMMARY STATISTICS
st.subheader("Summary Statistics")
total_books = books_df.shape[0]
unique_items = books_df['Name'].nunique()
average_price = books_df['Price'].mean()
average_rating = books_df['User Rating'].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total books", total_books)
col2.metric("Unique titles", unique_items)
col3.metric("Average Rating", average_rating)
col4.metric("Average Price", average_price)

#DATASET PREVIEW
st.subheader("Dataset Preview")
st.write(books_df.head())

#BOOK TITLE DISTRIBUTION AND AUTHOR DISTRIBUTION
col1, col2 = st.columns(2)
with col1:
    st.subheader("Top 10 Book Titles")
    top_titles = books_df['Name'].value_counts().head(10)
    st.bar_chart(top_titles)

with col2:
    st.subheader("Top 10 Authors")
    top_authors = books_df['Author'].value_counts().head(10)
    st.bar_chart(top_authors)

#GENRE DISTRIBUTION
st.subheader("Genre Distribution")
fig = px.pie(books_df, names='Genre', title="Most Liked Genre",
             color="Genre", color_discrete_sequence=px.colors.sequential.Plasma)
st.plotly_chart(fig)

#INTERACTIVITY: FILTER DATA BY GENRE
st.subheader("Filter Data by Genre")
genre_filter = st.selectbox("Select Genre",books_df['Genre'].unique())
filtered_df = books_df[books_df['Genre'] == genre_filter]
st.write(filtered_df)