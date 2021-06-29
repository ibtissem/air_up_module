from odoo import api, fields, models

class Warehouse(models.Model):
    _name = 'warehouse.stock'

    shelf_id = fields.Many2one('warehouse.shelf')
    product_id = fields.Many2one('airup.product')
    quantity = fields.Integer('Quantity of product by shelf')

    @api.model
    def get_product_quantity(self, *args, **kwargs):
        _cr = self.env.cr
        query = ('''
            select sum(ws.quantity) as amount, 
                    ws.product_id as id, 
                    ap.name as name
            from warehouse_stock ws
            left join airup_product ap  on ap.id = ws.product_id
            GROUP BY ws.product_id, ap.name;
        ''')

        _cr.execute(query)
        return _cr.dictfetchall()