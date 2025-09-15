{
    'name': 'ITCustom Portal',
    'version': '1.0',
    'category': 'Project',
    'summary': 'Modify portal visibility to restrict internal users to invited only',
    'description': 'This module modifies the portal privacy visibility option to allow access only to invited portal users and invited internal users (followers/collaborators).',
    'author': 'Your Name',
    'depends': ['project', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/project_rules.xml',
        'views/project_views.xml',
    ],
    'installable': True,
    'application': False,
}
