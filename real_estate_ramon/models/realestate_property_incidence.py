from odoo import models, fields

class RealEstatePropertyIncidence(models.Model):
    _name = "realestate.property.incidence"
    _description = "Property Incidence"

    sequence = fields.Integer(string="Sequence", default=10)
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    priority = fields.Selection(
        selection = [
            ("0", "Low"),
            ("1", "Normal"),
            ("2", "High"),
            ("3", "Very High"),
        ],
        string="Priority",
        default="0",
    )

    state = fields.Selection(
        selection = [
            ("new", "New"),
            ("in_progress", "In Progress"),
            ("done", "Done"),
            ("canceled", "Canceled"),
        ],
        string="Status",
        default="new",
        required=True
    )

    datetime = fields.Datetime(
        string="Date and Time",
        default=fields.Datetime.now,
    )

    user_id =  fields.Many2one(
        comodel_name="res.users",
        string="Assigned User",
    )

    property_id = fields.Many2one(
        comodel_name="realestate.property",
        string="Property",
        required=True,
        ondelete="cascade",
    )