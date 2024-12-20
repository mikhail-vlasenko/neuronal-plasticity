import requests
from bs4 import BeautifulSoup
import html2text
import time
from urllib.parse import urljoin, urlparse, urldefrag
import re


class Brian2DocScraper:
    def __init__(self, base_url='https://brian2.readthedocs.io/en/stable/'):
        self.base_url = base_url
        self.visited_urls = set()
        self.converter = html2text.HTML2Text()
        self.converter.ignore_links = False
        self.converter.body_width = 0  # Don't wrap lines
        self.full_content = []  # Store all content here

    def get_page_content(self, url):
        """Fetch and parse a page."""
        try:
            # Remove fragment identifier before making request
            clean_url = urldefrag(url)[0]
            response = requests.get(clean_url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def is_valid_url(self, url):
        """Check if URL is within the Brian2 documentation."""
        if "brian2.readthedocs.io/en/stable/reference/" in url:
            # Skip reference pages
            return False
        parsed = urlparse(url)
        # Remove fragment identifier for URL comparison
        clean_url = urldefrag(url)[0]
        return (
                'brian2.readthedocs.io' in parsed.netloc and
                'stable' in parsed.path and
                not any(ext in clean_url for ext in ['.pdf', '.png', '.jpg', '.jpeg', '.gif', '.npy']) and
                clean_url not in self.visited_urls
        )

    def extract_links(self, soup, current_url):
        """Extract all valid documentation links from the page."""
        links = set()
        for a in soup.find_all('a', href=True):
            href = a['href']
            full_url = urljoin(current_url, href)

            # Only consider the URL without the fragment identifier
            clean_url = urldefrag(full_url)[0]

            if self.is_valid_url(full_url):
                links.add(clean_url)
        return links

    def clean_content(self, content):
        """Clean the HTML content before conversion to Markdown."""
        # Remove the navigation sidebar
        if content.find('div', {'class': 'wy-nav-side'}):
            content.find('div', {'class': 'wy-nav-side'}).decompose()

        # Remove the search and version boxes
        for div in content.find_all('div', {'role': 'search'}):
            div.decompose()

        # Remove script tags
        for script in content.find_all('script'):
            script.decompose()

        # Get the main content
        main_content = content.find('div', {'role': 'main'})
        if main_content:
            return main_content
        return content

    def convert_to_markdown(self, html_content, url):
        """Convert HTML content to Markdown format."""
        soup = BeautifulSoup(html_content, 'html.parser')
        cleaned_content = self.clean_content(soup)

        # Extract title
        title = soup.title.string if soup.title else "Untitled"
        title = title.replace(" — Brian 2 ", "").strip()

        # Convert to Markdown
        markdown_content = self.converter.handle(str(cleaned_content))

        # Add title and metadata
        markdown_content = f"# {title}\n\nSource: {urldefrag(url)[0]}\n\n{markdown_content}"

        return markdown_content, title

    def save_markdown(self, output_file='brian2_documentation.md'):
        """Save all content to a single Markdown file."""
        print(f"\nSaving documentation to {output_file}")

        # Add a table of contents
        toc = "# Table of Contents\n\n"
        for i, (title, _) in enumerate(self.full_content, 1):
            # Create a clean anchor link
            anchor = re.sub(r'[^\w\s-]', '', title).strip().lower()
            anchor = re.sub(r'[-\s]+', '-', anchor)
            toc += f"{i}. [{title}](#{anchor})\n"

        # Combine all content
        full_markdown = f"# Brian2 Documentation\n\n{toc}\n\n"
        full_markdown += "\n\n---\n\n".join(content for _, content in self.full_content)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_markdown)

        print(f"Documentation saved to {output_file}")
        print(f"Total pages processed: {len(self.visited_urls)}")

    def scrape(self):
        """Main scraping function."""
        urls_to_visit = {self.base_url}
        index_page_content = None

        while urls_to_visit:
            current_url = urls_to_visit.pop()

            # Remove fragment identifier for comparison
            clean_url = urldefrag(current_url)[0]
            if clean_url in self.visited_urls:
                continue

            print(f"Processing: {clean_url}")
            self.visited_urls.add(clean_url)

            # Get page content
            html_content = self.get_page_content(clean_url)
            if not html_content:
                continue

            # Parse the page
            soup = BeautifulSoup(html_content, 'html.parser')

            # Convert to Markdown
            markdown_content, title = self.convert_to_markdown(html_content, clean_url)

            # Store the content
            if clean_url == self.base_url:
                index_page_content = (title, markdown_content)
            else:
                self.full_content.append((title, markdown_content))

            # Find new links
            new_links = self.extract_links(soup, clean_url)
            urls_to_visit.update(new_links)

            # Be nice to the server
            time.sleep(1)

        # Sort content by title (except index page)
        self.full_content.sort(key=lambda x: x[0])

        # Put index page first if it exists
        if index_page_content:
            self.full_content.insert(0, index_page_content)

        # Save all content to a single file
        self.save_markdown()


if __name__ == "__main__":
    scraper = Brian2DocScraper()
    scraper.scrape()
