import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pylab as plt


#---------DATA PROPROCESSING--------------#


# Life expectancy dataframe transposed and NaN values filled in
les = pd.read_csv("life_expectancy_years.csv")
tles = les.transpose()
tles_b = tles.fillna(method='bfill')
tles_f = tles_b.fillna(method='ffill')
#print(tles_f)
#print(tles_f.isna().sum().sum())


#Tidy Data Format
df = pd.DataFrame()

#country
country_col = tles_f.iloc[0, 0:].tolist()
country = list(np.repeat(country_col, 30))
df['country'] = country


#year
y = []
year = []
for i in range (1990, 2020):
    y.append(i)  
    
for i in range (182):
    year.append(y)
    
year = [ item for elem in year for item in elem]
df['year'] = year

#data
col_data = []
le_data = []
for column in range (182):
    col_data = tles_f.iloc[1:, column].tolist()
    le_data.append(col_data)
    
le_data = [ item for elem in le_data for item in elem]
df['life_expectancy_years'] = le_data


# GNP dataframe transposed and NaN values filled in
gni = pd.read_csv("gnipercapita_ppp_current_international.csv")
tgni = gni.transpose()
tgni_b = tgni.fillna(method='bfill')
tgni_f = tgni_b.fillna(method='ffill')

#data
col_gni = []
gni_data = []
for column in range (182):
    col_gni = tgni_f.iloc[1:, column].tolist()
    gni_data.append(col_gni)
    
gni_data = [ item for elem in gni_data for item in elem]
df['GNI/per capitta (PPP, $)'] = gni_data


# Population dataframe transposed and NaN values filled in
pt = pd.read_csv("population_total.csv")
tpt = pt.transpose()
tpt_b = tpt.fillna(method='bfill')
tpt_f = tpt_b.fillna(method='ffill')

#data
col_pop = []
pop_data = []
for column in range (182):
    col_pop = tpt_f.iloc[1:, column].tolist()
    pop_data.append(col_pop)
    
pop_data = [ item for elem in pop_data for item in elem]
df['Popultation Total'] = pop_data


#----------------Streamlit App---------------------#

st.title("Gapminder Dashboard")
st.write("Population, life expectancy and GNI per capita (PPP, current international $)")

#sidebar to select countries
countries = st.sidebar.multiselect(
    "Select Countries",
    df['country'].unique())

#slider
st.sidebar.markdown("## Year")
st.sidebar.markdown("You can **select** the year on which you want to display data in the *chart*.")
x_year = st.sidebar.slider('Slope', min_value=1990, max_value=2019, step=1)


#create the subset
subset_df = df.loc[lambda d: df['country'].isin(countries)]
subset_df = subset_df[subset_df['year'] == x_year]





# create bubble chart
fig, ax = plt.subplots()
ax.scatter(x = np.log(subset_df['GNI/per capitta (PPP, $)']), y = subset_df['life_expectancy_years'] ,
            s=subset_df['Popultation Total']/100000, alpha=0.5, c=np.random.rand(len(subset_df.index)) )

#chart title, axis labels
ax.set_title('GDP, Life expectancy, Population(bubble size)')
ax.set_xlabel('GNI/per capitta (PPP, $)')
ax.set_ylabel('Life Expectancy Years')
st.pyplot(fig)







