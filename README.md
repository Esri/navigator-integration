# Navigator custom URL scheme

This is a multi-language repository that contains documentation and sample code for creating custom URL schemes in [Navigator for ArcGIS](http://doc.arcgis.com/en/navigator/).

## Supported versions

* Navigator for ArcGIS 2.0.0 or later

## What's included

* [Documentation](#documentation) on the URL scheme structure
* [Sample code](#sample) for iOS (Swift), Android (Java), and Python

## Get started

Read the following documentation and clone down the appropriate language into your development environment.
<a name="documentation"></a>

## Documentation

#### What is the Navigator for ArcGIS URL scheme?

A URL scheme allows you to launch a native app from another app, website, or email. You can set options in the URL that will be passed to the app you want to open, causing it to perform specific functions, such as searching for destinations, calculating routes to one or more stops, and navigating. This capability is available on the iOS and Android platforms.

#### Basic URL scheme structure

All Navigator URL schemes start with the identifier `arcgis-navigator` and can contain additional parameters that follow the form:

`
arcgis-navigator://?parameter=value&parameter=value
`

The rest of this topic describes the various parameters Navigator currently supports.

#### Display directions to a single location

This is one of the simplest schemes that can be used. It requests and displays directions to a single location. The user’s current location is used as the starting point. The map’s default travel mode is used. 

`stop`: Sets the destination for directions. 

`stopname`: Specifies the name of the stop (*optional*).

The `stop` parameter can be either a set of latitude and longitude coordinates, or a query formatted address. 

The following example URL defines a single stop using a set of latitude and longitude coordinates:

```
arcgis-navigator://?stop=43.651508,-70.290554
```

This example URL defines a single stop using an address: 

```
arcgis-navigator://?stop=103+Fox+St,+Portland,+ME+04101
```

This example URL defines a single stop using a set of latitude and longitude coordinates and also includes a stop name:

```
arcgis-navigator://?stop=43.651508,-70.290554&stopname=Bissell+Bothers
```

If the name or address contains reserved characters, these should be URL encoded. For example, this URL defines a single stop named Street & Co.:

```
arcgis-navigator://?stop=33+Wharf+Street,+Portland+ME&stopname=Street+%26+Co.
```

#### Specify a custom starting point

Use this to specify a starting point different than the user’s current location:

`start`: Sets the starting point for directions.

`startname`: Specifies the name of the start (*optional*).

Note that specifying a startname does necessitate specifying a stopname.

The `start` parameter includes either a set of latitude and longitude coordinates, or a query formatted address.

The following example URL displays directions between Portland International Jetport and Hadlock Field:

```
arcgis-navigator://?stop=271+Park+Ave,+Portland+ME&stopname=Hadlock+Field&start=PWM&startname=Portland+International+Jetport
```

#### Generate directions to multiple stops

Navigator can generate directions to multiple stops. Each stop is denoted with a `stop` parameter. The following example URL displays directions to two stops:

```
arcgis-navigator://?stop=7+Exchange+St,+Portland,+ME&stop=225+Two+Lights+Rd,+Cape+Elizabeth,+ME
```

The following example contains two stops with two stop names:

```
arcgis-navigator://?stop=103+Fox+St,+Portland,+ME+04101&stopname=Rising+Tide&stop=43.651508,-70.290554&stopname=Bissell+Bothers
```

Note that if there's a stopname associated with one of the stops in your URL, all of the stops must have stopnames associated with them in the URL, otherwise it will not calculate a route. For example, if the above example URL contained two stops but just one stop name, it would not calculate a route. 

#### Enable route optimization 
Navigator can optimize the order of multiple stops if you include the `optimize` parameter in a URL scheme.

`optimize`: Specifies that the order of stops should be optimized. Defaults to false.

The following example URL specifies that the order of the stops should be optimized:

```
arcgis-navigator://?stop=43.65958,-70.25118&stop=43.65761,-70.25388&optimize=true
```

#### Set the travel mode
Navigator maps can include multiple travel modes. If the `travelmode` parameter is specified, it will be used when the directions are generated. Otherwise, the default travel mode will be used.

`travelmode`: Specifies the transportation method.

The following example URL displays directions to Esri that are generated based on the Trucking Time travel mode:

```
arcgis-navigator://?stop=380+New+York+St,+Redlands,+CA&stopname=Esri&travelmode=Trucking+Time
```

Note that the map defines which travel modes are available. The default Esri maps have the following travel modes: 

- Driving Time
- Driving Distance
- Trucking Time
- Trucking Distance
- Walking Time
- Walking Distance
- Rural Driving Time
- Rural Driving Distance

#### Automatically start navigating
To have Navigator automatically start navigating, specify the `navigate` parameter.

`navigate`: If true, navigation mode will be activated. 

#### Enable notifications when navigation completes
If you’d like your app users to be notified when navigation completes, include a callback URL. 

`callback`: Specifies which URL to call when navigation completes. If the `callback` parameter is specified, the app will be notified when navigation completes.  

`callbackprompt`: Indicates the app name that should be used when Navigator asks the user if control should be given back to the calling app (*optional*).

Note that your custom URL scheme must be registered with the operating system. For more information on this see [Apple's guide to custom URL Schemes](https://developer.apple.com/library/ios/featuredarticles/iPhoneURLScheme_Reference/Introduction/Introduction.html#//apple_ref/doc/uid/TP40007899) or [Google's guide to Android Intents and Intent Filters](https://developer.android.com/guide/components/intents-filters.html). 

The following URL specifies that Navigator should enter navigation mode and that the custom app, called my-cool-app in this example, should be notified when navigation completes. Since the `callbackprompt` parameter is not present, control will pass directly to the calling app and a prompt will not display. 

```
arcgis-navigator://?stop=43.65958,-70.25118&callbackprompt=My+Cool+App&callback=my-cool-app://
```

#### Errors
If an error is encountered when processing a URL scheme, the user will receive an alert.
<a name="sample"></a>

## Sample code

* [Swift (iOS)](https://github.com/Esri/navigator-integration/tree/master/src/Swift)
* [Java (Android)](https://github.com/Esri/navigator-integration/tree/master/src/Android)
* [Python](https://github.com/Esri/navigator-integration/tree/master/src/Python)

## Resources and related repositories

* [Navigator for ArcGIS documentation](http://doc.arcgis.com/en/navigator/)
* [Collector for ArcGIS integration repository](http://developers.arcgis.com)

Not Esri's doc but still pretty dang useful :-)

* [Apple's guide to custom URL schemes](https://developer.apple.com/library/ios/featuredarticles/iPhoneURLScheme_Reference/Introduction/Introduction.html#//apple_ref/doc/uid/TP40007899)
* [Google's guide to intents and intent filters](https://developer.android.com/guide/components/intents-filters.html)

## Issues

Find a bug or want to request a new feature? Please let us know by [submitting an issue](https://github.com/Esri/navigator-integration/issues/new). Thank you!

## Contribute

Anyone and everyone is welcome to contribute. See our [guidelines for contributing](https://github.com/esri/contributing).

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
