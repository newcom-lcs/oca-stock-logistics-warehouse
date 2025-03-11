# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    product_key = fields.Many2one(
        comodel_name="product.product",
        string="Product Key",
        help="Used to create different PO per product")

    @api.model
    def _make_po_get_domain(self, partner, company, picking_type=False, group_id=False):
        """Override to add product_key to the domain to ensure separate POs per product."""
        domain = super()._make_po_get_domain(partner, company, picking_type, group_id)
        
        # Get the product from context if set by the procurement rule
        force_product = self._context.get('force_product_po')
        if force_product:
            domain += [('product_key', '=', force_product.id)]
            _logger.info(
                "CUSTOM OVERRIDE - Added product_key filter for %s (ID: %d) to PO search domain", 
                force_product.name, force_product.id
            )
        
        return domain
        
    def _prepare_name(self):
        """Prepare a unique name for the PO that includes product info if available."""
        name = self.env['ir.sequence'].next_by_code('purchase.order') or '/'
        
        # Add product information to the name if available
        if self.product_key:
            product_code = self.product_key.default_code or str(self.product_key.id)
            name = f"{name}-P{product_code}"
            _logger.info("CUSTOM OVERRIDE - Generated unique PO name with product: %s", name)
            
        return name

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to ensure unique PO names per product."""
        for vals in vals_list:
            if not vals.get('name', '/') or vals.get('name', '/') == '/':
                vals['name'] = self._prepare_name(vals)
                _logger.info("CUSTOM DEBUG - Setting custom PO name: %s", vals['name'])
        
        return super(PurchaseOrder, self).create(vals_list) 