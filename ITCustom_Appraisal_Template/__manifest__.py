{
    'name': 'Appraisal Template',
    'version': '1.0',
    'depends': ['hr_appraisal'],
    'category': 'Human Resources',
    'summary': 'Manage Templates for Appraisal',
    'description': 'Add configuration menu for appraisal templates',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/appraisal_template_views.xml',
    ],
    'installable': True,
    'application': False,
}
