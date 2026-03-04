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


## Background Domain Knowledge
  - Short-term rental platforms such as Airbnb have emerged to be a key part of urban tourism and temporary housing markets. For a city such as Mexico City, which is a large metropolitan area, listings on such platforms vary in terms of price, capacity, and location.

  - The price charged per night by each listing is affected by various factors, which may be interacting with each other, such as the location in the city, proximity to popular tourist destinations, safety and amenities offered by the neighborhood, the number of bedrooms, the capacity to accommodate the number of guests, and the reputation of the host.

  - On the demand side, users weigh the trade-offs between price, privacy, and space depending on their needs. For example, a single person may choose to stay in a private room, which is priced lower, whereas a family may choose to stay in an entire home with many bedrooms. The number_of_reviews field is useful in terms of providing a proxy to the activity and popularity of the listing, though this is affected by the age of the listing and reviews as well.

  - In urban areas with high rates of tourism development, the supply of short-term rentals can shape the supply dynamics and economic structure of neighborhoods. Using publicly available data, as offered through InsideAirbnb, researchers can investigate the pricing and capacity distributions in a transparent and reproducible fashion. The variability in this dataset is consistent with expected market trends in a large and diverse urban tourism market.

**Sources:**
1. InsideAirbnb – Get the Data (Mexico City listings snapshots)
2. Airbnb Help Center / public materials on listing types and guest capacity concepts
3. Academic / policy overviews on short-term rentals and urban housing impacts.

## Dataset Generality
  - The data set seems representative of the Airbnb market in Mexico City because it reflects considerable variation along different dimensions of the market: price, capacity, listing size, popularity, and room type. For example, prices vary from 61 to 900,000 with a median price of 1,039. This suggests that the data set reflects a variety of prices and that there are not too many extreme values in this domain. 
  - Capacity varies from 1 to 16 guests with a median capacity of 2 guests. Similarly, the number of bedrooms varies from 0 to 50 with a median of 1. These suggest that the data set reflects common small urban listings as well as occasional large listings.
  - The review count varies from 0 to 1434 with a median review count of 24. This suggests that the data set reflects a variety of listing ages: not only newly created listings but also older ones that have accumulated more reviews. 
  Finally, the domain of room type reflects four different categories: "Entire home/apt" is the most common room type, while "Hotel room" is the least common room type. This is consistent with the general composition of such platforms.


## Data Transformations

### Transformation 1: Price Cleaning (currency → numeric)
**Description:** 

  - Converted the raw `price` field from a currency-formatted string (e.g., “$3,673.00”) into a numeric value by removing currency symbols and separators, then casting to float.
  - This transformation preserves the meaning of “nightly price” while enabling statistical operations such as correlation and median. No semantic content is removed; only formatting characters are stripped.

### Transformation 2: Feature Selection for EDA
**Description:** 

  - Selected a subset of meaningful variables for this milestone: `price`, `accommodates`, `bedrooms`, `number_of_reviews`, and `room_type`.
  - Produced `data_processed/processed_listings.csv`.
  - These features represent economic value (price), capacity/size (accommodates, bedrooms), demand proxy (reviews), and listing class (room_type). Removing the irrelevant columns makes the code easier to read without changing the meaning of the remaining features.


### Transformation 3: Handling Missing Values during Plotting/Correlation
**Description:** 

  - When computing correlations and scatter plots, the rows with missing values for the columns involved in the plots were skipped for the computation.
  - By skipping the rows with missing values for the columns involved, the use of any form of artificial data insertion, or imputation, was circumvented, ensuring the soundness of the computed values.



## Visualizations

### Visual 1: `visuals/scatter_accommodates_vs_bedrooms.png`
**Analysis:** 
  - This plot shows a clear positive relationship: listings with more bedrooms generally accommodate more guests. 
  - The pattern is consistent with expectations for residential properties and also matches the strong correlation observed between bedrooms and accommodates.


### Visual 2: `visuals/scatter_price_vs_bedrooms.png`
**Analysis:** 
  - Price increases slightly with the number of bedrooms, but the range is large, indicating that the number of bedrooms does not influence price significantly.
  - There are a number of extreme high-priced data points, indicating luxury properties.

### Visual 3: `visuals/scatter_price_vs_accommodates.png`
**Analysis:** 
  - It does not seem like the price increases for higher capacity, as a number of data points have the same value for accommodates but a different price range.

### Visual 4: `visuals/scatter_price_vs_number_of_reviews.png`
**Analysis:** 
  - Most data points are concentrated at lower price ranges, and the number of reviews ranges over the lower price range. 
  - There are a number of data points at higher prices, all of which have a lower number of reviews.

### Visual 5: `visuals/scatter_bedrooms_vs_number_of_reviews.png`
**Analysis:** 
  - Listings with 0 to 3 bedrooms display the widest range of reviews. This includes highly reviewed listings. This suggests that smaller property types dominate booking frequency in the market. 
  - Larger-bedroom-type listings (10+ bedrooms) are less common and have fewer reviews, which aligns with lower demand for very large property types.

 



