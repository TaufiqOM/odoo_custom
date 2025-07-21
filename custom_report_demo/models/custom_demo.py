# -*- coding: utf-8 -*-
from odoo import models, fields, api

class CustomDemo(models.Model):
    _name = 'custom.demo'
    _description = 'Custom Demo Model for Report'
    
    name = fields.Char(string='Name', required=True)
    date = fields.Date(string='Date', default=fields.Date.today)
    partner_id = fields.Many2one('res.partner', string='Customer')
    amount = fields.Float(string='Amount')
    description = fields.Text(string='Description')
    line_ids = fields.One2many('custom.demo.line', 'demo_id', string='Lines')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done')
    ], string='Status', default='draft')
    
    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount')
    currency_id = fields.Many2one('res.currency', string='Currency', 
                                  default=lambda self: self.env.company.currency_id)
    
    @api.depends('line_ids.subtotal')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(line.subtotal for line in record.line_ids)

    def action_confirm(self):
        """Confirm the demo record"""
        for record in self:
            if record.state == 'draft':
                record.state = 'confirmed'

    def action_done(self):
        """Mark the demo record as done"""
        for record in self:
            if record.state == 'confirmed':
                record.state = 'done'

    def action_draft(self):
        """Reset the demo record to draft"""
        for record in self:
            if record.state in ['confirmed', 'done']:
                record.state = 'draft'

class CustomDemoLine(models.Model):
    _name = 'custom.demo.line'
    _description = 'Custom Demo Line'
    
    demo_id = fields.Many2one('custom.demo', string='Demo')
    product_id = fields.Many2one('product.product', string='Product')
    quantity = fields.Float(string='Quantity', default=1.0)
    price_unit = fields.Float(string='Unit Price')
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal')
    
    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit
