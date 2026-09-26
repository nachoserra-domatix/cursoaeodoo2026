from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class RealEstateOffer(models.Model):
    _name = "realestate.offer"
    _description = "Real Estate Offer"
    _order = "date desc, id desc"
    _rec_name = "property_id"

    property_id = fields.Many2one(
        comodel_name="estate.property",
        string="Property",
        required=True,
        domain=[("availability_state", "=", True)],
    )
    buyer_id = fields.Many2one(
        comodel_name="res.partner",
        string="Buyer",
        required=True,
    )
    amount = fields.Float(string="Amount", compute="_compute_amount", store=True, required=True)
    date = fields.Date(string="Date", required=True, default=fields.Date.today)
    property_resp = fields.Many2one(
        comodel_name="res.users",
        string="Property Responsible",
        related="property_id.id_user",
        readonly=True,
    )
    
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("sent", "Sent"),
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
        ],
        string="State",
        default="draft",
        required=True,
    )
    notes = fields.Text(string="Notes")

    def write(self, vals):
        res = super().write(vals)
        if "state" in vals:
            if vals["state"] == "accepted":
                self.property_id.action_mark_reserved()
            elif vals["state"] == "draft":
                self.property_id.action_mark_available()
        return res

    def action_mark_sent(self):
        for record in self:
            record.state = "sent"
        return True

    def action_mark_accepted(self):
        for record in self:
            record.state = "accepted"
        return True

    def action_accept(self):
        return self.action_mark_accepted()

    def action_create_contract(self):
        self.ensure_one()
        today = fields.Date.today()
        contract = self.env["realestate.contract"].create(
            {
                "name": f"Contract - {self.property_id.name}",
                "contract_type": "sale",
                "property_id": self.property_id.id,
                "tenant_id": self.buyer_id.id,
                "start_date": today,
                "end_date": today,
                "rent": 0.0,
                "deposit": 0.0,
            }
        )
        return {
            "type": "ir.actions.act_window",
            "name": "Real Estate Contract",
            "res_model": "realestate.contract",
            "res_id": contract.id,
            "view_mode": "form",
            "view_id": self.env.ref("rsr.estate_contract_view_form").id,
        }

    def action_mark_rejected(self):
        for record in self:
            record.state = "rejected"
        return True

    def action_mark_draft(self):
        for record in self:
            record.state = "draft"
        return True

    @api.depends("property_id.price")
    def _compute_amount(self):
        for record in self:
            record.amount = record.property_id.price

    @api.constrains("amount", "property_id")
    def _check_amount_positive(self):
        for record in self:
            if record.amount < 0:
                raise ValidationError(_("The offer amount cannot be negative."))
