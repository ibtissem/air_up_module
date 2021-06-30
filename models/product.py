from odoo import api, models, fields


class Product(models.Model):
    _name = 'airup.product'

    name = fields.Char('Name')
    description = fields.Text('Description')

    @api.model
    def get_product(self, *args, **kwargs):
        _cr = self.env.cr
        query = ('''
            select name, id from airup_product
        ''')
        _cr.execute(query)
        return _cr.dictfetchall()
