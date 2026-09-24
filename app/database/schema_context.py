ALLOWED_TABLES = {
    "employees",
    "customers",
    "products",
    "suppliers",
    "orders",
    "payments",
    "inventory",
    "categories",
    "regions",
}


class SchemaContext:

    @classmethod
    def get_schema(cls) -> dict[str, list[str]]:

        return {
            "employees": [
                "id",
                "employee_code",
                "first_name",
                "last_name",
                "email",
                "phone",
                "designation",
                "hire_date",
                "region_id",
                "created_at",
                "updated_at",
                "is_active",
            ],
            "customers": [
                "id",
                "customer_code",
                "first_name",
                "last_name",
                "email",
                "phone",
                "address",
                "city",
                "state",
                "country",
                "postal_code",
                "region_id",
                "created_at",
                "updated_at",
                "is_active",
            ],
            "products": [
                "id",
                "product_code",
                "product_name",
                "description",
                "unit_price",
                "cost_price",
                "category_id",
                "supplier_id",
                "created_at",
                "updated_at",
                "is_active",
            ],
            "suppliers": [
                "id",
                "supplier_name",
                "contact_name",
                "email",
                "phone",
                "city",
                "country",
                "created_at",
                "updated_at",
                "is_active",
            ],
            "orders": [
                "id",
                "order_number",
                "order_date",
                "order_status",
                "total_amount",
                "customer_id",
                "employee_id",
                "created_at",
                "updated_at",
                "is_active",
            ],
            "payments": [
                "id",
                "order_id",
                "payment_reference",
                "payment_method",
                "payment_status",
                "amount",
                "payment_date",
                "created_at",
                "updated_at",
                "is_active",
            ],
            "inventory": [
                "id",
                "product_id",
                "quantity_in_stock",
                "reorder_level",
                "maximum_stock",
                "last_restocked",
                "created_at",
                "updated_at",
                "is_active",
            ],
            "categories": [
                "id",
                "category_name",
                "description",
                "created_at",
                "updated_at",
                "is_active",
            ],
            "regions": [
                "id",
                "region_name",
                "country",
                "created_at",
                "updated_at",
                "is_active",
            ],
        }

    @classmethod
    def get_relationships(cls) -> list[dict]:

        return [
            {
                "from_table": "employees",
                "from_column": "region_id",
                "to_table": "regions",
                "to_column": "id",
            },
            {
                "from_table": "customers",
                "from_column": "region_id",
                "to_table": "regions",
                "to_column": "id",
            },
            {
                "from_table": "products",
                "from_column": "category_id",
                "to_table": "categories",
                "to_column": "id",
            },
            {
                "from_table": "products",
                "from_column": "supplier_id",
                "to_table": "suppliers",
                "to_column": "id",
            },
            {
                "from_table": "orders",
                "from_column": "customer_id",
                "to_table": "customers",
                "to_column": "id",
            },
            {
                "from_table": "orders",
                "from_column": "employee_id",
                "to_table": "employees",
                "to_column": "id",
            },
            {
                "from_table": "payments",
                "from_column": "order_id",
                "to_table": "orders",
                "to_column": "id",
            },
            {
                "from_table": "inventory",
                "from_column": "product_id",
                "to_table": "products",
                "to_column": "id",
            },
        ]

    @classmethod
    def format_relationships(cls) -> str:

        relationships = cls.get_relationships()

        lines = []

        for relationship in relationships:

            lines.append(
                f"{relationship['from_table']}."
                f"{relationship['from_column']} -> "
                f"{relationship['to_table']}."
                f"{relationship['to_column']}"
            )

        return "\n".join(lines)

    @classmethod
    def format_schema(cls) -> str:

        schema = cls.get_schema()

        lines = []

        for table, columns in schema.items():

            lines.append(f"TABLE: {table}")

            for column in columns:
                lines.append(f"  - {column}")

            lines.append("")

        return "\n".join(lines)