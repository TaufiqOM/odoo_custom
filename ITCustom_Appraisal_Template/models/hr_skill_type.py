from odoo import models, fields

class HrSkillType(models.Model):
    _inherit = 'hr.skill.type'
    
    kepemimpinan = fields.Boolean(
        string='Kepemimpinan',
        default=False,
        help='Menandai jenis skill ini sebagai skill kepemimpinan'
    )
