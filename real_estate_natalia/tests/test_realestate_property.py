from odoo.tests import common
from odoo import fields
from datetime import timedelta

class TestRealEstateProperty(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.property = self.env['realestate.property'].create({
            'name': 'property_1',
            'price': 100000})
        self.now = fields.Datetime.now()

    def test_compute_next_visit_date(self):
        tomorrow = fields.Datetime.now() + timedelta(days=1)

        # Sin visitas
        self.assertFalse(self.property.next_visit_date)

        # Creo una visita confirmada para mañana
        visit = self.env['realestate.visit'].create({
                'property_id': self.property.id,
                'date': tomorrow,
                'state': 'confirmed'
                })

        # Ahora la próxima visita es mañana y está confirmada
        self.assertEqual(self.property.next_visit_date, tomorrow)
        self.assertEqual(visit.state, 'confirmed')
    
    def test_action_create_visit(self):
        self.property.action_create_visit()
        self.assertEqual(len(self.property.visit_ids), 1)

    def test_action_accept_best_offer(self):
        offer_1 = self.env['realestate.offer'].create({
            'property_id': self.property.id, 'amount': 95000, 'state': 'sent'})
        offer_2 = self.env['realestate.offer'].create({
            'property_id': self.property.id, 'amount': 97000, 'state': 'sent'})

        self.property.action_accept_best_offer()

        self.assertEqual(offer_2.state, 'accepted')
        self.assertEqual(offer_1.state, 'sent')
        self.assertFalse(self.property.availability)
