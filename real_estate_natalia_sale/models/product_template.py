from odoo import models, fields

class RealEstateProductTemplate(models.Model):
    _inherit = 'product.template'

    rental_ok = fields.Boolean(string="Rental")

    property_id = fields.Many2one(
        comodel_name="realestate.property",
        string="Property"
    )
    


