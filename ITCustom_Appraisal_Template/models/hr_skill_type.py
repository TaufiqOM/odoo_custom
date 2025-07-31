from odoo import models, fields

class HrSkillType(models.Model):
    _inherit = 'hr.skill.type'
    
    bobot_nilai = fields.Integer(
        string='Bobot Nilai',
        default=0,
        help='Bobot nilai untuk jenis skill ini'
    )
    
    kepemimpinan = fields.Boolean(
        string='Kepemimpinan',
        default=False,
        help='Menandai jenis skill ini sebagai skill kepemimpinan'
    )
