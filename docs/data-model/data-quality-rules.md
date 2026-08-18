# Data Quality Rules

## Overview
This document defines data validation and quality rules for the supply chain data platform. All data ingestion and processing must comply with these rules.

## Entity-Specific Rules

### Customers

**Required Fields:**
- `customer_id` - Must be non-null and unique
- `name` - Must be non-null and non-empty
- `contact_email` - Must be valid email format
- `country` - Must be non-null

**Validation Rules:**
- Email format: Must match standard email pattern (xxx@xxx.xxx)
- Phone format: If provided, must be valid phone number format
- Postal code: Country-specific validation if applicable
- Name: Must contain at least 1 character, maximum 255 characters

**Business Rules:**
- Cannot have duplicate `customer_id`
- Email must be unique per customer (optional, can have duplicates)
- Status must be either 'active' or 'inactive'

### Products

**Required Fields:**
- `product_id` - Must be non-null and unique
- `name` - Must be non-null and non-empty
- `sku` - Must be non-null and unique
- `category` - Must be non-null

**Validation Rules:**
- `unit_price` - Must be non-negative decimal (>= 0)
- `weight` - If provided, must be positive number (> 0)
- `sku` - Must follow format: alphanumeric, 3-50 characters
- `name` - Maximum 255 characters
- `description` - Maximum 1000 characters

**Business Rules:**
- Cannot have duplicate `product_id` or `sku`
- Category must be from predefined list of valid categories
- Discontinued products must have end_date recorded

### Warehouses

**Required Fields:**
- `warehouse_id` - Must be non-null and unique
- `name` - Must be non-null and non-empty
- `city` - Must be non-null
- `country` - Must be non-null

**Validation Rules:**
- `latitude` - Must be between -90 and 90
- `longitude` - Must be between -180 and 180
- `capacity` - Must be positive number (> 0)
- Postal code: Country-specific validation
- Email: Valid email format if provided

**Business Rules:**
- Cannot have duplicate `warehouse_id`
- Geographic coordinates must be within valid country boundaries
- Capacity must be consistent with warehouse type
- Only one primary warehouse per region

### Vehicles

**Required Fields:**
- `vehicle_id` - Must be non-null and unique
- `registration_number` - Must be non-null and unique
- `vehicle_type` - Must be non-null
- `capacity` - Must be positive number (> 0)

**Validation Rules:**
- `year` - Must be between 1900 and current year
- `make` and `model` - Maximum 100 characters each
- `capacity` - Must match vehicle type specifications
- `status` - Must be from: 'active', 'inactive', 'maintenance'

**Business Rules:**
- Cannot have duplicate `vehicle_id` or `registration_number`
- Vehicle must pass safety inspection before activation
- Maintenance status prevents assignment to new shipments

### Drivers

**Required Fields:**
- `driver_id` - Must be non-null and unique
- `first_name`, `last_name` - Must be non-null and non-empty
- `license_number` - Must be non-null and unique
- `license_expiry` - Must be in future date

**Validation Rules:**
- `email` - Valid email format if provided
- `phone` - Valid phone format if provided
- `license_expiry` - Must be after current date
- Names: Maximum 100 characters each
- `status` - Must be from: 'active', 'inactive', 'suspended'

**Business Rules:**
- Cannot have duplicate `driver_id` or `license_number`
- License must not be expired
- Inactive or suspended drivers cannot be assigned new shipments
- License expiry must trigger notification 30 days before expiration

### Orders

**Required Fields:**
- `order_id` - Must be non-null and unique
- `customer_id` - Must reference existing customer
- `order_date` - Must be non-null and not in future
- `status` - Must be non-null

**Validation Rules:**
- `order_date` - Must be <= current date
- `required_delivery_date` - Must be >= order_date
- `total_amount` - Must be positive (> 0)
- `status` - Must be from: 'pending', 'processing', 'shipped', 'delivered', 'cancelled'
- Dates must be in ISO 8601 format

**Business Rules:**
- Cannot have duplicate `order_id`
- customer_id must exist in Customers table
- Total amount must be sum of line items
- Cancelled orders cannot be modified
- Required delivery date should not exceed 90 days from order date

### Shipments

