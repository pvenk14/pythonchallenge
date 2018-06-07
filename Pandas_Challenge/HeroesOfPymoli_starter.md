
### Heroes Of Pymoli Data Analysis
* Of the 1163 active players, the vast majority are male (84%). There also exists, a smaller, but notable proportion of female players (14%).

* Our peak age demographic falls between 20-24 (44.8%) with secondary groups falling between 15-19 (18.60%) and 25-29 (13.4%).  
-----

### Note
* Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.


```python
# Dependencies and Setup
import pandas as pd
import numpy as np

# Raw data file
file_to_load = "Resources/purchase_data.csv"

# Read purchasing file and store into pandas data frame
purchase_data = pd.read_csv(file_to_load)
purchase_data.head()
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
      <th>Purchase ID</th>
      <th>SN</th>
      <th>Age</th>
      <th>Gender</th>
      <th>Item ID</th>
      <th>Item Name</th>
      <th>Price</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>Lisim78</td>
      <td>20</td>
      <td>Male</td>
      <td>108</td>
      <td>Extraction, Quickblade Of Trembling Hands</td>
      <td>$3.53</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>Lisovynya38</td>
      <td>40</td>
      <td>Male</td>
      <td>143</td>
      <td>Frenzied Scimitar</td>
      <td>$1.56</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>Ithergue48</td>
      <td>24</td>
      <td>Male</td>
      <td>92</td>
      <td>Final Critic</td>
      <td>$4.88</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>Chamassasya86</td>
      <td>24</td>
      <td>Male</td>
      <td>100</td>
      <td>Blindscythe</td>
      <td>$3.27</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>Iskosia90</td>
      <td>23</td>
      <td>Male</td>
      <td>131</td>
      <td>Fury</td>
      <td>$1.44</td>
    </tr>
  </tbody>
</table>
</div>



## Player Count

* Display the total number of players



```python
player_count = len(purchase_data["SN"].unique())
totalplayers_table = pd.DataFrame({"Total players": player_count}, index=[0])
totalplayers_table


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
      <th>Total players</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>576</td>
    </tr>
  </tbody>
</table>
</div>



## Purchasing Analysis (Total)

* Run basic calculations to obtain number of unique items, average price, etc.


* Create a summary data frame to hold the results


* Optional: give the displayed data cleaner formatting


* Display the summary data frame



```python
unique_items = len(purchase_data["Item ID"].value_counts())
avg_price = purchase_data["Price"].mean()
number_of_purchases = len(purchase_data["Purchase ID"].value_counts())
Total_revenue = purchase_data["Price"].sum()
pd.options.display.float_format = '${:,.2f}'.format
Summary_table = pd.DataFrame({"Number Of Unique Items": unique_items,
                              "Average Price": avg_price,
                              "Number of Purchases":number_of_purchases,
                              "Total Revenue": Total_revenue}, index=[0])
Summary_table
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
      <th>Average Price</th>
      <th>Number Of Unique Items</th>
      <th>Number of Purchases</th>
      <th>Total Revenue</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>$3.05</td>
      <td>183</td>
      <td>780</td>
      <td>$2,379.77</td>
    </tr>
  </tbody>
</table>
</div>



## Gender Demographics

* Run basic calculations to obtain number of unique items, average price, etc.


* Create a summary data frame to hold the results


* Optional: give the displayed data cleaner formatting


* Display the summary data frame



```python
gender_value = purchase_data["Gender"].value_counts()
gender_percent = (gender_value/player_count)*100
pd.options.display.float_format = '{:,.2f}'.format
Gender_demo = pd.DataFrame({"Total players": gender_value,
                              "Percent of Total Players": gender_percent})
Gender_demo

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
      <th>Percent of Total Players</th>
      <th>Total players</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Male</th>
      <td>113.19</td>
      <td>652</td>
    </tr>
    <tr>
      <th>Female</th>
      <td>19.62</td>
      <td>113</td>
    </tr>
    <tr>
      <th>Other / Non-Disclosed</th>
      <td>2.60</td>
      <td>15</td>
    </tr>
  </tbody>
</table>
</div>




## Purchasing Analysis (Gender)

* Run basic calculations to obtain purchase count, avg. purchase price, etc. by gender


* For normalized purchasing, divide total purchase value by purchase count, by gender


* Create a summary data frame to hold the results


* Optional: give the displayed data cleaner formatting


* Display the summary data frame


