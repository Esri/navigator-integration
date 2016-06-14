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


import Foundation

private extension String {
    private func queryArgumentEncodedString() -> String? {
        let charSet = NSCharacterSet.URLQueryAllowedCharacterSet().mutableCopy() as! NSMutableCharacterSet
        charSet.removeCharactersInString("&")

        return stringByAddingPercentEncodingWithAllowedCharacters(charSet)
    }
}

public final class NavigatorURLScheme {

    public static let scheme = "arcgis-navigator:"
    
    public static var canOpen: Bool {
        return UIApplication.sharedApplication().canOpenURL(NSURL(string: scheme)!)
    }

    public struct URLSchemeError: ErrorType {
        let unencodableString: String
    }

    public enum LocationType {

        case WGS84(point: AGSPoint)
        case Address(String)

        public func queryArgument() throws -> String {
            switch self {
            case .WGS84(point: let point):
                return "\(point.y),\(point.x)"
            case .Address(let address):
                if let address = address.queryArgumentEncodedString() {
                    return address
                } else {
                    throw URLSchemeError(unencodableString:address)
                }
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

    public init(optimizeRoute optimize: Bool = false, startNavigating navigate: Bool = false) {
        self.optimize = optimize
        self.navigate = navigate
    }

    public func setStartAtLocation(location: LocationType, withName name: String? = nil) {
        start = NavigatorStop(location: location, name: name, stopType: .Start)
    }

    public func addStopAtLocation(location: LocationType, withName name:String? = nil) {
        stops.append(NavigatorStop(location: location, name: name, stopType: .Stop))
    }

    public func setCallbackScheme(scheme: String, prompt: String? ) {
        callback = Callback(scheme: scheme, prompt: prompt)
    }

    public func generateURL() throws -> NSURL? {

        var stringBuilder = "\(NavigatorURLScheme.scheme)//?optimize=\(optimize ? "true" : "false")&navigate=\(navigate ? "true" : "false")"

        if let start = try start?.encodeStop() {
            stringBuilder += start
        }

        if !stops.isEmpty {
            let encodedStops = try stops.flatMap({ return try $0.encodeStop() }).joinWithSeparator("")
            stringBuilder += encodedStops
        }

        if let callback = try callback?.encodedArgumentString() {
            stringBuilder += callback
        }

        return NSURL(string: stringBuilder)
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

        private func encodeStop() throws -> String {

            let nameArgument: String

            if let name = name {
                if let encoded = name.queryArgumentEncodedString() {
                    nameArgument = "&\(stopType.rawValue)name=\(encoded)"
                } else {
                    throw URLSchemeError(unencodableString: name)
                }
            } else {
                nameArgument = ""
            }

            return "&\(stopType.rawValue)=\(try location.queryArgument())\(nameArgument)"
        }
    }

    private struct Callback {

        let callbackScheme: String
        let callbackPrompt: String?

        init(scheme: String, prompt: String?) {
            callbackScheme = scheme
            callbackPrompt = prompt
        }

        public func encodedArgumentString() throws -> String {

            let encodedScheme: String
            if let encoded = callbackScheme.queryArgumentEncodedString() {
                encodedScheme = "&callback=\(encoded)"
            } else {
                throw URLSchemeError(unencodableString: callbackScheme)
            }

            let encodedPrompt: String
            if let prompt = callbackPrompt {
                if let encoded = prompt.queryArgumentEncodedString() {
                    encodedPrompt = "&callbackprompt=\(encoded)"
                } else {
                    throw URLSchemeError(unencodableString: prompt)
                }
            } else {
                encodedPrompt = ""
            }
            
            return "\(encodedScheme)\(encodedPrompt)"
        }
    }
}