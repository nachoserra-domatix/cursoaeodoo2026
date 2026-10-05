from odoo import fields, models

class RealEstateOwner(models.Model):
    _name = "realestate.owner"
    _description = "Real Estate Owner"
    _inherits = {"res.partner": "partner_id"}

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Contact",
        required=True,
        ondelete="cascade",
    )
