#### SER541: Experimentation

#### Mexico City Airbnb Price Prediction

#### Aman Sharma

#### 2026-04-16

## Explainable Records

### Record 1

**Raw Data:**  
`id`: 386306  
`price`: 2594.0  
`accommodates`: 4  
`bedrooms`: 2.0  
`number_of_reviews`: 61  
`room_type`: Entire home/apt

**Prediction Explanation:**  
This listing is an entire home/apartment that accommodates four guests and has two bedrooms, which suggests a relatively large and private space. In the Airbnb domain, entire homes typically command higher prices than private rooms because guests are paying for complete privacy and exclusive access to the property. A two-bedroom unit also indicates that the property is suitable for families or small groups, which increases its value. The model predicting a higher price for a listing with these characteristics is therefore reasonable.

### Record 2

**Raw Data:**  
`id`: 48744328  
`price`: 605.0  
`accommodates`: 2  
`bedrooms`: 1.0  
`number_of_reviews`: 3  
`room_type`: Private room

**Prediction Explanation:**  
This listing is a private room for only two guests with one bedroom and very few reviews. In the Airbnb market, private rooms usually cost less than entire homes because guests are renting only part of a property and do not receive the same level of privacy. A smaller guest capacity also points to a smaller listing overall. Because of that, it is reasonable for the model to predict a lower price for this record than for a larger entire-home listing.

## Interesting Features

### Feature A

**Feature:** accommodates

**Justification:**  
The number of guests a listing can accommodate is directly related to the size and utility of the property. In the Airbnb domain, listings that can host more people are usually larger and can be marketed to families or groups, so they often have higher prices.

### Feature B

**Feature:** bedrooms

**Justification:**  
The number of bedrooms is another strong indicator of listing size and comfort. More bedrooms usually mean more usable private space, which increases the value of the property and makes higher pricing reasonable.

### Feature C

**Feature:** room_type

**Justification:**  
Room type is important because it reflects the kind of experience the guest is purchasing. An entire home/apartment provides more privacy and full access to the property, while a private room usually offers less space and less privacy. This difference strongly affects pricing in Airbnb markets.

## Experiments

### Varying A

**Prediction Trend Seen:**  
When only `accommodates` is increased while the other features are held constant, the predicted price generally increases. This suggests that the model has learned that larger guest capacity is associated with more expensive listings.

### Varying B

**Prediction Trend Seen:**  
When only `bedrooms` is increased while the other features remain fixed, the predicted price also tends to increase. This is consistent with the idea that additional bedrooms reflect a larger and more valuable property.

### Varying C

**Prediction Trend Seen:**  
When `room_type` is changed from `Private room` to `Entire home/apt` while the numeric features remain fixed, the predicted price increases noticeably. This suggests that the model recognizes privacy and full-property access as strong contributors to listing price.

### Varying A and B together

**Prediction Trend Seen:**  
When `accommodates` and `bedrooms` are increased together, the predicted price rises more clearly than when only one of them changes. This indicates that the model treats larger guest capacity and more bedrooms as reinforcing signals of a larger and more expensive property.

### Varying B and C together

**Prediction Trend Seen:**  
When `bedrooms` increases and `room_type` is set to `Entire home/apt`, the prediction tends to increase more than with either change alone. This makes domain sense because a multi-bedroom entire home is typically more premium than a similarly sized private room listing.

### Varying A and C together

**Prediction Trend Seen:**  
When `accommodates` increases and `room_type` changes to `Entire home/apt`, the predicted price increases strongly. This suggests that the model treats larger capacity plus full-property rental as a particularly valuable combination.

### Varying A and B inversely

**Prediction Trend Seen:**  
When `accommodates` increases but `bedrooms` decreases, the prediction still changes, but less strongly than when both increase together. This suggests the model uses both features jointly and that the most expensive listings are generally those where both capacity and bedrooms support a larger property size.

### Varying B and C inversely

**Prediction Trend Seen:**  
When `bedrooms` increases but `room_type` stays as `Private room`, the prediction increases somewhat, but not as much as when the room type is also upgraded to `Entire home/apt`. This suggests that bedroom count matters, but privacy level still strongly shapes expected price.

### Varying A and C inversely

**Prediction Trend Seen:**  
When `accommodates` increases but `room_type` remains `Private room`, the prediction increases less than it does for an entire-home listing with the same capacity. This shows that the model does not rely on guest capacity alone; it also accounts for the listing category and guest experience.
