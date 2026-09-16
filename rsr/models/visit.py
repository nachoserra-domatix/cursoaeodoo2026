from odoo import fields, models


class EstatePropertyVisit(models.Model):
    _name = "estate.property.visit"
    _description = "Estate Property Visit"
    _order = "date desc"

    property_id = fields.Many2one(comodel_name="estate.property", string="Property")
    date = fields.Datetime(string="Date")
    contact_id = fields.Many2one(comodel_name="res.partner", string="Contact")
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("planned", "Planned"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ],
        string="State",
        default="new",
    )
