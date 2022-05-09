"""
Class: CS230--Section 3
Name: Teresa Mercado
Description: Final Project - Streamlit
I pledge that I have completed the programming assignment independently. 
I have not copied the code from a student or any source.
I have not given my code to any student. 
"""

import streamlit as st
import pandas as pd
import matplotlib as plt
import matplotlib.pyplot as plt
import pydeck as pdk
sidebar = st.sidebar.selectbox("Find what you want to know about Fast Food in the US:", ["Choose an option", "See Complete Data Set", "Map with Restaurant Locations", "State Frequency", "Categories percentages", "Restaurants Freq by City", "Restaurant Information", "Create Simple Budget"])


# FUNCTIONS

# Reading the data
def read():
    return pd.read_csv("Fast Food Restaurants.csv").set_index("id")

# Filtering the data with just the selected provinces
def filtering(data, list1):
    data_frame1 = pd.DataFrame()
    for k in list1:
        data_frame1 = data_frame1.append(data[data['province'] == k])
    return data_frame1

# Filtering the data with just the selected categories
def filtering2(data, list1):
    data_frame2 = pd.DataFrame()
    for k in list1:
        data_frame2 = data_frame2.append(data[data['categories'] == k])
    return data_frame2

# Filtering the data with just selected cities
def filtering3(data, list1):
    data_frame3 = pd.DataFrame()
    for k in list1:
        data_frame3 = data_frame3.append(data[data['city'] == k])
    return data_frame3

# Filtering the data with just selected restaurants
def filtering4(data, list1):
    data_frame3 = pd.DataFrame()
    for k in list1:
        data_frame3 = data_frame3.append(data[data['name'] == k])
    return data_frame3

# Counting the frequency of provinces selected
def freq_dict(dict, selection):
    dict_frequency = {}
    for i in dict.keys():
        if dict[i][selection] not in dict_frequency.keys:
            item = dict[i][selection]
            dict_frequency[item] = 1
        else:
            item = dict[i][selection]
            dict_frequency[item] += 1
        return dict_frequency

# Creating a list with all the provinces in the data
def provinces():
    data_frame2 = read()
    provinces_list = []
    for ind, row in data_frame2.iterrows():
        if row['province'] not in provinces_list:
            provinces_list.append(row['province'])
    provinces_list.sort()
    return provinces_list

# Creating a list with all the categories in the data
def categories():
    data_frame3 = read()
    categories_list = []
    for ind, row in data_frame3.iterrows():
        if row['categories'] not in categories_list:
            categories_list.append(row['categories'])
    categories_list.sort()
    return categories_list

# Creating a list with all the postal codes
def cities():
    data_frame4 = read()
    city_list = []
    for ind, row in data_frame4.iterrows():
        if row['city'] not in city_list:
            city_list.append(row['city'])
    city_list.sort()
    return city_list

# Creating a list with all the restaurants names
def restaurants():
    data_frame5 = read()
    restaurant_list = []
    for ind, row in data_frame5.iterrows():
        if row['name'] not in restaurant_list:
            restaurant_list.append(row['name'])
    restaurant_list.sort()
    return restaurant_list

# Creating a map with all the restaurants in the US
def create_map(dataframe):
    st.header("Restaurants in the US - Map")
    map_df = dataframe.filter(['name', 'latitude', 'longitude'])
    view_state = pdk.ViewState(
        latitude=map_df["latitude"].mean(),
        longitude=map_df["longitude"].mean(),
        zoom=9)
    layer1 = pdk.Layer('ScatterplotLayer',
                       data=map_df,
                       get_position='[longitude,latitude]',
                       get_radius=1000,
                       get_color=[255, 0, 255],
                       pickable=True)
    tool_tip = {"html": "Restaurant Name:<br/> <b>{name}</b>",
                "style": {"backgroundClolor": "steelblue",
                         "color": "white"}}
    map1 = pdk.Deck(
        map_style='mapbox://style/mapbox/light-v9',
        initial_view_state=view_state,
        layers=[layer1],
        tooltip=tool_tip)
    st.pydeck_chart(map1)

# Creating a bar chart
def bar(x, y):
    plt.bar(x, y)
    fig, ax = plt.subplots()
    width = 0.4
    color = st.sidebar.color_picker('Pick A Color', '#00f900')
    ax.bar(x, y, width=width, align='center', color=color, linewidth=width*2, edgecolor='black')
    plt.title("Frequency of Restaurants per State")
    plt.ylabel("Num of Restaurants")
    plt.xlabel("States")
    plt.xticks(rotation=90)
    return plt

# Creating a pie chart
def pie_chart(sizes, list):
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=list, autopct='%1.1f%%')
        ax.axis('equal')
        plt.title("Percentage of Restaurants per Category")
        return plt

