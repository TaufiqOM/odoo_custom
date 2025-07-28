from odoo import models, fields

class AppraisalTemplate(models.Model):
    _name = 'appraisal.template'
    _description = 'Appraisal Template'

    name = fields.Char('Template Name', required=True)
