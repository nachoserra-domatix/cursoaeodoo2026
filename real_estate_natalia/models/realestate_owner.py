from odoo import models, fields

class RealEstateOwner(models.Model):
    _name="realestate.owner"
    _description="Owner"
    _inherits={"res.partner": "partner_id"}

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner",
        required=True,
        ondelete="cascade"
    )