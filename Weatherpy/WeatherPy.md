
# Weather Analysis
Whats the weather like?

Observable trends in the data 

1.	There is an inverse relationship between the latitude and temperature.  Lower latitudes have higher temperatures and the higher latitudes have lower temperatures.
2.	There is not much of a correlation between latitude and the humidity. This is because of the wide dispersion of the latitude values covering the entire globe.
3.	From the scatter plot it is very difficult to conclusively state a relationship between latitude and cloudiness.
4.	There is not much of correlation between Latitude and windspeed as well. It can be observed from the scatter plots that most of the regions had windspeeds of 0 to 10 mph. Windspeeds did not go beyond 30 mph in any of the regions. 
5.	The data samples were taken with respect to a 24 hr window and hence not much of conclusive relationship could be determined.


```python
# import required modules
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import json
from citipy import citipy 
from pprint import pprint
from datetime import datetime
import seaborn as sns
```


```python
api_key ="d33aebe16f59ddc1bc6dc0df5ee18ec1"
gkey = "AIzaSyAPZr-4j860PQcTm6mhG1gZA76eoljd8pM"
```


```python
#creating a empy data frame to hold list of cities
list_of_cities = pd.DataFrame()
list_of_cities["Latitude"] = ""
list_of_cities["Longitude"] = ""
```

# Generate Cities list


```python
# Randomly generate the lattitude and longitude
list_of_cities["Latitude"] = [np.random.uniform(-90, 90) for x in range(1500)]
list_of_cities["Longitude"] = [np.random.uniform(-180, 180) for x in range(1500)]

# find the nearest city and country based on latitude and lattitude

for index, row in list_of_cities.iterrows():
    lat = row["Latitude"]
    lng = row["Longitude"]
    list_of_cities.set_value(index, "City", citipy.nearest_city(lat, lng).city_name)
    list_of_cities.set_value(index, "Country", citipy.nearest_city(lat, lng).country_code)


```

    C:\ProgramData\Anaconda3\lib\site-packages\ipykernel_launcher.py:10: FutureWarning: set_value is deprecated and will be removed in a future release. Please use .at[] or .iat[] accessors instead
      # Remove the CWD from sys.path while we load stuff.
    C:\ProgramData\Anaconda3\lib\site-packages\ipykernel_launcher.py:11: FutureWarning: set_value is deprecated and will be removed in a future release. Please use .at[] or .iat[] accessors instead
      # This is added back by InteractiveShellApp.init_path()
    


```python
# Delete duplicate rows in the dataframe
list_of_cities = list_of_cities.drop_duplicates(['City', 'Country'])
list_of_cities = list_of_cities.dropna()

# Update data frame to just city and country column and 500 values
list_of_cities = list_of_cities[["City", "Country"]]
list_of_cities = list_of_cities.iloc[:500]
```


```python
#reset index and display
list_of_cities = list_of_cities.reset_index(drop = True)
list_of_cities.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>City</th>
      <th>Country</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>port macquarie</td>
      <td>au</td>
    </tr>
    <tr>
      <th>1</th>
      <td>saint-philippe</td>
      <td>re</td>
    </tr>
    <tr>
      <th>2</th>
      <td>tubuala</td>
      <td>pa</td>
    </tr>
    <tr>
      <th>3</th>
      <td>torbay</td>
      <td>ca</td>
    </tr>
    <tr>
      <th>4</th>
      <td>de aar</td>
      <td>za</td>
    </tr>
  </tbody>
</table>
</div>



# Perform API Calls


```python
# Perform API calls and display the new results 
list_of_cities["Cloudiness"] = ""
list_of_cities["Humidity"] = ""
list_of_cities["Latitude"] = ""
list_of_cities["Longitude"] = ""
list_of_cities["Temperature"] = ""
list_of_cities["Wind Speed"] = ""
list_of_cities["Date"] =""
```


```python
# Create row counter and set it to one
count = 1
# Create a dictionary with parameters
settings = {"appid": api_key, "units": "imperial"}
# Create a base url
base_url = "http://api.openweathermap.org/data/2.5/weather?"
# Create query url
query_url = f"{base_url}appid={settings['appid']}&units={settings['units']}&q="

# use iterrows to include city in query URL
print("Beginning Data Retrieval")
print("---------------------------")

for index, row in list_of_cities.iterrows():
    try:
        cities_response = requests.get(query_url + row["City"] + "," + row["Country"]).json()
        pprint(f"Processing Record {count} | {row['City']}, {row['Country']}")
        print(cities_response)
        # Update row counter
        count = count + 1
        
        # create variables to retrieve data from API
        list_of_cities.set_value(index, "Cloudiness", cities_response['clouds']['all'])
        list_of_cities.set_value(index, "Date", cities_response['dt'])
        list_of_cities.set_value(index, "Humidity", cities_response['main']['humidity'])
        list_of_cities.set_value(index, "Latitude", cities_response['coord']['lat'])
        list_of_cities.set_value(index, "Longitude", cities_response['coord']['lon'])
        list_of_cities.set_value(index, "Max Temperature", cities_response['main']['temp_max'])
        list_of_cities.set_value(index, "Wind Speed", cities_response['wind']['speed'])
    except:
        print(f"**Weather data does not exist for {row['City']}, {row['Country']}**")
        continue
    
print("---------------------------")
print("Data Retrieval Complete")
print("---------------------------")

