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

# generic library for generating the url schemes
# can be called by import NavigatorURLScheme.py
import csv
import os
import urllib
import datetime

class NavigatorURLScheme():
    __navigatorScheme = "arcgis-navigator://"
    __validParameters = ["start", "startname", "stop", "stopname", "optimize", "travelmode", "navigate", "callbackprompt", "callback"]
    __invalidStringCharacters = [" ", "&"]
    __parameterCount = 0  # counter for how many parameters have been passed to stringBuilder

    # constructor
    def __init__(self, parameterDictionary):
        self.__parameterDictionary = parameterDictionary
        self.__stops = self.__parameterDictionary.get("stops", None)
        self.__start = self.__parameterDictionary.get("start", None)
        self.__optimize = str(self.__parameterDictionary.get("optimize", None)).lower().replace(" ", "") \
            if self.__parameterDictionary.get("optimize", None) is not None else None
        self.__navigate = str(self.__parameterDictionary.get("navigate", None)).lower().replace(" ", "") \
            if self.__parameterDictionary.get("navigate", None) is not None else None
        self.__travelMode = self.__parameterDictionary.get("travelmode", None)
        self.__callback = self.__parameterDictionary.get("callback", None) \
            if self.__parameterDictionary.get("callback", None) is not None else None

    # generate the URL string
    def generateURL(self):
        stringBuilder = self.__navigatorScheme + "?"
        if self._encodedLocations(self.__stops):
            stringBuilder += self._encodedLocations(self.__stops)
            self.__parameterCount += 1
        if self._encodedLocations(self.__start, isStop=False):
            stringBuilder += self._encodedLocations(self.__start, isStop=False)
            self.__parameterCount += 1
        if self.__optimize:
            if self.__parameterCount > 0: stringBuilder += "&"
            stringBuilder += "optimize=" + self.__optimize
            self.__parameterCount += 1
        if self.__navigate:
            if self.__parameterCount > 0: stringBuilder += "&"
            stringBuilder += "navigate=" + self.__navigate
            self.__parameterCount += 1
        if self._encodedTravelMode(self.__travelMode):
            stringBuilder += "travelmode=" + self._encodedTravelMode(self.__travelMode)
            self.__parameterCount += 1
        if self.__callback:
            if self.__parameterCount > 0: stringBuilder += "&"
            stringBuilder += self._encodedCallback(self.__callback)
            self.__parameterCount += 1
        self._validateURL(stringBuilder)
        return stringBuilder

    # generic function for travel mode
    # encode travel mode
    def _encodedTravelMode(self, string=None):
        travelmodeBuilder = ""
        formattedString = str(string).lower().replace(" ", "")
        switcher = {
            "drivingtime": "Driving Time",
            "drivingdistance": "Driving Distance",
            "truckingtime": "Trucking Time",
            "truckingdistance": "Trucking Distance",
            "walkingtime": "Walking Time",
            "walkingdistance": "Walking Distance",
            "ruraldrivingtime": "Rural Driving Time",
            "ruraldrivingdistance": "Rural Driving Distance",
        }
        mode = switcher.get(formattedString, None)
        if mode:
            if self.__parameterCount > 0: travelmodeBuilder += "&"
            travelmodeBuilder += urllib.quote_plus(mode)
        else: return None

    # generic function for stops and starts
    # constructor # assuming always list of lists of stops OR list of start
    # [['43.222,-76.444','esri'],['100 Commercial St, Portland, ME,04101','esri']] OR ['43.222,-76.444','esri']
    # encode stop and starts
    def _encodedLocations(self, listLocations=None, isStop=True):
        stopBuilder = ""
        if listLocations:
            if not isStop:
                if self.__parameterCount > 0: stopBuilder += "&"
                locationType, locationNameType = "start=", "&startname="
                hasName = True if len(listLocations) > 1 else False
                if hasName:
                    location, locationName = urllib.quote_plus(str(listLocations[0]), ",'"), urllib.quote_plus(str(listLocations[1]), ",'")
                    stopBuilder += locationType + location + locationNameType + locationName
                else:
                    location = urllib.quote_plus(str(listLocations[0]), ",'")
                    stopBuilder += locationType + location
            else:
                locationType, locationNameType = "stop=", "&stopname="
                for listLocation in listLocations:
                    hasName = True if len(listLocation) > 1 else False
                    if self.__parameterCount > 0: stopBuilder += "&"
                    if hasName:
                        location, locationName = urllib.quote_plus(str(listLocation[0]), ",'"), urllib.quote_plus(str(listLocation[1]), ",'")
                        stopBuilder += locationType + location + locationNameType + locationName
                    else:
                        location = urllib.quote_plus(str(listLocation[0]), ",'")
                        stopBuilder += locationType + location
        return stopBuilder

    # generic function for call backs
    # constructor
    # encode the callback string
    def _encodedCallback(self, callbackList=None):
        callbackBuilder = ""
        hasPrompt = True if len(callbackList) > 1 else False
        if self.__parameterCount > 0: callbackBuilder += "&"
        if hasPrompt:
            callbackScheme, callbackPrompt = str(callbackList[0]), urllib.quote_plus(str(callbackList[1]), ",'")
            callbackBuilder += "callback=" + callbackScheme + "&callbackprompt=" + callbackPrompt
        else:
            callbackScheme = str(callbackList[0])
            callbackBuilder += "callback=" + callbackScheme
        return callbackBuilder

    # generic functions for validating url
    # deconstruct the URL and perform basic validity test
    def _validateURL(self, stringBuilder):
        applicationScheme, parameterString = self._splitStringBuilder(stringBuilder)
        # test applicationScheme is valid
        if applicationScheme != self.__navigatorScheme: raise ValueError("The application scheme is not valid for Navigator")
        parameters = self._splitParameterString(parameterString)
        if parameters is not None:
            for parameter in parameters:
                parameterSplit = parameter.split("=")
                parameterKey, parameterValue = parameterSplit[0], parameterSplit[1]
                if parameterKey not in self.__validParameters: raise ValueError("Invalid parameter key entered: " + parameterKey)
                for char in self.__invalidStringCharacters:
                    if char in parameterValue: raise ValueError("Invalid encoded value entered: " + parameterValue)

    # general function to split into application scheme and parameters
    def _splitStringBuilder(self, stringBuilder):
        stringBuilderSplit = stringBuilder.split("?")
        if stringBuilderSplit > 1: applicationScheme, parameterString = str(stringBuilderSplit[0]), str(stringBuilderSplit[1])
        else: applicationScheme, parameterString = str(stringBuilderSplit[0]), None
        return applicationScheme, parameterString

    # general function to split parameters
    def _splitParameterString(self, parameterString):
        if parameterString and parameterString[0] == "&": parameterString = parameterString[1:len(parameterString)]
        parameters = parameterString.split("&") if parameterString else None
        return parameters


