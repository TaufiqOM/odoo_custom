from odoo import models

class ProjectShareWizard(models.TransientModel):
    _inherit = 'project.share.wizard'

    def action_send_mail(self):
        self.ensure_one()
        project = self.env['project.project'].browse(self.res_id)
        if project.privacy_visibility != 'invited_only':
            project.privacy_visibility = 'portal'
        result = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'type': 'success',
                'message': _("Project shared with your collaborators."),
                'next': {'type': 'ir.actions.act_window_close'},
            }}
        partner_ids_in_readonly_mode = []
        partner_ids_in_edit_mode = []
        for collaborator in self.collaborator_ids:
            if not collaborator.send_invitation:
                continue
            if collaborator.access_mode == 'read':
                partner_ids_in_readonly_mode.append(collaborator.partner_id.id)
            else:
                partner_ids_in_edit_mode.append(collaborator.partner_id.id)
        if partner_ids_in_edit_mode:
            new_collaborators = self.env['res.partner'].browse(partner_ids_in_edit_mode)
            portal_partners = new_collaborators.filtered('user_ids')
            # send mail to users
            self._send_public_link(portal_partners)
            self._send_signup_link(partners=new_collaborators.with_context({'signup_valid': True}) - portal_partners)
        if partner_ids_in_readonly_mode:
            self.partner_ids = self.env['res.partner'].browse(partner_ids_in_readonly_mode)
            super().action_send_mail()
        return result

    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            project = self.env['project.project'].browse(record.res_id)
            if project.privacy_visibility == 'invited_only' and not project.access_token:
                project.access_token = self.env['mail.thread']._generate_access_token()
        return records
