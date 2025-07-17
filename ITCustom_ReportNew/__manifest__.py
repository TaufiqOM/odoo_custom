{
    'name': 'IT Custom Report',
    'version': '1.0',
    'summary': 'Custom PDF Report',
    'description': 'Generate custom PDF reports',
    'author': 'Your Name',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/menu_views.xml',
        'reports/custom_report_template.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'ITCustom_ReportNew/static/src/js/custom_report.js',
        ],
    },
    'installable': True,
    'application': True,
}