# Creating a bar chart 2
def bar2(x, y):
    plt.bar(x, y)
    fig, ax = plt.subplots()
    width = 0.4
    color = st.sidebar.color_picker('Pick A Color', '#00f900')
    ax.bar(x, y, width=width, align='center', color=color, linewidth=width*2, edgecolor='black')
    plt.title("Number of Restaurants per City")
    plt.ylabel("Num of Restaurants")
    plt.xlabel("Cities")
    plt.xticks(rotation=90)
    return plt

# DISPLAYING THE DIFFERENT PAGES

# Display Entry Page
if sidebar == "Choose an option":
    st.title("Fast-Data on Fast Food")
    st.caption("Click on the SIDEBAR know more about the Fast Food Restaurants Data Set")
    st.image('food.jpg')
    st.caption("Fast Food Data Set: This is a list of over 10,000 fast food restaurants provided by Datafiniti's Business Database. The dataset includes the restaurant's address, city, latitude and longitude coordinates, name, and more. ")

# Displaying all the data
if sidebar == "See Complete Data Set":
    st.title("Fast Food Restaurants in America Data set:")
    df = read()
    st.write(df)

# Display Map
if sidebar == "Map with Restaurant Locations":
    df = read()
    create_map(df)

# Displaying and Creating a multiselect with the provinces they want to count and BAR CHART
if sidebar == "State Frequency":
    p_list = provinces()
    select_province = st.multiselect("Select Provinces", p_list, default="AL")
    df = read()
    new_df = filtering(df, select_province)
    groups = new_df.groupby('province').count()
    st.write(groups.name)
    dict1 = groups.name.to_dict()
    st.pyplot(bar(dict1.keys(), dict1.values()))

# Displaying and Creating a multi select with the categories they want to see percentages and PIE CHART
if sidebar == "Categories percentages":
    c_list = categories()
    select_category = st.multiselect("Select a Category", c_list, default="American Restaurant and Fast Food Restaurant")
    df = read()
    df2 = filtering2(df, select_category)
    groups2 = df2.groupby('categories').count()
    st.write(groups2.name)
    dict2 = groups2.name.to_dict()
    st.pyplot(pie_chart(dict2.values(), dict2.keys()))

# Displaying and Creating a multi select with the cities they want to see frequency and BAR CHART
if sidebar == "Restaurants Freq by City":
    cities_list = cities()
    select_cities = st.multiselect("Select a City", cities_list, default='Acton')
    df = read()
    new_df2 = filtering3(df, select_cities)
    groups3 = new_df2.groupby('city').count()
    st.write(groups3.name)
    dict3 = groups3.name.to_dict()
    st.pyplot(bar2(dict3.keys(), dict3.values()))

# EXTRA > Displaying Restaurant WEBSITE after selection
if sidebar == "Restaurant Information":
    restaurants_list = restaurants()
    select_restaurant = st.selectbox("Select a Restaurant", restaurants_list)
    df = read()
    # new_df3 = filtering4(df, select_restaurant)
    st.header(f'{select_restaurant} Info Search:')
    st.write()
    no_space = select_restaurant.replace(" ","+")
    url = f"https://www.google.com/search?q={no_space}&sxsrf=ALiCzsa7vTBb1w9fQ8jV-lGCbigquC3L4w%3A1652060148396&source=hp&ei=9G94YqipFdKhptQP0_SrwA0&iflsig=AJiK0e8AAAAAYnh-BNNG1wBp3r0HyewZ7eixfEttgwwS&gs_ssp=eJzj4tTP1TcwSk4uKVRgNGB0YPDiTs7ITM5WSMvMUUgEAGrdB7E&oq=chick&gs_lcp=Cgdnd3Mtd2l6EAEYADIOCC4QgAQQsQMQxwEQowIyCgguELEDENQCEEMyCAgAEIAEELEDMgsIABCABBCxAxCDATILCC4QgAQQsQMQgwEyCwguELEDEMcBEKMCMgcIABCxAxBDMggIABCABBCxAzIICAAQgAQQyQMyBQgAEJIDOgQIIxAnOgUIABCRAjoICC4QsQMQgwE6CAgAELEDEIMBOhEILhCABBCxAxCDARDHARDRAzoKCC4QxwEQrwEQJzoECAAQQzoGCAAQChBDOhEILhCABBCxAxCDARDHARCjAjoFCAAQgAQ6CAguEIAEELEDOgUILhCABFAAWOMFYLgRaABwAHgBgAHcAYgBoQWSAQUzLjEuMZgBAKABAQ&sclient=gws-wiz"
    st.write("check out this [link](%s)" % url)
    st.balloons()

# Create a Simple Budget
if sidebar == "Create Simple Budget":
    st.header("Create a simple budget for your fast-food trip!")
    x = st.slider("Transportation Money", 0, 100, 1)
    y = st.slider("Food $ per person", 0, 100, 1)
    z = st.slider("Number of Attendees", 0, 10, 1)
    df = pd.DataFrame({"Trans": [x], "Food p/p": [y], "Attendees": [z], "Budget Total": [x + (y*z)]}, index=["Calculations"])
    st.write(df)
    st.subheader(f'Your Budget total with food and transportation is: US${x + (y*z)}')
