from odoo import models, fields

class RealestatePropertyIncident(models.Model):
    _name = 'realestate.property.incident'
    _description = 'Property Incident'


    # ---------------------------------------------------------------------------------------
    # Attributes (fields)
    # ---------------------------------------------------------------------------------------
    sequence = fields.Integer(string='Sequence', default=10)
    name = fields.Char(string='Incident Name', required=True)
    description = fields.Text(string='Description')
    incident_priority = fields.Selection(
        string='Incident Priority',
        selection=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('critical', 'Critical')],
        default='medium'
    )
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('in_progress', 'In Progress'), ('resolved', 'Resolved'), ('closed', 'Closed')],
        default='new'
    )
    date_time_reported = fields.Datetime(string='Date Time Reported', default=fields.Datetime.now)


    # ---------------------------------------------------------------------------------------
    # Relations M2O (Many2one)  
    # ---------------------------------------------------------------------------------------
    property_id = fields.Many2one(
        comodel_name='realestate.property', 
        string='Property', 
        ondelete='cascade')
    
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Assigned to',
        ondelete='set null')
    
