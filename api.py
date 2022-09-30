from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter
from jinja2 import Environment, FileSystemLoader
from requests import Session as RequestsSession
from webob import Request, Response
from parse import parse

import inspect
import os

class API:
    def __init__(self, templates_dir="index"):
        self.pathways = {}

        self.templates_env = Environment(
            loader = FileSystemLoader(
                os.path.abspath(templates_dir)
            )
        )

    def __call__(self, environ, start_res):
        req = Request(environ)

        res = self.handle_req(req)
        
        return res(environ, start_res)

    # работа с путями сайта
    def add_pathway(self, path, handler): # роутер, функция добавления путей сайта
        assert path not in self.pathways, "Such pathway already exists!"

        self.pathways[path] = handler

    def pathway(self, path): # роутер, декоратор путей сайта
        assert path not in self.pathways, "Such pathway already exists!"

        def wrapper(handler):
            self.add_pathway(path, handler)
            return handler
        
        return wrapper

    # слушатели событий
    def handle_req(self, req): # слушатель запроса
        res = Response()

        handler, kwargs = self.find_handler(req_path=req.path)

        if handler is not None:
            if inspect.isclass(handler):
                handler = getattr(handler(), req.method.lower(), None)

                if handler is None:
                    raise AttributeError("Method not allowed", req.method)

                handler(req, res, **kwargs)

            else:
                handler(req, res, **kwargs)
        else:
            self.default_res(res)
    
        return res

    def find_handler(self, req_path): # парсинг url-путя
        for path, handler in self.pathways.items():
            parse_result = parse(path, req_path)
            if parse_result is not None:
                return handler, parse_result.named
            
        return None, None

    def default_res(self, res): # Ошибка 404. Реакция на путь к пустой странице 
        res.status_code = 404
        res.text = "Unknown page"

    # Шаблоны
    def template(self, template_name, context=None):
        if context is None:
            context = {}

        return self.templates_env.get_template(template_name).render(**context)

    # Тесты
    def test_session(self, base_url="http://ion"):
        session = RequestsSession()
        session.mount(prefix=base_url, adapter=RequestsWSGIAdapter(self))

        return session