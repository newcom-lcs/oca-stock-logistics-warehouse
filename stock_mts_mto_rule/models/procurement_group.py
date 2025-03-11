# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models
import logging

_logger = logging.getLogger(__name__)


class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'
    
    @api.model_create_multi
    def create(self, vals_list):
        """Override create to add debugging information"""
        _logger.info(
            "DEBUG - MTS+MTO - Creating %s procurement groups", 
            len(vals_list)
        )
        
        for vals in vals_list:
            name = vals.get('name', 'Unknown')
            sale_id = vals.get('sale_id')
            
            _logger.info(
                "DEBUG - MTS+MTO - Creating Procurement Group: Name: %s, Sale ID: %s, Values: %s",
                name, sale_id, vals
            )
            
        result = super(ProcurementGroup, self).create(vals_list)
        
        # Log the created groups
        for group in result:
            sale_order = None
            if hasattr(group, 'sale_id'):
                sale_order = group.sale_id
                
            _logger.info(
                "DEBUG - MTS+MTO - Procurement Group Created: %s, Sale Order: %s",
                group.name, sale_order.name if sale_order else 'No Sale Order'
            )
                
        return result
        
    def run(self, procurements, raise_user_error=True):
        """Override run to add debugging - correctly handling the raise_user_error parameter"""
        _logger.info(
            "DEBUG - MTS+MTO - Running %s procurements (raise_user_error=%s)", 
            len(procurements), raise_user_error
        )
        
        for procurement in procurements:
            product = procurement.product_id
            values = procurement.values
            origin = values.get('origin', 'Unknown')
            group = values.get('group_id')
            group_name = group.name if group else 'No Group'
            
            _logger.info(
                "DEBUG - MTS+MTO - Running procurement: Product: %s, Qty: %s, Origin: %s, Group: %s",
                product.name, procurement.product_qty, origin, group_name
            )
            
            # Log the values that are important for tracking
            important_keys = ['group_id', 'sale_line_id', 'move_dest_ids', 'origin']
            important_values = {k: v for k, v in values.items() if k in important_keys}
            _logger.info(
                "DEBUG - MTS+MTO - Procurement important values: %s",
                important_values
            )
            
        # Call the original method with the correct signature
        result = super(ProcurementGroup, self).run(procurements, raise_user_error=raise_user_error)
        
        _logger.info("DEBUG - MTS+MTO - Procurement run completed")
        return result 