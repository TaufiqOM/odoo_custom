# -*- coding: utf-8 -*-
from odoo.tests import common

class TestHrAppraisalCustom(common.TransactionCase):
    
    def setUp(self):
        super(TestHrAppraisalCustom, self).setUp()
        self.Appraisal = self.env['hr.appraisal']
        self.employee = self.env['hr.employee'].create({
            'name': 'Test Employee'
        })
        
    def test_custom_fields_creation(self):
        """Test that custom fields are properly added to hr.appraisal"""
        appraisal = self.Appraisal.create({
            'employee_id': self.employee.id,
            'custom_notes': 'Test notes',
            'custom_rating': 'good',
            'custom_date': '2024-01-01',
            'custom_boolean': True
        })
        
        self.assertEqual(appraisal.custom_notes, 'Test notes')
        self.assertEqual(appraisal.custom_rating, 'good')
        self.assertEqual(str(appraisal.custom_date), '2024-01-01')
        self.assertTrue(appraisal.custom_boolean)
        
    def test_custom_summary_computation(self):
        """Test that custom_summary field is computed correctly"""
        appraisal = self.Appraisal.create({
            'employee_id': self.employee.id,
            'custom_notes': 'Test performance review',
            'custom_rating': 'excellent'
        })
        
        self.assertIn('excellent', appraisal.custom_summary)
        self.assertIn('Test performance review', appraisal.custom_summary)
