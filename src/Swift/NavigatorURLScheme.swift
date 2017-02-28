/*

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

 */

import CoreLocation
import Foundation
import UIKit

fileprivate extension String {
    fileprivate func queryArgumentEncodedString() -> String? {
        var charSet = NSCharacterSet.urlQueryAllowed
        charSet.remove(charactersIn: "&")
        return addingPercentEncoding(withAllowedCharacters: charSet)
    }
}

public final class NavigatorURLScheme {

    public static let scheme = "arcgis-navigator:"

    public static var canOpen: Bool {
        return UIApplication.shared.canOpenURL(URL(string: scheme)!)
    }

    public struct URLSchemeError: Error {
        let unencodableString: String
    }

    public enum LocationType {

        case coordinate(CLLocationCoordinate2D)
        case address(String)

        public func queryArgument() -> String? {
            switch self {
            case .coordinate(let coord):
                return "\(coord.latitude),\(coord.longitude)"
            case .address(let address):
                return address.queryArgumentEncodedString()
            }
        }
    }

    private enum StopType: String {

        case Start = "start"
        case Stop = "stop"
    }

    public let optimize: Bool

    public let navigate: Bool

    private var start: NavigatorStop?

    private var stops = [NavigatorStop]()

    private var callback: Callback?

    public convenience init(destination: LocationType, name: String? = nil) {
        self.init()
        addStop(at: destination, named: name)
    }

    public init(optimizeRoute optimize: Bool = false, startNavigating navigate: Bool = false) {
        self.optimize = optimize
        self.navigate = navigate
    }

    public func setStart(at location: LocationType, named name: String? = nil) {
        start = NavigatorStop(location: location, name: name, stopType: .Start)
    }

    public func addStop(at location: LocationType, named name: String? = nil) {
        stops.append(NavigatorStop(location: location, name: name, stopType: .Stop))
    }

    public func setCallbackScheme(scheme: String, prompt: String? ) {
        callback = Callback(scheme: scheme, prompt: prompt)
    }

    public var url: URL? {

        var stringBuilder = "\(NavigatorURLScheme.scheme)//?optimize=\(optimize ? "true" : "false")&navigate=\(navigate ? "true" : "false")"

        if start != nil {
            guard let start = start!.encodeStop() else {
                return nil
            }
            stringBuilder += start
        }

        if !stops.isEmpty {
            let encodedStops = stops.flatMap { $0.encodeStop() }
            guard encodedStops.count == stops.count else {
                return nil
            }
            let encodedStopsString = encodedStops.joined(separator: "")
            stringBuilder += encodedStopsString
        }

        if callback != nil {
            guard let callback = callback?.encodedArgumentString() else {
                return nil
            }
            stringBuilder += callback
        }

        return URL(string: stringBuilder)
    }

    private struct NavigatorStop {

        let location: LocationType
        let name: String?
        let stopType: StopType

        public init(location: LocationType,  name: String?, stopType: StopType) {
            self.location = location
            self.name = name
            self.stopType = stopType
        }

        fileprivate func encodeStop() -> String? {

            guard let queryArgument = location.queryArgument() else {
                return nil
            }

            let nameArgument: String

            if let name = name {

                guard let encoded = name.queryArgumentEncodedString() else {
                    return nil
                }

                nameArgument = "&\(stopType.rawValue)name=\(encoded)"
            } else {
                nameArgument = ""
            }

            return "&\(stopType.rawValue)=\(queryArgument)\(nameArgument)"
        }
    }

    private struct Callback {

        let callbackScheme: String
        let callbackPrompt: String?

        init(scheme: String, prompt: String?) {
            callbackScheme = scheme
            callbackPrompt = prompt
        }

        public func encodedArgumentString() -> String? {


            guard let encoded = callbackScheme.queryArgumentEncodedString() else {
                return nil
            }

            let encodedScheme = "&callback=\(encoded)"

            let encodedPrompt: String
            if let prompt = callbackPrompt {
                guard let encoded = prompt.queryArgumentEncodedString() else {
                    return nil
                }
                
                encodedPrompt = "&callbackprompt=\(encoded)"
            } else {
                encodedPrompt = ""
            }
            
            return "\(encodedScheme)\(encodedPrompt)"
        }
    }
}
