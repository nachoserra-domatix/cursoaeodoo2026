from odoo import models, fields, api, _


class EstateOwner(models.Model):
    _name = "estate.owner"
    _description = "Estate Owner"
    _inherits = {"res.partner": "partner_id"}
    _rec_name = "name"

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Related Partner",
        required=True,
        ondelete="cascade",
    )
    notes = fields.Text(string="Owner Notes")
    property_ids = fields.One2many(
        comodel_name="estate.property",
        inverse_name="owner_id",
        string="Real Estate Properties",
    )
    property_count = fields.Integer(string="Number of Properties", compute="_compute_property_count")

    @api.depends("property_ids")
    def _compute_property_count(self):
        for record in self:
            record.property_count = len(record.property_ids)

    def action_view_properties(self):
        self.ensure_one()
        return {
            "name": _("Properties"),
            "type": "ir.actions.act_window",
            "res_model": "estate.property",
            "view_mode": "list,form",
            "domain": [("owner_id", "=", self.id)],
            "context": {"default_owner_id": self.id},
        }
