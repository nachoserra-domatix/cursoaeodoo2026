from odoo import models, fields

class RealEstateProperty(models.Model):
    _name = "realestate.property"
    _description = "Property"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    value = fields.Monetary(string="Value", currency_field="currency_id",)
    currency_id = fields.Many2one(comodel_name="res.currency", string="Currency")
    area = fields.Float(string="Area")
    availability = fields.Boolean(string="Availability", default=True)
    active = fields.Boolean(string="Active", default=True)
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

    visit_ids = fields.One2many(
        comodel_name="realestate.visit",
        inverse_name="property_id",
        string="Visits",
    )

    contract_ids = fields.One2many(
        comodel_name="realestate.contract",
        inverse_name="property_id",
        string="Contracts",
    )

    contract_count = fields.Integer(
        string="Contracts",
        compute="_compute_contract_count",
    )

    next_visit_date = fields.Datetime(
        string="Next Visit Date",
        compute="_compute_next_visit_date",
    )

    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        required=True,
    )

    internalnote = fields.Text(
        string="Internal Note",
        company_dependent=True,
    )

    stage_id = fields.Many2one(
        comodel_name="realestate",
        string="Stage",
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

    def action_view_incidences(self):
        return {
            "type": "ir.action.act_window",
            "name": "incidences",
            "res_model": "realestate.property.incidence",
            "view_mode": "list,form",
            "domain": [("property_id", "=", self.id)],
            "context": {
                "default_property_id": self.id,
            },
        }

    def _compute_contract_count(self):
        for property in self:
            property.contract_count = self.env["realestate.contract"].search_count([
                ("property_id", "=", property.id),
            ])

    def action_view_contracts(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Contracts",
            "res_model": "realestate.contract",
            "view_mode": "list, form",
            "domain": [("property_id", "=", self.id)],
            "context": {
                "default_property_id": self.id,
            },
        }