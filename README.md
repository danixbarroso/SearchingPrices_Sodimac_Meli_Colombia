# Project: Price Scraper for Sodimac and Mercado Libre

This project is a Python script designed to scrape product information and prices from Sodimac and Mercado Libre for the Colombian market. The script consolidates the results into a master file for further analysis.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Setup and Requirements](#setup-and-requirements)
3. [Directory Structure](#directory-structure)
4. [Code Explanation](#code-explanation)
   - [Connection Rules](#connection-rules)
   - [Fetch with Retry](#fetch-with-retry)
   - [Sodimac Scraper](#sodimac-scraper)
   - [Mercado Libre Scraper](#mercado-libre-scraper)
   - [Data Collection Workflow](#data-collection-workflow)
5. [Output](#output)

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
