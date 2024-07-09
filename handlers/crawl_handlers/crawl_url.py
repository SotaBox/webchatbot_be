from flask import jsonify, request
from services.crawl_services import CrawlService

def crawl_data_single_link_handler():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    response, status_code = CrawlService.crawl_data_single_link(url)
    return jsonify(response), status_code
