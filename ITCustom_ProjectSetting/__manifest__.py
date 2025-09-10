{
    'name': 'ITCustom Project Setting',
    'version': '1.0',
    'category': 'Project',
    'summary': 'Add custom privacy visibility option to projects',
    'description': 'This module adds a new privacy visibility option "Invited Only" to the project model.',
    'author': 'Your Name',
    'depends': ['project'],
    'data': [
            'security/ir.model.access.csv',
            'security/project_rules.xml',
            'views/project_views.xml',
            ],
    'installable': True,
    'application': False,
}
