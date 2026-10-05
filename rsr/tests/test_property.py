from datetime import timedelta

from odoo import fields
from odoo.tests.common import TransactionCase


class TestEstateProperty(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.property_record = cls.env["estate.property"].create(
            {
                "name": "Demo",
                "reference": "TEST-DEMO-022",
                "price": 9002.0,
            }
        )
        cls.buyer = cls.env["res.partner"].create({"name": "Test Buy"})

    def test_create_visit(self):
        action = self.property_record.create_visit()
        visit = self.env["estate.property.visit"].browse(action["res_id"])

        self.assertTrue(action["res_id"])
        self.assertEqual(visit.property_id, self.property_record)

    def test_action_accept_best_offer(self):
        offer = self.env["realestate.offer"].create(
            {
                "property_id": self.property_record.id,
                "buyer_id": self.buyer.id,
                "state": "sent",
            }
        )

        self.property_record.action_accept_best_offer()
        self.assertEqual(offer.state, "accepted")
        self.assertFalse(self.property_record.availability_state)
        self.assertTrue(
            any(
                "The best offer was accepted" in message.body
                for message in self.property_record.message_ids
            )
        )

    def test_compute_next_visit_date(self):
        now = fields.Datetime.to_datetime(fields.Datetime.now()).replace(
            microsecond=0
        )
        expected = now + timedelta(days=2)
        self.env["estate.property.visit"].create(
            [
                {
                    "property_id": self.property_record.id,
                    "date": now + timedelta(days=5),
                    "state": "planned",
                },
                {
                    "property_id": self.property_record.id,
                    "date": expected,
                    "state": "planned",
                },
                {
                    "property_id": self.property_record.id,
                    "date": now + timedelta(days=1),
                    "state": "new",
                },
            ]
        )

        self.assertEqual(self.property_record.next_visit_date, expected)