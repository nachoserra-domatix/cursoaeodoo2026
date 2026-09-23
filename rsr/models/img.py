from odoo import fields, models

class RealestatePropertyImage(models.Model):
    _name = "estate.property.image"
    _description = "Property Image"
    _order = "sequence, id"

    name = fields.Char(string="Name", required=True)
    image = fields.Image(string="Image", required=True)
    sequence = fields.Integer(string="Sequence", default=10, index=True)
    property_id = fields.Many2one(
        comodel_name="estate.property",
        string="Property",
        required=True,
        ondelete="cascade",
    )

