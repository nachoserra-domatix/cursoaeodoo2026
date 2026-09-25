from odoo import models, fields

class RealEstateOffer(models.Model):
    _name = "realestate.offer"
    _description = "offer"

    property_id = fields.Many2one(
        comodel_name="realestate.property",
        string="Property",
        required="True",
        domain="[('availability', '=', True), ('category_id', '=', category_id)]",
    )

    buyer = fields.Many2one(
        comodel_name="res.partner",
        string="Buyer",
    )

    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
    )

    amount = fields.Monetary(
        string="Amount",
        currency_field="currency_id",
    )

    date = fields.Datetime(string="Offer Date")

    status = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("sent", "Sent"),
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
        default="draft",
    )

    notes = fields.Text(string="Notes")

    responsable_id = fields.Many2one(comodel_name="res.users", string="Responsable", related="property_id.user_id", store=True)

    category_id = fields.Many2one(
        comodel_name="realestate.category",
        string="Category",
        related="property_id.category_id",
        readonly=True,
    )

    def action_send(self):
        self.status = 'sent'

    def action_accept(self):
        self.status = 'accepted'
        self.property_id.action_reserve()

        self.env["realestate.contract"].create({
            "name": f"Contract - {self.property_id.name}",
            "property_id": self.property_id.id,
            "resident": self.buyer.od,
            "type": "sale",
            "begin_date": fields.Datetime.now(),
            "status": "draft",
        })

    def action_refuse(self):
        self.status = 'refused'

    def action_draft(self):
        self.status = 'draft'