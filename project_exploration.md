#### SER541: Exploratory Data Munging and Visualization
#### Mexico City Airbnb Listings: Exploratory Munging and Visual Analysis
#### Aman Sharma
#### 2026-03-03

## Basic Questions

**Dataset Author(s):** InsideAirbnb (Murray Cox and collaborators; InsideAirbnb public data project)


**Dataset Construction Date:**
The Dataset used is a periodic "city scrape" snapshot from InsideAirbnb.
- Command: 
    python3 -c 
    "import pandas as pd; 
    df=pd.read_csv('data_original/MexicoCityDataSet.csv'); 
    print(df['last_scraped'].dropna().max())"

- Output: 2025-09-28

**Dataset Record Count**
- 27051

**Dataset Field Meanings**
- **price** listing price (Convertef to numeric, original contained currency formatting).
- **accomodates** contains the maximum number of guests the listing supports.
- **bedrooms** number of bedrooms (Contains zero which may represents studio ).
- **number_of_reviews** total number of reviews recorded for the listing this is used as proxy for popularity.
- **room_type** categorical listing type.

**Dataset File Hash(es):**
- **Source:** InsideAirbnb “Get the Data” portal for Mexico City listings
- **File:** data_original/MexicoCityDataSet.csv
- **MD5:** `3f28a87e2085c235fed327f429d43e88`  computed via `md5 data_original/MexicoCityDataSet.csv`


## Interpretable Records

### Record 1
`35797,3673.0,2,1.0,0,Entire home/apt`

**Interpretation:**
  - This listing costs 3676 (local currency units as provided by the dataset).
  - Accomodates 2 guests, has 1 bedroom and is an entire home/apt.
  - It currently has 0 reviews which is reasonable for a new listing and with o ly the limited booking history.
  - The combination of small capacity and moderate-high is logical as in high-demand neighborhoods.

### Record 2
**Raw Data (from processed_listings.csv):**
`171109,321.0,2,1.0,123,Private room`

**Interpretation:** 
  - This listing costs 321, accommodates 2 guests, has 1 bedroom,and is “Private room. 
  - It has 123 reviews, which is reasonable for a lower-cost option that may attract frequent short stays and repeat demand.
  - Lower price and private room category align with hig no. of reviews.










