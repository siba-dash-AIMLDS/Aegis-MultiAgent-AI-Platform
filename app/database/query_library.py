QUERY_LIBRARY = {

    "employee": (
        "Employee Summary",
        """
        SELECT COUNT(*) AS total_employees
        FROM employees;
        """
    ),

    "customer": (
        "Customer Summary",
        """
        SELECT COUNT(*) AS total_customers
        FROM customers;
        """
    ),

    "product": (
        "Product Summary",
        """
        SELECT COUNT(*) AS total_products
        FROM products;
        """
    ),

    "supplier": (
        "Supplier Summary",
        """
        SELECT COUNT(*) AS total_suppliers
        FROM suppliers;
        """
    ),

    "order": (
        "Order Summary",
        """
        SELECT COUNT(*) AS total_orders
        FROM orders;
        """
    ),

    "payment": (
        "Payment Summary",
        """
        SELECT COUNT(*) AS total_payments
        FROM payments;
        """
    ),

    "inventory": (
        "Inventory Summary",
        """
        SELECT COUNT(*) AS total_inventory
        FROM inventory;
        """
    ),

    "categories": (
        "Category Summary",
        """
        SELECT COUNT(*) AS total_categories
        FROM categories;
        """
    ),

    "region": (
        "Region Summary",
        """
        SELECT COUNT(*) AS total_regions
        FROM regions;
        """
    )

}