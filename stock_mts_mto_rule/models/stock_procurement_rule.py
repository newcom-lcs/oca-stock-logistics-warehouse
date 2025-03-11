# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api
import logging

_logger = logging.getLogger(__name__)


class ProcurementRule(models.Model):
    _inherit = 'procurement.group'
    
    @api.model
    def run(self, procurements, raise_user_error=True):
        """Override run to log procurement groups and their contents."""
        _logger.info("CUSTOM DEBUG - Procurement run with %s procurements", len(procurements))
        
        # Group procurements by product to see what's being processed together
        product_groups = {}
        for procurement in procurements:
            product = procurement.product_id
            if product not in product_groups:
                product_groups[product] = []
            product_groups[product].append(procurement)
        
        for product, product_procurements in product_groups.items():
            _logger.info(
                "CUSTOM DEBUG - Product group: %s (ID: %s) has %s procurements",
                product.name, product.id, len(product_procurements)
            )
        
        return super(ProcurementRule, self).run(procurements, raise_user_error=raise_user_error) 