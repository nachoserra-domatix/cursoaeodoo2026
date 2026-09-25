from odoo import models, fields

class RealEstatePropertyStage(models.Model):
    _name = "realestate"
    _description = "Property Stage"

    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer(string="Sequence", default=10)