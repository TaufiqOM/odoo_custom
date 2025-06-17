{
    'name': 'IT Custom Inventory',
    'version': '1.0',
    'summary': 'Custom Inventory Rules and Features',
    'description': """
        Modul kustom untuk aturan dan fitur inventory khusus
        Termasuk record rule untuk membatasi akses produk
    """,
    'author': 'Your Name',
    'website': 'https://yourwebsite.com',
    'category': 'Inventory',
    'depends': ['stock', 'product'],
    'data': [
        'security/inventory_security.xml',
        'views/product_template_tear_sheet_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
