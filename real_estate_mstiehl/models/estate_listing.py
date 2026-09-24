from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime
from datetime import timedelta

class EstateListing(models.Model):
    _name = "estate.listing"
    _description = "Estate Listing"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_register desc"
    rec_name = "listing_ref_code"
    
    name = fields.Char(string="Name", required=True, default="New")
    property_id = fields.Many2one(comodel_name="estate.property", string="Property", tracking=True)
    listing_ref_code = fields.Char(string="Listing Code", store=True, tracking=True, readonly=True)
    type_id = fields.Many2one(comodel_name="estate.contract.type", string="Type")
    description = fields.Text(string="Description", tracking=True)
    seller_id = fields.Many2one(comodel_name="res.partner", string="Seller", tracking=True)
    agent_id = fields.Many2one(comodel_name="res.users", string="Agent", tracking=True)
    expected_price = fields.Float(string="Expected Price", default=0.0, tracking=True)
    selling_price = fields.Float(string="Selling Price", default=0.0, readonly=True, tracking=True)
    state = fields.Selection(selection=[('draft', 'Draft'), ('published', 'Published'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('reserved', 'Reserved'), ('sold', 'Sold'), ('canceled', 'Canceled')], string="State", default="draft", group_expand="_expand_states")
    color = fields.Integer(string="Color", default=0)
    property_image = fields.Image(string="Property Image", related="property_id.image_1920")
    date_register = fields.Date(string="Date Register", default=fields.Date.today())
    date_published = fields.Date(string="Date Published", readonly=True)
    date_offer_received = fields.Date(string="Date Offer Received", readonly=True)
    date_offer_accepted = fields.Date(string="Date Offer Accepted", readonly=True)
    date_reserved = fields.Date(string="Date Reserved", readonly=True)
    date_sold = fields.Date(string="Date Sold", readonly=True)
    date_canceled = fields.Date(string="Date Canceled", readonly=True)
    external_url = fields.Char(string="External URL")
    active = fields.Boolean(string="Active", default=True)
    tags_ids = fields.Many2many(comodel_name="estate.tag", string="Tags")
    offer_ids = fields.One2many(comodel_name="estate.listing.offer", inverse_name="listing_id", string="Offers")
    visit_ids = fields.One2many(comodel_name="estate.property.visit", inverse_name="listing_id", string="Visits")
    contract_ids = fields.One2many(comodel_name="estate.contract", inverse_name="listing_id", string="Contracts")
    contract_count = fields.Integer(string="Contract Count", compute="_compute_contract_count")

    user_id = fields.Many2one(comodel_name="res.users", string="User", default=lambda self: self.env.user)
    
    next_visit_date = fields.Datetime(string="Next Visit Date", readonly=True, compute="_compute_next_visit_date", store=True)
    num_pending_visits = fields.Integer(string="Number of Pending Visits", compute="_compute_next_visit_date", store=True)
    
    

    @api.depends('visit_ids.stage_id', 'visit_ids.date')
    def _compute_next_visit_date(self):
        today = fields.Datetime.to_datetime(fields.Date.today())
        for record in self:
            if not record._origin.id:
                record.next_visit_date = False
                continue
            next_visit = self.env['estate.property.visit'].search([
                ('listing_id', '=', record._origin.id),
                ('stage_id_code', '=', 'confirmed'),
                ('date', '>=', today),
            ], order='date asc', limit=1)
            record.next_visit_date = next_visit.date
            
    
    @api.depends('visit_ids.stage_id', 'visit_ids.date')
    def _compute_num_pending_visits(self):
        for record in self:
            pending_visits = self.env['estate.property.visit'].search([
                ('listing_id', '=', record._origin.id),
                ('stage_id_code', 'in', ('confirmed', 'draft')),
            ])
            record.num_pending_visits = len(pending_visits)

    def _expand_states(self, states, domain):
        return [key for key, _label in self._fields['state'].selection]

    @api.depends('contract_ids')
    def _compute_contract_count(self):
        for record in self:
            record.contract_count = len(record.contract_ids)

    def action_view_contract(self):
        self.ensure_one()
        action = {
            "name": _("Contract"),
            "type": "ir.actions.act_window",
            "res_model": "estate.contract",
            "context": {"default_listing_id": self.id},
        }
        if len(self.contract_ids) == 1:
            action["view_mode"] = "form"
            action["res_id"] = self.contract_ids.id
        else:
            action["view_mode"] = "list,form"
            action["domain"] = [("listing_id", "=", self.id)]
        return action
    
    @api.model_create_multi
    def create(self, vals_list):
        context = self._context
        val_ref = f"LIST#{(datetime.today()).strftime('%y%m%d%H%M%S')}"
        vals_list[0]["listing_ref_code"] = val_ref
        vals_list[0]["name"] = val_ref
        return super(EstateListing, self).create(vals_list)

    def action_reserved(self):
        for record in self:
            record.state = "reserved"
            record.date_reserved = fields.Date.today()

    def action_sold(self):
        for record in self:
            record.state = "sold"
            record.date_sold = fields.Date.today()
            record._create_contract()

    def _create_contract(self):
        self.ensure_one()
        accepted_offer = self.offer_ids.filtered(lambda o: o.state == "accepted")[:1]
        self.env["estate.contract"].create({
            "listing_id": self.id,
            "property_id": self.property_id.id,
            "offer_id": accepted_offer.id,
            "type_id": self.type_id.id,
            "description": self.description,
            "seller_id": self.seller_id.id,
            "agent_id": self.agent_id.id,
            "expected_price": self.expected_price,
            "price": accepted_offer.price if accepted_offer else self.selling_price,
            "tags_ids": [(6, 0, self.tags_ids.ids)],
            "buyer_ids": [(0, 0, {
                "partner_id": accepted_offer.partner_id.id,
                "numerator": 1,
                "denominator": 1,
            })] if accepted_offer else [],
        })
        
    def action_create_visit(self):
        self.ensure_one()
        try:
            self.env["estate.property.visit"].create({
                "date": fields.Date.today(),
                "listing_id": self.id,
            })
        except Exception as error:
            raise UserError(_("The visit could not be created: %s", error)) from error
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Visit Created"),
                "message": _("The visit was created successfully."),
                "type": "success",
                "sticky": False,
            },
        }
        
    def action_cancel_all_visits(self):
        self.ensure_one()
        canceled = self.browse()
        try:
            for record in self:
                visits_to_cancel = self.env["estate.property.visit"].search([("listing_id", "=", record.id), ("stage_id_code", "not in", ["done", "canceled"])])
                visits_to_cancel.action_canceled()
                canceled |= record
        except Exception as error:
            raise UserError(_("The visits could not be canceled: %s", error)) from error
        if not canceled:
            raise UserError(_("No visit was found to cancel."))
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Visits Canceled"),
                "message": _("All visits were canceled successfully."),
                "type": "success",
                "sticky": False,
            },
        }

    def action_accept_best_offer(self):
        accepted = self.browse()
        try:
            for record in self:
                best_offer = self.env["estate.listing.offer"].search(
                    [("listing_id", "=", record.id), ("state", "=", "submitted")],
                    order="price desc", limit=1,
                )
                if best_offer:
                    best_offer.action_accepted()
                    accepted |= record
        except Exception as error:
            raise UserError(_("The best offer could not be accepted: %s", error)) from error
        if not accepted:
            raise UserError(_("No submitted offer was found to accept."))
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Offer Accepted"),
                "message": _("The best offer was accepted successfully."),
                "type": "success",
                "sticky": False,
            },
        }


