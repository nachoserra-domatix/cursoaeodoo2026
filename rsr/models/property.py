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

    @api.model_create_multi
    def create(self, vals_list):
        first_stage = self.env["realestate.property.stage"].search(
            [], order="sequence, id", limit=1
        )
        for vals in vals_list:
            if "stage_id" not in vals and first_stage:
                vals["stage_id"] = first_stage.id
        return super().create(vals_list)

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = 0.0

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