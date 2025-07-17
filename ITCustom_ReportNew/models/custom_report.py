from odoo import models, fields, api

class CustomReport(models.Model):
    _name = 'custom.report'
    _description = 'Custom Report'

    name = fields.Char(string='Report Name', required=True)
    report_date = fields.Date(string='Report Date', default=fields.Date.today)
    report_type = fields.Selection([
        ('sales', 'Sales Report'),
        ('purchase', 'Purchase Report'),
        ('inventory', 'Inventory Report'),
        ('exim', 'Exim Report'),
        ('cs', 'CS Report'),
    ], string='Report Type', default='sales')
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)

    @api.model
    def print_report(self, report_id):
        return {
            'type': 'ir.actions.report',
            'report_name': 'ITCustom_ReportNew.custom_report_template',
            'report_type': 'qweb-pdf',
            'report_file': 'ITCustom_ReportNew.custom_report_template',
            'context': {'active_id': report_id},
        }
