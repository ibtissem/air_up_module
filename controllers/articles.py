import json
from odoo import http
from odoo.http import request
from .json_response import JSONResponse

article_model = request.env['product.product']


class WsAuth(http.Controller):
    @http.route('/api/articles', type='http', auth='public', methods=['GET'])
    def get_articles(self, *args, **kwargs):
        """
        Returns a list of articles

        Example response:


        :return:
        """
        res = article_model.get_product(*args, **kwargs)
        return JSONResponse(
            response=res
        )

    @http.route('/api/articles/<int:id>', type='http', auth='public', methods=['GET'])
    def get_article(self, id):
        """
        get article
        :param id:
        :return:
        """

        article_obj = http.request.env['product.product']
        article = article_obj.sudo().browse(int(id))
        if not article.exists():
            return JSONResponse(
                response={
                    'success': False,
                    'error': '[ERR_RESOURCE_NOT_FOUND] Resource not found'
                })

        res = article.read(list(set(article_obj._fields)))

        return JSONResponse(
            response=res
        )

    @http.route('/api/articles', type='http', auth='public', methods=['POST'], csrf=False)
    def create_product(self, **post):

        if False in [post.get('name', False), post.get('description', False)]:
            return http.Response(json.dumps({'response': 400, 'success': False}), status=400)

        values = {
            'name': post.get('name'),
            'description': post.get('description')
        }
        article = article_model.sudo().create(values)
        return http.Response(json.dumps({'response': 200 if article else 503,
                                         'success': True,
                                         'record_id': article.id}))

    @http.route('/api/articles/<int:id>', type='http', auth='public', methods=['PATCH'], csrf=False)
    def patch_product(self, id, **patch_data):
        print('poooooooooooooost %s', patch_data)
        if not patch_data.get('description', False):
            return http.Response(json.dumps({'response': '400 bad request', 'success': False}), status=400)

        # article = article_model.browse(id).sudo().write({"description": patch_data.get("description")})
        article_model.browse(id).sudo().write(patch_data)
        return http.Response(json.dumps({'response': 200,
                                         'success': True,
                                         'record_updated': True}), status=200)

    @http.route('/api/article/<int:id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def delete_article(self, id):
        """
        Unsubscribe the email from receiving emails
        :param token:
        :return:
        """
        article_obj = http.request.env['product.product']
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