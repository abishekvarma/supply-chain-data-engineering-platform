# 🚚 Supply Chain Data Engineering Platform

An end-to-end cloud data engineering platform designed to ingest, process, transform, govern, and visualize supply chain data using Microsoft Azure, Azure Databricks, Microsoft Fabric, and Power BI.

## 🏗️ Architecture

![Supply Chain Data Engineering Architecture](docs/architecture/architecture.png)

## 🎯 Project Overview

This project demonstrates a modern data engineering pipeline for processing supply chain and logistics data from multiple sources and transforming it into business-ready analytics.

The platform follows a scalable cloud architecture with Azure Data Factory for orchestration, Azure Data Lake Storage Gen2 for data storage, Azure Databricks for data processing, Microsoft Fabric OneLake for analytical storage, and Power BI for business reporting.

## 🔄 Data Flow

```text
Data Sources
     ↓
Azure Data Factory
     ↓
ADLS Gen2
     ↓
Azure Databricks
     ↓
Bronze → Silver → Gold
     ↓
Microsoft Fabric OneLake
     ↓
Power BI
     ↓
Executive Dashboard
