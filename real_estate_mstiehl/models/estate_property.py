from odoo import models, fields, api, _
from datetime import datetime
from datetime import timedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property"
    _order = "date_register desc"
    _rec_name = "name"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    
    name = fields.Char(string="Name", required=True, tracking=True)
    property_ref_code = fields.Char(string="Property Code", store=True, tracking=True, readonly=True)    
    description = fields.Text(string="Description", tracking=True)
    image_1920 = fields.Image("Primary Image", max_width=1920, max_height=1920)
    cunstruction_year = fields.Integer(string="Construction Year", tracking=True)
    
    seller_id = fields.Many2one(comodel_name="res.partner", string="Seller", tracking=True)
    agent_id = fields.Many2one(comodel_name="res.partner", string="Agent", tracking=True)
    
    google_maps_url = fields.Char(string="Google Maps URL")
    postcode = fields.Char(string="Postcode", tracking=True)
    address = fields.Char(string="Address", tracking=True)
    country_id = fields.Many2one(comodel_name="res.country", string="Country", default=1, tracking=True)
    # city_id = fields.Many2one(comodel_name="res.city", string="City", tracking=True)
    # address fields
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    country_code = fields.Char(related='country_id.code', string="Country Code")
    partner_latitude = fields.Float(string='Geo Latitude', digits=(10, 7))
    partner_longitude = fields.Float(string='Geo Longitude', digits=(10, 7))
    expected_price = fields.Float(string="Expected Price", default=0.0, tracking=True)
    selling_price = fields.Float(string="Selling Price", default=0.0, readonly=True, tracking=True)
    
    total_area = fields.Float(string="Total Area", default=0.0, tracking=True)
    living_area = fields.Integer(string="Living Area", default=0, tracking=True)
    bedrooms = fields.Integer(string="Bedrooms", default=0, tracking=True)
    bathrooms = fields.Integer(string="Bathrooms", default=0, tracking=True)
    garage = fields.Integer(string="Garage", default=0, tracking=True)
    garden = fields.Integer(string="Garden", default=0, tracking=True)
    garden_orientation = fields.Selection(selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')], string="Garden Orientation", default='north', tracking=True)
    garden_area = fields.Float(string="Garden Area", default=0.0, tracking=True)
    
    external_url = fields.Char(string="External URL")
    
    property_type_id = fields.Many2one(comodel_name="estate.property.type", string="Property Type", tracking=True)
    
    date_register = fields.Date(string="Date Register", default=fields.Date.today())
    date_sold = fields.Date(string="Date Sold", readonly=True)
        
    tags_ids = fields.Many2many(comodel_name="estate.tag", string="Tags")
    gallery_ids = fields.One2many(comodel_name="estate.property.gallery", inverse_name="property_id", string="Gallery")
    contacts_ids = fields.One2many(comodel_name="estate.property.contacts", inverse_name="property_id", string="Contacts")
    
    active = fields.Boolean(string="Active", default=True, tracking=True)
    available = fields.Boolean(string="Available", default=True, tracking=True)
    
    user_id = fields.Many2one(comodel_name="res.users", string="User", default=lambda self: self.env.user)
                
    @api.model_create_multi
    def create(self, vals_list):
        context = self._context
        vals_list[0]["property_ref_code"] = f"PROP#{(datetime.today()).strftime('%y%m%d%H%M%S')}"            
        return super(EstateProperty, self).create(vals_list)

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    
    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    active = fields.Boolean(string="Active", default=True)
        

class EstatePropertyGallery(models.Model):
    _name = "estate.property.gallery"
    _description = "Estate Property Gallery"
    
    name = fields.Char(string="Name", required=True)
    description = fields.Char(string="Description")
    property_id = fields.Many2one(comodel_name="estate.property", string="Property")
    image = fields.Image("Image", max_width=1920, max_height=1920)
    
    
class EstatePropertyContacts(models.Model):
    _name = "estate.property.contacts"
    _description = "Estate Property Contacts"
    
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner")
    property_id = fields.Many2one(comodel_name="estate.property", string="Property")
    role_id = fields.Many2one(comodel_name="estate.property.contacts.role", string="Role")
    

class EstatePropertyContactsRole(models.Model):
    _name = "estate.property.contacts.role"
    _description = "Estate Property Contacts Role"
    
    name = fields.Char(string="Name", required=True)
