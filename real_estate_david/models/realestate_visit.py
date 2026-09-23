from odoo import models, fields

class RealEstateVisit(models.Model):
    _name = 'realestate.visit'
    _description = 'Visit'
    _rec_name = 'property_id'

    property_id = fields.Many2one(
        comodel_name='realestate.property', 
        string='Property',
        required=True,
    )
    
    date = fields.Datetime(string='Visit Date')
    
    partner_id = fields.Many2one(
        comodel_name='res.partner', 
        string='Visitor'
    )
    
    user_id = fields.Many2one(
        comodel_name='res.users', 
        string='Salesperson'
    )
    
    phone = fields.Char(string='Phone', related='partner_id.phone', readonly=False)
    
    email = fields.Char(string='Email', related='partner_id.email')
    
    state = fields.Selection([
            ('draft', 'Draft'),
            ('scheduled', 'Scheduled'),
            ('done', 'Done'),
            ('canceled', 'Canceled')
        ], 
        string='State', 
        default='draft', 
        group_expand=True
    )

    def action_draft(self):
        self.state = 'draft'

    def action_scheduled(self):
        self.state = 'scheduled'
        # self.write({'state': 'scheduled'})
        
    def action_done(self):
        self.state = 'done'
    
    def action_canceled(self):
        self.state = 'canceled'