import requests
import pymysql
import pandas as pd
import sqlalchemy as sa
from sqlalchemy import create_engine
import streamlit as st

# Google Books API Configuration
API_KEY = 'Your API'
BASE_URL = 'https://www.googleapis.com/books/v1/volumes'

# SQL Connection Setup
sql_con = sa.engine.URL.create(
    drivername='mysql+pymysql',
    username="root",
    password="Add your password", 
    host="127.0.0.1",
    database="BookScape"
)

sql_engine = create_engine(sql_con)

# Streamlit App Configuration
st.set_page_config(page_title="BookScape", layout="wide")
st.markdown(
    """
    <style>
    body {
        background-color: black;
        color: white;
    }
    .stButton>button {
        background-color: #1a1a1a;
        color: white;
        border: 1px solid white;
    }
    .stButton>button:hover {
        background-color: #4CAF50;
        color: white;
    }
    .block-container {
        padding: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Add a header image
st.image("C:/Users/santh/Downloads/Colorful Photo Rainbow Facebook Cover.png", use_container_width=True)

# Fetch books from Google Books API
def fetch_books(search_key, max_results=1000):
    books = []
    start_index = 0
    while len(books) < max_results:
        params = {
            'q': search_key,
            'startIndex': start_index,
            'maxResults': 40,
            'key': API_KEY
        }
        response = requests.get(BASE_URL, params=params)
        if response.status_code != 200:
            st.error(f"Error fetching data: {response.status_code}")
            break
        data = response.json()
        books.extend(data.get('items', []))
        start_index += 40
        if 'items' not in data:
            break
    return books[:max_results]

# Parse book data
def parse_book_data(book, search_key):
    volume_info = book.get('volumeInfo', {})
    sale_info = book.get('saleInfo', {})
    list_price = sale_info.get('listPrice', {})
    retail_price = sale_info.get('retailPrice', {})
    return {
        'book_id': book.get('id'),
        'search_key': search_key,
        'book_title': volume_info.get('title'),
        'book_subtitle': volume_info.get('subtitle'),
        'book_authors': ', '.join(volume_info.get('authors', [])),
        'book_description': volume_info.get('description'),
        'industryIdentifiers': ', '.join([f"{id['type']}:{id['identifier']}" for id in volume_info.get('industryIdentifiers', [])]),
        'text_readingModes': volume_info.get('readingModes', {}).get('text', False),
        'image_readingModes': volume_info.get('readingModes', {}).get('image', False),
        'pageCount': volume_info.get('pageCount'),
        'categories': ', '.join(volume_info.get('categories', [])),
        'language': volume_info.get('language'),
        'imageLinks': volume_info.get('imageLinks', {}).get('thumbnail'),
        'ratingsCount': volume_info.get('ratingsCount'),
        'averageRating': volume_info.get('averageRating'),
        'country': sale_info.get('country'),
        'saleability': sale_info.get('saleability'),
        'isEbook': sale_info.get('isEbook', False),
        'amount_listPrice': list_price.get('amount'),
        'currencyCode_listPrice': list_price.get('currencyCode'),
        'amount_retailPrice': retail_price.get('amount'),
        'currencyCode_retailPrice': retail_price.get('currencyCode'),
        'buyLink': sale_info.get('buyLink'),
        'year': volume_info.get('publishedDate', '').split('-')[0],
        'publisher': volume_info.get('publisher')
    }

# Store books in MySQL database (Avoid duplicates)
def store_books_in_db(parsed_books):
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='Add your password',  
        database='BookScape'
    )
    cursor = connection.cursor()

    # Query to insert the books while avoiding duplicates based on book_id
    query = """
    INSERT INTO books (book_id, search_key, book_title, book_subtitle, book_authors, book_description,
                       industryIdentifiers, text_readingModes, image_readingModes, pageCount, categories,
                       language, imageLinks, ratingsCount, averageRating, country, saleability, isEbook,
                       amount_listPrice, currencyCode_listPrice, amount_retailPrice, currencyCode_retailPrice,
                       buyLink, year, publisher)
    VALUES (%(book_id)s, %(search_key)s, %(book_title)s, %(book_subtitle)s, %(book_authors)s, %(book_description)s,
            %(industryIdentifiers)s, %(text_readingModes)s, %(image_readingModes)s, %(pageCount)s, %(categories)s,
            %(language)s, %(imageLinks)s, %(ratingsCount)s, %(averageRating)s, %(country)s, %(saleability)s, %(isEbook)s,
            %(amount_listPrice)s, %(currencyCode_listPrice)s, %(amount_retailPrice)s, %(currencyCode_retailPrice)s,
            %(buyLink)s, %(year)s, %(publisher)s)
    ON DUPLICATE KEY UPDATE
        book_title=VALUES(book_title), book_subtitle=VALUES(book_subtitle),
        book_authors=VALUES(book_authors), book_description=VALUES(book_description),
        industryIdentifiers=VALUES(industryIdentifiers), text_readingModes=VALUES(text_readingModes),
        image_readingModes=VALUES(image_readingModes), pageCount=VALUES(pageCount),
        categories=VALUES(categories), language=VALUES(language), imageLinks=VALUES(imageLinks),
        ratingsCount=VALUES(ratingsCount), averageRating=VALUES(averageRating),
        country=VALUES(country), saleability=VALUES(saleability), isEbook=VALUES(isEbook),
        amount_listPrice=VALUES(amount_listPrice), currencyCode_listPrice=VALUES(currencyCode_listPrice),
        amount_retailPrice=VALUES(amount_retailPrice), currencyCode_retailPrice=VALUES(currencyCode_retailPrice),
        buyLink=VALUES(buyLink), year=VALUES(year), publisher=VALUES(publisher);
    """
    cursor.executemany(query, parsed_books)
    connection.commit()
    connection.close()

# Retrieve books from the database based on query
def retrieve_books_from_db(query):
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='Add your password',  
        database='BookScape'
    )
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    results = cursor.fetchall()
    connection.close()
    return pd.DataFrame(results)

# Define SQL queries for predefined analysis
def run_sql_queries():
    query_options = {
        "Check Availability of eBooks vs Physical Books": '''
            SELECT isEbook,
                COUNT(*) AS book_count 
            FROM books 
            GROUP BY isEbook;
        ''',

        "Find the Publisher with the Most Books Published": '''
            SELECT publisher, 
                Count(*) as book_count
            FROM books
            Group by publisher
            Order By book_count DESC
            Limit 5 offset 1;
        ''',

        "Identify the Publisher with the Highest Average Rating": '''
            SELECT publisher, AVG(averageRating) AS avg_rating
            FROM books
            GROUP BY publisher
            ORDER BY avg_rating DESC
            LIMIT 1 offset 1;
        ''',

        "Get the Top 5 Most Expensive Books by Retail Price": '''
            SELECT book_title, amount_retailPrice, currencyCode_retailPrice
            FROM books
            Order By amount_retailPrice DESC
            Limit 5;
        ''',
        "Find Books Published After 2010 with at Least 500 Pages": '''
        SELECT book_title, year, pageCount
        FROM books where year >= 2010 and pageCount >=500
        order by year;
    ''',

    "List Books with Discounts Greater than 20%": '''
        SELECT book_title, amount_listPrice, amount_retailPrice, 
            (amount_listPrice - amount_retailPrice) / amount_listPrice * 100 AS discount_percentage
        FROM books
        WHERE amount_listPrice > 0 
        AND (amount_listPrice - amount_retailPrice) / amount_listPrice * 100 > 20;
    ''',

    "Find the Average Page Count for eBooks vs Physical Books": '''
        SELECT isEbook, AVG(pageCount) AS avg_page_count
        FROM books
        GROUP BY isEbook;
    ''',

    "Find the Top 3 Authors with the Most Books": '''
        SELECT book_authors, COUNT(*) AS book_count
        FROM books
        GROUP BY book_authors
        ORDER BY book_count DESC
        LIMIT 3 offset 1;
    ''',

    "List Publishers with More than 10 Books": '''
        SELECT publisher, COUNT(*) AS book_count
        FROM books
        GROUP BY publisher
        HAVING book_count > 10;
    ''',

    "Find the Average Page Count for Each Category": '''
        SELECT categories, AVG(pageCount) AS avg_page_count
        FROM books
        GROUP BY categories;
    ''',

    "Retrieve Books with More than 3 Authors": '''
        SELECT book_title, book_authors
        FROM books
        WHERE LENGTH(book_authors) - LENGTH(REPLACE(book_authors, ',', '')) + 1 > 3;
    ''',

    "Books with Ratings Count Greater Than the Average": '''
        SELECT book_title, ratingsCount
        FROM books
        WHERE ratingsCount > (SELECT AVG(ratingsCount) FROM books);
    ''',

    "Books with the Same Author Published in the Same Year": '''
        SELECT book_authors, year, COUNT(*) AS book_count
        FROM books
        GROUP BY book_authors, year
        HAVING book_count > 1;
    ''',

    "Books with a Specific Keyword in the Title": '''
        SELECT book_title
        FROM books
        WHERE book_title LIKE '%%Python%%';
    ''',

    "Year with the Highest Average Book Price": '''
        SELECT year, AVG(amount_retailPrice) AS avg_price
        FROM books
        GROUP BY year
        ORDER BY avg_price DESC
        LIMIT 1;
    ''',

    "Count Authors Who Published 3 Consecutive Years": '''
        SELECT book_authors, COUNT(DISTINCT year) AS consecutive_years
        FROM books
        GROUP BY book_authors
        HAVING MAX(year) - MIN(year) >= 2;
    ''',

    "Authors Who Published in the Same Year Under Different Publishers": '''
        SELECT book_authors, year, COUNT(DISTINCT publisher) AS publisher_count
        FROM books
        GROUP BY book_authors, year
        HAVING publisher_count > 1;
    ''',

    "Average Retail Price of eBooks vs Physical Books": '''
        SELECT 
            AVG(CASE WHEN isEbook = 1 THEN amount_retailPrice END) AS avg_ebook_price,
            AVG(CASE WHEN isEbook = 0 THEN amount_retailPrice END) AS avg_physical_price
        FROM books;
    ''',

    "Identify Books with title, averageRating, and ratingsCount for these outliers": '''
        SELECT book_title, averageRating, ratingsCount
        FROM books
        WHERE averageRating > (
                SELECT AVG(averageRating) + 2 * STDDEV(averageRating)
                FROM books
            )
        OR averageRating < (
                SELECT AVG(averageRating) - 2 * STDDEV(averageRating)
                FROM books
            );
    ''',

    "Publisher with the Highest Average Rating": '''
        SELECT publisher, AVG(averageRating) AS avg_rating, COUNT(*) AS book_count
        FROM books
        GROUP BY publisher
        HAVING book_count > 10
        ORDER BY avg_rating DESC
        LIMIT 1;
    '''
    }
    return query_options

# Streamlit Sidebar
st.sidebar.title("Navigation")
nav_option = st.sidebar.radio("Navigate", ["Search Books", "Query Results"])

if nav_option == "Search Books":
    st.title("Search Books")
    search_key = st.text_input("Enter search term")

    if st.button("Search"):
        if search_key:
            books = fetch_books(search_key)
            parsed_books = [parse_book_data(book, search_key) for book in books]
            st.session_state.parsed_books = parsed_books
            books_df = pd.DataFrame(parsed_books)
            st.write(books_df)
        else:
            st.error("Please enter a search term.")

    if st.button("Store in Database"):
        if 'parsed_books' in st.session_state:
            store_books_in_db(st.session_state.parsed_books)
            st.success("Books stored in database.")
        else:
            st.error("No books to store. Search first.")

elif nav_option == "Query Results":
    st.title("Query Results")
    query_options = run_sql_queries()
    query = st.selectbox("Choose a query", list(query_options.keys()))
    if st.button("Run Query"):
        query_results = retrieve_books_from_db(query_options[query])
        st.dataframe(query_results)
