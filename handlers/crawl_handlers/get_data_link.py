from flask import jsonify, request
from services.chat_sevices import ChatService
from services.crawl_services import CrawlService

def get_data_link_handler():
    link = request.args.get('link')
    if not link:
        return jsonify({'error': 'URL is required'}), 400

    access_token_error = ChatService.check_valid_access_token()
    if access_token_error:
        return jsonify(access_token_error[0]), access_token_error[1]

    response, status_code = CrawlService.get_data_from_link(link)
    return jsonify(response), status_code