```python
grouped_gender_df = purchase_data.groupby(['Gender'])
purchase_count = purchase_data['Gender'].value_counts()

avg_price= grouped_gender_df["Price"].mean()

Total_purchase = grouped_gender_df["Price"].sum()

Normalized_total = Total_purchase/purchase_count

pd.options.display.float_format = '${:,.2f}'.format
purchasing_analysis = pd.DataFrame({"Purchase Count": purchase_count,
                              "Avg Purchase Price": avg_price,
                              "Total Purchase Value": Total_purchase,
                               "Normalized_total": Normalized_total})
purchasing_analysis

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
      <th>Avg Purchase Price</th>
      <th>Normalized_total</th>
      <th>Purchase Count</th>
      <th>Total Purchase Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Female</th>
      <td>$3.20</td>
      <td>$3.20</td>
      <td>113</td>
      <td>$361.94</td>
    </tr>
    <tr>
      <th>Male</th>
      <td>$3.02</td>
      <td>$3.02</td>
      <td>652</td>
      <td>$1,967.64</td>
    </tr>
    <tr>
      <th>Other / Non-Disclosed</th>
      <td>$3.35</td>
      <td>$3.35</td>
      <td>15</td>
      <td>$50.19</td>
    </tr>
  </tbody>
</table>
</div>



## Age Demographics

* Establish bins for ages


* Categorize the existing players using the age bins. Hint: use pd.cut()


* Calculate the numbers and percentages by age group


* Create a summary data frame to hold the results


* Optional: round the percentage column to two decimal points


* Display Age Demographics Table



```python
# Establish bins for ages
age_bins = [0, 9.90, 14.90, 19.90, 24.90, 29.90, 34.90, 39.90,9999]
group_names = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]
age_demo = pd.DataFrame(purchase_data["Age"])
total_players = len(purchase_data["SN"].value_counts())
age_demo["Age Label"] = pd.cut(age_demo["Age"], age_bins, labels=group_names)
age_group = age_demo.groupby("Age Label")
df_new= pd.DataFrame(age_group["Age Label"].count())
df_new.index.name =''
df_new.columns =["Total Count"]
pd.options.display.float_format = '{:,.2f}'.format
df_new["Percentage of Players"] = (df_new["Total Count"]/total_players)*100
df_new.head()
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
      <th>Total Count</th>
      <th>Percentage of Players</th>
    </tr>
    <tr>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>&lt;10</th>
      <td>23</td>
      <td>3.99</td>
    </tr>
    <tr>
      <th>10-14</th>
      <td>28</td>
      <td>4.86</td>
    </tr>
    <tr>
      <th>15-19</th>
      <td>136</td>
      <td>23.61</td>
    </tr>
    <tr>
      <th>20-24</th>
      <td>365</td>
      <td>63.37</td>
    </tr>
    <tr>
      <th>25-29</th>
      <td>101</td>
      <td>17.53</td>
    </tr>
  </tbody>
</table>
</div>



## Purchasing Analysis (Age)

* Bin the purchase_data data frame by age


* Run basic calculations to obtain purchase count, avg. purchase price, etc. in the table below


* Calculate Normalized Purchasing


* Create a summary data frame to hold the results


* Optional: give the displayed data cleaner formatting


* Display the summary data frame


```python
purchasing_analysis = pd.DataFrame(purchase_data["Age"])
purchasing_analysis ["Age Label"] = pd.cut(purchasing_analysis["Age"], age_bins, labels=group_names)
purchase_grp = purchasing_analysis.groupby(["Age Label"])
purchase_grp= pd.DataFrame(purchase_grp["Age Label"].count())
purchase_grp.columns =["Purchase Count"]
purchase_grp.index.name =' '

group_by_age = purchase_data.groupby("Age Label")
purchase_grp["Average Purchase Price"] = group_by_age["Price"].mean() 
purchase_grp["Total Purchase Value"] = group_by_age["Price"].sum()
purchase_grp["Normalized Totals"] = purchase_grp["Average Purchase Price"]/purchase_grp["Total Purchase Value"]
pd.options.display.float_format = '${:,.2f}'.format
purchase_grp

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
      <th>Purchase Count</th>
      <th>Average Purchase Price</th>
      <th>Total Purchase Value</th>
      <th>Normalized Totals</th>
    </tr>
    <tr>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>&lt;10</th>
      <td>23</td>
      <td>$3.35</td>
      <td>$77.13</td>
      <td>$0.04</td>
    </tr>
    <tr>
      <th>10-14</th>
      <td>28</td>
      <td>$2.96</td>
      <td>$82.78</td>
      <td>$0.04</td>
    </tr>
    <tr>
      <th>15-19</th>
      <td>136</td>
      <td>$3.04</td>
      <td>$412.89</td>
      <td>$0.01</td>
    </tr>
    <tr>
      <th>20-24</th>
      <td>365</td>
      <td>$3.05</td>
      <td>$1,114.06</td>
      <td>$0.00</td>
    </tr>
    <tr>
      <th>25-29</th>
      <td>101</td>
      <td>$2.90</td>
      <td>$293.00</td>
      <td>$0.01</td>
    </tr>
    <tr>
      <th>30-34</th>
      <td>73</td>
      <td>$2.93</td>
      <td>$214.00</td>
      <td>$0.01</td>
    </tr>
    <tr>
      <th>35-39</th>
      <td>41</td>
      <td>$3.60</td>
      <td>$147.67</td>
      <td>$0.02</td>
    </tr>
    <tr>
      <th>40+</th>
      <td>13</td>
      <td>$2.94</td>
      <td>$38.24</td>
      <td>$0.08</td>
    </tr>
  </tbody>
</table>
</div>



## Top Spenders

* Run basic calculations to obtain the results in the table below


* Create a summary data frame to hold the results


* Sort the total purchase value column in descending order


* Optional: give the displayed data cleaner formatting


* Display a preview of the summary data frame




```python
top_spenders = purchase_data.groupby("SN")
purchase_count = top_spenders["SN"].count()
Avg_purchase_price = top_spenders["Price"].mean()
Total_purchase_price =top_spenders["Price"].sum()
top_spenders_table = pd.DataFrame({"Purchase Count": purchase_count,
                                    "Average Purchase Price": Avg_purchase_price,
                                  "Total Purchase Value" : Total_purchase_price})
