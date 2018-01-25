{
    'name': 'Point of Sale Item Number',
    'version': '1.0',
    'category': 'Point of Sale',
    'summary': 'Simple Discounts in the Point of Sale ',
    'description': """

=======================

This module allows the cashier to quickly give a percentage
sale discount to a customer.

""",
    'depends': ['base', 'point_of_sale'],
    'data': [
        'views/item.xml',

        # 'data/product_sequence.xml',
        # 'views/pos_discount_templates.xml'
    ],
    'qweb': [
        'static/src/xml/item.xml',
    ],
    'installable': True,
    # 'website': 'https://www.odoo.com/page/point-of-sale',
}