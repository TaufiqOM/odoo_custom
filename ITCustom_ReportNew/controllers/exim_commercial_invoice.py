from odoo import http
from odoo.http import request
from reportlab.pdfgen import canvas
from io import BytesIO

class CustomReportController(http.Controller):

    @http.route('/custom_report/commercial_invoice/pdf', type='http', auth="user")
    def generate_commercial_invoice_pdf(self, **kwargs):
        # Buat PDF dummy
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 800, "This is a dummy COMMERCIAL INVOICE PDF")
        p.showPage()
        p.save()

        pdf_data = buffer.getvalue()
        buffer.close()

        # Kembalikan response PDF yang ditampilkan inline
        return request.make_response(
            pdf_data,
            headers=[
                ('Content-Type', 'application/pdf'),
                ('Content-Disposition', 'inline; filename="commercial_invoice.pdf"')
            ]
        )
