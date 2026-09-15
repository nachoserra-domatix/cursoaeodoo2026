from odoo import models, fields

class RealEstateProperty(models.Model):
    _name = "realestate.property"
    _description = "Property"
    
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    image_1920 = fields.Image("Image", max_width=1920, max_height=1920)
    price = fields.Float(string="Price", default=0.0)
    bedrooms = fields.Integer(string="Bedrooms", default=0)
    bathrooms = fields.Integer(string="Bathrooms", default=0)
    garage = fields.Integer(string="Garage", default=0)
    external_url = fields.Char(string="External URL")
    active = fields.Boolean(string="Active", default=True)
    property_type_id = fields.Many2one('realestate.domain', 'Property Type', domain=[('code', '=', 'real_estate_type')], index=True)
    date_register = fields.Date(string="Date Register", default=fields.Date.today())
    