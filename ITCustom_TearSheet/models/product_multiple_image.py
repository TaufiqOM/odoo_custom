from odoo import models, fields, api
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    sale_image_ids = fields.Many2many(
        'ir.attachment',
        string='Sale Images',
        domain="[('res_model', '=', 'product.template'), ('res_id', '=', id)]",
        help="Additional images to be displayed in Sales tab"
    )

    def action_upload_from_documents(self):
        self.ensure_one()
        return {
            'name': 'Select Documents from Products Folder',
            'type': 'ir.actions.act_window',
            'res_model': 'product.documents.selection.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_product_id': self.id},
        }

class ProductDocumentsSelectionWizard(models.TransientModel):
    _name = 'product.documents.selection.wizard'
    _description = 'Wizard to select documents from Products folder'

    product_id = fields.Many2one('product.template', string='Product', readonly=True)
    document_ids = fields.Many2many(
        'documents.document',
        string='Documents',
        domain="[('folder_id.name', '=', 'Products')]"
    )

    def action_link_documents(self):
        self.ensure_one()
        if not self.document_ids:
            raise UserError("Please select at least one document.")
        attachments = self.document_ids.mapped('attachment_id')  # Changed to 'attachment_id' (singular) as per Odoo documents module
        if not attachments:
            raise UserError("No attachments found in the selected documents.")
        # Link selected documents' attachments to product's sale_image_ids
        self.product_id.sale_image_ids = [(4, att.id) for att in attachments]
        return {'type': 'ir.actions.act_window_close'}