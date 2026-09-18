from odoo import models, fields, api, _
from datetime import datetime
from datetime import timedelta

class EstateVisit(models.Model):
    _name = "estate.property.visit"
    _description = "Estate Property Visit"
    
    name = fields.Char(string="Name", required=True, default=lambda self: f"Visit-{(datetime.today()).strftime('%y%m%d%H%M%S')}")
    listing_id = fields.Many2one(comodel_name="estate.listing", string="Listing")
    property_id = fields.Many2one(comodel_name="estate.property",string="Property",related="listing_id.property_id",store=True,readonly=True)
    visitor_id = fields.Many2one(comodel_name="res.partner", string="Visitor")
    date = fields.Date(string="Date", default=fields.Date.today())
    note = fields.Text(string="Note")
    agent_id = fields.Many2one(comodel_name="res.users", string="Agent", default=lambda self: self.env.user)
    user_id = fields.Many2one(comodel_name="res.users", string="User", default=lambda self: self.env.user)
    state = fields.Selection(selection=[('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done', 'Done'), ('canceled', 'Canceled')], string="State", default="draft")
    date_confirmed = fields.Date(string="Date Confirmed", readonly=True)
    date_done = fields.Date(string="Date Done", readonly=True)
    date_canceled = fields.Date(string="Date Canceled", readonly=True)
    
    def action_done(self):
        for record in self:
            record.state = "done"
            record.date_done = fields.Date.today()
            
    def action_canceled(self):
        for record in self:
            record.state = "canceled"
            record.date_canceled = fields.Date.today()
    
    def action_confirmed(self):
        for record in self:
            record.state = "confirmed"
            record.date_confirmed = fields.Date.today()
    
    def action_draft(self):
        for record in self:
            record.state = "draft"