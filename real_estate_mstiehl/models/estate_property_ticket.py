from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime
from datetime import timedelta

class EstatePropertyTicket(models.Model):
    _name = "estate.property.ticket"
    _description = "Property Ticket"
    _order = "create_date desc"
    _rec_name = "name"

    name = fields.Char(string="Name", required=True, tracking=True, default="New")
    sequence = fields.Integer(string="Sequence", default=1)
    ticket_ref_code = fields.Char(string="Ticket Code", store=True, tracking=True, readonly=True, default="New")
    property_id = fields.Many2one(comodel_name="estate.property", string="Property", ondelete="cascade")
    responsible_id = fields.Many2one(comodel_name="res.users", string="Responsible", tracking=True)
    description = fields.Text(string="Description", required=True)
    ticket_type = fields.Selection([
        ("issue", "Issue"),
        ("request", "Request"),
        ("task", "Task")
    ], string="Ticket Type", default="issue", tracking=True)
    priority = fields.Selection([
        ("1", "Low"),
        ("2", "Medium"),
        ("3", "High"),
        ("4", "Urgent")
    ], string="Priority", default="1", tracking=True)
    state = fields.Selection([
        ("new", "New"),
        ("in_progress", "In Progress"),
        ("done", "Done"),
        ("canceled", "Canceled")
    ], string="State", default="new", tracking=True)
    date_new = fields.Datetime(string="Date New", default=fields.Datetime.now, readonly=True,tracking=True)
    date_in_progress = fields.Datetime(string="Date In Progress", readonly=True ,tracking=True)
    date_done = fields.Datetime(string="Date Done", readonly=True,tracking=True)
    date_canceled = fields.Datetime(string="Date Canceled", readonly=True,tracking=True)

    def action_done(self):
        self.write({"state": "done", "date_done": fields.Datetime.now()})

    def action_canceled(self):
        self.write({"state": "canceled", "date_canceled": fields.Datetime.now()})

    def action_in_progress(self):
        self.write({"state": "in_progress", "date_in_progress": fields.Datetime.now()})

    def action_new(self):
        self.write({"state": "new", "date_new": fields.Datetime.now()})
        
        
    def create(self, vals_list):
        context = self._context
        val_ref = f"TICKET#{(datetime.today()).strftime('%y%m%d%H%M%S')}"   
        vals_list[0]["ticket_ref_code"] = val_ref
        vals_list[0]["name"] = val_ref     
        return super(EstatePropertyTicket, self).create(vals_list)