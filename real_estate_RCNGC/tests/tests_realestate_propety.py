from odoo.tests import common

class TestRealestateProperty(common.TransactionCase):

    def setUp(self):
        super().setUp()
        self.Property = self.env['realestate.property']
        self.Visit = self.env['realestate.visit']
        self.Offer = self.env['realestate.offer']

        self.property_1 = self.env['realestate.property'].create({
            'name': 'Test Property 1',
            'price': 150000,
            'availability': True,
        })

        self.offer_1 = self.env['realestate.offer'].create({
            'property_id': self.property_1.id,
            'amount': 160000,
        })  

        self.offer_2 = self.env['realestate.offer'].create({
            'property_id': self.property_1.id,
            'amount': 170000,
        })  
        

    def test_action_create_visit(self):
        self.property_1.action_create_visit()
        self.assertTrue(len(self.property_1.visit_ids) > 0)

    def test_action_accept_best_offer(self):
        self.property_1.action_accept_best_offer()
        self.assertEqual(self.offer_2.state, 'accepted')






    # def setUp(self):
    #     super(TestRealestateProperty, self).setUp()
    #     # Create a test property
    #     self.property = self.env['realestate.property'].create({
    #         'name': 'Test Property',
    #         'price': 100000,
    #         'availability': True,
    #     })

    # def test_create_offer(self):
    #     offer = self.env['realestate.offer'].create({
    #         'property_id': self.property.id,
    #         'amount': 120000,
    #     })
    #     self.assertEqual(offer.property_id, self.property)
    #     self.assertEqual(offer.amount, 120000)
