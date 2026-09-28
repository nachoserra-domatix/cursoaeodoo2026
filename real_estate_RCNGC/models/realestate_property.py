from odoo import models, fields, api  


class RealEstateProperty(models.Model):
    _name = 'realestate.property'
    _description = 'Real Estate Property'

    # Defaults


    # Attributes (fields)
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    price = fields.Float(string="Price")
    reference = fields.Char(string="Reference")
    availability = fields.Boolean(string="Availability", default=True)
    color = fields.Integer(string="Color")


    # Relations M2O (Many2one)
    category_id = fields.Many2one(
        comodel_name="realestate.category",
        string="Category",
    )

    user_id = fields.Many2one(
        comodel_name="res.users",
        string="User",
        default=lambda self: self.env.user.id
    )

    stage_id = fields.Many2one(
        comodel_name="realestate.property.stage",
        string="Stage",
        group_expand="_read_group_stage_ids"
    )

    # Relations O2M (One2many)
    image_ids = fields.One2many(
        comodel_name='realestate.property.image',
        inverse_name='property_id',
        string='Images'
    )

    visit_ids = fields.One2many(
        comodel_name='realestate.visit',
        inverse_name='property_id',
        string='Visits'
    )

    incident_ids = fields.One2many(
        comodel_name='realestate.property.incident',
        inverse_name='property_id',
        string='Incidents'
    )

    offer_ids = fields.One2many(
        comodel_name='realestate.offer',
        inverse_name='property_id',
        string='Offers'
    )


    # Computed fields
    next_visit_date = fields.Datetime(
        string="Next Visit Date", 
        compute='_compute_next_visit_date', 
        store=True
        )

    visit_count = fields.Integer(
        string="Visit Count",
        compute='_compute_visit_count',
    )

    incident_count = fields.Integer(    
        string="Incident Count",
        compute='_compute_incident_count',
    )

    # Compute methods
    @api.depends('visit_ids.date', 'visit_ids.state')
    def _compute_next_visit_date(self):
        for property in self:
            next_visit = self.env['realestate.visit'].search(
                [('property_id', '=', property.id), ('state', '=', 'scheduled')], 
                order='date asc', limit=1)
            property.next_visit_date = next_visit.date if next_visit else False 

    def _compute_visit_count(self):     
        for property in self:
            property.visit_count = len(property.visit_ids) 

    def _compute_incident_count(self):
        for property in self:
            property.incident_count = len(property.incident_ids)

    # Other methods
    def _read_group_stage_ids(self, stages, domain):
        return self.env['realestate.property.stage'].search([], order='sequence')


    # Constraints
    _reference_uniq = models.Constraint(
        'unique(reference)',
        'The reference must be unique.',      
    )    

    # Actions
    def action_reserve(self):
        self.availability = False
  
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

    def action_create_offer(self):
        vals = {
            'property_id': self.id,
            'amount': self.price,
        }
        offer = self.env['realestate.offer'].create(vals)
        offer.action_send()

    def action_cancel_pending_visits(self):
        pending_vists = self.env['realestate.visit'].search([
            ('property_id', '=', self.id),
            ('state', 'in', ['draft', 'scheduled']),
        ])
        pending_vists.write({
            'state': 'canceled',
        })

    def action_open_visits(self):   
        return {    
            'type': 'ir.actions.act_window',    
            'name': 'Visits',
            'res_model': 'realestate.visit',
            'view_mode': 'list,form',   
            'domain': [('property_id', '=', self.id)],
            'context': {'default_property_id': self.id},
        }

    def action_open_incidents(self):    
        return {    
            'type': 'ir.actions.act_window',    
            'name': 'Incidents',
            'res_model': 'realestate.property.incident',
            'view_mode': 'list,form',   
            'domain': [('property_id', '=', self.id)],
            'context': {'default_property_id': self.id},
        }
                
            