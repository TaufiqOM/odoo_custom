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

    def action_sync_trello_data(self):
        """Sync all data from Trello board to Project module"""
        self.ensure_one()
        
        if not self.trello_enabled:
            raise UserError(_("Trello integration is not enabled. Please enable it first."))
        
        if not self.trello_api_key or not self.trello_api_token:
            raise UserError(_("Please provide both Trello API Key and API Token."))
        
        if not self.trello_board_id:
            raise UserError(_("Please provide Trello Board ID."))
        
        try:
            # Show sync started notification
            self.env['bus.bus']._sendone(
                self.env.user.partner_id,
                'display_notification',
                {
                    'type': 'warning',
                    'title': _("Sync Started"),
                    'message': _("Starting Trello data sync..."),
                    'sticky': False,
                }
            )
            
            # Fetch board information
            board_url = f"https://api.trello.com/1/boards/{self.trello_board_id}"
            params = {
                'key': self.trello_api_key,
                'token': self.trello_api_token
            }
            
            board_response = requests.get(board_url, params=params, timeout=30)
            if board_response.status_code != 200:
                raise UserError(_("Failed to fetch board information. Status Code: %s") % board_response.status_code)
            
            board_data = board_response.json()
            board_name = board_data.get('name', 'Unknown Board')
            
            # Fetch all lists from the board
            lists = self._fetch_trello_lists()
            _logger.info("Found %d lists in Trello board", len(lists))
            
            # Fetch all cards from the board
            cards = self._fetch_trello_cards()
            _logger.info("Found %d cards in Trello board", len(cards))
            
            # Sync data to Project module
            sync_result = self._sync_to_project(board_name, lists, cards)
            
            # Show sync completed notification
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _("Sync Completed"),
                    'message': _("Trello data sync completed successfully!\n"
                                "Board: %s\n"
                                "Lists: %d\n"
                                "Cards: %d\n"
                                "Projects created/updated: %d\n"
                                "Tasks created/updated: %d") % (
                        board_name, len(lists), len(cards),
                        sync_result.get('projects_count', 0),
                        sync_result.get('tasks_count', 0)
                    ),
                    'type': 'success',
                    'sticky': True,
                }
            }
            
        except Exception as e:
            _logger.error("Trello sync failed: %s", str(e))
            raise UserError(_("Sync failed: %s") % str(e))

    def _fetch_trello_lists(self):
        """Fetch all lists from Trello board"""
        try:
            url = f"https://api.trello.com/1/boards/{self.trello_board_id}/lists"
            params = {
                'key': self.trello_api_key,
                'token': self.trello_api_token
            }
            
            response = requests.get(url, params=params, timeout=30)
            if response.status_code == 200:
                return response.json()
            else:
                _logger.error("Failed to fetch lists: %s", response.text)
                return []
        except Exception as e:
            _logger.error("Error fetching lists: %s", str(e))
            return []

    def _fetch_trello_cards(self):
        """Fetch all cards from Trello board with attachments"""
        try:
            url = f"https://api.trello.com/1/boards/{self.trello_board_id}/cards"
            params = {
                'key': self.trello_api_key,
                'token': self.trello_api_token,
                'attachments': 'true'  # Include attachments in the response
            }
            
            response = requests.get(url, params=params, timeout=30)
            if response.status_code == 200:
                return response.json()
            else:
                _logger.error("Failed to fetch cards: %s", response.text)
                return []
        except Exception as e:
            _logger.error("Error fetching cards: %s", str(e))
            return []

    def _fetch_trello_attachments(self, card_id):
        """Fetch attachments for a specific Trello card"""
        try:
            url = f"https://api.trello.com/1/cards/{card_id}/attachments"
            params = {
                'key': self.trello_api_key,
                'token': self.trello_api_token
            }
            
            response = requests.get(url, params=params, timeout=30)
            if response.status_code == 200:
                return response.json()
            else:
                _logger.error("Failed to fetch attachments for card %s: %s", card_id, response.text)
                return []
        except Exception as e:
            _logger.error("Error fetching attachments for card %s: %s", card_id, str(e))
            return []

    def _download_and_attach_file(self, task, attachment_url, filename):
        """Download file from URL and attach it to the task"""
        try:
            # Download the file
            response = requests.get(attachment_url, timeout=30)
            if response.status_code == 200:
                # Create attachment
                attachment = self.env['ir.attachment'].create({
                    'name': filename,
                    'datas': response.content.encode('base64'),
                    'res_model': 'project.task',
                    'res_id': task.id,
                    'type': 'binary',
                })
                _logger.info("Attached file %s to task %s", filename, task.name)
                return attachment
            else:
                _logger.error("Failed to download file %s: %s", attachment_url, response.text)
                return None
        except Exception as e:
            _logger.error("Error downloading file %s: %s", attachment_url, str(e))
            return None

    def _sync_to_project(self, board_name, lists, cards):
        """Sync Trello data to Project module"""
        project_model = self.env['project.project']
        task_model = self.env['project.task']
        stage_model = self.env['project.task.type']
        
        projects_count = 0
        tasks_count = 0
        
        # Create main project for the board
        main_project = project_model.search([
            ('name', '=', board_name),
            ('trello_board_id', '=', self.trello_board_id)
        ], limit=1)
        
        if not main_project:
            main_project = project_model.create({
                'name': board_name,
                'trello_board_id': self.trello_board_id,
                'description': f"Trello Board: {board_name}\nBoard ID: {self.trello_board_id}"
            })
            projects_count += 1
            _logger.info("Created main project: %s", board_name)
        else:
            _logger.info("Found existing project: %s", board_name)
        
        # Create stages for each list and map them to the project
        stage_mapping = {}
        for trello_list in lists:
            list_name = trello_list.get('name', 'Unnamed List')
            list_id = trello_list.get('id')
            
            # Create or update stage for this list
            stage = stage_model.search([
                ('name', '=', list_name)
            ], limit=1)
            
            if not stage:
                stage = stage_model.create({
                    'name': list_name,
                })
                _logger.info("Created stage for list: %s", list_name)
            
            stage_mapping[list_id] = stage.id
        
        # Link stages to the project if they're not already linked
        current_stage_ids = main_project.type_ids.ids
        new_stage_ids = list(stage_mapping.values())
        stages_to_add = list(set(new_stage_ids) - set(current_stage_ids))
        
        if stages_to_add:
            main_project.write({
                'type_ids': [(4, stage_id) for stage_id in stages_to_add]
            })
            _logger.info("Added %d stages to project", len(stages_to_add))
        
        # Create tasks for all cards and assign them to the correct stage
        for card in cards:
            card_name = card.get('name', 'Unnamed Card')
            card_id = card.get('id')
            card_desc = card.get('desc', '')
            card_due = card.get('due')
            card_url = card.get('url')
            list_id = card.get('idList')
            
            # Get the corresponding stage for this card's list
            stage_id = stage_mapping.get(list_id)
            
            # Create or update task
            task = task_model.search([
                ('name', '=', card_name),
                ('trello_card_id', '=', card_id),
                ('project_id', '=', main_project.id)
            ], limit=1)
            
            task_vals = {
                'name': card_name,
                'description': card_desc or '',
                'trello_card_id': card_id,
                'project_id': main_project.id,
            }
            
            if stage_id:
                task_vals['stage_id'] = stage_id
            
            if card_due:
                # Convert Trello date format (ISO 8601 with Zulu time) to Odoo format
                try:
                    from datetime import datetime
                    # Parse the ISO format date and convert to Odoo format
                    due_date = datetime.fromisoformat(card_due.replace('Z', '+00:00'))
                    task_vals['date_deadline'] = due_date.strftime('%Y-%m-%d %H:%M:%S')
                except (ValueError, TypeError):
                    _logger.warning("Invalid date format for card %s: %s", card_name, card_due)
            
            if not task:
                task = task_model.create(task_vals)
                tasks_count += 1
                _logger.info("Created task: %s in stage %s", card_name, stage_mapping.get(list_id, 'Unknown'))
            else:
                task.write(task_vals)
                tasks_count += 1
                _logger.info("Updated task: %s", card_name)
            
            # Process attachments for this card
            if 'attachments' in card and card['attachments']:
                for attachment in card['attachments']:
                    if attachment.get('isUpload'):
                        attachment_url = attachment.get('url')
                        filename = attachment.get('name', f'attachment_{attachment["id"]}')
                        self._download_and_attach_file(task, attachment_url, filename)
        
        return {
            'projects_count': projects_count,
            'tasks_count': tasks_count
        }
