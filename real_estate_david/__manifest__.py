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
    'version': '1.10',

    'data': [
        'data/ir_cron.xml',
        'security/real_estate_security.xml',
        'security/ir.model.access.csv',
        'views/realestate_property_views.xml',
        'views/realestate_visit_views.xml',
        'views/realestate_category_views.xml',
        'views/realestate_offer_views.xml',
        'views/realestate_contract_views.xml',
        'views/realestate_menuitems.xml',
        'wizard/realestate_property_change_stage.xml',
        'wizard/realestate_property_create_visits.xml',
        'report/realestate_property_report.xml',
        'report/realestate_property_simple_report.xml',
        'report/realestate_contract_report.xml',
    ],
}