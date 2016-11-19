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

import csv
import os
import datetime
import urllib.parse
import io
import pyqrcode

'''
Library for generating valid url schemes and generated html links/pages
'''

class NavigatorURLScheme:
    """
    generic library for generating the url schemes
    """
    # global variables
    __navigatorScheme = "arcgis-navigator://"
    __validParameters = ["start", "startname", "stop", "stopname", "optimize", "travelmode", "navigate", "callbackprompt", "callback"]
    __invalidStringCharacters = [" ", "&"]
    __parameterCount = 0  # counter for how many parameters have been passed to stringBuilder

    def __init__(self, parameterDictionary):
        """
        constructor for the NavigatorURLScheme library
        :param parameterDictionary: the dictionary of key/value pairs to be used when building url
        """
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

    def generateURL(self):
        """
        function to generate the URL string
        :return: stringBuilder: the validated url
        """
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

    def _encodedTravelMode(self, string=None):
        """
        generic function to encode travel mode if one is passed in via the parameterDictionary
        :param string: optional string for travel mode
        :return: travelmodelBuilder or None: returns encoded travel mode if one exists for inputted string
        """
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
            travelmodeBuilder += urllib.parse.quote_plus(mode)
            return travelmodeBuilder
        else: return None

    def _encodedLocations(self, listLocations=None, isStop=True):
        """
        generic function for stops and starts assuming always list of lists of stops OR list of start
        :param listLocations: [['43.222,-76.444','esri'],['100 Commercial St, Portland, ME,04101','esri']] OR ['43.222,-76.444','esri']
        :param isStop: Boolean for start or stop
        :return: stopBuilder: encode stop and starts
        """
        stopBuilder = ""
        if listLocations:
            if not isStop:
                if self.__parameterCount > 0: stopBuilder += "&"
                locationType, locationNameType = "start=", "&startname="
                hasName = True if len(listLocations) > 1 else False
                if hasName:
                    location, locationName = urllib.parse.quote_plus(str(listLocations[0]), ",'"), urllib.parse.quote_plus(str(listLocations[1]), ",'")
                    stopBuilder += locationType + location + locationNameType + locationName
                else:
                    location = urllib.parse.quote_plus(str(listLocations[0]), ",'")
                    stopBuilder += locationType + location
            else:
                locationType, locationNameType = "stop=", "&stopname="
                stop_count = 0
                for listLocation in listLocations:
                    hasName = True if len(listLocation) > 1 else False
                    if self.__parameterCount > 0: stopBuilder += "&"
                    elif stop_count > 0: stopBuilder += "&"
                    if hasName:
                        location, locationName = urllib.parse.quote_plus(str(listLocation[0]), ",'"), urllib.parse.quote_plus(str(listLocation[1]), ",'")
                        stopBuilder += locationType + location + locationNameType + locationName
                    else:
                        location = urllib.parse.quote_plus(str(listLocation[0]), ",'")
                        stopBuilder += locationType + location
                    stop_count += 1
        return stopBuilder

    def _encodedCallback(self, callbackList=None):
        """
        generic function for encoding call backs
        :param callbackList: optional list for callback ["my-cool-app://", "My Cool App"]
        :return: callbackBuilder: encoded the callback string
        """
        callbackBuilder = ""
        hasPrompt = True if len(callbackList) > 1 else False
        if self.__parameterCount > 0: callbackBuilder += "&"
        if hasPrompt:
            callbackScheme, callbackPrompt = str(callbackList[0]), urllib.parse.quote_plus(str(callbackList[1]), ",'")
            callbackBuilder += "callback=" + callbackScheme + "&callbackprompt=" + callbackPrompt
        else:
            callbackScheme = str(callbackList[0])
            callbackBuilder += "callback=" + callbackScheme
        return callbackBuilder

    def _validateURL(self, stringBuilder):
        """
        generic function for validating url. deconstruct the URL and perform basic validity test
        :param stringBuilder: takes the constructed url string
        """
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

    def _splitStringBuilder(self, stringBuilder):
        """
        supporting function of validateURL to split into application scheme and parameters
        :param stringBuilder: takes the constructed url string
        :return: applicationScheme, parameterString: splits the string by applicationScheme and parameterString
        """
        stringBuilderSplit = stringBuilder.split("?")
        if len(stringBuilderSplit) > 1: applicationScheme, parameterString = str(stringBuilderSplit[0]), str(stringBuilderSplit[1])
        else: applicationScheme, parameterString = str(stringBuilderSplit[0]), None
        return applicationScheme, parameterString

    def _splitParameterString(self, parameterString):
        """
        supporting function of validateURL to split parameterString into individual parameters
        :param parameterString: takes parameterString of url scheme
        :return: parameters: list of parameters [param=value, param=value, ...]
        """
        if parameterString and parameterString[0] == "&": parameterString = parameterString[1:len(parameterString)]
        parameters = parameterString.split("&") if parameterString else None
        return parameters


