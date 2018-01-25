{
    'name': 'Point of Sale Cart Print',
    'version': '1.0',
    'category': 'Point of Sale',
    'summary': 'Print Orderline of Point of Sale ',
    'description': """

=======================

This module allows the print orderline.

""",
    'depends': ['base', 'point_of_sale',  ],
    'data': [
        'views/cart_inherit.xml',
        'views/orderline_report_menu.xml',
        'views/orderline_template.xml',


        # 'data/product_sequence.xml',
        # 'views/pos_discount_templates.xml'
    ],
    'qweb': [
        'static/src/xml/cart.xml',
    ],
    'installable': True,
    # 'website': 'https://www.odoo.com/page/point-of-sale',
}