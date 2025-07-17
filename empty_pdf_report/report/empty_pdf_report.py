# -*- coding: utf-8 -*-
from odoo import api, models

class EmptyPDFReport(models.AbstractModel):
    _name = 'report.empty_pdf_report.empty_pdf_report_template'
    _description = 'Empty PDF Report'
    
    @api.model
    def _get_report_values(self, docids, data=None):
        """Return empty report values"""
        return {
            'doc_ids': docids,
            'doc_model': 'empty.pdf.model',
            'docs': [],
            'data': data,
        }
