# Entity Relationships

## Core Relationships

```text
Customers
   │
   └── customer_id
          │
          ▼
       Orders
          │
          ├── product_id ───────► Products
          │
          └── warehouse_id ─────► Warehouses
          │
          ▼
      Shipments
          │
          ├── vehicle_id ───────► Vehicles
          │
          ├── driver_id ────────► Drivers
          │
          └── shipment_id
                  │
                  ▼
          Shipment Events
