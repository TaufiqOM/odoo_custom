from odoo import models, fields, api

class AppraisalTemplate(models.Model):
    _name = 'appraisal.template'
    _description = 'Appraisal Template'

    name = fields.Char('Template Name', required=True)
    department_id = fields.Many2one(
        'hr.department', 
        string='Department'
    )
    skill_types = fields.Many2many(
        'hr.skill.type',
        'appraisal_template_skill_type_rel',
        'template_id', 'skill_type_id',
        string='Skill Types'
    )
    skills = fields.Many2many(
        'hr.skill',
        'appraisal_template_skill_rel',
        'template_id', 'skill_id',
        string='Skills',
        domain="[('skill_type_id', 'in', skill_types)]"
    )
    skill_names = fields.Text(
        compute='_compute_skill_names',
        string='Skill Names',
        readonly=True
    )

    @api.depends('skills')
    def _compute_skill_names(self):
        for record in self:
            if record.skills:
                record.skill_names = '\n'.join(record.skills.mapped('name'))
            else:
                record.skill_names = ''
