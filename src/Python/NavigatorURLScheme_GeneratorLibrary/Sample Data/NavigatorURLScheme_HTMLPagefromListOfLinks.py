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

'''1) Call to libraries -- Generate multiple link pages from explicit list of links'''
# define list of link lists and generate html page
hyperlinkObject = NavigatorURLHyperlinks()
explicitURLs = (('arcgis-navigator://?stop=43.681959,-70.092359&stopname=Jewell+Island&start=43.633332,-70.259971&startname=My+house', 'stopInaccessible'),
                ('arcgis-navigator://?stop=43.681959,-70.092359&stopname=Jewell+Island&start=43.633332,-70.259971&startname=My+house', 'stopInaccessible'),
                ('arcgis-navigator://?stop=43.681959,-70.092359&stopname=Jewell+Island&start=43.633332,-70.259971&startname=My+house', 'stopInaccessible'),)
htmlPageTitle = "ExplicitListOfURLs"
hyperlinkObject.generateHTMLpage(explicitURLs, htmlPageTitle)
