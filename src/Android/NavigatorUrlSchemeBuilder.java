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

package com.esri.urlschemedemo;

import android.content.Intent;
import android.net.Uri;
import android.support.annotation.FloatRange;
import android.support.annotation.NonNull;
import android.text.TextUtils;

import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;
import java.util.ArrayList;
import java.util.List;

public class NavigatorUrlSchemeBuilder {

  //region public inner classes / interfaces

  /**
   * This may be used to constrain the value passed to {@link #setTravelMode(String)} to one of the
   * default Esri travel modes if you're not using a custom travel mode.
   */
  public static class EsriTravelMode {

    public static final String DRIVING_TIME = "Driving Time";

    public static final String DRIVING_DISTANCE = "Driving Distance";

    public static final String TRUCKING_TIME = "Trucking Time";

    public static final String TRUCKING_DISTANCE = "Trucking Distance";

    public static final String WALKING_TIME = "Walking Time";

    public static final String WALKING_DISTANCE = "Walking Distance";

  }

  //endregion public classes / interfaces
  //region constants

  private static final String NAVIGATOR_SCHEME = "arcgis-navigator";

  private static final String CHARSET = "UTF-8";

  private static final String STOP_PARAM = "stop";

  private static final String STOP_NAME_PARAM = "stopname";

  private static final String START_PARAM = "start";

  private static final String START_NAME_PARAM = "startname";

  private static final String OPTIMIZE_PARAM = "optimize";

  private static final String TRAVEL_MODE_PARAM = "travelmode";

  private static final String NAVIGATE_PARAM = "navigate";

  private static final String CALLBACK_URI_PARAM = "callback";

  private static final String CALLBACK_PROMPT_PARAM = "callbackprompt";

  //endregion constants
  //region properties

  private List<Stop> mStops;

  private Stop mStart;

  private Boolean mOptimize;

  private String mTravelMode;

  private Boolean mNavigate;

  private String mCallbackUri;

  private String mCallbackPrompt;

  //endregion properties
  //region constructors

  public NavigatorUrlSchemeBuilder() {
    mStops = new ArrayList<>();
  }

  //endregion constructors
  //region public methods

  /**
   * Adds stop with WGS84 coordinates
   *
   * @param latitude   the latitude coordinate
   * @param longitude  the longitude coordinate
   * @param name       the optional name, may be {@code null}
   * @return this NavigatorUrlSchemeBuilder object to allow for chaining of method calls
   */
  public NavigatorUrlSchemeBuilder addStop(
      @FloatRange(from = -90, to = 90) double latitude,
      @FloatRange(from = -180, to = 180) double longitude,
      String name) {

    mStops.add(new Wgs84Stop(latitude, longitude, name));

    return this;
  }

  /**
   * Adds stop with address
   *
   * @param address  the address
   * @param name     the optional name, may be {@code null}
   * @return this NavigatorUrlSchemeBuilder object to allow for chaining of method calls
   */
  public NavigatorUrlSchemeBuilder addStop(@NonNull String address, String name) {
    mStops.add(new AddressStop(address, name));

    return this;
  }

  /**
   * Sets start with WGS84 coordinates
   *
   * @param latitude   the latitude coordinate
   * @param longitude  the longitude coordinate
   * @param name       the optional name, may be {@code null}
   * @return this NavigatorUrlSchemeBuilder object to allow for chaining of method calls
   */
  public NavigatorUrlSchemeBuilder setStart(
      @FloatRange(from = -90, to = 90) double latitude,
      @FloatRange(from = -180, to = 180) double longitude,
      String name) {

    mStart = new Wgs84Stop(latitude, longitude, name);

    return this;
  }

  /**
   * Sets start with address
   *
   * @param address  the address
   * @param name     the optional name, may be {@code null}
   * @return this NavigatorUrlSchemeBuilder object to allow for chaining of method calls
   */
  public NavigatorUrlSchemeBuilder setStart(@NonNull String address, String name) {
    mStart = new AddressStop(address, name);

    return this;
  }

  /**
   * Sets the optimize flag
   *
   * @param optimize  {@code true} if stops should be re-ordered optimally, {@code false} otherwise
   * @return this NavigatorUrlSchemeBuilder object to allow for chaining of method calls
   */
  public NavigatorUrlSchemeBuilder setOptimize(boolean optimize) {
    mOptimize = optimize;

    return this;
  }

