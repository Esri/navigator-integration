"""
COPYRIGHT 2016 ESRI

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

'''EXAMPLE OF HOW TO CALL -- THIS WOULD ALL BE OUTSIDE LIBRARY'''
'''import library'''
# if library is inside folder as your script you can use:
# import NavigatorURLScheme
# or explicitly point to folders with dot notation
from src.Python.NavigatorURLScheme_GeneratorLibrary.NavigatorURLScheme import NavigatorURLScheme, NavigatorURLHyperlinks

'''1) Specify if you want to generate or use explicit url'''
generateURL = False

'''2a) Example variables for building url -- USE THIS INFO IF YOU WANT TO GENERATE A HTML PAGE USING LIBRARY GENERATED URL'''
start = ['43.633332,-70.259971', 'My house']  # <-- use list (name item is optional)
stops = [['43.681959,-70.092359', 'Jewell Island']]  # <-- use list of lists (name item is optional)
optimize = "false"  # <-- use string
travelmode = "driving time"  # <-- use string
navigate = "false"  # <-- use string
callback = ["my-cool-app://", "My Cool App"]  # <-- use list
# dictionary of variables -- parameters are optional by deleting key/value
parameterDictionary = {'start': start, 'stops': stops}

'''2b) Example string for explicit url -- USE THIS INFO IF YOU WANT TO GENERATE A HTML PAGE USING EXPLICIT URL'''
explicitURL = 'arcgis-navigator://?start=100+Commercial+St+Portland+ME&startname=Esri&stop=43.633332,-70.259971&stopname=My+House'
title = "simple_startThenStop"

'''3) Call to libraries -- Generate single link pages from data above'''
navigatorURLObject = NavigatorURLScheme(parameterDictionary)  # create NavigatorURLScheme object and generateURL
navigatorURL = navigatorURLObject.generateURL() if generateURL == True else explicitURL   # based on above setting, build or use explicit url
NavigatorURLHyperlinks().generateHTMLlink(navigatorURL, title)  # create HTML file with single link


