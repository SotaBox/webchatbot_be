import requests
from bs4 import BeautifulSoup
from repo.url_stiemap import insert_data_to_db , insert_link_to_db , check_link_exists, get_list_link_from_db , get_data_link , get_data_url
import logging

class CrawlService:
    @staticmethod
    def crawl_sitemap(url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Extract unique links
                links_set = {a['href'] for a in soup.find_all('a', href=True)}
                links = list(links_set)
                
                # Check and insert links
                for link in links:
                    if not check_link_exists(link):
                        insert_link_to_db(link, url)

                return {   
                    'links': links
                }, 200
            else:
                return {'error': f"Failed to retrieve the URL: {url}"}, 400
        except Exception as e:
            logging.error("Error crawling sitemap: %s", str(e))
            return {'error': f"An error occurred: {str(e)}"}, 500
        
    @staticmethod
    def crawl_data_link(link):
        try:
            response = requests.get(link)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Extract the title
                title = soup.title.string if soup.title else 'No title'

                # Extract the description from meta tags
                description_tag = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
                description = description_tag['content'] if description_tag else 'No description'

                # Extract the content
                content = soup.get_text(separator=' ', strip=True)

                vector_status = "null"

                insert_data_to_db(link, title , description , content , vector_status)
                
                return {
                    "title": title,
                    "description": description,
                    "content": content,
                    "vector_status": vector_status
                }, 200
            else:
                return {'error': f"Failed to retrieve the URL: {link}"}, 400
        except Exception as e:
            logging.error("Error crawling sitemap: %s", str(e))
            return {'error': f"An error occurred: {str(e)}"}, 500
    
    @staticmethod 
    def get_list_link(url):
        try:
            data= get_list_link_from_db(url)
            if data:
                return data, 200
            else:
                return {'error': 'Data not found for the given URL'}, 404
        except Exception as e:
            logging.error("Error getting URL data: %s", str(e))
            return {'error': 'An error occurred while getting URL data', 'details': str(e)}, 500
        
    @staticmethod
    def get_data_from_link(link):
        try:
            data = get_data_link(link)
            if data:
                return data, 200
            else:
                return {'error': 'Data not found for the given URL'} , 404
        except Exception as e:
            logging.error("Error getting URL data: %s", str(e))
            return {'error': 'An error occurred while getting URL data', 'details': str(e)}, 500
        
    @staticmethod
    def search_data_from_url(url):
        try:
            data = get_data_url(url)
            if data:
                return data, 200
            else:
                return {'error': 'Data not found for the given URL'} , 404
        except Exception as e:
            logging.error("Error getting URL data: %s", str(e))
            return {'error': 'An error occurred while getting URL data', 'details': str(e)}, 500