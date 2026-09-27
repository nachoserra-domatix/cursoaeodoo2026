from odoo import models, fields

class RealEstateOffer(models.Model):
    _name = "realestate.offer"
    _description = "Offer"
    _rec_name = "partner_id"

    #Atributos propios
    sequence = fields.Integer(string="Sequence")
    amount = fields.Float(string="Amount")
    date = fields.Datetime(string="Date")

    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('sent', 'Sent'),
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        string="State",
        default='draft',
    )
    color = fields.Integer(string="Color")
    note = fields.Html(string="Note")

    #Relaciones
    property_id = fields.Many2one(
        comodel_name="realestate.property",
        string="Property",
    )

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner",
    )

    user_id = fields.Many2one(
        comodel_name="res.users",
        string="User",
        related="property_id.user_id",
        readonly=True,
        store=True,
    )

    category_id = fields.Many2one(
        comodel_name="realestate.category",
        string="Category",
        related="property_id.category_id",
        readonly=True,
        store=True,
    )

    #Acciones
    def action_send(self):
        self.state = 'sent'

    def action_accept(self):
        self.state = 'accepted'
        self.property_id.action_reserve()

    def action_refuse(self):
        self.state = 'refused'

    def action_draft(self):
        self.state = 'draft'

    #Crea una UNICA oferta individual como contrato
    def create_contract(self):
        self.ensure_one()
        return self.env['realestate.contract'].create({
            'partner_id': self.partner_id.id,
            'property_id': self.property_id.id,
            'start_date': fields.Date.today(),
            'contract_type': 'sale',
        })