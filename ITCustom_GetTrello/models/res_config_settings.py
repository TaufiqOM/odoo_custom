# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    trello_api_key = fields.Char(
        string='Trello API Key',
        config_parameter='itcustom_gettrello.trello_api_key',
        help='API Key untuk mengakses Trello API'
    )
    
    trello_api_token = fields.Char(
        string='Trello API Token',
        config_parameter='itcustom_gettrello.trello_api_token',
        help='API Token untuk mengakses Trello API'
    )
    
    trello_board_id = fields.Char(
        string='Trello Board ID',
        config_parameter='itcustom_gettrello.trello_board_id',
        help='ID Board Trello yang akan digunakan'
    )
    
    trello_enabled = fields.Boolean(
        string='Enable Trello Integration',
        config_parameter='itcustom_gettrello.trello_enabled',
        help='Aktifkan integrasi dengan Trello'
    )
    
    trello_sync_interval = fields.Selection([
        ('15', '15 menit'),
        ('30', '30 menit'),
        ('60', '1 jam'),
        ('120', '2 jam'),
        ('360', '6 jam'),
        ('720', '12 jam'),
        ('1440', '24 jam'),
    ], string='Sync Interval',
        config_parameter='itcustom_gettrello.trello_sync_interval',
        default='60',
        help='Interval sinkronisasi dengan Trello'
    )
