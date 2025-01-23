# Project: Price Scraper for Sodimac and Mercado Libre in Colombia

This project is a Python script designed to scrape product information and prices from Sodimac and Mercado Libre for the Colombian market. The script consolidates the results into a master file for further analysis.

---

## Table of Contents

- [Project: Price Scraper for Sodimac and Mercado Libre in Colombia](#project-price-scraper-for-sodimac-and-mercado-libre-in-colombia)
  - [Table of Contents](#table-of-contents)
  - [Project Overview](#project-overview)
  - [Setup and Requirements](#setup-and-requirements)
    - [Requirements](#requirements)
    - [Setup](#setup)
  - [Directory Structure](#directory-structure)
    - [Input Files:](#input-files)
    - [Output Directories:](#output-directories)
  - [Code Explanation](#code-explanation)
    - [Connection Rules](#connection-rules)
      - [Sets up:](#sets-up)
      - [Fetch with Retry](#fetch-with-retry)
      - [Sodimac Scraper:](#sodimac-scraper)
      - [Mercado Libre Scraper](#mercado-libre-scraper)
      - [Data Collection Workflow](#data-collection-workflow)
  - [Output](#output)
    - [Sodimac Results](#sodimac-results)
    - [Mercado Libre Results](#mercado-libre-results)
    - [Consolidated Master File](#consolidated-master-file)
  - [Notes](#notes)

---

## Project Overview

This script automates the collection of product prices and other details from:
- **Sodimac:** Based on SKUs provided in an input Excel file.
- **Mercado Libre:** Based on EANs provided in the same file.

The results are saved in specific directories and consolidated into a master file.

---

## Setup and Requirements

### Requirements
- Python 3.x
- Dependencies listed in `requirements.txt`:
  - `pandas`
  - `requests`
  - `beautifulsoup4`
  - `requests-kerberos`
  - `tqdm`
  - `python-dotenv`
  - `random-user-agent`

### Setup
1. Clone this repository:
   ```bash
   git clone https://github.com/your-repository.git

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Set up your .env file with the following content:
   ```makefile
   API_KEY=your_api_key_here

---

## Directory Structure
### Input Files:
- `PortfolioMeli2025.xlsx`: Contains EANs and SKUs for Mercado Libre.
- `PortfolioSodimac2025.xlsx`: Contains SKUs for Sodimac.

### Output Directories:
- `Backup/Meli`: Stores Mercado Libre results.
- `Backup/Sodimac`: Stores Sodimac results.
- `Backup/MasterResults`: Stores backups of the consolidated master file.

---

## Code Explanation

### Connection Rules

#### Sets up:

- **Proxy authentication**: Using Kerberos for secure access.
- **User-Agent rotation**: Randomized headers to avoid being blocked by websites.

#### Fetch with Retry

**A reusable function to fetch URLs with retries:**

- Retries 3 times for errors like 429 (Too Many Requests) or 403 (Forbidden).
- Implements exponential backoff to wait longer between retries.


#### Sodimac Scraper:

**Scrapes product details from Sodimac, including:**

- Link
- Title
- Image URL
- Price


#### Mercado Libre Scraper

**Uses the Mercado Libre API to retrieve:**

- Thumbnail
- Product Link
- Price
- Seller Information
- Title

#### Data Collection Workflow

1. Reads input Excel files for SKUs and EANs.
2. Scrapes data from Sodimac and Mercado Libre.
3. Consolidates results into a master file (MasterPrice_Colombia.csv).
4. Creates a backup of the previous master file.

---

## Output

### Sodimac Results
- Saved as:
   ```bash
   Backup/Sodimac/ResultadosSodimac_<date>.csv

### Mercado Libre Results
- Saved as:
   ```bash
   Backup/Meli/ResultadosMeli_<date>.csv

### Consolidated Master File
- **File**: `MasterPrice_Colombia.csv`
- **Backup**: `Backup/MasterResults/MasterPrice_Backup_<date>.csv`

---

## Notes

- Ensure the .env file contains a valid API key.
- Proxy details are configured in the script and require network access permissions.
- Review the fetch_with_retry function for response-specific handling if other error codes arise.

