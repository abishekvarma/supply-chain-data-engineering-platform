# Data Dictionary

## Overview
This document provides detailed descriptions of all entities and their attributes in the supply chain data platform.

## Entities

### Customers
Information about customers in the supply chain network.

**Attributes:**
- `customer_id` - Unique customer identifier
- `name` - Customer name
- `address` - Customer address
- `city` - Customer city
- `state` - Customer state/province
- `postal_code` - Customer postal code
- `country` - Customer country
- `contact_email` - Primary contact email
- `contact_phone` - Primary contact phone
- `created_at` - Record creation timestamp
- `updated_at` - Record update timestamp

### Products
Catalog of products in the supply chain.

**Attributes:**
- `product_id` - Unique product identifier
- `name` - Product name
- `description` - Product description
- `category` - Product category
- `sku` - Stock Keeping Unit
- `unit_price` - Unit price
- `weight` - Product weight
- `dimensions` - Product dimensions (L x W x H)
- `created_at` - Record creation timestamp
- `updated_at` - Record update timestamp

### Warehouses
Physical warehouse and distribution center locations.

**Attributes:**
- `warehouse_id` - Unique warehouse identifier
- `name` - Warehouse name
- `address` - Warehouse address
- `city` - Warehouse city
- `state` - Warehouse state/province
- `postal_code` - Warehouse postal code
- `country` - Warehouse country
- `latitude` - Geographic latitude
- `longitude` - Geographic longitude
- `capacity` - Storage capacity (units)
- `manager_name` - Warehouse manager name
- `contact_email` - Contact email
- `created_at` - Record creation timestamp
- `updated_at` - Record update timestamp

### Vehicles
Transportation fleet vehicles.

**Attributes:**
- `vehicle_id` - Unique vehicle identifier
- `registration_number` - Vehicle registration/license plate
- `vehicle_type` - Type of vehicle (truck, van, etc.)
- `make` - Vehicle manufacturer
- `model` - Vehicle model
- `year` - Manufacturing year
- `capacity` - Vehicle cargo capacity (weight or volume)
- `status` - Current status (active, inactive, maintenance)
- `created_at` - Record creation timestamp
- `updated_at` - Record update timestamp

### Drivers
Personnel operating vehicles.

**Attributes:**
- `driver_id` - Unique driver identifier
- `first_name` - Driver first name
- `last_name` - Driver last name
- `license_number` - Driver license number
- `license_expiry` - License expiration date
- `phone` - Contact phone number
- `email` - Contact email address
- `status` - Employment status (active, inactive)
- `created_at` - Record creation timestamp
- `updated_at` - Record update timestamp

### Orders
Customer orders.

**Attributes:**
- `order_id` - Unique order identifier
- `customer_id` - Reference to customer
- `order_date` - Date order was placed
- `required_delivery_date` - Expected delivery date
- `status` - Order status (pending, processing, shipped, delivered)
- `total_amount` - Total order amount
- `created_at` - Record creation timestamp
- `updated_at` - Record update timestamp

### Shipments
Individual shipments for delivery.

**Attributes:**
- `shipment_id` - Unique shipment identifier
- `order_id` - Reference to order
- `warehouse_id` - Reference to origin warehouse
- `vehicle_id` - Reference to vehicle
- `driver_id` - Reference to driver
- `origin_address` - Shipment origin address
- `destination_address` - Shipment destination address
- `shipment_date` - Date shipment was dispatched
- `expected_delivery_date` - Expected delivery date
- `actual_delivery_date` - Actual delivery date
- `status` - Shipment status (in_transit, delivered, delayed, cancelled)
- `created_at` - Record creation timestamp
- `updated_at` - Record update timestamp

### Shipment Events
Real-time tracking events for shipments.

**Attributes:**
- `event_id` - Unique event identifier
- `shipment_id` - Reference to shipment
- `event_type` - Type of event (pickup, in_transit, delivery, exception)
- `event_timestamp` - When event occurred
- `location` - Location of event
- `latitude` - Geographic latitude
- `longitude` - Geographic longitude
- `notes` - Additional event notes
- `created_at` - Record creation timestamp

## Data Types

- **String** - Text data
- **Integer** - Whole numbers
- **Decimal** - Numeric values with decimal places
- **Date** - Calendar date (YYYY-MM-DD)
- **Timestamp** - Date and time (ISO 8601 format)
- **Boolean** - True/False values

## Conventions

- All IDs follow format: `entity_type` + `_id` (e.g., `customer_id`, `order_id`)
- All timestamps use ISO 8601 format with UTC timezone
- Null values are not permitted in primary and foreign keys
- Status fields use lowercase with underscores (e.g., `in_transit`, `pending`)
