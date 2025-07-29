from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class HrAppraisal(models.Model):
    _inherit = 'hr.appraisal'

    memiliki_bawahan = fields.Boolean(string="Memiliki Bawahan")

    def action_get_skills_data(self):
        """
        Action to get skills data from appraisal templates based on department_id
        and include leadership skills if memiliki_bawahan is True.
        This method will be triggered by the 'Get Data' button in the Skills tab
        """
        self.ensure_one()
        
        _logger.info("Starting action_get_skills_data for appraisal ID %s, department %s, memiliki_bawahan: %s",
                     self.id, self.department_id.name, self.memiliki_bawahan)
        
        # Initialize list for skills to add
        skills_to_add = []
        
        # Find appraisal templates that match the department_id
        matching_templates = self.env['appraisal.template'].search([
            ('department_id', '=', self.department_id.id)
        ])
        _logger.info("Found %d matching templates for department %s",
                     len(matching_templates), self.department_id.name)
        
        # Get skills from matching templates
        for template in matching_templates:
            skills_to_add.extend(template.skills.ids)
            _logger.info("Added %d skills from template %s", len(template.skills), template.name)
        
        # If memiliki_bawahan is True, include skills from skill types where kepemimpinan is True
        if self.memiliki_bawahan:
            leadership_skill_types = self.env['hr.skill.type'].search([
                ('kepemimpinan', '=', True)
            ])
            _logger.info("Found %d skill types with kepemimpinan=True", len(leadership_skill_types))
            
            for skill_type in leadership_skill_types:
                leadership_skills = self.env['hr.skill'].search([
                    ('skill_type_id', '=', skill_type.id)
                ])
                _logger.info("Found %d skills for skill type %s", len(leadership_skills), skill_type.name)
                skills_to_add.extend(leadership_skills.ids)
        
        # Remove duplicates
        skills_to_add = list(set(skills_to_add))
        _logger.info("Total unique skills to add: %d", len(skills_to_add))
        
        if not skills_to_add:
            raise UserError(_('No skills found in templates or leadership skills for department %s') % self.department_id.name)
        
        # Create appraisal skills
        created_skills = []
        for skill_id in skills_to_add:
            # Check if skill already exists in appraisal
            existing_skill = self.skill_ids.filtered(
                lambda s: s.skill_id.id == skill_id
            )
            
            if not existing_skill:
                skill = self.env['hr.skill'].browse(skill_id)
                
                # Get default skill level (Belum Dinilai) for this skill type
                default_level = self.env['hr.skill.level'].search([
                    ('skill_type_id', '=', skill.skill_type_id.id),
                    ('name', '=', 'Belum Dinilai')
                ], limit=1)
                
                if not default_level:
                    _logger.info("No 'Belum Dinilai' skill level found for skill type %s, creating default", skill.skill_type_id.name)
                    default_level = self.env['hr.skill.level'].create({
                        'name': 'Belum Dinilai',
                        'skill_type_id': skill.skill_type_id.id,
                        'level_progress': 0,
                    })
                
                # Use skill's definisi as justification
                justification = skill.definisi or _('Tidak ada defisini untuk skill ini')
                
                # Create new appraisal skill, letting Odoo apply default values for unspecified fields
                values = {
                    'appraisal_id': self.id,
                    'skill_type_id': skill.skill_type_id.id,
                    'skill_id': skill.id,
                    'skill_level_id': default_level.id,
                    'justification': justification,
                }
                
                new_skill = self.env['hr.appraisal.skill'].create(values)
                created_skills.append(new_skill)
                _logger.info("Created appraisal skill: %s (Type: %s, Skill Level: %s)",
                             skill.name, skill.skill_type_id.name, default_level.name)
        
        if created_skills:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Success'),
                    'message': _('%d skills have been loaded from appraisal templates and leadership skills for department %s') % (
                        len(created_skills), self.department_id.name),
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
                    'message': _('All template and leadership skills are already present in this appraisal'),
                    'type': 'info',
                    'sticky': False,
                }
            }