from odoo import models, fields, api

class ProductDimensionHistory(models.Model):
    _name = 'product.dimension.history'
    _description = 'Product Dimension History'

    product_tmpl_id = fields.Many2one('product.template', string='Product', required=True)
    field_name = fields.Char(string='Field Name', required=True)
    old_value = fields.Float(string='Old Value', digits=(16, 2))
    new_value = fields.Float(string='New Value', digits=(16, 2))
    change_date = fields.Datetime(string='Change Date', default=fields.Datetime.now, required=True)
