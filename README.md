README

Overview

This script automates the scraping of product data from Sodimac and Mercado Libre, consolidates the results, and saves the data in organized directories. It uses various Python libraries and techniques, such as Kerberos authentication, retry logic, and random User-Agent rotation, to ensure reliable and efficient scraping.

Requirements

Dependencies:

Python 3.8+

Required libraries:

pandas

random_user_agent

requests

requests_kerberos

BeautifulSoup (bs4)

tqdm

python-dotenv

Installation:

Run the following command to install the required libraries:

pip install pandas random-user-agent requests requests-kerberos beautifulsoup4 tqdm python-dotenv

Code Breakdown

1. Connection Rules

Environment Variables:
Loads the API key from a .env file.

Proxy Settings:
Configures the proxy settings and authentication using Kerberos.

User-Agent Rotation:
Utilizes random_user_agent to rotate User-Agent headers, simulating real user requests to avoid detection.

2. Retry Logic

Defines the fetch_with_retry function to handle HTTP requests with retries for errors such as 429, 403, and 443. Implements an exponential backoff to wait between retries.

3. Sodimac Scraping

Defines the buscaSodimac function to scrape:

Link: Extracts the product link.

Title: Extracts the product title.

Image: Finds the product image URL by matching the alt attribute with the title.

Price: Parses and cleans the product price.

4. Mercado Libre API Scraping

Defines the coletandoMeli function to:

Query the Mercado Libre API using product EAN.

Parse and organize the JSON response into a DataFrame.

Extract relevant fields: thumbnail, permalink, price, seller, and title.

5. Data Handling and Saving

Mercado Libre Results:

Reads PortfolioMeli2025.xlsx to get product details.

Scrapes data and saves it to:
S:/PT/ac-la/AC_MKB/7. TP ON/E-dealers/01_EspejoDePrecios/v2/Colombia/SearchingPrices_Sodimac_Meli_Colombia/Backup/Meli/ResultadosMeli_{date}.csv

Sodimac Results:

Reads PortfolioSodimac2025.xlsx to get product details.

Scrapes data and saves it to:
S:/PT/ac-la/AC_MKB/7. TP ON/E-dealers/01_EspejoDePrecios/v2/Colombia/SearchingPrices_Sodimac_Meli_Colombia/Backup/Sodimac/ResultadosSodimac_{date}.csv

6. Data Consolidation

Combines results from Sodimac and Mercado Libre into a single DataFrame.

Merges with existing master file, if available.

Saves:

Backup: S:/PT/ac-la/AC_MKB/7. TP ON/E-dealers/01_EspejoDePrecios/v2/Peru/SearchingPrices_Sodimac_Meli_Peru/Backup/MasterResults/MasterPrice_Backup_{date}.csv

Updated Master File: S:/PT/ac-la/AC_MKB/7. TP ON/E-dealers/01_EspejoDePrecios/v2/Colombia/SearchingPrices_Sodimac_Meli_Colombia/Masterprice_Colombia.csv

Directory Structure

Input Files:

PortfolioMeli2025.xlsx: Contains Mercado Libre product details.

PortfolioSodimac2025.xlsx: Contains Sodimac product details.

Output Directories:

Mercado Libre Results:
S:/PT/ac-la/AC_MKB/7. TP ON/E-dealers/01_EspejoDePrecios/v2/Colombia/SearchingPrices_Sodimac_Meli_Colombia/Backup/Meli

Sodimac Results:
S:/PT/ac-la/AC_MKB/7. TP ON/E-dealers/01_EspejoDePrecios/v2/Colombia/SearchingPrices_Sodimac_Meli_Colombia/Backup/Sodimac

Master File Backup:
S:/PT/ac-la/AC_MKB/7. TP ON/E-dealers/01_EspejoDePrecios/v2/Peru/SearchingPrices_Sodimac_Meli_Peru/Backup/MasterResults

Master File:
S:/PT/ac-la/AC_MKB/7. TP ON/E-dealers/01_EspejoDePrecios/v2/Colombia/SearchingPrices_Sodimac_Meli_Colombia

Notes

Ensure the .env file contains the API_KEY for Mercado Libre API access.

Proxy authentication requires a valid Kerberos setup.

The script implements error handling and retry mechanisms to enhance reliability during scraping.

Future Improvements

Optimize retry logic to handle additional error codes.

Enhance logging for better traceability.

Modularize the script for better maintainability.