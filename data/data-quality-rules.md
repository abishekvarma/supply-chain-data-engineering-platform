# Data Quality Rules

## General Rules

| Rule | Description |
|---|---|
| Primary Key Uniqueness | Primary keys must be unique |
| Primary Key Not Null | Primary keys cannot contain NULL values |
| Foreign Key Integrity | Foreign keys must reference valid records |
| Schema Validation | Incoming data must match the expected schema |
| Duplicate Detection | Duplicate business records must be identified |
| Date Validation | Dates must follow valid business rules |
| Numeric Validation | Quantities, capacities and costs cannot contain invalid negative values |
| Status Validation | Status columns must contain approved values |

## Orders

- `order_id` must be unique and not null.
- `customer_id` must exist in Customers.
- `product_id` must exist in Products.
- `warehouse_id` must exist in Warehouses.
- `quantity` must be greater than 0.
- `order_date` must be a valid date.

## Shipments

- `shipment_id` must be unique and not null.
- `order_id` must exist in Orders.
- `vehicle_id` must exist in Vehicles.
- `driver_id` must exist in Drivers.
- `shipment_date` must be a valid date.
- `delivery_date` must not be earlier than `shipment_date`.
- `shipping_cost` must be greater than or equal to 0.

## Shipment Events

- `event_id` must be unique and not null.
- `shipment_id` must exist in Shipments.
- `event_time` must be a valid timestamp.
- `delay_minutes` must be greater than or equal to 0.

## Data Quality Handling

Invalid records should be:

1. Detected during processing.
2. Logged with the reason for failure.
3. Separated from valid records when appropriate.
4. Prevented from corrupting Silver and Gold datasets.

## Medallion Quality Strategy

### Bronze

Preserve source data with minimal transformation.

### Silver

Apply schema validation, cleansing, deduplication, standardization and referential checks.

### Gold

Only validated and business-ready data should be exposed for analytics and Power BI.
