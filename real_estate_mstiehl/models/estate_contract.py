from odoo import models, fields, api, _
from datetime import datetime
from datetime import timedelta

class EstateContract(models.Model):
    _name = "estate.contract"
    _description = "Estate Contract"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "contract_ref_code"
    
    name = fields.Char(string="Name", required=True, default="New")
    listing_id = fields.Many2one(comodel_name="estate.listing", string="Listing", tracking=True)
    property_id = fields.Many2one(comodel_name="estate.property",string="Property",related="listing_id.property_id",store=True,readonly=True)
    contract_ref_code = fields.Char(string="Contract Code", store=True, tracking=True, readonly=True, default="New")
    offer_id = fields.Many2one(comodel_name="estate.listing.offer", string="Offer", tracking=True)
    type_id = fields.Many2one(comodel_name="estate.contract.type", string="Type")
    description = fields.Text(string="Description", tracking=True)
    seller_id = fields.Many2one(comodel_name="res.partner", string="Seller", tracking=True)
    buyer_ids = fields.One2many(comodel_name="estate.contract.buyer", inverse_name="contract_id", string="Buyers")
    agent_id = fields.Many2one(comodel_name="res.users", string="Agent", tracking=True)
    expected_price = fields.Float(string="Expected Price", default=0.0, tracking=True)
    price = fields.Float(string="Price", default=0.0, readonly=True, tracking=True)
    state = fields.Selection(selection=[('draft', 'Draft'), ('published', 'Published'), ('signed', 'Signed'), ('canceled', 'Canceled')], string="State", default="draft")
    date_register = fields.Date(string="Date Register", default=fields.Date.today())
    date_published = fields.Date(string="Date Published", readonly=True)
    date_signed = fields.Date(string="Date Signed", readonly=True)
    date_canceled = fields.Date(string="Date Canceled", readonly=True)
    date_start = fields.Date(string="Start Date", default=fields.Date.today())
    date_end = fields.Date(string="End Date")
    active = fields.Boolean(string="Active", default=True)
    tags_ids = fields.Many2many(comodel_name="estate.tag", string="Tags")
    
    @api.model_create_multi
    def create(self, vals_list):
        context = self._context
        val_ref = f"CONT#{(datetime.today()).strftime('%y%m%d%H%M%S')}"  
        vals_list[0]["contract_ref_code"] = val_ref          
        vals_list[0]["name"] = val_ref
        return super(EstateContract, self).create(vals_list)
    
class EstateContractType(models.Model):
    _name = "estate.contract.type"
    _description = "Estate Contract Type"
    
    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    active = fields.Boolean(string="Active", default=True)
    
class EstateContractBuyers(models.Model):
    _name = "estate.contract.buyer"
    _description = "Estate Contract Buyer"
    _rec_name = "contract_id"
    
    contract_id = fields.Many2one(comodel_name="estate.contract", string="Contract")
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner")
    notes = fields.Text(string="Notes")
    numerator = fields.Integer(string="Numerator", default=1)
    denominator = fields.Integer(string="Denominator", default=1)
    total_share = fields.Float(string="Total", compute="_compute_total_share")
    
    @api.depends('numerator', 'denominator')
    def _compute_total_share(self):
        for record in self:
            record.total_share = record.numerator / record.denominator