```

    Beginning Data Retrieval
    ---------------------------
    'Processing Record 1 | port macquarie, au'
    {'coord': {'lon': 152.91, 'lat': -31.43}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 60.8, 'pressure': 1025, 'humidity': 72, 'temp_min': 60.8, 'temp_max': 60.8}, 'visibility': 10000, 'wind': {'speed': 5.82, 'deg': 210}, 'clouds': {'all': 90}, 'dt': 1529553600, 'sys': {'type': 1, 'id': 8239, 'message': 0.0041, 'country': 'AU', 'sunrise': 1529527625, 'sunset': 1529563986}, 'id': 2152659, 'name': 'Port Macquarie', 'cod': 200}
    'Processing Record 2 | saint-philippe, re'
    {'coord': {'lon': 55.77, 'lat': -21.36}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 68.22, 'pressure': 1021, 'humidity': 53, 'temp_min': 66.2, 'temp_max': 71.6}, 'visibility': 10000, 'wind': {'speed': 8.05, 'deg': 30}, 'clouds': {'all': 75}, 'dt': 1529551800, 'sys': {'type': 1, 'id': 6792, 'message': 0.008, 'country': 'RE', 'sunrise': 1529549625, 'sunset': 1529588620}, 'id': 935215, 'name': 'Saint-Philippe', 'cod': 200}
    'Processing Record 3 | tubuala, pa'
    {'coord': {'lon': -79.03, 'lat': 9.52}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'base': 'stations', 'main': {'temp': 77, 'pressure': 1013, 'humidity': 88, 'temp_min': 77, 'temp_max': 77}, 'visibility': 10000, 'wind': {'speed': 4.7, 'deg': 40}, 'clouds': {'all': 40}, 'dt': 1529553600, 'sys': {'type': 1, 'id': 4230, 'message': 0.0046, 'country': 'PA', 'sunrise': 1529578654, 'sunset': 1529624305}, 'id': 3700393, 'name': 'Tubuala', 'cod': 200}
    

    C:\ProgramData\Anaconda3\lib\site-packages\ipykernel_launcher.py:23: FutureWarning: set_value is deprecated and will be removed in a future release. Please use .at[] or .iat[] accessors instead
    C:\ProgramData\Anaconda3\lib\site-packages\ipykernel_launcher.py:24: FutureWarning: set_value is deprecated and will be removed in a future release. Please use .at[] or .iat[] accessors instead
    C:\ProgramData\Anaconda3\lib\site-packages\ipykernel_launcher.py:25: FutureWarning: set_value is deprecated and will be removed in a future release. Please use .at[] or .iat[] accessors instead
    C:\ProgramData\Anaconda3\lib\site-packages\ipykernel_launcher.py:26: FutureWarning: set_value is deprecated and will be removed in a future release. Please use .at[] or .iat[] accessors instead
    C:\ProgramData\Anaconda3\lib\site-packages\ipykernel_launcher.py:27: FutureWarning: set_value is deprecated and will be removed in a future release. Please use .at[] or .iat[] accessors instead
    C:\ProgramData\Anaconda3\lib\site-packages\ipykernel_launcher.py:28: FutureWarning: set_value is deprecated and will be removed in a future release. Please use .at[] or .iat[] accessors instead
    C:\ProgramData\Anaconda3\lib\site-packages\ipykernel_launcher.py:29: FutureWarning: set_value is deprecated and will be removed in a future release. Please use .at[] or .iat[] accessors instead
    

    'Processing Record 4 | torbay, ca'
    {'coord': {'lon': -52.73, 'lat': 47.66}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 51.8, 'pressure': 1006, 'humidity': 71, 'temp_min': 51.8, 'temp_max': 51.8}, 'visibility': 24140, 'wind': {'speed': 20.8, 'deg': 260, 'gust': 12.3}, 'clouds': {'all': 90}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 3467, 'message': 0.005, 'country': 'CA', 'sunrise': 1529566374, 'sunset': 1529623958}, 'id': 6167817, 'name': 'Torbay', 'cod': 200}
    'Processing Record 5 | de aar, za'
    {'coord': {'lon': 24.01, 'lat': -30.65}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 32.76, 'pressure': 888.44, 'humidity': 79, 'temp_min': 32.76, 'temp_max': 32.76, 'sea_level': 1038.07, 'grnd_level': 888.44}, 'wind': {'speed': 5.64, 'deg': 341.503}, 'clouds': {'all': 0}, 'dt': 1529554542, 'sys': {'message': 0.0033, 'country': 'ZA', 'sunrise': 1529558454, 'sunset': 1529595038}, 'id': 1011632, 'name': 'De Aar', 'cod': 200}
    'Processing Record 6 | rikitea, pf'
    {'coord': {'lon': -134.97, 'lat': -23.12}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'base': 'stations', 'main': {'temp': 73.8, 'pressure': 1032.48, 'humidity': 100, 'temp_min': 73.8, 'temp_max': 73.8, 'sea_level': 1032.6, 'grnd_level': 1032.48}, 'wind': {'speed': 6.98, 'deg': 21.0034}, 'clouds': {'all': 32}, 'dt': 1529554542, 'sys': {'message': 0.0037, 'country': 'PF', 'sunrise': 1529595623, 'sunset': 1529634191}, 'id': 4030556, 'name': 'Rikitea', 'cod': 200}
    'Processing Record 7 | otradnoye, ru'
    {'coord': {'lon': 30.8, 'lat': 59.77}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 55.4, 'pressure': 1007, 'humidity': 66, 'temp_min': 55.4, 'temp_max': 55.4}, 'visibility': 10000, 'wind': {'speed': 6.71, 'deg': 260}, 'clouds': {'all': 0}, 'dt': 1529551800, 'sys': {'type': 1, 'id': 7267, 'message': 0.029, 'country': 'RU', 'sunrise': 1529541310, 'sunset': 1529608921}, 'id': 513898, 'name': 'Otradnoye', 'cod': 200}
    'Processing Record 8 | kapaa, us'
    {'coord': {'lon': -159.32, 'lat': 22.08}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'base': 'stations', 'main': {'temp': 80.6, 'pressure': 1016, 'humidity': 74, 'temp_min': 80.6, 'temp_max': 80.6}, 'visibility': 16093, 'wind': {'speed': 9.17, 'deg': 50}, 'clouds': {'all': 40}, 'dt': 1529553360, 'sys': {'type': 1, 'id': 833, 'message': 0.0072, 'country': 'US', 'sunrise': 1529596479, 'sunset': 1529645025}, 'id': 5848280, 'name': 'Kapaa', 'cod': 200}
    'Processing Record 9 | ushuaia, ar'
    {'coord': {'lon': -68.31, 'lat': -54.81}, 'weather': [{'id': 602, 'main': 'Snow', 'description': 'heavy snow', 'icon': '13n'}], 'base': 'stations', 'main': {'temp': 30.2, 'pressure': 984, 'humidity': 92, 'temp_min': 30.2, 'temp_max': 30.2}, 'visibility': 1000, 'wind': {'speed': 17.22, 'deg': 250, 'gust': 14.4}, 'clouds': {'all': 90}, 'dt': 1529553600, 'sys': {'type': 1, 'id': 4754, 'message': 0.0033, 'country': 'AR', 'sunrise': 1529585934, 'sunset': 1529611878}, 'id': 3833367, 'name': 'Ushuaia', 'cod': 200}
    'Processing Record 10 | labutta, mm'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for labutta, mm**
    'Processing Record 11 | puerto ayora, ec'
    {'coord': {'lon': -90.35, 'lat': -0.74}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 71.37, 'pressure': 1020.57, 'humidity': 100, 'temp_min': 71.37, 'temp_max': 71.37, 'sea_level': 1027.66, 'grnd_level': 1020.57}, 'wind': {'speed': 11.45, 'deg': 177.003}, 'clouds': {'all': 20}, 'dt': 1529554357, 'sys': {'message': 0.0041, 'country': 'EC', 'sunrise': 1529582452, 'sunset': 1529625941}, 'id': 3652764, 'name': 'Puerto Ayora', 'cod': 200}
    'Processing Record 12 | coquimbo, cl'
    {'coord': {'lon': -71.34, 'lat': -29.95}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 44.6, 'pressure': 1019, 'humidity': 100, 'temp_min': 44.6, 'temp_max': 44.6}, 'visibility': 8000, 'wind': {'speed': 3.36, 'deg': 120}, 'clouds': {'all': 24}, 'dt': 1529553600, 'sys': {'type': 1, 'id': 4666, 'message': 0.0041, 'country': 'CL', 'sunrise': 1529581243, 'sunset': 1529618024}, 'id': 3893629, 'name': 'Coquimbo', 'cod': 200}
    'Processing Record 13 | nkowakowa, za'
    {'coord': {'lon': 30.29, 'lat': -23.89}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10n'}], 'base': 'stations', 'main': {'temp': 50.67, 'pressure': 905.87, 'humidity': 97, 'temp_min': 50.67, 'temp_max': 50.67, 'sea_level': 1040.3, 'grnd_level': 905.87}, 'wind': {'speed': 0.94, 'deg': 73.0034}, 'rain': {'3h': 0.29}, 'clouds': {'all': 88}, 'dt': 1529554543, 'sys': {'message': 0.0038, 'country': 'ZA', 'sunrise': 1529556050, 'sunset': 1529594427}, 'id': 970341, 'name': 'Nkowakowa', 'cod': 200}
    'Processing Record 14 | ust-kamchatsk, ru'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for ust-kamchatsk, ru**
    'Processing Record 15 | cape town, za'
    {'coord': {'lon': 18.42, 'lat': -33.93}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 42.8, 'pressure': 1020, 'humidity': 93, 'temp_min': 42.8, 'temp_max': 42.8}, 'visibility': 10000, 'wind': {'speed': 4.7, 'deg': 20}, 'clouds': {'all': 0}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 6529, 'message': 0.0049, 'country': 'ZA', 'sunrise': 1529560281, 'sunset': 1529595895}, 'id': 3369157, 'name': 'Cape Town', 'cod': 200}
    'Processing Record 16 | east london, za'
    {'coord': {'lon': 27.91, 'lat': -33.02}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 55.4, 'pressure': 1023, 'humidity': 71, 'temp_min': 55.4, 'temp_max': 55.4}, 'visibility': 10000, 'wind': {'speed': 9.17, 'deg': 10}, 'clouds': {'all': 0}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 6538, 'message': 0.0039, 'country': 'ZA', 'sunrise': 1529557864, 'sunset': 1529593756}, 'id': 1006984, 'name': 'East London', 'cod': 200}
    'Processing Record 17 | saint-denis, re'
    {'coord': {'lon': 55.47, 'lat': -20.87}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 68.88, 'pressure': 1021, 'humidity': 53, 'temp_min': 66.2, 'temp_max': 71.6}, 'visibility': 10000, 'wind': {'speed': 8.05, 'deg': 30}, 'clouds': {'all': 75}, 'dt': 1529551800, 'sys': {'type': 1, 'id': 6792, 'message': 0.0157, 'country': 'RE', 'sunrise': 1529549639, 'sunset': 1529588751}, 'id': 6690295, 'name': 'Saint-Denis', 'cod': 200}
    'Processing Record 18 | havre-saint-pierre, ca'
    {'coord': {'lon': -63.6, 'lat': 50.23}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'base': 'stations', 'main': {'temp': 50, 'pressure': 998, 'humidity': 93, 'temp_min': 50, 'temp_max': 50}, 'visibility': 14484, 'wind': {'speed': 3.36, 'deg': 260}, 'clouds': {'all': 40}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 3785, 'message': 0.0039, 'country': 'CA', 'sunrise': 1529568236, 'sunset': 1529627315}, 'id': 5972291, 'name': 'Havre-Saint-Pierre', 'cod': 200}
    'Processing Record 19 | atuona, pf'
    {'coord': {'lon': -139.03, 'lat': -9.8}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'base': 'stations', 'main': {'temp': 80.91, 'pressure': 1026.16, 'humidity': 100, 'temp_min': 80.91, 'temp_max': 80.91, 'sea_level': 1026.24, 'grnd_level': 1026.16}, 'wind': {'speed': 11.79, 'deg': 95.5034}, 'clouds': {'all': 48}, 'dt': 1529554544, 'sys': {'message': 0.0044, 'country': 'PF', 'sunrise': 1529595087, 'sunset': 1529636676}, 'id': 4020109, 'name': 'Atuona', 'cod': 200}
    'Processing Record 20 | vostok, ru'
    {'coord': {'lon': 135.83, 'lat': 46.45}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 56.34, 'pressure': 946.23, 'humidity': 100, 'temp_min': 56.34, 'temp_max': 56.34, 'sea_level': 1009.58, 'grnd_level': 946.23}, 'wind': {'speed': 2.73, 'deg': 254.503}, 'rain': {'3h': 2.355}, 'clouds': {'all': 92}, 'dt': 1529554544, 'sys': {'message': 0.0033, 'country': 'RU', 'sunrise': 1529521433, 'sunset': 1529578378}, 'id': 2013279, 'name': 'Vostok', 'cod': 200}
    'Processing Record 21 | llanes, es'
    {'coord': {'lon': -4.75, 'lat': 43.42}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'base': 'stations', 'main': {'temp': 57.33, 'pressure': 929.54, 'humidity': 97, 'temp_min': 57.33, 'temp_max': 57.33, 'sea_level': 1034.06, 'grnd_level': 929.54}, 'wind': {'speed': 0.83, 'deg': 251.003}, 'clouds': {'all': 36}, 'dt': 1529554544, 'sys': {'message': 0.0038, 'country': 'ES', 'sunrise': 1529555902, 'sunset': 1529611396}, 'id': 3118304, 'name': 'Llanes', 'cod': 200}
    'Processing Record 22 | mys shmidta, ru'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for mys shmidta, ru**
    'Processing Record 23 | saint-augustin, ca'
    {'coord': {'lon': -73.98, 'lat': 45.63}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 65.73, 'pressure': 1008, 'humidity': 77, 'temp_min': 62.6, 'temp_max': 68}, 'visibility': 40233, 'wind': {'speed': 3.36, 'deg': 270}, 'clouds': {'all': 75}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 3831, 'message': 0.0069, 'country': 'CA', 'sunrise': 1529572001, 'sunset': 1529628533}, 'id': 6138501, 'name': 'Saint-Augustin', 'cod': 200}
    'Processing Record 24 | dagda, lv'
    {'coord': {'lon': 27.54, 'lat': 56.09}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 57.96, 'pressure': 1009.79, 'humidity': 76, 'temp_min': 57.96, 'temp_max': 57.96, 'sea_level': 1027.42, 'grnd_level': 1009.79}, 'wind': {'speed': 11.68, 'deg': 242.503}, 'clouds': {'all': 0}, 'dt': 1529554545, 'sys': {'message': 0.0035, 'country': 'LV', 'sunrise': 1529544138, 'sunset': 1529607659}, 'id': 460474, 'name': 'Dagda', 'cod': 200}
    'Processing Record 25 | safakulevo, ru'
    {'coord': {'lon': 62.54, 'lat': 54.99}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 61.74, 'pressure': 991.22, 'humidity': 64, 'temp_min': 61.74, 'temp_max': 61.74, 'sea_level': 1011.73, 'grnd_level': 991.22}, 'wind': {'speed': 18.61, 'deg': 289.503}, 'clouds': {'all': 0}, 'dt': 1529554545, 'sys': {'message': 0.0036, 'country': 'RU', 'sunrise': 1529536227, 'sunset': 1529598768}, 'id': 1493268, 'name': 'Safakulevo', 'cod': 200}
    'Processing Record 26 | castro, cl'
    {'coord': {'lon': -73.76, 'lat': -42.48}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10n'}], 'base': 'stations', 'main': {'temp': 45.36, 'pressure': 1016.43, 'humidity': 86, 'temp_min': 45.36, 'temp_max': 45.36, 'sea_level': 1031.35, 'grnd_level': 1016.43}, 'wind': {'speed': 11.56, 'deg': 250.003}, 'rain': {'3h': 0.16}, 'clouds': {'all': 88}, 'dt': 1529554545, 'sys': {'message': 0.0033, 'country': 'CL', 'sunrise': 1529583904, 'sunset': 1529616525}, 'id': 3896218, 'name': 'Castro', 'cod': 200}
    'Processing Record 27 | manchar, in'
    {'coord': {'lon': 73.94, 'lat': 19}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 75.24, 'pressure': 943.96, 'humidity': 96, 'temp_min': 75.24, 'temp_max': 75.24, 'sea_level': 1018.46, 'grnd_level': 943.96}, 'wind': {'speed': 4.97, 'deg': 276.003}, 'rain': {'3h': 0.315}, 'clouds': {'all': 92}, 'dt': 1529554545, 'sys': {'message': 0.0037, 'country': 'IN', 'sunrise': 1529540864, 'sunset': 1529588658}, 'id': 1263937, 'name': 'Manchar', 'cod': 200}
    'Processing Record 28 | busselton, au'
    {'coord': {'lon': 115.35, 'lat': -33.64}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 62.19, 'pressure': 1040.59, 'humidity': 100, 'temp_min': 62.19, 'temp_max': 62.19, 'sea_level': 1041.68, 'grnd_level': 1040.59}, 'wind': {'speed': 11.56, 'deg': 279.503}, 'rain': {'3h': 0.67}, 'clouds': {'all': 92}, 'dt': 1529554545, 'sys': {'message': 0.0034, 'country': 'AU', 'sunrise': 1529536969, 'sunset': 1529572673}, 'id': 2075265, 'name': 'Busselton', 'cod': 200}
    'Processing Record 29 | georgetown, sh'
    {'coord': {'lon': -14.42, 'lat': -7.93}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'base': 'stations', 'main': {'temp': 76.5, 'pressure': 1029.48, 'humidity': 100, 'temp_min': 76.5, 'temp_max': 76.5, 'sea_level': 1029.56, 'grnd_level': 1029.48}, 'wind': {'speed': 16.49, 'deg': 115.003}, 'clouds': {'all': 44}, 'dt': 1529554497, 'sys': {'message': 0.003, 'country': 'SH', 'sunrise': 1529564978, 'sunset': 1529606963}, 'id': 2411397, 'name': 'Georgetown', 'cod': 200}
    'Processing Record 30 | faanui, pf'
    {'coord': {'lon': -151.75, 'lat': -16.48}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 81.27, 'pressure': 1027.94, 'humidity': 99, 'temp_min': 81.27, 'temp_max': 81.27, 'sea_level': 1027.98, 'grnd_level': 1027.94}, 'wind': {'speed': 16.71, 'deg': 91.5034}, 'clouds': {'all': 88}, 'dt': 1529554546, 'sys': {'message': 0.0042, 'country': 'PF', 'sunrise': 1529598871, 'sunset': 1529638999}, 'id': 4034551, 'name': 'Faanui', 'cod': 200}
    'Processing Record 31 | saskylakh, ru'
    {'coord': {'lon': 114.09, 'lat': 71.97}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 'base': 'stations', 'main': {'temp': 59.22, 'pressure': 1010.03, 'humidity': 74, 'temp_min': 59.22, 'temp_max': 59.22, 'sea_level': 1021.25, 'grnd_level': 1010.03}, 'wind': {'speed': 8.77, 'deg': 77.0034}, 'clouds': {'all': 20}, 'dt': 1529554546, 'sys': {'message': 0.0034, 'country': 'RU', 'sunrise': 0, 'sunset': 0}, 'id': 2017155, 'name': 'Saskylakh', 'cod': 200}
    'Processing Record 32 | chernyshevskiy, ru'
    {'coord': {'lon': 112.47, 'lat': 63.01}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 64.44, 'pressure': 980.04, 'humidity': 47, 'temp_min': 64.44, 'temp_max': 64.44, 'sea_level': 1016.96, 'grnd_level': 980.04}, 'wind': {'speed': 3.51, 'deg': 45.5034}, 'clouds': {'all': 0}, 'dt': 1529554546, 'sys': {'message': 0.003, 'country': 'RU', 'sunrise': 1529518937, 'sunset': 1529592088}, 'id': 2025456, 'name': 'Chernyshevskiy', 'cod': 200}
    'Processing Record 33 | paradwip, in'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for paradwip, in**
    'Processing Record 34 | grand river south east, mu'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for grand river south east, mu**
    'Processing Record 35 | vestmanna, fo'
    {'coord': {'lon': -7.17, 'lat': 62.16}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 46.4, 'pressure': 1018, 'humidity': 75, 'temp_min': 46.4, 'temp_max': 46.4}, 'wind': {'speed': 31.09, 'deg': 320, 'gust': 19.5}, 'rain': {'3h': 0.235}, 'clouds': {'all': 88}, 'dt': 1529553000, 'sys': {'type': 1, 'id': 5266, 'message': 0.004, 'country': 'FO', 'sunrise': 1529548531, 'sunset': 1529619928}, 'id': 2610343, 'name': 'Vestmanna', 'cod': 200}
    'Processing Record 36 | port elizabeth, za'
    {'coord': {'lon': 25.57, 'lat': -33.92}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 41, 'pressure': 1021, 'humidity': 93, 'temp_min': 41, 'temp_max': 41}, 'visibility': 10000, 'wind': {'speed': 2.24, 'deg': 290}, 'clouds': {'all': 0}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 6596, 'message': 0.0033, 'country': 'ZA', 'sunrise': 1529558563, 'sunset': 1529594181}, 'id': 964420, 'name': 'Port Elizabeth', 'cod': 200}
    'Processing Record 37 | dikson, ru'
    {'coord': {'lon': 80.55, 'lat': 73.51}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 34.11, 'pressure': 1021.94, 'humidity': 91, 'temp_min': 34.11, 'temp_max': 34.11, 'sea_level': 1022.27, 'grnd_level': 1021.94}, 'wind': {'speed': 23.76, 'deg': 68.0034}, 'clouds': {'all': 0}, 'dt': 1529554491, 'sys': {'message': 0.0037, 'country': 'RU', 'sunrise': 0, 'sunset': 0}, 'id': 1507390, 'name': 'Dikson', 'cod': 200}
    'Processing Record 38 | port alfred, za'
    {'coord': {'lon': 26.89, 'lat': -33.59}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 60.3, 'pressure': 1025.11, 'humidity': 96, 'temp_min': 60.3, 'temp_max': 60.3, 'sea_level': 1034.22, 'grnd_level': 1025.11}, 'wind': {'speed': 9.89, 'deg': 57.5034}, 'clouds': {'all': 0}, 'dt': 1529554477, 'sys': {'message': 0.0102, 'country': 'ZA', 'sunrise': 1529558195, 'sunset': 1529593914}, 'id': 964432, 'name': 'Port Alfred', 'cod': 200}
    'Processing Record 39 | chipinge, zw'
    {'coord': {'lon': 32.62, 'lat': -20.19}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'base': 'stations', 'main': {'temp': 57.06, 'pressure': 963.99, 'humidity': 84, 'temp_min': 57.06, 'temp_max': 57.06, 'sea_level': 1037.06, 'grnd_level': 963.99}, 'wind': {'speed': 2.73, 'deg': 108.503}, 'clouds': {'all': 36}, 'dt': 1529554547, 'sys': {'message': 0.0039, 'country': 'ZW', 'sunrise': 1529555043, 'sunset': 1529594316}, 'id': 893549, 'name': 'Chipinge', 'cod': 200}
    'Processing Record 40 | punta arenas, cl'
    {'coord': {'lon': -70.91, 'lat': -53.16}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 32, 'pressure': 992, 'humidity': 100, 'temp_min': 32, 'temp_max': 32}, 'visibility': 10000, 'wind': {'speed': 20.8, 'deg': 260}, 'clouds': {'all': 20}, 'dt': 1529553600, 'sys': {'type': 1, 'id': 4642, 'message': 0.0054, 'country': 'CL', 'sunrise': 1529585972, 'sunset': 1529613089}, 'id': 3874787, 'name': 'Punta Arenas', 'cod': 200}
    'Processing Record 41 | richards bay, za'
    {'coord': {'lon': 32.06, 'lat': -28.77}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 61.56, 'pressure': 1019.92, 'humidity': 94, 'temp_min': 61.56, 'temp_max': 61.56, 'sea_level': 1038.2, 'grnd_level': 1019.92}, 'wind': {'speed': 7.65, 'deg': 6.50342}, 'clouds': {'all': 0}, 'dt': 1529554547, 'sys': {'message': 0.0033, 'country': 'ZA', 'sunrise': 1529556260, 'sunset': 1529593367}, 'id': 962367, 'name': 'Richards Bay', 'cod': 200}
    'Processing Record 42 | vardo, no'
    {'coord': {'lon': 31.11, 'lat': 70.37}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 42.8, 'pressure': 996, 'humidity': 100, 'temp_min': 42.8, 'temp_max': 42.8}, 'visibility': 10000, 'wind': {'speed': 19.46, 'deg': 50}, 'clouds': {'all': 75}, 'dt': 1529553000, 'sys': {'type': 1, 'id': 5342, 'message': 0.004, 'country': 'NO', 'sunrise': 0, 'sunset': 0}, 'id': 777019, 'name': 'Vardo', 'cod': 200}
    'Processing Record 43 | salinopolis, br'
    {'coord': {'lon': -47.36, 'lat': -0.61}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 78.48, 'pressure': 1028.83, 'humidity': 100, 'temp_min': 78.48, 'temp_max': 78.48, 'sea_level': 1028.91, 'grnd_level': 1028.83}, 'wind': {'speed': 14.03, 'deg': 119.503}, 'clouds': {'all': 64}, 'dt': 1529554803, 'sys': {'message': 0.0036, 'country': 'BR', 'sunrise': 1529572120, 'sunset': 1529615635}, 'id': 3389822, 'name': 'Salinopolis', 'cod': 200}
    'Processing Record 44 | hasaki, jp'
    {'coord': {'lon': 140.83, 'lat': 35.73}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 71.6, 'pressure': 1002, 'humidity': 88, 'temp_min': 71.6, 'temp_max': 71.6}, 'visibility': 10000, 'wind': {'speed': 6.93, 'deg': 170}, 'clouds': {'all': 75}, 'dt': 1529551800, 'sys': {'type': 1, 'id': 7505, 'message': 0.0034, 'country': 'JP', 'sunrise': 1529522457, 'sunset': 1529574953}, 'id': 2112802, 'name': 'Hasaki', 'cod': 200}
    'Processing Record 45 | koungou, yt'
    {'coord': {'lon': 45.2, 'lat': -12.73}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'base': 'stations', 'main': {'temp': 78.8, 'pressure': 1018, 'humidity': 83, 'temp_min': 78.8, 'temp_max': 78.8}, 'visibility': 10000, 'wind': {'speed': 12.75, 'deg': 180}, 'clouds': {'all': 40}, 'dt': 1529551800, 'sys': {'type': 1, 'id': 6790, 'message': 0.0047, 'country': 'YT', 'sunrise': 1529551181, 'sunset': 1529592138}, 'id': 1090225, 'name': 'Koungou', 'cod': 200}
    'Processing Record 46 | zamora, ec'
    {'coord': {'lon': -78.95, 'lat': -4.07}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 47.52, 'pressure': 804.22, 'humidity': 81, 'temp_min': 47.52, 'temp_max': 47.52, 'sea_level': 1028.1, 'grnd_level': 804.22}, 'wind': {'speed': 1.95, 'deg': 92.0034}, 'clouds': {'all': 0}, 'dt': 1529554548, 'sys': {'message': 0.0044, 'country': 'EC', 'sunrise': 1529580063, 'sunset': 1529622858}, 'id': 3649959, 'name': 'Zamora', 'cod': 200}
    'Processing Record 47 | hilo, us'
    {'coord': {'lon': -155.08, 'lat': 19.71}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 72.28, 'pressure': 1015, 'humidity': 65, 'temp_min': 66.2, 'temp_max': 80.6}, 'visibility': 16093, 'wind': {'speed': 10.29, 'deg': 120}, 'clouds': {'all': 75}, 'dt': 1529549760, 'sys': {'type': 1, 'id': 818, 'message': 0.0036, 'country': 'US', 'sunrise': 1529595752, 'sunset': 1529643716}, 'id': 5855927, 'name': 'Hilo', 'cod': 200}
    'Processing Record 48 | iracoubo, gf'
    {'coord': {'lon': -53.21, 'lat': 5.48}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 76.86, 'pressure': 1023.97, 'humidity': 84, 'temp_min': 76.86, 'temp_max': 76.86, 'sea_level': 1028.63, 'grnd_level': 1023.97}, 'wind': {'speed': 5.3, 'deg': 98.5034}, 'clouds': {'all': 12}, 'dt': 1529554549, 'sys': {'message': 0.0035, 'country': 'GF', 'sunrise': 1529572887, 'sunset': 1529617676}, 'id': 3381428, 'name': 'Iracoubo', 'cod': 200}
    'Processing Record 49 | monrovia, lr'
    {'coord': {'lon': -10.8, 'lat': 6.33}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10n'}], 'base': 'stations', 'main': {'temp': 73.98, 'pressure': 1017.89, 'humidity': 97, 'temp_min': 73.98, 'temp_max': 73.98, 'sea_level': 1028.47, 'grnd_level': 1017.89}, 'wind': {'speed': 5.3, 'deg': 305.503}, 'rain': {'3h': 0.355}, 'clouds': {'all': 100}, 'dt': 1529554549, 'sys': {'message': 0.0035, 'country': 'LR', 'sunrise': 1529562617, 'sunset': 1529607586}, 'id': 2274895, 'name': 'Monrovia', 'cod': 200}
    'Processing Record 50 | sakakah, sa'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for sakakah, sa**
    'Processing Record 51 | vigrestad, no'
    {'coord': {'lon': 5.7, 'lat': 58.57}, 'weather': [{'id': 521, 'main': 'Rain', 'description': 'shower rain', 'icon': '09d'}], 'base': 'stations', 'main': {'temp': 48.2, 'pressure': 1010, 'humidity': 76, 'temp_min': 48.2, 'temp_max': 48.2}, 'visibility': 10000, 'wind': {'speed': 5.82, 'deg': 330}, 'clouds': {'all': 40}, 'dt': 1529553000, 'sys': {'type': 1, 'id': 5343, 'message': 0.0029, 'country': 'NO', 'sunrise': 1529548087, 'sunset': 1529614194}, 'id': 3131824, 'name': 'Vigrestad', 'cod': 200}
    'Processing Record 52 | nome, us'
    {'coord': {'lon': -94.42, 'lat': 30.04}, 'weather': [{'id': 211, 'main': 'Thunderstorm', 'description': 'thunderstorm', 'icon': '11n'}, {'id': 701, 'main': 'Mist', 'description': 'mist', 'icon': '50n'}], 'base': 'stations', 'main': {'temp': 76.59, 'pressure': 1013, 'humidity': 94, 'temp_min': 75.2, 'temp_max': 80.6}, 'visibility': 16093, 'wind': {'speed': 6.42, 'deg': 132.503}, 'clouds': {'all': 40}, 'dt': 1529552700, 'sys': {'type': 1, 'id': 2561, 'message': 0.0069, 'country': 'US', 'sunrise': 1529579825, 'sunset': 1529630522}, 'id': 4732862, 'name': 'Nome', 'cod': 200}
    'Processing Record 53 | fortuna, us'
    {'coord': {'lon': -124.16, 'lat': 40.6}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 54.59, 'pressure': 1019, 'humidity': 87, 'temp_min': 53.6, 'temp_max': 55.4}, 'visibility': 16093, 'wind': {'speed': 5.82, 'deg': 300}, 'clouds': {'all': 90}, 'dt': 1529553600, 'sys': {'type': 1, 'id': 386, 'message': 0.0044, 'country': 'US', 'sunrise': 1529585163, 'sunset': 1529639460}, 'id': 5563839, 'name': 'Fortuna', 'cod': 200}
    'Processing Record 54 | mapiripan, co'
    {'coord': {'lon': -72.13, 'lat': 2.89}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 72.36, 'pressure': 995.6, 'humidity': 89, 'temp_min': 72.36, 'temp_max': 72.36, 'sea_level': 1028.35, 'grnd_level': 995.6}, 'wind': {'speed': 3.18, 'deg': 145.503}, 'clouds': {'all': 12}, 'dt': 1529554549, 'sys': {'message': 0.0038, 'country': 'CO', 'sunrise': 1529577701, 'sunset': 1529621946}, 'id': 3792394, 'name': 'Mapiripan', 'cod': 200}
    'Processing Record 55 | lavrentiya, ru'
    {'coord': {'lon': -170.99, 'lat': 65.58}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 39.69, 'pressure': 1025.92, 'humidity': 93, 'temp_min': 39.69, 'temp_max': 39.69, 'sea_level': 1029.97, 'grnd_level': 1025.92}, 'wind': {'speed': 9.55, 'deg': 3.50342}, 'clouds': {'all': 8}, 'dt': 1529554550, 'sys': {'message': 0.0037, 'country': 'RU', 'sunrise': 1529581974, 'sunset': 1529665107}, 'id': 4031637, 'name': 'Lavrentiya', 'cod': 200}
    'Processing Record 56 | nicoya, cr'
    {'coord': {'lon': -85.45, 'lat': 10.15}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 73.4, 'pressure': 1015, 'humidity': 100, 'temp_min': 73.4, 'temp_max': 73.4}, 'visibility': 10000, 'wind': {'speed': 4.7, 'deg': 180}, 'clouds': {'all': 75}, 'dt': 1529553600, 'sys': {'type': 1, 'id': 4217, 'message': 0.0032, 'country': 'CR', 'sunrise': 1529580127, 'sunset': 1529625914}, 'id': 3622716, 'name': 'Nicoya', 'cod': 200}
    'Processing Record 57 | yaan, cn'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for yaan, cn**
    'Processing Record 58 | calmar, ca'
    {'coord': {'lon': -113.81, 'lat': 53.27}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'base': 'stations', 'main': {'temp': 76.21, 'pressure': 1013, 'humidity': 47, 'temp_min': 75.2, 'temp_max': 77}, 'visibility': 24140, 'wind': {'speed': 9.17, 'deg': 140}, 'clouds': {'all': 40}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 3158, 'message': 0.0041, 'country': 'CA', 'sunrise': 1529579247, 'sunset': 1529640408}, 'id': 5913601, 'name': 'Calmar', 'cod': 200}
    'Processing Record 59 | dzhusaly, kz'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for dzhusaly, kz**
    'Processing Record 60 | hobart, au'
    {'coord': {'lon': 147.33, 'lat': -42.88}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'base': 'stations', 'main': {'temp': 55.4, 'pressure': 1023, 'humidity': 43, 'temp_min': 55.4, 'temp_max': 55.4}, 'visibility': 10000, 'wind': {'speed': 11.41, 'deg': 290}, 'clouds': {'all': 40}, 'dt': 1529551800, 'sys': {'type': 1, 'id': 8195, 'message': 0.0227, 'country': 'AU', 'sunrise': 1529530916, 'sunset': 1529563374}, 'id': 2163355, 'name': 'Hobart', 'cod': 200}
    'Processing Record 61 | bukachacha, ru'
    {'coord': {'lon': 116.91, 'lat': 52.99}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 75.24, 'pressure': 925.08, 'humidity': 56, 'temp_min': 75.24, 'temp_max': 75.24, 'sea_level': 1015.78, 'grnd_level': 925.08}, 'wind': {'speed': 3.4, 'deg': 231.003}, 'clouds': {'all': 0}, 'dt': 1529554550, 'sys': {'message': 0.0034, 'country': 'RU', 'sunrise': 1529523970, 'sunset': 1529584923}, 'id': 2026023, 'name': 'Bukachacha', 'cod': 200}
    'Processing Record 62 | beni, cd'
    {'coord': {'lon': 29.47, 'lat': 0.49}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 62.82, 'pressure': 917.62, 'humidity': 98, 'temp_min': 62.82, 'temp_max': 62.82, 'sea_level': 1028.79, 'grnd_level': 917.62}, 'wind': {'speed': 3.18, 'deg': 116.503}, 'rain': {'3h': 1.43}, 'clouds': {'all': 88}, 'dt': 1529554551, 'sys': {'message': 0.0033, 'country': 'CD', 'sunrise': 1529553563, 'sunset': 1529597308}, 'id': 219057, 'name': 'Beni', 'cod': 200}
    'Processing Record 63 | taolanaro, mg'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for taolanaro, mg**
    'Processing Record 64 | luderitz, na'
    {'coord': {'lon': 15.16, 'lat': -26.65}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 50.22, 'pressure': 1019.92, 'humidity': 87, 'temp_min': 50.22, 'temp_max': 50.22, 'sea_level': 1034.67, 'grnd_level': 1019.92}, 'wind': {'speed': 6.31, 'deg': 155.503}, 'clouds': {'all': 0}, 'dt': 1529554551, 'sys': {'message': 0.0042, 'country': 'NA', 'sunrise': 1529560034, 'sunset': 1529597707}, 'id': 3355672, 'name': 'Luderitz', 'cod': 200}
    'Processing Record 65 | road town, vg'
    {'coord': {'lon': -64.62, 'lat': 18.42}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 78.8, 'pressure': 1018, 'humidity': 83, 'temp_min': 78.8, 'temp_max': 78.8}, 'visibility': 16093, 'wind': {'speed': 3.36, 'deg': 80}, 'clouds': {'all': 20}, 'dt': 1529553180, 'sys': {'type': 1, 'id': 4137, 'message': 0.0081, 'country': 'VG', 'sunrise': 1529574192, 'sunset': 1529621848}, 'id': 3577430, 'name': 'Road Town', 'cod': 200}
    'Processing Record 66 | nikolskoye, ru'
    {'coord': {'lon': 30.79, 'lat': 59.7}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 55.4, 'pressure': 1007, 'humidity': 66, 'temp_min': 55.4, 'temp_max': 55.4}, 'visibility': 10000, 'wind': {'speed': 6.71, 'deg': 260}, 'clouds': {'all': 0}, 'dt': 1529551800, 'sys': {'type': 1, 'id': 7267, 'message': 0.0046, 'country': 'RU', 'sunrise': 1529541360, 'sunset': 1529608877}, 'id': 546105, 'name': 'Nikolskoye', 'cod': 200}
    'Processing Record 67 | norman wells, ca'
    {'coord': {'lon': -126.83, 'lat': 65.28}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'base': 'stations', 'main': {'temp': 73.4, 'pressure': 1016, 'humidity': 49, 'temp_min': 73.4, 'temp_max': 73.4}, 'visibility': 48279, 'wind': {'speed': 5.82, 'deg': 220}, 'clouds': {'all': 40}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 3547, 'message': 0.0038, 'country': 'CA', 'sunrise': 1529572539, 'sunset': 1529653355}, 'id': 6089245, 'name': 'Norman Wells', 'cod': 200}
    'Processing Record 68 | margate, za'
    {'coord': {'lon': 30.37, 'lat': -30.86}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 63.36, 'pressure': 1021.05, 'humidity': 87, 'temp_min': 63.36, 'temp_max': 63.36, 'sea_level': 1036.45, 'grnd_level': 1021.05}, 'wind': {'speed': 12.91, 'deg': 15.0034}, 'clouds': {'all': 0}, 'dt': 1529554517, 'sys': {'message': 0.0032, 'country': 'ZA', 'sunrise': 1529556957, 'sunset': 1529593482}, 'id': 978895, 'name': 'Margate', 'cod': 200}
    'Processing Record 69 | bredasdorp, za'
    {'coord': {'lon': 20.04, 'lat': -34.53}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 37.4, 'pressure': 1019, 'humidity': 93, 'temp_min': 37.4, 'temp_max': 37.4}, 'wind': {'speed': 3.36, 'deg': 20}, 'clouds': {'all': 8}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 6591, 'message': 0.0036, 'country': 'ZA', 'sunrise': 1529559985, 'sunset': 1529595413}, 'id': 1015776, 'name': 'Bredasdorp', 'cod': 200}
    'Processing Record 70 | vaitupu, wf'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for vaitupu, wf**
    'Processing Record 71 | hermanus, za'
    {'coord': {'lon': 19.24, 'lat': -34.42}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 32.94, 'pressure': 992.68, 'humidity': 92, 'temp_min': 32.94, 'temp_max': 32.94, 'sea_level': 1033.54, 'grnd_level': 992.68}, 'wind': {'speed': 2.62, 'deg': 323.503}, 'clouds': {'all': 0}, 'dt': 1529554552, 'sys': {'message': 0.0036, 'country': 'ZA', 'sunrise': 1529560160, 'sunset': 1529595623}, 'id': 3366880, 'name': 'Hermanus', 'cod': 200}
    'Processing Record 72 | bluff, nz'
    {'coord': {'lon': 168.33, 'lat': -46.6}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'base': 'stations', 'main': {'temp': 44.91, 'pressure': 1035.24, 'humidity': 100, 'temp_min': 44.91, 'temp_max': 44.91, 'sea_level': 1036.37, 'grnd_level': 1035.24}, 'wind': {'speed': 1.61, 'deg': 267.003}, 'clouds': {'all': 48}, 'dt': 1529554552, 'sys': {'message': 0.0091, 'country': 'NZ', 'sunrise': 1529526695, 'sunset': 1529557513}, 'id': 2206939, 'name': 'Bluff', 'cod': 200}
    'Processing Record 73 | kamenskoye, ru'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for kamenskoye, ru**
    'Processing Record 74 | mehriz, ir'
    {'coord': {'lon': 54.44, 'lat': 31.58}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 84.2, 'pressure': 1014, 'humidity': 13, 'temp_min': 84.2, 'temp_max': 84.2}, 'visibility': 10000, 'wind': {'speed': 4.7, 'deg': 310}, 'clouds': {'all': 0}, 'dt': 1529551800, 'sys': {'type': 1, 'id': 7060, 'message': 0.004, 'country': 'IR', 'sunrise': 1529543863, 'sunset': 1529595021}, 'id': 124274, 'name': 'Mehriz', 'cod': 200}
    'Processing Record 75 | bengkulu, id'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for bengkulu, id**
    'Processing Record 76 | mwanza, mw'
    {'coord': {'lon': 34.52, 'lat': -15.61}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 64.71, 'pressure': 968.04, 'humidity': 76, 'temp_min': 64.71, 'temp_max': 64.71, 'sea_level': 1034.22, 'grnd_level': 968.04}, 'wind': {'speed': 0.72, 'deg': 209.003}, 'clouds': {'all': 100}, 'dt': 1529554553, 'sys': {'message': 0.0038, 'country': 'MW', 'sunrise': 1529554062, 'sunset': 1529594385}, 'id': 925596, 'name': 'Mwanza', 'cod': 200}
    'Processing Record 77 | gamba, ga'
    {'coord': {'lon': 10.02, 'lat': -2.72}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'base': 'stations', 'main': {'temp': 73.26, 'pressure': 1028.19, 'humidity': 100, 'temp_min': 73.26, 'temp_max': 73.26, 'sea_level': 1028.83, 'grnd_level': 1028.19}, 'wind': {'speed': 12.24, 'deg': 165.003}, 'clouds': {'all': 36}, 'dt': 1529554553, 'sys': {'message': 0.0036, 'country': 'GA', 'sunrise': 1529558566, 'sunset': 1529601642}, 'id': 2400547, 'name': 'Gamba', 'cod': 200}
    'Processing Record 78 | hay river, ca'
    {'coord': {'lon': -115.79, 'lat': 60.82}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 78.8, 'pressure': 1011, 'humidity': 44, 'temp_min': 78.8, 'temp_max': 78.8}, 'visibility': 24140, 'wind': {'speed': 6.93, 'deg': 80}, 'clouds': {'all': 75}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 3530, 'message': 0.0042, 'country': 'CA', 'sunrise': 1529575745, 'sunset': 1529644859}, 'id': 5972762, 'name': 'Hay River', 'cod': 200}
    'Processing Record 79 | ternate, id'
    {'coord': {'lon': 127.4, 'lat': 0.8}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 82.17, 'pressure': 1023.4, 'humidity': 100, 'temp_min': 82.17, 'temp_max': 82.17, 'sea_level': 1025.27, 'grnd_level': 1023.4}, 'wind': {'speed': 1.95, 'deg': 214.003}, 'clouds': {'all': 0}, 'dt': 1529554806, 'sys': {'message': 0.0043, 'country': 'ID', 'sunrise': 1529530024, 'sunset': 1529573833}, 'id': 1624041, 'name': 'Ternate', 'cod': 200}
    'Processing Record 80 | barrow, us'
    {'coord': {'lon': -90.4, 'lat': 39.51}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'base': 'stations', 'main': {'temp': 71.78, 'pressure': 1009, 'humidity': 94, 'temp_min': 69.8, 'temp_max': 75.2}, 'visibility': 16093, 'wind': {'speed': 4.29, 'deg': 195.503}, 'clouds': {'all': 40}, 'dt': 1529552100, 'sys': {'type': 1, 'id': 978, 'message': 0.004, 'country': 'US', 'sunrise': 1529577274, 'sunset': 1529631142}, 'id': 4252975, 'name': 'Barrow', 'cod': 200}
    'Processing Record 81 | yellowknife, ca'
    {'coord': {'lon': -114.38, 'lat': 62.45}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 77, 'pressure': 1013, 'humidity': 41, 'temp_min': 77, 'temp_max': 77}, 'visibility': 24140, 'wind': {'speed': 14.99, 'deg': 60}, 'clouds': {'all': 75}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 3558, 'message': 0.0031, 'country': 'CA', 'sunrise': 1529573983, 'sunset': 1529645943}, 'id': 6185377, 'name': 'Yellowknife', 'cod': 200}
    'Processing Record 82 | axim, gh'
    {'coord': {'lon': -2.24, 'lat': 4.87}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10n'}], 'base': 'stations', 'main': {'temp': 77.31, 'pressure': 1025.43, 'humidity': 100, 'temp_min': 77.31, 'temp_max': 77.31, 'sea_level': 1027.74, 'grnd_level': 1025.43}, 'wind': {'speed': 11.79, 'deg': 254.003}, 'rain': {'3h': 0.1025}, 'clouds': {'all': 88}, 'dt': 1529554554, 'sys': {'message': 0.0032, 'country': 'GH', 'sunrise': 1529560717, 'sunset': 1529605377}, 'id': 2303611, 'name': 'Axim', 'cod': 200}
    'Processing Record 83 | tuggurt, dz'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for tuggurt, dz**
    'Processing Record 84 | banda aceh, id'
    {'coord': {'lon': 95.32, 'lat': 5.56}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'base': 'stations', 'main': {'temp': 84.15, 'pressure': 998.76, 'humidity': 78, 'temp_min': 84.15, 'temp_max': 84.15, 'sea_level': 1024.7, 'grnd_level': 998.76}, 'wind': {'speed': 3.18, 'deg': 357.503}, 'clouds': {'all': 48}, 'dt': 1529554444, 'sys': {'message': 0.0032, 'country': 'ID', 'sunrise': 1529537226, 'sunset': 1529582032}, 'id': 1215502, 'name': 'Banda Aceh', 'cod': 200}
    'Processing Record 85 | xudat, az'
    {'coord': {'lon': 48.68, 'lat': 41.63}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 66.51, 'pressure': 961.07, 'humidity': 84, 'temp_min': 66.51, 'temp_max': 66.51, 'sea_level': 1028.43, 'grnd_level': 961.07}, 'wind': {'speed': 2.84, 'deg': 245.503}, 'clouds': {'all': 0}, 'dt': 1529554554, 'sys': {'message': 0.0031, 'country': 'AZ', 'sunrise': 1529543464, 'sunset': 1529598184}, 'id': 586001, 'name': 'Khudat', 'cod': 200}
    'Processing Record 86 | bonavista, ca'
    {'coord': {'lon': -53.11, 'lat': 48.65}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 52.47, 'pressure': 1015.38, 'humidity': 74, 'temp_min': 52.47, 'temp_max': 52.47, 'sea_level': 1017.61, 'grnd_level': 1015.38}, 'wind': {'speed': 13.58, 'deg': 219.003}, 'clouds': {'all': 56}, 'dt': 1529554554, 'sys': {'message': 0.0035, 'country': 'CA', 'sunrise': 1529566189, 'sunset': 1529624325}, 'id': 5905393, 'name': 'Bonavista', 'cod': 200}
    'Processing Record 87 | moose jaw, ca'
    {'coord': {'lon': -105.54, 'lat': 50.4}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 73.4, 'pressure': 1016, 'humidity': 40, 'temp_min': 73.4, 'temp_max': 73.4}, 'visibility': 24140, 'wind': {'speed': 3.36, 'deg': 230}, 'clouds': {'all': 20}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 3927, 'message': 0.0039, 'country': 'CA', 'sunrise': 1529578249, 'sunset': 1529637435}, 'id': 6078112, 'name': 'Moose Jaw', 'cod': 200}
    'Processing Record 88 | choucheng, cn'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for choucheng, cn**
    'Processing Record 89 | albany, au'
    {'coord': {'lon': 117.88, 'lat': -35.02}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 59.94, 'pressure': 1027.46, 'humidity': 86, 'temp_min': 59.94, 'temp_max': 59.94, 'sea_level': 1040.51, 'grnd_level': 1027.46}, 'wind': {'speed': 11.9, 'deg': 297.003}, 'rain': {'3h': 0.47}, 'clouds': {'all': 24}, 'dt': 1529554338, 'sys': {'message': 0.0036, 'country': 'AU', 'sunrise': 1529536577, 'sunset': 1529571851}, 'id': 2077963, 'name': 'Albany', 'cod': 200}
    'Processing Record 90 | rincon, an'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for rincon, an**
    'Processing Record 91 | qaanaaq, gl'
    {'coord': {'lon': -69.36, 'lat': 77.48}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 31.23, 'pressure': 986.04, 'humidity': 98, 'temp_min': 31.23, 'temp_max': 31.23, 'sea_level': 1017.73, 'grnd_level': 986.04}, 'wind': {'speed': 1.16, 'deg': 115.503}, 'clouds': {'all': 64}, 'dt': 1529554517, 'sys': {'message': 0.0031, 'country': 'GL', 'sunrise': 0, 'sunset': 0}, 'id': 3831208, 'name': 'Qaanaaq', 'cod': 200}
    'Processing Record 92 | geraldton, ca'
    {'coord': {'lon': -86.95, 'lat': 49.72}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 53.6, 'pressure': 1016, 'humidity': 62, 'temp_min': 53.6, 'temp_max': 53.6}, 'visibility': 24140, 'wind': {'speed': 4.7, 'deg': 80}, 'clouds': {'all': 20}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 3656, 'message': 0.0036, 'country': 'CA', 'sunrise': 1529573997, 'sunset': 1529632763}, 'id': 5960603, 'name': 'Geraldton', 'cod': 200}
    'Processing Record 93 | mar del plata, ar'
    {'coord': {'lon': -67.52, 'lat': -46.43}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10n'}], 'base': 'stations', 'main': {'temp': 42.21, 'pressure': 990.82, 'humidity': 76, 'temp_min': 42.21, 'temp_max': 42.21, 'sea_level': 1012.38, 'grnd_level': 990.82}, 'wind': {'speed': 18.5, 'deg': 252.503}, 'rain': {'3h': 1.495}, 'clouds': {'all': 88}, 'dt': 1529554555, 'sys': {'message': 0.0032, 'country': 'AR', 'sunrise': 1529583267, 'sunset': 1529614166}, 'id': 3863379, 'name': 'Mar del Plata', 'cod': 200}
    'Processing Record 94 | hofn, is'
    {'coord': {'lon': -15.21, 'lat': 64.25}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 46.98, 'pressure': 1024.54, 'humidity': 92, 'temp_min': 46.98, 'temp_max': 46.98, 'sea_level': 1035.6, 'grnd_level': 1024.54}, 'wind': {'speed': 4.85, 'deg': 247.003}, 'clouds': {'all': 0}, 'dt': 1529554555, 'sys': {'message': 0.0034, 'country': 'IS', 'sunrise': 1529547934, 'sunset': 1529624383}, 'id': 2630299, 'name': 'Hofn', 'cod': 200}
    'Processing Record 95 | asfi, ma'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for asfi, ma**
    'Processing Record 96 | cabo san lucas, mx'
    {'coord': {'lon': -109.91, 'lat': 22.89}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 72.59, 'pressure': 1014, 'humidity': 78, 'temp_min': 71.6, 'temp_max': 73.4}, 'visibility': 9656, 'wind': {'speed': 4.7, 'deg': 320}, 'clouds': {'all': 5}, 'dt': 1529552880, 'sys': {'type': 1, 'id': 4016, 'message': 0.0036, 'country': 'MX', 'sunrise': 1529584516, 'sunset': 1529633267}, 'id': 3985710, 'name': 'Cabo San Lucas', 'cod': 200}
    'Processing Record 97 | roma, au'
    {'coord': {'lon': 148.79, 'lat': -26.57}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 61.92, 'pressure': 989.2, 'humidity': 79, 'temp_min': 61.92, 'temp_max': 61.92, 'sea_level': 1037.87, 'grnd_level': 989.2}, 'wind': {'speed': 5.64, 'deg': 103.503}, 'clouds': {'all': 0}, 'dt': 1529554807, 'sys': {'message': 0.0134, 'country': 'AU', 'sunrise': 1529527947, 'sunset': 1529565641}, 'id': 2151187, 'name': 'Roma', 'cod': 200}
    'Processing Record 98 | muli, mv'
    {'coord': {'lon': 73.57, 'lat': 2.92}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 81.9, 'pressure': 1024.86, 'humidity': 100, 'temp_min': 81.9, 'temp_max': 81.9, 'sea_level': 1024.94, 'grnd_level': 1024.86}, 'wind': {'speed': 11.34, 'deg': 244.503}, 'clouds': {'all': 80}, 'dt': 1529554556, 'sys': {'message': 0.0027, 'country': 'MV', 'sunrise': 1529542724, 'sunset': 1529586976}, 'id': 1337617, 'name': 'Muli', 'cod': 200}
    'Processing Record 99 | mataura, pf'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for mataura, pf**
    'Processing Record 100 | kodiak, us'
    {'coord': {'lon': -94.76, 'lat': 39.95}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 73.4, 'pressure': 1009, 'humidity': 78, 'temp_min': 73.4, 'temp_max': 73.4}, 'visibility': 16093, 'wind': {'speed': 8.05, 'deg': 310}, 'clouds': {'all': 1}, 'dt': 1529549580, 'sys': {'type': 1, 'id': 1664, 'message': 0.0391, 'country': 'US', 'sunrise': 1529578235, 'sunset': 1529632275}, 'id': 4407665, 'name': 'Kodiak', 'cod': 200}
    'Processing Record 101 | sambava, mg'
    {'coord': {'lon': 50.17, 'lat': -14.27}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 74.16, 'pressure': 1029.81, 'humidity': 100, 'temp_min': 74.16, 'temp_max': 74.16, 'sea_level': 1032.4, 'grnd_level': 1029.81}, 'wind': {'speed': 16.93, 'deg': 170.503}, 'clouds': {'all': 68}, 'dt': 1529554556, 'sys': {'message': 0.0035, 'country': 'MG', 'sunrise': 1529550157, 'sunset': 1529590777}, 'id': 1056899, 'name': 'Sambava', 'cod': 200}
    'Processing Record 102 | lazaro cardenas, mx'
    {'coord': {'lon': -105.62, 'lat': 28.39}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 82.4, 'pressure': 1015, 'humidity': 17, 'temp_min': 82.4, 'temp_max': 82.4}, 'visibility': 16093, 'wind': {'speed': 3.36, 'deg': 280}, 'clouds': {'all': 5}, 'dt': 1529552400, 'sys': {'type': 1, 'id': 3971, 'message': 0.0088, 'country': 'MX', 'sunrise': 1529582751, 'sunset': 1529632973}, 'id': 3996234, 'name': 'Lazaro Cardenas', 'cod': 200}
    'Processing Record 103 | shakawe, bw'
    {'coord': {'lon': 21.84, 'lat': -18.36}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 45.81, 'pressure': 917.13, 'humidity': 63, 'temp_min': 45.81, 'temp_max': 45.81, 'sea_level': 1036.58, 'grnd_level': 917.13}, 'wind': {'speed': 2.28, 'deg': 193.503}, 'clouds': {'all': 0}, 'dt': 1529554556, 'sys': {'message': 0.0043, 'country': 'BW', 'sunrise': 1529557417, 'sunset': 1529597117}, 'id': 933077, 'name': 'Shakawe', 'cod': 200}
    'Processing Record 104 | bojnurd, ir'
    {'coord': {'lon': 57.33, 'lat': 37.47}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 'base': 'stations', 'main': {'temp': 69.8, 'pressure': 1018, 'humidity': 49, 'temp_min': 69.8, 'temp_max': 69.8}, 'visibility': 9000, 'wind': {'speed': 2.24, 'deg': 220}, 'clouds': {'all': 20}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 7044, 'message': 0.0036, 'country': 'IR', 'sunrise': 1529542195, 'sunset': 1529595301}, 'id': 140380, 'name': 'Bojnurd', 'cod': 200}
    'Processing Record 105 | yulara, au'
    {'coord': {'lon': 130.99, 'lat': -25.24}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 60.8, 'pressure': 1026, 'humidity': 41, 'temp_min': 60.8, 'temp_max': 60.8}, 'visibility': 10000, 'wind': {'speed': 10.29, 'deg': 120}, 'clouds': {'all': 0}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 8160, 'message': 0.0112, 'country': 'AU', 'sunrise': 1529532048, 'sunset': 1529570086}, 'id': 6355222, 'name': 'Yulara', 'cod': 200}
    'Processing Record 106 | vila franca do campo, pt'
    {'coord': {'lon': -25.43, 'lat': 37.72}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'base': 'stations', 'main': {'temp': 69.8, 'pressure': 1025, 'humidity': 94, 'temp_min': 69.8, 'temp_max': 69.8}, 'visibility': 10000, 'wind': {'speed': 5.82, 'deg': 280}, 'clouds': {'all': 40}, 'dt': 1529551800, 'sys': {'type': 1, 'id': 5957, 'message': 0.004, 'country': 'PT', 'sunrise': 1529562015, 'sunset': 1529615212}, 'id': 3372472, 'name': 'Vila Franca do Campo', 'cod': 200}
    'Processing Record 107 | karratha, au'
    {'coord': {'lon': 116.85, 'lat': -20.74}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 73.53, 'pressure': 1022.11, 'humidity': 22, 'temp_min': 73.53, 'temp_max': 73.53, 'sea_level': 1035.6, 'grnd_level': 1022.11}, 'wind': {'speed': 15.7, 'deg': 116.503}, 'clouds': {'all': 0}, 'dt': 1529554808, 'sys': {'message': 0.0028, 'country': 'AU', 'sunrise': 1529534890, 'sunset': 1529574033}, 'id': 6620339, 'name': 'Karratha', 'cod': 200}
    'Processing Record 108 | atambua, id'
    {'coord': {'lon': 124.89, 'lat': -9.11}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 85.05, 'pressure': 1003.46, 'humidity': 79, 'temp_min': 85.05, 'temp_max': 85.05, 'sea_level': 1026.4, 'grnd_level': 1003.46}, 'wind': {'speed': 4.97, 'deg': 134.003}, 'clouds': {'all': 0}, 'dt': 1529554808, 'sys': {'message': 0.0032, 'country': 'ID', 'sunrise': 1529531664, 'sunset': 1529573399}, 'id': 1651103, 'name': 'Atambua', 'cod': 200}
    'Processing Record 109 | cabedelo, br'
    {'coord': {'lon': -34.84, 'lat': -6.97}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'base': 'stations', 'main': {'temp': 69.8, 'pressure': 1017, 'humidity': 88, 'temp_min': 69.8, 'temp_max': 69.8}, 'visibility': 10000, 'wind': {'speed': 3.36, 'deg': 160}, 'clouds': {'all': 40}, 'dt': 1529553600, 'sys': {'type': 1, 'id': 4516, 'message': 0.0032, 'country': 'BR', 'sunrise': 1529569778, 'sunset': 1529611966}, 'id': 3404558, 'name': 'Cabedelo', 'cod': 200}
    'Processing Record 110 | utiroa, ki'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for utiroa, ki**
    'Processing Record 111 | almonte, es'
    {'coord': {'lon': -6.52, 'lat': 37.26}, 'weather': [{'id': 501, 'main': 'Rain', 'description': 'moderate rain', 'icon': '10n'}], 'base': 'stations', 'main': {'temp': 67.95, 'pressure': 1016, 'humidity': 83, 'temp_min': 66.2, 'temp_max': 69.8}, 'visibility': 10000, 'wind': {'speed': 5.82, 'deg': 180}, 'clouds': {'all': 0}, 'dt': 1529553600, 'sys': {'type': 1, 'id': 5511, 'message': 0.0033, 'country': 'ES', 'sunrise': 1529557559, 'sunset': 1529610590}, 'id': 2521857, 'name': 'Almonte', 'cod': 200}
    'Processing Record 112 | burley, us'
    {'coord': {'lon': -113.79, 'lat': 42.54}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 72.1, 'pressure': 1018, 'humidity': 40, 'temp_min': 71.6, 'temp_max': 73.4}, 'visibility': 16093, 'wind': {'speed': 5.82, 'deg': 80}, 'clouds': {'all': 1}, 'dt': 1529549580, 'sys': {'type': 1, 'id': 912, 'message': 0.004, 'country': 'US', 'sunrise': 1529582270, 'sunset': 1529637376}, 'id': 5587385, 'name': 'Burley', 'cod': 200}
    'Processing Record 113 | fenoarivo, mg'
    {'coord': {'lon': 47.44, 'lat': -18.93}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 'base': 'stations', 'main': {'temp': 51.8, 'pressure': 1026, 'humidity': 93, 'temp_min': 51.8, 'temp_max': 51.8}, 'visibility': 10000, 'wind': {'speed': 6.93, 'deg': 110}, 'clouds': {'all': 20}, 'dt': 1529551800, 'sys': {'type': 1, 'id': 6795, 'message': 0.0053, 'country': 'MG', 'sunrise': 1529551338, 'sunset': 1529590906}, 'id': 1070940, 'name': 'Fenoarivo', 'cod': 200}
    'Processing Record 114 | kilindoni, tz'
    {'coord': {'lon': 39.67, 'lat': -7.91}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 80.01, 'pressure': 1030.29, 'humidity': 92, 'temp_min': 80.01, 'temp_max': 80.01, 'sea_level': 1030.5, 'grnd_level': 1030.29}, 'wind': {'speed': 12.12, 'deg': 166.003}, 'clouds': {'all': 64}, 'dt': 1529554558, 'sys': {'message': 0.0033, 'country': 'TZ', 'sunrise': 1529551992, 'sunset': 1529593982}, 'id': 157429, 'name': 'Kilindoni', 'cod': 200}
    'Processing Record 115 | port hedland, au'
    {'coord': {'lon': 118.58, 'lat': -20.31}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 77, 'pressure': 1020, 'humidity': 22, 'temp_min': 77, 'temp_max': 77}, 'visibility': 10000, 'wind': {'speed': 16.11, 'deg': 100}, 'clouds': {'all': 0}, 'dt': 1529553600, 'sys': {'type': 1, 'id': 8219, 'message': 0.0038, 'country': 'AU', 'sunrise': 1529534423, 'sunset': 1529573668}, 'id': 2063042, 'name': 'Port Hedland', 'cod': 200}
    'Processing Record 116 | bathsheba, bb'
    {'coord': {'lon': -59.52, 'lat': 13.22}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 78.8, 'pressure': 1016, 'humidity': 78, 'temp_min': 78.8, 'temp_max': 78.8}, 'visibility': 10000, 'wind': {'speed': 13.87, 'deg': 70}, 'clouds': {'all': 75}, 'dt': 1529553600, 'sys': {'type': 1, 'id': 4160, 'message': 0.0044, 'country': 'BB', 'sunrise': 1529573565, 'sunset': 1529620028}, 'id': 3374083, 'name': 'Bathsheba', 'cod': 200}
    'Processing Record 117 | new norfolk, au'
    {'coord': {'lon': 147.06, 'lat': -42.78}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'base': 'stations', 'main': {'temp': 55.4, 'pressure': 1023, 'humidity': 43, 'temp_min': 55.4, 'temp_max': 55.4}, 'visibility': 10000, 'wind': {'speed': 11.41, 'deg': 290}, 'clouds': {'all': 40}, 'dt': 1529551800, 'sys': {'type': 1, 'id': 8195, 'message': 0.004, 'country': 'AU', 'sunrise': 1529530960, 'sunset': 1529563459}, 'id': 2155415, 'name': 'New Norfolk', 'cod': 200}
    'Processing Record 118 | avarua, ck'
    {'coord': {'lon': -159.78, 'lat': -21.21}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'base': 'stations', 'main': {'temp': 75.2, 'pressure': 1016, 'humidity': 64, 'temp_min': 75.2, 'temp_max': 75.2}, 'visibility': 10000, 'wind': {'speed': 9.17, 'deg': 60}, 'clouds': {'all': 40}, 'dt': 1529553600, 'sys': {'type': 1, 'id': 8340, 'message': 0.0032, 'country': 'CK', 'sunrise': 1529601347, 'sunset': 1529640378}, 'id': 4035715, 'name': 'Avarua', 'cod': 200}
    'Processing Record 119 | tiksi, ru'
    {'coord': {'lon': 128.87, 'lat': 71.64}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 57.69, 'pressure': 1003.87, 'humidity': 72, 'temp_min': 57.69, 'temp_max': 57.69, 'sea_level': 1020.53, 'grnd_level': 1003.87}, 'wind': {'speed': 3.62, 'deg': 21.0034}, 'clouds': {'all': 56}, 'dt': 1529554558, 'sys': {'message': 0.0036, 'country': 'RU', 'sunrise': 0, 'sunset': 0}, 'id': 2015306, 'name': 'Tiksi', 'cod': 200}
    'Processing Record 120 | samusu, ws'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for samusu, ws**
    'Processing Record 121 | biryusinsk, ru'
    {'coord': {'lon': 97.82, 'lat': 55.96}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 'base': 'stations', 'main': {'temp': 75.96, 'pressure': 973.47, 'humidity': 58, 'temp_min': 75.96, 'temp_max': 75.96, 'sea_level': 1018.21, 'grnd_level': 973.47}, 'wind': {'speed': 3.51, 'deg': 142.503}, 'clouds': {'all': 12}, 'dt': 1529554559, 'sys': {'message': 0.0031, 'country': 'RU', 'sunrise': 1529527329, 'sunset': 1529590729}, 'id': 1510041, 'name': 'Biryusinsk', 'cod': 200}
    'Processing Record 122 | chadiza, zm'
    {'coord': {'lon': 32.43, 'lat': -14.06}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 50.94, 'pressure': 913.57, 'humidity': 84, 'temp_min': 50.94, 'temp_max': 50.94, 'sea_level': 1033.98, 'grnd_level': 913.57}, 'wind': {'speed': 5.64, 'deg': 111.003}, 'clouds': {'all': 0}, 'dt': 1529554559, 'sys': {'message': 0.0035, 'country': 'ZM', 'sunrise': 1529554392, 'sunset': 1529595058}, 'id': 921028, 'name': 'Chadiza', 'cod': 200}
    'Processing Record 123 | tasiilaq, gl'
    {'coord': {'lon': -37.64, 'lat': 65.61}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 41, 'pressure': 1010, 'humidity': 92, 'temp_min': 41, 'temp_max': 41}, 'wind': {'speed': 18.34, 'deg': 70}, 'rain': {'3h': 1.22}, 'clouds': {'all': 92}, 'dt': 1529553000, 'sys': {'type': 1, 'id': 4806, 'message': 0.0034, 'country': 'GL', 'sunrise': 1529549795, 'sunset': 1529633279}, 'id': 3424607, 'name': 'Tasiilaq', 'cod': 200}
    'Processing Record 124 | ilulissat, gl'
    {'coord': {'lon': -51.1, 'lat': 69.22}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 51.8, 'pressure': 994, 'humidity': 43, 'temp_min': 51.8, 'temp_max': 51.8}, 'wind': {'speed': 16.11, 'deg': 110}, 'clouds': {'all': 0}, 'dt': 1529553000, 'sys': {'type': 1, 'id': 4805, 'message': 0.0039, 'country': 'GL', 'sunrise': 0, 'sunset': 0}, 'id': 3423146, 'name': 'Ilulissat', 'cod': 200}
    'Processing Record 125 | butaritari, ki'
    {'coord': {'lon': 172.79, 'lat': 3.07}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 84.06, 'pressure': 1023.65, 'humidity': 100, 'temp_min': 84.06, 'temp_max': 84.06, 'sea_level': 1023.65, 'grnd_level': 1023.65}, 'wind': {'speed': 5.64, 'deg': 208.003}, 'clouds': {'all': 88}, 'dt': 1529554559, 'sys': {'message': 0.0044, 'country': 'KI', 'sunrise': 1529518892, 'sunset': 1529563175}, 'id': 2110227, 'name': 'Butaritari', 'cod': 200}
    'Processing Record 126 | hirara, jp'
    {'coord': {'lon': 125.28, 'lat': 24.8}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 86, 'pressure': 1007, 'humidity': 84, 'temp_min': 86, 'temp_max': 86}, 'visibility': 10000, 'wind': {'speed': 17.22, 'deg': 200}, 'clouds': {'all': 75}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 7630, 'message': 0.004, 'country': 'JP', 'sunrise': 1529527816, 'sunset': 1529577060}, 'id': 1862505, 'name': 'Hirara', 'cod': 200}
    'Processing Record 127 | beitbridge, zw'
    {'coord': {'lon': 30, 'lat': -22.22}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10n'}], 'base': 'stations', 'main': {'temp': 60.84, 'pressure': 974.61, 'humidity': 99, 'temp_min': 60.84, 'temp_max': 60.84, 'sea_level': 1038.76, 'grnd_level': 974.61}, 'wind': {'speed': 7.43, 'deg': 120.503}, 'rain': {'3h': 0.11}, 'clouds': {'all': 48}, 'dt': 1529554560, 'sys': {'message': 0.0033, 'country': 'ZW', 'sunrise': 1529555914, 'sunset': 1529594702}, 'id': 895269, 'name': 'Beitbridge', 'cod': 200}
    'Processing Record 128 | aksarka, ru'
    {'coord': {'lon': 67.8, 'lat': 66.56}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 54.27, 'pressure': 998.03, 'humidity': 98, 'temp_min': 54.27, 'temp_max': 54.27, 'sea_level': 1001.88, 'grnd_level': 998.03}, 'wind': {'speed': 8.77, 'deg': 316.003}, 'rain': {'3h': 0.985}, 'clouds': {'all': 56}, 'dt': 1529554560, 'sys': {'message': 0.0037, 'country': 'RU', 'sunrise': 0, 'sunset': 0}, 'id': 1512019, 'name': 'Aksarka', 'cod': 200}
    'Processing Record 129 | tsihombe, mg'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for tsihombe, mg**
    'Processing Record 130 | santa cruz das palmeiras, br'
    {'coord': {'lon': -47.25, 'lat': -21.82}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 56.25, 'pressure': 959.29, 'humidity': 86, 'temp_min': 56.25, 'temp_max': 56.25, 'sea_level': 1034.71, 'grnd_level': 959.29}, 'wind': {'speed': 3.96, 'deg': 72.5034}, 'clouds': {'all': 0}, 'dt': 1529554560, 'sys': {'message': 0.0039, 'country': 'BR', 'sunrise': 1529574409, 'sunset': 1529613293}, 'id': 3450283, 'name': 'Santa Cruz das Palmeiras', 'cod': 200}
    'Processing Record 131 | lusambo, cd'
    {'coord': {'lon': 23.44, 'lat': -4.97}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'base': 'stations', 'main': {'temp': 70.56, 'pressure': 964.88, 'humidity': 75, 'temp_min': 70.56, 'temp_max': 70.56, 'sea_level': 1026.12, 'grnd_level': 964.88}, 'wind': {'speed': 1.95, 'deg': 282.503}, 'clouds': {'all': 32}, 'dt': 1529554560, 'sys': {'message': 0.0037, 'country': 'CD', 'sunrise': 1529555579, 'sunset': 1529598186}, 'id': 210379, 'name': 'Lusambo', 'cod': 200}
    'Processing Record 132 | arraial do cabo, br'
    {'coord': {'lon': -42.02, 'lat': -22.97}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 68.04, 'pressure': 1034.51, 'humidity': 99, 'temp_min': 68.04, 'temp_max': 68.04, 'sea_level': 1035.56, 'grnd_level': 1034.51}, 'wind': {'speed': 12.24, 'deg': 34.0034}, 'clouds': {'all': 0}, 'dt': 1529554481, 'sys': {'message': 0.0044, 'country': 'BR', 'sunrise': 1529573293, 'sunset': 1529611898}, 'id': 3471451, 'name': 'Arraial do Cabo', 'cod': 200}
    'Processing Record 133 | meadow lake, ca'
    {'coord': {'lon': -108.44, 'lat': 54.13}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 79.83, 'pressure': 958.88, 'humidity': 32, 'temp_min': 79.83, 'temp_max': 79.83, 'sea_level': 1024.5, 'grnd_level': 958.88}, 'wind': {'speed': 5.19, 'deg': 227.003}, 'clouds': {'all': 0}, 'dt': 1529554561, 'sys': {'message': 0.0028, 'country': 'CA', 'sunrise': 1529577624, 'sunset': 1529639453}, 'id': 6071421, 'name': 'Meadow Lake', 'cod': 200}
    'Processing Record 134 | mandera, ke'
    {'coord': {'lon': 41.87, 'lat': 3.94}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'base': 'stations', 'main': {'temp': 76.59, 'pressure': 1002.08, 'humidity': 64, 'temp_min': 76.59, 'temp_max': 76.59, 'sea_level': 1027.58, 'grnd_level': 1002.08}, 'wind': {'speed': 8.99, 'deg': 244.503}, 'clouds': {'all': 32}, 'dt': 1529554561, 'sys': {'message': 0.0044, 'country': 'KE', 'sunrise': 1529550227, 'sunset': 1529594692}, 'id': 187896, 'name': 'Mandera', 'cod': 200}
    'Processing Record 135 | tecoanapa, mx'
    {'coord': {'lon': -99.26, 'lat': 16.99}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 82.4, 'pressure': 1011, 'humidity': 78, 'temp_min': 82.4, 'temp_max': 82.4}, 'visibility': 12874, 'wind': {'speed': 6.93, 'deg': 270}, 'clouds': {'all': 75}, 'dt': 1529552760, 'sys': {'type': 1, 'id': 3965, 'message': 0.0029, 'country': 'MX', 'sunrise': 1529582675, 'sunset': 1529629995}, 'id': 3532499, 'name': 'Tecoanapa', 'cod': 200}
    'Processing Record 136 | polson, us'
    {'coord': {'lon': -114.16, 'lat': 47.69}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10n'}], 'base': 'stations', 'main': {'temp': 63.27, 'pressure': 873.93, 'humidity': 57, 'temp_min': 63.27, 'temp_max': 63.27, 'sea_level': 1025.75, 'grnd_level': 873.93}, 'wind': {'speed': 2.39, 'deg': 191.503}, 'rain': {'3h': 0.1725}, 'clouds': {'all': 80}, 'dt': 1529554291, 'sys': {'message': 0.0138, 'country': 'US', 'sunrise': 1529581112, 'sunset': 1529638711}, 'id': 5671996, 'name': 'Polson', 'cod': 200}
    'Processing Record 137 | aklavik, ca'
    {'coord': {'lon': -135.01, 'lat': 68.22}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 'base': 'stations', 'main': {'temp': 64.4, 'pressure': 1017, 'humidity': 52, 'temp_min': 64.4, 'temp_max': 64.4}, 'visibility': 24140, 'wind': {'speed': 5.82, 'deg': 60}, 'clouds': {'all': 20}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 3535, 'message': 0.0061, 'country': 'CA', 'sunrise': 0, 'sunset': 0}, 'id': 5882953, 'name': 'Aklavik', 'cod': 200}
    'Processing Record 138 | barentsburg, sj'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for barentsburg, sj**
    'Processing Record 139 | harrisonburg, us'
    {'coord': {'lon': -78.87, 'lat': 38.45}, 'weather': [{'id': 211, 'main': 'Thunderstorm', 'description': 'thunderstorm', 'icon': '11n'}, {'id': 501, 'main': 'Rain', 'description': 'moderate rain', 'icon': '10n'}, {'id': 701, 'main': 'Mist', 'description': 'mist', 'icon': '50n'}], 'base': 'stations', 'main': {'temp': 69.35, 'pressure': 1012, 'humidity': 100, 'temp_min': 68, 'temp_max': 71.6}, 'visibility': 16093, 'wind': {'speed': 2.95, 'deg': 202.503}, 'clouds': {'all': 1}, 'dt': 1529553180, 'sys': {'type': 1, 'id': 2880, 'message': 0.0034, 'country': 'US', 'sunrise': 1529574708, 'sunset': 1529628174}, 'id': 4763231, 'name': 'Harrisonburg', 'cod': 200}
    'Processing Record 140 | bereda, so'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for bereda, so**
    'Processing Record 141 | urucara, br'
    {'coord': {'lon': -57.76, 'lat': -2.54}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 69.3, 'pressure': 1021.86, 'humidity': 98, 'temp_min': 69.3, 'temp_max': 69.3, 'sea_level': 1028.79, 'grnd_level': 1021.86}, 'wind': {'speed': 2.51, 'deg': 88.5034}, 'clouds': {'all': 8}, 'dt': 1529554562, 'sys': {'message': 0.0042, 'country': 'BR', 'sunrise': 1529574817, 'sunset': 1529617931}, 'id': 3385670, 'name': 'Urucara', 'cod': 200}
    'Processing Record 142 | mbandaka, cd'
    {'coord': {'lon': 18.26, 'lat': 0.05}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 71.37, 'pressure': 985.22, 'humidity': 96, 'temp_min': 71.37, 'temp_max': 71.37, 'sea_level': 1027.17, 'grnd_level': 985.22}, 'wind': {'speed': 2.39, 'deg': 287.003}, 'clouds': {'all': 8}, 'dt': 1529554811, 'sys': {'message': 0.0035, 'country': 'CD', 'sunrise': 1529556300, 'sunset': 1529599953}, 'id': 2312895, 'name': 'Mbandaka', 'cod': 200}
    'Processing Record 143 | beira, mz'
    {'coord': {'lon': 34.84, 'lat': -19.84}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 'base': 'stations', 'main': {'temp': 68.67, 'pressure': 1034.75, 'humidity': 85, 'temp_min': 68.67, 'temp_max': 68.67, 'sea_level': 1036.25, 'grnd_level': 1034.75}, 'wind': {'speed': 3.4, 'deg': 135.003}, 'clouds': {'all': 24}, 'dt': 1529554562, 'sys': {'message': 0.0038, 'country': 'MZ', 'sunrise': 1529554469, 'sunset': 1529593824}, 'id': 1052373, 'name': 'Beira', 'cod': 200}
    'Processing Record 144 | college, us'
    {'coord': {'lon': -147.8, 'lat': 64.86}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 77, 'pressure': 1008, 'humidity': 29, 'temp_min': 77, 'temp_max': 77}, 'visibility': 16093, 'wind': {'speed': 5.82, 'deg': 350}, 'clouds': {'all': 1}, 'dt': 1529553480, 'sys': {'type': 1, 'id': 63, 'message': 0.004, 'country': 'US', 'sunrise': 1529578635, 'sunset': 1529657329}, 'id': 5859699, 'name': 'College', 'cod': 200}
    'Processing Record 145 | jamestown, sh'
    {'coord': {'lon': -5.72, 'lat': -15.94}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 70.11, 'pressure': 1033.78, 'humidity': 100, 'temp_min': 70.11, 'temp_max': 70.11, 'sea_level': 1033.82, 'grnd_level': 1033.78}, 'wind': {'speed': 17.94, 'deg': 127.003}, 'clouds': {'all': 88}, 'dt': 1529554563, 'sys': {'message': 0.0035, 'country': 'SH', 'sunrise': 1529563758, 'sunset': 1529604007}, 'id': 3370903, 'name': 'Jamestown', 'cod': 200}
    'Processing Record 146 | vallenar, cl'
    {'coord': {'lon': -70.76, 'lat': -28.58}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 44.01, 'pressure': 898.73, 'humidity': 67, 'temp_min': 44.01, 'temp_max': 44.01, 'sea_level': 1032.4, 'grnd_level': 898.73}, 'wind': {'speed': 2.06, 'deg': 158.503}, 'clouds': {'all': 0}, 'dt': 1529554563, 'sys': {'message': 0.0038, 'country': 'CL', 'sunrise': 1529580915, 'sunset': 1529618074}, 'id': 3868633, 'name': 'Vallenar', 'cod': 200}
    'Processing Record 147 | ponta do sol, cv'
    {'coord': {'lon': -25.09, 'lat': 17.2}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 71.55, 'pressure': 1027.54, 'humidity': 100, 'temp_min': 71.55, 'temp_max': 71.55, 'sea_level': 1030.9, 'grnd_level': 1027.54}, 'wind': {'speed': 13.02, 'deg': 20.5034}, 'clouds': {'all': 0}, 'dt': 1529554563, 'sys': {'message': 0.0039, 'country': 'CV', 'sunrise': 1529564847, 'sunset': 1529612216}, 'id': 3374346, 'name': 'Ponta do Sol', 'cod': 200}
    'Processing Record 148 | vaini, to'
    {'coord': {'lon': -175.2, 'lat': -21.2}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'base': 'stations', 'main': {'temp': 80.6, 'pressure': 1013, 'humidity': 78, 'temp_min': 80.6, 'temp_max': 80.6}, 'visibility': 10000, 'wind': {'speed': 5.82, 'deg': 360}, 'clouds': {'all': 40}, 'dt': 1529553600, 'sys': {'type': 1, 'id': 8323, 'message': 0.0045, 'country': 'TO', 'sunrise': 1529605047, 'sunset': 1529644081}, 'id': 4032243, 'name': 'Vaini', 'cod': 200}
    'Processing Record 149 | linxia, cn'
    {'coord': {'lon': 103.21, 'lat': 35.6}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 56.07, 'pressure': 754.37, 'humidity': 100, 'temp_min': 56.07, 'temp_max': 56.07, 'sea_level': 1017.28, 'grnd_level': 754.37}, 'wind': {'speed': 3.4, 'deg': 289.003}, 'rain': {'3h': 2.845}, 'clouds': {'all': 92}, 'dt': 1529554563, 'sys': {'message': 0.0032, 'country': 'CN', 'sunrise': 1529531509, 'sunset': 1529583961}, 'id': 1803331, 'name': 'Linxia', 'cod': 200}
    'Processing Record 150 | kachiry, kz'
    {'coord': {'lon': 76.1, 'lat': 53.07}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 69.93, 'pressure': 1006.87, 'humidity': 61, 'temp_min': 69.93, 'temp_max': 69.93, 'sea_level': 1019.71, 'grnd_level': 1006.87}, 'wind': {'speed': 10.67, 'deg': 222.003}, 'clouds': {'all': 0}, 'dt': 1529554564, 'sys': {'message': 0.0033, 'country': 'KZ', 'sunrise': 1529533737, 'sunset': 1529594749}, 'id': 1523662, 'name': 'Kachiry', 'cod': 200}
    'Processing Record 151 | shelburne, ca'
    {'coord': {'lon': -80.2, 'lat': 44.08}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 63.95, 'pressure': 1011, 'humidity': 67, 'temp_min': 60.8, 'temp_max': 68}, 'visibility': 14484, 'wind': {'speed': 3.36, 'deg': 320}, 'clouds': {'all': 1}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 3632, 'message': 0.0045, 'country': 'CA', 'sunrise': 1529573863, 'sunset': 1529629657}, 'id': 6145890, 'name': 'Shelburne', 'cod': 200}
    'Processing Record 152 | ituni, gy'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for ituni, gy**
    'Processing Record 153 | hithadhoo, mv'
    {'coord': {'lon': 73.08, 'lat': -0.6}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 83.97, 'pressure': 1024.86, 'humidity': 100, 'temp_min': 83.97, 'temp_max': 83.97, 'sea_level': 1024.98, 'grnd_level': 1024.86}, 'wind': {'speed': 7.43, 'deg': 190.003}, 'clouds': {'all': 80}, 'dt': 1529554497, 'sys': {'message': 0.0083, 'country': 'MV', 'sunrise': 1529543209, 'sunset': 1529586726}, 'id': 1282256, 'name': 'Hithadhoo', 'cod': 200}
    'Processing Record 154 | amahai, id'
    {'coord': {'lon': 129, 'lat': -3.31}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 78.84, 'pressure': 1024.86, 'humidity': 100, 'temp_min': 78.84, 'temp_max': 78.84, 'sea_level': 1025.39, 'grnd_level': 1024.86}, 'wind': {'speed': 3.96, 'deg': 129.003}, 'rain': {'3h': 0.14}, 'clouds': {'all': 88}, 'dt': 1529554564, 'sys': {'message': 0.0032, 'country': 'ID', 'sunrise': 1529530068, 'sunset': 1529573021}, 'id': 1651591, 'name': 'Amahai', 'cod': 200}
    'Processing Record 155 | imeni babushkina, ru'
    {'coord': {'lon': 43.13, 'lat': 59.76}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 49.68, 'pressure': 994.47, 'humidity': 96, 'temp_min': 49.68, 'temp_max': 49.68, 'sea_level': 1012.62, 'grnd_level': 994.47}, 'wind': {'speed': 20.85, 'deg': 301.003}, 'rain': {'3h': 2.295}, 'clouds': {'all': 92}, 'dt': 1529554564, 'sys': {'message': 0.0058, 'country': 'RU', 'sunrise': 1529538357, 'sunset': 1529605955}, 'id': 556858, 'name': 'Imeni Babushkina', 'cod': 200}
    'Processing Record 156 | portland, au'
    {'coord': {'lon': 149.98, 'lat': -33.35}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 49.14, 'pressure': 944.86, 'humidity': 78, 'temp_min': 49.14, 'temp_max': 49.14, 'sea_level': 1041.64, 'grnd_level': 944.86}, 'wind': {'speed': 2.73, 'deg': 223.503}, 'clouds': {'all': 68}, 'dt': 1529554564, 'sys': {'message': 0.0041, 'country': 'AU', 'sunrise': 1529528613, 'sunset': 1529564405}, 'id': 2152668, 'name': 'Portland', 'cod': 200}
    'Processing Record 157 | provideniya, ru'
    {'coord': {'lon': -173.23, 'lat': 64.42}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 44.6, 'pressure': 1016, 'humidity': 70, 'temp_min': 44.6, 'temp_max': 44.6}, 'visibility': 10000, 'wind': {'speed': 13.42, 'deg': 10}, 'clouds': {'all': 75}, 'dt': 1529551800, 'sys': {'type': 1, 'id': 7239, 'message': 0.0038, 'country': 'RU', 'sunrise': 1529585582, 'sunset': 1529662591}, 'id': 4031574, 'name': 'Provideniya', 'cod': 200}
    'Processing Record 158 | potiskum, ng'
    {'coord': {'lon': 11.08, 'lat': 11.71}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 70.56, 'pressure': 981.98, 'humidity': 94, 'temp_min': 70.56, 'temp_max': 70.56, 'sea_level': 1024.98, 'grnd_level': 981.98}, 'wind': {'speed': 8.77, 'deg': 213.503}, 'clouds': {'all': 92}, 'dt': 1529554565, 'sys': {'message': 0.0032, 'country': 'NG', 'sunrise': 1529556786, 'sunset': 1529602914}, 'id': 2324767, 'name': 'Potiskum', 'cod': 200}
    'Processing Record 159 | san cristobal, ec'
    {'coord': {'lon': -79.44, 'lat': -1.02}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10n'}], 'base': 'stations', 'main': {'temp': 59.04, 'pressure': 861.28, 'humidity': 100, 'temp_min': 59.04, 'temp_max': 59.04, 'sea_level': 1026.89, 'grnd_level': 861.28}, 'wind': {'speed': 1.16, 'deg': 68.0034}, 'rain': {'3h': 2.725}, 'clouds': {'all': 64}, 'dt': 1529554530, 'sys': {'message': 0.0046, 'country': 'EC', 'sunrise': 1529579863, 'sunset': 1529623293}, 'id': 3652567, 'name': 'San Cristobal', 'cod': 200}
    'Processing Record 160 | husavik, is'
    {'coord': {'lon': -17.34, 'lat': 66.04}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 35.6, 'pressure': 1020, 'humidity': 100, 'temp_min': 35.6, 'temp_max': 35.6}, 'visibility': 10000, 'wind': {'speed': 2.24}, 'clouds': {'all': 0}, 'dt': 1529553600, 'sys': {'type': 1, 'id': 4826, 'message': 0.0048, 'country': 'IS', 'sunrise': 0, 'sunset': 0}, 'id': 2629833, 'name': 'Husavik', 'cod': 200}
    'Processing Record 161 | posse, br'
    {'coord': {'lon': -46.36, 'lat': -14.08}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 66.87, 'pressure': 942.02, 'humidity': 66, 'temp_min': 66.87, 'temp_max': 66.87, 'sea_level': 1032.12, 'grnd_level': 942.02}, 'wind': {'speed': 12.91, 'deg': 94.5034}, 'clouds': {'all': 0}, 'dt': 1529554565, 'sys': {'message': 0.004, 'country': 'BR', 'sunrise': 1529573307, 'sunset': 1529613968}, 'id': 3452599, 'name': 'Posse', 'cod': 200}
    'Processing Record 162 | posadas, ar'
    {'coord': {'lon': -55.9, 'lat': -27.37}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 64.4, 'pressure': 1016, 'humidity': 88, 'temp_min': 64.4, 'temp_max': 64.4}, 'visibility': 10000, 'wind': {'speed': 4.7, 'deg': 110}, 'clouds': {'all': 0}, 'dt': 1529553600, 'sys': {'type': 1, 'id': 4727, 'message': 0.0037, 'country': 'AR', 'sunrise': 1529577186, 'sunset': 1529614669}, 'id': 3429886, 'name': 'Posadas', 'cod': 200}
    'Processing Record 163 | hami, cn'
    {'coord': {'lon': 93.51, 'lat': 42.84}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 85.77, 'pressure': 937.64, 'humidity': 45, 'temp_min': 85.77, 'temp_max': 85.77, 'sea_level': 1015.74, 'grnd_level': 937.64}, 'wind': {'speed': 4.63, 'deg': 143.003}, 'clouds': {'all': 80}, 'dt': 1529554565, 'sys': {'message': 0.0031, 'country': 'CN', 'sunrise': 1529532445, 'sunset': 1529587682}, 'id': 1529484, 'name': 'Hami', 'cod': 200}
    'Processing Record 164 | samarai, pg'
    {'coord': {'lon': 150.67, 'lat': -10.62}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 78.12, 'pressure': 1023.89, 'humidity': 100, 'temp_min': 78.12, 'temp_max': 78.12, 'sea_level': 1027.01, 'grnd_level': 1023.89}, 'wind': {'speed': 17.05, 'deg': 137.503}, 'clouds': {'all': 92}, 'dt': 1529554487, 'sys': {'message': 0.0035, 'country': 'PG', 'sunrise': 1529525637, 'sunset': 1529567050}, 'id': 2132606, 'name': 'Samarai', 'cod': 200}
    'Processing Record 165 | laguna, br'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for laguna, br**
    'Processing Record 166 | kaitangata, nz'
    {'coord': {'lon': 169.85, 'lat': -46.28}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 43.29, 'pressure': 1018.78, 'humidity': 90, 'temp_min': 43.29, 'temp_max': 43.29, 'sea_level': 1036.21, 'grnd_level': 1018.78}, 'wind': {'speed': 3.62, 'deg': 125.503}, 'clouds': {'all': 0}, 'dt': 1529554812, 'sys': {'message': 0.0034, 'country': 'NZ', 'sunrise': 1529526254, 'sunset': 1529557224}, 'id': 2208248, 'name': 'Kaitangata', 'cod': 200}
    'Processing Record 167 | airai, pw'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for airai, pw**
    'Processing Record 168 | melfort, ca'
    {'coord': {'lon': -104.61, 'lat': 52.87}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 78.8, 'pressure': 1013, 'humidity': 41, 'temp_min': 78.8, 'temp_max': 78.8}, 'visibility': 14484, 'wind': {'speed': 10.29, 'deg': 210}, 'clouds': {'all': 75}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 3923, 'message': 0.0029, 'country': 'CA', 'sunrise': 1529577187, 'sunset': 1529638051}, 'id': 6071876, 'name': 'Melfort', 'cod': 200}
    'Processing Record 169 | codrington, ag'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for codrington, ag**
    'Processing Record 170 | tiarei, pf'
    {'coord': {'lon': -149.33, 'lat': -17.53}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'base': 'stations', 'main': {'temp': 80.6, 'pressure': 1015, 'humidity': 69, 'temp_min': 80.6, 'temp_max': 80.6}, 'visibility': 10000, 'wind': {'speed': 1.12, 'deg': 220}, 'clouds': {'all': 40}, 'dt': 1529553600, 'sys': {'type': 1, 'id': 8343, 'message': 0.0078, 'country': 'PF', 'sunrise': 1529598409, 'sunset': 1529638299}, 'id': 4033356, 'name': 'Tiarei', 'cod': 200}
    'Processing Record 171 | casa nova, br'
    {'coord': {'lon': -39.23, 'lat': -11.77}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10n'}], 'base': 'stations', 'main': {'temp': 69.21, 'pressure': 1004.35, 'humidity': 98, 'temp_min': 69.21, 'temp_max': 69.21, 'sea_level': 1032.77, 'grnd_level': 1004.35}, 'wind': {'speed': 5.19, 'deg': 118.503}, 'rain': {'3h': 1.345}, 'clouds': {'all': 92}, 'dt': 1529554566, 'sys': {'message': 0.0033, 'country': 'BR', 'sunrise': 1529571343, 'sunset': 1529612509}, 'id': 3451474, 'name': 'Casa Nova', 'cod': 200}
    'Processing Record 172 | kramat, id'
    {'coord': {'lon': 112.64, 'lat': -7.04}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 83.97, 'pressure': 1024.86, 'humidity': 88, 'temp_min': 83.97, 'temp_max': 83.97, 'sea_level': 1025.92, 'grnd_level': 1024.86}, 'wind': {'speed': 3.4, 'deg': 132.003}, 'clouds': {'all': 80}, 'dt': 1529554567, 'sys': {'message': 0.0075, 'country': 'ID', 'sunrise': 1529534385, 'sunset': 1529576558}, 'id': 1640765, 'name': 'Kramat', 'cod': 200}
    'Processing Record 173 | belushya guba, ru'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for belushya guba, ru**
    'Processing Record 174 | kaili, cn'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for kaili, cn**
    'Processing Record 175 | villa bruzual, ve'
    {'coord': {'lon': -69.12, 'lat': 9.33}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'base': 'stations', 'main': {'temp': 73.4, 'pressure': 1017, 'humidity': 94, 'temp_min': 73.4, 'temp_max': 73.4}, 'visibility': 10000, 'wind': {'speed': 2.95, 'deg': 83.5034}, 'clouds': {'all': 40}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 4287, 'message': 0.0042, 'country': 'VE', 'sunrise': 1529576296, 'sunset': 1529621906}, 'id': 3625346, 'name': 'Villa Bruzual', 'cod': 200}
    'Processing Record 176 | cuiluan, cn'
    {'coord': {'lon': 128.65, 'lat': 47.72}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'base': 'stations', 'main': {'temp': 67.23, 'pressure': 966.99, 'humidity': 61, 'temp_min': 67.23, 'temp_max': 67.23, 'sea_level': 1013.19, 'grnd_level': 966.99}, 'wind': {'speed': 8.88, 'deg': 341.503}, 'clouds': {'all': 36}, 'dt': 1529554567, 'sys': {'message': 0.0046, 'country': 'CN', 'sunrise': 1529522820, 'sunset': 1529580437}, 'id': 2033413, 'name': 'Cuiluan', 'cod': 200}
    'Processing Record 177 | mendota, us'
    {'coord': {'lon': -120.38, 'lat': 36.75}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 83.12, 'pressure': 1012, 'humidity': 32, 'temp_min': 80.6, 'temp_max': 86}, 'visibility': 16093, 'wind': {'speed': 11.41, 'deg': 320}, 'clouds': {'all': 1}, 'dt': 1529553360, 'sys': {'type': 1, 'id': 418, 'message': 0.0034, 'country': 'US', 'sunrise': 1529584980, 'sunset': 1529637829}, 'id': 5372190, 'name': 'Mendota', 'cod': 200}
    'Processing Record 178 | bambous virieux, mu'
    {'coord': {'lon': 57.76, 'lat': -20.34}, 'weather': [{'id': 521, 'main': 'Rain', 'description': 'shower rain', 'icon': '09d'}], 'base': 'stations', 'main': {'temp': 71.6, 'pressure': 1021, 'humidity': 94, 'temp_min': 71.6, 'temp_max': 71.6}, 'visibility': 10000, 'wind': {'speed': 4.41, 'deg': 148.003}, 'clouds': {'all': 75}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 6729, 'message': 0.0041, 'country': 'MU', 'sunrise': 1529549026, 'sunset': 1529588264}, 'id': 1106677, 'name': 'Bambous Virieux', 'cod': 200}
    'Processing Record 179 | santa cruz, cr'
    {'coord': {'lon': -85.58, 'lat': 10.26}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 73.4, 'pressure': 1015, 'humidity': 100, 'temp_min': 73.4, 'temp_max': 73.4}, 'visibility': 10000, 'wind': {'speed': 4.7, 'deg': 180}, 'clouds': {'all': 75}, 'dt': 1529553600, 'sys': {'type': 1, 'id': 4217, 'message': 0.0043, 'country': 'CR', 'sunrise': 1529580146, 'sunset': 1529625957}, 'id': 3621607, 'name': 'Santa Cruz', 'cod': 200}
    'Processing Record 180 | meulaboh, id'
    {'coord': {'lon': 96.13, 'lat': 4.14}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 84.15, 'pressure': 1021.94, 'humidity': 100, 'temp_min': 84.15, 'temp_max': 84.15, 'sea_level': 1024.29, 'grnd_level': 1021.94}, 'wind': {'speed': 1.72, 'deg': 190.503}, 'clouds': {'all': 0}, 'dt': 1529554568, 'sys': {'message': 0.0039, 'country': 'ID', 'sunrise': 1529537181, 'sunset': 1529581688}, 'id': 1214488, 'name': 'Meulaboh', 'cod': 200}
    'Processing Record 181 | khatanga, ru'
    {'coord': {'lon': 102.47, 'lat': 71.98}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 54.81, 'pressure': 1013.51, 'humidity': 100, 'temp_min': 54.81, 'temp_max': 54.81, 'sea_level': 1018.21, 'grnd_level': 1013.51}, 'wind': {'speed': 18.05, 'deg': 56.0034}, 'rain': {'3h': 0.275}, 'clouds': {'all': 80}, 'dt': 1529554568, 'sys': {'message': 0.024, 'country': 'RU', 'sunrise': 0, 'sunset': 0}, 'id': 2022572, 'name': 'Khatanga', 'cod': 200}
    'Processing Record 182 | samalaeulu, ws'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for samalaeulu, ws**
    'Processing Record 183 | khasan, ru'
    {'coord': {'lon': 130.64, 'lat': 42.43}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 65.52, 'pressure': 1006.14, 'humidity': 77, 'temp_min': 65.52, 'temp_max': 65.52, 'sea_level': 1014.36, 'grnd_level': 1006.14}, 'wind': {'speed': 10.33, 'deg': 322.503}, 'clouds': {'all': 64}, 'dt': 1529554568, 'sys': {'message': 0.0207, 'country': 'RU', 'sunrise': 1529523622, 'sunset': 1529578681}, 'id': 2039557, 'name': 'Khasan', 'cod': 200}
    'Processing Record 184 | berlevag, no'
    {'coord': {'lon': 29.09, 'lat': 70.86}, 'weather': [{'id': 520, 'main': 'Rain', 'description': 'light intensity shower rain', 'icon': '09d'}], 'base': 'stations', 'main': {'temp': 44.6, 'pressure': 997, 'humidity': 93, 'temp_min': 44.6, 'temp_max': 44.6}, 'visibility': 10000, 'wind': {'speed': 8.05, 'deg': 60}, 'clouds': {'all': 75}, 'dt': 1529553000, 'sys': {'type': 1, 'id': 5307, 'message': 0.0038, 'country': 'NO', 'sunrise': 0, 'sunset': 0}, 'id': 780687, 'name': 'Berlevag', 'cod': 200}
    'Processing Record 185 | illoqqortoormiut, gl'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for illoqqortoormiut, gl**
    'Processing Record 186 | magtanggol, ph'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for magtanggol, ph**
    'Processing Record 187 | lauria, it'
    {'coord': {'lon': 15.84, 'lat': 40.05}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 55.08, 'pressure': 960.91, 'humidity': 100, 'temp_min': 55.08, 'temp_max': 55.08, 'sea_level': 1032.08, 'grnd_level': 960.91}, 'wind': {'speed': 0.94, 'deg': 89.5034}, 'clouds': {'all': 0}, 'dt': 1529554569, 'sys': {'message': 0.0032, 'country': 'IT', 'sunrise': 1529551668, 'sunset': 1529605747}, 'id': 3175034, 'name': 'Lauria', 'cod': 200}
    'Processing Record 188 | ambilobe, mg'
    {'coord': {'lon': 49.05, 'lat': -13.19}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 64.71, 'pressure': 1006.3, 'humidity': 85, 'temp_min': 64.71, 'temp_max': 64.71, 'sea_level': 1030.5, 'grnd_level': 1006.3}, 'wind': {'speed': 5.64, 'deg': 111.503}, 'clouds': {'all': 0}, 'dt': 1529554536, 'sys': {'message': 0.0033, 'country': 'MG', 'sunrise': 1529550307, 'sunset': 1529591164}, 'id': 1082243, 'name': 'Ambilobe', 'cod': 200}
    'Processing Record 189 | saint george, bm'
    {'coord': {'lon': -64.68, 'lat': 32.38}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 77, 'pressure': 1014, 'humidity': 83, 'temp_min': 77, 'temp_max': 77}, 'visibility': 10000, 'wind': {'speed': 13.87, 'deg': 230}, 'clouds': {'all': 20}, 'dt': 1529553300, 'sys': {'type': 1, 'id': 4169, 'message': 0.0032, 'country': 'BM', 'sunrise': 1529572333, 'sunset': 1529623737}, 'id': 3573061, 'name': 'Saint George', 'cod': 200}
    'Processing Record 190 | zhigansk, ru'
    {'coord': {'lon': 123.37, 'lat': 66.77}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 68.94, 'pressure': 1009.3, 'humidity': 39, 'temp_min': 68.94, 'temp_max': 68.94, 'sea_level': 1017.2, 'grnd_level': 1009.3}, 'wind': {'speed': 3.85, 'deg': 229.503}, 'clouds': {'all': 0}, 'dt': 1529554537, 'sys': {'message': 0.0035, 'country': 'RU', 'sunrise': 0, 'sunset': 0}, 'id': 2012530, 'name': 'Zhigansk', 'cod': 200}
    'Processing Record 191 | lebu, cl'
    {'coord': {'lon': -73.65, 'lat': -37.62}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10n'}], 'base': 'stations', 'main': {'temp': 52.11, 'pressure': 1036.13, 'humidity': 100, 'temp_min': 52.11, 'temp_max': 52.11, 'sea_level': 1039.86, 'grnd_level': 1036.13}, 'wind': {'speed': 12.01, 'deg': 286.003}, 'rain': {'3h': 0.215}, 'clouds': {'all': 92}, 'dt': 1529554569, 'sys': {'message': 0.0114, 'country': 'CL', 'sunrise': 1529582978, 'sunset': 1529617398}, 'id': 3883457, 'name': 'Lebu', 'cod': 200}
    'Processing Record 192 | tornio, fi'
    {'coord': {'lon': 27.27, 'lat': 61.12}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 53.02, 'pressure': 1006, 'humidity': 76, 'temp_min': 51.8, 'temp_max': 53.6}, 'visibility': 10000, 'wind': {'speed': 3.36, 'deg': 210}, 'clouds': {'all': 0}, 'dt': 1529553000, 'sys': {'type': 1, 'id': 5047, 'message': 0.0034, 'country': 'FI', 'sunrise': 1529541170, 'sunset': 1529610757}, 'id': 637314, 'name': 'Tornio', 'cod': 200}
    'Processing Record 193 | ribeira grande, pt'
    {'coord': {'lon': -28.7, 'lat': 38.52}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 70.83, 'pressure': 1036.37, 'humidity': 100, 'temp_min': 70.83, 'temp_max': 70.83, 'sea_level': 1039.86, 'grnd_level': 1036.37}, 'wind': {'speed': 2.62, 'deg': 306.003}, 'clouds': {'all': 68}, 'dt': 1529554570, 'sys': {'message': 0.004, 'country': 'PT', 'sunrise': 1529562652, 'sunset': 1529616144}, 'id': 3372707, 'name': 'Ribeira Grande', 'cod': 200}
    'Processing Record 194 | matagami, ca'
    {'coord': {'lon': -77.63, 'lat': 49.76}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 41, 'pressure': 1015, 'humidity': 53, 'temp_min': 41, 'temp_max': 41}, 'visibility': 14484, 'wind': {'speed': 8.05, 'deg': 340}, 'clouds': {'all': 1}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 3822, 'message': 0.005, 'country': 'CA', 'sunrise': 1529571748, 'sunset': 1529630538}, 'id': 6067747, 'name': 'Matagami', 'cod': 200}
    'Processing Record 195 | saint-francois, gp'
    {'coord': {'lon': -61.27, 'lat': 16.25}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 75.2, 'pressure': 1017, 'humidity': 78, 'temp_min': 75.2, 'temp_max': 75.2}, 'visibility': 10000, 'wind': {'speed': 6.93, 'deg': 120}, 'clouds': {'all': 20}, 'dt': 1529553600, 'sys': {'type': 1, 'id': 4145, 'message': 0.009, 'country': 'GP', 'sunrise': 1529573642, 'sunset': 1529620791}, 'id': 3578441, 'name': 'Saint-Francois', 'cod': 200}
    'Processing Record 196 | evensk, ru'
    {'coord': {'lon': 159.24, 'lat': 61.92}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 'base': 'stations', 'main': {'temp': 44.91, 'pressure': 1022.75, 'humidity': 100, 'temp_min': 44.91, 'temp_max': 44.91, 'sea_level': 1030.94, 'grnd_level': 1022.75}, 'wind': {'speed': 5.41, 'deg': 179.503}, 'clouds': {'all': 12}, 'dt': 1529554531, 'sys': {'message': 0.0046, 'country': 'RU', 'sunrise': 1529508811, 'sunset': 1529579762}, 'id': 2125693, 'name': 'Evensk', 'cod': 200}
    'Processing Record 197 | ossora, ru'
    {'coord': {'lon': 163.07, 'lat': 59.24}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 'base': 'stations', 'main': {'temp': 51.93, 'pressure': 1018.78, 'humidity': 94, 'temp_min': 51.93, 'temp_max': 51.93, 'sea_level': 1031.23, 'grnd_level': 1018.78}, 'wind': {'speed': 1.72, 'deg': 161.003}, 'clouds': {'all': 20}, 'dt': 1529554814, 'sys': {'message': 0.0041, 'country': 'RU', 'sunrise': 1529509906, 'sunset': 1529576828}, 'id': 2122389, 'name': 'Ossora', 'cod': 200}
    'Processing Record 198 | yar-sale, ru'
    {'coord': {'lon': 70.83, 'lat': 66.83}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '02d'}], 'base': 'stations', 'main': {'temp': 52.11, 'pressure': 998.68, 'humidity': 85, 'temp_min': 52.11, 'temp_max': 52.11, 'sea_level': 1000.01, 'grnd_level': 998.68}, 'wind': {'speed': 3.74, 'deg': 354.003}, 'clouds': {'all': 8}, 'dt': 1529554747, 'sys': {'message': 0.0035, 'country': 'RU', 'sunrise': 0, 'sunset': 0}, 'id': 1486321, 'name': 'Yar-Sale', 'cod': 200}
    'Processing Record 199 | severo-kurilsk, ru'
    {'coord': {'lon': 156.12, 'lat': 50.68}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 42.66, 'pressure': 1020.16, 'humidity': 100, 'temp_min': 42.66, 'temp_max': 42.66, 'sea_level': 1033.29, 'grnd_level': 1020.16}, 'wind': {'speed': 7.2, 'deg': 164.003}, 'clouds': {'all': 76}, 'dt': 1529554482, 'sys': {'message': 0.0136, 'country': 'RU', 'sunrise': 1529515353, 'sunset': 1529574717}, 'id': 2121385, 'name': 'Severo-Kurilsk', 'cod': 200}
    'Processing Record 200 | saint-joseph, re'
    {'coord': {'lon': 55.62, 'lat': -21.37}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 68.13, 'pressure': 1021, 'humidity': 53, 'temp_min': 66.2, 'temp_max': 71.6}, 'visibility': 10000, 'wind': {'speed': 8.05, 'deg': 30}, 'clouds': {'all': 75}, 'dt': 1529551800, 'sys': {'type': 1, 'id': 6792, 'message': 0.0039, 'country': 'RE', 'sunrise': 1529549662, 'sunset': 1529588655}, 'id': 6690296, 'name': 'Saint-Joseph', 'cod': 200}
    'Processing Record 201 | plettenberg bay, za'
    {'coord': {'lon': 23.37, 'lat': -34.05}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 56.52, 'pressure': 1025.11, 'humidity': 100, 'temp_min': 56.52, 'temp_max': 56.52, 'sea_level': 1032.32, 'grnd_level': 1025.11}, 'wind': {'speed': 7.76, 'deg': 66.0034}, 'clouds': {'all': 0}, 'dt': 1529554815, 'sys': {'message': 0.0037, 'country': 'ZA', 'sunrise': 1529559111, 'sunset': 1529594689}, 'id': 964712, 'name': 'Plettenberg Bay', 'cod': 200}
    'Processing Record 202 | moquegua, pe'
    {'coord': {'lon': -70.93, 'lat': -17.19}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 51.84, 'pressure': 847.83, 'humidity': 76, 'temp_min': 51.84, 'temp_max': 51.84, 'sea_level': 1031.95, 'grnd_level': 847.83}, 'wind': {'speed': 1.83, 'deg': 80.5034}, 'clouds': {'all': 8}, 'dt': 1529554570, 'sys': {'message': 0.0035, 'country': 'PE', 'sunrise': 1529579552, 'sunset': 1529619519}, 'id': 3934608, 'name': 'Moquegua', 'cod': 200}
    'Processing Record 203 | ulyanovo, ru'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for ulyanovo, ru**
    'Processing Record 204 | cairns, au'
    {'coord': {'lon': 145.77, 'lat': -16.92}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 'base': 'stations', 'main': {'temp': 77, 'pressure': 1018, 'humidity': 44, 'temp_min': 77, 'temp_max': 77}, 'visibility': 10000, 'wind': {'speed': 19.46, 'deg': 130}, 'clouds': {'all': 20}, 'dt': 1529551800, 'sys': {'type': 1, 'id': 8166, 'message': 0.0149, 'country': 'AU', 'sunrise': 1529527505, 'sunset': 1529567533}, 'id': 2172797, 'name': 'Cairns', 'cod': 200}
    'Processing Record 205 | brejinho, br'
    {'coord': {'lon': -35.36, 'lat': -6.2}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 73.4, 'pressure': 1016, 'humidity': 78, 'temp_min': 73.4, 'temp_max': 73.4}, 'visibility': 10000, 'wind': {'speed': 8.05, 'deg': 160}, 'clouds': {'all': 0}, 'dt': 1529553600, 'sys': {'type': 1, 'id': 4546, 'message': 0.0042, 'country': 'BR', 'sunrise': 1529569822, 'sunset': 1529612172}, 'id': 3404924, 'name': 'Brejinho', 'cod': 200}
    'Processing Record 206 | da lat, vn'
    {'coord': {'lon': 108.44, 'lat': 11.95}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 74.16, 'pressure': 906.6, 'humidity': 80, 'temp_min': 74.16, 'temp_max': 74.16, 'sea_level': 1023.85, 'grnd_level': 906.6}, 'wind': {'speed': 3.4, 'deg': 274.503}, 'clouds': {'all': 92}, 'dt': 1529554571, 'sys': {'message': 0.0037, 'country': 'VN', 'sunrise': 1529533389, 'sunset': 1529579570}, 'id': 1584071, 'name': 'Da Lat', 'cod': 200}
    'Processing Record 207 | chuy, uy'
    {'coord': {'lon': -53.46, 'lat': -33.69}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 58.86, 'pressure': 1026.16, 'humidity': 90, 'temp_min': 58.86, 'temp_max': 58.86, 'sea_level': 1027.74, 'grnd_level': 1026.16}, 'wind': {'speed': 11.68, 'deg': 345.503}, 'clouds': {'all': 68}, 'dt': 1529554571, 'sys': {'message': 0.0037, 'country': 'UY', 'sunrise': 1529577497, 'sunset': 1529613186}, 'id': 3443061, 'name': 'Chuy', 'cod': 200}
    'Processing Record 208 | sirjan, ir'
    {'coord': {'lon': 55.67, 'lat': 29.44}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 70.47, 'pressure': 821.32, 'humidity': 23, 'temp_min': 70.47, 'temp_max': 70.47, 'sea_level': 1018.58, 'grnd_level': 821.32}, 'wind': {'speed': 3.18, 'deg': 73.0034}, 'clouds': {'all': 0}, 'dt': 1529554571, 'sys': {'message': 0.0034, 'country': 'IR', 'sunrise': 1529543885, 'sunset': 1529594408}, 'id': 114259, 'name': 'Sirjan', 'cod': 200}
    'Processing Record 209 | ancud, cl'
    {'coord': {'lon': -73.83, 'lat': -41.87}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 46.44, 'pressure': 1025.02, 'humidity': 82, 'temp_min': 46.44, 'temp_max': 46.44, 'sea_level': 1032.6, 'grnd_level': 1025.02}, 'wind': {'speed': 10.45, 'deg': 251.003}, 'clouds': {'all': 88}, 'dt': 1529554480, 'sys': {'message': 0.0035, 'country': 'CL', 'sunrise': 1529583800, 'sunset': 1529616663}, 'id': 3899695, 'name': 'Ancud', 'cod': 200}
    'Processing Record 210 | yiyang, cn'
    {'coord': {'lon': 112.35, 'lat': 28.59}, 'weather': [{'id': 501, 'main': 'Rain', 'description': 'moderate rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 75.69, 'pressure': 1013.27, 'humidity': 100, 'temp_min': 75.69, 'temp_max': 75.69, 'sea_level': 1018.82, 'grnd_level': 1013.27}, 'wind': {'speed': 5.19, 'deg': 49.0034}, 'rain': {'3h': 8.71}, 'clouds': {'all': 92}, 'dt': 1529554572, 'sys': {'message': 0.0034, 'country': 'CN', 'sunrise': 1529530402, 'sunset': 1529580681}, 'id': 1808316, 'name': 'Yiyang', 'cod': 200}
    'Processing Record 211 | maceio, br'
    {'coord': {'lon': -35.74, 'lat': -9.67}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 68, 'pressure': 1018, 'humidity': 100, 'temp_min': 68, 'temp_max': 68}, 'visibility': 10000, 'wind': {'speed': 3.36, 'deg': 280}, 'clouds': {'all': 75}, 'dt': 1529553600, 'sys': {'type': 1, 'id': 4538, 'message': 0.0037, 'country': 'BR', 'sunrise': 1529570280, 'sunset': 1529611896}, 'id': 3395981, 'name': 'Maceio', 'cod': 200}
    'Processing Record 212 | vega de alatorre, mx'
    {'coord': {'lon': -96.65, 'lat': 20.03}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 77.04, 'pressure': 973.71, 'humidity': 92, 'temp_min': 77.04, 'temp_max': 77.04, 'sea_level': 1021.09, 'grnd_level': 973.71}, 'wind': {'speed': 5.08, 'deg': 149.503}, 'clouds': {'all': 92}, 'dt': 1529554572, 'sys': {'message': 0.0042, 'country': 'MX', 'sunrise': 1529581688, 'sunset': 1529629730}, 'id': 3514843, 'name': 'Vega de Alatorre', 'cod': 200}
    'Processing Record 213 | roald, no'
    {'coord': {'lon': 6.12, 'lat': 62.58}, 'weather': [{'id': 300, 'main': 'Drizzle', 'description': 'light intensity drizzle', 'icon': '09d'}, {'id': 521, 'main': 'Rain', 'description': 'shower rain', 'icon': '09d'}], 'base': 'stations', 'main': {'temp': 45.79, 'pressure': 1007, 'humidity': 100, 'temp_min': 44.6, 'temp_max': 46.4}, 'visibility': 10000, 'wind': {'speed': 8.05, 'deg': 200}, 'clouds': {'all': 75}, 'dt': 1529553000, 'sys': {'type': 1, 'id': 5271, 'message': 0.0148, 'country': 'NO', 'sunrise': 1529544927, 'sunset': 1529617153}, 'id': 3141667, 'name': 'Roald', 'cod': 200}
    'Processing Record 214 | thompson, ca'
    {'coord': {'lon': -97.86, 'lat': 55.74}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 75.2, 'pressure': 1008, 'humidity': 53, 'temp_min': 75.2, 'temp_max': 75.2}, 'visibility': 24140, 'wind': {'speed': 4.7, 'deg': 90}, 'clouds': {'all': 75}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 3406, 'message': 0.011, 'country': 'CA', 'sunrise': 1529574399, 'sunset': 1529637598}, 'id': 6165406, 'name': 'Thompson', 'cod': 200}
    'Processing Record 215 | amderma, ru'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for amderma, ru**
    'Processing Record 216 | saleaula, ws'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for saleaula, ws**
    'Processing Record 217 | mahebourg, mu'
    {'coord': {'lon': 57.7, 'lat': -20.41}, 'weather': [{'id': 521, 'main': 'Rain', 'description': 'shower rain', 'icon': '09d'}], 'base': 'stations', 'main': {'temp': 71.6, 'pressure': 1021, 'humidity': 94, 'temp_min': 71.6, 'temp_max': 71.6}, 'visibility': 10000, 'wind': {'speed': 4.41, 'deg': 148.003}, 'clouds': {'all': 75}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 6729, 'message': 0.003, 'country': 'MU', 'sunrise': 1529549049, 'sunset': 1529588270}, 'id': 934322, 'name': 'Mahebourg', 'cod': 200}
    'Processing Record 218 | ketchikan, us'
    {'coord': {'lon': -131.65, 'lat': 55.34}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10n'}, {'id': 741, 'main': 'Fog', 'description': 'fog', 'icon': '50n'}, {'id': 701, 'main': 'Mist', 'description': 'mist', 'icon': '50n'}], 'base': 'stations', 'main': {'temp': 55.96, 'pressure': 1014, 'humidity': 100, 'temp_min': 53.6, 'temp_max': 60.8}, 'visibility': 805, 'wind': {'speed': 9.17, 'deg': 210}, 'clouds': {'all': 90}, 'dt': 1529554020, 'sys': {'type': 1, 'id': 113, 'message': 0.005, 'country': 'US', 'sunrise': 1529582688, 'sunset': 1529645530}, 'id': 5554428, 'name': 'Ketchikan', 'cod': 200}
    'Processing Record 219 | strathpeffer, gb'
    {'coord': {'lon': -4.54, 'lat': 57.59}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'base': 'stations', 'main': {'temp': 45.55, 'pressure': 1021, 'humidity': 87, 'temp_min': 44.6, 'temp_max': 46.4}, 'visibility': 10000, 'wind': {'speed': 5.82, 'deg': 250}, 'clouds': {'all': 40}, 'dt': 1529553000, 'sys': {'type': 1, 'id': 5120, 'message': 0.0032, 'country': 'GB', 'sunrise': 1529551092, 'sunset': 1529616105}, 'id': 2651245, 'name': 'Strathpeffer', 'cod': 200}
    'Processing Record 220 | khovu-aksy, ru'
    {'coord': {'lon': 93.72, 'lat': 51.13}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 66.69, 'pressure': 857.23, 'humidity': 61, 'temp_min': 66.69, 'temp_max': 66.69, 'sea_level': 1018.21, 'grnd_level': 857.23}, 'wind': {'speed': 2.17, 'deg': 320.003}, 'rain': {'3h': 0.497}, 'clouds': {'all': 48}, 'dt': 1529554573, 'sys': {'message': 0.0071, 'country': 'RU', 'sunrise': 1529530185, 'sunset': 1529589841}, 'id': 1503527, 'name': 'Khovu-Aksy', 'cod': 200}
    'Processing Record 221 | iralaya, hn'
    {'coord': {'lon': -83.23, 'lat': 15}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 78.75, 'pressure': 1025.92, 'humidity': 97, 'temp_min': 78.75, 'temp_max': 78.75, 'sea_level': 1026.44, 'grnd_level': 1025.92}, 'wind': {'speed': 5.86, 'deg': 105.503}, 'clouds': {'all': 56}, 'dt': 1529554573, 'sys': {'message': 0.01, 'country': 'HN', 'sunrise': 1529579056, 'sunset': 1529625919}, 'id': 3608828, 'name': 'Iralaya', 'cod': 200}
    'Processing Record 222 | yomitan, jp'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for yomitan, jp**
    'Processing Record 223 | boca do acre, br'
    {'coord': {'lon': -67.39, 'lat': -8.76}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'base': 'stations', 'main': {'temp': 70.47, 'pressure': 1010.68, 'humidity': 84, 'temp_min': 70.47, 'temp_max': 70.47, 'sea_level': 1028.14, 'grnd_level': 1010.68}, 'wind': {'speed': 2.39, 'deg': 186.003}, 'clouds': {'all': 32}, 'dt': 1529554573, 'sys': {'message': 0.0042, 'country': 'BR', 'sunrise': 1529577781, 'sunset': 1529619590}, 'id': 3664956, 'name': 'Boca do Acre', 'cod': 200}
    'Processing Record 224 | rawson, ar'
    {'coord': {'lon': -65.11, 'lat': -43.3}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 48.87, 'pressure': 1002.81, 'humidity': 42, 'temp_min': 48.87, 'temp_max': 48.87, 'sea_level': 1014.04, 'grnd_level': 1002.81}, 'wind': {'speed': 21.52, 'deg': 258.003}, 'clouds': {'all': 0}, 'dt': 1529554574, 'sys': {'message': 0.0042, 'country': 'AR', 'sunrise': 1529581996, 'sunset': 1529614281}, 'id': 3839307, 'name': 'Rawson', 'cod': 200}
    'Processing Record 225 | san luis, mx'
    {'coord': {'lon': -114.78, 'lat': 32.49}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 88.43, 'pressure': 1008, 'humidity': 15, 'temp_min': 86, 'temp_max': 91.4}, 'visibility': 16093, 'wind': {'speed': 6.93, 'deg': 190}, 'clouds': {'all': 1}, 'dt': 1529553420, 'sys': {'type': 1, 'id': 337, 'message': 0.0036, 'country': 'MX', 'sunrise': 1529584342, 'sunset': 1529635779}, 'id': 5312913, 'name': 'San Luis', 'cod': 200}
    'Processing Record 226 | athens, us'
    {'coord': {'lon': -83.39, 'lat': 33.96}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 80.22, 'pressure': 1013, 'humidity': 61, 'temp_min': 78.8, 'temp_max': 82.4}, 'visibility': 16093, 'wind': {'speed': 8.05, 'deg': 300}, 'clouds': {'all': 1}, 'dt': 1529553360, 'sys': {'type': 1, 'id': 746, 'message': 0.0132, 'country': 'US', 'sunrise': 1529576573, 'sunset': 1529628479}, 'id': 4180386, 'name': 'Athens', 'cod': 200}
    'Processing Record 227 | bocaranga, cf'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for bocaranga, cf**
    'Processing Record 228 | la ronge, ca'
    {'coord': {'lon': -105.3, 'lat': 55.1}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'base': 'stations', 'main': {'temp': 78.8, 'pressure': 1011, 'humidity': 47, 'temp_min': 78.8, 'temp_max': 78.8}, 'visibility': 24140, 'wind': {'speed': 6.93, 'deg': 230}, 'clouds': {'all': 40}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 3914, 'message': 0.0031, 'country': 'CA', 'sunrise': 1529576468, 'sunset': 1529639101}, 'id': 6050066, 'name': 'La Ronge', 'cod': 200}
    'Processing Record 229 | tuktoyaktuk, ca'
    {'coord': {'lon': -133.03, 'lat': 69.44}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'base': 'stations', 'main': {'temp': 50, 'pressure': 1018, 'humidity': 90, 'temp_min': 50, 'temp_max': 50}, 'visibility': 24140, 'wind': {'speed': 10.29, 'deg': 60}, 'clouds': {'all': 40}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 3555, 'message': 0.0032, 'country': 'CA', 'sunrise': 0, 'sunset': 0}, 'id': 6170031, 'name': 'Tuktoyaktuk', 'cod': 200}
    'Processing Record 230 | fare, pf'
    {'coord': {'lon': -151.02, 'lat': -16.7}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 81.54, 'pressure': 1027.05, 'humidity': 96, 'temp_min': 81.54, 'temp_max': 81.54, 'sea_level': 1028.35, 'grnd_level': 1027.05}, 'wind': {'speed': 15.59, 'deg': 96.0034}, 'clouds': {'all': 92}, 'dt': 1529554575, 'sys': {'message': 0.0033, 'country': 'PF', 'sunrise': 1529598721, 'sunset': 1529638799}, 'id': 4034496, 'name': 'Fare', 'cod': 200}
    'Processing Record 231 | gao, ml'
    {'coord': {'lon': -0.04, 'lat': 16.28}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 80.01, 'pressure': 986.28, 'humidity': 31, 'temp_min': 80.01, 'temp_max': 80.01, 'sea_level': 1017.97, 'grnd_level': 986.28}, 'wind': {'speed': 4.85, 'deg': 161.003}, 'clouds': {'all': 8}, 'dt': 1529554575, 'sys': {'message': 0.0032, 'country': 'ML', 'sunrise': 1529558941, 'sunset': 1529606097}, 'id': 2457163, 'name': 'Gao', 'cod': 200}
    'Processing Record 232 | wagar, sd'
    {'coord': {'lon': 36.2, 'lat': 16.15}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '02d'}], 'base': 'stations', 'main': {'temp': 76.68, 'pressure': 976.23, 'humidity': 75, 'temp_min': 76.68, 'temp_max': 76.68, 'sea_level': 1024.86, 'grnd_level': 976.23}, 'wind': {'speed': 3.96, 'deg': 231.503}, 'clouds': {'all': 8}, 'dt': 1529554817, 'sys': {'message': 0.0034, 'country': 'SD', 'sunrise': 1529550257, 'sunset': 1529597383}, 'id': 364027, 'name': 'Wagar', 'cod': 200}
    'Processing Record 233 | sinnamary, gf'
    {'coord': {'lon': -52.96, 'lat': 5.38}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 80.82, 'pressure': 1027.29, 'humidity': 95, 'temp_min': 80.82, 'temp_max': 80.82, 'sea_level': 1028.75, 'grnd_level': 1027.29}, 'wind': {'speed': 11.12, 'deg': 108.003}, 'clouds': {'all': 80}, 'dt': 1529554818, 'sys': {'message': 0.0126, 'country': 'GF', 'sunrise': 1529572838, 'sunset': 1529617606}, 'id': 3380290, 'name': 'Sinnamary', 'cod': 200}
    'Processing Record 234 | rianxo, es'
    {'coord': {'lon': -8.82, 'lat': 42.65}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 65.43, 'pressure': 1019, 'humidity': 100, 'temp_min': 60.8, 'temp_max': 69.8}, 'visibility': 7000, 'wind': {'speed': 4.7, 'deg': 20}, 'clouds': {'all': 20}, 'dt': 1529551800, 'sys': {'type': 1, 'id': 5500, 'message': 0.0038, 'country': 'ES', 'sunrise': 1529557049, 'sunset': 1529612203}, 'id': 3111879, 'name': 'Rianxo', 'cod': 200}
    'Processing Record 235 | honningsvag, no'
    {'coord': {'lon': 25.97, 'lat': 70.98}, 'weather': [{'id': 300, 'main': 'Drizzle', 'description': 'light intensity drizzle', 'icon': '09d'}, {'id': 520, 'main': 'Rain', 'description': 'light intensity shower rain', 'icon': '09d'}], 'base': 'stations', 'main': {'temp': 44.6, 'pressure': 997, 'humidity': 100, 'temp_min': 44.6, 'temp_max': 44.6}, 'visibility': 6000, 'wind': {'speed': 8.05, 'deg': 340}, 'clouds': {'all': 90}, 'dt': 1529553000, 'sys': {'type': 1, 'id': 5300, 'message': 0.0045, 'country': 'NO', 'sunrise': 0, 'sunset': 0}, 'id': 779554, 'name': 'Honningsvag', 'cod': 200}
    'Processing Record 236 | pevek, ru'
    {'coord': {'lon': 170.27, 'lat': 69.7}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 47.34, 'pressure': 1021.05, 'humidity': 70, 'temp_min': 47.34, 'temp_max': 47.34, 'sea_level': 1028.31, 'grnd_level': 1021.05}, 'wind': {'speed': 2.17, 'deg': 31.5034}, 'clouds': {'all': 0}, 'dt': 1529554575, 'sys': {'message': 0.0034, 'country': 'RU', 'sunrise': 0, 'sunset': 0}, 'id': 2122090, 'name': 'Pevek', 'cod': 200}
    'Processing Record 237 | patitirion, gr'
    {'coord': {'lon': 23.87, 'lat': 39.15}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 'base': 'stations', 'main': {'temp': 76.05, 'pressure': 1014, 'humidity': 69, 'temp_min': 75.2, 'temp_max': 77}, 'visibility': 10000, 'wind': {'speed': 12.91, 'deg': 28.5034}, 'clouds': {'all': 20}, 'dt': 1529553000, 'sys': {'type': 1, 'id': 5696, 'message': 0.0194, 'country': 'GR', 'sunrise': 1529549915, 'sunset': 1529603645}, 'id': 255689, 'name': 'Patitirion', 'cod': 200}
    'Processing Record 238 | harper, lr'
    {'coord': {'lon': -7.71, 'lat': 4.38}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10n'}], 'base': 'stations', 'main': {'temp': 78.48, 'pressure': 1026.89, 'humidity': 100, 'temp_min': 78.48, 'temp_max': 78.48, 'sea_level': 1028.23, 'grnd_level': 1026.89}, 'wind': {'speed': 9.66, 'deg': 267.003}, 'rain': {'3h': 0.195}, 'clouds': {'all': 100}, 'dt': 1529554576, 'sys': {'message': 0.0035, 'country': 'LR', 'sunrise': 1529562081, 'sunset': 1529606639}, 'id': 2276492, 'name': 'Harper', 'cod': 200}
    'Processing Record 239 | cheyenne, us'
    {'coord': {'lon': -104.82, 'lat': 41.14}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 56.5, 'pressure': 1025, 'humidity': 82, 'temp_min': 55.4, 'temp_max': 57.2}, 'visibility': 16093, 'wind': {'speed': 5.82, 'deg': 10}, 'clouds': {'all': 1}, 'dt': 1529553180, 'sys': {'type': 1, 'id': 3073, 'message': 0.0044, 'country': 'US', 'sunrise': 1529580411, 'sunset': 1529634928}, 'id': 5821086, 'name': 'Cheyenne', 'cod': 200}
    'Processing Record 240 | porbandar, in'
    {'coord': {'lon': 69.61, 'lat': 21.64}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'base': 'stations', 'main': {'temp': 87.8, 'pressure': 1004, 'humidity': 70, 'temp_min': 87.8, 'temp_max': 87.8}, 'visibility': 6000, 'wind': {'speed': 13.87, 'deg': 310}, 'clouds': {'all': 40}, 'dt': 1529551800, 'sys': {'type': 1, 'id': 7777, 'message': 0.0034, 'country': 'IN', 'sunrise': 1529541582, 'sunset': 1529590019}, 'id': 1259395, 'name': 'Porbandar', 'cod': 200}
    'Processing Record 241 | san quintin, mx'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for san quintin, mx**
    'Processing Record 242 | coihaique, cl'
    {'coord': {'lon': -72.07, 'lat': -45.58}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 34.43, 'pressure': 1008, 'humidity': 69, 'temp_min': 32, 'temp_max': 37.4}, 'visibility': 10000, 'wind': {'speed': 8.05, 'deg': 250}, 'clouds': {'all': 75}, 'dt': 1529553600, 'sys': {'type': 1, 'id': 4643, 'message': 0.0047, 'country': 'CL', 'sunrise': 1529584162, 'sunset': 1529615456}, 'id': 3894426, 'name': 'Coihaique', 'cod': 200}
    'Processing Record 243 | nanortalik, gl'
    {'coord': {'lon': -45.24, 'lat': 60.14}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10n'}], 'base': 'stations', 'main': {'temp': 36.9, 'pressure': 1001.19, 'humidity': 95, 'temp_min': 36.9, 'temp_max': 36.9, 'sea_level': 1013.15, 'grnd_level': 1001.19}, 'wind': {'speed': 28.12, 'deg': 97.0034}, 'rain': {'3h': 1.87}, 'clouds': {'all': 92}, 'dt': 1529554481, 'sys': {'message': 0.0042, 'country': 'GL', 'sunrise': 1529559309, 'sunset': 1529627427}, 'id': 3421765, 'name': 'Nanortalik', 'cod': 200}
    'Processing Record 244 | sirvintos, lt'
    {'coord': {'lon': 24.95, 'lat': 55.05}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 59.05, 'pressure': 1015, 'humidity': 76, 'temp_min': 55.4, 'temp_max': 62.6}, 'visibility': 10000, 'wind': {'speed': 10.29, 'deg': 180}, 'clouds': {'all': 0}, 'dt': 1529553000, 'sys': {'type': 1, 'id': 5437, 'message': 0.0041, 'country': 'LT', 'sunrise': 1529545224, 'sunset': 1529607816}, 'id': 594607, 'name': 'Sirvintos', 'cod': 200}
    'Processing Record 245 | clarence town, bs'
    {'coord': {'lon': -74.98, 'lat': 23.1}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10n'}], 'base': 'stations', 'main': {'temp': 82.71, 'pressure': 1028.43, 'humidity': 100, 'temp_min': 82.71, 'temp_max': 82.71, 'sea_level': 1028.51, 'grnd_level': 1028.43}, 'wind': {'speed': 5.97, 'deg': 137.003}, 'rain': {'3h': 0.11}, 'clouds': {'all': 0}, 'dt': 1529554819, 'sys': {'message': 0.004, 'country': 'BS', 'sunrise': 1529576105, 'sunset': 1529624909}, 'id': 3572640, 'name': 'Clarence Town', 'cod': 200}
    'Processing Record 246 | ixtapa, mx'
    {'coord': {'lon': -105.21, 'lat': 20.71}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 78.8, 'pressure': 1013, 'humidity': 88, 'temp_min': 78.8, 'temp_max': 78.8}, 'visibility': 16093, 'wind': {'speed': 2.17, 'deg': 297.003}, 'clouds': {'all': 75}, 'dt': 1529552760, 'sys': {'type': 1, 'id': 4011, 'message': 0.0036, 'country': 'MX', 'sunrise': 1529583660, 'sunset': 1529631867}, 'id': 4004293, 'name': 'Ixtapa', 'cod': 200}
    'Processing Record 247 | krasnotorka, ua'
    {'coord': {'lon': 37.52, 'lat': 48.68}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 70.11, 'pressure': 1011.08, 'humidity': 38, 'temp_min': 70.11, 'temp_max': 70.11, 'sea_level': 1029.85, 'grnd_level': 1011.08}, 'wind': {'speed': 8.21, 'deg': 357.503}, 'clouds': {'all': 0}, 'dt': 1529554577, 'sys': {'message': 0.0039, 'country': 'UA', 'sunrise': 1529544426, 'sunset': 1529602580}, 'id': 704303, 'name': 'Krasnotorka', 'cod': 200}
    'Processing Record 248 | pacifica, us'
    {'coord': {'lon': -122.49, 'lat': 37.61}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 57.7, 'pressure': 1016, 'humidity': 76, 'temp_min': 55.4, 'temp_max': 60.8}, 'visibility': 16093, 'wind': {'speed': 18.34, 'deg': 260, 'gust': 10.8}, 'clouds': {'all': 75}, 'dt': 1529553360, 'sys': {'type': 1, 'id': 478, 'message': 0.0055, 'country': 'US', 'sunrise': 1529585333, 'sunset': 1529638490}, 'id': 5380420, 'name': 'Pacifica', 'cod': 200}
    'Processing Record 249 | fort nelson, ca'
    {'coord': {'lon': -122.69, 'lat': 58.81}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 82.4, 'pressure': 1009, 'humidity': 42, 'temp_min': 82.4, 'temp_max': 82.4}, 'visibility': 48279, 'wind': {'speed': 3.36, 'deg': 310}, 'clouds': {'all': 75}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 3278, 'message': 0.0036, 'country': 'CA', 'sunrise': 1529578763, 'sunset': 1529645154}, 'id': 5955902, 'name': 'Fort Nelson', 'cod': 200}
    'Processing Record 250 | pangnirtung, ca'
    {'coord': {'lon': -65.72, 'lat': 66.15}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 31.32, 'pressure': 995.11, 'humidity': 99, 'temp_min': 31.32, 'temp_max': 31.32, 'sea_level': 1013.76, 'grnd_level': 995.11}, 'wind': {'speed': 1.95, 'deg': 153.503}, 'clouds': {'all': 76}, 'dt': 1529554481, 'sys': {'message': 0.0074, 'country': 'CA', 'sunrise': 0, 'sunset': 0}, 'id': 6096551, 'name': 'Pangnirtung', 'cod': 200}
    'Processing Record 251 | clovis, us'
    {'coord': {'lon': -119.7, 'lat': 36.83}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 83.88, 'pressure': 1012, 'humidity': 33, 'temp_min': 82.4, 'temp_max': 86}, 'visibility': 16093, 'wind': {'speed': 13.87, 'deg': 300}, 'clouds': {'all': 20}, 'dt': 1529553360, 'sys': {'type': 1, 'id': 387, 'message': 0.0037, 'country': 'US', 'sunrise': 1529584803, 'sunset': 1529637680}, 'id': 5338122, 'name': 'Clovis', 'cod': 200}
    'Processing Record 252 | noumea, nc'
    {'coord': {'lon': 166.46, 'lat': -22.28}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 73.4, 'pressure': 1016, 'humidity': 53, 'temp_min': 73.4, 'temp_max': 73.4}, 'visibility': 10000, 'wind': {'speed': 9.17, 'deg': 250}, 'clouds': {'all': 75}, 'dt': 1529553600, 'sys': {'type': 1, 'id': 8344, 'message': 0.0041, 'country': 'NC', 'sunrise': 1529523166, 'sunset': 1529561940}, 'id': 2139521, 'name': 'Noumea', 'cod': 200}
    'Processing Record 253 | tura, ru'
    {'coord': {'lon': 100.22, 'lat': 64.27}, 'weather': [{'id': 501, 'main': 'Rain', 'description': 'moderate rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 60.93, 'pressure': 965.12, 'humidity': 100, 'temp_min': 60.93, 'temp_max': 60.93, 'sea_level': 1012.82, 'grnd_level': 965.12}, 'wind': {'speed': 2.84, 'deg': 243.503}, 'rain': {'3h': 3.625}, 'clouds': {'all': 88}, 'dt': 1529554520, 'sys': {'message': 0.0029, 'country': 'RU', 'sunrise': 1529520196, 'sunset': 1529596710}, 'id': 2014833, 'name': 'Tura', 'cod': 200}
    'Processing Record 254 | gombong, id'
    {'coord': {'lon': 109.31, 'lat': -7.19}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'base': 'stations', 'main': {'temp': 81.09, 'pressure': 983.12, 'humidity': 75, 'temp_min': 81.09, 'temp_max': 81.09, 'sea_level': 1025.79, 'grnd_level': 983.12}, 'wind': {'speed': 3.18, 'deg': 174.503}, 'clouds': {'all': 36}, 'dt': 1529554578, 'sys': {'message': 0.0197, 'country': 'ID', 'sunrise': 1529535200, 'sunset': 1529577342}, 'id': 1649595, 'name': 'Gombong', 'cod': 200}
    'Processing Record 255 | lompoc, us'
    {'coord': {'lon': -120.46, 'lat': 34.64}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 57.24, 'pressure': 1015, 'humidity': 87, 'temp_min': 53.6, 'temp_max': 62.6}, 'visibility': 16093, 'wind': {'speed': 10.29, 'deg': 350}, 'clouds': {'all': 90}, 'dt': 1529553480, 'sys': {'type': 1, 'id': 507, 'message': 0.0045, 'country': 'US', 'sunrise': 1529585359, 'sunset': 1529637488}, 'id': 5367788, 'name': 'Lompoc', 'cod': 200}
    'Processing Record 256 | ondangwa, na'
    {'coord': {'lon': 15.98, 'lat': -17.91}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 47.52, 'pressure': 909.35, 'humidity': 47, 'temp_min': 47.52, 'temp_max': 47.52, 'sea_level': 1034.51, 'grnd_level': 909.35}, 'wind': {'speed': 8.1, 'deg': 107.003}, 'clouds': {'all': 0}, 'dt': 1529554578, 'sys': {'message': 0.0035, 'country': 'NA', 'sunrise': 1529558772, 'sunset': 1529598575}, 'id': 3354247, 'name': 'Ondangwa', 'cod': 200}
    'Processing Record 257 | lexington, us'
    {'coord': {'lon': -84.5, 'lat': 38.05}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 74.05, 'pressure': 1013, 'humidity': 83, 'temp_min': 73.4, 'temp_max': 75.2}, 'visibility': 16093, 'wind': {'speed': 4.7, 'deg': 230}, 'clouds': {'all': 1}, 'dt': 1529552100, 'sys': {'type': 1, 'id': 1129, 'message': 0.0043, 'country': 'US', 'sunrise': 1529576133, 'sunset': 1529629451}, 'id': 4297983, 'name': 'Lexington', 'cod': 200}
    'Processing Record 258 | helong, cn'
    {'coord': {'lon': 116.13, 'lat': 25.94}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 80.46, 'pressure': 963.34, 'humidity': 88, 'temp_min': 80.46, 'temp_max': 80.46, 'sea_level': 1019.39, 'grnd_level': 963.34}, 'wind': {'speed': 4.41, 'deg': 208.503}, 'clouds': {'all': 92}, 'dt': 1529554578, 'sys': {'message': 0.0038, 'country': 'CN', 'sunrise': 1529529860, 'sunset': 1529579407}, 'id': 1808534, 'name': 'Helong', 'cod': 200}
    'Processing Record 259 | victor harbor, au'
    {'coord': {'lon': 138.62, 'lat': -35.55}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 57.2, 'pressure': 1028, 'humidity': 54, 'temp_min': 57.2, 'temp_max': 57.2}, 'visibility': 10000, 'wind': {'speed': 8.05, 'deg': 300}, 'clouds': {'all': 0}, 'dt': 1529551800, 'sys': {'type': 1, 'id': 8204, 'message': 0.0041, 'country': 'AU', 'sunrise': 1529531683, 'sunset': 1529566788}, 'id': 2059470, 'name': 'Victor Harbor', 'cod': 200}
    'Processing Record 260 | andenes, no'
    {'coord': {'lon': 16.12, 'lat': 69.31}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 48.2, 'pressure': 1000, 'humidity': 93, 'temp_min': 48.2, 'temp_max': 48.2}, 'visibility': 10000, 'wind': {'speed': 6.93, 'deg': 290}, 'clouds': {'all': 75}, 'dt': 1529553000, 'sys': {'type': 1, 'id': 5272, 'message': 0.0052, 'country': 'NO', 'sunrise': 0, 'sunset': 0}, 'id': 3163146, 'name': 'Andenes', 'cod': 200}
    'Processing Record 261 | olafsvik, is'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for olafsvik, is**
    'Processing Record 262 | teknaf, bd'
    {'coord': {'lon': 92.31, 'lat': 20.86}, 'weather': [{'id': 501, 'main': 'Rain', 'description': 'moderate rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 77.49, 'pressure': 1009.22, 'humidity': 100, 'temp_min': 77.49, 'temp_max': 77.49, 'sea_level': 1017.81, 'grnd_level': 1009.22}, 'wind': {'speed': 3.74, 'deg': 154.003}, 'rain': {'3h': 5.835}, 'clouds': {'all': 92}, 'dt': 1529554820, 'sys': {'message': 0.0043, 'country': 'BD', 'sunrise': 1529536229, 'sunset': 1529584474}, 'id': 1185095, 'name': 'Teknaf', 'cod': 200}
    'Processing Record 263 | moerai, pf'
    {'coord': {'lon': -151.33, 'lat': -22.43}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 74.97, 'pressure': 1032.08, 'humidity': 100, 'temp_min': 74.97, 'temp_max': 74.97, 'sea_level': 1032.12, 'grnd_level': 1032.08}, 'wind': {'speed': 4.74, 'deg': 120.003}, 'clouds': {'all': 12}, 'dt': 1529554579, 'sys': {'message': 0.0036, 'country': 'PF', 'sunrise': 1529599466, 'sunset': 1529638203}, 'id': 4034188, 'name': 'Moerai', 'cod': 200}
    'Processing Record 264 | misratah, ly'
    {'coord': {'lon': 15.09, 'lat': 32.38}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 68.31, 'pressure': 1027.54, 'humidity': 98, 'temp_min': 68.31, 'temp_max': 68.31, 'sea_level': 1030.5, 'grnd_level': 1027.54}, 'wind': {'speed': 4.85, 'deg': 70.5034}, 'clouds': {'all': 0}, 'dt': 1529554514, 'sys': {'message': 0.0031, 'country': 'LY', 'sunrise': 1529553185, 'sunset': 1529604589}, 'id': 2214846, 'name': 'Misratah', 'cod': 200}
    'Processing Record 265 | nioro, ml'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for nioro, ml**
    'Processing Record 266 | lieksa, fi'
    {'coord': {'lon': 30.02, 'lat': 63.32}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 'base': 'stations', 'main': {'temp': 51.75, 'pressure': 995.03, 'humidity': 67, 'temp_min': 51.75, 'temp_max': 51.75, 'sea_level': 1015.26, 'grnd_level': 995.03}, 'wind': {'speed': 5.41, 'deg': 256.503}, 'clouds': {'all': 20}, 'dt': 1529554579, 'sys': {'message': 0.004, 'country': 'FI', 'sunrise': 1529538366, 'sunset': 1529612239}, 'id': 648090, 'name': 'Lieksa', 'cod': 200}
    'Processing Record 267 | requena, pe'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for requena, pe**
    'Processing Record 268 | lebyazhye, ru'
    {'coord': {'lon': 29.42, 'lat': 59.96}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 55.4, 'pressure': 1007, 'humidity': 66, 'temp_min': 55.4, 'temp_max': 55.4}, 'visibility': 10000, 'wind': {'speed': 6.71, 'deg': 260}, 'clouds': {'all': 0}, 'dt': 1529551800, 'sys': {'type': 1, 'id': 7267, 'message': 0.0041, 'country': 'RU', 'sunrise': 1529541513, 'sunset': 1529609381}, 'id': 536466, 'name': 'Lebyazhye', 'cod': 200}
    'Processing Record 269 | tezu, in'
    {'coord': {'lon': 96.16, 'lat': 27.93}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 'base': 'stations', 'main': {'temp': 75.96, 'pressure': 875.47, 'humidity': 85, 'temp_min': 75.96, 'temp_max': 75.96, 'sea_level': 1016.39, 'grnd_level': 875.47}, 'wind': {'speed': 0.6, 'deg': 243.003}, 'clouds': {'all': 20}, 'dt': 1529554820, 'sys': {'message': 0.0164, 'country': 'IN', 'sunrise': 1529534381, 'sunset': 1529584474}, 'id': 1254709, 'name': 'Tezu', 'cod': 200}
    'Processing Record 270 | sabang, id'
    {'coord': {'lon': 120.82, 'lat': 1.17}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 82.44, 'pressure': 1017.89, 'humidity': 100, 'temp_min': 82.44, 'temp_max': 82.44, 'sea_level': 1025.06, 'grnd_level': 1017.89}, 'wind': {'speed': 3.4, 'deg': 291.503}, 'clouds': {'all': 0}, 'dt': 1529554500, 'sys': {'message': 0.0031, 'country': 'ID', 'sunrise': 1529531565, 'sunset': 1529575451}, 'id': 1623502, 'name': 'Sabang', 'cod': 200}
    'Processing Record 271 | kahului, us'
    {'coord': {'lon': -156.47, 'lat': 20.89}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'base': 'stations', 'main': {'temp': 78.67, 'pressure': 1014, 'humidity': 65, 'temp_min': 73.4, 'temp_max': 82.4}, 'visibility': 16093, 'wind': {'speed': 16.11, 'deg': 60, 'gust': 11.8}, 'clouds': {'all': 40}, 'dt': 1529553360, 'sys': {'type': 1, 'id': 823, 'message': 0.004, 'country': 'US', 'sunrise': 1529595942, 'sunset': 1529644193}, 'id': 5847411, 'name': 'Kahului', 'cod': 200}
    'Processing Record 272 | mawlaik, mm'
    {'coord': {'lon': 94.42, 'lat': 23.63}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 80.64, 'pressure': 974.12, 'humidity': 93, 'temp_min': 80.64, 'temp_max': 80.64, 'sea_level': 1016.76, 'grnd_level': 974.12}, 'wind': {'speed': 2.73, 'deg': 110.503}, 'rain': {'3h': 0.165}, 'clouds': {'all': 80}, 'dt': 1529554580, 'sys': {'message': 0.0047, 'country': 'MM', 'sunrise': 1529535375, 'sunset': 1529584315}, 'id': 1310120, 'name': 'Mawlaik', 'cod': 200}
    'Processing Record 273 | kizukuri, jp'
    {'coord': {'lon': 140.39, 'lat': 40.81}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 68.74, 'pressure': 1000, 'humidity': 100, 'temp_min': 68, 'temp_max': 69.8}, 'visibility': 10000, 'wind': {'speed': 8.05, 'deg': 210}, 'clouds': {'all': 75}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 7591, 'message': 0.0041, 'country': 'JP', 'sunrise': 1529521619, 'sunset': 1529576002}, 'id': 2129513, 'name': 'Kizukuri', 'cod': 200}
    'Processing Record 274 | dragu, ro'
    {'coord': {'lon': 23.4, 'lat': 47.04}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 65.39, 'pressure': 1019, 'humidity': 82, 'temp_min': 64.4, 'temp_max': 66.2}, 'visibility': 10000, 'wind': {'speed': 1.12}, 'clouds': {'all': 0}, 'dt': 1529551800, 'sys': {'type': 1, 'id': 5988, 'message': 0.0038, 'country': 'RO', 'sunrise': 1529548266, 'sunset': 1529605518}, 'id': 678894, 'name': 'Dragu', 'cod': 200}
    'Processing Record 275 | nizhneyansk, ru'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for nizhneyansk, ru**
    'Processing Record 276 | ginda, er'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for ginda, er**
    'Processing Record 277 | touros, br'
    {'coord': {'lon': -35.46, 'lat': -5.2}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10n'}], 'base': 'stations', 'main': {'temp': 76.41, 'pressure': 1025.27, 'humidity': 82, 'temp_min': 76.41, 'temp_max': 76.41, 'sea_level': 1029.48, 'grnd_level': 1025.27}, 'wind': {'speed': 15.14, 'deg': 154.003}, 'rain': {'3h': 0.385}, 'clouds': {'all': 68}, 'dt': 1529554581, 'sys': {'message': 0.0038, 'country': 'BR', 'sunrise': 1529569742, 'sunset': 1529612301}, 'id': 3386213, 'name': 'Touros', 'cod': 200}
    'Processing Record 278 | bethel, us'
    {'coord': {'lon': -161.76, 'lat': 60.79}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 59, 'pressure': 1007, 'humidity': 62, 'temp_min': 59, 'temp_max': 59}, 'visibility': 16093, 'wind': {'speed': 6.93, 'deg': 240}, 'clouds': {'all': 90}, 'dt': 1529553180, 'sys': {'type': 1, 'id': 28, 'message': 0.004, 'country': 'US', 'sunrise': 1529586802, 'sunset': 1529655870}, 'id': 5880568, 'name': 'Bethel', 'cod': 200}
    'Processing Record 279 | los llanos de aridane, es'
    {'coord': {'lon': -17.92, 'lat': 28.66}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 68, 'pressure': 1019, 'humidity': 77, 'temp_min': 68, 'temp_max': 68}, 'visibility': 10000, 'wind': {'speed': 11.41, 'deg': 40}, 'clouds': {'all': 56}, 'dt': 1529553600, 'sys': {'type': 1, 'id': 5515, 'message': 0.0036, 'country': 'ES', 'sunrise': 1529561662, 'sunset': 1529611960}, 'id': 2514651, 'name': 'Los Llanos de Aridane', 'cod': 200}
    'Processing Record 280 | kankaanpaa, fi'
    {'coord': {'lon': 22.42, 'lat': 61.8}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 53.6, 'pressure': 1004, 'humidity': 76, 'temp_min': 53.6, 'temp_max': 53.6}, 'visibility': 10000, 'wind': {'speed': 3.36, 'deg': 120}, 'clouds': {'all': 0}, 'dt': 1529553000, 'sys': {'type': 1, 'id': 5038, 'message': 0.004, 'country': 'FI', 'sunrise': 1529541759, 'sunset': 1529612495}, 'id': 654363, 'name': 'Kankaanpaa', 'cod': 200}
    'Processing Record 281 | baykit, ru'
    {'coord': {'lon': 96.39, 'lat': 61.68}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 66.24, 'pressure': 956.21, 'humidity': 79, 'temp_min': 66.24, 'temp_max': 66.24, 'sea_level': 1014.81, 'grnd_level': 956.21}, 'wind': {'speed': 3.85, 'deg': 234.503}, 'rain': {'3h': 0.215}, 'clouds': {'all': 56}, 'dt': 1529554821, 'sys': {'message': 0.0032, 'country': 'RU', 'sunrise': 1529524110, 'sunset': 1529594634}, 'id': 1510689, 'name': 'Baykit', 'cod': 200}
    'Processing Record 282 | puerto lopez, co'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for puerto lopez, co**
    'Processing Record 283 | sampit, id'
    {'coord': {'lon': 112.95, 'lat': -2.54}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'base': 'stations', 'main': {'temp': 83.34, 'pressure': 1016.27, 'humidity': 84, 'temp_min': 83.34, 'temp_max': 83.34, 'sea_level': 1025.06, 'grnd_level': 1016.27}, 'wind': {'speed': 6.42, 'deg': 91.0034}, 'clouds': {'all': 48}, 'dt': 1529554582, 'sys': {'message': 0.004, 'country': 'ID', 'sunrise': 1529533840, 'sunset': 1529576954}, 'id': 1628884, 'name': 'Sampit', 'cod': 200}
    'Processing Record 284 | leningradskiy, ru'
    {'coord': {'lon': 178.42, 'lat': 69.38}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '02d'}], 'base': 'stations', 'main': {'temp': 32.4, 'pressure': 1029.81, 'humidity': 98, 'temp_min': 32.4, 'temp_max': 32.4, 'sea_level': 1032.56, 'grnd_level': 1029.81}, 'wind': {'speed': 16.49, 'deg': 116.503}, 'clouds': {'all': 8}, 'dt': 1529554582, 'sys': {'message': 0.0038, 'country': 'RU', 'sunrise': 0, 'sunset': 0}, 'id': 2123814, 'name': 'Leningradskiy', 'cod': 200}
    'Processing Record 285 | beloha, mg'
    {'coord': {'lon': 45.06, 'lat': -25.17}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 54.36, 'pressure': 1019.92, 'humidity': 80, 'temp_min': 54.36, 'temp_max': 54.36, 'sea_level': 1036.74, 'grnd_level': 1019.92}, 'wind': {'speed': 2.73, 'deg': 131.003}, 'clouds': {'all': 0}, 'dt': 1529554822, 'sys': {'message': 0.0037, 'country': 'MG', 'sunrise': 1529552666, 'sunset': 1529590721}, 'id': 1067565, 'name': 'Beloha', 'cod': 200}
    'Processing Record 286 | bandarbeyla, so'
    {'coord': {'lon': 50.81, 'lat': 9.49}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 77.76, 'pressure': 1016.67, 'humidity': 81, 'temp_min': 77.76, 'temp_max': 77.76, 'sea_level': 1021.66, 'grnd_level': 1016.67}, 'wind': {'speed': 29.01, 'deg': 203.503}, 'clouds': {'all': 0}, 'dt': 1529554582, 'sys': {'message': 0.0031, 'country': 'SO', 'sunrise': 1529547491, 'sunset': 1529593135}, 'id': 64814, 'name': 'Bandarbeyla', 'cod': 200}
    'Processing Record 287 | diplo, pk'
    {'coord': {'lon': 69.59, 'lat': 24.47}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 84.24, 'pressure': 1010.84, 'humidity': 76, 'temp_min': 84.24, 'temp_max': 84.24, 'sea_level': 1014.32, 'grnd_level': 1010.84}, 'wind': {'speed': 12.57, 'deg': 236.003}, 'clouds': {'all': 64}, 'dt': 1529554582, 'sys': {'message': 0.0039, 'country': 'PK', 'sunrise': 1529541226, 'sunset': 1529590384}, 'id': 1179758, 'name': 'Diplo', 'cod': 200}
    'Processing Record 288 | koundara, gn'
    {'coord': {'lon': -13.3, 'lat': 12.49}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 78.21, 'pressure': 1018.13, 'humidity': 74, 'temp_min': 78.21, 'temp_max': 78.21, 'sea_level': 1027.62, 'grnd_level': 1018.13}, 'wind': {'speed': 12.46, 'deg': 237.003}, 'clouds': {'all': 24}, 'dt': 1529554583, 'sys': {'message': 0.0034, 'country': 'GN', 'sunrise': 1529562552, 'sunset': 1529608852}, 'id': 2418596, 'name': 'Koundara', 'cod': 200}
    'Processing Record 289 | marzuq, ly'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for marzuq, ly**
    'Processing Record 290 | voh, nc'
    {'coord': {'lon': 164.69, 'lat': -20.95}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 70.92, 'pressure': 1023.65, 'humidity': 100, 'temp_min': 70.92, 'temp_max': 70.92, 'sea_level': 1029.97, 'grnd_level': 1023.65}, 'wind': {'speed': 11.68, 'deg': 179.503}, 'clouds': {'all': 64}, 'dt': 1529554583, 'sys': {'message': 0.003, 'country': 'NC', 'sunrise': 1529523431, 'sunset': 1529562524}, 'id': 2137748, 'name': 'Voh', 'cod': 200}
    'Processing Record 291 | yelizovo, ru'
    {'coord': {'lon': 158.38, 'lat': 53.19}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 68, 'pressure': 1015, 'humidity': 49, 'temp_min': 68, 'temp_max': 68}, 'visibility': 10000, 'wind': {'speed': 15.66, 'deg': 160}, 'clouds': {'all': 56}, 'dt': 1529551800, 'sys': {'type': 1, 'id': 7248, 'message': 0.0047, 'country': 'RU', 'sunrise': 1529513942, 'sunset': 1529575043}, 'id': 2119538, 'name': 'Yelizovo', 'cod': 200}
    'Processing Record 292 | dingle, ie'
    {'coord': {'lon': -10.27, 'lat': 52.14}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 54.99, 'pressure': 1037.18, 'humidity': 100, 'temp_min': 54.99, 'temp_max': 54.99, 'sea_level': 1043.63, 'grnd_level': 1037.18}, 'wind': {'speed': 14.47, 'deg': 343.003}, 'clouds': {'all': 80}, 'dt': 1529554822, 'sys': {'message': 0.0034, 'country': 'IE', 'sunrise': 1529554804, 'sunset': 1529615145}, 'id': 2964782, 'name': 'Dingle', 'cod': 200}
    'Processing Record 293 | faya, td'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for faya, td**
    'Processing Record 294 | georgetown, us'
    {'coord': {'lon': -79.29, 'lat': 33.38}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 77.11, 'pressure': 1012, 'humidity': 100, 'temp_min': 73.4, 'temp_max': 80.6}, 'visibility': 16093, 'wind': {'speed': 5.53, 'deg': 214.003}, 'clouds': {'all': 1}, 'dt': 1529553300, 'sys': {'type': 1, 'id': 2414, 'message': 0.0119, 'country': 'US', 'sunrise': 1529575682, 'sunset': 1529627401}, 'id': 4579662, 'name': 'Georgetown', 'cod': 200}
    'Processing Record 295 | adrar, dz'
    {'coord': {'lon': -0.29, 'lat': 27.87}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 84.2, 'pressure': 1010, 'humidity': 13, 'temp_min': 84.2, 'temp_max': 84.2}, 'visibility': 10000, 'wind': {'speed': 14.99, 'deg': 90}, 'clouds': {'all': 0}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 6220, 'message': 0.0032, 'country': 'DZ', 'sunrise': 1529557541, 'sunset': 1529607617}, 'id': 2508813, 'name': 'Adrar', 'cod': 200}
    'Processing Record 296 | yako, bf'
    {'coord': {'lon': -2.26, 'lat': 12.96}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 82.17, 'pressure': 986.36, 'humidity': 54, 'temp_min': 82.17, 'temp_max': 82.17, 'sea_level': 1021.98, 'grnd_level': 986.36}, 'wind': {'speed': 13.47, 'deg': 219.503}, 'clouds': {'all': 0}, 'dt': 1529554584, 'sys': {'message': 0.0035, 'country': 'BF', 'sunrise': 1529559849, 'sunset': 1529606254}, 'id': 2353688, 'name': 'Yako', 'cod': 200}
    'Processing Record 297 | myski, ru'
    {'coord': {'lon': 87.8, 'lat': 53.71}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '02d'}], 'base': 'stations', 'main': {'temp': 68.76, 'pressure': 983.68, 'humidity': 69, 'temp_min': 68.76, 'temp_max': 68.76, 'sea_level': 1021.54, 'grnd_level': 983.68}, 'wind': {'speed': 5.75, 'deg': 229.003}, 'clouds': {'all': 8}, 'dt': 1529554584, 'sys': {'message': 0.0034, 'country': 'RU', 'sunrise': 1529530685, 'sunset': 1529592183}, 'id': 1498129, 'name': 'Myski', 'cod': 200}
    'Processing Record 298 | chokurdakh, ru'
    {'coord': {'lon': 147.9, 'lat': 70.62}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 53.37, 'pressure': 1022.59, 'humidity': 86, 'temp_min': 53.37, 'temp_max': 53.37, 'sea_level': 1024.7, 'grnd_level': 1022.59}, 'wind': {'speed': 10.67, 'deg': 98.5034}, 'clouds': {'all': 0}, 'dt': 1529554495, 'sys': {'message': 0.0041, 'country': 'RU', 'sunrise': 0, 'sunset': 0}, 'id': 2126123, 'name': 'Chokurdakh', 'cod': 200}
    'Processing Record 299 | alta floresta, br'
    {'coord': {'lon': -56.08, 'lat': -9.87}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 77.76, 'pressure': 1003.14, 'humidity': 66, 'temp_min': 77.76, 'temp_max': 77.76, 'sea_level': 1029.08, 'grnd_level': 1003.14}, 'wind': {'speed': 4.29, 'deg': 111.503}, 'clouds': {'all': 24}, 'dt': 1529554585, 'sys': {'message': 0.007, 'country': 'BR', 'sunrise': 1529575184, 'sunset': 1529616757}, 'id': 6316343, 'name': 'Alta Floresta', 'cod': 200}
    'Processing Record 300 | narsaq, gl'
    {'coord': {'lon': -46.05, 'lat': 60.91}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10n'}], 'base': 'stations', 'main': {'temp': 51.8, 'pressure': 997, 'humidity': 37, 'temp_min': 51.8, 'temp_max': 51.8}, 'visibility': 10000, 'wind': {'speed': 6.93}, 'clouds': {'all': 75}, 'dt': 1529553000, 'sys': {'type': 1, 'id': 4791, 'message': 0.004, 'country': 'GL', 'sunrise': 1529558935, 'sunset': 1529628189}, 'id': 3421719, 'name': 'Narsaq', 'cod': 200}
    'Processing Record 301 | halalo, wf'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for halalo, wf**
    'Processing Record 302 | mezen, ru'
    {'coord': {'lon': 44.24, 'lat': 65.85}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 57.06, 'pressure': 998.92, 'humidity': 100, 'temp_min': 57.06, 'temp_max': 57.06, 'sea_level': 1003.86, 'grnd_level': 998.92}, 'wind': {'speed': 3.4, 'deg': 307.503}, 'rain': {'3h': 0.46}, 'clouds': {'all': 80}, 'dt': 1529554585, 'sys': {'message': 0.0032, 'country': 'RU', 'sunrise': 0, 'sunset': 0}, 'id': 527321, 'name': 'Mezen', 'cod': 200}
    'Processing Record 303 | bay city, us'
    {'coord': {'lon': -83.89, 'lat': 43.59}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 59.95, 'pressure': 1012, 'humidity': 77, 'temp_min': 53.6, 'temp_max': 64.4}, 'visibility': 16093, 'wind': {'speed': 2.84, 'deg': 79.0034}, 'clouds': {'all': 1}, 'dt': 1529552160, 'sys': {'type': 1, 'id': 1451, 'message': 0.0044, 'country': 'US', 'sunrise': 1529574861, 'sunset': 1529630431}, 'id': 4985180, 'name': 'Bay City', 'cod': 200}
    'Processing Record 304 | sitka, us'
    {'coord': {'lon': -99.65, 'lat': 37.17}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 75.42, 'pressure': 954.1, 'humidity': 58, 'temp_min': 75.42, 'temp_max': 75.42, 'sea_level': 1025.51, 'grnd_level': 954.1}, 'wind': {'speed': 9.78, 'deg': 356.503}, 'clouds': {'all': 0}, 'dt': 1529554585, 'sys': {'message': 0.0031, 'country': 'US', 'sunrise': 1529579929, 'sunset': 1529632928}, 'id': 4267710, 'name': 'Sitka', 'cod': 200}
    'Processing Record 305 | trelew, ar'
    {'coord': {'lon': -65.31, 'lat': -43.25}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 48.87, 'pressure': 1002.81, 'humidity': 42, 'temp_min': 48.87, 'temp_max': 48.87, 'sea_level': 1014.04, 'grnd_level': 1002.81}, 'wind': {'speed': 21.52, 'deg': 258.003}, 'clouds': {'all': 0}, 'dt': 1529554823, 'sys': {'message': 0.0033, 'country': 'AR', 'sunrise': 1529582033, 'sunset': 1529614339}, 'id': 3833883, 'name': 'Trelew', 'cod': 200}
    'Processing Record 306 | dzilam gonzalez, mx'
    {'coord': {'lon': -88.93, 'lat': 21.28}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 85.5, 'pressure': 1022.19, 'humidity': 50, 'temp_min': 85.5, 'temp_max': 85.5, 'sea_level': 1024.58, 'grnd_level': 1022.19}, 'wind': {'speed': 8.77, 'deg': 131.003}, 'clouds': {'all': 0}, 'dt': 1529554585, 'sys': {'message': 0.0031, 'country': 'MX', 'sunrise': 1529579682, 'sunset': 1529628030}, 'id': 3529654, 'name': 'Dzilam Gonzalez', 'cod': 200}
    'Processing Record 307 | prince george, ca'
    {'coord': {'lon': -122.75, 'lat': 53.92}, 'weather': [{'id': 211, 'main': 'Thunderstorm', 'description': 'thunderstorm', 'icon': '11n'}], 'base': 'stations', 'main': {'temp': 78.8, 'pressure': 1012, 'humidity': 39, 'temp_min': 78.8, 'temp_max': 78.8}, 'visibility': 14484, 'wind': {'speed': 25.28, 'deg': 190, 'gust': 14.9}, 'clouds': {'all': 75}, 'dt': 1529552640, 'sys': {'type': 1, 'id': 3324, 'message': 0.0032, 'country': 'CA', 'sunrise': 1529581142, 'sunset': 1529642804}, 'id': 6113365, 'name': 'Prince George', 'cod': 200}
    'Processing Record 308 | bara, sd'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for bara, sd**
    'Processing Record 309 | carnarvon, au'
    {'coord': {'lon': 113.63, 'lat': -24.87}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 63.09, 'pressure': 1037.02, 'humidity': 100, 'temp_min': 63.09, 'temp_max': 63.09, 'sea_level': 1038.36, 'grnd_level': 1037.02}, 'wind': {'speed': 10.22, 'deg': 105.003}, 'clouds': {'all': 0}, 'dt': 1529554749, 'sys': {'message': 0.003, 'country': 'AU', 'sunrise': 1529536168, 'sunset': 1529574300}, 'id': 2074865, 'name': 'Carnarvon', 'cod': 200}
    'Processing Record 310 | usinsk, ru'
    {'coord': {'lon': 57.56, 'lat': 66}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 58.86, 'pressure': 994.22, 'humidity': 76, 'temp_min': 58.86, 'temp_max': 58.86, 'sea_level': 1003.01, 'grnd_level': 994.22}, 'wind': {'speed': 7.65, 'deg': 58.0034}, 'clouds': {'all': 0}, 'dt': 1529554586, 'sys': {'message': 0.0034, 'country': 'RU', 'sunrise': 0, 'sunset': 0}, 'id': 863061, 'name': 'Usinsk', 'cod': 200}
    'Processing Record 311 | riyadh, sa'
    {'coord': {'lon': 46.72, 'lat': 24.63}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 86, 'pressure': 1010, 'humidity': 16, 'temp_min': 86, 'temp_max': 86}, 'visibility': 10000, 'wind': {'speed': 4.7, 'deg': 300}, 'clouds': {'all': 0}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 7001, 'message': 0.0033, 'country': 'SA', 'sunrise': 1529546695, 'sunset': 1529595895}, 'id': 108410, 'name': 'Riyadh', 'cod': 200}
    'Processing Record 312 | myanaung, mm'
    {'coord': {'lon': 95.32, 'lat': 18.28}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 78.03, 'pressure': 1015.78, 'humidity': 100, 'temp_min': 78.03, 'temp_max': 78.03, 'sea_level': 1019.51, 'grnd_level': 1015.78}, 'wind': {'speed': 7.76, 'deg': 203.003}, 'rain': {'3h': 0.91}, 'clouds': {'all': 88}, 'dt': 1529554586, 'sys': {'message': 0.0037, 'country': 'MM', 'sunrise': 1529535818, 'sunset': 1529583441}, 'id': 1308204, 'name': 'Myanaung', 'cod': 200}
    'Processing Record 313 | balkhash, kz'
    {'coord': {'lon': 74.98, 'lat': 46.84}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 'base': 'stations', 'main': {'temp': 74.88, 'pressure': 981.66, 'humidity': 77, 'temp_min': 74.88, 'temp_max': 74.88, 'sea_level': 1024.01, 'grnd_level': 981.66}, 'wind': {'speed': 5.64, 'deg': 216.503}, 'clouds': {'all': 20}, 'dt': 1529554824, 'sys': {'message': 0.0031, 'country': 'KZ', 'sunrise': 1529535938, 'sunset': 1529593085}, 'id': 1525798, 'name': 'Balkhash', 'cod': 200}
    'Processing Record 314 | swan river, ca'
    {'coord': {'lon': -101.27, 'lat': 52.11}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 80.19, 'pressure': 971.28, 'humidity': 28, 'temp_min': 80.19, 'temp_max': 80.19, 'sea_level': 1025.88, 'grnd_level': 971.28}, 'wind': {'speed': 6.53, 'deg': 257.503}, 'clouds': {'all': 8}, 'dt': 1529554587, 'sys': {'message': 0.0035, 'country': 'CA', 'sunrise': 1529576658, 'sunset': 1529636977}, 'id': 6160362, 'name': 'Swan River', 'cod': 200}
    'Processing Record 315 | mandalgovi, mn'
    {'coord': {'lon': 106.27, 'lat': 45.76}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 76.41, 'pressure': 865.58, 'humidity': 32, 'temp_min': 76.41, 'temp_max': 76.41, 'sea_level': 1015.58, 'grnd_level': 865.58}, 'wind': {'speed': 6.08, 'deg': 171.503}, 'clouds': {'all': 64}, 'dt': 1529554587, 'sys': {'message': 0.0042, 'country': 'MN', 'sunrise': 1529528702, 'sunset': 1529585299}, 'id': 2030065, 'name': 'Mandalgovi', 'cod': 200}
    'Processing Record 316 | clyde river, ca'
    {'coord': {'lon': -68.59, 'lat': 70.47}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 33.8, 'pressure': 1000, 'humidity': 92, 'temp_min': 33.8, 'temp_max': 33.8}, 'visibility': 14484, 'wind': {'speed': 10.29, 'deg': 110}, 'clouds': {'all': 90}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 3585, 'message': 0.0035, 'country': 'CA', 'sunrise': 0, 'sunset': 0}, 'id': 5924351, 'name': 'Clyde River', 'cod': 200}
    'Processing Record 317 | pisco, pe'
    {'coord': {'lon': -76.2, 'lat': -13.71}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 62.6, 'pressure': 1019, 'humidity': 82, 'temp_min': 62.6, 'temp_max': 62.6}, 'visibility': 8000, 'wind': {'speed': 3.36, 'deg': 220}, 'clouds': {'all': 90}, 'dt': 1529553600, 'sys': {'type': 1, 'id': 4405, 'message': 0.0039, 'country': 'PE', 'sunrise': 1529580429, 'sunset': 1529621172}, 'id': 3932145, 'name': 'Pisco', 'cod': 200}
    'Processing Record 318 | esperance, au'
    {'coord': {'lon': 121.89, 'lat': -33.86}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 61.74, 'pressure': 1029.32, 'humidity': 68, 'temp_min': 61.74, 'temp_max': 61.74, 'sea_level': 1041.36, 'grnd_level': 1029.32}, 'wind': {'speed': 7.43, 'deg': 297.503}, 'clouds': {'all': 0}, 'dt': 1529554587, 'sys': {'message': 0.0039, 'country': 'AU', 'sunrise': 1529535433, 'sunset': 1529571069}, 'id': 2071860, 'name': 'Esperance', 'cod': 200}
    'Processing Record 319 | port blair, in'
    {'coord': {'lon': 92.75, 'lat': 11.67}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 82.08, 'pressure': 1022.51, 'humidity': 100, 'temp_min': 82.08, 'temp_max': 82.08, 'sea_level': 1022.75, 'grnd_level': 1022.51}, 'wind': {'speed': 16.15, 'deg': 224.003}, 'rain': {'3h': 0.42}, 'clouds': {'all': 56}, 'dt': 1529554587, 'sys': {'message': 0.0033, 'country': 'IN', 'sunrise': 1529537186, 'sunset': 1529583306}, 'id': 1259385, 'name': 'Port Blair', 'cod': 200}
    'Processing Record 320 | sulangan, ph'
    {'coord': {'lon': 123.72, 'lat': 11.14}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 84.24, 'pressure': 1024.78, 'humidity': 100, 'temp_min': 84.24, 'temp_max': 84.24, 'sea_level': 1024.78, 'grnd_level': 1024.78}, 'wind': {'speed': 7.43, 'deg': 226.003}, 'rain': {'3h': 2.155}, 'clouds': {'all': 24}, 'dt': 1529554587, 'sys': {'message': 0.0042, 'country': 'PH', 'sunrise': 1529529810, 'sunset': 1529575814}, 'id': 1685422, 'name': 'Sulangan', 'cod': 200}
    'Processing Record 321 | kawalu, id'
    {'coord': {'lon': 108.21, 'lat': -7.38}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 74.34, 'pressure': 929.62, 'humidity': 84, 'temp_min': 74.34, 'temp_max': 74.34, 'sea_level': 1025.92, 'grnd_level': 929.62}, 'wind': {'speed': 2.39, 'deg': 140.003}, 'rain': {'3h': 0.28}, 'clouds': {'all': 80}, 'dt': 1529554500, 'sys': {'message': 0.0038, 'country': 'ID', 'sunrise': 1529535484, 'sunset': 1529577586}, 'id': 1640902, 'name': 'Kawalu', 'cod': 200}
    'Processing Record 322 | tumut, au'
    {'coord': {'lon': 148.22, 'lat': -35.3}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 'base': 'stations', 'main': {'temp': 52.02, 'pressure': 969.82, 'humidity': 72, 'temp_min': 52.02, 'temp_max': 52.02, 'sea_level': 1041.76, 'grnd_level': 969.82}, 'wind': {'speed': 2.39, 'deg': 286.003}, 'clouds': {'all': 24}, 'dt': 1529554588, 'sys': {'message': 0.0029, 'country': 'AU', 'sunrise': 1529529338, 'sunset': 1529564524}, 'id': 2145875, 'name': 'Tumut', 'cod': 200}
    'Processing Record 323 | ahipara, nz'
    {'coord': {'lon': 173.16, 'lat': -35.17}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 55.26, 'pressure': 1009.46, 'humidity': 100, 'temp_min': 55.26, 'temp_max': 55.26, 'sea_level': 1022.96, 'grnd_level': 1009.46}, 'wind': {'speed': 21.52, 'deg': 104.003}, 'rain': {'3h': 2.53}, 'clouds': {'all': 92}, 'dt': 1529554527, 'sys': {'message': 0.0038, 'country': 'NZ', 'sunrise': 1529523331, 'sunset': 1529558558}, 'id': 2194098, 'name': 'Ahipara', 'cod': 200}
    'Processing Record 324 | lata, sb'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for lata, sb**
    'Processing Record 325 | saint pete beach, us'
    {'coord': {'lon': -82.74, 'lat': 27.73}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 82.4, 'pressure': 1014, 'humidity': 74, 'temp_min': 80.6, 'temp_max': 84.2}, 'visibility': 16093, 'wind': {'speed': 8.99, 'deg': 267.503}, 'clouds': {'all': 75}, 'dt': 1529553360, 'sys': {'type': 1, 'id': 721, 'message': 0.0048, 'country': 'US', 'sunrise': 1529577352, 'sunset': 1529627388}, 'id': 4171522, 'name': 'Saint Pete Beach', 'cod': 200}
    'Processing Record 326 | shimanovsk, ru'
    {'coord': {'lon': 127.67, 'lat': 52}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '02d'}], 'base': 'stations', 'main': {'temp': 73.62, 'pressure': 980.04, 'humidity': 49, 'temp_min': 73.62, 'temp_max': 73.62, 'sea_level': 1013.27, 'grnd_level': 980.04}, 'wind': {'speed': 3.62, 'deg': 359.003}, 'clouds': {'all': 8}, 'dt': 1529554588, 'sys': {'message': 0.0043, 'country': 'RU', 'sunrise': 1529521742, 'sunset': 1529581986}, 'id': 2016701, 'name': 'Shimanovsk', 'cod': 200}
    'Processing Record 327 | skagastrond, is'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for skagastrond, is**
    'Processing Record 328 | namibe, ao'
    {'coord': {'lon': 12.15, 'lat': -15.19}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 67.95, 'pressure': 1025.67, 'humidity': 100, 'temp_min': 67.95, 'temp_max': 67.95, 'sea_level': 1029.64, 'grnd_level': 1025.67}, 'wind': {'speed': 4.52, 'deg': 150.503}, 'clouds': {'all': 0}, 'dt': 1529554588, 'sys': {'message': 0.0039, 'country': 'AO', 'sunrise': 1529559385, 'sunset': 1529599801}, 'id': 3347019, 'name': 'Namibe', 'cod': 200}
    'Processing Record 329 | mount gambier, au'
    {'coord': {'lon': 140.78, 'lat': -37.83}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 51.75, 'pressure': 1033.13, 'humidity': 98, 'temp_min': 51.75, 'temp_max': 51.75, 'sea_level': 1041.64, 'grnd_level': 1033.13}, 'wind': {'speed': 3.4, 'deg': 250.003}, 'rain': {'3h': 0.55}, 'clouds': {'all': 56}, 'dt': 1529554431, 'sys': {'message': 0.0032, 'country': 'AU', 'sunrise': 1529531543, 'sunset': 1529565891}, 'id': 2156643, 'name': 'Mount Gambier', 'cod': 200}
    'Processing Record 330 | dunedin, nz'
    {'coord': {'lon': 170.5, 'lat': -45.87}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 41.94, 'pressure': 994.87, 'humidity': 89, 'temp_min': 41.94, 'temp_max': 41.94, 'sea_level': 1036.17, 'grnd_level': 994.87}, 'wind': {'speed': 3.29, 'deg': 29.0034}, 'clouds': {'all': 0}, 'dt': 1529554589, 'sys': {'message': 0.0044, 'country': 'NZ', 'sunrise': 1529526003, 'sunset': 1529557163}, 'id': 2191562, 'name': 'Dunedin', 'cod': 200}
    'Processing Record 331 | male, mv'
    {'coord': {'lon': 73.51, 'lat': 4.17}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 84.2, 'pressure': 1011, 'humidity': 74, 'temp_min': 84.2, 'temp_max': 84.2}, 'visibility': 10000, 'wind': {'speed': 10.29, 'deg': 230}, 'clouds': {'all': 75}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 7915, 'message': 0.0037, 'country': 'MV', 'sunrise': 1529542608, 'sunset': 1529587121}, 'id': 1282027, 'name': 'Male', 'cod': 200}
    'Processing Record 332 | beruwala, lk'
    {'coord': {'lon': 79.98, 'lat': 6.48}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 79.29, 'pressure': 1022.19, 'humidity': 100, 'temp_min': 79.29, 'temp_max': 79.29, 'sea_level': 1023.77, 'grnd_level': 1022.19}, 'wind': {'speed': 14.03, 'deg': 264.503}, 'rain': {'3h': 1.965}, 'clouds': {'all': 80}, 'dt': 1529554589, 'sys': {'message': 0.003, 'country': 'LK', 'sunrise': 1529540811, 'sunset': 1529585812}, 'id': 1249931, 'name': 'Beruwala', 'cod': 200}
    'Processing Record 333 | enshi, cn'
    {'coord': {'lon': 109.48, 'lat': 30.29}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 69.57, 'pressure': 911.05, 'humidity': 100, 'temp_min': 69.57, 'temp_max': 69.57, 'sea_level': 1018.78, 'grnd_level': 911.05}, 'wind': {'speed': 3.62, 'deg': 87.0034}, 'rain': {'3h': 0.71}, 'clouds': {'all': 92}, 'dt': 1529554589, 'sys': {'message': 0.0067, 'country': 'CN', 'sunrise': 1529530845, 'sunset': 1529581616}, 'id': 1811720, 'name': 'Enshi', 'cod': 200}
    'Processing Record 334 | cherskiy, ru'
    {'coord': {'lon': 161.3, 'lat': 68.75}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 62.19, 'pressure': 1017.32, 'humidity': 50, 'temp_min': 62.19, 'temp_max': 62.19, 'sea_level': 1025.15, 'grnd_level': 1017.32}, 'wind': {'speed': 1.61, 'deg': 288.503}, 'clouds': {'all': 0}, 'dt': 1529554483, 'sys': {'message': 0.0032, 'country': 'RU', 'sunrise': 0, 'sunset': 0}, 'id': 2126199, 'name': 'Cherskiy', 'cod': 200}
    'Processing Record 335 | urulga, ru'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for urulga, ru**
    'Processing Record 336 | mach, pk'
    {'coord': {'lon': 67.33, 'lat': 29.87}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 73.71, 'pressure': 832.91, 'humidity': 34, 'temp_min': 73.71, 'temp_max': 73.71, 'sea_level': 1015.5, 'grnd_level': 832.91}, 'wind': {'speed': 3.18, 'deg': 77.0034}, 'clouds': {'all': 0}, 'dt': 1529554589, 'sys': {'message': 0.0035, 'country': 'PK', 'sunrise': 1529541024, 'sunset': 1529591671}, 'id': 1171757, 'name': 'Mach', 'cod': 200}
    'Processing Record 337 | lodja, cd'
    {'coord': {'lon': 23.6, 'lat': -3.52}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 72.36, 'pressure': 963.74, 'humidity': 78, 'temp_min': 72.36, 'temp_max': 72.36, 'sea_level': 1026.56, 'grnd_level': 963.74}, 'wind': {'speed': 3.85, 'deg': 15.0034}, 'clouds': {'all': 12}, 'dt': 1529554825, 'sys': {'message': 0.0031, 'country': 'CD', 'sunrise': 1529555390, 'sunset': 1529598299}, 'id': 211647, 'name': 'Lodja', 'cod': 200}
    'Processing Record 338 | urdzhar, kz'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for urdzhar, kz**
    'Processing Record 339 | abalak, ne'
    {'coord': {'lon': 6.28, 'lat': 15.46}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 79.74, 'pressure': 969.42, 'humidity': 63, 'temp_min': 79.74, 'temp_max': 79.74, 'sea_level': 1022.15, 'grnd_level': 969.42}, 'wind': {'speed': 14.92, 'deg': 213.503}, 'clouds': {'all': 0}, 'dt': 1529554590, 'sys': {'message': 0.0031, 'country': 'NE', 'sunrise': 1529557518, 'sunset': 1529604486}, 'id': 2448245, 'name': 'Abalak', 'cod': 200}
    'Processing Record 340 | havre, us'
    {'coord': {'lon': -109.68, 'lat': 48.55}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 69.8, 'pressure': 1017, 'humidity': 64, 'temp_min': 69.8, 'temp_max': 69.8}, 'visibility': 16093, 'wind': {'speed': 8.05, 'deg': 120}, 'clouds': {'all': 75}, 'dt': 1529549580, 'sys': {'type': 1, 'id': 1733, 'message': 0.0043, 'country': 'US', 'sunrise': 1529579797, 'sunset': 1529637875}, 'id': 5656497, 'name': 'Havre', 'cod': 200}
    'Processing Record 341 | bambanglipuro, id'
    {'coord': {'lon': 110.28, 'lat': -7.95}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 82.71, 'pressure': 995.76, 'humidity': 67, 'temp_min': 82.71, 'temp_max': 82.71, 'sea_level': 1026.08, 'grnd_level': 995.76}, 'wind': {'speed': 8.43, 'deg': 118.503}, 'clouds': {'all': 56}, 'dt': 1529554590, 'sys': {'message': 0.003, 'country': 'ID', 'sunrise': 1529535048, 'sunset': 1529577029}, 'id': 1650434, 'name': 'Bambanglipuro', 'cod': 200}
    'Processing Record 342 | flin flon, ca'
    {'coord': {'lon': -101.88, 'lat': 54.77}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 79.65, 'pressure': 986.28, 'humidity': 31, 'temp_min': 79.65, 'temp_max': 79.65, 'sea_level': 1022.11, 'grnd_level': 986.28}, 'wind': {'speed': 4.97, 'deg': 260.003}, 'clouds': {'all': 12}, 'dt': 1529554590, 'sys': {'message': 0.0034, 'country': 'CA', 'sunrise': 1529575787, 'sunset': 1529638140}, 'id': 5954718, 'name': 'Flin Flon', 'cod': 200}
    'Processing Record 343 | vao, nc'
    {'coord': {'lon': 167.48, 'lat': -22.67}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'base': 'stations', 'main': {'temp': 71.19, 'pressure': 1029.08, 'humidity': 100, 'temp_min': 71.19, 'temp_max': 71.19, 'sea_level': 1029.24, 'grnd_level': 1029.08}, 'wind': {'speed': 14.03, 'deg': 218.003}, 'clouds': {'all': 48}, 'dt': 1529554538, 'sys': {'message': 0.0035, 'country': 'NC', 'sunrise': 1529522969, 'sunset': 1529561647}, 'id': 2137773, 'name': 'Vao', 'cod': 200}
    'Processing Record 344 | half moon bay, us'
    {'coord': {'lon': -122.43, 'lat': 37.46}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 57.61, 'pressure': 1017, 'humidity': 87, 'temp_min': 55.4, 'temp_max': 60.8}, 'visibility': 16093, 'wind': {'speed': 12.75, 'deg': 320, 'gust': 7.7}, 'clouds': {'all': 90}, 'dt': 1529553360, 'sys': {'type': 1, 'id': 392, 'message': 0.0052, 'country': 'US', 'sunrise': 1529585345, 'sunset': 1529638448}, 'id': 5354943, 'name': 'Half Moon Bay', 'cod': 200}
    'Processing Record 345 | victoria, sc'
    {'coord': {'lon': 55.45, 'lat': -4.62}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'base': 'stations', 'main': {'temp': 78.8, 'pressure': 1013, 'humidity': 83, 'temp_min': 78.8, 'temp_max': 78.8}, 'visibility': 10000, 'wind': {'speed': 13.87, 'deg': 130}, 'clouds': {'all': 40}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 6865, 'message': 0.0032, 'country': 'SC', 'sunrise': 1529547859, 'sunset': 1529590539}, 'id': 241131, 'name': 'Victoria', 'cod': 200}
    'Processing Record 346 | peruibe, br'
    {'coord': {'lon': -47, 'lat': -24.32}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 69.57, 'pressure': 1034.1, 'humidity': 100, 'temp_min': 69.57, 'temp_max': 69.57, 'sea_level': 1034.26, 'grnd_level': 1034.1}, 'wind': {'speed': 8.21, 'deg': 21.0034}, 'clouds': {'all': 0}, 'dt': 1529554590, 'sys': {'message': 0.0033, 'country': 'BR', 'sunrise': 1529574656, 'sunset': 1529612926}, 'id': 3454061, 'name': 'Peruibe', 'cod': 200}
    'Processing Record 347 | kalemie, cd'
    {'coord': {'lon': 29.2, 'lat': -5.95}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 74.79, 'pressure': 933.02, 'humidity': 98, 'temp_min': 74.79, 'temp_max': 74.79, 'sea_level': 1027.25, 'grnd_level': 933.02}, 'wind': {'speed': 3.18, 'deg': 127.503}, 'clouds': {'all': 76}, 'dt': 1529554591, 'sys': {'message': 0.0028, 'country': 'CD', 'sunrise': 1529554299, 'sunset': 1529596701}, 'id': 214974, 'name': 'Kalemie', 'cod': 200}
    'Processing Record 348 | te anau, nz'
    {'coord': {'lon': 167.72, 'lat': -45.41}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 41.22, 'pressure': 969.17, 'humidity': 95, 'temp_min': 41.22, 'temp_max': 41.22, 'sea_level': 1035.72, 'grnd_level': 969.17}, 'wind': {'speed': 2.95, 'deg': 276.503}, 'clouds': {'all': 0}, 'dt': 1529554826, 'sys': {'message': 0.0042, 'country': 'NZ', 'sunrise': 1529526565, 'sunset': 1529557936}, 'id': 2181625, 'name': 'Te Anau', 'cod': 200}
    'Processing Record 349 | san jeronimo, mx'
    {'coord': {'lon': -110.79, 'lat': 29.37}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 87.8, 'pressure': 1011, 'humidity': 40, 'temp_min': 87.8, 'temp_max': 87.8}, 'visibility': 16093, 'wind': {'speed': 8.05, 'deg': 240}, 'clouds': {'all': 5}, 'dt': 1529552460, 'sys': {'type': 1, 'id': 3985, 'message': 0.0033, 'country': 'MX', 'sunrise': 1529583852, 'sunset': 1529634354}, 'id': 3982846, 'name': 'San Jeronimo', 'cod': 200}
    'Processing Record 350 | takanabe, jp'
    {'coord': {'lon': 131.49, 'lat': 32.13}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 75.2, 'pressure': 1006, 'humidity': 88, 'temp_min': 75.2, 'temp_max': 75.2}, 'visibility': 10000, 'wind': {'speed': 3.36, 'deg': 190}, 'clouds': {'all': 75}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 7549, 'message': 0.0039, 'country': 'JP', 'sunrise': 1529525284, 'sunset': 1529576610}, 'id': 1851068, 'name': 'Takanabe', 'cod': 200}
    'Processing Record 351 | hunza, pk'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for hunza, pk**
    'Processing Record 352 | ostrovnoy, ru'
    {'coord': {'lon': 39.51, 'lat': 68.05}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 44.19, 'pressure': 982.06, 'humidity': 100, 'temp_min': 44.19, 'temp_max': 44.19, 'sea_level': 1007.31, 'grnd_level': 982.06}, 'wind': {'speed': 8.66, 'deg': 41.5034}, 'clouds': {'all': 92}, 'dt': 1529554591, 'sys': {'message': 0.018, 'country': 'RU', 'sunrise': 0, 'sunset': 0}, 'id': 556268, 'name': 'Ostrovnoy', 'cod': 200}
    'Processing Record 353 | elko, us'
    {'coord': {'lon': -115.76, 'lat': 40.83}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 82.4, 'pressure': 1017, 'humidity': 17, 'temp_min': 82.4, 'temp_max': 82.4}, 'visibility': 16093, 'wind': {'speed': 3.36, 'deg': 320}, 'clouds': {'all': 1}, 'dt': 1529549760, 'sys': {'type': 1, 'id': 2053, 'message': 0.0038, 'country': 'US', 'sunrise': 1529583101, 'sunset': 1529637491}, 'id': 5703670, 'name': 'Elko', 'cod': 200}
    'Processing Record 354 | braganca, pt'
    {'coord': {'lon': -6.76, 'lat': 41.81}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 55.89, 'pressure': 918.11, 'humidity': 91, 'temp_min': 55.89, 'temp_max': 55.89, 'sea_level': 1032.2, 'grnd_level': 918.11}, 'wind': {'speed': 2.39, 'deg': 8.00342}, 'clouds': {'all': 0}, 'dt': 1529554592, 'sys': {'message': 0.0043, 'country': 'PT', 'sunrise': 1529556734, 'sunset': 1529611529}, 'id': 2742027, 'name': 'Braganca', 'cod': 200}
    'Processing Record 355 | cherdyn, ru'
    {'coord': {'lon': 56.48, 'lat': 60.4}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 51.39, 'pressure': 982.87, 'humidity': 95, 'temp_min': 51.39, 'temp_max': 51.39, 'sea_level': 1002.69, 'grnd_level': 982.87}, 'wind': {'speed': 9.66, 'deg': 263.503}, 'rain': {'3h': 0.415}, 'clouds': {'all': 92}, 'dt': 1529554592, 'sys': {'message': 0.0038, 'country': 'RU', 'sunrise': 1529534707, 'sunset': 1529603197}, 'id': 569359, 'name': 'Cherdyn', 'cod': 200}
    'Processing Record 356 | yumen, cn'
    {'coord': {'lon': 97.04, 'lat': 40.29}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 81.63, 'pressure': 844.02, 'humidity': 35, 'temp_min': 81.63, 'temp_max': 81.63, 'sea_level': 1015.74, 'grnd_level': 844.02}, 'wind': {'speed': 1.16, 'deg': 44.0034}, 'clouds': {'all': 0}, 'dt': 1529554592, 'sys': {'message': 0.0033, 'country': 'CN', 'sunrise': 1529532129, 'sunset': 1529586303}, 'id': 1528998, 'name': 'Yumen', 'cod': 200}
    'Processing Record 357 | vyshneve, ua'
    {'coord': {'lon': 30.37, 'lat': 50.39}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 64.4, 'pressure': 1018, 'humidity': 77, 'temp_min': 64.4, 'temp_max': 64.4}, 'visibility': 10000, 'wind': {'speed': 4.47, 'deg': 260}, 'clouds': {'all': 0}, 'dt': 1529551800, 'sys': {'type': 1, 'id': 7358, 'message': 0.0031, 'country': 'UA', 'sunrise': 1529545629, 'sunset': 1529604809}, 'id': 689487, 'name': 'Vyshneve', 'cod': 200}
    'Processing Record 358 | creel, mx'
    {'coord': {'lon': -107.63, 'lat': 27.75}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10n'}], 'base': 'stations', 'main': {'temp': 72.09, 'pressure': 786.55, 'humidity': 37, 'temp_min': 72.09, 'temp_max': 72.09, 'sea_level': 1021.3, 'grnd_level': 786.55}, 'wind': {'speed': 3.06, 'deg': 21.0034}, 'rain': {'3h': 0.185}, 'clouds': {'all': 76}, 'dt': 1529554593, 'sys': {'message': 0.0078, 'country': 'MX', 'sunrise': 1529583323, 'sunset': 1529633365}, 'id': 4012593, 'name': 'Creel', 'cod': 200}
    'Processing Record 359 | cururupu, br'
    {'coord': {'lon': -44.87, 'lat': -1.82}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'base': 'stations', 'main': {'temp': 71.46, 'pressure': 1028.02, 'humidity': 100, 'temp_min': 71.46, 'temp_max': 71.46, 'sea_level': 1029.08, 'grnd_level': 1028.02}, 'wind': {'speed': 3.06, 'deg': 146.003}, 'clouds': {'all': 48}, 'dt': 1529554593, 'sys': {'message': 0.0049, 'country': 'BR', 'sunrise': 1529571648, 'sunset': 1529614912}, 'id': 3401148, 'name': 'Cururupu', 'cod': 200}
    'Processing Record 360 | asau, tv'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for asau, tv**
    'Processing Record 361 | raga, sd'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for raga, sd**
    'Processing Record 362 | kegayli, uz'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for kegayli, uz**
    'Processing Record 363 | pundaguitan, ph'
    {'coord': {'lon': 126.17, 'lat': 6.37}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 83.16, 'pressure': 1020.16, 'humidity': 100, 'temp_min': 83.16, 'temp_max': 83.16, 'sea_level': 1025.31, 'grnd_level': 1020.16}, 'wind': {'speed': 1.61, 'deg': 215.003}, 'clouds': {'all': 0}, 'dt': 1529554593, 'sys': {'message': 0.0037, 'country': 'PH', 'sunrise': 1529529735, 'sunset': 1529574713}, 'id': 1698289, 'name': 'Pundaguitan', 'cod': 200}
    'Processing Record 364 | sao geraldo do araguaia, br'
    {'coord': {'lon': -48.55, 'lat': -6.4}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 69.66, 'pressure': 1006.54, 'humidity': 96, 'temp_min': 69.66, 'temp_max': 69.66, 'sea_level': 1028.79, 'grnd_level': 1006.54}, 'wind': {'speed': 3.18, 'deg': 0.00341797}, 'clouds': {'all': 12}, 'dt': 1529554594, 'sys': {'message': 0.0079, 'country': 'BR', 'sunrise': 1529573009, 'sunset': 1529615317}, 'id': 3388760, 'name': 'Sao Geraldo do Araguaia', 'cod': 200}
    'Processing Record 365 | sennoy, ru'
    {'coord': {'lon': 46.96, 'lat': 52.16}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 63.81, 'pressure': 1006.62, 'humidity': 43, 'temp_min': 63.81, 'temp_max': 63.81, 'sea_level': 1023.85, 'grnd_level': 1006.62}, 'wind': {'speed': 7.65, 'deg': 306.503}, 'clouds': {'all': 0}, 'dt': 1529554594, 'sys': {'message': 0.0028, 'country': 'RU', 'sunrise': 1529541060, 'sunset': 1529601415}, 'id': 497019, 'name': 'Sennoy', 'cod': 200}
    'Processing Record 366 | zhenlai, cn'
    {'coord': {'lon': 123.2, 'lat': 45.84}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 81.54, 'pressure': 1000.54, 'humidity': 49, 'temp_min': 81.54, 'temp_max': 81.54, 'sea_level': 1017.28, 'grnd_level': 1000.54}, 'wind': {'speed': 7.76, 'deg': 314.503}, 'clouds': {'all': 0}, 'dt': 1529554594, 'sys': {'message': 0.0037, 'country': 'CN', 'sunrise': 1529524618, 'sunset': 1529581256}, 'id': 2033128, 'name': 'Zhenlai', 'cod': 200}
    'Processing Record 367 | kouroussa, gn'
    {'coord': {'lon': -9.88, 'lat': 10.65}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 72.54, 'pressure': 981.09, 'humidity': 95, 'temp_min': 72.54, 'temp_max': 72.54, 'sea_level': 1027.25, 'grnd_level': 981.09}, 'wind': {'speed': 10.45, 'deg': 240.503}, 'clouds': {'all': 56}, 'dt': 1529554531, 'sys': {'message': 0.0038, 'country': 'GN', 'sunrise': 1529561933, 'sunset': 1529607829}, 'id': 2418437, 'name': 'Kouroussa', 'cod': 200}
    'Processing Record 368 | dunda, tz'
    {'coord': {'lon': 34.25, 'lat': -8.12}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'base': 'stations', 'main': {'temp': 62.82, 'pressure': 911.3, 'humidity': 83, 'temp_min': 62.82, 'temp_max': 62.82, 'sea_level': 1031.43, 'grnd_level': 911.3}, 'wind': {'speed': 7.87, 'deg': 142.503}, 'clouds': {'all': 32}, 'dt': 1529554594, 'sys': {'message': 0.0027, 'country': 'TZ', 'sunrise': 1529553316, 'sunset': 1529595261}, 'id': 160141, 'name': 'Dunda', 'cod': 200}
    'Processing Record 369 | santa maria, cv'
    {'coord': {'lon': -22.9, 'lat': 16.6}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 71.6, 'pressure': 1017, 'humidity': 83, 'temp_min': 71.6, 'temp_max': 71.6}, 'visibility': 10000, 'wind': {'speed': 12.75, 'deg': 20}, 'clouds': {'all': 75}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 6186, 'message': 0.0092, 'country': 'CV', 'sunrise': 1529564391, 'sunset': 1529611621}, 'id': 3374218, 'name': 'Santa Maria', 'cod': 200}
    'Processing Record 370 | mrirt, ma'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for mrirt, ma**
    'Processing Record 371 | ruatoria, nz'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for ruatoria, nz**
    'Processing Record 372 | padang, id'
    {'coord': {'lon': 100.36, 'lat': -0.92}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 'base': 'stations', 'main': {'temp': 85.14, 'pressure': 1017.89, 'humidity': 100, 'temp_min': 85.14, 'temp_max': 85.14, 'sea_level': 1023.36, 'grnd_level': 1017.89}, 'wind': {'speed': 3.62, 'deg': 88.5034}, 'clouds': {'all': 20}, 'dt': 1529554828, 'sys': {'message': 0.0044, 'country': 'ID', 'sunrise': 1529536694, 'sunset': 1529580145}, 'id': 1633419, 'name': 'Padang', 'cod': 200}
    'Processing Record 373 | katha, mm'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for katha, mm**
    'Processing Record 374 | kamenka, ru'
    {'coord': {'lon': 44.05, 'lat': 53.19}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 63, 'pressure': 998.92, 'humidity': 50, 'temp_min': 63, 'temp_max': 63, 'sea_level': 1024.42, 'grnd_level': 998.92}, 'wind': {'speed': 9.55, 'deg': 289.503}, 'clouds': {'all': 0}, 'dt': 1529554828, 'sys': {'message': 0.0043, 'country': 'RU', 'sunrise': 1529541385, 'sunset': 1529602486}, 'id': 553725, 'name': 'Kamenka', 'cod': 200}
    'Processing Record 375 | zaysan, kz'
    {'coord': {'lon': 84.87, 'lat': 47.47}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '02d'}], 'base': 'stations', 'main': {'temp': 69.3, 'pressure': 907, 'humidity': 48, 'temp_min': 69.3, 'temp_max': 69.3, 'sea_level': 1024.5, 'grnd_level': 907}, 'wind': {'speed': 4.97, 'deg': 275.003}, 'clouds': {'all': 8}, 'dt': 1529554595, 'sys': {'message': 0.0039, 'country': 'KZ', 'sunrise': 1529533397, 'sunset': 1529590878}, 'id': 1517060, 'name': 'Zaysan', 'cod': 200}
    'Processing Record 376 | ouesso, cg'
    {'coord': {'lon': 16.05, 'lat': 1.61}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 71.19, 'pressure': 986.52, 'humidity': 95, 'temp_min': 71.19, 'temp_max': 71.19, 'sea_level': 1027.5, 'grnd_level': 986.52}, 'wind': {'speed': 2.28, 'deg': 171.503}, 'clouds': {'all': 64}, 'dt': 1529554595, 'sys': {'message': 0.0032, 'country': 'CG', 'sunrise': 1529556668, 'sunset': 1529600646}, 'id': 2255564, 'name': 'Ouesso', 'cod': 200}
    'Processing Record 377 | cidreira, br'
    {'coord': {'lon': -50.22, 'lat': -30.17}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 50.22, 'pressure': 1021.46, 'humidity': 87, 'temp_min': 50.22, 'temp_max': 50.22, 'sea_level': 1031.71, 'grnd_level': 1021.46}, 'wind': {'speed': 2.39, 'deg': 50.0034}, 'clouds': {'all': 0}, 'dt': 1529554595, 'sys': {'message': 0.0039, 'country': 'BR', 'sunrise': 1529576204, 'sunset': 1529612924}, 'id': 3466165, 'name': 'Cidreira', 'cod': 200}
    'Processing Record 378 | sibolga, id'
    {'coord': {'lon': 98.78, 'lat': 1.74}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 75.33, 'pressure': 943.48, 'humidity': 95, 'temp_min': 75.33, 'temp_max': 75.33, 'sea_level': 1024.09, 'grnd_level': 943.48}, 'wind': {'speed': 2.62, 'deg': 55.5034}, 'clouds': {'all': 80}, 'dt': 1529554829, 'sys': {'message': 0.004, 'country': 'ID', 'sunrise': 1529536796, 'sunset': 1529580801}, 'id': 1213855, 'name': 'Sibolga', 'cod': 200}
    'Processing Record 379 | tapaua, br'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for tapaua, br**
    'Processing Record 380 | tallahassee, us'
    {'coord': {'lon': -84.28, 'lat': 30.44}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 81.46, 'pressure': 1014, 'humidity': 74, 'temp_min': 78.8, 'temp_max': 82.4}, 'visibility': 16093, 'wind': {'speed': 6.93, 'deg': 280}, 'clouds': {'all': 20}, 'dt': 1529554500, 'sys': {'type': 1, 'id': 716, 'message': 0.004, 'country': 'US', 'sunrise': 1529577332, 'sunset': 1529628147}, 'id': 4174715, 'name': 'Tallahassee', 'cod': 200}
    'Processing Record 381 | nuevo progreso, mx'
    {'coord': {'lon': -95.05, 'lat': 17.14}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'base': 'stations', 'main': {'temp': 84.33, 'pressure': 1011.57, 'humidity': 60, 'temp_min': 84.33, 'temp_max': 84.33, 'sea_level': 1022.43, 'grnd_level': 1011.57}, 'wind': {'speed': 19.28, 'deg': 187.503}, 'clouds': {'all': 44}, 'dt': 1529554595, 'sys': {'message': 0.0041, 'country': 'MX', 'sunrise': 1529581647, 'sunset': 1529629002}, 'id': 3522013, 'name': 'Nuevo Progreso', 'cod': 200}
    'Processing Record 382 | palabuhanratu, id'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for palabuhanratu, id**
    'Processing Record 383 | tessalit, ml'
    {'coord': {'lon': 1.01, 'lat': 20.2}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 82.44, 'pressure': 962.69, 'humidity': 17, 'temp_min': 82.44, 'temp_max': 82.44, 'sea_level': 1020.85, 'grnd_level': 962.69}, 'wind': {'speed': 11.45, 'deg': 45.5034}, 'clouds': {'all': 0}, 'dt': 1529554829, 'sys': {'message': 0.0046, 'country': 'ML', 'sunrise': 1529558225, 'sunset': 1529606308}, 'id': 2449893, 'name': 'Tessalit', 'cod': 200}
    'Processing Record 384 | gizo, sb'
    {'coord': {'lon': 156.84, 'lat': -8.1}, 'weather': [{'id': 501, 'main': 'Rain', 'description': 'moderate rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 82.17, 'pressure': 1024.54, 'humidity': 100, 'temp_min': 82.17, 'temp_max': 82.17, 'sea_level': 1024.7, 'grnd_level': 1024.54}, 'wind': {'speed': 14.58, 'deg': 119.503}, 'rain': {'3h': 3.74}, 'clouds': {'all': 80}, 'dt': 1529554596, 'sys': {'message': 0.0037, 'country': 'SB', 'sunrise': 1529523887, 'sunset': 1529565837}, 'id': 2108857, 'name': 'Gizo', 'cod': 200}
    'Processing Record 385 | puerto del rosario, es'
    {'coord': {'lon': -13.86, 'lat': 28.5}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'base': 'stations', 'main': {'temp': 69.8, 'pressure': 1017, 'humidity': 73, 'temp_min': 69.8, 'temp_max': 69.8}, 'visibility': 10000, 'wind': {'speed': 14.99, 'deg': 350}, 'clouds': {'all': 40}, 'dt': 1529553600, 'sys': {'type': 1, 'id': 5512, 'message': 0.0031, 'country': 'ES', 'sunrise': 1529560710, 'sunset': 1529610963}, 'id': 2512186, 'name': 'Puerto del Rosario', 'cod': 200}
    'Processing Record 386 | mergui, mm'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for mergui, mm**
    'Processing Record 387 | panzhihua, cn'
    {'coord': {'lon': 101.72, 'lat': 26.59}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 67.86, 'pressure': 832.99, 'humidity': 95, 'temp_min': 67.86, 'temp_max': 67.86, 'sea_level': 1015.18, 'grnd_level': 832.99}, 'wind': {'speed': 3.06, 'deg': 120.003}, 'rain': {'3h': 0.705}, 'clouds': {'all': 88}, 'dt': 1529554596, 'sys': {'message': 0.0025, 'country': 'CN', 'sunrise': 1529533232, 'sunset': 1529582954}, 'id': 6929460, 'name': 'Panzhihua', 'cod': 200}
    'Processing Record 388 | hamilton, bm'
    {'coord': {'lon': -64.78, 'lat': 32.3}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 77, 'pressure': 1014, 'humidity': 83, 'temp_min': 77, 'temp_max': 77}, 'visibility': 10000, 'wind': {'speed': 13.87, 'deg': 230}, 'clouds': {'all': 20}, 'dt': 1529553300, 'sys': {'type': 1, 'id': 4169, 'message': 0.0038, 'country': 'BM', 'sunrise': 1529572369, 'sunset': 1529623748}, 'id': 3573197, 'name': 'Hamilton', 'cod': 200}
    'Processing Record 389 | burnie, au'
    {'coord': {'lon': 145.91, 'lat': -41.05}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 52.92, 'pressure': 1036.78, 'humidity': 100, 'temp_min': 52.92, 'temp_max': 52.92, 'sea_level': 1039.53, 'grnd_level': 1036.78}, 'wind': {'speed': 10.22, 'deg': 242.003}, 'clouds': {'all': 0}, 'dt': 1529554597, 'sys': {'message': 0.0042, 'country': 'AU', 'sunrise': 1529530895, 'sunset': 1529564076}, 'id': 2173125, 'name': 'Burnie', 'cod': 200}
    'Processing Record 390 | kawana waters, au'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for kawana waters, au**
    'Processing Record 391 | babanusah, sd'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for babanusah, sd**
    'Processing Record 392 | ishigaki, jp'
    {'coord': {'lon': 124.16, 'lat': 24.34}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 86, 'pressure': 1007, 'humidity': 84, 'temp_min': 86, 'temp_max': 86}, 'visibility': 10000, 'wind': {'speed': 18.34, 'deg': 190}, 'clouds': {'all': 75}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 7627, 'message': 0.0035, 'country': 'JP', 'sunrise': 1529528145, 'sunset': 1529577268}, 'id': 1861416, 'name': 'Ishigaki', 'cod': 200}
    'Processing Record 393 | price, us'
    {'coord': {'lon': -110.81, 'lat': 39.6}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 78.8, 'pressure': 1021, 'humidity': 22, 'temp_min': 78.8, 'temp_max': 78.8}, 'visibility': 16093, 'wind': {'speed': 9.17, 'deg': 320}, 'clouds': {'all': 1}, 'dt': 1529549580, 'sys': {'type': 1, 'id': 2823, 'message': 0.0034, 'country': 'US', 'sunrise': 1529582156, 'sunset': 1529636059}, 'id': 5545269, 'name': 'Price', 'cod': 200}
    'Processing Record 394 | doctor pedro p. pena, py'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for doctor pedro p. pena, py**
    'Processing Record 395 | ust-kuyga, ru'
    {'coord': {'lon': 135.55, 'lat': 70}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 71.46, 'pressure': 993.33, 'humidity': 49, 'temp_min': 71.46, 'temp_max': 71.46, 'sea_level': 1018.78, 'grnd_level': 993.33}, 'wind': {'speed': 6.98, 'deg': 60.0034}, 'clouds': {'all': 0}, 'dt': 1529554597, 'sys': {'message': 0.003, 'country': 'RU', 'sunrise': 0, 'sunset': 0}, 'id': 2013921, 'name': 'Ust-Kuyga', 'cod': 200}
    'Processing Record 396 | bur gabo, so'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for bur gabo, so**
    'Processing Record 397 | moindou, nc'
    {'coord': {'lon': 165.68, 'lat': -21.69}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 73.4, 'pressure': 1016, 'humidity': 53, 'temp_min': 73.4, 'temp_max': 73.4}, 'visibility': 10000, 'wind': {'speed': 9.17, 'deg': 250}, 'clouds': {'all': 75}, 'dt': 1529553600, 'sys': {'type': 1, 'id': 8344, 'message': 0.003, 'country': 'NC', 'sunrise': 1529523282, 'sunset': 1529562198}, 'id': 2140466, 'name': 'Moindou', 'cod': 200}
    'Processing Record 398 | chicama, pe'
    {'coord': {'lon': -79.15, 'lat': -7.84}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 64.4, 'pressure': 1017, 'humidity': 88, 'temp_min': 64.4, 'temp_max': 64.4}, 'visibility': 8000, 'wind': {'speed': 8.05, 'deg': 150}, 'clouds': {'all': 90}, 'dt': 1529553600, 'sys': {'type': 1, 'id': 4404, 'message': 0.0034, 'country': 'PE', 'sunrise': 1529580506, 'sunset': 1529622510}, 'id': 3698359, 'name': 'Chicama', 'cod': 200}
    'Processing Record 399 | smithers, ca'
    {'coord': {'lon': -127.17, 'lat': 54.78}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 64.4, 'pressure': 1013, 'humidity': 88, 'temp_min': 64.4, 'temp_max': 64.4}, 'visibility': 40233, 'wind': {'speed': 1.72, 'deg': 280.003}, 'clouds': {'all': 75}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 3345, 'message': 0.0038, 'country': 'CA', 'sunrise': 1529581853, 'sunset': 1529644215}, 'id': 6149996, 'name': 'Smithers', 'cod': 200}
    'Processing Record 400 | alice town, bs'
    {'coord': {'lon': -79.3, 'lat': 25.72}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 83.7, 'pressure': 1027.7, 'humidity': 100, 'temp_min': 83.7, 'temp_max': 83.7, 'sea_level': 1027.74, 'grnd_level': 1027.7}, 'wind': {'speed': 7.76, 'deg': 179.003}, 'clouds': {'all': 8}, 'dt': 1529554598, 'sys': {'message': 0.0039, 'country': 'BS', 'sunrise': 1529576800, 'sunset': 1529626288}, 'id': 3572924, 'name': 'Alice Town', 'cod': 200}
    'Processing Record 401 | varska, ee'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for varska, ee**
    'Processing Record 402 | zhezkazgan, kz'
    {'coord': {'lon': 67.71, 'lat': 47.8}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 82.4, 'pressure': 1010, 'humidity': 21, 'temp_min': 82.4, 'temp_max': 82.4}, 'visibility': 10000, 'wind': {'speed': 8.95, 'deg': 250}, 'clouds': {'all': 0}, 'dt': 1529551800, 'sys': {'type': 1, 'id': 7201, 'message': 0.004, 'country': 'KZ', 'sunrise': 1529537426, 'sunset': 1529595087}, 'id': 1516589, 'name': 'Zhezkazgan', 'cod': 200}
    'Processing Record 403 | manado, id'
    {'coord': {'lon': 124.85, 'lat': 1.49}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'base': 'stations', 'main': {'temp': 86, 'pressure': 1011, 'humidity': 66, 'temp_min': 86, 'temp_max': 86}, 'visibility': 10000, 'wind': {'speed': 5.82, 'deg': 260}, 'clouds': {'all': 40}, 'dt': 1529553600, 'sys': {'type': 1, 'id': 8012, 'message': 0.0039, 'country': 'ID', 'sunrise': 1529530564, 'sunset': 1529574517}, 'id': 1636544, 'name': 'Manado', 'cod': 200}
    'Processing Record 404 | santa rosa, ar'
    {'coord': {'lon': -64.29, 'lat': -36.62}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 48.24, 'pressure': 1008.81, 'humidity': 53, 'temp_min': 48.24, 'temp_max': 48.24, 'sea_level': 1027.78, 'grnd_level': 1008.81}, 'wind': {'speed': 13.47, 'deg': 219.503}, 'clouds': {'all': 0}, 'dt': 1529554599, 'sys': {'message': 0.0033, 'country': 'AR', 'sunrise': 1529580563, 'sunset': 1529615320}, 'id': 3835994, 'name': 'Santa Rosa', 'cod': 200}
    'Processing Record 405 | grenada, us'
    {'coord': {'lon': -89.81, 'lat': 33.77}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 78.8, 'pressure': 1013, 'humidity': 88, 'temp_min': 78.8, 'temp_max': 78.8}, 'visibility': 16093, 'wind': {'speed': 4.07, 'deg': 262.503}, 'clouds': {'all': 90}, 'dt': 1529549580, 'sys': {'type': 1, 'id': 1686, 'message': 0.0085, 'country': 'US', 'sunrise': 1529578145, 'sunset': 1529629989}, 'id': 4428539, 'name': 'Grenada', 'cod': 200}
    'Processing Record 406 | leshukonskoye, ru'
    {'coord': {'lon': 45.76, 'lat': 64.9}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 56.16, 'pressure': 994.47, 'humidity': 100, 'temp_min': 56.16, 'temp_max': 56.16, 'sea_level': 1003.18, 'grnd_level': 994.47}, 'wind': {'speed': 5.97, 'deg': 318.003}, 'rain': {'3h': 2.9}, 'clouds': {'all': 100}, 'dt': 1529554745, 'sys': {'message': 0.003, 'country': 'RU', 'sunrise': 1529532087, 'sunset': 1529610962}, 'id': 535839, 'name': 'Leshukonskoye', 'cod': 200}
    'Processing Record 407 | khandyga, ru'
    {'coord': {'lon': 135.58, 'lat': 62.65}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 67.41, 'pressure': 993.98, 'humidity': 39, 'temp_min': 67.41, 'temp_max': 67.41, 'sea_level': 1017.44, 'grnd_level': 993.98}, 'wind': {'speed': 6.87, 'deg': 138.003}, 'clouds': {'all': 88}, 'dt': 1529554478, 'sys': {'message': 0.0029, 'country': 'RU', 'sunrise': 1529513780, 'sunset': 1529586151}, 'id': 2022773, 'name': 'Khandyga', 'cod': 200}
    'Processing Record 408 | matay, eg'
    {'coord': {'lon': 30.79, 'lat': 28.42}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 75.6, 'pressure': 1015.86, 'humidity': 49, 'temp_min': 75.6, 'temp_max': 75.6, 'sea_level': 1027.33, 'grnd_level': 1015.86}, 'wind': {'speed': 8.32, 'deg': 27.0034}, 'clouds': {'all': 0}, 'dt': 1529554599, 'sys': {'message': 0.0034, 'country': 'EG', 'sunrise': 1529550003, 'sunset': 1529600234}, 'id': 352628, 'name': 'Matay', 'cod': 200}
    'Processing Record 409 | dalvik, is'
    {'coord': {'lon': -18.53, 'lat': 65.97}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 35.6, 'pressure': 1020, 'humidity': 92, 'temp_min': 35.6, 'temp_max': 35.6}, 'visibility': 10000, 'wind': {'speed': 2.24}, 'clouds': {'all': 0}, 'dt': 1529553600, 'sys': {'type': 1, 'id': 4826, 'message': 0.0029, 'country': 'IS', 'sunrise': 0, 'sunset': 0}, 'id': 2632287, 'name': 'Dalvik', 'cod': 200}
    'Processing Record 410 | leh, in'
    {'coord': {'lon': 77.58, 'lat': 34.16}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 31.77, 'pressure': 609.59, 'humidity': 100, 'temp_min': 31.77, 'temp_max': 31.77, 'sea_level': 1018.98, 'grnd_level': 609.59}, 'wind': {'speed': 0.72, 'deg': 63.5034}, 'clouds': {'all': 76}, 'dt': 1529554599, 'sys': {'message': 0.0028, 'country': 'IN', 'sunrise': 1529537902, 'sunset': 1529589873}, 'id': 1264976, 'name': 'Leh', 'cod': 200}
    'Processing Record 411 | belyy yar, ru'
    {'coord': {'lon': 91.39, 'lat': 53.6}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 73.4, 'pressure': 1009, 'humidity': 56, 'temp_min': 73.4, 'temp_max': 73.4}, 'visibility': 10000, 'wind': {'speed': 4.47, 'deg': 190}, 'clouds': {'all': 0}, 'dt': 1529551800, 'sys': {'type': 1, 'id': 7276, 'message': 0.0034, 'country': 'RU', 'sunrise': 1529529866, 'sunset': 1529591279}, 'id': 1510377, 'name': 'Belyy Yar', 'cod': 200}
    'Processing Record 412 | san jose, bo'
    {'coord': {'lon': -63.35, 'lat': -17.94}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 62.6, 'pressure': 1016, 'humidity': 93, 'temp_min': 62.6, 'temp_max': 62.6}, 'visibility': 10000, 'wind': {'speed': 5.82, 'deg': 330}, 'clouds': {'all': 0}, 'dt': 1529553600, 'sys': {'type': 1, 'id': 4443, 'message': 0.0037, 'country': 'BO', 'sunrise': 1529577818, 'sunset': 1529617614}, 'id': 3904666, 'name': 'San Jose', 'cod': 200}
    'Processing Record 413 | skala, gr'
    {'coord': {'lon': 22.66, 'lat': 36.85}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 'base': 'stations', 'main': {'temp': 60.8, 'pressure': 1015, 'humidity': 82, 'temp_min': 60.8, 'temp_max': 60.8}, 'visibility': 10000, 'wind': {'speed': 5.19, 'deg': 289.503}, 'clouds': {'all': 20}, 'dt': 1529553000, 'sys': {'type': 1, 'id': 5680, 'message': 0.0041, 'country': 'GR', 'sunrise': 1529550627, 'sunset': 1529603513}, 'id': 253739, 'name': 'Skala', 'cod': 200}
    'Processing Record 414 | isangel, vu'
    {'coord': {'lon': 169.27, 'lat': -19.55}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 74.25, 'pressure': 1026.16, 'humidity': 100, 'temp_min': 74.25, 'temp_max': 74.25, 'sea_level': 1028.19, 'grnd_level': 1026.16}, 'wind': {'speed': 11.68, 'deg': 196.003}, 'clouds': {'all': 0}, 'dt': 1529554831, 'sys': {'message': 0.0086, 'country': 'VU', 'sunrise': 1529522167, 'sunset': 1529561590}, 'id': 2136825, 'name': 'Isangel', 'cod': 200}
    'Processing Record 415 | pimampiro, ec'
    {'coord': {'lon': -77.94, 'lat': 0.39}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10n'}], 'base': 'stations', 'main': {'temp': 42.66, 'pressure': 741.56, 'humidity': 100, 'temp_min': 42.66, 'temp_max': 42.66, 'sea_level': 1027.58, 'grnd_level': 741.56}, 'wind': {'speed': 1.95, 'deg': 117.003}, 'rain': {'3h': 0.15}, 'clouds': {'all': 32}, 'dt': 1529554600, 'sys': {'message': 0.0039, 'country': 'EC', 'sunrise': 1529579356, 'sunset': 1529623080}, 'id': 3653146, 'name': 'Pimampiro', 'cod': 200}
    'Processing Record 416 | bushehr, ir'
    {'coord': {'lon': 50.84, 'lat': 28.97}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 87.8, 'pressure': 1001, 'humidity': 48, 'temp_min': 87.8, 'temp_max': 87.8}, 'visibility': 10000, 'wind': {'speed': 11.41, 'deg': 330}, 'clouds': {'all': 0}, 'dt': 1529551800, 'sys': {'type': 1, 'id': 7019, 'message': 0.004, 'country': 'IR', 'sunrise': 1529545112, 'sunset': 1529595499}, 'id': 139817, 'name': 'Bushehr', 'cod': 200}
    'Processing Record 417 | kiama, au'
    {'coord': {'lon': 150.86, 'lat': -34.67}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 60.8, 'pressure': 1026, 'humidity': 55, 'temp_min': 60.8, 'temp_max': 60.8}, 'visibility': 10000, 'wind': {'speed': 5.82, 'deg': 310}, 'clouds': {'all': 0}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 8231, 'message': 0.0042, 'country': 'AU', 'sunrise': 1529528605, 'sunset': 1529563990}, 'id': 2161515, 'name': 'Kiama', 'cod': 200}
    'Processing Record 418 | kaeo, nz'
    {'coord': {'lon': 173.78, 'lat': -35.1}, 'weather': [{'id': 501, 'main': 'Rain', 'description': 'moderate rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 54, 'pressure': 1008.57, 'humidity': 99, 'temp_min': 54, 'temp_max': 54, 'sea_level': 1023.4, 'grnd_level': 1008.57}, 'wind': {'speed': 17.27, 'deg': 109.003}, 'rain': {'3h': 4.03}, 'clouds': {'all': 92}, 'dt': 1529554510, 'sys': {'message': 0.0034, 'country': 'NZ', 'sunrise': 1529523171, 'sunset': 1529558420}, 'id': 2189343, 'name': 'Kaeo', 'cod': 200}
    'Processing Record 419 | sepuka, tz'
    {'coord': {'lon': 34.53, 'lat': -4.75}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 56.79, 'pressure': 863.8, 'humidity': 90, 'temp_min': 56.79, 'temp_max': 56.79, 'sea_level': 1030.09, 'grnd_level': 863.8}, 'wind': {'speed': 10.67, 'deg': 100.003}, 'clouds': {'all': 0}, 'dt': 1529554601, 'sys': {'message': 0.0038, 'country': 'TZ', 'sunrise': 1529552894, 'sunset': 1529595547}, 'id': 150099, 'name': 'Sepuka', 'cod': 200}
    'Processing Record 420 | linhai, cn'
    {'coord': {'lon': 121.14, 'lat': 28.86}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 73.98, 'pressure': 1000.71, 'humidity': 93, 'temp_min': 73.98, 'temp_max': 73.98, 'sea_level': 1022.39, 'grnd_level': 1000.71}, 'wind': {'speed': 4.63, 'deg': 56.5034}, 'rain': {'3h': 0.25999999999999}, 'clouds': {'all': 88}, 'dt': 1529554601, 'sys': {'message': 0.0031, 'country': 'CN', 'sunrise': 1529528254, 'sunset': 1529578609}, 'id': 1803422, 'name': 'Linhai', 'cod': 200}
    'Processing Record 421 | taytay, ph'
    {'coord': {'lon': 119.52, 'lat': 10.83}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'base': 'stations', 'main': {'temp': 84.87, 'pressure': 1020.32, 'humidity': 93, 'temp_min': 84.87, 'temp_max': 84.87, 'sea_level': 1025.11, 'grnd_level': 1020.32}, 'wind': {'speed': 8.43, 'deg': 200.503}, 'clouds': {'all': 48}, 'dt': 1529554601, 'sys': {'message': 0.0035, 'country': 'PH', 'sunrise': 1529530852, 'sunset': 1529576788}, 'id': 1682606, 'name': 'Taytay', 'cod': 200}
    'Processing Record 422 | santa isabel do rio negro, br'
    {'coord': {'lon': -65.02, 'lat': -0.41}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'base': 'stations', 'main': {'temp': 71.73, 'pressure': 1022.84, 'humidity': 100, 'temp_min': 71.73, 'temp_max': 71.73, 'sea_level': 1028.75, 'grnd_level': 1022.84}, 'wind': {'speed': 3.18, 'deg': 321.503}, 'clouds': {'all': 36}, 'dt': 1529554832, 'sys': {'message': 0.0036, 'country': 'BR', 'sunrise': 1529576338, 'sunset': 1529619895}, 'id': 3662489, 'name': 'Santa Isabel do Rio Negro', 'cod': 200}
    'Processing Record 423 | bichura, ru'
    {'coord': {'lon': 107.6, 'lat': 50.59}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 71.37, 'pressure': 914.7, 'humidity': 65, 'temp_min': 71.37, 'temp_max': 71.37, 'sea_level': 1016.19, 'grnd_level': 914.7}, 'wind': {'speed': 2.17, 'deg': 62.0034}, 'clouds': {'all': 92}, 'dt': 1529554601, 'sys': {'message': 0.0035, 'country': 'RU', 'sunrise': 1529527028, 'sunset': 1529586335}, 'id': 2026708, 'name': 'Bichura', 'cod': 200}
    'Processing Record 424 | warangal, in'
    {'coord': {'lon': 79.6, 'lat': 17.99}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 84.69, 'pressure': 986.04, 'humidity': 70, 'temp_min': 84.69, 'temp_max': 84.69, 'sea_level': 1017.16, 'grnd_level': 986.04}, 'wind': {'speed': 4.18, 'deg': 328.003}, 'clouds': {'all': 0}, 'dt': 1529554601, 'sys': {'message': 0.0081, 'country': 'IN', 'sunrise': 1529539625, 'sunset': 1529587180}, 'id': 1252948, 'name': 'Warangal', 'cod': 200}
    'Processing Record 425 | vestmannaeyjar, is'
    {'coord': {'lon': -20.27, 'lat': 63.44}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 45.27, 'pressure': 1030.86, 'humidity': 97, 'temp_min': 45.27, 'temp_max': 45.27, 'sea_level': 1037.02, 'grnd_level': 1030.86}, 'wind': {'speed': 11.68, 'deg': 261.003}, 'clouds': {'all': 0}, 'dt': 1529554602, 'sys': {'message': 0.0165, 'country': 'IS', 'sunrise': 1529550290, 'sunset': 1529624457}, 'id': 3412093, 'name': 'Vestmannaeyjar', 'cod': 200}
    'Processing Record 426 | sentyabrskiy, ru'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for sentyabrskiy, ru**
    'Processing Record 427 | lolua, tv'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for lolua, tv**
    'Processing Record 428 | aksu, cn'
    {'coord': {'lon': 80.26, 'lat': 41.12}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 'base': 'stations', 'main': {'temp': 69.66, 'pressure': 860.39, 'humidity': 50, 'temp_min': 69.66, 'temp_max': 69.66, 'sea_level': 1019.11, 'grnd_level': 860.39}, 'wind': {'speed': 4.74, 'deg': 359.003}, 'clouds': {'all': 12}, 'dt': 1529554602, 'sys': {'message': 0.0034, 'country': 'CN', 'sunrise': 1529535990, 'sunset': 1529590498}, 'id': 1529660, 'name': 'Aksu', 'cod': 200}
    'Processing Record 429 | yarada, in'
    {'coord': {'lon': 83.27, 'lat': 17.65}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 83.97, 'pressure': 1016.76, 'humidity': 99, 'temp_min': 83.97, 'temp_max': 83.97, 'sea_level': 1017.04, 'grnd_level': 1016.76}, 'wind': {'speed': 14.92, 'deg': 245.503}, 'rain': {'3h': 0.11}, 'clouds': {'all': 36}, 'dt': 1529554529, 'sys': {'message': 0.003, 'country': 'IN', 'sunrise': 1529538784, 'sunset': 1529586259}, 'id': 1252783, 'name': 'Yarada', 'cod': 200}
    'Processing Record 430 | kampong thum, kh'
    {'coord': {'lon': 104.89, 'lat': 12.71}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'base': 'stations', 'main': {'temp': 86.76, 'pressure': 1020.81, 'humidity': 82, 'temp_min': 86.76, 'temp_max': 86.76, 'sea_level': 1024.01, 'grnd_level': 1020.81}, 'wind': {'speed': 5.75, 'deg': 196.003}, 'clouds': {'all': 44}, 'dt': 1529554602, 'sys': {'message': 0.0037, 'country': 'KH', 'sunrise': 1529534157, 'sunset': 1529580507}, 'id': 1831125, 'name': 'Kampong Thum', 'cod': 200}
    'Processing Record 431 | satana, in'
    {'coord': {'lon': 74.2, 'lat': 20.6}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '02d'}], 'base': 'stations', 'main': {'temp': 80.1, 'pressure': 954.18, 'humidity': 86, 'temp_min': 80.1, 'temp_max': 80.1, 'sea_level': 1017.04, 'grnd_level': 954.18}, 'wind': {'speed': 9.78, 'deg': 278.003}, 'clouds': {'all': 8}, 'dt': 1529554602, 'sys': {'message': 0.0031, 'country': 'IN', 'sunrise': 1529540608, 'sunset': 1529588789}, 'id': 1257060, 'name': 'Satana', 'cod': 200}
    'Processing Record 432 | longyearbyen, sj'
    {'coord': {'lon': 15.64, 'lat': 78.22}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 42.8, 'pressure': 1007, 'humidity': 81, 'temp_min': 42.8, 'temp_max': 42.8}, 'visibility': 10000, 'wind': {'speed': 5.82, 'deg': 300}, 'clouds': {'all': 75}, 'dt': 1529553000, 'sys': {'type': 1, 'id': 5326, 'message': 0.0045, 'country': 'SJ', 'sunrise': 0, 'sunset': 0}, 'id': 2729907, 'name': 'Longyearbyen', 'cod': 200}
    'Processing Record 433 | avera, pf'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for avera, pf**
    'Processing Record 434 | la libertad, sv'
    {'coord': {'lon': -89.32, 'lat': 13.49}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 77.65, 'pressure': 1014, 'humidity': 88, 'temp_min': 73.4, 'temp_max': 80.6}, 'visibility': 10000, 'wind': {'speed': 3.36, 'deg': 10}, 'clouds': {'all': 20}, 'dt': 1529553000, 'sys': {'type': 1, 'id': 4204, 'message': 0.0071, 'country': 'SV', 'sunrise': 1529580688, 'sunset': 1529627211}, 'id': 3585157, 'name': 'La Libertad', 'cod': 200}
    'Processing Record 435 | vila velha, br'
    {'coord': {'lon': -38.6, 'lat': -3.71}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'base': 'stations', 'main': {'temp': 80.6, 'pressure': 1015, 'humidity': 78, 'temp_min': 80.6, 'temp_max': 80.6}, 'visibility': 10000, 'wind': {'speed': 9.17, 'deg': 90}, 'clouds': {'all': 40}, 'dt': 1529553600, 'sys': {'type': 1, 'id': 4498, 'message': 0.0033, 'country': 'BR', 'sunrise': 1529570340, 'sunset': 1529613210}, 'id': 6320062, 'name': 'Vila Velha', 'cod': 200}
    'Processing Record 436 | formoso do araguaia, br'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for formoso do araguaia, br**
    'Processing Record 437 | bellmead, us'
    {'coord': {'lon': -97.11, 'lat': 31.59}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'base': 'stations', 'main': {'temp': 77.58, 'pressure': 1012, 'humidity': 83, 'temp_min': 75.2, 'temp_max': 78.8}, 'visibility': 16093, 'wind': {'speed': 8.05, 'deg': 140}, 'clouds': {'all': 40}, 'dt': 1529553300, 'sys': {'type': 1, 'id': 2735, 'message': 0.0044, 'country': 'US', 'sunrise': 1529580239, 'sunset': 1529631399}, 'id': 4673389, 'name': 'Bellmead', 'cod': 200}
    'Processing Record 438 | cranbrook, ca'
    {'coord': {'lon': -115.76, 'lat': 49.51}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03n'}], 'base': 'stations', 'main': {'temp': 77, 'pressure': 1013, 'humidity': 33, 'temp_min': 77, 'temp_max': 77}, 'visibility': 40233, 'wind': {'speed': 11.41, 'deg': 200}, 'clouds': {'all': 40}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 3264, 'message': 0.0064, 'country': 'CA', 'sunrise': 1529580976, 'sunset': 1529639615}, 'id': 5931800, 'name': 'Cranbrook', 'cod': 200}
    'Processing Record 439 | bubaque, gw'
    {'coord': {'lon': -15.83, 'lat': 11.28}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 79.56, 'pressure': 1027.94, 'humidity': 100, 'temp_min': 79.56, 'temp_max': 79.56, 'sea_level': 1028.31, 'grnd_level': 1027.94}, 'wind': {'speed': 10.45, 'deg': 248.003}, 'clouds': {'all': 64}, 'dt': 1529554604, 'sys': {'message': 0.0034, 'country': 'GW', 'sunrise': 1529563292, 'sunset': 1529609326}, 'id': 2374583, 'name': 'Bubaque', 'cod': 200}
    'Processing Record 440 | alice springs, au'
    {'coord': {'lon': 133.88, 'lat': -23.7}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 60.8, 'pressure': 1025, 'humidity': 36, 'temp_min': 60.8, 'temp_max': 60.8}, 'visibility': 10000, 'wind': {'speed': 13.87, 'deg': 140}, 'clouds': {'all': 0}, 'dt': 1529551800, 'sys': {'type': 1, 'id': 8163, 'message': 0.0041, 'country': 'AU', 'sunrise': 1529531161, 'sunset': 1529569586}, 'id': 2077895, 'name': 'Alice Springs', 'cod': 200}
    'Processing Record 441 | mwinilunga, zm'
    {'coord': {'lon': 24.43, 'lat': -11.73}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 49.95, 'pressure': 879.2, 'humidity': 76, 'temp_min': 49.95, 'temp_max': 49.95, 'sea_level': 1033.33, 'grnd_level': 879.2}, 'wind': {'speed': 2.62, 'deg': 117.503}, 'clouds': {'all': 0}, 'dt': 1529554604, 'sys': {'message': 0.0031, 'country': 'ZM', 'sunrise': 1529556058, 'sunset': 1529597232}, 'id': 902620, 'name': 'Mwinilunga', 'cod': 200}
    'Processing Record 442 | griffith, au'
    {'coord': {'lon': 146.06, 'lat': -34.29}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 58.32, 'pressure': 1025.51, 'humidity': 100, 'temp_min': 58.32, 'temp_max': 58.32, 'sea_level': 1041.64, 'grnd_level': 1025.51}, 'wind': {'speed': 4.63, 'deg': 12.0034}, 'clouds': {'all': 0}, 'dt': 1529554833, 'sys': {'message': 0.0035, 'country': 'AU', 'sunrise': 1529529698, 'sunset': 1529565201}, 'id': 2164422, 'name': 'Griffith', 'cod': 200}
    'Processing Record 443 | bajil, ye'
    {'coord': {'lon': 43.29, 'lat': 15.06}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 72.18, 'pressure': 997.06, 'humidity': 75, 'temp_min': 72.18, 'temp_max': 72.18, 'sea_level': 1020.93, 'grnd_level': 997.06}, 'wind': {'speed': 2.62, 'deg': 42.5034}, 'clouds': {'all': 0}, 'dt': 1529554604, 'sys': {'message': 0.0031, 'country': 'YE', 'sunrise': 1529548680, 'sunset': 1529595557}, 'id': 77408, 'name': 'Bajil', 'cod': 200}
    'Processing Record 444 | comodoro rivadavia, ar'
    {'coord': {'lon': -67.48, 'lat': -45.87}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 44.6, 'pressure': 1001, 'humidity': 45, 'temp_min': 44.6, 'temp_max': 44.6}, 'visibility': 10000, 'wind': {'speed': 16.11, 'deg': 270}, 'clouds': {'all': 0}, 'dt': 1529553600, 'sys': {'type': 1, 'id': 4741, 'message': 0.0033, 'country': 'AR', 'sunrise': 1529583127, 'sunset': 1529614288}, 'id': 3860443, 'name': 'Comodoro Rivadavia', 'cod': 200}
    'Processing Record 445 | kruisfontein, za'
    {'coord': {'lon': 24.73, 'lat': -34}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 52.47, 'pressure': 1023.65, 'humidity': 94, 'temp_min': 52.47, 'temp_max': 52.47, 'sea_level': 1033.45, 'grnd_level': 1023.65}, 'wind': {'speed': 10.89, 'deg': 53.5034}, 'clouds': {'all': 0}, 'dt': 1529554605, 'sys': {'message': 0.003, 'country': 'ZA', 'sunrise': 1529558777, 'sunset': 1529594370}, 'id': 986717, 'name': 'Kruisfontein', 'cod': 200}
    'Processing Record 446 | tshane, bw'
    {'coord': {'lon': 21.87, 'lat': -24.02}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 43.11, 'pressure': 905.22, 'humidity': 41, 'temp_min': 43.11, 'temp_max': 43.11, 'sea_level': 1038.76, 'grnd_level': 905.22}, 'wind': {'speed': 6.98, 'deg': 29.5034}, 'clouds': {'all': 0}, 'dt': 1529554605, 'sys': {'message': 0.0035, 'country': 'BW', 'sunrise': 1529558087, 'sunset': 1529596432}, 'id': 933726, 'name': 'Tshane', 'cod': 200}
    'Processing Record 447 | montepuez, mz'
    {'coord': {'lon': 39, 'lat': -13.13}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 61.65, 'pressure': 976.39, 'humidity': 92, 'temp_min': 61.65, 'temp_max': 61.65, 'sea_level': 1033.25, 'grnd_level': 976.39}, 'wind': {'speed': 7.43, 'deg': 177.503}, 'clouds': {'all': 0}, 'dt': 1529554605, 'sys': {'message': 0.0026, 'country': 'MZ', 'sunrise': 1529552713, 'sunset': 1529593583}, 'id': 1037125, 'name': 'Montepuez', 'cod': 200}
    'Processing Record 448 | ikorodu, ng'
    {'coord': {'lon': 3.5, 'lat': 6.62}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 73.4, 'pressure': 1015, 'humidity': 100, 'temp_min': 73.4, 'temp_max': 73.4}, 'visibility': 7000, 'wind': {'speed': 3.36, 'deg': 330}, 'clouds': {'all': 20}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 6296, 'message': 0.0045, 'country': 'NG', 'sunrise': 1529559154, 'sunset': 1529604184}, 'id': 2344082, 'name': 'Ikorodu', 'cod': 200}
    'Processing Record 449 | nhulunbuy, au'
    {'coord': {'lon': 136.78, 'lat': -12.18}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'base': 'stations', 'main': {'temp': 84.2, 'pressure': 1014, 'humidity': 58, 'temp_min': 84.2, 'temp_max': 84.2}, 'visibility': 10000, 'wind': {'speed': 14.99, 'deg': 140}, 'clouds': {'all': 40}, 'dt': 1529551800, 'sys': {'type': 1, 'id': 8188, 'message': 0.0032, 'country': 'AU', 'sunrise': 1529529139, 'sunset': 1529570216}, 'id': 2064735, 'name': 'Nhulunbuy', 'cod': 200}
    'Processing Record 450 | hobyo, so'
    {'coord': {'lon': 48.53, 'lat': 5.35}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 74.97, 'pressure': 1017.32, 'humidity': 85, 'temp_min': 74.97, 'temp_max': 74.97, 'sea_level': 1026.73, 'grnd_level': 1017.32}, 'wind': {'speed': 20.18, 'deg': 216.503}, 'clouds': {'all': 0}, 'dt': 1529554605, 'sys': {'message': 0.0035, 'country': 'SO', 'sunrise': 1529548480, 'sunset': 1529593241}, 'id': 57000, 'name': 'Hobyo', 'cod': 200}
    'Processing Record 451 | sangar, ru'
    {'coord': {'lon': 127.47, 'lat': 63.92}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 'base': 'stations', 'main': {'temp': 65.16, 'pressure': 990.33, 'humidity': 51, 'temp_min': 65.16, 'temp_max': 65.16, 'sea_level': 1017.16, 'grnd_level': 990.33}, 'wind': {'speed': 9.22, 'deg': 113.003}, 'clouds': {'all': 12}, 'dt': 1529554606, 'sys': {'message': 0.0038, 'country': 'RU', 'sunrise': 1529514187, 'sunset': 1529589637}, 'id': 2017215, 'name': 'Sangar', 'cod': 200}
    'Processing Record 452 | eureka, us'
    {'coord': {'lon': -124.16, 'lat': 40.8}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 54.68, 'pressure': 1019, 'humidity': 87, 'temp_min': 53.6, 'temp_max': 55.4}, 'visibility': 16093, 'wind': {'speed': 6.93, 'deg': 300}, 'clouds': {'all': 90}, 'dt': 1529552400, 'sys': {'type': 1, 'id': 386, 'message': 0.0037, 'country': 'US', 'sunrise': 1529585123, 'sunset': 1529639501}, 'id': 5563397, 'name': 'Eureka', 'cod': 200}
    'Processing Record 453 | itarema, br'
    {'coord': {'lon': -39.92, 'lat': -2.92}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 75.6, 'pressure': 1022.59, 'humidity': 87, 'temp_min': 75.6, 'temp_max': 75.6, 'sea_level': 1028.35, 'grnd_level': 1022.59}, 'wind': {'speed': 10, 'deg': 78.5034}, 'clouds': {'all': 0}, 'dt': 1529554606, 'sys': {'message': 0.0058, 'country': 'BR', 'sunrise': 1529570574, 'sunset': 1529613609}, 'id': 3393692, 'name': 'Itarema', 'cod': 200}
    'Processing Record 454 | nelson bay, au'
    {'coord': {'lon': 152.14, 'lat': -32.72}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 59, 'pressure': 1026, 'humidity': 82, 'temp_min': 59, 'temp_max': 59}, 'visibility': 10000, 'wind': {'speed': 5.82, 'deg': 170}, 'clouds': {'all': 75}, 'dt': 1529553600, 'sys': {'type': 1, 'id': 8242, 'message': 0.0043, 'country': 'AU', 'sunrise': 1529528000, 'sunset': 1529563981}, 'id': 2155562, 'name': 'Nelson Bay', 'cod': 200}
    'Processing Record 455 | coruripe, br'
    {'coord': {'lon': -36.18, 'lat': -10.12}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 78.21, 'pressure': 1030.29, 'humidity': 95, 'temp_min': 78.21, 'temp_max': 78.21, 'sea_level': 1031.43, 'grnd_level': 1030.29}, 'wind': {'speed': 14.81, 'deg': 117.003}, 'clouds': {'all': 92}, 'dt': 1529554606, 'sys': {'message': 0.004, 'country': 'BR', 'sunrise': 1529570434, 'sunset': 1529611954}, 'id': 3465329, 'name': 'Coruripe', 'cod': 200}
    'Processing Record 456 | viedma, ar'
    {'coord': {'lon': -62.99, 'lat': -40.81}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 48.24, 'pressure': 1015.13, 'humidity': 44, 'temp_min': 48.24, 'temp_max': 48.24, 'sea_level': 1018.9, 'grnd_level': 1015.13}, 'wind': {'speed': 21.97, 'deg': 268.003}, 'clouds': {'all': 0}, 'dt': 1529554606, 'sys': {'message': 0.0035, 'country': 'AR', 'sunrise': 1529580993, 'sunset': 1529614266}, 'id': 3832899, 'name': 'Viedma', 'cod': 200}
    'Processing Record 457 | carballo, es'
    {'coord': {'lon': -8.69, 'lat': 43.21}, 'weather': [{'id': 701, 'main': 'Mist', 'description': 'mist', 'icon': '50n'}], 'base': 'stations', 'main': {'temp': 61.66, 'pressure': 1019, 'humidity': 100, 'temp_min': 60.8, 'temp_max': 62.6}, 'visibility': 10000, 'wind': {'speed': 3.36, 'deg': 10}, 'clouds': {'all': 0}, 'dt': 1529553600, 'sys': {'type': 1, 'id': 5474, 'message': 0.0037, 'country': 'ES', 'sunrise': 1529556895, 'sunset': 1529612295}, 'id': 3126369, 'name': 'Carballo', 'cod': 200}
    'Processing Record 458 | kongolo, cd'
    {'coord': {'lon': 27, 'lat': -5.39}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 74.7, 'pressure': 952.15, 'humidity': 50, 'temp_min': 74.7, 'temp_max': 74.7, 'sea_level': 1026.08, 'grnd_level': 952.15}, 'wind': {'speed': 2.39, 'deg': 136.003}, 'clouds': {'all': 76}, 'dt': 1529554607, 'sys': {'message': 0.0034, 'country': 'CD', 'sunrise': 1529554769, 'sunset': 1529597288}, 'id': 212360, 'name': 'Kongolo', 'cod': 200}
    'Processing Record 459 | port hardy, ca'
    {'coord': {'lon': -127.42, 'lat': 50.7}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 66.2, 'pressure': 1014, 'humidity': 68, 'temp_min': 66.2, 'temp_max': 66.2}, 'visibility': 32186, 'wind': {'speed': 8.05, 'deg': 340}, 'clouds': {'all': 75}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 3322, 'message': 0.0045, 'country': 'CA', 'sunrise': 1529583406, 'sunset': 1529642782}, 'id': 6111862, 'name': 'Port Hardy', 'cod': 200}
    'Processing Record 460 | kisangani, cd'
    {'coord': {'lon': 25.21, 'lat': 0.52}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 71.91, 'pressure': 977.04, 'humidity': 100, 'temp_min': 71.91, 'temp_max': 71.91, 'sea_level': 1027.62, 'grnd_level': 977.04}, 'wind': {'speed': 2.62, 'deg': 48.0034}, 'clouds': {'all': 88}, 'dt': 1529554834, 'sys': {'message': 0.0064, 'country': 'CD', 'sunrise': 1529554583, 'sunset': 1529598333}, 'id': 212730, 'name': 'Kisangani', 'cod': 200}
    'Processing Record 461 | kyaikkami, mm'
    {'coord': {'lon': 97.57, 'lat': 16.08}, 'weather': [{'id': 501, 'main': 'Rain', 'description': 'moderate rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 75.96, 'pressure': 1018.7, 'humidity': 100, 'temp_min': 75.96, 'temp_max': 75.96, 'sea_level': 1022.02, 'grnd_level': 1018.7}, 'wind': {'speed': 5.64, 'deg': 201.003}, 'rain': {'3h': 9.36}, 'clouds': {'all': 92}, 'dt': 1529554607, 'sys': {'message': 0.0041, 'country': 'MM', 'sunrise': 1529535534, 'sunset': 1529582644}, 'id': 1317402, 'name': 'Kyaikkami', 'cod': 200}
    'Processing Record 462 | mogwase, za'
    {'coord': {'lon': 27.22, 'lat': -25.28}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 38.88, 'pressure': 910.89, 'humidity': 89, 'temp_min': 38.88, 'temp_max': 38.88, 'sea_level': 1041.2, 'grnd_level': 910.89}, 'wind': {'speed': 3.96, 'deg': 339.503}, 'clouds': {'all': 0}, 'dt': 1529554607, 'sys': {'message': 0.0028, 'country': 'ZA', 'sunrise': 1529556962, 'sunset': 1529594989}, 'id': 974933, 'name': 'Mogwase', 'cod': 200}
    'Processing Record 463 | moissac, fr'
    {'coord': {'lon': 1.08, 'lat': 44.11}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 67.06, 'pressure': 1018, 'humidity': 94, 'temp_min': 66.2, 'temp_max': 68}, 'visibility': 6000, 'wind': {'speed': 8.05, 'deg': 260}, 'clouds': {'all': 90}, 'dt': 1529553600, 'sys': {'type': 1, 'id': 5523, 'message': 0.0038, 'country': 'FR', 'sunrise': 1529554346, 'sunset': 1529610154}, 'id': 2993586, 'name': 'Moissac', 'cod': 200}
    'Processing Record 464 | oranjemund, na'
    {'coord': {'lon': 16.43, 'lat': -28.55}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 57.42, 'pressure': 1034.51, 'humidity': 100, 'temp_min': 57.42, 'temp_max': 57.42, 'sea_level': 1035.36, 'grnd_level': 1034.51}, 'wind': {'speed': 3.06, 'deg': 55.5034}, 'clouds': {'all': 0}, 'dt': 1529554835, 'sys': {'message': 0.003, 'country': 'NA', 'sunrise': 1529559982, 'sunset': 1529597149}, 'id': 3354071, 'name': 'Oranjemund', 'cod': 200}
    'Processing Record 465 | tabialan, ph'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for tabialan, ph**
    'Processing Record 466 | bridlington, gb'
    {'coord': {'lon': -0.19, 'lat': 54.08}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 'base': 'stations', 'main': {'temp': 48.18, 'pressure': 1019, 'humidity': 76, 'temp_min': 46.4, 'temp_max': 50}, 'visibility': 10000, 'wind': {'speed': 10.29, 'deg': 280}, 'clouds': {'all': 12}, 'dt': 1529553000, 'sys': {'type': 1, 'id': 5181, 'message': 0.0038, 'country': 'GB', 'sunrise': 1529551660, 'sunset': 1529613449}, 'id': 2654728, 'name': 'Bridlington', 'cod': 200}
    'Processing Record 467 | ozgon, kg'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for ozgon, kg**
    'Processing Record 468 | kapit, my'
    {'coord': {'lon': 112.94, 'lat': 2.02}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 84.51, 'pressure': 1000.95, 'humidity': 77, 'temp_min': 84.51, 'temp_max': 84.51, 'sea_level': 1024.42, 'grnd_level': 1000.95}, 'wind': {'speed': 2.95, 'deg': 69.5034}, 'clouds': {'all': 0}, 'dt': 1529554608, 'sys': {'message': 0.0043, 'country': 'MY', 'sunrise': 1529533368, 'sunset': 1529577431}, 'id': 1737185, 'name': 'Kapit', 'cod': 200}
    'Processing Record 469 | rungata, ki'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for rungata, ki**
    'Processing Record 470 | presidente epitacio, br'
    {'coord': {'lon': -52.12, 'lat': -21.76}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 61.47, 'pressure': 997.3, 'humidity': 85, 'temp_min': 61.47, 'temp_max': 61.47, 'sea_level': 1032.32, 'grnd_level': 997.3}, 'wind': {'speed': 2.39, 'deg': 141.003}, 'clouds': {'all': 0}, 'dt': 1529554476, 'sys': {'message': 0.0097, 'country': 'BR', 'sunrise': 1529575571, 'sunset': 1529614470}, 'id': 3452331, 'name': 'Presidente Epitacio', 'cod': 200}
    'Processing Record 471 | upernavik, gl'
    {'coord': {'lon': -56.15, 'lat': 72.79}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 32.58, 'pressure': 1009.22, 'humidity': 95, 'temp_min': 32.58, 'temp_max': 32.58, 'sea_level': 1012.38, 'grnd_level': 1009.22}, 'wind': {'speed': 10.89, 'deg': 359.003}, 'clouds': {'all': 88}, 'dt': 1529554486, 'sys': {'message': 0.0034, 'country': 'GL', 'sunrise': 0, 'sunset': 0}, 'id': 3418910, 'name': 'Upernavik', 'cod': 200}
    'Processing Record 472 | preobrazheniye, ru'
    {'coord': {'lon': 133.91, 'lat': 42.9}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 61.83, 'pressure': 956.85, 'humidity': 88, 'temp_min': 61.83, 'temp_max': 61.83, 'sea_level': 1011.04, 'grnd_level': 956.85}, 'wind': {'speed': 2.62, 'deg': 329.503}, 'rain': {'3h': 0.36}, 'clouds': {'all': 68}, 'dt': 1529554608, 'sys': {'message': 0.0033, 'country': 'RU', 'sunrise': 1529522735, 'sunset': 1529577998}, 'id': 2017658, 'name': 'Preobrazheniye', 'cod': 200}
    'Processing Record 473 | smolenka, ru'
    {'coord': {'lon': 56.05, 'lat': 54.28}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 60.8, 'pressure': 1002, 'humidity': 72, 'temp_min': 60.8, 'temp_max': 60.8}, 'visibility': 10000, 'wind': {'speed': 13.42, 'deg': 250}, 'clouds': {'all': 0}, 'dt': 1529551800, 'sys': {'type': 1, 'id': 7344, 'message': 0.0033, 'country': 'RU', 'sunrise': 1529538080, 'sunset': 1529600030}, 'id': 552312, 'name': 'Smolenka', 'cod': 200}
    'Processing Record 474 | jalingo, ng'
    {'coord': {'lon': 10.93, 'lat': 10.3}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10n'}], 'base': 'stations', 'main': {'temp': 68.76, 'pressure': 978.5, 'humidity': 98, 'temp_min': 68.76, 'temp_max': 68.76, 'sea_level': 1025.88, 'grnd_level': 978.5}, 'wind': {'speed': 9.66, 'deg': 217.003}, 'rain': {'3h': 2.53}, 'clouds': {'all': 92}, 'dt': 1529554609, 'sys': {'message': 0.0032, 'country': 'NG', 'sunrise': 1529556976, 'sunset': 1529602796}, 'id': 2351027, 'name': 'Jalingo', 'cod': 200}
    'Processing Record 475 | ferkessedougou, ci'
    {'coord': {'lon': -5.2, 'lat': 9.6}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10n'}], 'base': 'stations', 'main': {'temp': 73.53, 'pressure': 988.06, 'humidity': 87, 'temp_min': 73.53, 'temp_max': 73.53, 'sea_level': 1026.73, 'grnd_level': 988.06}, 'wind': {'speed': 6.98, 'deg': 206.003}, 'rain': {'3h': 0.575}, 'clouds': {'all': 76}, 'dt': 1529554609, 'sys': {'message': 0.0034, 'country': 'CI', 'sunrise': 1529560923, 'sunset': 1529606592}, 'id': 2289049, 'name': 'Ferkessedougou', 'cod': 200}
    'Processing Record 476 | jiangyou, cn'
    {'coord': {'lon': 104.73, 'lat': 31.78}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 72.09, 'pressure': 940.32, 'humidity': 97, 'temp_min': 72.09, 'temp_max': 72.09, 'sea_level': 1017.28, 'grnd_level': 940.32}, 'wind': {'speed': 4.97, 'deg': 45.5034}, 'rain': {'3h': 2.285}, 'clouds': {'all': 100}, 'dt': 1529554609, 'sys': {'message': 0.0041, 'country': 'CN', 'sunrise': 1529531761, 'sunset': 1529582980}, 'id': 1885823, 'name': 'Jiangyou', 'cod': 200}
    'Processing Record 477 | havoysund, no'
    {'coord': {'lon': 24.66, 'lat': 71}, 'weather': [{'id': 301, 'main': 'Drizzle', 'description': 'drizzle', 'icon': '09d'}], 'base': 'stations', 'main': {'temp': 44.6, 'pressure': 997, 'humidity': 100, 'temp_min': 44.6, 'temp_max': 44.6}, 'visibility': 6000, 'wind': {'speed': 8.05, 'deg': 340}, 'clouds': {'all': 90}, 'dt': 1529553000, 'sys': {'type': 1, 'id': 5300, 'message': 0.0045, 'country': 'NO', 'sunrise': 0, 'sunset': 0}, 'id': 779622, 'name': 'Havoysund', 'cod': 200}
    'Processing Record 478 | san carlos, co'
    {'coord': {'lon': -74.99, 'lat': 6.19}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 59, 'pressure': 1029, 'humidity': 93, 'temp_min': 59, 'temp_max': 59}, 'visibility': 8000, 'wind': {'speed': 1.61, 'deg': 326.503}, 'clouds': {'all': 75}, 'dt': 1529553600, 'sys': {'type': 1, 'id': 4274, 'message': 0.0041, 'country': 'CO', 'sunrise': 1529578040, 'sunset': 1529622979}, 'id': 3670000, 'name': 'San Carlos', 'cod': 200}
    'Processing Record 479 | dinar, tr'
    {'coord': {'lon': 30.16, 'lat': 38.07}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 'base': 'stations', 'main': {'temp': 57.2, 'pressure': 1017, 'humidity': 93, 'temp_min': 57.2, 'temp_max': 57.2}, 'visibility': 10000, 'wind': {'speed': 2.24}, 'clouds': {'all': 20}, 'dt': 1529551200, 'sys': {'type': 1, 'id': 6081, 'message': 0.0037, 'country': 'TR', 'sunrise': 1529548607, 'sunset': 1529601933}, 'id': 316634, 'name': 'Dinar', 'cod': 200}
    'Processing Record 480 | houma, cn'
    {'coord': {'lon': 111.36, 'lat': 35.63}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 'base': 'stations', 'main': {'temp': 81.09, 'pressure': 927.1, 'humidity': 52, 'temp_min': 81.09, 'temp_max': 81.09, 'sea_level': 1019.96, 'grnd_level': 927.1}, 'wind': {'speed': 7.76, 'deg': 147.503}, 'clouds': {'all': 20}, 'dt': 1529554610, 'sys': {'message': 0.0048, 'country': 'CN', 'sunrise': 1529529548, 'sunset': 1529582010}, 'id': 1784874, 'name': 'Houma', 'cod': 200}
    'Processing Record 481 | shahr-e babak, ir'
    {'coord': {'lon': 55.12, 'lat': 30.12}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 72.72, 'pressure': 822.62, 'humidity': 20, 'temp_min': 72.72, 'temp_max': 72.72, 'sea_level': 1018.9, 'grnd_level': 822.62}, 'wind': {'speed': 5.19, 'deg': 42.0034}, 'clouds': {'all': 0}, 'dt': 1529554610, 'sys': {'message': 0.0033, 'country': 'IR', 'sunrise': 1529543918, 'sunset': 1529594639}, 'id': 115781, 'name': 'Shahr-e Babak', 'cod': 200}
    'Processing Record 482 | kisujszallas, hu'
    {'coord': {'lon': 20.77, 'lat': 47.22}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 66.78, 'pressure': 1017, 'humidity': 94, 'temp_min': 66.2, 'temp_max': 68}, 'visibility': 10000, 'wind': {'speed': 2.24, 'deg': 150}, 'clouds': {'all': 0}, 'dt': 1529552700, 'sys': {'type': 1, 'id': 5731, 'message': 0.0041, 'country': 'HU', 'sunrise': 1529548850, 'sunset': 1529606197}, 'id': 718744, 'name': 'Kisujszallas', 'cod': 200}
    'Processing Record 483 | yerbogachen, ru'
    {'coord': {'lon': 108.01, 'lat': 61.28}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 78.3, 'pressure': 976.39, 'humidity': 55, 'temp_min': 78.3, 'temp_max': 78.3, 'sea_level': 1014.16, 'grnd_level': 976.39}, 'wind': {'speed': 2.06, 'deg': 186.003}, 'clouds': {'all': 56}, 'dt': 1529554611, 'sys': {'message': 0.0039, 'country': 'RU', 'sunrise': 1529521660, 'sunset': 1529591507}, 'id': 2012956, 'name': 'Yerbogachen', 'cod': 200}
    'Processing Record 484 | qasigiannguit, gl'
    {'coord': {'lon': -51.19, 'lat': 68.82}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 51.8, 'pressure': 994, 'humidity': 43, 'temp_min': 51.8, 'temp_max': 51.8}, 'wind': {'speed': 16.11, 'deg': 110}, 'clouds': {'all': 0}, 'dt': 1529553000, 'sys': {'type': 1, 'id': 4805, 'message': 0.0039, 'country': 'GL', 'sunrise': 0, 'sunset': 0}, 'id': 3420768, 'name': 'Qasigiannguit', 'cod': 200}
    'Processing Record 485 | belaya kholunitsa, ru'
    {'coord': {'lon': 50.85, 'lat': 58.84}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'base': 'stations', 'main': {'temp': 52.92, 'pressure': 987.17, 'humidity': 84, 'temp_min': 52.92, 'temp_max': 52.92, 'sea_level': 1008.28, 'grnd_level': 987.17}, 'wind': {'speed': 16.71, 'deg': 264.503}, 'rain': {'3h': 0.325}, 'clouds': {'all': 68}, 'dt': 1529554611, 'sys': {'message': 0.003, 'country': 'RU', 'sunrise': 1529537089, 'sunset': 1529603518}, 'id': 578152, 'name': 'Belaya Kholunitsa', 'cod': 200}
    'Processing Record 486 | camacha, pt'
    {'coord': {'lon': -16.33, 'lat': 33.08}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 65.44, 'pressure': 1019, 'humidity': 88, 'temp_min': 64.4, 'temp_max': 66.2}, 'visibility': 10000, 'wind': {'speed': 12.75, 'deg': 330}, 'clouds': {'all': 75}, 'dt': 1529551800, 'sys': {'type': 1, 'id': 5960, 'message': 0.0036, 'country': 'PT', 'sunrise': 1529560617, 'sunset': 1529612241}, 'id': 2270385, 'name': 'Camacha', 'cod': 200}
    'Processing Record 487 | urumqi, cn'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for urumqi, cn**
    'Processing Record 488 | alotau, pg'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for alotau, pg**
    'Processing Record 489 | chama, zm'
    {'coord': {'lon': 33.16, 'lat': -11.22}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 53.91, 'pressure': 917.86, 'humidity': 91, 'temp_min': 53.91, 'temp_max': 53.91, 'sea_level': 1032.97, 'grnd_level': 917.86}, 'wind': {'speed': 4.85, 'deg': 109.503}, 'clouds': {'all': 0}, 'dt': 1529554611, 'sys': {'message': 0.0032, 'country': 'ZM', 'sunrise': 1529553908, 'sunset': 1529595192}, 'id': 920901, 'name': 'Chama', 'cod': 200}
    'Processing Record 490 | mayo, ca'
    {'coord': {'lon': -135.9, 'lat': 63.59}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 80.6, 'pressure': 1011, 'humidity': 26, 'temp_min': 80.6, 'temp_max': 80.6}, 'visibility': 32186, 'wind': {'speed': 3.36, 'deg': 290}, 'clouds': {'all': 90}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 3955, 'message': 0.0073, 'country': 'CA', 'sunrise': 1529577854, 'sunset': 1529652401}, 'id': 6068416, 'name': 'Mayo', 'cod': 200}
    'Processing Record 491 | dongsheng, cn'
    {'coord': {'lon': 112.52, 'lat': 29.72}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 83.43, 'pressure': 1015.38, 'humidity': 77, 'temp_min': 83.43, 'temp_max': 83.43, 'sea_level': 1018.9, 'grnd_level': 1015.38}, 'wind': {'speed': 10.89, 'deg': 91.5034}, 'clouds': {'all': 68}, 'dt': 1529554612, 'sys': {'message': 0.004, 'country': 'CN', 'sunrise': 1529530199, 'sunset': 1529580802}, 'id': 1788268, 'name': 'Dongsheng', 'cod': 200}
    'Processing Record 492 | naze, jp'
    {'coord': {'lon': 129.48, 'lat': 28.37}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 84.2, 'pressure': 1006, 'humidity': 83, 'temp_min': 84.2, 'temp_max': 84.2}, 'visibility': 10000, 'wind': {'speed': 18.34, 'deg': 220}, 'clouds': {'all': 75}, 'dt': 1529550000, 'sys': {'type': 1, 'id': 7560, 'message': 0.0032, 'country': 'JP', 'sunrise': 1529526321, 'sunset': 1529576538}, 'id': 1855540, 'name': 'Naze', 'cod': 200}
    'Processing Record 493 | constitucion, mx'
    {'coord': {'lon': -104.67, 'lat': 23.99}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 77, 'pressure': 1019, 'humidity': 33, 'temp_min': 77, 'temp_max': 77}, 'visibility': 16093, 'wind': {'speed': 5.82, 'deg': 60}, 'clouds': {'all': 5}, 'dt': 1529549160, 'sys': {'type': 1, 'id': 3983, 'message': 0.0041, 'country': 'MX', 'sunrise': 1529583117, 'sunset': 1529632150}, 'id': 4011743, 'name': 'Constitucion', 'cod': 200}
    'Processing Record 494 | zhanatas, kz'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for zhanatas, kz**
    'Processing Record 495 | geraldton, au'
    {'coord': {'lon': 114.6, 'lat': -28.77}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 68, 'pressure': 1028, 'humidity': 52, 'temp_min': 68, 'temp_max': 68}, 'visibility': 10000, 'wind': {'speed': 9.17, 'deg': 40}, 'clouds': {'all': 0}, 'dt': 1529551800, 'sys': {'type': 1, 'id': 8186, 'message': 0.0038, 'country': 'AU', 'sunrise': 1529536448, 'sunset': 1529573555}, 'id': 2070998, 'name': 'Geraldton', 'cod': 200}
    'Processing Record 496 | guerrero negro, mx'
    {'coord': {'lon': -114.04, 'lat': 27.97}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 'base': 'stations', 'main': {'temp': 63.27, 'pressure': 1014.24, 'humidity': 86, 'temp_min': 63.27, 'temp_max': 63.27, 'sea_level': 1025.51, 'grnd_level': 1014.24}, 'wind': {'speed': 8.99, 'deg': 314.003}, 'clouds': {'all': 0}, 'dt': 1529554521, 'sys': {'message': 0.0038, 'country': 'MX', 'sunrise': 1529584831, 'sunset': 1529634935}, 'id': 4021858, 'name': 'Guerrero Negro', 'cod': 200}
    'Processing Record 497 | weiser, us'
    {'coord': {'lon': -116.97, 'lat': 44.25}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02n'}], 'base': 'stations', 'main': {'temp': 75.2, 'pressure': 1013, 'humidity': 38, 'temp_min': 75.2, 'temp_max': 75.2}, 'visibility': 16093, 'wind': {'speed': 9.17, 'deg': 360, 'gust': 9.8}, 'clouds': {'all': 20}, 'dt': 1529551440, 'sys': {'type': 1, 'id': 2303, 'message': 0.0038, 'country': 'US', 'sunrise': 1529582650, 'sunset': 1529638522}, 'id': 5611730, 'name': 'Weiser', 'cod': 200}
    'Processing Record 498 | jyvaskyla, fi'
    {'cod': '404', 'message': 'city not found'}
    **Weather data does not exist for jyvaskyla, fi**
    'Processing Record 499 | tazovskiy, ru'
    {'coord': {'lon': 78.7, 'lat': 67.47}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 'base': 'stations', 'main': {'temp': 65.97, 'pressure': 1000.95, 'humidity': 72, 'temp_min': 65.97, 'temp_max': 65.97, 'sea_level': 1004.35, 'grnd_level': 1000.95}, 'wind': {'speed': 15.7, 'deg': 122.003}, 'clouds': {'all': 12}, 'dt': 1529554837, 'sys': {'message': 0.0047, 'country': 'RU', 'sunrise': 0, 'sunset': 0}, 'id': 1489853, 'name': 'Tazovskiy', 'cod': 200}
    'Processing Record 500 | deputatskiy, ru'
    {'coord': {'lon': 139.9, 'lat': 69.3}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 70.56, 'pressure': 957.02, 'humidity': 23, 'temp_min': 70.56, 'temp_max': 70.56, 'sea_level': 1019.31, 'grnd_level': 957.02}, 'wind': {'speed': 8.66, 'deg': 140.003}, 'clouds': {'all': 0}, 'dt': 1529554613, 'sys': {'message': 0.0036, 'country': 'RU', 'sunrise': 0, 'sunset': 0}, 'id': 2028164, 'name': 'Deputatskiy', 'cod': 200}
    ---------------------------
    Data Retrieval Complete
    ---------------------------
    


```python
list_of_cities
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>City</th>
      <th>Country</th>
      <th>Cloudiness</th>
      <th>Humidity</th>
      <th>Latitude</th>
      <th>Longitude</th>
      <th>Temperature</th>
      <th>Wind Speed</th>
      <th>Date</th>
      <th>Max Temperature</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>port macquarie</td>
      <td>au</td>
      <td>90</td>
      <td>72</td>
      <td>-31.43</td>
      <td>152.91</td>
      <td></td>
      <td>5.82</td>
      <td>1529553600</td>
      <td>60.80</td>
    </tr>
    <tr>
      <th>1</th>
      <td>saint-philippe</td>
      <td>re</td>
      <td>75</td>
      <td>53</td>
      <td>-21.36</td>
      <td>55.77</td>
      <td></td>
      <td>8.05</td>
      <td>1529551800</td>
      <td>68.22</td>
    </tr>
    <tr>
      <th>2</th>
      <td>tubuala</td>
      <td>pa</td>
      <td>40</td>
      <td>88</td>
      <td>9.52</td>
      <td>-79.03</td>
      <td></td>
      <td>4.7</td>
      <td>1529553600</td>
      <td>77.00</td>
    </tr>
    <tr>
      <th>3</th>
      <td>torbay</td>
      <td>ca</td>
      <td>90</td>
      <td>71</td>
      <td>47.66</td>
      <td>-52.73</td>
      <td></td>
      <td>20.8</td>
      <td>1529550000</td>
      <td>51.80</td>
    </tr>
    <tr>
      <th>4</th>
      <td>de aar</td>
      <td>za</td>
      <td>0</td>
      <td>79</td>
      <td>-30.65</td>
      <td>24.01</td>
      <td></td>
      <td>5.64</td>
      <td>1529554542</td>
      <td>32.76</td>
    </tr>
    <tr>
      <th>5</th>
      <td>rikitea</td>
      <td>pf</td>
      <td>32</td>
      <td>100</td>
      <td>-23.12</td>
      <td>-134.97</td>
      <td></td>
      <td>6.98</td>
      <td>1529554542</td>
      <td>73.80</td>
    </tr>
    <tr>
      <th>6</th>
      <td>otradnoye</td>
      <td>ru</td>
      <td>0</td>
      <td>66</td>
      <td>59.77</td>
      <td>30.8</td>
      <td></td>
      <td>6.71</td>
      <td>1529551800</td>
      <td>55.40</td>
    </tr>
    <tr>
      <th>7</th>
      <td>kapaa</td>
      <td>us</td>
      <td>40</td>
      <td>74</td>
      <td>22.08</td>
      <td>-159.32</td>
      <td></td>
      <td>9.17</td>
      <td>1529553360</td>
      <td>80.60</td>
    </tr>
    <tr>
      <th>8</th>
      <td>ushuaia</td>
      <td>ar</td>
      <td>90</td>
      <td>92</td>
      <td>-54.81</td>
      <td>-68.31</td>
      <td></td>
      <td>17.22</td>
      <td>1529553600</td>
      <td>30.20</td>
    </tr>
    <tr>
      <th>9</th>
      <td>labutta</td>
      <td>mm</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>10</th>
      <td>puerto ayora</td>
      <td>ec</td>
      <td>20</td>
      <td>100</td>
      <td>-0.74</td>
      <td>-90.35</td>
      <td></td>
      <td>11.45</td>
      <td>1529554357</td>
      <td>71.37</td>
    </tr>
    <tr>
      <th>11</th>
      <td>coquimbo</td>
      <td>cl</td>
      <td>24</td>
      <td>100</td>
      <td>-29.95</td>
      <td>-71.34</td>
      <td></td>
      <td>3.36</td>
      <td>1529553600</td>
      <td>44.60</td>
    </tr>
    <tr>
      <th>12</th>
      <td>nkowakowa</td>
      <td>za</td>
      <td>88</td>
      <td>97</td>
      <td>-23.89</td>
      <td>30.29</td>
      <td></td>
      <td>0.94</td>
      <td>1529554543</td>
      <td>50.67</td>
    </tr>
    <tr>
      <th>13</th>
      <td>ust-kamchatsk</td>
      <td>ru</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>14</th>
      <td>cape town</td>
      <td>za</td>
      <td>0</td>
      <td>93</td>
      <td>-33.93</td>
      <td>18.42</td>
      <td></td>
      <td>4.7</td>
      <td>1529550000</td>
      <td>42.80</td>
    </tr>
    <tr>
      <th>15</th>
      <td>east london</td>
      <td>za</td>
      <td>0</td>
      <td>71</td>
      <td>-33.02</td>
      <td>27.91</td>
      <td></td>
      <td>9.17</td>
      <td>1529550000</td>
      <td>55.40</td>
    </tr>
    <tr>
      <th>16</th>
      <td>saint-denis</td>
      <td>re</td>
      <td>75</td>
      <td>53</td>
      <td>-20.87</td>
      <td>55.47</td>
      <td></td>
      <td>8.05</td>
      <td>1529551800</td>
      <td>68.88</td>
    </tr>
    <tr>
      <th>17</th>
      <td>havre-saint-pierre</td>
      <td>ca</td>
      <td>40</td>
      <td>93</td>
      <td>50.23</td>
      <td>-63.6</td>
      <td></td>
      <td>3.36</td>
      <td>1529550000</td>
      <td>50.00</td>
    </tr>
    <tr>
      <th>18</th>
      <td>atuona</td>
      <td>pf</td>
      <td>48</td>
      <td>100</td>
      <td>-9.8</td>
      <td>-139.03</td>
      <td></td>
      <td>11.79</td>
      <td>1529554544</td>
      <td>80.91</td>
    </tr>
    <tr>
      <th>19</th>
      <td>vostok</td>
      <td>ru</td>
      <td>92</td>
      <td>100</td>
      <td>46.45</td>
      <td>135.83</td>
      <td></td>
      <td>2.73</td>
      <td>1529554544</td>
      <td>56.34</td>
    </tr>
    <tr>
      <th>20</th>
      <td>llanes</td>
      <td>es</td>
      <td>36</td>
      <td>97</td>
      <td>43.42</td>
      <td>-4.75</td>
      <td></td>
      <td>0.83</td>
      <td>1529554544</td>
      <td>57.33</td>
    </tr>
    <tr>
      <th>21</th>
      <td>mys shmidta</td>
      <td>ru</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>22</th>
      <td>saint-augustin</td>
      <td>ca</td>
      <td>75</td>
      <td>77</td>
      <td>45.63</td>
      <td>-73.98</td>
      <td></td>
      <td>3.36</td>
      <td>1529550000</td>
      <td>65.71</td>
    </tr>
    <tr>
      <th>23</th>
      <td>dagda</td>
      <td>lv</td>
      <td>0</td>
      <td>76</td>
      <td>56.09</td>
      <td>27.54</td>
      <td></td>
      <td>11.68</td>
      <td>1529554545</td>
      <td>57.96</td>
    </tr>
    <tr>
      <th>24</th>
      <td>safakulevo</td>
      <td>ru</td>
      <td>0</td>
      <td>64</td>
      <td>54.99</td>
      <td>62.54</td>
      <td></td>
      <td>18.61</td>
      <td>1529554545</td>
      <td>61.74</td>
    </tr>
    <tr>
      <th>25</th>
      <td>castro</td>
      <td>cl</td>
      <td>88</td>
      <td>86</td>
      <td>-42.48</td>
      <td>-73.76</td>
      <td></td>
      <td>11.56</td>
      <td>1529554545</td>
      <td>45.36</td>
    </tr>
    <tr>
      <th>26</th>
      <td>manchar</td>
      <td>in</td>
      <td>92</td>
      <td>96</td>
      <td>19</td>
      <td>73.94</td>
      <td></td>
      <td>4.97</td>
      <td>1529554545</td>
      <td>75.24</td>
    </tr>
    <tr>
      <th>27</th>
      <td>busselton</td>
      <td>au</td>
      <td>92</td>
      <td>100</td>
      <td>-33.64</td>
      <td>115.35</td>
      <td></td>
      <td>11.56</td>
      <td>1529554545</td>
      <td>62.19</td>
    </tr>
    <tr>
      <th>28</th>
      <td>georgetown</td>
      <td>sh</td>
      <td>44</td>
      <td>100</td>
      <td>-7.93</td>
      <td>-14.42</td>
      <td></td>
      <td>16.49</td>
      <td>1529554497</td>
      <td>76.50</td>
    </tr>
    <tr>
      <th>29</th>
      <td>faanui</td>
      <td>pf</td>
      <td>88</td>
      <td>99</td>
      <td>-16.48</td>
      <td>-151.75</td>
      <td></td>
      <td>16.71</td>
      <td>1529554546</td>
      <td>81.27</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>470</th>
      <td>upernavik</td>
      <td>gl</td>
      <td>88</td>
      <td>95</td>
      <td>72.79</td>
      <td>-56.15</td>
      <td></td>
      <td>10.89</td>
      <td>1529554486</td>
      <td>32.58</td>
    </tr>
    <tr>
      <th>471</th>
      <td>preobrazheniye</td>
      <td>ru</td>
      <td>68</td>
      <td>88</td>
      <td>42.9</td>
      <td>133.91</td>
      <td></td>
      <td>2.62</td>
      <td>1529554608</td>
      <td>61.83</td>
    </tr>
    <tr>
      <th>472</th>
      <td>smolenka</td>
      <td>ru</td>
      <td>0</td>
      <td>72</td>
      <td>54.28</td>
      <td>56.05</td>
      <td></td>
      <td>13.42</td>
      <td>1529551800</td>
      <td>60.80</td>
    </tr>
    <tr>
      <th>473</th>
      <td>jalingo</td>
      <td>ng</td>
      <td>92</td>
      <td>98</td>
      <td>10.3</td>
      <td>10.93</td>
      <td></td>
      <td>9.66</td>
      <td>1529554609</td>
      <td>68.76</td>
    </tr>
    <tr>
      <th>474</th>
      <td>ferkessedougou</td>
      <td>ci</td>
      <td>76</td>
      <td>87</td>
      <td>9.6</td>
      <td>-5.2</td>
      <td></td>
      <td>6.98</td>
      <td>1529554609</td>
      <td>73.53</td>
    </tr>
    <tr>
      <th>475</th>
      <td>jiangyou</td>
      <td>cn</td>
      <td>100</td>
      <td>97</td>
      <td>31.78</td>
      <td>104.73</td>
      <td></td>
      <td>4.97</td>
      <td>1529554609</td>
      <td>72.09</td>
    </tr>
    <tr>
      <th>476</th>
      <td>havoysund</td>
      <td>no</td>
      <td>90</td>
      <td>100</td>
      <td>71</td>
      <td>24.66</td>
      <td></td>
      <td>8.05</td>
      <td>1529553000</td>
      <td>44.60</td>
    </tr>
    <tr>
      <th>477</th>
      <td>san carlos</td>
      <td>co</td>
      <td>75</td>
      <td>93</td>
      <td>6.19</td>
      <td>-74.99</td>
      <td></td>
      <td>1.61</td>
      <td>1529553600</td>
      <td>59.00</td>
    </tr>
    <tr>
      <th>478</th>
      <td>dinar</td>
      <td>tr</td>
      <td>20</td>
      <td>93</td>
      <td>38.07</td>
      <td>30.16</td>
      <td></td>
      <td>2.24</td>
      <td>1529551200</td>
      <td>57.20</td>
    </tr>
    <tr>
      <th>479</th>
      <td>houma</td>
      <td>cn</td>
      <td>20</td>
      <td>52</td>
      <td>35.63</td>
      <td>111.36</td>
      <td></td>
      <td>7.76</td>
      <td>1529554610</td>
      <td>81.09</td>
    </tr>
    <tr>
      <th>480</th>
      <td>shahr-e babak</td>
      <td>ir</td>
      <td>0</td>
      <td>20</td>
      <td>30.12</td>
      <td>55.12</td>
      <td></td>
      <td>5.19</td>
      <td>1529554610</td>
      <td>72.72</td>
    </tr>
    <tr>
      <th>481</th>
      <td>kisujszallas</td>
      <td>hu</td>
      <td>0</td>
      <td>94</td>
      <td>47.22</td>
      <td>20.77</td>
      <td></td>
      <td>2.24</td>
      <td>1529552700</td>
      <td>66.78</td>
    </tr>
    <tr>
      <th>482</th>
      <td>yerbogachen</td>
      <td>ru</td>
      <td>56</td>
      <td>55</td>
      <td>61.28</td>
      <td>108.01</td>
      <td></td>
      <td>2.06</td>
      <td>1529554611</td>
      <td>78.30</td>
    </tr>
    <tr>
      <th>483</th>
      <td>qasigiannguit</td>
      <td>gl</td>
      <td>0</td>
      <td>43</td>
      <td>68.82</td>
      <td>-51.19</td>
      <td></td>
      <td>16.11</td>
      <td>1529553000</td>
      <td>51.80</td>
    </tr>
    <tr>
      <th>484</th>
      <td>belaya kholunitsa</td>
      <td>ru</td>
      <td>68</td>
      <td>84</td>
      <td>58.84</td>
      <td>50.85</td>
      <td></td>
      <td>16.71</td>
      <td>1529554611</td>
      <td>52.92</td>
    </tr>
    <tr>
      <th>485</th>
      <td>camacha</td>
      <td>pt</td>
      <td>75</td>
      <td>88</td>
      <td>33.08</td>
      <td>-16.33</td>
      <td></td>
      <td>12.75</td>
      <td>1529551800</td>
      <td>65.44</td>
    </tr>
    <tr>
      <th>486</th>
      <td>urumqi</td>
      <td>cn</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>487</th>
      <td>alotau</td>
      <td>pg</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>488</th>
      <td>chama</td>
      <td>zm</td>
      <td>0</td>
      <td>91</td>
      <td>-11.22</td>
      <td>33.16</td>
      <td></td>
      <td>4.85</td>
      <td>1529554611</td>
      <td>53.91</td>
    </tr>
    <tr>
      <th>489</th>
      <td>mayo</td>
      <td>ca</td>
      <td>90</td>
      <td>26</td>
      <td>63.59</td>
      <td>-135.9</td>
      <td></td>
      <td>3.36</td>
      <td>1529550000</td>
      <td>80.60</td>
    </tr>
    <tr>
      <th>490</th>
      <td>dongsheng</td>
      <td>cn</td>
      <td>68</td>
      <td>77</td>
      <td>29.72</td>
      <td>112.52</td>
      <td></td>
      <td>10.89</td>
      <td>1529554612</td>
      <td>83.43</td>
    </tr>
    <tr>
      <th>491</th>
      <td>naze</td>
      <td>jp</td>
      <td>75</td>
      <td>83</td>
      <td>28.37</td>
      <td>129.48</td>
      <td></td>
      <td>18.34</td>
      <td>1529550000</td>
      <td>84.20</td>
    </tr>
    <tr>
      <th>492</th>
      <td>constitucion</td>
      <td>mx</td>
      <td>5</td>
      <td>33</td>
      <td>23.99</td>
      <td>-104.67</td>
      <td></td>
      <td>5.82</td>
      <td>1529549160</td>
      <td>77.00</td>
    </tr>
    <tr>
      <th>493</th>
      <td>zhanatas</td>
      <td>kz</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>494</th>
      <td>geraldton</td>
      <td>au</td>
      <td>0</td>
      <td>52</td>
      <td>-28.77</td>
      <td>114.6</td>
      <td></td>
      <td>9.17</td>
      <td>1529551800</td>
      <td>68.00</td>
    </tr>
    <tr>
      <th>495</th>
      <td>guerrero negro</td>
      <td>mx</td>
      <td>0</td>
      <td>86</td>
      <td>27.97</td>
      <td>-114.04</td>
      <td></td>
      <td>8.99</td>
      <td>1529554521</td>
      <td>63.27</td>
    </tr>
    <tr>
      <th>496</th>
      <td>weiser</td>
      <td>us</td>
      <td>20</td>
      <td>38</td>
      <td>44.25</td>
      <td>-116.97</td>
      <td></td>
      <td>9.17</td>
      <td>1529551440</td>
      <td>75.20</td>
    </tr>
    <tr>
      <th>497</th>
      <td>jyvaskyla</td>
      <td>fi</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>498</th>
      <td>tazovskiy</td>
      <td>ru</td>
      <td>12</td>
      <td>72</td>
      <td>67.47</td>
      <td>78.7</td>
      <td></td>
      <td>15.7</td>
      <td>1529554012</td>
      <td>65.97</td>
    </tr>
    <tr>
      <th>499</th>
      <td>deputatskiy</td>
      <td>ru</td>
      <td>0</td>
      <td>23</td>
      <td>69.3</td>
      <td>139.9</td>
      <td></td>
      <td>8.66</td>
      <td>1529554613</td>
      <td>70.56</td>
    </tr>
  </tbody>
