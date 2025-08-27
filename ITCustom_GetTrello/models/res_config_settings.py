# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import requests
import logging

_logger = logging.getLogger(__name__)


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

    def action_test_trello_connection(self):
        """Test connection to Trello API"""
        self.ensure_one()
        
        if not self.trello_enabled:
            raise UserError(_("Trello integration is not enabled. Please enable it first."))
        
        if not self.trello_api_key or not self.trello_api_token:
            raise UserError(_("Please provide both Trello API Key and API Token."))
        
        if not self.trello_board_id:
            raise UserError(_("Please provide Trello Board ID."))
        
        # Test connection to Trello API
        try:
            url = f"https://api.trello.com/1/boards/{self.trello_board_id}"
            params = {
                'key': self.trello_api_key,
                'token': self.trello_api_token
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                board_data = response.json()
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _("Success"),
                        'message': _("Trello connection successful! Board: %s") % board_data.get('name', 'Unknown'),
                        'type': 'success',
                        'sticky': False,
                    }
                }
            else:
                error_msg = _("Failed to connect to Trello. Status Code: %s") % response.status_code
                if response.text:
                    error_msg += _("\nResponse: %s") % response.text[:200]
                raise UserError(error_msg)
                
        except requests.exceptions.ConnectionError:
            raise UserError(_("Connection error: Could not reach Trello API. Please check your internet connection."))
        except requests.exceptions.Timeout:
            raise UserError(_("Connection timeout: Trello API did not respond in time."))
        except requests.exceptions.RequestException as e:
            raise UserError(_("Error connecting to Trello: %s") % str(e))
        except Exception as e:
            _logger.error("Trello connection test failed: %s", str(e))
            raise UserError(_("Unexpected error occurred: %s") % str(e))
