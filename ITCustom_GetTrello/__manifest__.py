{
    'name': 'Get Trello',
    'version': '1.0',
    'depends': ['base', 'base_setup'],
    'category': 'Tools',
    'summary': 'Integration with Trello API',
    'description': 'Module untuk mengintegrasikan Odoo dengan Trello API',
    'data': [
        'views/config_settings_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'external_dependencies': {
        'python': ['requests'],
    },
}
