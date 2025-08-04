from odoo import models, fields, api

class PerformanceGuidelines(models.Model):
    _name = 'performance.guidelines'
    _description = 'Performance Evaluation Guidelines'
    _order = 'sequence, id'

    sequence = fields.Integer('Sequence', default=10)
    template_id = fields.Many2one(
        'appraisal.template', 
        string='Appraisal Template', 
        required=True, 
        ondelete='cascade'
    )
    factor = fields.Char('Faktor Perilaku Kerja', required=True)
    definition = fields.Text('Definisi')
    value_1 = fields.Text('NILAI 1 (Kurang Diterima)')
    value_2 = fields.Text('NILAI 2 (Butuh Arahan)')
    value_3 = fields.Text('NILAI 3 (Standart)')
    value_4 = fields.Text('NILAI 4 (Performa Bagus)')
    value_5 = fields.Text('NILAI 5 (Luar Biasa)')