</table>
<p>500 rows × 10 columns</p>
</div>




```python
list_of_cities.to_csv("500cities_weatherdata.csv", index=False)
```

# Latitude Vs Temperature Plot


```python
# Temperature (F) vs. Latitude
date = list_of_cities['Date'][0]
# cocnvert date to readable form
convert_date = datetime.date(datetime.utcfromtimestamp(date))

Latitude = pd.to_numeric(list_of_cities["Latitude"])
Temp = pd.to_numeric(list_of_cities["Max Temperature"])

plt.title(f"City Latitude vs Max Temperature ({convert_date})")

plt.xlabel("Latitude")
plt.ylabel("Max Temperature (F)")
plt.scatter(x=Latitude, y=Temp, color="blue", alpha=0.75, edgecolor="black")
plt.grid(b=True, which='major', color='w', linewidth=1.0)
plt.grid(b=True, which='minor', color='w', linewidth=0.5)
sns.set_style("dark")
plt.show()
plt.savefig("Images/LatVsTemp.png")
```


![png](output_15_0.png)



    <matplotlib.figure.Figure at 0x2e64c37ca90>


# Latitude vs. Humidity


```python
humidity = list_of_cities["Humidity"]

plt.title(f"City Latitude vs Humidity  ({convert_date})")

plt.xlabel("Latitude")
plt.ylabel("Humidity %")
plt.scatter(x=Latitude, y=humidity, color="blue", alpha=0.75, edgecolor="black")
plt.grid(b=True, which='major', color='w', linewidth=1.0)
plt.grid(b=True, which='minor', color='w', linewidth=0.5)
sns.set_style("dark")
plt.show()
plt.savefig("Images/LatVsHumidity.png")
```


