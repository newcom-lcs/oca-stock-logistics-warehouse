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
        
        # Log the values dictionary which contains important info like group_id
        important_keys = ['group_id', 'sale_line_id', 'move_dest_ids', 'propagate_group']
        important_values = {k: v for k, v in values.items() if k in important_keys}
        _logger.info(
            "DEBUG - MTS+MTO - Candidate search values: %s",
            important_values
        )
        
        candidates = self.search([
            ('product_id', '=', product_id.id),
            ('state', 'in', ['draft', 'sent']),
            ('order_id.picking_type_id', '=', picking_type_id.id),
            ('order_id.company_id', '=', company_id.id),
        ], limit=1)
        
        _logger.info(
            "DEBUG - MTS+MTO - Found %s candidate lines for product %s",
            len(candidates), product_id.name
        )
        
        # Log details about each candidate
        for candidate in candidates:
            _logger.info(
                "DEBUG - MTS+MTO - Candidate line: PO: %s, Product: %s, Qty: %s, Origin: %s, Group: %s, Sale Line: %s",
                candidate.order_id.name, 
                candidate.product_id.name, 
                candidate.product_qty,
                candidate.order_id.origin,
                candidate.group_id.name if candidate.group_id else 'No Group',
                candidate.sale_line_id.id if candidate.sale_line_id else 'No Sale Line'
            )
        
        result = super(PurchaseOrderLine, self)._find_candidate(
            product_id, product_qty, product_uom, picking_type_id, 
            location_id, name, origin, company_id, values
        )
        
        if result:
            _logger.info(
                "DEBUG - MTS+MTO - Selected candidate: PO: %s, Line ID: %s, Product: %s, Qty: %s",
                result.order_id.name, result.id, result.product_id.name, result.product_qty
            )
        else:
            _logger.info(
                "DEBUG - MTS+MTO - No candidate selected, will create new line for product %s",
                product_id.name
            )
            
        return result 