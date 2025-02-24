import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Base URL of the website
BASE_URL = "http://books.toscrape.com/catalogue/"

# Function to fetch book data from a single page
def scrape_books(url):
    books_data = []
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error for failed requests
        
        # Parse the page content
        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup.find_all('article', class_='product_pod')

        # Extract details of each book
        for book in books:
            title = book.find('h3').find('a')['title']
            price = book.find('p', class_='price_color').text
            link = urljoin(BASE_URL, book.find('h3').find('a')['href'])  # Convert relative link to absolute

            books_data.append({"Title": title, "Price": price, "Link": link})

        return books_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

# Function to scrape multiple pages
def scrape_multiple_pages(start_url, pages=3):
    all_books = []
    current_page = start_url
    
    for _ in range(pages):
        print(f"Scraping: {current_page}")
        books_on_page = scrape_books(current_page)
        all_books.extend(books_on_page)

        # Print books from the current page
        for book in books_on_page:
            print(f"Title: {book['Title']}")
            print(f"Price: {book['Price']}")
            print(f"Link: {book['Link']}")
            print("-" * 50)

        # Find next page link
        response = requests.get(current_page)
        soup = BeautifulSoup(response.text, 'html.parser')
        next_page = soup.find('li', class_='next')

        if next_page:
            next_page_url = urljoin(BASE_URL, next_page.find('a')['href'])
            current_page = next_page_url
        else:
            break  # No more pages

# Start scraping from the first page
start_url = "http://books.toscrape.com/catalogue/page-1.html"
scrape_multiple_pages(start_url, pages=5)  # Scrape 5 pages
