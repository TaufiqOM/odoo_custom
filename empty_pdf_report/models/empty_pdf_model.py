# -*- coding: utf-8 -*-
from odoo import models, fields, api

class EmptyPDFModel(models.Model):
    _name = 'empty.pdf.model'
    _description = 'Empty PDF Report Model'
    
    name = fields.Char(string='Name', default='Empty Report')
    date = fields.Date(string='Date', default=fields.Date.today())
    description = fields.Text(string='Description')
