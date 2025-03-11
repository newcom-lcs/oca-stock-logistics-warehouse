# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    product_key = fields.Many2one(
        "product.product", 
        string="Product Key",
        help="Technical field used to ensure separate purchase orders per product"
    ) 