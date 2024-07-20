import os
import json
from bs4 import BeautifulSoup

def extract_content(html, url):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.string if soup.title else ''
    headings = ' '.join([h.get_text() for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])])
    homepath = ' '.join([div.get_text() for div in soup.find_all('div', class_="header-parent-page-link")])
    lineage = homepath.replace('Home |', "")
    hometown = ' '.join([div.get_text() for div in soup.find_all('div', class_="home-town")])
    parent1 = ' '.join([div.get_text() for div in soup.find_all('div', class_="parent1")])
    parent2 = ' '.join([div.get_text() for div in soup.find_all('div', class_="parent2")])
    #wife = ' '.join([div.get_text() for div in soup.find_all('div', class_="wife")])
    children = ', '.join([div.get_text() for div in soup.find_all('div', class_="child")])
    names = ' '.join([img.get('data-name') for img in soup.find_all('img') if img.get('data-name')])
    return {
        'url': '.\\' + url,
        'title': title,
        'lineage': lineage,
        'headings': headings,
        'hometown': hometown,
        'parents': parent1 + ', ' +
                   parent2,
        'children': children,
        'names': names
    }

def index_html_files(directory):
    index = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    html = f.read()
                    url = os.path.relpath(file_path, directory)
                    content = extract_content(html, url)
                    index.append(content)
    return index

if __name__ == '__main__':
    directory = './'  # Update this path
    index = index_html_files(directory)
    with open('index.json', 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
