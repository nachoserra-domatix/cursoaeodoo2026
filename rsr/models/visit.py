from odoo import fields, models


class EstatePropertyVisit(models.Model):
    _name = "estate.property.visit"
    _description = "Estate Property Visit"
    _order = "sequence, date desc"
    _rec_name = "property_id"

    sequence = fields.Integer(string="Sequence", default=10, index=True)
    property_id = fields.Many2one(comodel_name="estate.property", string="Property")
    date = fields.Datetime(string="Date")
    contact_id = fields.Many2one(comodel_name="res.partner", string="Contact")
    user_id = fields.Many2one(comodel_name="res.users", string="User")
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("new", "New"),
            ("planned", "Planned"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ],
        string="State",
        default="new",
    )

    def action_mark_done(self):
        for record in self:
            record.state = "done"
        return True

    def action_mark_cancelled(self):
        for record in self:
            record.state = "cancelled"
        return True

    def action_mark_draft(self):
        for record in self:
            record.state = "draft"
        return True

    def action_mark_new(self):
        for record in self:
            record.state = "new"
        return True

    def action_mark_planned(self):
        for record in self:
            record.state = "planned"
        return True
