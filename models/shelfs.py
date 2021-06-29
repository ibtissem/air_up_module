from odoo import api, fields, models

class WarehouseShelf(models.Model):
    _name = 'warehouse.shelf'

    row = fields.Integer(string="Ref")
    bay = fields.Integer(string="Product")
    depth = fields.Float(digits=(4, 3), required=True)
    width = fields.Float(digits=(4, 3), required=True)
    height = fields.Float(digits=(4, 3), required=True)

    @api.model
    def get_shelfs(self, *args, **kwargs):
        _cr = self.env.cr
        query = ('''
            select row , bay from warehouse_shelf  
        ''')

        _cr.execute(query)
        return _cr.dictfetchall()

    @api.model
    def get_bay_by_row(self, row):
        _cr = self.env.cr
        query = ('''
            select bay from warehouse_shelf where row = %s
        ''')

        _cr.execute(query, (row,))
        return _cr.dictfetchall()

    @api.model
    def get_shelf_by_bay_row(self, row, bay):
        _cr = self.env.cr

        query = ('''
                select height, width, depth from warehouse_shelf where row = %s and bay = %s
            ''')

        _cr.execute(query, (row, bay,))
        return _cr.dictfetchall()
