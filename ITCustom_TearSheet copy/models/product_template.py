from odoo import models, fields, api
from datetime import datetime

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    tear_sheet_pdf = fields.Binary(string="Tear Sheet PDF")
    tear_sheet_pdf_filename = fields.Char(string="PDF Filename")