import json
from odoo import http
from odoo.http import request
from .json_response import JSONResponse


class WsAuth(http.Controller):
    @http.route('/api/articles', type='http', auth='public', methods=['GET'])
    def get_articles(self, *args, **kwargs):
        """
        Display all articles
        :param:
        :return: JSON response
        """
        article_model = request.env['airup.product']
        res = article_model.get_product(*args, **kwargs)
        return JSONResponse(
            response=res
        )

    @http.route('/api/articles/<int:id>', type='http', auth='public', methods=['GET'])
    def get_article(self, id):
        """
        Return article by id
        :param id:
        :return: JSON response
        """
        article_obj = http.request.env['airup.product']
        article = article_obj.sudo().browse(int(id))
        if not article.exists():
            return JSONResponse(
                response={
                    'success': False,
                    'error': '[ERR_RESOURCE_NOT_FOUND] Resource not found'
                })

        return JSONResponse(
            response=article.read(list(set(article_obj._fields)))
        )

    @http.route('/api/articles', type='http', auth='public', methods=['POST'], csrf=False)
    def create_product(self, **post):
        """
        Create article
        :param post: HTTP POST data
        :return: JSON response
        """
        if False in [post.get('name', False), post.get('description', False)]:
            return http.Response(json.dumps({'response': '[ERR_RESOURCE_NOT_FOUND] Resource not found',
                                             'success': False}), status=400)

        values = {
            'name': post.get('name'),
            'description': post.get('description')
        }
        article_model = request.env['airup.product']
        article = article_model.sudo().create(values)
        return http.Response(json.dumps({'response': 200 if article else 503,
                                         'success': True,
                                         'record_id': article.id}))

    @http.route('/api/articles/<int:id>', type='http', auth='public', methods=['PATCH'], csrf=False)
    def patch_product(self, id, **patch_data):
        """
        Update article
        :param id, patch_data: HTTP PATCH data
        :return: JSON response
        """
        if not patch_data.get('description', False):
            return http.Response(json.dumps({'response': '400 bad request',
                                             'success': False}), status=400)
        article_model = request.env['airup.product']
        article = article_model.browse(id)
        if not article.exists():
            return http.Response(json.dumps({'response': '[ERR_RESOURCE_NOT_FOUND] 404 not found',
                                             'success': False}), status=404)
        article.sudo().write(patch_data)
        return http.Response(json.dumps({'response': 200,
                                         'success': True,
                                         'record_updated': True}), status=200)

    @http.route('/api/articles/<int:id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def delete_article(self, id, *args, **kwargs):
        """
        Delete article by id
        :param id:
        :return: JSON response
        """
        article_obj = http.request.env['airup.product']
        article = article_obj.sudo().browse(int(id))
        if not article.exists():
            return JSONResponse(
                response={
                    'success': False,
                    'error': '[ERR_RESOURCE_NOT_FOUND] Resource not found'
                })
        article.unlink()
        return JSONResponse(
            response={
                'success': True,
                'deleted_id': int(id)
            }
        )