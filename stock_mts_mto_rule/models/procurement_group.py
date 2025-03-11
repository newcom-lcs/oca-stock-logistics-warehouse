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
            _logger.info(
                "DEBUG - MTS+MTO - Procurement Group Created: %s, Sale Order: %s",
                group.name, group.sale_id.name if group.sale_id else 'No Sale Order'
            )
                
        return result
        
    @api.model
    def run(self, procurements):
        """Override run to add debugging"""
        _logger.info(
            "DEBUG - MTS+MTO - Running %s procurements", 
            len(procurements)
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
            important_keys = ['group_id', 'sale_line_id', 'move_dest_ids', 'origin', 'propagate_group']
            important_values = {k: v for k, v in values.items() if k in important_keys}
            _logger.info(
                "DEBUG - MTS+MTO - Procurement important values: %s",
                important_values
            )
            
        result = super(ProcurementGroup, self).run(procurements)
        
        _logger.info("DEBUG - MTS+MTO - Procurement run completed")
        return result 