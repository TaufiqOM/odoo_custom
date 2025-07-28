{
    'name': 'Custom Appraisal Skills',
    'version': '1.0',
    'summary': 'Add custom skill groups to appraisals',
    'description': """
        Allows creating custom skill groups like "Cemara", "Anggrek" in appraisals
    """,
    'author': 'Your Name',
    'depends': ['hr_appraisal', 'hr_appraisal_skills'],
    'data': [
        'security/ir.model.access.csv',
        'views/appraisal_skill_views.xml',
    ],
    'js': ['static/src/js/appraisal_skill.js'],
    'installable': True,
    'application': True,
}