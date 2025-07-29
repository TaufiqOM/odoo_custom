from odoo import models, fields, api

class AppraisalTemplate(models.Model):
    _name = 'appraisal.template'
    _description = 'Appraisal Template'

    name = fields.Char('Template Name', required=True)
    department_id = fields.Many2one(
        'hr.department', 
        string='Department'
    )
    skill_type_id = fields.Many2one(
        'hr.skill.type',
        string='Skill Type'
    )
    skill_ids = fields.One2many(
        'hr.skill',
        compute='_compute_skill_ids',
        string='Skills'
    )
    skill_names = fields.Text(
        compute='_compute_skill_names',
        string='Skill Names',
        readonly=True
    )

    @api.depends('skill_type_id')
    def _compute_skill_ids(self):
        for record in self:
            if record.skill_type_id:
                record.skill_ids = self.env['hr.skill'].search([
                    ('skill_type_id', '=', record.skill_type_id.id)
                ])
            else:
                record.skill_ids = False

    @api.depends('skill_type_id')
    def _compute_skill_names(self):
        for record in self:
            if record.skill_type_id and record.skill_type_id.skill_ids:
                skill_names = record.skill_type_id.skill_ids.mapped('name')
                record.skill_names = '\n'.join(skill_names)
            else:
                record.skill_names = ''