top_spenders_table = top_spenders_table.sort_values("Total Purchase Value", ascending=False)
top_spenders_table
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
      <th>Average Purchase Price</th>
      <th>Purchase Count</th>
      <th>Total Purchase Value</th>
    </tr>
    <tr>
      <th>SN</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Lisosia93</th>
      <td>$3.79</td>
      <td>5</td>
      <td>$18.96</td>
    </tr>
    <tr>
      <th>Idastidru52</th>
      <td>$3.86</td>
      <td>4</td>
      <td>$15.45</td>
    </tr>
    <tr>
      <th>Chamjask73</th>
      <td>$4.61</td>
      <td>3</td>
      <td>$13.83</td>
    </tr>
    <tr>
      <th>Iral74</th>
      <td>$3.40</td>
      <td>4</td>
      <td>$13.62</td>
    </tr>
    <tr>
      <th>Iskadarya95</th>
      <td>$4.37</td>
      <td>3</td>
      <td>$13.10</td>
    </tr>
    <tr>
      <th>Ilarin91</th>
      <td>$4.23</td>
      <td>3</td>
      <td>$12.70</td>
    </tr>
    <tr>
      <th>Ialallo29</th>
      <td>$3.95</td>
      <td>3</td>
      <td>$11.84</td>
    </tr>
    <tr>
      <th>Tyidaim51</th>
      <td>$3.94</td>
      <td>3</td>
      <td>$11.83</td>
    </tr>
    <tr>
      <th>Lassilsala30</th>
      <td>$3.84</td>
      <td>3</td>
      <td>$11.51</td>
    </tr>
    <tr>
      <th>Chadolyla44</th>
      <td>$3.82</td>
      <td>3</td>
      <td>$11.46</td>
    </tr>
    <tr>
      <th>Iri67</th>
      <td>$3.79</td>
      <td>3</td>
      <td>$11.37</td>
    </tr>
    <tr>
      <th>Inguron55</th>
      <td>$3.70</td>
      <td>3</td>
      <td>$11.11</td>
    </tr>
    <tr>
      <th>Siallylis44</th>
      <td>$3.46</td>
      <td>3</td>
      <td>$10.37</td>
    </tr>
    <tr>
      <th>Saistyphos30</th>
      <td>$3.44</td>
      <td>3</td>
      <td>$10.33</td>
    </tr>
    <tr>
      <th>Phyali88</th>
      <td>$3.43</td>
      <td>3</td>
      <td>$10.30</td>
    </tr>
    <tr>
      <th>Strithenu87</th>
      <td>$3.39</td>
      <td>3</td>
      <td>$10.18</td>
    </tr>
    <tr>
      <th>Lisim78</th>
      <td>$3.34</td>
      <td>3</td>
      <td>$10.02</td>
    </tr>
    <tr>
      <th>Haillyrgue51</th>
      <td>$3.17</td>
      <td>3</td>
      <td>$9.50</td>
    </tr>
    <tr>
      <th>Phistym51</th>
      <td>$4.75</td>
      <td>2</td>
      <td>$9.50</td>
    </tr>
    <tr>
      <th>Lamil79</th>
      <td>$4.64</td>
      <td>2</td>
      <td>$9.29</td>
    </tr>
    <tr>
      <th>Aina42</th>
      <td>$3.07</td>
      <td>3</td>
      <td>$9.22</td>
    </tr>
    <tr>
      <th>Saesrideu94</th>
      <td>$4.59</td>
      <td>2</td>
      <td>$9.18</td>
    </tr>
    <tr>
      <th>Arin32</th>
      <td>$4.54</td>
      <td>2</td>
      <td>$9.09</td>
    </tr>
    <tr>
      <th>Rarallo90</th>
      <td>$3.02</td>
      <td>3</td>
      <td>$9.05</td>
    </tr>
    <tr>
      <th>Baelollodeu94</th>
      <td>$4.51</td>
      <td>2</td>
      <td>$9.03</td>
    </tr>
    <tr>
      <th>Aelin32</th>
      <td>$2.99</td>
      <td>3</td>
      <td>$8.98</td>
    </tr>
    <tr>
      <th>Lisopela58</th>
      <td>$2.95</td>
      <td>3</td>
      <td>$8.86</td>
    </tr>
    <tr>
      <th>Saedaiphos46</th>
      <td>$2.94</td>
      <td>3</td>
      <td>$8.83</td>
    </tr>
    <tr>
      <th>Reunasu60</th>
      <td>$4.41</td>
      <td>2</td>
      <td>$8.82</td>
    </tr>
    <tr>
      <th>Chanastnya43</th>
      <td>$2.94</td>
      <td>3</td>
      <td>$8.82</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>Lirtim36</th>
      <td>$1.33</td>
      <td>1</td>
      <td>$1.33</td>
    </tr>
    <tr>
      <th>Shidai42</th>
      <td>$1.33</td>
      <td>1</td>
      <td>$1.33</td>
    </tr>
    <tr>
      <th>Philodil43</th>
      <td>$1.29</td>
      <td>1</td>
      <td>$1.29</td>
    </tr>
    <tr>
      <th>Eyista89</th>
      <td>$1.29</td>
      <td>1</td>
      <td>$1.29</td>
    </tr>
    <tr>
      <th>Mindilsa60</th>
      <td>$1.28</td>
      <td>1</td>
      <td>$1.28</td>
    </tr>
    <tr>
      <th>Tyarithn67</th>
      <td>$1.14</td>
      <td>1</td>
      <td>$1.14</td>
    </tr>
    <tr>
      <th>Aisur51</th>
      <td>$1.14</td>
      <td>1</td>
      <td>$1.14</td>
    </tr>
    <tr>
      <th>Ilista82</th>
      <td>$1.14</td>
      <td>1</td>
      <td>$1.14</td>
    </tr>
    <tr>
      <th>Jiskimsda56</th>
      <td>$1.14</td>
      <td>1</td>
      <td>$1.14</td>
    </tr>
    <tr>
      <th>Aillyriadru65</th>
      <td>$1.10</td>
      <td>1</td>
      <td>$1.10</td>
    </tr>
    <tr>
      <th>Eryon48</th>
      <td>$1.10</td>
      <td>1</td>
      <td>$1.10</td>
    </tr>
    <tr>
      <th>Iduelis31</th>
      <td>$1.10</td>
      <td>1</td>
      <td>$1.10</td>
    </tr>
    <tr>
      <th>Yasur85</th>
      <td>$1.10</td>
      <td>1</td>
      <td>$1.10</td>
    </tr>
    <tr>
      <th>Undjask33</th>
      <td>$1.10</td>
      <td>1</td>
      <td>$1.10</td>
    </tr>
    <tr>
      <th>Lirtassa52</th>
      <td>$1.09</td>
      <td>1</td>
      <td>$1.09</td>
    </tr>
    <tr>
      <th>Aelidru27</th>
      <td>$1.09</td>
      <td>1</td>
      <td>$1.09</td>
    </tr>
    <tr>
      <th>Yalaeria91</th>
      <td>$1.06</td>
      <td>1</td>
      <td>$1.06</td>
    </tr>
    <tr>
      <th>Aesurstilis64</th>
      <td>$1.03</td>
      <td>1</td>
      <td>$1.03</td>
    </tr>
    <tr>
      <th>Saida58</th>
      <td>$1.03</td>
      <td>1</td>
      <td>$1.03</td>
    </tr>
    <tr>
      <th>Euthe35</th>
      <td>$1.03</td>
      <td>1</td>
      <td>$1.03</td>
    </tr>
    <tr>
      <th>Hala31</th>
      <td>$1.02</td>
      <td>1</td>
      <td>$1.02</td>
    </tr>
    <tr>
      <th>Qilalista41</th>
      <td>$1.02</td>
      <td>1</td>
      <td>$1.02</td>
    </tr>
    <tr>
      <th>Frichjaskan98</th>
      <td>$1.02</td>
      <td>1</td>
      <td>$1.02</td>
    </tr>
    <tr>
      <th>Isurria36</th>
      <td>$1.02</td>
      <td>1</td>
      <td>$1.02</td>
    </tr>
    <tr>
      <th>Eudanu84</th>
      <td>$1.02</td>
      <td>1</td>
      <td>$1.02</td>
    </tr>
    <tr>
      <th>Ililsasya43</th>
      <td>$1.02</td>
      <td>1</td>
      <td>$1.02</td>
    </tr>
    <tr>
      <th>Irilis75</th>
      <td>$1.02</td>
      <td>1</td>
      <td>$1.02</td>
    </tr>
    <tr>
      <th>Aidai61</th>
      <td>$1.01</td>
      <td>1</td>
      <td>$1.01</td>
    </tr>
    <tr>
      <th>Chanirra79</th>
      <td>$1.01</td>
      <td>1</td>
      <td>$1.01</td>
    </tr>
    <tr>
      <th>Alo38</th>
      <td>$1.00</td>
      <td>1</td>
      <td>$1.00</td>
    </tr>
  </tbody>
