import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
#%matplotlib inline
import seaborn as sns

#reading data
data = pd.read_csv(r'listings.csv')

#created dataframe of relevant variables
df = pd.DataFrame(data, columns = ['neighbourhood_group','neighbourhood', 'room_type', 'price', 'minimum_nights','number_of_reviews'])
#print(df)

#cleaning/checking data

#checking datatype
#print(df.dtypes)
#checking for null values
#print(df.isnull().sum())
#renaming columns to make more sense
df_new = df.rename(columns={'neighbourhood_group':'Borough','neighbourhood':'Neighborhood','room_type':'Room_Type','price':'Price','minimum_nights':'Minimum_Nights','number_of_reviews':'Number_of_Reviews'})
#print(df_new)

#check for unique values
#print(df_new.Borough.unique())
#because there were so many different neighborhoods, we thought len would be better for analysis
#print(df_new.Neighborhood.unique())
#print(len(df_new.Neighborhood.unique()))
#print(df_new.Room_Type.unique())

#check to see which neighborhoods have the most Airbnb listings. shows top 25 neighborhoods
top_neighborhoods = df_new.Neighborhood.value_counts().head(25)
#print(top_neighborhoods)
#create table to show data (for map analysis later)
top_neighborhoods_df=pd.DataFrame(top_neighborhoods)
top_neighborhoods_df.reset_index(inplace=True)
top_neighborhoods_df.rename(columns={'index':'Neighborhood','Neighborhood':'Number of Listings'}, inplace=True)
print(top_neighborhoods_df)

#bar graph
neighborhood_bar=sns.barplot(x='Neighborhood', y='Number of Listings',data=top_neighborhoods_df, palette='Greens_d')
neighborhood_bar.set_title('Number of Listings by Neighborhood')
neighborhood_bar.set_xlabel('Neighborhood')
neighborhood_bar.set_ylabel('Number of Listings')
neighborhood_bar.set_xticklabels(neighborhood_bar.get_xticklabels(), rotation=45)
plt.show()