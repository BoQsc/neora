import os
import urllib.request
from html.parser import HTMLParser

# Step 1: Create a simple HTMLParser to extract links
class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    self.links.append(attr[1])

# Step 2: Download the HTML content of the page
url = "https://archive.ubuntu.com/ubuntu/dists/noble/"

# Download the page content
with urllib.request.urlopen(url) as response:
    html_content = response.read().decode()

# Step 3: Parse the HTML content and extract all the links
parser = MyHTMLParser()
parser.feed(html_content)

# Step 4: Download the files or list directories
for idx, link in enumerate(parser.links):
    file_url = os.path.join(url, link)

    # Check if it's a file or directory
    if file_url.endswith('/'):
        print(f"Directory: {file_url}")
        # If you need to recursively list directories, you can repeat the process
    else:
        print(f"File: {file_url}")
        # Step 5: Download the file and search for the keyword "Linux"
        try:
            with urllib.request.urlopen(file_url) as file_response:
                file_content = file_response.read().decode(errors='ignore')
                if "Linux" in file_content:
                    # Save matched content to a separate file
                    file_name = f"matched_content_{idx + 1}.txt"
                    with open(file_name, 'w', encoding='utf-8') as f:
                        f.write(file_content)
                    print(f"Keyword 'Linux' found and saved in file: {file_name}")
        except Exception as e:
            print(f"Failed to process {file_url}: {e}")
