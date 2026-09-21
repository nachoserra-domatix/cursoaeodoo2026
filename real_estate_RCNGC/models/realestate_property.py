from odoo import models, fields

class RealEstateProperty(models.Model):
    _name = 'realestate.property'
    _description = 'Real Estate Property'

    name = fields.Char(string='Property Name')
    description = fields.Text(string='Description')

