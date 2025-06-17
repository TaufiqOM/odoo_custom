from odoo import models, fields, api

class DocumentImageSelector(models.TransientModel):
    _name = 'document.image.selector'
    _description = 'Select Images from Documents'

    document_ids = fields.Many2many(
        'documents.document',
        domain="[('res_model', '=', 'product.template'), ('type', '=', 'binary')]"
    )
    product_tmpl_id = fields.Many2one(
        'product.template',
        required=True
    )

    def action_add_images(self):
        attachments = self.env['ir.attachment']
        for document in self.document_ids:
            attachment = attachments.create({
                'name': document.name,
                'datas': document.datas,
                'res_model': 'product.template',
                'res_id': self.product_tmpl_id.id,
            })
        self.product_tmpl_id.sale_image_ids = [(4, attachment.id) for attachment in attachments]
        return {'type': 'ir.actions.act_window_close'}