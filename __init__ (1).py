{
    'name': 'SPX Cash on Delivery',
    'version': '1.0.1',
    'category': 'Payments',
    'summary': 'Cash on Delivery settings foundation for Odoo',
    'description': 'Custom Cash on Delivery settings foundation for Odoo website checkout.',
    'author': 'SPX',
    'depends': ['payment', 'website_sale'],
    'data': [
        'views/payment_provider_views.xml'
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
