# -*- coding: utf-8 -*-
{
    'name': 'HR Appraisal Custom Tab',
    'version': '18.0.1.0.0',
    'category': 'Human Resources/Appraisals',
    'summary': 'Menambahkan tab custom pada form appraisal',
    'description': """
        Module ini menambahkan tab baru pada form hr.appraisal
        dengan fitur tambahan untuk custom fields dan informasi
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['hr_appraisal'],
    'data': [
        'views/hr_appraisal_views.xml',
        'security/ir.model.access.csv',
    ],
    'test': [
        'tests/test_hr_appraisal_custom.py',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
