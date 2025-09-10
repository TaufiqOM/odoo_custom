from odoo import models, fields

class ProjectProject(models.Model):
    _inherit = 'project.project'

    privacy_visibility = fields.Selection(
        selection_add=[
            ('invited_only', 'Invited Only'),
        ],
        ondelete={'invited_only': 'set default'}
    )
