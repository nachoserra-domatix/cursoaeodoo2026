from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class RealEstateContract(models.Model):
    _name = "realestate.contract"
    _description = "Real Estate Contract"
    _order = "start_date desc, id desc"
    _rec_name = "name"

    name = fields.Char(string="Name", required=True)
    _name_unique = models.Constraint(
        "UNIQUE(name)",
        "The contract name must be unique.",
    )
    contract_type = fields.Selection(
        selection=[
            ("rental", "Rental"),
            ("sale", "Sale"),
        ],
        string="Type",
        required=True,
    )
    property_id = fields.Many2one(
        comodel_name="estate.property",
        string="Property",
        required=True,
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        related="property_id.currency_id",
        readonly=True,
    )
    tenant_id = fields.Many2one(
        comodel_name="res.partner",
        string="Tenant",
        required=True,
    )
    start_date = fields.Date(
        string="Start Date",
        required=True,
        default=fields.Date.today
    )
    end_date = fields.Date(string="End Date", required=True)
    rent = fields.Monetary(
        string="Rent", required=True, currency_field="currency_id"
    )
    deposit = fields.Monetary(
        string="Deposit", required=True, currency_field="currency_id"
    )
    days_between = fields.Integer(compute="_compute_days", string="Duration (Days)")
    duration_d = fields.Integer(compute="_compute_duration", string="Duration (Days)")
    has_deposit = fields.Boolean(compute="_compute_has_deposit", store=True, string="With Deposit")
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("in_progress", "In Progress"),
            ("finished", "Finished"),
            ("cancelled", "Cancelled"),
        ],
        string="State",
        default="draft",
        required=True,
    )

    @api.constrains("start_date", "end_date")
    def _check_date_order(self):
        for record in self:
            if (
                record.start_date
                and record.end_date
                and record.end_date < record.start_date
            ):
                raise ValidationError(_("The end date cannot be earlier than the start date."))

    @api.onchange("property_id")
    def _onchange_property_id(self):
        for record in self:
            record.rent = record.property_id.price if record.property_id else 0.0

    @api.depends("start_date", "end_date")
    def _compute_duration(self):
        for record in self:
            if record.start_date and record.end_date:
                record.duration_d = (record.end_date - record.start_date).days
            else:
                record.duration_d = 0
                
    def _compute_days(self):
        date_today = fields.Date.today()
        for record in self:
            if record.start_date:
                record.days_between = (date_today - record.start_date).days
            else:
                record.days_between = 0

    @api.depends("deposit")
    def _compute_has_deposit(self):
        for record in self:
            record.has_deposit = record.deposit > 0

    def action_mark_in_progress(self):
        for record in self:
            record.state = "in_progress"
        return True

    @api.model
    def _cron_contract_date(self):
        expired_contracts = self.search(
            [
                ("state", "=", "in_progress"),
                ("end_date", "<", fields.Date.today()),
            ]
        )
        expired_contracts.write({"state": "finished"})

    def action_mark_finished(self):
        for record in self:
            record.state = "finished"
        return True

    def action_mark_cancelled(self):
        for record in self:
            record.state = "cancelled"
        return True

    def action_mark_draft(self):
        for record in self:
            record.state = "draft"
        return True
