from odoo import fields, models

class RealEstateCategory(models.Model):
    _name = "realestate.category"
    _description = "Real Estate Category"
    _order = "name"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
