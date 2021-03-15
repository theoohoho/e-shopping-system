"""
The Crawler to scraping data from movie source
"""

import requests
import uuid
from bs4 import BeautifulSoup, element as bs4_element

from crud.crud_product import product
from schemas import Product as ProductSchema
from database import get_db_session


class Crawler:
    _instance = None
    source_url = 'https://www.themoviedb.org'

    def __init__(self):
        """Init crawler class and create crawler instance
        """
        if Crawler._instance is not None:
            raise Exception('Crawler instance already created')

        self.id = id(self)
        Crawler._instance = self
        print(f'Create crawler instance, the id of instance: {self.id}')

    @staticmethod
    def get_crawler_instance():
        """Get crawler instance.
        """
        if Crawler._instance is None:
            return Crawler()
        return Crawler._instance

    def fetch_resource(self, source_url: str):
        """ Fetch resource"""
        print(f'Fetch resource: {source_url} ....')
        res = requests.get(source_url)
        return res.text

    def to_html_soup(self, source_str: str):
        """Parse to beautiful soup with html
        """
        return BeautifulSoup(source_str, "html.parser")

    def extract_movie_information(self, soup):
        """Access movie information resource, and extract target source.
        """
        print('Start to extract movie information resource...')
        card_elements = soup.find_all(class_='card style_1')
        movie_list = []
        for card_elem in card_elements:
            movie_list.append({
                "source_url": Crawler.source_url + card_elem.find('a', class_='image').get('href'),
                "product_name": card_elem.find('a', class_='image').get('title'),
                "image_url": Crawler.source_url + card_elem.find('img', class_='poster').get('src'),
                "movie_score": card_elem.find(class_='user_score_chart').get('data-percent'),
                "publish_date": card_elem.find('p').text,
            })
        print('End to extracting....')
        return movie_list

    def extract_movie_detail(self, movie_information):
        """Access movie detail resource, and extract target source.
        """
        print('Start to extract movie detail resource...')
        for movie in movie_information:
            resp = self.fetch_resource(movie.get('source_url'))
            soup = self.to_html_soup(resp)
            movie.update({
                "description": soup.find(class_='overview').find('p').text,
                "product_type": soup.find(class_='genres').find('a').text,
                "release_date": soup.find(class_='release').text.strip() if soup.find('release') else None,
                "movie_runtime": soup.find(class_='runtime').text.strip()
            })
        print('End to extracting....')
        return movie_information

    def store_data(self, movie_data):
        """Store data into database."""
        with get_db_session() as db_session:
            product_data = [ProductSchema(
                product_id=str(uuid.uuid4())[:10],
                store_pcs=len(data.get('product_name')),
                price=int(float(data.get('movie_score')))*10 if data.get('movie_score') else 0,
                **data
            ) for data in movie_data]
            product.add_all(db_session, product_data)
            db_session.commit()

    def run(self):
        """Execute crawler to scraping."""
        print('Start to run crawler to scrap target source...')
        resource_raw = self.fetch_resource(Crawler.source_url + '/movie?language=zh-TW')
        soup = self.to_html_soup(resource_raw)
        movie_information = self.extract_movie_information(soup)
        completed_movie_information = self.extract_movie_detail(movie_information)
        self.store_data(completed_movie_information)


if __name__ == '__main__':
    crawler = Crawler()
    crawler.run()
