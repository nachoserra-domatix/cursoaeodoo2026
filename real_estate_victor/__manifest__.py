# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Real Estate - Victor",
    "version": "19.0.1.0.1",
    "category": "Custom",
    "author": "Víctor León",
    "license": "AGPL-3",
    "depends": [
        "base",],
    "data": [
        'data/ir_cron.xml',
        'security/realestate_security.xml',
        'security/ir.model.access.csv',
        'views/realestate_property_view.xml',
        'views/realestate_visit_view.xml',
        'views/realestate_category_view.xml',
        'views/realestate_offer_view.xml',
        'views/realestate_contract_view.xml',
        'wizard/realestate_property_change_stage_views.xml',
        'wizard/realestate_visit_lot_create_views.xml',
        'views/realestate_menuitems.xml',
        ],
    "installable": True,
}
