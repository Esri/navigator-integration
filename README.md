# Navigator Integration

Multi Language repository which explains the use of the custom URL scheme in Navigator for ArcGIS. This project contains documentation and sample code for creating custom URL schemes.

##What's included

* [Documentation](#documentation) on the structure of the URL scheme
* Sample code for iOS, Android and JavaScript

##Getting started

Read the documentation below and then clone down the appropriate language into your development environment

## Documentation

###Navigator for ArcGIS URL Scheme

A URL scheme allows you to launch a native app from another native or web application. You can set options in the URL that will be passed to the launched application allowing it to perform specific functions. This capability exists on both the iOS an Android platforms.

You can use the Navigator for ArcGIS URL scheme to launch Navigator and perform searches, calculate routes to one or more stops, and to enter navigation mode. 

Navigator URLs start with the identifier `arcgis-navigator` and may contain additional parameters of the form:

`
arcgis-navigator://?parameter=value&parameter=value
`

The remainder of this document describes the various parameters supported by Navigator.

###Display directions:

The simplest scheme that may be used to request and display directions to a single location. The user’s current location is used as the starting point. The map’s default travel mode is used. 

`stop`: Sets the destination for directions. 

`stopname`: Specifies the name of the stop (*optional*).

The `stop` parameter may be either a latitude and longitude or a query formatted address. 
The `stopname` parameter is optional. 


The following example URL defines a single stop using a latitude and longitude:

```
arcgis-navigator://?stop=43.651508,-70.290554
```

This example URL defines a single stop using an address.

```html
arcgis-navigator://?stop=103+Fox+St,+Portland,+ME+04101
```

This example URL defines a single stop using a latitude and longitude and includes a name for the stop.

```
arcgis-navigator://?stop=43.651508,-70.290554&stopname=Bissell+Bothers
```

If either the name or address contains reserved characters, these should be encoded. For example, this URL defines a single stop named ‘Street & Co.’:

```html
arcgis-navigator://?stop=33+Wharf+Street,+Portland+ME&stopname=Street+%26+Co.
```

###Custom starting point:

To specify a starting point other than the user’s current location:

`start`: Sets the starting point for directions.


`startname`: Specifies the name of the start (optional).

The `start` parameter includes either a latitude and longitude or a query formatted address. The `startname` parameter is optional. 

The following example URL displays directions between the Portland International Jetport and Hadlock Field:

```html
arcgis-navigator://?stop=271+Park+Ave,+Portland+ME&stopname=Hadlock+Field&start=PWM&startname=Portland+International+Jetport
```

###Multiple stops:

Navigator can generate directions to multiple stops. Each stop is denoted with a `stop` parameter. The following example URL displays directions to two stops.

```html
arcgis-navigator://?stop=7+Exchange+St,+Portland,+ME&stop=225+Two+Lights+Rd,+Cape+Elizabeth,+ME
```

In the following example the URL contains two stops with stop names:

```html
arcgis-navigator://?stop=103+Fox+St,+Portland,+ME+04101&stopname=Rising+Tide&stop=43.651508,-70.290554&stopname=Bissell+Bothers
```
###Optimize route:
When multiple stops are included, Navigator can optionally optimize the order of the stops. To optimize the order of the stops, include the `optimize` parameter.

`optimize`: Specifies that the order of the stops should be optimized. Defaults to false.

The following example URL specifies that the order of the stops should be optimized.

```html
arcgis-navigator://?stop=43.65958,-70.25118&stop=43.65761,-70.25388&optimize=true
```

###Travel mode:
Navigator maps can include multiple travel modes. If the `travelmode` parameter is specified it will be used when the directions are generated. Otherwise the default travel mode will be used.

`travelmode`: Specifies the method of transportation.

The following example URL displays walking directions to Esri.

```html
arcgis-navigator://?stop=380+New+York+St,+Redlands,+CA&stopname=Esri&travelmode=Walking+Time
```

Note that travel modes are defined by the map. The travel modes for the default Esri maps are: 

- Driving Time
- Driving Distance
- Trucking Time
- Trucking Distance
- Walking Time
- Walking Distance

###Navigation mode:
To automatically enter navigation mode, specify the `navigate` parameter.

`navigate`: If true, navigation mode will be activated. 

###Specify a callback URL:
If you’d like your app to be notified when navigation completes you can include a callback URL. 

`callback`: Specifies the URL to call when navigation is complete. 

`callbackprompt`: Indicates that an alert should be shown asking the user if control should be given back to the calling app. Specifies the text to display when prompting the user. (*optional*)

If the `callback` parameter is specified the app will be notified regardless of the value of the `navigate` parameter. Note that your custom URL scheme must be registered with the operating system.

The following example URL specifies that Navigator should enter navigation mode and that the custom app, my-cool-app, should be notified when navigation completes. Because the `callbackprompt` parameter is not present, control will pass directly to the calling app and no prompt will be displayed. 

```html
arcgis-navigator://?stop=43.65958,-70.25118&callbackprompt=My+Cool+App&callback=my-cool-app://
```

###Errors:
If an error is encountered when processing a URL scheme, an alert will be displayed to the user.

## Resources and Related Repositories

* [Navigator Documentation](http://doc.arcgis.com/en/navigator/)
* [Collector for ArcGIS Integration Repository](http://developers.arcgis.com)
* [Explorer for ArcGIS Integration Repository](http://developers.arcgis.com)

## Issues

Find a bug or want to request a new feature? Please let us know by submitting an issue (we don't bite and you just might get some swag). Thank you!

## Contributing

Anyone and everyone is welcome to contribute. Please see our [guidelines for contributing](https://github.com/esri/contributing).

## Credits

## Licensing
Copyright 2016 Esri

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

[](Esri Tags: iOS, Android, Navigator, URL Scheme)
[](Esri Language: Java, Swift, Javascript)
