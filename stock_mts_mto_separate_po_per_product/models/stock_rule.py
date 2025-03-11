# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from collections import defaultdict
from odoo import models, api
import logging

_logger = logging.getLogger(__name__)


class StockRule(models.Model):
    _inherit = "stock.rule"

    def _make_po_get_domain(self, company_id, values, partner):
        """Override to add product to the domain to ensure one PO per product."""
        domain = super()._make_po_get_domain(company_id, values, partner)
        
        # Get the product from the values
        product = values.get('product_id')
        if product:
            # Include product in the domain to ensure separate POs per product
            domain.append(('product_key', '=', product.id))
            
        return domain

    def _prepare_purchase_order(self, company_id, origins, values):
        """Override to add product_key to the PO values"""
        vals = super()._prepare_purchase_order(company_id, origins, values)
        
        # Add product_key from the first procurement's values
        product = values[0].get('product_id')
        if product:
            vals['product_key'] = product.id
            
        return vals
            
    def _run_buy(self, procurements):
        """Override _run_buy to log that we're using our custom logic."""
        _logger.info("Running _run_buy with separate PO per product logic")
        return super()._run_buy(procurements) 