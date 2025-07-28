from odoo import models, fields, api

class AppraisalSkillGroup(models.Model):
    _name = 'appraisal.skill.group'
    _description = 'Appraisal Skill Group'
    
    name = fields.Char(string='Group Name', required=True)
    description = fields.Text(string='Description')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    active = fields.Boolean(default=True)

class AppraisalSkill(models.Model):
    _inherit = 'hr.appraisal.skill'
    
    group_id = fields.Many2one('appraisal.skill.group', string='Skill Group')
    custom_group = fields.Char(string='Custom Group')
    
    def get_group_display(self):
        return self.group_id.name if self.group_id else self.custom_group