# generic class for hyperlink tools related to app link
class NavigatorURLHyperlinks():
    # empty constructor
    def __init__(self):
        pass

    # generates an html page for a single link. Pass function url string and title
    def generateHTMLlink(self, validURL, title):
        outfile = "applink_" + str(title) + ".htm"
        fp = open(outfile, 'w')
        fp.write("<!doctype html public \"-//w3c/dtd html 4.0 Transitional//en\">\
        <html> <head><title>HTML Link</title></head> <body bgcolor=\"white\"> <h1>HTML Link</h1><p><br>\n")
        print("Generating HTML file at location of library...")
        urlString = str("<a href=\"{}\">Click here to open the navigator app link </a><br>\n").format(validURL)
        # Example of what string looks like --Delete after testing
        print(urlString)
        # Write link to file
        fp.write(urlString)
        fp.write("</body></html>")
        fp.close()

    # generates a html page given a list of url lists ((urlStr_1, urlTitleStr_1), .... , (urlStr_N, urlTitleStr_N))
    def generateHTMLpage(self, validURLs, title):
        outfile = "applinksPage_" + str(title) + ".htm"
        fp = open(outfile, 'w')
        fp.write("<!doctype html public \"-//w3c/dtd html 4.0 Transitional//en\">\
        <html> <head><title>Navigator App Links</title></head> <body bgcolor=\"white\"> <h1>Navigator App Links</h1><p><br>\n")
        print("Generating HTML page at location of library...")
        print("Processing hyperlinks...\n")
        for validURL in validURLs:
            validURLtitle = str("<b>{}</b><br>").format(str(validURL[1]))
            urlString = str("<a href=\"{}\">Click here to open the navigator app link </a><br><br>\n").format(str(validURL[0]))
            # Example of what string looks like --Delete after testing
            print(validURL[1])
            print(validURL[0] + "\n")
            # Write link to file
            fp.write(validURLtitle)
            fp.write(urlString)
        fp.write("</body></html>")
        fp.close()
        print("HTML page completed")

    # generates url lists ((urlStr_1, urlTitleStr_1), .... , (urlStr_N, urlTitleStr_N)) for making html page
    def csv2Lists(self, csvLocation, urllinkIndex=0, titleIndex=1, delimiter=','):
        csvLists = []
        with open(str(csvLocation)) as csvFile:
            readCSV = csv.reader(csvFile, delimiter=delimiter)
            next(readCSV, None)
            next(readCSV, None)
            for row in readCSV:
                rowString = [str(row[urllinkIndex]), str(row[titleIndex])]
                csvLists.append(rowString)
        csvFile.close()
        return csvLists