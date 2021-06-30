import json
from odoo import http
from odoo.http import request
from .json_response import JSONResponse


class WsAuth(http.Controller):
    @http.route('/api/shelfs', type='http', auth='public', methods=['GET'])
    def get_shelfs(self, *args, **kwargs):
        """
        Display all shelfs
        :param:
        :return: JSON response
        """
        shelfs_model = http.request.env['warehouse.shelf']
        res = shelfs_model.get_shelfs(*args, **kwargs)
        return JSONResponse(
            response=res
        )

    @http.route('/api/shelfs/<int:row>', type='http', auth='public', methods=['GET'])
    def get_shelfs_by_row(self, row):
        """
        Return shelf by id
        :param row:
        :return: JSON response
        """
        shelfs_model = http.request.env['warehouse.shelf']
        shelfs = shelfs_model.get_bay_by_row(row)
        if not shelfs:
            return JSONResponse(
                response={
                    'success': False,
                    'error': '[ERR_RESOURCE_NOT_FOUND] Resource not found'
                })

        return JSONResponse(
            response=shelfs
        )

    @http.route('/api/shelfs/<int:row>/<int:bay>', type='http', auth='public', methods=['GET'])
    def get_shelfs_by_row_bay(self, row, bay):
        """
        Return article by row and bay combo
        :param row, bay:
        :return: JSON response
        """
        shelfs_model = http.request.env['warehouse.shelf']
        shelfs = shelfs_model.get_shelf_by_bay_row(row, bay)
        if not shelfs:
            return JSONResponse(
                response={
                    'success': False,
                    'error': '[ERR_RESOURCE_NOT_FOUND] Resource not found'
                })

        return JSONResponse(
            response=shelfs
        )

    @http.route('/api/shelfs', type='http', auth='public', methods=['POST'], csrf=False)
    def create_shelf(self, **post):
        """
        Create Shelf
        :param post: HTTP POST data
        :return: JSON response
        """
        if False in [post.get('row', False), post.get('bay', False),
                     post.get('height', False), post.get('width', False),
                     post.get('depth', False)]:
            return http.Response(json.dumps({'response': 500,
                                             'success': False,
                                             'error': '[ERR_MISSING_DATA] Missing Data'}))

        shelf_model = request.env['warehouse.shelf']
        values = {
            'row': post.get('row'),
            'bay': post.get('bay'),
            'depth': post.get('depth'),
            'height': post.get('height'),
            'width': post.get('width'),
        }
        try:
            shelf = shelf_model.sudo().create(values)
            return http.Response(json.dumps({'response': 200 if shelf else 503,
                                             'success': True,
                                             'record_id': shelf.id}))
        except Exception:
            return http.Response(json.dumps({'response': 'bad data introduced',
                                             'success': False}), status=400)

    @http.route('/api/shelfs/<int:row>/<int:bay>', type='http', auth='public', methods=['PATCH'], csrf=False)
    def patch_shelf_row_bay(self, row, bay, **patch_data):
        """
        Update shelf b row and bay
        :param row, bay: HTTP PATCH data
        :return: JSON response
        """
        shelf_model = request.env['warehouse.shelf']
        shelfs = shelf_model.sudo().search([('row', '=', row),
                                            ('bay', '=', bay)])
        if not shelfs:
            return http.Response(json.dumps({'response': '[ERR_RESOURCE_NOT_FOUND] 404 not found',
                                             'success': False}), status=404)
        try:
            shelfs.sudo().write(patch_data)
            return http.Response(json.dumps({'response': 200,
                                             'success': True,
                                             'record_updated': shelfs.ids}), status=200)
        except Exception:
            return http.Response(json.dumps({'response': '400 bad request',
                                             'success': False}), status=400)

    @http.route('/api/shelfs/<int:row>/<int:bay>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def delete_shelf(self, row, bay):
        """
        Delete shelf by row and bay
        :param row, bay:
        :return: JSON response
        """
        shelf_model = request.env['warehouse.shelf']
        shelfs = shelf_model.sudo().search([('row', '=', row),
                                            ('bay', '=', bay)])
        to_be_deleted_ids = shelfs.ids
        if not shelfs.exists():
            return JSONResponse(
                response={
                    'success': False,
                    'error': '[ERR_RESOURCE_NOT_FOUND] Resource not found'
                })
        shelfs.unlink()
        return JSONResponse(
            response={
                'success': True,
                'deleted_id': to_be_deleted_ids
            }
        )
