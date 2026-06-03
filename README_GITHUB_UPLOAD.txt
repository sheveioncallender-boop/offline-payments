{
    'name': 'SPX Cash on Delivery',
    'version': '2.0.0',
    'category': 'Payments',
    'summary': 'Cash on Delivery rules and settings for Odoo',
    'description': 'Adds Cash on Delivery configuration fields, eligibility rules, country limits, product/customer exclusions, and fee settings.',
    'author': 'Spxcorp Limited',
    'depends': ['payment', 'website_sale', 'sale', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/payment_provider_views.xml',
        'views/product_template_views.xml'
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3'
}
