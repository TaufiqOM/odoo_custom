# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    trello_board_id = fields.Char(
        string='Trello Board ID',
        help='ID of the Trello board this project is linked to'
    )
    
    trello_list_id = fields.Char(
        string='Trello List ID',
        help='ID of the Trello list this project represents'
    )


class ProjectTask(models.Model):
    _inherit = 'project.task'

    trello_card_id = fields.Char(
        string='Trello Card ID',
        help='ID of the Trello card this task is linked to'
    )