  /**
   * Sets the travel mode - this may be one of the static {@link EsriTravelMode} properties, or it
   * can be a custom value if the map's transportation network supports it.
   *
   * @param travelMode  the travel mode name
   * @return this NavigatorUrlSchemeBuilder object to allow for chaining of method calls
   */
  public NavigatorUrlSchemeBuilder setTravelMode(String travelMode) {
    mTravelMode = travelMode;

    return this;
  }

  /**
   * Sets the navigate flag
   *
   * @param navigate  {@code true} if Navigator should automatically start navigating, {@code false} otherwise
   * @return this NavigatorUrlSchemeBuilder object to allow for chaining of method calls
   */
  public NavigatorUrlSchemeBuilder setNavigate(boolean navigate) {
    mNavigate = navigate;

    return this;
  }

  /**
   * Sets the callback, which should be registered as the {@code data} node of an activity's
   * {@code intent-filter} in the manifest.
   *
   * @param callbackUri  the callback
   * @return this NavigatorUrlSchemeBuilder object to allow for chaining of method calls
   */
  public NavigatorUrlSchemeBuilder setCallbackUri(String callbackUri) {
    mCallbackUri = callbackUri;

    return this;
  }

  /**
   * Sets the callback prompt which will be shown when navigation completes.
   *
   * @param callbackPrompt  the callback prompt
   * @return this NavigatorUrlSchemeBuilder object to allow for chaining of method calls
   */
  public NavigatorUrlSchemeBuilder setCallbackPrompt(String callbackPrompt) {
    mCallbackPrompt = callbackPrompt;

    return this;
  }

  /**
   * Creates a Uri object which has query parameters based on the values that have been previously
   * passed to this builder.
   *
   * @return the Uri
   */
  public Uri buildUri() {
    Uri.Builder builder = new Uri.Builder()
        .scheme(NAVIGATOR_SCHEME)
        .authority("");

    if (mStart != null) {
      builder.appendQueryParameter(START_PARAM, encode(mStart.getValue()));
      String name = mStart.getName();
      if (name != null) {
        builder.appendQueryParameter(START_NAME_PARAM, encode(name));
      }
    }

    if (!mStops.isEmpty()) {
      for (Stop stop : mStops) {
        builder.appendQueryParameter(STOP_PARAM, encode(stop.getValue()));
        String name = stop.getName();
        if (name != null) {
          builder.appendQueryParameter(STOP_NAME_PARAM, encode(name));
        }
      }
    } else {
      throw new RuntimeException("Must have at least one stop!");
    }

    if (mOptimize != null) {
      builder.appendQueryParameter(OPTIMIZE_PARAM, Boolean.toString(mOptimize));
    }

    if (mTravelMode != null) {
      mTravelMode = mTravelMode.trim();
      if (!TextUtils.isEmpty(mTravelMode)) {
        builder.appendQueryParameter(TRAVEL_MODE_PARAM, encode(mTravelMode));
      }
    }

    if (mNavigate != null) {
      builder.appendQueryParameter(NAVIGATE_PARAM, Boolean.toString(mNavigate));
    }

    if (mCallbackUri != null) {
      builder.appendQueryParameter(CALLBACK_URI_PARAM, encode(mCallbackUri));
    }

    if (mCallbackPrompt != null) {
      builder.appendQueryParameter(CALLBACK_PROMPT_PARAM, encode(mCallbackPrompt));
    }

    return builder.build();
  }

  public Intent buildIntent() {
    Uri uri = buildUri();

    return new Intent(Intent.ACTION_VIEW, uri);
  }

  //endregion public methods
  //region private methods

  private static String encode(String value) {
    try {
      return URLEncoder.encode(value, CHARSET);
    } catch (UnsupportedEncodingException e) {
      return Uri.encode(value);
    }
  }

  //endregion private methods
  //region private inner classes

  abstract private class Stop {

    private String mName;

    abstract String getValue();

    public Stop(String name) {
      mName = name;
    }

    public String getName() {
      return mName;
    }

  }

  private class Wgs84Stop extends Stop {

    private double mLatitude;

    private double mLongitude;

    public Wgs84Stop(
        @FloatRange(from = -90, to = 90) double latitude,
        @FloatRange(from = -180, to = 180) double longitude,
        String name) {

      super(name);

      mLatitude = latitude;
      mLongitude = longitude;
    }

    @Override
    String getValue() {
      return Double.toString(mLatitude) + "," + Double.toString(mLongitude);
    }

  }

  private class AddressStop extends Stop {

    private String mAddress;

    public AddressStop(@NonNull String address, String name) {
      super(name);

      mAddress = address;
    }

    @Override
    public String getValue() {
      return mAddress;
    }

  }

  //endregion private inner classes

}
