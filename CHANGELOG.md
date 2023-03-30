# Changes

## 0.14 (31/03/2023)
* Fix for signature change in rest data class in Home Assistant 2023.4.0.
  **Please upgrade, previous versions of this integration will not work with 2023.4.0+.** 
* Added Portuguese translation (thanks @ViPeR5000).
* Added German translation.

## 0.13 (13/02/2023)
* Fixed the way how council names are parsed, removing whitespace around the name.
* Fixed internal configuration setup process (probably won't have any effect on users).
* Added automated testing.
* Bump library version dependencies.

## 0.12 (01/11/2022)
* Added option to automatically convert value "NONE" into "No Rating".
* Fixed issue with district name "ACT" in standard feed.
* Added integration type "service".

## 0.11 (20/09/2022)
* Added support for an extended feed that provides a forecast for 4 days.
* Replaced deprecated method.
* Now requires at least Home Assistant 2022.8.0.

## 0.10 (19/07/2022)
* **Breaking change:** Migrated to new standardised entity naming schema which likely changes the names of your entities.
* Now requires at least Home Assistant 2022.7.0.
* Fixed an issue causing an error when removing this integration.
* Bump library version dependencies.
* Code improvements based on recent Home Assistant core changes.

## 0.9 (15/02/2022)
* Now requires at least Home Assistant 2021.12.0.
* Replaced deprecated methods and constants.
* Migrated to `DataUpdateCoordinator` to reduce code complexity and improve performance.
* Code housekeeping.

## 0.8 (06/05/2021)
* Add IoT class to manifest.

## 0.7 (06/02/2021)
* Add version to manifest.

## 0.6 (02/01/2021)
* Fix for signature change in rest data class now also covers Home Assistant 2021.1+.

## 0.5 (04/12/2020)
* Fix for signature change in rest data class now also covers Home Assistant 2020.12+.

## 0.4 (03/12/2020)
* Fix for signature change in rest data class in Home Assistant 0.119.
* Code housekeeping (black formatting, isort, flake8).

## 0.3 (30/10/2020)
* Shorten name and entity id to avoid database issues.

## 0.2 (28/10/2020)
* Supporting configuration from UI.
* Automatically generates 4 sensors.
* Fixed dependencies.

## 0.1 (24/10/2020)
* Initial release, compatible with Home Assistant version 0.117.0b3 onwards.
* Added HACS related files.
