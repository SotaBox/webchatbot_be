from flask import Blueprint
from flask_jwt_extended import jwt_required

from handlers.crawl_handlers.crawl_link import crawl_link_handler
from handlers.crawl_handlers.crawl_sitemap import crawl_sitemap_handler
from handlers.crawl_handlers.get_sitemap import get_sitemap_handler
from handlers.crawl_handlers.get_data_link import get_data_link_handler
from handlers.crawl_handlers.search_data_from_parent_link import search_data_from_parent_link_handler

routers_crawl = Blueprint('crawl',__name__)

@routers_crawl.route('/crawl/crawl-data-from-link',methods = ['POST'])
@jwt_required()
def crawl_text_from_url():
    return crawl_link_handler()

@routers_crawl.route('/crawl/crawl-sitemap',methods = ['POST'])
@jwt_required()
def crawl_sitemap():
    return crawl_sitemap_handler()

@routers_crawl.route('/crawl/get-sitemap',methods = ['GET'])
@jwt_required()
def get_sitemap():
    return get_sitemap_handler()

@routers_crawl.route('/crawl/get-data-from-link',methods = ['GET'])
@jwt_required()
def get_data_link():
    return get_data_link_handler()

@routers_crawl.route('/crawl/search-data-from-parent-link',methods = ['GET'])
@jwt_required()
def search_data_from_url():
    return search_data_from_parent_link_handler()

