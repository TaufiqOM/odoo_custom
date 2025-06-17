{
    'name': 'IT Custom Tear Sheet',
    'version': '1.0',
    'summary': 'Add Tear Sheet tab to product form',
    'description': 'Custom module to add a Tear Sheet tab in product form view',
    'author': 'Your Name',
    'website': 'https://yourwebsite.com',
    'category': 'Inventory',
    'depends': ['product', 'documents'],
    'data': [
        'views/product_template_tear_sheet_views.xml',
        'views/product_image_multi.xml',
        'views/product_documents_selection_wizard_views.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
