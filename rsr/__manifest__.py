{
    "name": "Estate Jnc 2",  # Jnc 
    "version": "19.0.3",  # Version
    "application": True,
    "depends": ["base"],  
    "data": [
        # security
        'security/estate_security.xml',
        'security/ir.model.access.csv',

        # temaplates
        'templates/estate_property_action.xml',
        'templates/estate_property_view.xml',
        'templates/estate_category_action.xml',
        'templates/estate_category_view.xml',
        'templates/estate_property_stage_action.xml',
        'templates/estate_property_stage_view.xml',
        'templates/estate_contract_action.xml',
        'templates/estate_contract_view.xml',
        'templates/estate_offer_action.xml',
        'templates/estate_offer_view.xml',
        'templates/estate_property_visit_action.xml',
        'templates/estate_property_visit_view.xml',

        # root menu
        'templates/estate_menu_root.xml',
    ],
    "installable": True,
    'license': 'LGPL-3',
}
