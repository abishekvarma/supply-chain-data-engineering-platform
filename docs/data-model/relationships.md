# Entity Relationships

## Relationship Diagram

```
Customers (1) -------- (N) Orders
                          |
                          |
                      (1) | (N)
                          |
                      Shipments (1) ------ (1) Warehouses
                          |
                          | (1)
                          |
                      (1) | (N)
                          |
                      Vehicles
                          |
                          | (1)
                          |
                      (1) | (N)
                          |
                      Drivers
                          |
                          |
                      (1) | (N)
                          |
                    Shipment_Events

Products -- (M) -- Orders
(through order_items implicit relationship)
```

## Relationship Details

### Customers → Orders
- **Cardinality:** One-to-Many (1:N)
- **Foreign Key:** `customer_id` in Orders table
- **Description:** One customer can place multiple orders
- **Constraint:** Every order must reference exactly one customer

### Orders → Shipments
- **Cardinality:** One-to-Many (1:N)
- **Foreign Key:** `order_id` in Shipments table
- **Description:** One order can have multiple shipments (partial shipments)
- **Constraint:** Every shipment must reference exactly one order

### Shipments → Warehouses
- **Cardinality:** Many-to-One (N:1)
- **Foreign Key:** `warehouse_id` in Shipments table
- **Description:** Multiple shipments can originate from the same warehouse
- **Constraint:** Every shipment must originate from exactly one warehouse

### Shipments → Vehicles
- **Cardinality:** Many-to-One (N:1)
- **Foreign Key:** `vehicle_id` in Shipments table
- **Description:** Multiple shipments can be transported by the same vehicle
- **Constraint:** A shipment uses exactly one vehicle

### Shipments → Drivers
- **Cardinality:** Many-to-One (N:1)
- **Foreign Key:** `driver_id` in Shipments table
- **Description:** Multiple shipments can be handled by the same driver
- **Constraint:** A shipment is assigned to exactly one driver

### Shipments → Shipment_Events
- **Cardinality:** One-to-Many (1:N)
- **Foreign Key:** `shipment_id` in Shipment_Events table
- **Description:** One shipment can have multiple tracking events
- **Constraint:** Every event must reference exactly one shipment

### Orders → Products
- **Cardinality:** Many-to-Many (M:N)
- **Bridge Table:** `order_items` (not yet defined)
- **Description:** One order can contain multiple products; one product can appear in multiple orders
- **Note:** This relationship is implicit and would typically be managed through an `order_items` junction table

## Key Constraints

### Primary Keys
- `Customers.customer_id`
- `Products.product_id`
- `Warehouses.warehouse_id`
- `Vehicles.vehicle_id`
- `Drivers.driver_id`
- `Orders.order_id`
- `Shipments.shipment_id`
- `Shipment_Events.event_id`

### Foreign Keys
- `Orders.customer_id` → `Customers.customer_id`
- `Shipments.order_id` → `Orders.order_id`
- `Shipments.warehouse_id` → `Warehouses.warehouse_id`
- `Shipments.vehicle_id` → `Vehicles.vehicle_id`
- `Shipments.driver_id` → `Drivers.driver_id`
- `Shipment_Events.shipment_id` → `Shipments.shipment_id`

## Cascade Rules

### On Delete Behavior

**Customers:** Cascade deletes to Orders and Shipments
- Deleting a customer removes all associated orders and shipments

**Orders:** Cascade deletes to Shipments and Shipment_Events
- Deleting an order removes all associated shipments and events

**Shipments:** Cascade deletes to Shipment_Events
- Deleting a shipment removes all associated tracking events

**Warehouses, Vehicles, Drivers:** Restrict deletes
- Cannot delete if referenced by active shipments

### On Update Behavior

**All Foreign Keys:** Cascade updates to dependent records
- Changing an ID in parent table updates all child records

## Data Integrity Rules

1. **Referential Integrity:** All foreign key values must reference existing primary keys
2. **Non-Null Constraints:** Primary and foreign keys cannot be NULL
3. **Unique Constraints:** Primary key values must be unique within their respective tables
4. **Date Constraints:** Delivery dates must be after order/shipment dates
5. **Status Constraints:** Status values must be from predefined enumerations

## Query Patterns

### Common Joins

**Get all orders for a customer:**
```sql
SELECT o.* FROM Orders o
JOIN Customers c ON o.customer_id = c.customer_id
WHERE c.customer_id = ?
```

**Get shipment details with tracking events:**
```sql
SELECT s.*, se.* FROM Shipments s
LEFT JOIN Shipment_Events se ON s.shipment_id = se.shipment_id
WHERE s.shipment_id = ?
ORDER BY se.event_timestamp
```

**Get vehicle utilization:**
```sql
SELECT v.*, COUNT(s.shipment_id) as active_shipments
FROM Vehicles v
LEFT JOIN Shipments s ON v.vehicle_id = s.vehicle_id
WHERE s.status != 'delivered'
GROUP BY v.vehicle_id
```
