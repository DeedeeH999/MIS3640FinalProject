import pandas as pd 

data = pd.read_csv(r'listings.csv')
df = pd.DataFrame(data, columns = ['neighbourhood_group','neighbourhood', 'room_type', 'price', 'minimum_nights','number_of_reviews'])
print(df)