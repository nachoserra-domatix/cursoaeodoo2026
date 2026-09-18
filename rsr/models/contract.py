from odoo import fields, models

class RealEstateContract(models.Model):
    _name = "realestate.contract"
    _description = "Real Estate Contract"
    _order = "start_date desc, id desc"
    _rec_name = "name"

    name = fields.Char(string="Name", required=True)
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
    tenant_id = fields.Many2one(
        comodel_name="res.partner",
        string="Tenant",
        required=True,
    )
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    rent = fields.Float(string="Rent", required=True)
    deposit = fields.Float(string="Deposit", required=True)
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

    def action_mark_in_progress(self):
        for record in self:
            record.state = "in_progress"
        return True

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
