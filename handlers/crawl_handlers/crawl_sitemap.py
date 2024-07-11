from flask import jsonify, request
from services.crawl_services import CrawlService
from services.chat_sevices import ChatService

def crawl_sitemap_handler():
    data = request.get_json()
    parent_link = data.get('parent_link')
    if not parent_link:
        return jsonify({'error': 'Parent link is required'}), 400
    
    access_token_error = ChatService.check_valid_access_token()
    if access_token_error:
        return jsonify(access_token_error[0]), access_token_error[1]
    
    response, status_code = CrawlService.crawl_sitemap(parent_link)
    return jsonify(response), status_code
