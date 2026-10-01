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
        "views/realestate_offer_views.xml",
        "views/realestate_category_views.xml",
        "views/realestate_contract_views.xml",
        'views/realestate_menuitems.xml',
        'wizard/realestate_property_change_stage.xml',
        'wizard/realestate_property_schedule_visits.xml',
        'wizard/realestate_visit_change_state.xml',
        'report/realestate_report_paperformats.xml',
        'report/realestate_property_report.xml',
        'report/realestate_properties_simple_report.xml',
        'report/realestate_contract_report.xml',
        'report/realestate_offer_report.xml',
        'data/ir_cron.xml',
    ],
    'installable': True,
    'application': True
}