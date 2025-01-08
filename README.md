# BookScape Explorer

## Overview
**BookScape Explorer** is a comprehensive tool designed to help users explore and analyze book data. By integrating the Google Books API with SQL and Streamlit, the project enables users to search for books, extract insights, and make informed reading decisions. It is targeted at avid readers, researchers, and book enthusiasts.

---

## Skills Takeaway from This Project
- **Python Scripting**: API integration and data handling.
- **Data Collection**: Extracting and managing data via APIs.
- **Streamlit**: Creating interactive web applications.
- **SQL**: Database schema design and complex queries for data analysis.

---

## Problem Statement
The **BookScape Explorer** aims to:
- Facilitate book discovery and analysis through an intuitive web application.
- Provide insights into book trends, user preferences, and reviews.
- Offer actionable insights for libraries and bookstores.

---

## Business Use Cases
1. **Search Optimization**: Filter books based on genre, author, or publication year.
2. **Trend Analysis**: Identify trending genres or authors.
3. **Data Insights**: Analyze user reviews and ratings for popular books.
4. **Decision Support**: Help libraries and bookstores stock trending books.

---

## Approach
### 1. Data Extraction
- Use the **Google Books API** to fetch:
  - Titles, authors, publication dates, genres, descriptions, and more.
- Implement pagination to retrieve up to 1000 book entries.

### 2. Data Storage
- Design a SQL database with a well-structured schema:
  - **book_id**: Unique identifier.
  - **search_key**: Search term used for API.
  - Other attributes: Title, authors, descriptions, ratings, price, etc.

### 3. Data Analysis
- Answer questions using SQL queries:
  - Availability of eBooks vs. physical books.
  - Publishers with the highest ratings.
  - Most expensive books, average page count, and more.

### 4. Streamlit Application
- Develop a user-friendly interface with:
  - Search functionality.
  - Real-time SQL query execution.
  - Results displayed as tables, charts, and dashboards.

### 5. Deployment
- Host the SQL database and Streamlit app on a suitable platform for accessibility.

---

## Expected Results
1. A fully functional Streamlit application for book exploration.
2. A structured SQL database populated with book data.
3. A set of SQL queries providing actionable insights.

---

## Project Deliverables
- **SQL Database**: Fully populated with book data.
- **API Scripts**: For data extraction and transformation.
- **Streamlit Application**: User-friendly exploration tool.

---

## Project Evaluation Metrics
- **Data Extraction Accuracy**: Successful and complete data retrieval.
- **SQL Design**: Well-structured and normalized tables.
- **Query Efficiency**: Optimized SQL queries.
- **Streamlit Functionality**: Smooth, interactive user experience.

---

## Technical Tags
- **Languages**: Python
- **Database**: SQL (MySQL/PostgreSQL)
- **Visualization Tool**: Streamlit
- **API Integration**: Google Books API
- **Libraries**: Pandas, MySQL

---

## Getting Started
### Prerequisites
1. Python 3.7+
2. MySQL or PostgreSQL
3. API Key for Google Books API
4. Required Libraries:
   ```bash
   pip install pandas streamlit pymysql requests
   ```

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/bookscape-explorer.git
   ```
2. Set up the SQL database and populate it using the provided scripts.
3. Configure the Streamlit app with your database credentials.
4. Run the application:
   ```bash
   streamlit run app.py
   ```

---

## References
1. [Google Books API Documentation](https://developers.google.com/books)
2. [Streamlit Documentation](https://docs.streamlit.io)

---
Output:

![image](https://github.com/user-attachments/assets/ae190727-3347-46ed-8b93-59c88a3e6740)





