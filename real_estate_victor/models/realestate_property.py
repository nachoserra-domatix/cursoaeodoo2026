# -*- coding: utf-8 -*-

from odoo import models, fields, api

class RealEstateProperty(models.Model):
    _name = 'realestate.property'
    _description = 'RealEstateProperty'

    active = fields.Boolean(string="Active", default=True)
    name = fields.Char(string='Property')
    desc = fields.Char(string='Description')
    size = fields.Float(string='Size')
    user_id = fields.Many2one(comodel_name="res.users", string="Manager", default=lambda self: self.env.user.id)
    category_id = fields.Many2one(comodel_name="realestate.category", string="Category")

    price = fields.Monetary(string="Price", currency_field='currency_id')
    reference = fields.Char(string="Reference", copy=False)
    availability = fields.Boolean(string="Availability", default=True)

    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id.id
    )

    stage_id = fields.Many2one(
        comodel_name="realestate.property.stage",
        string="Stage",
        group_expand="_read_group_stage_ids"
    )

    image_ids = fields.One2many(
        comodel_name="realestate.property.image",
        inverse_name="property_id",
        string="Images"
    )

    visit_ids = fields.One2many(
        comodel_name="realestate.visit",
        inverse_name="property_id",
        string="Visits"
    )

    internal_note = fields.Text(string="Internal Note", company_dependent=True)
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.company.id
    )

    next_visit_date = fields.Datetime(
            string="Next visit date",
            compute="_compute_next_visit_date",
            inverse="_inverse_next_visit_date",
            store=True
        )

    incidence_ids = fields.One2many(
            comodel_name="realestate.property.incidence",
            inverse_name="property_id",
            string="Incidences"
        )

    offer_ids = fields.One2many(
            comodel_name="realestate.offer",
            inverse_name="property_id",
            string="Offers"
        )

    color = fields.Integer(string="Color")

    visit_count = fields.Integer(string="Visit Count", compute="_compute_visit_count")

    incidence_count = fields.Integer(string="Incidence Count", compute="_compute_incidence_count")

    _reference_uniq = models.Constraint(
        "unique(reference)",
        "The property reference must be unique."
    )

    def _inverse_next_visit_date(self):
        for record in self:
            if record.next_visit_date:
                scheduled_visits = record.visit_ids.filtered(lambda visit: visit.state == 'scheduled')
                if scheduled_visits:
                    scheduled_visits[0].date = record.next_visit_date

    def _compute_visit_count(self):
        for record in self:
            # visit_ids = len(self.env['realestate.visit'].search([('property_id', '=', record.id)]))
            # visit_ids = self.env['realestate.visit'].search_count([('property_id', '=', record.id)])
            record.visit_count = len(record.visit_ids)

    def _compute_incidence_count(self):
        for record in self:
            record.incidence_count = len(record.incidence_ids)


    @api.depends('visit_ids.date', 'visit_ids.status')
    def _compute_next_visit_date(self):
        for record in self:
            now = fields.Datetime.now()
            dates = record.visit_ids.filtered(
                lambda v: v.date and v.date > now and v.status == 'S'
            ).mapped('date')
            record.next_visit_date = min(dates) if dates else False

    def action_reserve(self):
        self.availability = False


    def _read_group_stage_ids(self, stages, domain):
        return self.env['realestate.property.stage'].search([], order='sequence')


    def action_create_visit(self):
        import pdb;pdb.set_trace()
        vals = {
            'property_id': self.id,
            'date': fields.Datetime.now(),
            'user_id': self.user_id.id
        }
        self.env['realestate.visit'].create(vals)


    def action_accept_best_offer(self):
        best_offer = self.env['realestate.offer'].search([('property_id', '=', self.id),('state', '=', 'sent')], order='amount desc', limit=1)
        if best_offer:
            best_offer.action_accept()


    def action_delete_refused_offers(self):
        refused_offers = self.env['realestate.offer'].search([('property_id', '=', self.id),('state', '=', 'refused')])
        refused_offers.unlink()


    def action_cancel_visits(self):
        visits = self.env['realestate.visit'].search([
            ('property_id', '=', self.id),
            ('status', 'in', ['P'])
        ])
        visits.write({'status': 'C'})

    def action_open_visits(self):
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Visits',
            'res_model': 'realestate.visit',
            'view_mode': 'kanban,list,form',
            'domain': [('property_id', '=', self.id)],
            'context': {'default_property_id': self.id}
        }
        return action

    def action_open_incidences(self):
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Incidences',
            'res_model': 'realestate.property.incidence',
            'view_mode': 'list,form',
            'domain': [('property_id', '=', self.id)],
            'context': {'default_property_id': self.id}
        }
        return action

    def action_create_offer(self):
        vals = {
            'property_id': self.id,
            'date': fields.Datetime.now(),
            'offer': self.price
        }
        self.env['realestate.offer'].create(vals)
