from odoo import models, fields


class RealEstateVisitWizard(models.TransientModel):
    _name = "realestate.visit.wizard"
    _description = "Create Visits"

    property_id = fields.Many2one(
        comodel_name="realestate.property",
        string="Property",
        required=True,
    )

    date_start = fields.Date(
        string="Start Date",
        required=True,
    )

    date_end = fields.Date(
        string="End Date",
        required=True,
    )

    def action_create_visits(self):
        current_date = self.date_start

        while current_date <= self.date_end:
            self.env["realestate.visit"].create({
                "property_id": self.property_id.id,
                "datetime": current_date,
                "user_id": self.property_id.user_id.id,
                "status": "scheduled",
            })

            current_date = fields.Date.add(current_date, days=1)

        return {"type": "ir.actions.act_window_close"}

    