
# Project: Price Scraper and Merger for Sodimac and Mercado Libre in Colombia

This project automates the collection and merging of product price data from Sodimac and Mercado Libre for the Colombian market. It includes scripts for scraping product information, consolidating the data into master files, and performing data analysis.

---

## Table of Contents

- [Project: Price Scraper and Merger for Sodimac and Mercado Libre in Colombia](#project-price-scraper-and-merger-for-sodimac-and-mercado-libre-in-colombia)
  - [Table of Contents](#table-of-contents)
  - [Project Overview](#project-overview)
  - [Setup and Requirements](#setup-and-requirements)
    - [Requirements](#requirements)
    - [Setup](#setup)
  - [Directory Structure](#directory-structure)
    - [Input Files](#input-files)
    - [Output Directories](#output-directories)
  - [Code Explanation](#code-explanation)
    - [Scraper Scripts](#scraper-scripts)
    - [Merge Script](#merge-script)
  - [Output](#output)
    - [Scraping Results](#scraping-results)
    - [Merged Data](#merged-data)
    - [Visualizations](#visualizations)
  - [Notes](#notes)

---

## Project Overview

This project consists of two main components:
1. **Scraper scripts**: Automate the extraction of product prices and details from Sodimac and Mercado Libre.
2. **Merge script**: Combines the scraped data with an input dataset, enabling further analysis and visualizations.

---

## Setup and Requirements

### Requirements

- Python 3.x
- Dependencies listed in `requirements.txt`:
  - `pandas`
  - `matplotlib`
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
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your `.env` file with the following content:
   ```makefile
   API_KEY=your_api_key_here
   ```

---

## Directory Structure

### Input Files

- **MasterPrice file**: A `.csv` file containing scraped data from Sodimac and Mercado Libre.
- **MasterColombia file**: An `.xlsx` file containing product metadata (e.g., SKUs, EANs).

### Output Directories

- The merged data is saved to:
  ```
  S:/PT/ac-la/AC_MKB/7. TP ON/E-dealers/01_EspejoDePrecios/v2/Colombia/SearchingPrices_Sodimac_Meli_Colombia/final_merged_master.csv
  ```

---

## Code Explanation

### Scraper Scripts

The scraper scripts are responsible for:
1. Extracting product data (price, seller, and images) from Sodimac and Mercado Libre.
2. Saving the data into a master `.csv` file for later merging.

### Merge Script

The `merge.py` script:
1. Loads the scraped data (`MasterPrice`) and the metadata (`MasterColombia`).
2. Cleans and formats columns for consistency.
3. Merges the datasets based on SKU and EAN mappings.
4. Saves the merged dataset as a `.csv` file.
5. Generates a plot of average product prices over time for both platforms.

---

## Output

### Scraping Results

The scraping scripts save a consolidated `.csv` file with the following structure:
- `source`: The data source (Sodimac or Mercado Libre).
- `query`: The SKU or EAN queried.
- `price`: The extracted product price.
- `seller`: The seller's name.
- `dateSearch`: The date of data collection.

### Merged Data

The merge script generates a final `.csv` file that includes:
- Consolidated product information.
- Matching metadata from `MasterColombia`.

### Visualizations

The merge script generates a plot showing the average price over time for each platform.

---

## Notes

- Ensure all file paths are correct and accessible.
- The `.env` file must be properly configured for authentication.
- Use a proxy or Kerberos setup if required to access external networks.
