# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models
import logging

_logger = logging.getLogger(__name__)


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"
    
    def _find_candidate(self, product_id, product_qty, product_uom, picking_type_id, location_id, name, origin, company_id, values):
        """Override to add debugging for candidate finding"""
        _logger.info(
            "DEBUG - MTS+MTO - Finding candidate line for: Product: %s, Qty: %s, Origin: %s",
            product_id.name, product_qty, origin
        )
        
        # Log the values dictionary which contains important info
        important_keys = ['group_id', 'move_dest_ids']
        important_values = {k: str(v) for k, v in values.items() if k in important_keys and v}
        _logger.info(
            "DEBUG - MTS+MTO - Candidate search values (simplified): %s",
            important_values
        )
        
        # Search for candidates but don't log details that might cause database issues
        result = super(PurchaseOrderLine, self)._find_candidate(
            product_id, product_qty, product_uom, picking_type_id, 
            location_id, name, origin, company_id, values
        )
        
        # Just log if we found a candidate or not
        if result:
            _logger.info(
                "DEBUG - MTS+MTO - Found candidate line for product %s",
                product_id.name
            )
        else:
            _logger.info(
                "DEBUG - MTS+MTO - No candidate found for product %s, will create new line",
                product_id.name
            )
            
        return result 