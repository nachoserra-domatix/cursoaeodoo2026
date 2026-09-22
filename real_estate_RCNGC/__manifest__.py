# pyright: reportUnusedExpression=false

{
    'name': 'Real Estate RCNGC',
    'version': '1.0.0',
    'summary': 'Real Estate Management Module',
    'description': 'Real Estate RCNGC',
    'author': 'RCNGC',
    'category': 'Real Estate',
    'depends': ['base'],
    'data': [
        'security/real_estate_security.xml',
        'security/ir.model.access.csv',
        'views/realestate_property_views.xml',
        "views/realestate_visit_views.xml",
        'views/realestate_menuitems.xml',
    ],
    'installable': True,
    'application': True
}