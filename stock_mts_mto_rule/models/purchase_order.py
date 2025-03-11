# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models
import logging

_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to add simple debugging information without accessing relationships"""
        _logger.info(
            "DEBUG - MTS+MTO - Creating %s purchase orders", 
            len(vals_list)
        )
        
        # Just log essential info from vals without accessing related records
        for vals in vals_list:
            origin = vals.get('origin', 'Unknown')
            partner_id = vals.get('partner_id', 'Unknown')
            
            _logger.info(
                "DEBUG - MTS+MTO - PO Creation: Origin: %s, Partner ID: %s",
                origin, partner_id
            )
            
        result = super(PurchaseOrder, self).create(vals_list)
        
        # Log minimal info about the created POs
        for po in result:
            _logger.info(
                "DEBUG - MTS+MTO - PO Created: %s, Origin: %s",
                po.name, po.origin
            )
                
        return result


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"
    
    def write(self, vals):
        """Override write with minimal debugging"""
        if 'product_qty' in vals:
            for line in self:
                _logger.info(
                    "DEBUG - MTS+MTO - Updating PO Line: Product: %s, Qty %s -> %s",
                    line.product_id.name if line.product_id else 'Unknown',
                    line.product_qty, vals['product_qty']
                )
                
        result = super(PurchaseOrderLine, self).write(vals)
        return result
    
    @api.model_create_multi
    def create(self, vals_list):
        """Override create with minimal debugging"""
        _logger.info(
            "DEBUG - MTS+MTO - Creating %s purchase order lines", 
            len(vals_list)
        )
        
        # Just log product_id and qty without accessing related records
        for vals in vals_list:
            product_id = vals.get('product_id', 'Unknown')
            product_qty = vals.get('product_qty', 0.0)
            
            _logger.info(
                "DEBUG - MTS+MTO - Creating PO Line: Product ID: %s, Qty: %s",
                product_id, product_qty
            )
            
        result = super(PurchaseOrderLine, self).create(vals_list)
        return result 