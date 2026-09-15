{
    'name': 'Real Estate MSTIEHL',
    'version': '19.0.1.0.0',
    'summary': 'Real Estate MSTIEHL',
    'description': '',
    'author': 'Marco Stiehl',
    'website': '',
    'license': 'LGPL-3',
    'depends': ['base'],
    "data": [
        "security/ir.model.access.csv",
        "views/property_views.xml",
        "views/domain_views.xml",
        "menu/menu.xml"
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}