# -*- coding: utf-8 -*-
{
    'name': 'Custom Report Demo',
    'version': '1.0',
    'description': 'Demo module showing how to create custom reports in Odoo',
    'author': 'IT Team',
    'website': 'https://www.example.com',
    'depends': ['sale', 'base'],
    'data': [
        'security/ir.model.access.csv',
        'reports/custom_report_actions.xml',
        'reports/custom_report_template.xml',
        'reports/report_pre_shipping_template.xml',
        'views/custom_demo_views.xml',
        'data/demo_data.xml',
    ],
    'installable': True,
    'application': False,
}
