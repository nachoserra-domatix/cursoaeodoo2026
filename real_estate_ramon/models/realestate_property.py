from odoo import models, fields

class RealEstateProperty(models.Model):
    _name = "realestate.property"
    _description = "Property"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    value = fields.Float(string="Value")
    area = fields.Float(string="Area")
    availability = fields.Boolean(string="Availability", default=True)
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="User",
    )
    category_id = fields.Many2one(
        comodel_name="realestate.category",
        string="Category",
    )

    image_ids = fields.One2many(
        comodel_name="realestate.property.image",
        inverse_name="property_id",
        string="Images"
    )

    incidences_ids = fields.One2many(
        comodel_name="realestate.property.incidence",
        inverse_name="property_id",
        string="Incidences",
    )

    offer_ids = fields.One2many(
        comodel_name="realestate.offer",
        inverse_name="property_id",
        string="Offers",
    )

    next_visit_date = fields.Datetime(
        string="Next Visit Date",
        compute="_compute_next_visit_date",
    )

    def action_reserve(self):
        self.availability = False

    def action_create_visit(self):

        vals = {
            "property_id": self.id,
            "datetime": fields.Datetime.now(),
            "user_id": self.env.user.id,
        }

        self.env["realestate.visit"].create(vals)

    def action_accept_best_offer(self):
        best_offer = self.env['realestate.offer'].search([('property_id', '=', self.id),('status', '=', 'sent')], order='amount desc', limit=1)
        if best_offer:
            best_offer.action_accept()

    def action_delete_refused_offers(self):
        refused_offers = self.env['realestate.offer'].search([('property_id', '=', self.id),('status', '=', 'refused')])
        refused_offers.unlink()

    def action_create_offer(self):
        vals = {
            'property_id': self.id,
            'amount': self.value,
        }
        offer = self.env['realestate.offer'].create(vals)
        offer.action_send()

    def _compute_next_visit_date(self):
        for property in self:
            visit = self.env["realestate.visit"].search([
                ("property_id", "=", property.id),
                ("status", "=", "scheduled"),
                ("datetime", "!=", False),
            ], order="datetime asc", limit=1)

            property.next_visit_date = visit.datetime if visit else False

    def action_cancel_visits(self):
        visits = self.env["realestate.visit"].search([
            ("property_id", "=", self.id),
            ("status", "in", ["draft", "scheduled"]),
        ])

        visits.write({"status": "canceled"})