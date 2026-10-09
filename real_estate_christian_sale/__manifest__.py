{
    'name': 'Real Estate Christian Sale',
    'version': '1.0',
    'summary': 'Integracion de ventas para el modulo de inmobiliaria',
    'description': 'Vincula contratos inmobiliarios con pedidos de venta.',
    'author': 'Christian',
    'category': 'Real Estate',
    'license': 'LGPL-3',
    'depends': ['sale', 'real_estate_christian'],
    'data': [
        'data/ir_sequence.xml',
        'views/real_estate_contract_views.xml',
        'views/sale_order_views.xml',
    ],
    'application': False,
    'installable': True,
}
