import json
from odoo import http
from odoo.http import request
from .json_response import JSONResponse


class WsAuth(http.Controller):
    @http.route('/api/warehouse', type='http', auth='public', methods=['GET'])
    def get_warehouse(self, *args, **kwargs):
        warehouse_model = http.request.env['warehouse.stock']
        res = warehouse_model.get_product_quantity(*args, **kwargs)

        print(res)
        return JSONResponse(
            response=res
        )

    @http.route('/api/warehouse', type='http', auth='public', methods=['POST'], csrf=False)
    def create_warehouse(self, **post):
        print('pppppppppppppost %s', post)
        if False in [post.get('row', False), post.get('bay', False),
                     post.get('id', False), post.get('amount', False)]:
            return http.Response(json.dumps({'response': 500,
                                             'success': False,
                                             'error': '[ERR_MISSING_DATA] Missing Data'}))

        shelf = request.env['warehouse.shelf'].sudo().search(
            [('row', '=', post.get('row')), ('bay', '=', post.get('bay'))], limit=1)
        warehouse_model = request.env['warehouse.stock']
        values = {
            'shelf_id': shelf.id,
            'product_id': post.get('id'),
            'quantity': post.get('amount'),
        }
        warehouse_stock = warehouse_model.sudo().create(values)
        return http.Response(json.dumps({'response': 200 if shelf else 503,
                                         'success': True,
                                         'record_id': warehouse_stock.id}))

    @http.route('/api/warehouse', type='http', auth='public', methods=['PUT'], csrf=False)
    def put_product_shelf(self, **put_data):
        if False in [put_data.get('row', False), put_data.get('bay', False),
                     put_data.get('id', False)]:
            return http.Response(json.dumps({'response': 500,
                                             'success': False,
                                             'error': '[ERR_MISSING_DATA] Missing Data'}))
        warehouse_model = request.env['warehouse.stock']
        shelf = request.env['warehouse.shelf'].sudo().search([('row', '=', int(put_data['row'])),
                                                ('bay', '=', int(put_data['bay']))], limit=1)
        print('shelf', shelf)
        if not shelf:
            return http.Response(json.dumps({'response': '404 resource not found',
                                             'success': False}),
                                 status=404)
        try:
            warehouse = warehouse_model.sudo().search([('shelf_id', '=', shelf.id),
                                    ('product_id', '=', int(put_data['id']))])
            print('waaaarehouse', warehouse)
            quant = warehouse.quantity - 1 if warehouse.quantity > 0 else 0
            print('quant', quant)
            warehouse.sudo().write({'quantity': quant})
            return http.Response(json.dumps({'response': 200,
                                             'success': True,
                                             'record_updated': warehouse.quantity}), status=200)
        except Exception:
            return http.Response(json.dumps({'response': '400 bad request', 'success': False}), status=400)
