from odoo import models, fields, api, _
from odoo.exceptions import UserError

class HrAppraisal(models.Model):
    _inherit = 'hr.appraisal'

    def action_get_skills_data(self):
        """
        Action to get skills data from appraisal templates based on department_id
        This method will be triggered by the 'Get Data' button in the Skills tab
        """
        self.ensure_one()
        
        # Find appraisal templates that match the department_id
        matching_templates = self.env['appraisal.template'].search([
            ('department_id', '=', self.department_id.id)
        ])
        
        if not matching_templates:
            raise UserError(_('No appraisal templates found for department %s') % self.department_id.name)
        
        # Get all skills from matching templates
        skills_to_add = []
        for template in matching_templates:
            skills_to_add.extend(template.skills.ids)
        
        # Remove duplicates
        skills_to_add = list(set(skills_to_add))
        
        if not skills_to_add:
            raise UserError(_('No skills found in templates for department %s') % self.department_id.name)
        
        # Create appraisal skills based on template skills
        created_skills = []
        for skill_id in skills_to_add:
            # Check if skill already exists in appraisal
            existing_skill = self.skill_ids.filtered(
                lambda s: s.skill_id.id == skill_id
            )
            
            if not existing_skill:
                skill = self.env['hr.skill'].browse(skill_id)
                
                # Get default skill level for this skill type
                default_level = self.env['hr.skill.level'].search([
                    ('skill_type_id', '=', skill.skill_type_id.id)
                ], limit=1)
                
                if not default_level:
                    # Create a default level if none exists
                    default_level = self.env['hr.skill.level'].create({
                        'name': _('Entry Level'),
                        'skill_type_id': skill.skill_type_id.id,
                        'level_progress': 0,
                    })
                
                # Create new appraisal skill
                new_skill = self.env['hr.appraisal.skill'].create({
                    'appraisal_id': self.id,
                    'skill_type_id': skill.skill_type_id.id,
                    'skill_id': skill.id,
                    'skill_level_id': default_level.id,
                    'level_progress': 0,
                    'justification': _('Loaded from template: %s') % ', '.join(
                        matching_templates.filtered(lambda t: skill.id in t.skills.ids).mapped('name')
                    ),
                })
                created_skills.append(new_skill)
        
        if created_skills:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Success'),
                    'message': _('%d skills have been loaded from appraisal templates for department %s') % (len(created_skills), self.department_id.name),
                    'type': 'success',
                    'sticky': False,
                }
            }
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Info'),
                    'message': _('All template skills are already present in this appraisal'),
                    'type': 'info',
                    'sticky': False,
                }
            }
