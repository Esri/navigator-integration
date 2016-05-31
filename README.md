# Navigator custom URL scheme

Multi Language repository that contains documentation and sample code for creating custom URL schemes in [Navigator for ArcGIS](http://doc.arcgis.com/en/navigator/).

## What's included

* [Documentation](#documentation) on the URL scheme structure
* [Sample code](#sample) for iOS (Swift), Android (Java) and Web (JavaScript)

## Getting started

Read the documentation below and then clone down the appropriate language into your development environment.

## Documentation<a name="documentation"></a>

####Navigator for ArcGIS URL scheme

A URL scheme allows you to launch a native app from another native or web app. You can set options in the URL that will be passed to the app you want to launch, causing it to perform specific functions. This capability is available on the iOS and Android platforms.

You can use this URL scheme to launch Navigator and perform searches for destinations, calculate routes to one or more stops, or start navigating. 

Navigator URLs start with the identifier `arcgis-navigator` and may contain additional parameters that follow the form:

`
arcgis-navigator://?parameter=value&parameter=value
`

The remainder of this document describes the various parameters supported by Navigator.

####Display directions

This is one of the simplest schemes that can be used. It requests and displays directions to a single location. The user’s current location is used as the starting point. The map’s default travel mode is used. 

`stop`: Sets the destination for directions. 

`stopname`: Specifies the name of the stop (*optional*).

The `stop` parameter may either be a set of latitude and longitude coordinates, or a query formatted address. 

The following example URL defines a single stop using a set of latitude and longitude coordinates:

```
arcgis-navigator://?stop=43.651508,-70.290554
```

This example URL defines a single stop using an address: 

```
arcgis-navigator://?stop=103+Fox+St,+Portland,+ME+04101
```

This example URL defines a single stop using a set of latitude and longitude coordinates, and includes a stop name:

```
arcgis-navigator://?stop=43.651508,-70.290554&stopname=Bissell+Bothers
```

If either the name or address contains reserved characters, these should be URL encoded. For example, this URL defines a single stop named ‘Street & Co.’:

```
arcgis-navigator://?stop=33+Wharf+Street,+Portland+ME&stopname=Street+%26+Co.
```

####Custom starting point

Use this to specify a starting point different than the user’s current location:

`start`: Sets the starting point for directions.

`startname`: Specifies the name of the start (optional).

The `start` parameter includes either a set of latitude and longitude coordinates, or a query formatted address.

The following example URL displays directions between Portland International Jetport and Hadlock Field:

```
arcgis-navigator://?stop=271+Park+Ave,+Portland+ME&stopname=Hadlock+Field&start=PWM&startname=Portland+International+Jetport
```

####Multiple stops

Navigator can generate directions to multiple stops. Each stop is denoted with a `stop` parameter. The following example URL displays directions to two stops:

```
arcgis-navigator://?stop=7+Exchange+St,+Portland,+ME&stop=225+Two+Lights+Rd,+Cape+Elizabeth,+ME
```

In the following example the URL contains two stops with stop names:

```
arcgis-navigator://?stop=103+Fox+St,+Portland,+ME+04101&stopname=Rising+Tide&stop=43.651508,-70.290554&stopname=Bissell+Bothers
```
####Optimize route
Navigator can optimize the order of multiple stops, if you include the `optimize` parameter.

`optimize`: Specifies that the order of stops should be optimized. Defaults to false.

The following example URL specifies that the order of the stops should be optimized:

```
arcgis-navigator://?stop=43.65958,-70.25118&stop=43.65761,-70.25388&optimize=true
```

####Travel mode
Navigator maps can include multiple travel modes. If the `travelmode` parameter is specified it will be used when the directions are generated. Otherwise the default travel mode will be used.

`travelmode`: Specifies the transportation method.

The following example URL displays directions to Esri that were generated based on the Trucking Time travel mode:

```
arcgis-navigator://?stop=380+New+York+St,+Redlands,+CA&stopname=Esri&travelmode=Trucking+Time
```

Note that travel modes are defined by the map. The travel modes for the default Esri maps are: 

- Driving Time
- Driving Distance
- Trucking Time
- Trucking Distance
- Walking Time
- Walking Distance
- Rural Driving Time
- Rural Driving Distance

####Navigation mode
To automatically start navigating, specify the `navigate` parameter.

`navigate`: If true, navigation mode will be activated. 

####Specify a callback URL
If you’d like users of your app to be notified when navigation completes, you can include a callback URL. 

`callback`: Specifies the URL to call when navigation is complete. 

`callbackprompt`: Indicates that an alert should appear asking the user if control should be given back to the calling app, and specifies the text of that alert (*optional*).

If the `callback` parameter is specified the app will be notified regardless of the value of the `navigate` parameter. 

*Note:* Your custom URL scheme must be registered with the operating system, for more information on this see [Apple's guide to custom URL Schemes](https://developer.apple.com/library/ios/featuredarticles/iPhoneURLScheme_Reference/Introduction/Introduction.html#//apple_ref/doc/uid/TP40007899) or [Google's guide to Android Intents and Intent Filters](https://developer.android.com/guide/components/intents-filters.html) 

The following example URL specifies that Navigator should enter navigation mode and that the custom app, called my-cool-app in the below URL, should be notified when navigation completes. Because the `callbackprompt` parameter is not present, control will pass directly to the calling app and a prompt will not display. 

```
arcgis-navigator://?stop=43.65958,-70.25118&callbackprompt=My+Cool+App&callback=my-cool-app://
```

####Errors
If an error is encountered when processing a URL scheme, the user will receive an alert.

## Sample code<a name="sample"></a>

Links to sample code

## Resources and related repositories

* [Navigator for ArcGIS Documentation](http://doc.arcgis.com/en/navigator/)
* [Collector for ArcGIS Integration Repository](http://developers.arcgis.com)

Not Esri's doc but still pretty dang useful :-)

* [Apple's guide to custom URL Schemes](https://developer.apple.com/library/ios/featuredarticles/iPhoneURLScheme_Reference/Introduction/Introduction.html#//apple_ref/doc/uid/TP40007899)
* [Google's guide to Intents and Intent Filters](https://developer.android.com/guide/components/intents-filters.html)

## Issues

Find a bug or want to request a new feature? Please let us know by submitting an issue. Thank you!

## Contributing

Anyone and everyone is welcome to contribute. Please see our [guidelines for contributing](https://github.com/esri/contributing).

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
