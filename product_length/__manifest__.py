{
    'name' : 'Product Length',
    'version' : '1.1',
    
    'category': 'Sales',
    
    'depends' : ['base_setup', 'sale', 'account', 'product',],
    'data': [
            'views/views.xml',
            'views/sale_report_inherit_template.xml',
        
    ],
    
        
   
    'installable': True,
    'application': True,
    
}
