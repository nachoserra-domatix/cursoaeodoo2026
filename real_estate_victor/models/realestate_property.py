# -*- coding: utf-8 -*-

from odoo import models, fields, api

class RealEstateProperty(models.Model):
    _name = 'realestate.property'
    _description = 'RealEstateProperty'

    name = fields.Char(string='Property')
    desc = fields.Char(string='Description')
    size = fields.Float(string='Size')
    user_id = fields.Many2one(comodel_name="res.users", string="Manager")
    category_id = fields.Many2one(comodel_name="realestate.category", string="Category")

    price = fields.Float(string="Price")
    reference = fields.Char(string="Reference")
    availability = fields.Boolean(string="Availability", default=True)

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

    next_visit_date = fields.Datetime(
            string="Next visit date",
            compute="_compute_next_visit_date"
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

    def action_create_offer(self):
        vals = {
            'property_id': self.id,
            'date': fields.Datetime.now(),
            'offer': self.price
        }
        self.env['realestate.offer'].create(vals)
