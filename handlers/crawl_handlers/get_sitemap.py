from flask import jsonify, request
from services.chat_sevices import ChatService
from services.crawl_services import CrawlService

def get_sitemap_handler():
    parent_link = request.args.get('parent_link')
    if not parent_link:
        return jsonify({'error': 'Parent link is required'}), 400

    access_token_error = ChatService.check_valid_access_token()
    if access_token_error:
        return jsonify(access_token_error[0]), access_token_error[1]

    response, status_code = CrawlService.get_list_link(parent_link)
    return jsonify(response), status_code
