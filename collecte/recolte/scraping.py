import os
import pooch
import requests
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, base_url, data_folder):
        self.base_url = base_url
        self.data_folder = data_folder

    def collect_json_links(self):
        response = requests.get(self.base_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        json_links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.endswith('.json') and "archive" not in href:
                json_links.append(href)
        return json_links

    def download_and_fuse_json(self, json_links, fusion_file):
        with open(fusion_file, 'w') as outfile:
            outfile.write('[')
            first = True
            for json_link in json_links:
                filename = os.path.basename(json_link)
                file_path = pooch.retrieve(
                    url=json_link,
                    known_hash=None,
                    fname=filename,
                    path=self.data_folder
                )
                with open(file_path, 'r') as infile:
                    for line in infile:
                        if not first:
                            outfile.write(',\n')
                        outfile.write(line.strip())
                        first = False
                os.remove(file_path)
            outfile.write(']')
