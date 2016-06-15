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

from NavigatorURLScheme import *

'''User information'''
# example variables -- all optional
start = ['43.633332,-70.259971', 'My house']  # <-- use list (name item is optional)
stops = [['43.681959,-70.092359', 'Jewell Island']]  # <-- use list of lists (name item is optional)
optimize = "false"  # <-- use string
travelmode = "driving time"  # <-- use list of lists
navigate = "false"  # <-- use list of lists
callback = ["my-cool-app://", "My Cool App"]  # <-- use list
# dictionary of variables -- parameters are optional by deleting key/value <--- need some error handling, like at least one stop??
parameterDictionary = {'start': start, 'stops': stops}

title = "stopInaccessible"
explicitURL = 'arcgis-navigator://?stop=43.681959,-70.092359&stopname=Jewell+Island&start=43.633332,-70.259971&startname=My+house'


# '''Call to libraries -- Generate single link pages from data above'''
# # create NavigatorURLScheme object
# # generateURL
# navigatorURLObject = NavigatorURLScheme(parameterDictionary)
# navigatorURL = navigatorURLObject.generateURL()
# # OR
# # create HTML file with single link
# NavigatorURLHyperlinks().generateHTMLlink(navigatorURL, title)
# #NavigatorURLHyperlinks().generateHTMLlink(explicitURL, title)


'''Call to libraries -- Generate multiple link pages from either explicit list of CSV'''
hyperlinkObject = NavigatorURLHyperlinks()
# define list of link lists
# generate html page from proper input
# explicitURLs = (('arcgis-navigator://?stop=43.681959,-70.092359&stopname=Jewell+Island&start=43.633332,-70.259971&startname=My+house', 'stopInaccessible'),
#                 ('arcgis-navigator://?stop=43.681959,-70.092359&stopname=Jewell+Island&start=43.633332,-70.259971&startname=My+house', 'stopInaccessible'),
#                 ('arcgis-navigator://?stop=43.681959,-70.092359&stopname=Jewell+Island&start=43.633332,-70.259971&startname=My+house', 'stopInaccessible'),)
# hyperlinkObject.generateHTMLpage(explicitURLs)
# OR
# prepare list of link lists from CSV
# generate html page from proper input
fileLocation = '/Users/joel8641/Dropbox/Esri Material/NavigatorURLScheme/NavigatorURLScheme_Library/applink_testcases.csv'
csvLists = hyperlinkObject.csv2Lists(fileLocation, delimiter=",")
htmlPageTitle = "FryesLeap"
hyperlinkObject.generateHTMLpage(csvLists, htmlPageTitle)