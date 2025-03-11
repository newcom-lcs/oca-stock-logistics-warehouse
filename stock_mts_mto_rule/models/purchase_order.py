# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models
import logging

_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to add debugging information"""
        _logger.info(
            "DEBUG - MTS+MTO - Creating %s purchase orders", 
            len(vals_list)
        )
        
        for vals in vals_list:
            origin = vals.get('origin', 'Unknown')
            group_id = vals.get('group_id')
            partner_id = vals.get('partner_id')
            
            # Get partner name
            partner_name = 'Unknown'
            if partner_id:
                partner_name = self.env['res.partner'].browse(partner_id).name
                
            _logger.info(
                "DEBUG - MTS+MTO - PO Creation: Origin: %s, Partner: %s, Group ID: %s, Values: %s",
                origin, partner_name, group_id, vals
            )
            
        result = super(PurchaseOrder, self).create(vals_list)
        
        # Log the created POs
        for po in result:
            _logger.info(
                "DEBUG - MTS+MTO - PO Created: %s, Origin: %s, Partner: %s, Group: %s, Lines: %s",
                po.name, po.origin, po.partner_id.name, po.group_id.name if po.group_id else 'No Group',
                len(po.order_line)
            )
            
            # Log line details
            for line in po.order_line:
                _logger.info(
                    "DEBUG - MTS+MTO - PO Line: PO: %s, Product: %s, Qty: %s, Sale Order: %s, Group: %s",
                    po.name, line.product_id.name, line.product_qty,
                    line.sale_order_id.name if line.sale_order_id else 'No SO',
                    line.group_id.name if line.group_id else 'No Group'
                )
                
        return result


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"
    
    def write(self, vals):
        """Override write to add debugging information"""
        # Only log if product_qty is changed (adding to an existing line)
        if 'product_qty' in vals:
            for line in self:
                _logger.info(
                    "DEBUG - MTS+MTO - Updating PO Line: PO: %s, Product: %s, Current Qty: %s, New Qty: %s, Sale Line: %s",
                    line.order_id.name, line.product_id.name, line.product_qty, vals['product_qty'],
                    line.sale_line_id.id if line.sale_line_id else 'No Sale Line'
                )
                
        result = super(PurchaseOrderLine, self).write(vals)
        return result
    
    @api.model_create_multi
    def create(self, vals_list):
        """Override create to add debugging information"""
        _logger.info(
            "DEBUG - MTS+MTO - Creating %s purchase order lines", 
            len(vals_list)
        )
        
        for vals in vals_list:
            product_id = vals.get('product_id')
            order_id = vals.get('order_id')
            product_qty = vals.get('product_qty')
            sale_line_id = vals.get('sale_line_id', False)
            
            # Get names
            product_name = 'Unknown'
            po_name = 'Unknown'
            if product_id:
                product_name = self.env['product.product'].browse(product_id).name
            if order_id:
                po_name = self.env['purchase.order'].browse(order_id).name
                
            _logger.info(
                "DEBUG - MTS+MTO - Creating PO Line: PO: %s, Product: %s, Qty: %s, Sale Line ID: %s",
                po_name, product_name, product_qty, sale_line_id
            )
            
        result = super(PurchaseOrderLine, self).create(vals_list)
        return result 