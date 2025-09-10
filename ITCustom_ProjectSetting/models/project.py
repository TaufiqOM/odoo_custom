from odoo import models, fields

class ProjectProject(models.Model):
    _inherit = 'project.project'

    privacy_visibility = fields.Selection(
        selection_add=[
            ('invited_only', 'Invited Only'),
        ],
        ondelete={'invited_only': 'set default'}
    )

    def action_open_share_project_wizard(self):
        self.ensure_one()
        if self.privacy_visibility not in ['portal', 'invited_only']:
            return False
        template = self.env.ref('project.mail_template_project_sharing', raise_if_not_found=False)

        local_context = self.env.context | {
            'default_template_id': template.id if template else False,
            'default_email_layout_xmlid': 'mail.mail_notification_light',
            'active_id': self.id,
            'active_model': 'project.project',
        }
        action = self.env["ir.actions.actions"]._for_xml_id("project.project_share_wizard_action")
        if self.env.context.get('default_access_mode'):
            action['name'] = "Share Project"
        action['context'] = local_context
        return action

    def _check_project_sharing_access(self):
        self.ensure_one()
        if self.privacy_visibility not in ['portal', 'invited_only']:
            return False
        if self.env.user._is_portal():
            return self.env['project.collaborator'].search([('project_id', '=', self.sudo().id), ('partner_id', '=', self.env.user.partner_id.id)])
        return self.env.user._is_internal()

    def write(self, vals):
        if vals.get('access_token'):
            self.ensure_one()
            if self.privacy_visibility not in ['portal', 'invited_only']:
                vals['access_token'] = ''
        return super().write(vals)
