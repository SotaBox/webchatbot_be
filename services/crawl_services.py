import requests
from bs4 import BeautifulSoup
from repo.parent_link import insert_parent_link , get_id_by_parent_link , get_data_parent_link, check_parent_link_exists
from repo.link import check_link_exists, insert_link, insert_data_link, get_list_link_by_parent_id, get_data_link, get_link_by_id
import logging
import re

class CrawlService:
    @staticmethod
    def crawl_sitemap(parent_link):
        try:
            if check_parent_link_exists(parent_link):
                logging.info(f"Parent link '{parent_link}' already exists. Skipping database insertion.")
                parent_id = get_id_by_parent_link(parent_link)
            else:
                parent_id = insert_parent_link(parent_link)
                logging.info(f"Inserted parent link '{parent_link}' into the database with ID: {parent_id}")

            response = requests.get(parent_link)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Extract unique links
                links_set = {a['href'] for a in soup.find_all('a', href=True)}

                # Optional: Filter links using regex 
                regex = re.compile(r"((https?):((//)|(\\\\))+[\w\d:#@%/;$()~_?\+-=\\\.&]*)", re.MULTILINE|re.UNICODE)
                filtered_links = [link for link in links_set if regex.match(link)]
                
                # Check and insert links
                for link in filtered_links:
                    if not check_link_exists(link):
                        insert_link(link, parent_id)

                return {   
                    'links': filtered_links
                }, 200
            else:
                return {'error': f"Failed to retrieve the URL: {parent_link}"}, 400
        except Exception as e:
            logging.error("Error crawling sitemap: %s", str(e))
            return {'error': f"An error occurred: {str(e)}"}, 500
        
    @staticmethod
    def crawl_data_link(link_id):
        try:
            link = get_link_by_id(link_id)
            if link:
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

                    insert_data_link(link, title, description, content, vector_status)
                    
                    return {
                        "title": title,
                        "description": description,
                        "content": content,
                        "vector_status": vector_status
                    }, 200
                else:
                    return {'error': f"Failed to retrieve the URL: {link}"}, 400
            else:
                return {'error': f"Link not found for ID: {id}"}, 404
        except Exception as e:
            logging.error("Error crawling data link: %s", str(e))
            return {'error': f"An error occurred: {str(e)}"}, 500
    
    @staticmethod 
    def get_list_link(parent_link):
        try:
            parent_id = get_id_by_parent_link(parent_link)
            if parent_id:
                data = get_list_link_by_parent_id(parent_id)
                if data:
                    return data,200
                else:
                    return {'error': 'Data not found for the given parent link'}, 404
            else:
                return {'error': 'Parent link not found'}, 404
        except Exception as e:
            logging.error("Error getting list of links: %s", str(e))
            return {'error': 'An error occurred while getting the list of links', 'details': str(e)}, 500
        
    @staticmethod
    def get_data_from_link(link_id):
        try:
            data = get_data_link(link_id)
            if data:
                return data, 200
            else:
                return {'error': 'Data not found for the given link ID'}, 404
        except Exception as e:
            logging.error("Error getting data from link: %s", str(e))
            return {'error': 'An error occurred while getting data from link', 'details': str(e)}, 500
        
    @staticmethod
    def search_data_from_parent_link(parent_link):
        try:
            data = get_data_parent_link(parent_link)
            if data:
                return data, 200
            else:
                return {'error': 'Data not found for the given URL'}, 404
        except Exception as e:
            logging.error("Error searching data from URL: %s", str(e))
            return {'error': 'An error occurred while searching data from URL', 'details': str(e)}, 500