</table>
<p>576 rows × 3 columns</p>
</div>



## Most Popular Items

* Retrieve the Item ID, Item Name, and Item Price columns


* Group by Item ID and Item Name. Perform calculations to obtain purchase count, item price, and total purchase value


* Create a summary data frame to hold the results


* Sort the purchase count column in descending order


* Optional: give the displayed data cleaner formatting


* Display a preview of the summary data frame




```python
most_pop = purchase_data[["Item ID","Item Name","Price"]]
most_pop_grp = most_pop.groupby(['Item ID','Item Name'])
purchase_count = most_pop_grp["Item Name"].count()
total_price = most_pop_grp["Price"].sum()

item_price = total_price/purchase_count

most_popular_table = pd.DataFrame({"Purchase Count": purchase_count,
                                   "Item price" : item_price,
                                  "Total Purchase Value": total_price
                                  })
most_popular_table = most_popular_table.sort_values("Purchase Count", ascending=False)
most_popular_table

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
      <th></th>
      <th>Item price</th>
      <th>Purchase Count</th>
      <th>Total Purchase Value</th>
    </tr>
    <tr>
      <th>Item ID</th>
      <th>Item Name</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>178</th>
      <th>Oathbreaker, Last Hope of the Breaking Storm</th>
      <td>$4.23</td>
      <td>12</td>
      <td>$50.76</td>
    </tr>
    <tr>
      <th>145</th>
      <th>Fiery Glass Crusader</th>
      <td>$4.58</td>
      <td>9</td>
      <td>$41.22</td>
    </tr>
    <tr>
      <th>108</th>
      <th>Extraction, Quickblade Of Trembling Hands</th>
      <td>$3.53</td>
      <td>9</td>
      <td>$31.77</td>
    </tr>
    <tr>
      <th>82</th>
      <th>Nirvana</th>
      <td>$4.90</td>
      <td>9</td>
      <td>$44.10</td>
    </tr>
    <tr>
      <th>19</th>
      <th>Pursuit, Cudgel of Necromancy</th>
      <td>$1.02</td>
      <td>8</td>
      <td>$8.16</td>
    </tr>
    <tr>
      <th>103</th>
      <th>Singed Scalpel</th>
      <td>$4.35</td>
      <td>8</td>
      <td>$34.80</td>
    </tr>
    <tr>
      <th>75</th>
      <th>Brutality Ivory Warmace</th>
      <td>$2.42</td>
      <td>8</td>
      <td>$19.36</td>
    </tr>
    <tr>
      <th>72</th>
      <th>Winter's Bite</th>
      <td>$3.77</td>
      <td>8</td>
      <td>$30.16</td>
    </tr>
    <tr>
      <th>60</th>
      <th>Wolf</th>
      <td>$3.54</td>
      <td>8</td>
      <td>$28.32</td>
    </tr>
    <tr>
      <th>59</th>
      <th>Lightning, Etcher of the King</th>
      <td>$4.23</td>
      <td>8</td>
      <td>$33.84</td>
    </tr>
    <tr>
      <th>37</th>
      <th>Shadow Strike, Glory of Ending Hope</th>
      <td>$3.16</td>
      <td>8</td>
      <td>$25.28</td>
    </tr>
    <tr>
      <th>34</th>
      <th>Retribution Axe</th>
      <td>$2.22</td>
      <td>8</td>
      <td>$17.76</td>
    </tr>
    <tr>
      <th>92</th>
      <th>Final Critic</th>
      <td>$4.88</td>
      <td>8</td>
      <td>$39.04</td>
    </tr>
    <tr>
      <th>53</th>
      <th>Vengeance Cleaver</th>
      <td>$2.05</td>
      <td>7</td>
      <td>$14.35</td>
    </tr>
    <tr>
      <th>110</th>
      <th>Suspension</th>
      <td>$1.44</td>
      <td>7</td>
      <td>$10.08</td>
    </tr>
    <tr>
      <th>7</th>
      <th>Thorn, Satchel of Dark Souls</th>
      <td>$1.33</td>
      <td>7</td>
      <td>$9.31</td>
    </tr>
    <tr>
      <th>71</th>
      <th>Demise</th>
      <td>$1.61</td>
      <td>7</td>
      <td>$11.27</td>
    </tr>
    <tr>
      <th>117</th>
      <th>Heartstriker, Legacy of the Light</th>
      <td>$1.79</td>
      <td>7</td>
      <td>$12.53</td>
    </tr>
    <tr>
      <th>159</th>
      <th>Oathbreaker, Spellblade of Trials</th>
      <td>$3.08</td>
      <td>7</td>
      <td>$21.56</td>
    </tr>
    <tr>
      <th>85</th>
      <th>Malificent Bag</th>
      <td>$1.75</td>
      <td>7</td>
      <td>$12.25</td>
    </tr>
    <tr>
      <th>164</th>
      <th>Exiled Doomblade</th>
      <td>$1.63</td>
      <td>7</td>
      <td>$11.41</td>
    </tr>
    <tr>
      <th>141</th>
      <th>Persuasion</th>
      <td>$3.19</td>
      <td>7</td>
      <td>$22.33</td>
    </tr>
    <tr>
      <th>78</th>
      <th>Glimmer, Ender of the Moon</th>
      <td>$4.40</td>
      <td>7</td>
      <td>$30.80</td>
    </tr>
    <tr>
      <th>102</th>
      <th>Avenger</th>
      <td>$3.44</td>
      <td>6</td>
      <td>$20.64</td>
    </tr>
    <tr>
      <th>129</th>
      <th>Fate, Vengeance of Eternal Justice</th>
      <td>$1.54</td>
      <td>6</td>
      <td>$9.24</td>
    </tr>
    <tr>
      <th>93</th>
      <th>Apocalyptic Battlescythe</th>
      <td>$1.97</td>
      <td>6</td>
      <td>$11.82</td>
    </tr>
    <tr>
      <th>54</th>
      <th>Eternal Cleaver</th>
      <td>$2.50</td>
      <td>6</td>
      <td>$15.00</td>
    </tr>
    <tr>
      <th>3</th>
      <th>Phantomlight</th>
      <td>$2.49</td>
      <td>6</td>
      <td>$14.94</td>
    </tr>
    <tr>
      <th>2</th>
      <th>Verdict</th>
      <td>$2.48</td>
      <td>6</td>
      <td>$14.88</td>
    </tr>
    <tr>
      <th>40</th>
      <th>Second Chance</th>
      <td>$2.52</td>
      <td>6</td>
      <td>$15.12</td>
    </tr>
    <tr>
      <th>...</th>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>81</th>
      <th>Dreamkiss</th>
      <td>$3.61</td>
      <td>2</td>
      <td>$7.22</td>
    </tr>
    <tr>
      <th>6</th>
      <th>Rusty Skull</th>
      <td>$3.70</td>
      <td>2</td>
      <td>$7.40</td>
    </tr>
    <tr>
      <th>18</th>
      <th>Torchlight, Bond of Storms</th>
      <td>$4.65</td>
      <td>2</td>
      <td>$9.30</td>
    </tr>
    <tr>
      <th>26</th>
      <th>Unholy Wand</th>
      <td>$1.12</td>
      <td>2</td>
      <td>$2.24</td>
    </tr>
    <tr>
      <th>28</th>
      <th>Flux, Destroyer of Due Diligence</th>
      <td>$1.06</td>
      <td>2</td>
      <td>$2.12</td>
    </tr>
    <tr>
      <th>30</th>
      <th>Stormcaller</th>
      <td>$2.21</td>
      <td>2</td>
      <td>$4.42</td>
    </tr>
    <tr>
      <th>158</th>
      <th>Darkheart, Butcher of the Champion</th>
      <td>$2.45</td>
      <td>2</td>
      <td>$4.90</td>
    </tr>
    <tr>
      <th>69</th>
      <th>Frenzy, Defender of the Harvest</th>
      <td>$1.98</td>
      <td>2</td>
      <td>$3.96</td>
    </tr>
    <tr>
      <th>132</th>
      <th>Persuasion</th>
      <td>$3.33</td>
      <td>2</td>
      <td>$6.66</td>
    </tr>
    <tr>
      <th>63</th>
      <th>Stormfury Mace</th>
      <td>$4.99</td>
      <td>2</td>
      <td>$9.98</td>
    </tr>
    <tr>
      <th>56</th>
      <th>Foul Titanium Battle Axe</th>
      <td>$2.92</td>
      <td>2</td>
      <td>$5.84</td>
    </tr>
    <tr>
      <th>127</th>
      <th>Heartseeker, Reaver of Souls</th>
      <td>$3.92</td>
      <td>2</td>
      <td>$7.84</td>
    </tr>
    <tr>
      <th>48</th>
      <th>Rage, Legacy of the Lone Victor</th>
      <td>$2.48</td>
      <td>2</td>
      <td>$4.96</td>
    </tr>
    <tr>
      <th>125</th>
      <th>Whistling Mithril Warblade</th>
      <td>$1.00</td>
      <td>2</td>
      <td>$2.00</td>
    </tr>
    <tr>
      <th>43</th>
      <th>Foul Edge</th>
      <td>$3.54</td>
      <td>2</td>
      <td>$7.08</td>
    </tr>
    <tr>
      <th>115</th>
      <th>Spectral Diamond Doomblade</th>
      <td>$2.04</td>
      <td>2</td>
      <td>$4.08</td>
    </tr>
    <tr>
      <th>33</th>
      <th>Curved Axe</th>
      <td>$1.16</td>
      <td>2</td>
      <td>$2.32</td>
    </tr>
    <tr>
      <th>31</th>
      <th>Trickster</th>
      <td>$1.55</td>
      <td>2</td>
      <td>$3.10</td>
    </tr>
    <tr>
      <th>118</th>
      <th>Ghost Reaver, Longsword of Magic</th>
      <td>$2.17</td>
      <td>1</td>
      <td>$2.17</td>
    </tr>
    <tr>
      <th>47</th>
      <th>Alpha, Reach of Ending Hope</th>
      <td>$3.58</td>
      <td>1</td>
      <td>$3.58</td>
    </tr>
    <tr>
      <th>42</th>
      <th>The Decapitator</th>
      <td>$1.75</td>
      <td>1</td>
      <td>$1.75</td>
    </tr>
    <tr>
      <th>27</th>
      <th>Riddle, Tribute of Ended Dreams</th>
      <td>$3.30</td>
      <td>1</td>
      <td>$3.30</td>
    </tr>
    <tr>
      <th>126</th>
      <th>Exiled Mithril Longsword</th>
      <td>$2.00</td>
      <td>1</td>
      <td>$2.00</td>
    </tr>
    <tr>
      <th>51</th>
      <th>Endbringer</th>
      <td>$4.66</td>
      <td>1</td>
      <td>$4.66</td>
    </tr>
    <tr>
      <th>90</th>
      <th>Betrayer</th>
      <td>$2.94</td>
      <td>1</td>
      <td>$2.94</td>
    </tr>
    <tr>
      <th>104</th>
      <th>Gladiator's Glaive</th>
      <td>$1.93</td>
      <td>1</td>
      <td>$1.93</td>
    </tr>
    <tr>
      <th>23</th>
      <th>Crucifer</th>
      <td>$1.99</td>
      <td>1</td>
      <td>$1.99</td>
    </tr>
    <tr>
      <th>180</th>
      <th>Stormcaller</th>
      <td>$3.36</td>
      <td>1</td>
      <td>$3.36</td>
    </tr>
    <tr>
      <th>91</th>
      <th>Celeste</th>
      <td>$4.17</td>
      <td>1</td>
      <td>$4.17</td>
    </tr>
    <tr>
      <th>134</th>
      <th>Undead Crusader</th>
      <td>$4.50</td>
      <td>1</td>
      <td>$4.50</td>
    </tr>
  </tbody>
</table>
<p>183 rows × 3 columns</p>
</div>



## Most Profitable Items

* Sort the above table by total purchase value in descending order


* Optional: give the displayed data cleaner formatting


* Display a preview of the data frame




```python
most_popular_table = pd.DataFrame({"Purchase Count": purchase_count,
                                   "Item price" : item_price,
                                  "Total Purchase Value": total_price
                                  })
