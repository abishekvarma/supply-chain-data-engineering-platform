#!/usr/bin/env python3
"""
Schema validation script for supply chain data engineering platform.

This script validates CSV files against their corresponding JSON schemas by:
- Reading JSON schemas from data/schemas/
- Reading CSV files from data/sample/
- Validating each CSV against its corresponding schema
- Checking required columns and data types
- Reporting clear validation errors
"""

import sys
import json
import os
from pathlib import Path
from typing import Dict, List, Tuple, Any

# Try to import pandas, fall back to csv module if not available
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    import csv


def find_schema_and_csv_pairs() -> List[Tuple[Path, Path]]:
    """
    Find matching pairs of JSON schemas and CSV files.
    
    Returns:
        List of tuples containing (schema_path, csv_path)
    """
    schema_dir = Path("data/schemas")
    sample_dir = Path("data/sample")
    
    pairs = []
    
    if not schema_dir.exists():
        print(f"Error: Schema directory not found: {schema_dir}")
        return pairs
    
    if not sample_dir.exists():
        print(f"Error: Sample data directory not found: {sample_dir}")
        return pairs
    
    # Find all JSON schemas
    for schema_file in schema_dir.glob("*.json"):
        csv_name = schema_file.stem + ".csv"
        csv_path = sample_dir / csv_name
        
        if csv_path.exists():
            pairs.append((schema_file, csv_path))
        else:
            print(f"Warning: No matching CSV found for schema {schema_file.name}")
    
    return pairs


def load_schema(schema_path: Path) -> Dict[str, Any]:
    """
    Load a JSON schema from file.
    
    Args:
        schema_path: Path to the JSON schema file
        
    Returns:
        Parsed schema dictionary
        
    Raises:
        Exception if schema cannot be loaded or parsed
    """
    try:
        with open(schema_path, 'r') as f:
            schema = json.load(f)
        return schema
    except json.JSONDecodeError as e:
        raise Exception(f"Invalid JSON in schema {schema_path.name}: {e}")
    except Exception as e:
        raise Exception(f"Error reading schema {schema_path.name}: {e}")


def load_csv_data(csv_path: Path) -> Tuple[List[str], List[List[Any]]]:
    """
    Load CSV data from file.
    
    Args:
        csv_path: Path to the CSV file
        
    Returns:
        Tuple of (column_names, rows)
        
    Raises:
        Exception if CSV cannot be loaded
    """
    try:
        if HAS_PANDAS:
            df = pd.read_csv(csv_path)
            columns = df.columns.tolist()
            rows = df.values.tolist()
            return columns, rows
        else:
            with open(csv_path, 'r') as f:
                reader = csv.reader(f)
                columns = next(reader)
                rows = list(reader)
            return columns, rows
    except Exception as e:
        raise Exception(f"Error reading CSV {csv_path.name}: {e}")


def get_python_type(value: Any) -> str:
    """
    Determine the Python type of a value.
    
    Args:
        value: The value to check
        
    Returns:
        Type name as string
    """
    if value is None or (isinstance(value, float) and pd.isna(value) if HAS_PANDAS else value == ''):
        return "null"
    elif isinstance(value, bool):
        return "boolean"
    elif isinstance(value, int):
        return "integer"
    elif isinstance(value, float):
        return "number"
    else:
        # Try to parse string as number
        str_val = str(value).strip()
        if str_val.lower() in ('true', 'false'):
            return "boolean"
        try:
            int(str_val)
            return "integer"
        except ValueError:
            try:
                float(str_val)
                return "number"
            except ValueError:
                return "string"


def validate_column_type(value: Any, expected_type: str) -> bool:
    """
    Check if a value matches the expected type.
    
    Args:
        value: The value to check
        expected_type: The expected type (string, integer, number, boolean)
        
    Returns:
        True if value matches type, False otherwise
    """
    if expected_type == "null":
        return value is None or (isinstance(value, float) and pd.isna(value) if HAS_PANDAS else value == '')
    
    actual_type = get_python_type(value)
    
    # Allow null values for optional columns
    if actual_type == "null":
        return True
    
    # Type matching
    if expected_type == actual_type:
        return True
    
    # Allow integer values for number type
    if expected_type == "number" and actual_type == "integer":
        return True
    
    return False


def validate_csv_against_schema(schema: Dict[str, Any], csv_path: Path, 
                                columns: List[str], rows: List[List[Any]]) -> List[str]:
    """
    Validate a CSV file against its schema.
    
    Args:
        schema: Parsed JSON schema
        csv_path: Path to the CSV file
        columns: Column names from CSV
        rows: Data rows from CSV
        
    Returns:
        List of error messages (empty if validation passes)
    """
    errors = []
    
    # Extract schema properties
    properties = schema.get("properties", {})
    required = schema.get("required", [])
    
    if not properties:
        errors.append(f"Schema has no properties defined")
        return errors
    
    # Check for required columns
    for req_col in required:
        if req_col not in columns:
            errors.append(f"Required column missing: '{req_col}'")
    
    # Check for unexpected columns
    schema_cols = set(properties.keys())
    csv_cols = set(columns)
    unexpected = csv_cols - schema_cols
    if unexpected:
        errors.append(f"Unexpected columns in CSV: {', '.join(sorted(unexpected))}")
    
    # Validate data types for each column
    for col_idx, col_name in enumerate(columns):
        if col_name not in properties:
            continue
        
        col_schema = properties[col_name]
        expected_type = col_schema.get("type", "string")
        
        # Check data types in rows
        for row_idx, row in enumerate(rows):
            if col_idx >= len(row):
                errors.append(f"Row {row_idx + 2} (data row {row_idx + 1}): Column '{col_name}' is missing")
                continue
            
            value = row[col_idx]
            
            if not validate_column_type(value, expected_type):
                actual_type = get_python_type(value)
                errors.append(
                    f"Row {row_idx + 2} (data row {row_idx + 1}), Column '{col_name}': "
                    f"Expected {expected_type}, got {actual_type} (value: {repr(value)})"
                )
    
    return errors


def main() -> int:
    """
    Main validation function.
    
    Returns:
        0 if all validations pass, 1 if any validation fails
    """
    pairs = find_schema_and_csv_pairs()
    
    if not pairs:
        print("Error: No schema-CSV pairs found")
        return 1
    
    print(f"Found {len(pairs)} schema-CSV pair(s) to validate\n")
    
    all_passed = True
    
    for schema_path, csv_path in pairs:
        print(f"Validating {csv_path.name} against {schema_path.name}...")
        
        try:
            # Load schema and CSV
            schema = load_schema(schema_path)
            columns, rows = load_csv_data(csv_path)
            
            # Validate
            errors = validate_csv_against_schema(schema, csv_path, columns, rows)
            
            if errors:
                all_passed = False
                print(f"  ✗ Validation FAILED with {len(errors)} error(s):")
                for error in errors:
                    print(f"    - {error}")
            else:
                print(f"  ✓ Validation PASSED ({len(rows)} rows, {len(columns)} columns)")
        
        except Exception as e:
            all_passed = False
            print(f"  ✗ Error during validation: {e}")
        
        print()
    
    if all_passed:
        print("✓ All datasets passed validation!")
        return 0
    else:
        print("✗ One or more datasets failed validation")
        return 1


if __name__ == "__main__":
    sys.exit(main())
