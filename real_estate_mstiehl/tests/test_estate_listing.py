from odoo import fields
from odoo.tests import common
from datetime import timedelta


class TestEstateProperty(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.estate_property = self.env['estate.property']
        self.estate_listing = self.env['estate.listing']
        self.estate_property_visit = self.env['estate.property.visit']
        self.estate_property_type = self.env['estate.property.type']
        self.estate_contract_type = self.env['estate.contract.type']
        self.estate_owner = self.env['estate.owner']
        self.estate_stage = self.env['estate.stage']
        self.estate_stage_type = self.env['estate.stage.type']

        self.contract_type_sale = self.estate_contract_type.create({
            'name': 'Sale',
            'code': 'sale',
        })

        self.stage_type_visit = self.estate_stage_type.create({
            'name': 'Visit',
            'code': 'visit',
        })
        self.stage_draft = self.estate_stage.create({
            'name': 'Draft',
            'code': 'draft',
            'sequence': 1,
            'type_id': self.stage_type_visit.id,
        })
        self.stage_confirmed = self.estate_stage.create({
            'name': 'Confirmed',
            'code': 'confirmed',
            'sequence': 2,
            'type_id': self.stage_type_visit.id,
        })

        self.property_1 = self.estate_property.create({
            'name': 'Property 1',
            'property_type_id': self.estate_property_type.create({'name': 'Apartment', 'code': 'apartment'}).id,
            'expected_price': 100000,
            'selling_price': 120000,
            'available': True,
            'agent_id': self.env.user.id,
            'owner_id': self.estate_owner.create({
                'partner_id': self.env.user.partner_id.id,
            }).id,
        })

        self.listing_1 = self.estate_listing.create({
            'property_id': self.property_1.id,
            'expected_price': self.property_1.expected_price,
            'selling_price': self.property_1.selling_price,
            'description': self.property_1.description,
            'type_id': self.contract_type_sale.id,
            'seller_id': self.property_1.owner_id.partner_id.id,
            'agent_id': self.property_1.agent_id.id,
        })

        self.visit_1 = self.estate_property_visit.create({
            'property_id': self.property_1.id,
            'listing_id': self.listing_1.id,
            'date': fields.Datetime.now() - timedelta(days=1),
            'stage_id': self.stage_draft.id,
        })

        self.visit_2 = self.estate_property_visit.create({
            'property_id': self.property_1.id,
            'listing_id': self.listing_1.id,
            'date': fields.Datetime.now() + timedelta(days=1),
            'stage_id': self.stage_confirmed.id,
        })

        self.visit_3 = self.estate_property_visit.create({
            'property_id': self.property_1.id,
            'listing_id': self.listing_1.id,
            'date': fields.Datetime.now() + timedelta(days=2),
            'stage_id': self.stage_draft.id,
        })
        
        self.visit_4 = self.estate_property_visit.create({
            'property_id': self.property_1.id,
            'listing_id': self.listing_1.id,
            'date': fields.Datetime.now() + timedelta(days=5),
            'stage_id': self.stage_confirmed.id,
        })

    def test_compute_next_visit_date(self):
        """The next visit date is the closest *confirmed* future visit, even when a
        later confirmed visit (visit_4) also exists."""        
        self.assertEqual(self.visit_2.stage_id.code, 'confirmed')
        self.assertEqual(self.visit_4.stage_id.code, 'confirmed')
        self.assertTrue(self.visit_2.date < self.visit_4.date)
        # force error
        #self.assertFalse(self.visit_2.date < self.visit_4.date)

        self.assertEqual(self.listing_1.next_visit_date, self.visit_2.date)
        self.assertTrue(self.listing_1.next_visit_date > fields.Datetime.now())

