from odoo import _, api, fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    living_area = fields.Integer(string="Living Area (m²)")
    garden_area = fields.Integer(string="Garden Area (m²)")

    date_availability = fields.Date(
        copy=False,
        default=lambda self: fields.Date.add(fields.Date.today(), months=3),
        string="Available from",
    )
    price = fields.Float(string="Expected Price")
    selling_price = fields.Float(readonly=True, copy=False, string="Selling Price")

    total_area = fields.Integer(
        compute="_compute_total_area", store=True, string="Total Area (m²)"
    )
    best_price = fields.Float(
        compute="_compute_best_price", store=True, string="Best Offer"
    )
    next_visit_date = fields.Datetime(
        compute="_compute_next_visit_date",
        string="Next Visit Date",
    )

    availability_state = fields.Boolean(string="Available", default=True)

    id_user = fields.Many2one(
        comodel_name="res.users",
        string="User",
    )
    stage_id = fields.Many2one(
        comodel_name="realestate.property.stage",
        string="Stage",
    )
    category_id = fields.Many2one(
        comodel_name="realestate.category",
        string="Category",
    )
    incidence_ids = fields.One2many(
        comodel_name="estate.property.incidence",
        inverse_name="property_id",
        string="Incidences",
    )
    visit_ids = fields.One2many(
        comodel_name="estate.property.visit",
        inverse_name="property_id",
        string="Visits",
    )
    image_ids = fields.One2many(
        comodel_name="estate.property.image",
        inverse_name="property_id",
        string="Images",
    )
    offer_ids = fields.One2many(
        comodel_name="realestate.offer",
        inverse_name="property_id",
        string="Offers",
    )

    @api.model_create_multi
    def create(self, vals_list):
        first_stage = self.env["realestate.property.stage"].search(
            [], order="sequence, id", limit=1
        )
        for vals in vals_list:
            if "stage_id" not in vals and first_stage:
                vals["stage_id"] = first_stage.id
        return super().create(vals_list)
    
    def createVisit(self, vals):
        return self.create([vals])

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = 0.0

    @api.depends("visit_ids", "visit_ids.date", "visit_ids.state")
    def _compute_next_visit_date(self):
        now = fields.Datetime.now() 
        for record in self:
            planned_dates = record.visit_ids.filtered(
                lambda visit: visit.state == "planned"
                and visit.date
                and visit.date > now
            ).mapped("date")
            record.next_visit_date = min(planned_dates) if planned_dates else False

    @api.onchange("availability_state")
    def _onchange_availability_state(self):
        if not self.availability_state:
            self.action_mark_reserved()

    def action_mark_reserved(self):
        for record in self:
            record.availability_state = False
        return True

    def action_mark_available(self):
        for record in self:
            record.availability_state = True
        return True 

    def create_visit(self):
        self.ensure_one()
        visit = self.env["estate.property.visit"].create(
            {
                "property_id": self.id,
                "user_id": self.id_user.id,
                "date": fields.Datetime.now(),
            }
        )
        return {
            "type": "ir.actions.act_window",
            "name": "Property Visit",
            "res_model": "estate.property.visit",
            "res_id": visit.id,
            "view_mode": "form",
            "view_id": self.env.ref("rsr.estate_property_visit_view_form").id,
        }
    
    def action_accept_best_offer(self):
        self.ensure_one()
        best_offer = self.env["realestate.offer"].search(
            [
                ("property_id", "=", self.id),
                ("state", "=", "sent"),
            ],
            order="amount desc",
            limit=1,
        )
        if best_offer:
            best_offer.action_accept()
        return True

    def action_delete_rejected_offers(self):
        self.ensure_one()
        rejected_offers = self.env["realestate.offer"].search(
            [
                ("property_id", "=", self.id),
                ("state", "=", "rejected"),
            ]
        )
        rejected_offers.unlink()
        return True

    def action_cancel_open_visits(self):
        visits = self.env["estate.property.visit"].search(
            [
                ("property_id", "in", self.ids),
                ("state", "in", ["draft", "planned"]),
            ]
        )
        visits.write({"state": "cancelled"})
        return True


    def action_create_offer(self):
        self.ensure_one()
        offer = self.env["realestate.offer"].create(
            {
                "property_id": self.id,
                "buyer_id": self.env.user.partner_id.id,
                "amount": self.price,
                "state": "draft",
            }
        )
        return {
            "type": "ir.actions.act_window",
            "name": "Property Offer",
            "res_model": "realestate.offer",
            "res_id": offer.id,
            "view_mode": "form",
            "view_id": self.env.ref("rsr.estate_offer_view_form").id,
        }