from odoo import models, fields, api
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    sale_image_ids = fields.Many2many(
        'ir.attachment',
        string='Sale Images',
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
    
    main_image_filename = fields.Char(string="Main Image Filename")

    def action_batch_update_images(self):
        for product in self:
            if product.main_image_filename:
                filename = product.main_image_filename.strip()
                doc = self.env['documents.document'].search([
                    ('name', '=', filename),
                    ('folder_id.name', '=', 'Products'),
                    ('attachment_id.datas', '!=', False)
                ], limit=1)

                if doc and doc.attachment_id:
                    product.image_1920 = doc.attachment_id.datas
                else:
                    product.image_1920 = False




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

    def _sync_sale_image_ids_with_filenames(self):
        for product in self:
            if not product.image_filenames:
                product.sale_image_ids = [(5, 0, 0)]
            else:
                filenames = [name.strip() for name in product.image_filenames.split(',') if name.strip()]
                # Search attachments linked to documents.document with matching names
                document_attachments = self.env['ir.attachment'].search([
                    ('name', 'in', filenames),
                    ('res_model', '=', 'documents.document'),
                ])
                # Do not update res_model and res_id to allow multiple product links
                # document_attachments.write({'res_model': 'product.template', 'res_id': product.id})
                # Merge existing sale_image_ids with found attachments
                existing_ids = product.sale_image_ids.ids
                new_ids = list(set(existing_ids + document_attachments.ids))
                product.sale_image_ids = [(6, 0, new_ids)]

    @api.model_create_multi
    def create(self, vals_list):
        records = super(ProductTemplate, self).create(vals_list)
        records._sync_sale_image_ids_with_filenames()
        return records

    def write(self, vals):
        res = super(ProductTemplate, self).write(vals)
        if 'image_filenames' in vals:
            self._sync_sale_image_ids_with_filenames()
        return res

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
        self.env.cache.invalidate([('filtered_sale_image_ids', self.ids)])
        self._compute_filtered_sale_image_ids()

    def remove_image_with_attachment(self, attachment):
        if attachment in self.sale_image_ids:
            self.sale_image_ids = [(3, attachment.id)]
        if self.image_filenames:
            filenames = [name.strip() for name in self.image_filenames.split(',') if name.strip()]
            if attachment.name in filenames:
                filenames.remove(attachment.name)
                self.image_filenames = ','.join(filenames)

    def remove_image_with_attachment_for_product(self, attachment, product):
        product.ensure_one()
        if attachment in product.sale_image_ids:
            product.sale_image_ids = [(3, attachment.id)]
        if product.image_filenames:
            filenames = [name.strip() for name in product.image_filenames.split(',') if name.strip()]
            if attachment.name in filenames:
                filenames.remove(attachment.name)
                product.write({'image_filenames': ','.join(filenames)})
        product.env.cache.invalidate([('filtered_sale_image_ids', product.ids)])
        product._compute_filtered_sale_image_ids()

class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    product_id = fields.Many2one(
        'product.template',
        string='Product',
        compute='_compute_product_id',
        store=False,
        help='Product linked to this attachment if any',
    )

    def _compute_product_id(self):
        for attachment in self:
            products = self.env['product.template'].search([('sale_image_ids', 'in', attachment.id)], limit=1)
            attachment.product_id = products.id if products else False

    def remove_image(self):
        import logging
        _logger = logging.getLogger(__name__)
        product_id = self.env.context.get('product_id')
        _logger.info(f"remove_image called with product_id: {product_id}")
        for attachment in self:
            if product_id:
                product = self.env['product.template'].browse(product_id)
                _logger.info(f"Removing attachment {attachment.id} from product {product.id}")
                if product and attachment in product.sale_image_ids:
                    # Remove attachment from product's sale_image_ids
                    product.sale_image_ids = [(3, attachment.id)]
                    # Update image_filenames only for this product
                    if product.image_filenames:
                        filenames = [name.strip() for name in product.image_filenames.split(',') if name.strip()]
                        if attachment.name in filenames:
                            filenames.remove(attachment.name)
                            product.image_filenames = ','.join(filenames)
                    product.env.cache.invalidate([('filtered_sale_image_ids', product.ids)])
                    product._compute_filtered_sale_image_ids()
            else:
                products = self.env['product.template'].search([('sale_image_ids', 'in', attachment.id)])
                for product in products:
                    product.remove_image_with_attachment(attachment)
        return {}

class ProductDocumentsSelectionWizard(models.TransientModel):
    _name = 'product.documents.selection.wizard'
    _description = 'Wizard to select documents from Products folder'

    product_id = fields.Many2one('product.template', string='Product', readonly=True)
    document_ids = fields.Many2many(
        'documents.document',
        string='Documents',
        domain="[('folder_id.name', '=', 'Products')]"
    )
    upload_file = fields.Binary(string="Upload Image")
    upload_filename = fields.Char(string="Upload Filename")

    def action_link_documents(self):
        self.ensure_one()
        attachments = []
        # Handle uploaded file if present
        if self.upload_file and self.upload_filename:
            # Save uploaded file as attachment and create documents.document linked to Products folder
            documents_folder = self.env['documents.document'].search([('folder_id.name', '=', 'Products')], limit=1)
            folder_id = documents_folder.folder_id.id if documents_folder else False
            attachment_vals = {
                'name': self.upload_filename,
                'datas': self.upload_file,
                'res_model': 'documents.document',
                'res_id': 0,
                'mimetype': 'image/png',  # Could be improved to detect mimetype
            }
            attachment = self.env['ir.attachment'].create(attachment_vals)
            document_vals = {
                'name': self.upload_filename,
                'folder_id': folder_id,
                'attachment_id': attachment.id,
            }
            document = self.env['documents.document'].create(document_vals)
            attachments.append(attachment)
        # Handle selected documents
        if self.document_ids:
            attachments += self.document_ids.mapped('attachment_id')
        if not attachments:
            raise UserError("Please select or upload at least one image.")
        # Link attachments to product's sale_image_ids
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