![png](output_17_0.png)



    <matplotlib.figure.Figure at 0x2e64c7b10f0>


# Latitude Vs Cloudiness


```python
cloudiness = list_of_cities['Cloudiness']
plt.title(f"City Latitude vs Cloudiness  ({convert_date})")

plt.xlabel("Latitude")
plt.ylabel("Cloudiness (%)")
plt.scatter(x=Latitude, y=cloudiness, color="blue", alpha=0.75, edgecolor="black")
plt.grid(b=True, which='major', color='w', linewidth=1.0)
plt.grid(b=True, which='minor', color='w', linewidth=0.5)
sns.set_style("dark")
plt.show()
plt.savefig("Images/LatVscloud.png")
```


![png](output_19_0.png)



    <matplotlib.figure.Figure at 0x2e64c8b4ef0>


# Latitude vs. Wind Speed Plot


```python
wind_speed = list_of_cities["Wind Speed"]

plt.title(f"City Latitude vs Wind Speed ({convert_date})")

plt.xlabel("Latitude")
plt.ylabel("Wind Speed (mph)")
plt.scatter(x=Latitude, y=wind_speed, color="blue", alpha=0.75, edgecolor="black")
plt.grid(b=True, which='major', color='w', linewidth=1.0)
plt.grid(b=True, which='minor', color='w', linewidth=0.5)
sns.set_style("dark")
plt.show()
plt.savefig("Images/LatVsWindSpd.png")
```


![png](output_21_0.png)



    <matplotlib.figure.Figure at 0x2e64c7f0e48>

