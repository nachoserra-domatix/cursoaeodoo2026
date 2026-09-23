from odoo import api, fields, models

class EstatePropertyIncidence(models.Model):
    _name = "estate.property.incidence"
    _description = "Estate Property Incidence"
    _order = "sequence, date desc"

    sequence = fields.Integer(string="Sequence", default=10, index=True)
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    priority = fields.Selection(
        selection=[
            ("0", "None"),
            ("1", "Low"),
            ("2", "Medium"),
            ("3", "High"),
        ],
        string="Priority",
        default="0",
    )
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("in_progress", "In Progress"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ],
        string="State",
        default="new",
        required=True,
    )
    date = fields.Datetime(string="Date", default=fields.Datetime.now, required=True)
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Assigned User",
        default=lambda self: self.env.user,
    )
    property_id = fields.Many2one(
        comodel_name="estate.property",
        string="Property",
        required=True,
        ondelete="cascade",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("user_id") and vals.get("property_id"):
                property_record = self.env["estate.property"].browse(
                    vals["property_id"]
                )
                vals["user_id"] = property_record.id_user.id
        return super().create(vals_list)