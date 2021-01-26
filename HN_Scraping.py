from bs4 import BeautifulSoup
import requests
import pprint

hn = []


class Scrape:
    def __init__(self):
        self.total_links = []
        self.total_sub = []

    def import_links(self, page_num):
        for i in range(1, page_num + 1):
            res = requests.get(f'https://news.ycombinator.com/news?p={i}')  # Get the response from the page
            soup = BeautifulSoup(res.text, 'html.parser')  # Convert the response to text

            # Separate the link and subtext class

            links = soup.select('.storylink')
            subtexts = soup.select('.subtext')
            self.total_links += links
            self.total_sub += subtexts
        return self.custom_hn(self.total_links, self.total_sub)

    def sorted_hn(self, hn_list):
        # Sort the list by votes

        return sorted(hn_list, key=lambda k: k['Score'], reverse=True)

    def custom_hn(self, link, subtext):
        hn.clear()

        for idx, item in enumerate(link):
            title = item.get_text()
            url = item.get('href', None)
            vote = subtext[idx].select('.score')

            if len(vote):
                score = int(vote[0].getText().replace(' points', ''))

                if score > 99:
                    hn.append({'Title': title, 'Link': url, 'Score': score})

        return pprint.pprint(self.sorted_hn(hn))


output = Scrape()
output.import_links()