**Required Fields:**
- `shipment_id` - Must be non-null and unique
- `order_id` - Must reference existing order
- `warehouse_id` - Must reference existing warehouse
- `vehicle_id` - Must reference existing vehicle
- `driver_id` - Must reference existing driver (when assigned)
- `status` - Must be non-null

**Validation Rules:**
- `shipment_date` - Must be non-null and <= current date
- `expected_delivery_date` - Must be > shipment_date
- `actual_delivery_date` - Must be >= shipment_date if provided
- `status` - Must be from: 'in_transit', 'delivered', 'delayed', 'cancelled'
- Addresses: Non-null and minimum 10 characters

**Business Rules:**
- Cannot have duplicate `shipment_id`
- Vehicle capacity must be sufficient for shipment
- Driver license must not be expired
- Vehicle must be in 'active' status
- Driver must be in 'active' status
- Actual delivery cannot be before shipment date
- Shipment status must follow valid state transitions
- Multiple shipments from same order must have different vehicles or different dates

### Shipment Events

**Required Fields:**
- `event_id` - Must be non-null and unique
- `shipment_id` - Must reference existing shipment
- `event_type` - Must be non-null
- `event_timestamp` - Must be non-null

**Validation Rules:**
- `event_type` - Must be from: 'pickup', 'in_transit', 'delivery', 'exception', 'delayed'
- `event_timestamp` - Must be in ISO 8601 format
- `latitude` - Must be between -90 and 90 if provided
- `longitude` - Must be between -180 and 180 if provided
- `notes` - Maximum 1000 characters

**Business Rules:**
- Cannot have duplicate `event_id`
- Event timestamp must not be before shipment date
- Events must be in chronological order per shipment
- Delivery event must mark shipment as delivered
- Location must be valid geographic coordinates if provided

## Cross-Entity Rules

### Referential Integrity
1. All foreign key references must exist
2. Customer deletion must cascade to orders and shipments
3. Order deletion must cascade to shipments and events
4. Shipment deletion must cascade to events

### Date Consistency
1. Order date <= Required delivery date
2. Shipment date <= Expected delivery date
3. Expected delivery date >= Shipment date
4. Actual delivery date >= Shipment date (if provided)
5. Event timestamp >= Shipment date

### Status Transitions

**Order Status Flow:**
```
pending → processing → shipped → delivered
   ↓                      ↓         ↓
   └──────→ cancelled ←───┴─────────┘
```

**Shipment Status Flow:**
```
in_transit → delivered
    ↓            ↓
    └→ delayed ──┘
    ↓
  cancelled
```

## Data Quality Metrics

### Completeness
- Required fields: 100% non-null
- Optional fields: Target > 80% populated for commonly used fields
- Foreign key references: 100% valid

### Accuracy
- Email addresses: 95%+ valid format
- Phone numbers: 90%+ valid format
- Geographic coordinates: 99%+ within valid ranges
- Dates: 100% in valid format

### Consistency
- Duplicate check: 0% duplicates on unique fields
- Status values: 100% from valid enumeration
- Date logic: 100% chronologically valid

### Timeliness
- Real-time data (Shipment Events): < 5 minute latency
- Batch data (Orders, Customers): Daily synchronization
- Daily quality checks: All rules must pass

## Quality Assurance Procedures

### Pre-Load Validation
1. Schema validation - All records match expected schema
2. Data type validation - Fields conform to defined types
3. Constraint validation - All constraints are satisfied
4. Referential integrity - All foreign keys are valid

### Post-Load Validation
1. Duplicate detection - Check for unexpected duplicates
2. Statistical validation - Check data distribution
3. Relationship validation - Verify all relationships are intact
4. Audit trail - Maintain change logs

### Monitoring and Alerts
1. Quality score tracking - Monitor overall data quality
2. Anomaly detection - Alert on unusual patterns
3. Threshold violations - Alert when metrics fall below targets
4. Regular audits - Weekly manual data quality reviews

## Error Handling

### Validation Failure Actions
- **Critical errors:** Reject entire batch, log error, notify data owner
- **Non-critical errors:** Quarantine records, create exception report, allow manual review
- **Warnings:** Log warning, allow load to proceed, create audit entry

### Error Logging
- All validation failures must be logged with:
  - Record identifier
  - Field and value that failed
  - Rule that was violated
  - Timestamp
  - Source system
