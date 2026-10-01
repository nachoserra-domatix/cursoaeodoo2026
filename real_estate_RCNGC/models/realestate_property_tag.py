from odoo import models, fields

class RealEstatePropertyTag(models.Model):
    _name = 'realestate.property.tag'
    _description = 'Real Estate Property Tag'

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color") 

    property_ids = fields.Many2many(
        comodel_name='realestate.property',
        relation='realestate_property_tag_rel',
        column1='tag_id',
        column2='property_id',
        string='Properties'
    )

