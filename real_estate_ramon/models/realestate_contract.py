from odoo import models, fields, api

class RealEstateContract(models.Model):
    _name = "realestate.contract"
    _description = "realestate.property"

    name = fields.Char(string="Name", required=True)
    type = fields.Selection(
        selection=[
            ("rent", "Rent"),
            ("sale", "Sale"),
        ],
        string="Type",
        default="sale",
    )
    
    property_id = fields.Many2one(
        comodel_name="realestate.property",
        string="Property",
        required = "True",
    )

    resident = fields.Many2one(
        comodel_name="res.partner",
        string="User",
    )

    user_id = fields.Many2one(
        comodel_name="res.users",
        string="User",
    )

    begin_date = fields.Datetime(string="Begin Date")

    end_date = fields.Datetime(string="End Date")

    duration = fields.Integer(string="Duration (Days)",
        compute="_compute_duration",
        store =  True)

    remaining_days = fields.Integer(string="Remaining Days",
        compute="_compute_days_remaining")

    active_days = fields.Integer(string="Active Days",
        compute="_compute_active_days")
 
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
    )

    rent = fields.Monetary(
        string="Rent",
        currency_field="currency_id",
    )

    bail = fields.Monetary(
        string="Bail",
        currency_field="currency_id",
    )

    has_bail = fields.Boolean(string="Bailed Contract",
        compute="_compute_has_bail"
    )
    
    status = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("scheduled", "Scheduled"),
            ("done", "Done"),
            ("canceled", "Canceled"),
        ],
        string="Status",
        default="draft",
    )

    @api.depends('begin_date', 'end_date')
    def _compute_duration(self):
        for record in self:
            if record.begin_date and record.end_date:
                record.duration = (record.end_date - record.begin_date).days
            else:
                record.duration = 0

    def _compute_days_remaining(self):
        for record in self:
            if record.end_date:
                record.remaining_days = (record.end_date - fields.Date.today()).days
            else:
                record.remaining_days = 0

    def _compute_active_days(self):
        for record in self:
            if record.begin_date:
                record.active_days = (fields.Date.today() - record.begin_date.date()).days
            else:
                record.active_days = 0

    def _compute_has_bail(self):
        for record in self:
            if record.bail > 0:
                record.has_bail = True
            else:
                record.has_bail = False

    def action_draft(self):
        self.status = 'draft'

    def action_scheduled(self):
        self.status = 'scheduled'

    def action_done(self):
        self.status = 'done'

    def action_canceled(self):
        self.status = 'canceled'