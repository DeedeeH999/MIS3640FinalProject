import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
from bokeh.plotting import ColumnDataSource, figure, output_file, show
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import r2_score

"""reading data"""
data = pd.read_csv(r"team_project/listings.csv") #for when deedee is coding
#data = pd.read_csv(r"listings.csv") #for when julia is coding

"""created dataframe of relevant variables"""
df = pd.DataFrame(data, columns = ['neighbourhood', 'room_type', 'price', 'minimum_nights','number_of_reviews', 'latitude', 'longitude'])
# print(df) #3254 rows and 7 columns

#cleaning/checking data
"""checking datatype"""
# print(df.dtypes)
"""checking for null values"""
# print(df.isnull().sum())
"""renaming columns to make more sense"""
df_new = df.rename(columns={'neighbourhood':'Neighborhood','room_type':'Room_Type','price':'Price','minimum_nights':'Minimum_Nights','number_of_reviews':'Number_of_Reviews', 'latitude':"Latitude", 'longitude':'Longitude'})
# print(df_new)

"""check for unique values"""
# print(df_new.Neighborhood.unique())
"""because there were so many different neighborhoods, we thought len would be better for analysis"""
# print(len(df_new.Neighborhood.unique())) #25 Neighborhoods
# print(df_new.Room_Type.unique())

"""check to see which neighborhoods have the most Airbnb listings. shows top 10 neighborhoods"""
top_neighborhoods = df_new.Neighborhood.value_counts().head(10)
# print(top_neighborhoods)
"""create table to show data (for map analysis later)"""
top_neighborhoods_df=pd.DataFrame(top_neighborhoods)
top_neighborhoods_df.reset_index(inplace=True)
top_neighborhoods_df.rename(columns={'index':'Neighborhood','Neighborhood':'Number of Listings'}, inplace=True)
# print(top_neighborhoods_df)

"""BAR GRAPH"""
neighborhood_bar=sns.barplot(x='Neighborhood', y='Number of Listings',data=top_neighborhoods_df, palette='Greens_d')
neighborhood_bar.set_title('Number of Listings by Neighborhood')
neighborhood_bar.set_xlabel('Neighborhood')
neighborhood_bar.set_ylabel('Number of Listings')
neighborhood_bar.set_xticklabels(neighborhood_bar.get_xticklabels(), rotation=45)
# plt.show()

"""price distribution by Neighborhood on a map"""
"""convert latitdue and longitude to mercator values to plot on a map"""
average_prices_df = pd.read_csv(r"team_project/average_prices_final.csv") #for deedee
# average_prices_df = pd.read_csv(r"Average Prices Final.csv") #for julia

"""Dorchester"""
dorchester_price=df_new.loc[df_new['Neighborhood'] == 'Dorchester']
price_dorchester=dorchester_price[['Price']]
"""Downtown"""
downtown_price=df_new.loc[df_new['Neighborhood'] == 'Downtown']
price_downtown=downtown_price[['Price']]
"""Jamaica Plain"""
jamaicaplain_price=df_new.loc[df_new['Neighborhood'] == 'Jamaica Plain']
price_jamaicaplain=jamaicaplain_price[['Price']]
"""Brighton"""
brighton_price=df_new.loc[df_new['Neighborhood'] == 'Brighton']
price_brighton=brighton_price[['Price']]
"""Roxbury"""
roxbury_price=df_new.loc[df_new['Neighborhood'] == 'Roxbury']
price_roxbury=roxbury_price[['Price']]

"""putting all the prices' dfs in the list"""
price_list=[price_dorchester, price_downtown, price_jamaicaplain, price_brighton, price_roxbury]
# print(price_list)
"""creating an empty list"""
price_list_dist=[]
"""creating list for Neighborhood column"""
neighborhood_list=['Dorchester', 'Downtown', 'Jamaica Plain', 'Brighton', 'Roxbury']
"""creating a for loop to get statistics for price ranges and append it to our empty list"""
for x in price_list:
    i=x.describe(percentiles=[.25, .50, .75])
    i=i.iloc[3:]
    i.reset_index(inplace=True)
    i.rename(columns={'index':'Stats'}, inplace=True)
    price_list_dist.append(i)
"""changing names of the price column to the Borough name"""   
price_list_dist[0].rename(columns={'Price':neighborhood_list[0]}, inplace=True)
price_list_dist[1].rename(columns={'Price':neighborhood_list[1]}, inplace=True)
price_list_dist[2].rename(columns={'Price':neighborhood_list[2]}, inplace=True)
price_list_dist[3].rename(columns={'Price':neighborhood_list[3]}, inplace=True)
price_list_dist[4].rename(columns={'Price':neighborhood_list[4]}, inplace=True)
"""finilizing our dataframe for final view"""    
stat_df=price_list_dist
stat_df=[df.set_index('Stats') for df in stat_df]
stat_df=stat_df[0].join(stat_df[1:])
# print(stat_df)

"""sort by room type"""
sub_7=df_new.loc[df_new['Neighborhood'].isin(['Dorchester','Downtown','Jamaica Plain','Brighton',
                 'Roxbury','South End','Back Bay','East Boston','Allston','South Boston'])]
viz_3=sns.catplot(x='Neighborhood', col='Room_Type', data=sub_7, kind='count')
viz_3.set_xticklabels(rotation=90) 
# plt.show()

"""map of neighborhoods"""
plt.figure(figsize=(10,6))
sns.scatterplot(df_new.Longitude,df_new.Latitude,hue=df_new.Neighborhood)
# plt.show()

"""Regression model"""
df_new.drop(['Latitude','Longitude'], axis=1, inplace=True)
"""examing the changes"""
# print(df_new)
"""encoding input variables"""
def input_var(data):
    for column in data.columns[data.columns.isin(['Neighborhood', 'Room_Type'])]:
        data[column] = data[column].factorize()[0]
    return data
df_en = input_var(df_new.copy())
print(df_en.head(10))
"""get Correlation between different variables"""
corr = df_en.corr(method='kendall')
plt.figure(figsize=(18,12))
sns.heatmap(corr, annot=True)
# plt.show()
"""independent variables and dependent variables"""
x = df_en.iloc[:,[0,1,3,4]]
y = df_en['Price']
"""Getting Test and Training Set"""
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=.2,random_state=1000)
# print(x_test.shape)
# print(x_train.shape)
# print(y_train.head())

"""prepare a regression model""" 
regression = LinearRegression()
regression.fit(x_train, y_train)
y_pred = regression.predict(x_test) #unsure, what is this trying to do 
# print(r2_score(y_test, y_pred))


"""MAP"""
# import geopy
# from geopy.geocoders import Nominatim, GoogleV3
# # geolocator = GoogleV3()
# geolocator = Nominatim()

