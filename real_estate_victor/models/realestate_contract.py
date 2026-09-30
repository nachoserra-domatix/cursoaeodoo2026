# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class RealEstateContract(models.Model):
    _name = 'realestate.contract'
    _description = 'RealEstateContract'

    name = fields.Char(string='Contract', copy=False)
    type = fields.Selection([('R', 'Rent'), ('S', 'Sale')], string='Type')
    property_id = fields.Many2one(
        comodel_name="realestate.property",
        string="Property",
        domain="[('availability', '=', False)]"
    )
    partner_id = fields.Many2one(comodel_name="res.partner", string="Tenant")
    start_date = fields.Date(string="Start Date", default=fields.Date.today)
    end_date = fields.Date(string='End date')
    rent = fields.Float(string='Rent')
    bail = fields.Float(string='Bail')
    status = fields.Selection([('D', 'Draft'), ('E', 'Ended'), ('C', 'Canceled'), ('O', 'Ongoing')], string='Status', default='D')

    duration_days = fields.Integer(string="Duration (Days)", compute="_compute_duration_days", store=True)

    days_to_end = fields.Integer(string="Days to End", compute="_compute_days_to_end")

    with_bail = fields.Boolean(string='Woth bail',compute='_compute_with_bail', store=True)
    ongoing_days = fields.Integer(string="Ongoing days", compute='_compute_ongoing_days')

    _name_uniq = models.Constraint(
        "unique(name)",
        "The contract name must be unique."
    )


    def action_draft(self):
        self.write({'status': 'D'})
        return True

    def action_ended(self):
        self.write({'status': 'E'})
        return True

    def action_canceled(self):
        self.write({'status': 'C'})
        return True

    def _cron_finish_contracts(self):
        contracts = self.env['realestate.contract'].search(
            [('end_date', '<', fields.Date.today()),
             ('status', '=', 'O')])
        contracts.write({'status': 'E'})


    def action_ongoing(self):
        self.write({'status': 'O'})
        return True

    @api.depends('bail')
    def _compute_with_bail(self):
        for record in self:
            if record.bail:
                record.with_bail = True
            else:
                record.with_bail = False

    def _compute_ongoing_days(self):
        for record in self:
            if record.start_date:
                record.ongoing_days = (fields.Date.today() - record.start_date).days
            else:
                record.ongoing_days = 0

    @api.onchange('property_id')
    def _onchange_property_id(self):
        if self.property_id:
            self.rent = self.property_id.price

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date and record.end_date < record.start_date:
                raise ValidationError(_("The end date cannot be earlier than the start date."))

    @api.depends('start_date', 'end_date')
    def _compute_duration_days(self):
        for record in self:
            if record.start_date and record.end_date:
                record.duration_days = (record.end_date - record.start_date).days
            else:
                record.duration_days = 0
    
    def _compute_days_to_end(self):
        for record in self:
            if record.end_date:
                record.days_to_end = (record.end_date - fields.Date.today()).days
            else:
                record.days_to_end = 0

