# -*- coding: utf-8 -*-
from odoo import models, fields, api

class HrAppraisal(models.Model):
    _inherit = 'hr.appraisal'
    
    # Custom fields untuk tab baru
    custom_notes = fields.Text(string='Catatan Tambahan')
    custom_rating = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('average', 'Average'),
        ('poor', 'Poor')
    ], string='Penilaian Custom')
    
    custom_date = fields.Date(string='Tanggal Custom')
    custom_boolean = fields.Boolean(string='Opsi Tambahan')
    
    # Contoh field relasional
    custom_user_id = fields.Many2one('res.users', string='User Custom')
    
    # Contoh field computed
    custom_summary = fields.Char(string='Ringkasan', compute='_compute_custom_summary')
    
    @api.depends('custom_notes', 'custom_rating')
    def _compute_custom_summary(self):
        for record in self:
            if record.custom_rating and record.custom_notes:
                record.custom_summary = f"{record.custom_rating}: {record.custom_notes[:50]}..."
            else:
                record.custom_summary = "Belum ada data"
