{
    'name': 'Real Estate David',
    'summary': '''Módulo de Real Estate''',  
    'description': '''Módulo para gestionar propiedades, clientes y ventas de bienes raíces.''',
    
    'author': 'ENDEOS',
    'website': 'https://www.endeos.com',
    'license': 'Other proprietary',
    'category': 'ENDEOS / Customizations',
    'application': True,
    
    'depends': ['base'],
    'version': '1.5',

    'data': [
        'security/real_estate_security.xml',
        'security/ir.model.access.csv',
        'views/realestate_property_views.xml',
        'views/realestate_visit_views.xml',
        'views/realestate_category_views.xml',
        'views/realestate_offer_views.xml',
        'views/realestate_contract_views.xml',
        'views/realestate_menuitems.xml',
    ],
}