class EstateListingOffer(models.Model):
    _name = "estate.listing.offer"
    _description = "Estate Listing Offer"
    _rec_name = "listing_id"
    
    listing_id = fields.Many2one(comodel_name="estate.listing", string="Listing")
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner")
    price = fields.Float(string="Price", default=0.0)
    valid = fields.Boolean(string="Valid", default=True)
    valid_until = fields.Date(string="Date Valid", default=fields.Date.today() + timedelta(days=7))
    active = fields.Boolean(string="Active", default=True)
    property_id = fields.Many2one(comodel_name="estate.property", string="Property", related="listing_id.property_id", store=True, readonly=True)
    agent_id = fields.Many2one(comodel_name="res.users", string="Agent", related="listing_id.agent_id", store=True, readonly=True)
    color = fields.Integer(string="Color", default=0)
    state = fields.Selection(selection=[('submitted', 'Submitted'), ('in_analysis', 'In Analysis'),('accepted', 'Accepted'), ('refused', 'Refused'), ('expired', 'Expired')], string="State", default="submitted", group_expand="_expand_states")
    date = fields.Date(string="Date", default=fields.Date.today())
    date_in_analysis = fields.Date(string="Date In Analysis")
    date_accepted = fields.Date(string="Date Accepted")
    date_refused = fields.Date(string="Date Refused")
    date_expired = fields.Date(string="Date Expired")
    
    user_id = fields.Many2one(comodel_name="res.users", string="User", default=lambda self: self.env.user)

    def _expand_states(self, states, domain):
        return [key for key, _label in self._fields['state'].selection]

    @api.model_create_multi
    def create(self, vals_list):
        records = super(EstateListingOffer, self).create(vals_list)
        for record in records:
            if record.listing_id.state in ("draft", "published"):
                record.listing_id.state = "offer_received"
                record.listing_id.date_offer_received = fields.Date.today()
        return records

    def action_in_analysis(self):
        for record in self:
            record.state = "in_analysis"
            record.date_in_analysis = fields.Date.today()
            
    def action_accepted(self):
        for record in self:
            record.state = "accepted"
            record.date_accepted = fields.Date.today()
            other_offers = record.listing_id.offer_ids - record
            other_offers.filtered(lambda o: o.state not in ("refused", "expired")).action_refused()
            record.listing_id.selling_price = record.price
            record.listing_id.state = "offer_accepted"
            record.listing_id.date_offer_accepted = fields.Date.today()
    
    def action_refused(self):
        for record in self:
            record.state = "refused"
            record.date_refused = fields.Date.today()
            
    def action_expired(self):
        for record in self:
            record.state = "expired"
            record.date_expired = fields.Date.today()