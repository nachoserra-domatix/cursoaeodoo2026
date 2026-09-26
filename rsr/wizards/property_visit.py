from datetime import datetime, time, timedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class EstatePropertyVisitWizard(models.TransientModel):
    _name = "estate.property.visit.wizard"
    _description = "Create Estate Property Visits"

    date_from = fields.Date(
        string="From",
        required=True,
        default=fields.Date.context_today,
    )
    date_to = fields.Date(
        string="To",
        required=True,
        default=fields.Date.context_today,
    )

    @api.onchange("date_from")
    def onchange_date_from(self):
        if self.date_from and (not self.date_to or self.date_to < self.date_from):
            self.date_to = self.date_from

    @api.constrains("date_from", "date_to")
    def check_date_range(self):
        for wizard in self:
            if wizard.date_from and wizard.date_to and wizard.date_to < wizard.date_from:
                raise ValidationError(_("The end date cannot be earlier than the start date."))

    def action_apply(self):
        properties = self.env["estate.property"].browse(
            self.env.context.get("active_ids", [])
        ).exists()
        if not properties:
            raise ValidationError(_("Select at least one property."))
        if self.date_to < self.date_from:
            raise ValidationError(_("The end date cannot be earlier than the start date."))

        visit_values = []
        current_date = self.date_from
        while current_date <= self.date_to:
            visit_datetime = fields.Datetime.to_string(
                datetime.combine(current_date, time.min)
            )
            visit_values.extend(
                {
                    "property_id": property_record.id,
                    "user_id": property_record.id_user.id,
                    "date": visit_datetime,
                    "state": "planned",
                }
                for property_record in properties
            )
            current_date += timedelta(days=1)

        self.env["estate.property.visit"].create(visit_values)
        return {"type": "ir.actions.act_window_close"}
