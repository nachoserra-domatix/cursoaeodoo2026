from odoo import models, fields

class RealestatePropertyImage(models.Model):
    _name = 'realestate.property.image'
    _description = 'Real Estate Property Image'

    # Attributes (fields)
    sequence = fields.Integer(string='Sequence', default=10)
    name = fields.Char(string='Image Name', default="Image ", required=True)
    description = fields.Text(string='Description')
    image = fields.Binary(string='Image', required=True)
    
    # Relations M2O (Many2one)
    property_id = fields.Many2one(
        comodel_name='realestate.property', 
        string='Property', 
        ondelete='cascade')

    