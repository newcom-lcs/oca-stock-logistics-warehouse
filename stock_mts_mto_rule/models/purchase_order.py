# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    product_key = fields.Many2one(
        "product.product",
        string="Product Key",
        help="Technical field used to ensure separate purchase orders per product"
    )
    
    @api.model
    def _prepare_name(self, vals):
        """Add product information to PO name to ensure uniqueness."""
        seq = self.env['ir.sequence']
        name = seq.next_by_code('purchase.order') or '/'
        
        # See if we have product info and add it to the PO name
        product_key = vals.get('product_key')
        if product_key:
            product = self.env['product.product'].browse(product_key)
            if product.exists():
                # Append product code/id to make name unique
                product_code = product.default_code or str(product.id)
                name = f"{name}-{product_code}"
                _logger.info("CUSTOM DEBUG - Created unique PO name: %s for product: %s", name, product.name)
        
        return name
    
    @api.model_create_multi
    def create(self, vals_list):
        """Override create to ensure unique PO names per product."""
        for vals in vals_list:
            if not vals.get('name', '/') or vals.get('name', '/') == '/':
                vals['name'] = self._prepare_name(vals)
                _logger.info("CUSTOM DEBUG - Setting custom PO name: %s", vals['name'])
        
        return super(PurchaseOrder, self).create(vals_list) 