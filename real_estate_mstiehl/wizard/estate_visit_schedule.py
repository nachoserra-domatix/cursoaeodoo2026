from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class EstateVisitSchedule(models.TransientModel):
    _name = "estate.visit.schedule"
    _description = "Estate Visit Schedule"

    listing_ids = fields.Many2many(comodel_name="estate.listing", string="Listings", required=True, default=lambda self: self.env.context.get("active_ids"))
    listing_id = fields.Many2one(comodel_name="estate.listing", string="Listing", compute="_compute_listing_id")
    property_id = fields.Many2one(comodel_name="estate.property", string="Property", related="listing_id.property_id", readonly=True)
    agent_id = fields.Many2one(comodel_name="res.users", string="Responsible", compute="_compute_agent_id", store=True, readonly=False)
    visitor_id = fields.Many2one(comodel_name="res.partner", string="Visitor")
    date_start = fields.Datetime(string="Start", required=True, default=fields.Datetime.now)
    date_end = fields.Datetime(string="End", required=True)
    note = fields.Text(string="Note")

    @api.depends("listing_ids")
    def _compute_listing_id(self):
        for wizard in self:
            wizard.listing_id = wizard.listing_ids[:1]

    @api.depends("listing_ids")
    def _compute_agent_id(self):
        for wizard in self:
            listing = wizard.listing_ids[:1]
            wizard.agent_id = listing.property_id.agent_id or listing.agent_id

    @api.constrains("date_start", "date_end")
    def _check_dates(self):
        for wizard in self:
            if wizard.date_end < wizard.date_start:
                raise ValidationError(_("The end date must be after the start date."))

    def action_schedule_visit(self):
        self.ensure_one()
        visits = self.env["estate.property.visit"]
        for listing in self.listing_ids:
            visits |= self.env["estate.property.visit"].create({
                "listing_id": listing.id,
                "visitor_id": self.visitor_id.id,
                "agent_id": self.agent_id.id,
                "date": self.date_start,
                "date_end": self.date_end,
                "note": self.note,
            })
        visits.action_confirmed()
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Visits Scheduled"),
                "message": _("%d visit(s) were scheduled successfully.", len(visits)),
                "type": "success",
                "sticky": False,
                "next": {"type": "ir.actions.act_window_close"},
            },
        }
