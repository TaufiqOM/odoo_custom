# -*- coding: utf-8 -*-
{
    'name': 'Empty PDF Report',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Module to generate empty PDF report in new tab',
    'description': """
        Custom module that creates a menu item to open an empty PDF report in a new tab.
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu_views.xml',
        'report/empty_pdf_report.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
