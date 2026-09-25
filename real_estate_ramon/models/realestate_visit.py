from odoo import models, fields

class RealEstateVisit(models.Model):
    _name = "realestate.visit"
    _description = "Visit"
    _rec_name = "property_id"

    property_id = fields.Many2one(
        comodel_name="realestate.property",
        string="Property",
        required="True",
    )

    datetime = fields.Datetime(string="Visit Date")

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="User",
    )

    user_id = fields.Many2one(
        comodel_name="res.users",
        string="User",
    )
    
    status = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("scheduled", "Scheduled"),
            ("done", "Done"),
            ("canceled", "Canceled"),
        ],
        string="State",
        default="draft",
    )

    phone_number = fields.Char(string="Phone Number", related='partner_id.phone', readonly= False, store=True)

    email = fields.Char(string="Email", related='partner_id.email', store="True")

    def action_draft(self):
        self.status = "draft"

    def action_schedule(self):
        self.status = "scheduled"

    def action_done(self):
        self.status = "done"

    def action_cancel(self):
        self.status = "canceled"