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


