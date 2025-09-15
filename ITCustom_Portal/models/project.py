from odoo import models, fields

class ProjectProject(models.Model):
    _inherit = 'project.project'

    privacy_visibility = fields.Selection(
        selection=[
            ('followers', 'Invited internal users (private)'),
            ('employees', 'All internal users'),
            ('portal', 'Invited portal users and invited internal users (public)'),
        ]
    )

    def _check_project_sharing_access(self):
        self.ensure_one()
        if self.privacy_visibility == 'portal':
            if self.env.user._is_portal():
                return self.env['project.collaborator'].search([('project_id', '=', self.sudo().id), ('partner_id', '=', self.env.user.partner_id.id)])
            else:
                return self.env.user.partner_id in self.message_follower_ids.mapped('partner_id')
        return super()._check_project_sharing_access()
