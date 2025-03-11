=====================================
Stock MTS+MTO - Separate PO per Product
=====================================

This module extends the functionality of stock_mts_mto_rule to create separate purchase orders for each product in a sales order.

In the standard stock_mts_mto_rule module, products from different sales orders that have the same supplier are grouped into a single purchase order. This can make it difficult to track which products were ordered for which sales order.

This module ensures that:

* Each product in a sales order gets its own purchase order
* The module preserves all the existing MTS+MTO functionality that determines how much to purchase based on available stock

Configuration
=============

No specific configuration is needed beyond what's required for the stock_mts_mto_rule module:

* Enable Make To Order + Make To Stock route on products
* Configure proper suppliers on products

Usage
=====

* Create a sales order with multiple products using the MTS+MTO route
* Confirm the order
* Separate purchase orders will be created for each product, preserving the link to the original sales order

Bug Tracker
==========

Contact your system administrator if you encounter any issues with this module.

Credits
=======

Contributors
~~~~~~~~~~~

* Newcom Development Team 