import requests
from bs4 import BeautifulSoup

URL = "https://tabelog.com/tokyo/A1308/A130802/13015251/dtlrvwlst/"  # example URL


def get_reviews(url):
    """
    Fetches reviews from the given URL.

    Args:
        url (str): The URL of the restaurant page.

    Returns:
        list: A list of reviews.
    """
    response = requests.get(url, timeout=5)
    response.raise_for_status()  # Raise an error for bad responses
    reviews = find_reviews(response.text)
    return reviews


def find_reviews(html_content):
    """
    Parses the HTML content to find reviews.

    Args:
        html_content (str): The HTML content of the page.

    Returns:
        list: A list of reviews found in the HTML.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    review_elements = soup.find_all("div", class_="rvw-item__rvw-comment")
    reviews = [element.get_text(strip=True) for element in review_elements]
    return reviews


if __name__ == "__main__":
    get_reviews(URL)
