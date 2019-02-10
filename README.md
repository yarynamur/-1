# -1
This module defines which movies were made in the year, given by user, and builds a map with three layers (base, population and movies).
Information is taken from files "locations.list.txt" and "world.json".
Module uses libraries geopy and folium.
HTML file, in which map is presented, uses patterns of folium library (including links in <head>, that defines information about document), tag <!DOCTYPE> defines type of file, tag <body> presents information, that class of this file is folium-map, and then, <script> gives some map parameters and works with information from file "world.json".
This map gives us information about population (for countries with population less than one milion colour is green, with population between one and two milions - orange, more than two milions - red) and locations of movies made in certain year (these are marked by red dots on map).
