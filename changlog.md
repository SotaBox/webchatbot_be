### Changlog
## Release v1.0.0(25/06/2024)
# New Features:

- Add modules to handle login (login.py), logout (logout.py), refresh token (refresh_token.py), get user information (get_profile.py), register (register.py) in auth_handlers.
- Add router to handle login, register and token management (auth_routers.py).
- Add service to handle authentication related logic (auth_services.py).
- Add user.py repo to interact with database for User entity.

## Release v1.0.1(28/06/2024)
# Add new feartures:

- Add module to handle process message (process_mesage.py) in chat_handlers.
- Add router to handle process message (chat_routers.py)
- Add service to handle the process of giving the sever's answer to the client, comblined with Azure OpenAI

## Release v1.0.2(09/07/2024)
# Add new feartures:

- Add module to crawl list of links from URL (craw_sitemap.py) in crawl_handlers.
- Add module to crawl data from links (crawl_link.py) in crawl_handlers.
- Add router to handle crawling operations (crawl_routers.py)
- Add service to handle crawl related logic (crawl_services.py).
- Add url_sitemap.py repo to interact with database for URL entity.