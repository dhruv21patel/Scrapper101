# Scrapper101
    Scrapper 101 is a simple Python-based web scraper designed to extract product information (such as name, full price, and sale price) from an e-commerce website. This scraper uses httpx for making HTTP requests and selectolax for parsing HTML content. It showcases how to automate the scraping of product data, which can then be used for price comparison, analysis, or other tasks.

## Features:
    - Scrapes product names, full prices, and sale prices from an e-commerce website.
    - Implements error handling for page availability and request timeouts.
    - Follows pagination and scrapes multiple pages of product data.
    - Uses lightweight libraries (httpx for requests, selectolax for HTML parsing) for performance.
    - Outputs scraped data to the console (can be easily modified to save to CSV or JSON).

## Technologies Used:
    + Python
    + httpx (for HTTP requests)
    + selectolax (for HTML parsing)
    + time (for controlling request intervals)

## How It Works:
    1. The scraper sends GET requests to the e-commerce site's product listing pages.
    2. It parses the HTML to extract product details (name, full price, sale price) using CSS selectors.
    3. The scraper handles multiple pages by adjusting pagination URLs.
    4. Extracted product data is printed to the console in a structured format.
    ### How to Use:
        # Clone the repository to your local machine:
            - bash
            - Copy code
            - git clone https://github.com/yourusername/scrapper101.git

        # Install the required dependencies using pip:
            - pip install httpx selectolax

        # Run the script:
            - python scrapper101.py

        # Code Breakdown:
            - getHtml(baseurl, page)
            - Sends an HTTP GET request to the e-commerce site with headers to mimic a real browser.
            - Handles redirects and raises errors for non-200 responses.
            - Returns the parsed HTML content.
            - getproduct(product, identifier) and getsaleprice(product, identifier)
            - Extracts text or attributes from HTML elements based on the provided CSS identifier.
            - Gracefully handles missing elements.
            - parser(html)
            - Parses the HTML to find the list of products and retrieves their name, full price, and sale price.
            - Handles potential read timeouts.
            - main()
            - Defines the base URL and loops through multiple pages of the product list.
            - Calls the parser to extract product details for each page.

        # Example Output:
            {'name': 'Product 1', 'fullprice': '$50', 'saleprice': '$30'}
            {'name': 'Product 2', 'fullprice': '$60', 'saleprice': '$40'}
            ...

    ## Customization:
        Modify the url variable in the main() function to scrape other e-commerce websites.
        Update the CSS selectors in the getproduct() and getsaleprice() functions to match the structure of the target site.
