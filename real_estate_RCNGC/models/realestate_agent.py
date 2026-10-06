from odoo import models, fields, api    

class RealEstateAgent(models.Model):    
    _name = "realestate.agent"
    _description = "Real Estate Agent"
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner",
        required=True,
        ondelete="restrict"
    )

    commission = fields.Float(string="Commission %")  
