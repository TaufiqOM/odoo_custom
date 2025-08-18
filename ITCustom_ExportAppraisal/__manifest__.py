# -*- coding: utf-8 -*-
{
    'name': 'IT Custom Export Appraisal',
    'version': '1.0',
    'summary': 'Tambahkan tombol Export Laporan pada hr.appraisal',
    'description': 'Module untuk menambahkan tombol Export Laporan di form hr.appraisal',
    'author': 'IT Team',
    'category': 'Human Resources',
    'depends': ['hr_appraisal'],
    'data': [
        'views/hr_appraisal_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
