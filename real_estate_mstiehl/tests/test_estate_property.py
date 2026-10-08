from odoo.tests import common


class TestEstateProperty(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.estate_property = self.env['estate.property']
        self.estate_owner = self.env['estate.owner']
        self.estate_property_type = self.env['estate.property.type']

        self.property_type_apartment = self.estate_property_type.create({
            'name': 'Apartment',
            'code': 'apartment',
        })

        self.property_1 = self.estate_property.create({
            'name': 'Property 1',
            'property_type_id': self.property_type_apartment.id,
            'expected_price': 100000,
            'selling_price': 120000,
            'available': True,
            'agent_id': self.env.user.id,
            'owner_id': self.estate_owner.create({
                'partner_id': self.env.user.partner_id.id,
            }).id,
            'date_register': '2026-01-01',
        })

        self.property_2 = self.estate_property.create({
            'name': 'Property 2',
            'property_type_id': self.property_type_apartment.id,
            'expected_price': 100000,
            'selling_price': 120000,
            'available': True,
            'agent_id': self.env.user.id,
            'owner_id': self.estate_owner.create({
                'partner_id': self.env.ref('base.partner_root').id,
            }).id,
            'date_register': '2027-01-01',
        })

    def test_property_ref_code_generated(self):
        self.assertTrue(self.property_1.property_ref_code)
        self.assertTrue(self.property_2.property_ref_code)
        self.assertNotEqual(self.property_1.property_ref_code, self.property_2.property_ref_code)

    def test_default_order_by_date_register_desc(self):
        properties = self.estate_property.search([
            ('id', 'in', [self.property_1.id, self.property_2.id]),
        ])
        self.assertEqual(properties[0], self.property_2)
        self.assertEqual(properties[1], self.property_1)
