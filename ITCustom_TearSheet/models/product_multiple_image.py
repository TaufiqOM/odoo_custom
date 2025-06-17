# Inherit model product.template

from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    sale_image_ids = fields.Many2many(
        'ir.attachment',
        string='Sale Images',
        domain="[('res_model', '=', 'product.template'), ('res_id', '=', id)]",
        help="Additional images to be displayed in Sales tab"
    )