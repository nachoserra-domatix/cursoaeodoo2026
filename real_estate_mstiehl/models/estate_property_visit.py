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
    visitor_phone = fields.Char(string="Visitor Phone", related="visitor_id.phone", store=True, readonly=True)
    date = fields.Datetime(string="Date", default=lambda self: datetime.now())
    note = fields.Text(string="Note")
    agent_id = fields.Many2one(comodel_name="res.users", string="Agent", default=lambda self: self.env.user)
    user_id = fields.Many2one(comodel_name="res.users", string="User", default=lambda self: self.env.user)
    date_confirmed = fields.Date(string="Date Confirmed", readonly=True)
    date_done = fields.Date(string="Date Done", readonly=True)
    date_canceled = fields.Date(string="Date Canceled", readonly=True)
    stage_id = fields.Many2one(comodel_name="estate.stage", string="Stage", domain="[('type_id.code','=','visit')]", group_expand='_read_group_stage_ids', tracking=True)
    stage_id_code = fields.Char(string="Stage Code", related="stage_id.code", store=True, readonly=True)
    color = fields.Integer(string="Color Index", default=0)
    
    def _read_group_stage_ids(self, stages, domain):
        return self.env['estate.stage'].search([('type_id.code', '=', 'visit')])
        
    def action_done(self):
        for record in self:
            record.stage_id = self.env['estate.stage'].search([('type_id.code', '=', 'visit'), ('code', '=', 'done')], limit=1)
            record.date_done = fields.Date.today()
            
    def action_canceled(self):
        for record in self:
            record.stage_id = self.env['estate.stage'].search([('type_id.code', '=', 'visit'), ('code', '=', 'canceled')], limit=1)
            record.date_canceled = fields.Date.today()
    
    def action_confirmed(self):
        for record in self:
            record.stage_id = self.env['estate.stage'].search([('type_id.code', '=', 'visit'), ('code', '=', 'confirmed')], limit=1)
            record.date_confirmed = fields.Date.today()
    
    def action_draft(self):
        for record in self:
            record.stage_id = self.env['estate.stage'].search([('type_id.code', '=', 'visit'), ('code', '=', 'draft')], limit=1)
            record.date_confirmed = False