most_popular_table = most_popular_table.sort_values("Total Purchase Value", ascending=False)
most_popular_table
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
      <th></th>
      <th>Item price</th>
      <th>Purchase Count</th>
      <th>Total Purchase Value</th>
    </tr>
    <tr>
      <th>Item ID</th>
      <th>Item Name</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>178</th>
      <th>Oathbreaker, Last Hope of the Breaking Storm</th>
      <td>$4.23</td>
      <td>12</td>
      <td>$50.76</td>
    </tr>
    <tr>
      <th>82</th>
      <th>Nirvana</th>
      <td>$4.90</td>
      <td>9</td>
      <td>$44.10</td>
    </tr>
    <tr>
      <th>145</th>
      <th>Fiery Glass Crusader</th>
      <td>$4.58</td>
      <td>9</td>
      <td>$41.22</td>
    </tr>
    <tr>
      <th>92</th>
      <th>Final Critic</th>
      <td>$4.88</td>
      <td>8</td>
      <td>$39.04</td>
    </tr>
    <tr>
      <th>103</th>
      <th>Singed Scalpel</th>
      <td>$4.35</td>
      <td>8</td>
      <td>$34.80</td>
    </tr>
    <tr>
      <th>59</th>
      <th>Lightning, Etcher of the King</th>
      <td>$4.23</td>
      <td>8</td>
      <td>$33.84</td>
    </tr>
    <tr>
      <th>108</th>
      <th>Extraction, Quickblade Of Trembling Hands</th>
      <td>$3.53</td>
      <td>9</td>
      <td>$31.77</td>
    </tr>
    <tr>
      <th>78</th>
      <th>Glimmer, Ender of the Moon</th>
      <td>$4.40</td>
      <td>7</td>
      <td>$30.80</td>
    </tr>
    <tr>
      <th>72</th>
      <th>Winter's Bite</th>
      <td>$3.77</td>
      <td>8</td>
      <td>$30.16</td>
    </tr>
    <tr>
      <th>60</th>
      <th>Wolf</th>
      <td>$3.54</td>
      <td>8</td>
      <td>$28.32</td>
    </tr>
    <tr>
      <th>179</th>
      <th>Wolf, Promise of the Moonwalker</th>
      <td>$4.48</td>
      <td>6</td>
      <td>$26.88</td>
    </tr>
    <tr>
      <th>160</th>
      <th>Azurewrath</th>
      <td>$4.40</td>
      <td>6</td>
      <td>$26.40</td>
    </tr>
    <tr>
      <th>25</th>
      <th>Hero Cane</th>
      <td>$4.35</td>
      <td>6</td>
      <td>$26.10</td>
    </tr>
    <tr>
      <th>37</th>
      <th>Shadow Strike, Glory of Ending Hope</th>
      <td>$3.16</td>
      <td>8</td>
      <td>$25.28</td>
    </tr>
    <tr>
      <th>139</th>
      <th>Mercy, Katana of Dismay</th>
      <td>$4.94</td>
      <td>5</td>
      <td>$24.70</td>
    </tr>
    <tr>
      <th>128</th>
      <th>Blazeguard, Reach of Eternity</th>
      <td>$4.91</td>
      <td>5</td>
      <td>$24.55</td>
    </tr>
    <tr>
      <th>138</th>
      <th>Peacekeeper, Wit of Dark Magic</th>
      <td>$4.74</td>
      <td>5</td>
      <td>$23.70</td>
    </tr>
    <tr>
      <th>141</th>
      <th>Persuasion</th>
      <td>$3.19</td>
      <td>7</td>
      <td>$22.33</td>
    </tr>
    <tr>
      <th>87</th>
      <th>Deluge, Edge of the West</th>
      <td>$4.43</td>
      <td>5</td>
      <td>$22.15</td>
    </tr>
    <tr>
      <th>159</th>
      <th>Oathbreaker, Spellblade of Trials</th>
      <td>$3.08</td>
      <td>7</td>
      <td>$21.56</td>
    </tr>
    <tr>
      <th>136</th>
      <th>Ghastly Adamantite Protector</th>
      <td>$3.58</td>
      <td>6</td>
      <td>$21.48</td>
    </tr>
    <tr>
      <th>65</th>
      <th>Conqueror Adamantite Mace</th>
      <td>$4.24</td>
      <td>5</td>
      <td>$21.20</td>
    </tr>
    <tr>
      <th>101</th>
      <th>Final Critic</th>
      <td>$4.19</td>
      <td>5</td>
      <td>$20.95</td>
    </tr>
    <tr>
      <th>102</th>
      <th>Avenger</th>
      <td>$3.44</td>
      <td>6</td>
      <td>$20.64</td>
    </tr>
    <tr>
      <th>133</th>
      <th>Faith's Scimitar</th>
      <td>$4.09</td>
      <td>5</td>
      <td>$20.45</td>
    </tr>
    <tr>
      <th>39</th>
      <th>Betrayal, Whisper of Grieving Widows</th>
      <td>$3.94</td>
      <td>5</td>
      <td>$19.70</td>
    </tr>
    <tr>
      <th>111</th>
      <th>Misery's End</th>
      <td>$4.89</td>
      <td>4</td>
      <td>$19.56</td>
    </tr>
    <tr>
      <th>165</th>
      <th>Bone Crushing Silver Skewer</th>
      <td>$4.86</td>
      <td>4</td>
      <td>$19.44</td>
    </tr>
    <tr>
      <th>75</th>
      <th>Brutality Ivory Warmace</th>
      <td>$2.42</td>
      <td>8</td>
      <td>$19.36</td>
    </tr>
    <tr>
      <th>52</th>
      <th>Hatred</th>
      <td>$4.84</td>
      <td>4</td>
      <td>$19.36</td>
    </tr>
    <tr>
      <th>...</th>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>124</th>
      <th>Venom Claymore</th>
      <td>$1.29</td>
      <td>4</td>
      <td>$5.16</td>
    </tr>
    <tr>
      <th>0</th>
      <th>Splinter</th>
      <td>$1.28</td>
      <td>4</td>
      <td>$5.12</td>
    </tr>
    <tr>
      <th>155</th>
      <th>War-Forged Gold Deflector</th>
      <td>$1.01</td>
      <td>5</td>
      <td>$5.05</td>
    </tr>
    <tr>
      <th>48</th>
      <th>Rage, Legacy of the Lone Victor</th>
      <td>$2.48</td>
      <td>2</td>
      <td>$4.96</td>
    </tr>
    <tr>
      <th>158</th>
      <th>Darkheart, Butcher of the Champion</th>
      <td>$2.45</td>
      <td>2</td>
      <td>$4.90</td>
    </tr>
    <tr>
      <th>51</th>
      <th>Endbringer</th>
      <td>$4.66</td>
      <td>1</td>
      <td>$4.66</td>
    </tr>
    <tr>
      <th>134</th>
      <th>Undead Crusader</th>
      <td>$4.50</td>
      <td>1</td>
      <td>$4.50</td>
    </tr>
    <tr>
      <th>30</th>
      <th>Stormcaller</th>
      <td>$2.21</td>
      <td>2</td>
      <td>$4.42</td>
    </tr>
    <tr>
      <th>135</th>
      <th>Warped Diamond Crusader</th>
      <td>$1.40</td>
      <td>3</td>
      <td>$4.20</td>
    </tr>
    <tr>
      <th>91</th>
      <th>Celeste</th>
      <td>$4.17</td>
      <td>1</td>
      <td>$4.17</td>
    </tr>
    <tr>
      <th>177</th>
      <th>Winterthorn, Defender of Shifting Worlds</th>
      <td>$2.08</td>
      <td>2</td>
      <td>$4.16</td>
    </tr>
    <tr>
      <th>70</th>
      <th>Hope's End</th>
      <td>$1.03</td>
      <td>4</td>
      <td>$4.12</td>
    </tr>
    <tr>
      <th>115</th>
      <th>Spectral Diamond Doomblade</th>
      <td>$2.04</td>
      <td>2</td>
      <td>$4.08</td>
    </tr>
    <tr>
      <th>69</th>
      <th>Frenzy, Defender of the Harvest</th>
      <td>$1.98</td>
      <td>2</td>
      <td>$3.96</td>
    </tr>
    <tr>
      <th>47</th>
      <th>Alpha, Reach of Ending Hope</th>
      <td>$3.58</td>
      <td>1</td>
      <td>$3.58</td>
    </tr>
    <tr>
      <th>180</th>
      <th>Stormcaller</th>
      <td>$3.36</td>
      <td>1</td>
      <td>$3.36</td>
    </tr>
    <tr>
      <th>27</th>
      <th>Riddle, Tribute of Ended Dreams</th>
      <td>$3.30</td>
      <td>1</td>
      <td>$3.30</td>
    </tr>
    <tr>
      <th>183</th>
      <th>Dragon's Greatsword</th>
      <td>$1.09</td>
      <td>3</td>
      <td>$3.27</td>
    </tr>
    <tr>
      <th>31</th>
      <th>Trickster</th>
      <td>$1.55</td>
      <td>2</td>
      <td>$3.10</td>
    </tr>
    <tr>
      <th>168</th>
      <th>Sun Strike, Jaws of Twisted Visions</th>
      <td>$1.48</td>
      <td>2</td>
      <td>$2.96</td>
    </tr>
    <tr>
      <th>90</th>
      <th>Betrayer</th>
      <td>$2.94</td>
      <td>1</td>
      <td>$2.94</td>
    </tr>
    <tr>
      <th>33</th>
      <th>Curved Axe</th>
      <td>$1.16</td>
      <td>2</td>
      <td>$2.32</td>
    </tr>
    <tr>
      <th>26</th>
      <th>Unholy Wand</th>
      <td>$1.12</td>
      <td>2</td>
      <td>$2.24</td>
    </tr>
    <tr>
      <th>118</th>
      <th>Ghost Reaver, Longsword of Magic</th>
      <td>$2.17</td>
      <td>1</td>
      <td>$2.17</td>
    </tr>
    <tr>
      <th>28</th>
      <th>Flux, Destroyer of Due Diligence</th>
      <td>$1.06</td>
      <td>2</td>
      <td>$2.12</td>
    </tr>
    <tr>
      <th>125</th>
      <th>Whistling Mithril Warblade</th>
      <td>$1.00</td>
      <td>2</td>
      <td>$2.00</td>
    </tr>
    <tr>
      <th>126</th>
      <th>Exiled Mithril Longsword</th>
      <td>$2.00</td>
      <td>1</td>
      <td>$2.00</td>
    </tr>
    <tr>
      <th>23</th>
      <th>Crucifer</th>
      <td>$1.99</td>
      <td>1</td>
      <td>$1.99</td>
    </tr>
    <tr>
      <th>104</th>
      <th>Gladiator's Glaive</th>
      <td>$1.93</td>
      <td>1</td>
      <td>$1.93</td>
    </tr>
    <tr>
      <th>42</th>
      <th>The Decapitator</th>
      <td>$1.75</td>
      <td>1</td>
      <td>$1.75</td>
    </tr>
  </tbody>
</table>
<p>183 rows × 3 columns</p>
</div>


