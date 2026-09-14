{
    "name": "Estate Jnc 2",  # Jnc 
    "version": "19.0.0",  # Version
    "application": True,
    "depends": ["base"],  
    "data": [
        'security/ir.model.access.csv',
        'templates/estate_property_action.xml',

        # root menu
        'templates/estate_menu_root.xml',
    ],
    "installable": True,
    'license': 'LGPL-3',
}
