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

    image_filenames = fields.Text(
        string='Image Filenames',
        help='Daftar nama file gambar yang terkait dengan produk, dipisah koma atau format JSON'
    )

    filtered_sale_image_ids = fields.Many2many(
        'ir.attachment',
        string='Filtered Sale Images',
        compute='_compute_filtered_sale_image_ids',
        store=False,
    )

    @api.depends('sale_image_ids', 'image_filenames')
    def _compute_filtered_sale_image_ids(self):
        for product in self:
            if not product.image_filenames:
                # If image_filenames is empty or null, set filtered_sale_image_ids to empty
                product.filtered_sale_image_ids = self.env['ir.attachment']
            else:
                filenames = [name.strip() for name in product.image_filenames.split(',') if name.strip()]
                filtered_attachments = product.sale_image_ids.filtered(lambda att: att.name in filenames)
                product.filtered_sale_image_ids = filtered_attachments

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

    def remove_image(self):
        self.ensure_one()
        attachment_id = self.env.context.get('attachment_id')
        if not attachment_id:
            return
        attachment = self.env['ir.attachment'].browse(attachment_id)
        if attachment in self.sale_image_ids:
            self.sale_image_ids = [(3, attachment.id)]
        # Update image_filenames field by removing the attachment name
        if self.image_filenames:
            filenames = [name.strip() for name in self.image_filenames.split(',') if name.strip()]
            if attachment.name in filenames:
                filenames.remove(attachment.name)
                self.image_filenames = ','.join(filenames)
        # Force recompute of filtered_sale_image_ids
        self.invalidate_cache(fnames=['filtered_sale_image_ids'])
        self._compute_filtered_sale_image_ids()

    def remove_image_with_attachment(self, attachment):
        if attachment in self.sale_image_ids:
            self.sale_image_ids = [(3, attachment.id)]
        if self.image_filenames:
            filenames = [name.strip() for name in self.image_filenames.split(',') if name.strip()]
            if attachment.name in filenames:
                filenames.remove(attachment.name)
                self.image_filenames = ','.join(filenames)

class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    def remove_image(self):
        for attachment in self:
            products = self.env['product.template'].search([('sale_image_ids', 'in', attachment.id)])
            for product in products:
                product.remove_image_with_attachment(attachment)

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
        existing_attachments = self.product_id.sale_image_ids
        new_attachment_ids = [att.id for att in attachments if att not in existing_attachments]
        if new_attachment_ids:
            self.product_id.sale_image_ids = [(4, att_id) for att_id in new_attachment_ids]
        # Update image_filenames field with combined list of attachment names without duplicates
        existing_filenames = []
        if self.product_id.image_filenames:
            existing_filenames = [name.strip() for name in self.product_id.image_filenames.split(',') if name.strip()]
        new_filenames = [att.name for att in attachments if att.name not in existing_filenames]
        combined_filenames = existing_filenames + new_filenames
        self.product_id.image_filenames = ','.join(combined_filenames)
        return {'type': 'ir.actions.act_window_close'}
