from odoo.tests import common

class TestRealEstateProperty(common.TransactionCase):
   def setUp(self):
      super().setUp()
      self.Property = self.env['realestate.property']
      self.Visit = self.env['realestate.visit']
      self.Offer = self.env['realestate.offer']
      
      self.property_1 = self.Property.create({
         'name': 'Property 1',
         'price': 100000,
      })
      
      self.visit_1 = self.Visit.create({
         'property_id': self.property_1.id,
         'date': '2024-01-01 10:00:00',
         'state': 'scheduled',
      })
      
      self.visit_2 = self.Visit.create({
         'property_id': self.property_1.id,
         'date': '2027-06-09 14:00:00',
         'state': 'draft',
      })
      
      self.visit_3 = self.Visit.create({
         'property_id': self.property_1.id,
         'date': '2026-05-01 10:00:00',
         'state': 'draft',
      })
      
      self.offer_1 = self.Offer.create({
         'property_id': self.property_1.id,
         'amount': 95000,
         'state': 'sent',
      })
      
      self.offer_2 = self.Offer.create({
         'property_id': self.property_1.id,
         'amount': 199000,
         'state': 'sent',
      })
      
   def test_action_create_visit(self):
      self.property_1.action_create_visit()
      self.assertEqual(len(self.property_1.visit_ids), 4)
        
   def test_action_accept_best_offer(self):
      self.property_1.action_accept_best_offer()
      self.assertEqual(self.offer_2.state, 'accepted')
      self.assertEqual(self.offer_1.state, 'sent')
      self.assertFalse(self.property_1.availability)
      self.assertTrue(self.offer_2.amount > self.offer_1.amount)
      
   def test_compute_next_visit_date(self):
      self.assertEqual(self.property_1.next_visit_date, self.visit_1.date)
      self.assertTrue(self.property_1.next_visit_date < self.visit_3.date)
