# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api
import logging
from collections import defaultdict

_logger = logging.getLogger(__name__)


class PurchaseStockRule(models.Model):
    _inherit = 'stock.rule'
    
    def _run_buy(self, procurements):
        """Override the _run_buy method from purchase_stock to create separate POs per product."""
        _logger.info("CUSTOM OVERRIDE - _run_buy directly overridden with %d procurements", len(procurements))
        
        # Group procurements by product to ensure separate POs
        procurements_by_product = defaultdict(list)
        for procurement in procurements:
            product = procurement[0].product_id
            procurements_by_product[product].append(procurement)
        
        # Process each product's procurements separately
        for product, product_procurements in procurements_by_product.items():
            _logger.info(
                "CUSTOM OVERRIDE - Processing %d procurements for product %s (ID: %d) separately",
                len(product_procurements), product.name, product.id
            )
            
            # Inject product context to be used in PO search domain
            self = self.with_context(force_product_po=product)
            
            # Call parent method with only this product's procurements
            super(PurchaseStockRule, self)._run_buy(product_procurements)
        
        return True
        
    def _get_group_keys(self, values, partner):
        """Add product to grouping keys to force separate POs per product."""
        keys = super()._get_group_keys(values, partner)
        
        # Add product_id to the grouping keys
        product = values.get('product_id')
        if product:
            # Convert to tuple if necessary (some versions might return a list)
            if isinstance(keys, list):
                keys = tuple(keys)
            
            # Add product to keys
            keys = keys + (product,)
            _logger.info(
                "CUSTOM OVERRIDE - Added product %s (ID: %d) to grouping keys",
                product.name, product.id
            )
        
        return keys
    
    def _prepare_purchase_order(self, company_id, origins, values):
        """Ensure product_key is set on new purchase orders."""
        vals = super()._prepare_purchase_order(company_id, origins, values)
        
        # Add product_key from the procurement values
        product = values[0].get('product_id')
        if product:
            vals['product_key'] = product.id
            _logger.info(
                "CUSTOM OVERRIDE - Set product_key to %s (ID: %d) on new PO",
                product.name, product.id
            )
            
            # Force a unique name for the PO with product info
            name = self.env['ir.sequence'].next_by_code('purchase.order') or '/'
            product_code = product.default_code or str(product.id)
            vals['name'] = f"{name}-P{product_code}"
            
            _logger.info("CUSTOM OVERRIDE - Set unique PO name: %s", vals['name'])
            
        return vals 