# Data Dictionary

## Customers

| Column | Type | Description |
|---|---|---|
| customer_id | STRING | Unique customer identifier |
| customer_name | STRING | Customer name |
| email | STRING | Customer email |
| city | STRING | Customer city |
| state | STRING | Customer state |
| country | STRING | Customer country |
| customer_status | STRING | Active or inactive status |

## Products

| Column | Type | Description |
|---|---|---|
| product_id | STRING | Unique product identifier |
| product_name | STRING | Product name |
| category | STRING | Product category |
| unit_price | DECIMAL | Product selling price |
| weight_kg | DECIMAL | Product weight |

## Warehouses

| Column | Type | Description |
|---|---|---|
| warehouse_id | STRING | Unique warehouse identifier |
| warehouse_name | STRING | Warehouse name |
| city | STRING | Warehouse city |
| state | STRING | Warehouse state |
| warehouse_capacity | DECIMAL | Storage capacity |

## Orders

| Column | Type | Description |
|---|---|---|
| order_id | STRING | Unique order identifier |
| customer_id | STRING | Customer reference |
| product_id | STRING | Product reference |
| warehouse_id | STRING | Warehouse reference |
| order_date | DATE | Date order was placed |
| quantity | INT | Quantity ordered |
| order_status | STRING | Current order status |

## Shipments

| Column | Type | Description |
|---|---|---|
| shipment_id | STRING | Unique shipment identifier |
| order_id | STRING | Order reference |
| vehicle_id | STRING | Vehicle reference |
| driver_id | STRING | Driver reference |
| warehouse_id | STRING | Origin warehouse |
| shipment_date | DATE | Shipment date |
| delivery_date | DATE | Delivery date |
| shipment_status | STRING | Shipment status |
| shipping_cost | DECIMAL | Shipping cost |

## Shipment Events

| Column | Type | Description |
|---|---|---|
| event_id | STRING | Unique event identifier |
| shipment_id | STRING | Shipment reference |
| event_time | TIMESTAMP | Event timestamp |
| location | STRING | Event location |
| event_type | STRING | Type of shipment event |
| delay_minutes | INT | Delay duration |

## Vehicles

| Column | Type | Description |
|---|---|---|
| vehicle_id | STRING | Unique vehicle identifier |
| vehicle_type | STRING | Vehicle type |
| capacity_kg | DECIMAL | Vehicle capacity |
| vehicle_status | STRING | Vehicle status |
| manufacture_year | INT | Manufacturing year |

## Drivers

| Column | Type | Description |
|---|---|---|
| driver_id | STRING | Unique driver identifier |
| driver_name | STRING | Driver name |
| experience_years | INT | Driving experience |
| license_type | STRING | License category |
| driver_status | STRING | Driver status |