class NavigatorURLHyperlinks:
    """
    generic class for hyperlink tools related to app link
    """
    # empty constructor
    def __init__(self):
        pass

    def generateHTMLlink(self, validURL, title):
        """
        generates an html page for a single link
        :param validURL: valid url string
        :param title: title of hyperlink as string
        """
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

    def generateHTMLpage(self, validURLs, title):
        """
        generates a html page given
        :param validURLs: a list of url lists [[urlStr_1, urlTitleStr_1], .... , [urlStr_N, urlTitleStr_N]]
        :param title: title of html page as string
        """
        outfile = "applinksPage_" + str(title) + ".htm"
        fp = open(outfile, 'w')
        fp.write(str("<!doctype html public \"-//w3c/dtd html 4.0 Transitional//en\">\
        <html> <head><title>{}: Navigator App Links</title></head> <body bgcolor=\"white\"> <h1>{}: Navigator App Links</h1><p><br>\n").format(str(title), str(title)))
        print("Generating HTML page at location of library...")
        print("Processing hyperlinks...\n")
        count = 1
        for validURL in validURLs:
            urlString = str("<a href=\"{}\">{}. {}</a>").format(str(validURL[0]), str(count), str(validURL[1]))  # the hyperlink
            urlStringText = str("<a>{}</a><br><br>\n").format(validURL[0])  # the url scheme text
            # additional indices if used
            validURLcomments, validURLcomments2 = "", ""
            if len(validURL) > 2:
                if validURL[3] is not "": validURLcomments2 = str("<b>{}</b><br>").format(validURL[3])  # the test group info
                if validURL[2] is not "": validURLcomments = str("<a>\t({})</a><br>").format(validURL[2])  # the PASS/FAIL info
            # # Example of what string looks like --Delete after testing
            # if validURL[3] is not "": print(validURL[3])
            # print(validURL[1])
            # if validURL[2] is not "": print(validURL[2])
            # print(validURL[0] + "\n")
            # Write info to file
            if validURLcomments2 is not "": fp.write(validURLcomments2)
            fp.write(urlString)
            if validURLcomments is not "": fp.write(validURLcomments)
            else: fp.write("<br>")
            fp.write(urlStringText)
            count += 1
        fp.write("</body></html>")
        fp.close()
        print("HTML page completed")

    def csv2Lists(self, csvLocation, delimiter=','):
        """
        supporting function for generateHTMLpage and generates url lists from csv file
        :param csvLocation: full path to csv file
        :param urllinkIndex: optional index of url within row tuple
        :param titleIndex: optional index of title within row tuple
        :param delimiter: optional delimiter parameter
        :return: csvLists: a list of url lists [[urlStr_1, urlTitleStr_1], .... , [urlStr_N, urlTitleStr_N]]
        """
        csvLists = []
        with open(str(csvLocation)) as csvFile:
            readCSV = csv.reader(csvFile, delimiter=delimiter)
            next(readCSV, None)
            for row in readCSV:
                csvLists.append(row)
        csvFile.close()
        return csvLists


class NavigatorURLQRCode:
    """
    generic class for making QR codes for app-links
    """
    def __init__(self):
        pass

    def returnQRCodeText(self, validURL):
        objectQRCode = pyqrcode.create(validURL)
        return objectQRCode.text()

    def saveQRCodeSVG(self, validURL, filename, imageDirectory=None):
        fullfilename = imageDirectory + filename if imageDirectory is not None else filename
        objectQRCode = pyqrcode.create(validURL)
        objectQRCode.svg(fullfilename + ".svg", scale=4)
        # in-memory stream is also supported
        buffer = io.BytesIO()
        objectQRCode.svg(buffer)
        # do whatever you want with buffer.getvalue()
        print(list(buffer.getvalue()))

    def saveQRCodePNG(self, validURL, filename, imageDirectory=None):
        fullfilename = imageDirectory + filename if imageDirectory is not None else filename
        objectQRCode = pyqrcode.create(validURL)
        with open(fullfilename + ".png", 'wb') as fstream:
            objectQRCode.png(fstream, scale=5)
        # same as above
        objectQRCode.png(fullfilename + ".png", scale=5)
        # in-memory stream is also supported
        buffer = io.BytesIO()
        objectQRCode.png(buffer)
        # do whatever you want with buffer.getvalue()
        print(list(buffer.getvalue()))
