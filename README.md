# NSW Rural Fire Service - Fire Danger

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release](https://img.shields.io/github/release/exxamalte/home-assistant-custom-components-nsw-rural-fire-service-fire-danger)](https://gitHub.com/exxamalte/home-assistant-custom-components-nsw-rural-fire-service-fire-danger/releases/)
[![GitHub license](https://img.shields.io/github/license/exxamalte/home-assistant-custom-components-nsw-rural-fire-service-fire-danger)](https://github.com/exxamalte/home-assistant-custom-components-nsw-rural-fire-service-fire-danger/blob/master/LICENSE)

The NSW Rural Fire Service provides an [XML feed](http://www.rfs.nsw.gov.au/feeds/fdrToban.xml) that contains the fire danger
details for today and tomorrow for districts in the state.

This custom component is implemented as a simple sensor that fetches the feed
and stores all details of the configured district. You can then use template
sensors to present these details in Home Assistant as you like.

Please note: This version is compatible with Home Assistant version 0.117 onwards.

## Installation

### Install custom component code
In your [configuration folder](https://www.home-assistant.io/docs/configuration/)
create subfolder `<config>/custom_components` and copy the folder
`nsw_rural_fire_service_fire_danger` into the new `custom_components` folder.

Please note: This folder structure will work at least from Home Assistant 
version 0.88 onwards. If you are using an older version, you will need to create
sub-folders `<config>/custom_components/sensor` and move the `sensor.py` file
in there and rename it to `nsw_rural_fire_service_fire_danger.py`.

### Install dependencies
This custom component comes with its own `manifest.json` and thus dependencies
should be installed automatically. 

Both third-party libraries are also used by the `rest` integration, so they
are likely already installed if you are using that integration.


## Configuration Example


### Fire Danger Sensor

Have a look at the XML feed at http://www.rfs.nsw.gov.au/feeds/fdrToban.xml
and find your district. The district's name must be configured as 
`district_name` as shown in the following example:

```yaml
sensor:
  - platform: nsw_rural_fire_service_fire_danger
    district_name: Greater Sydney Region
```

The above configuration will generate a sensor with entity id 
`sensor.fire_danger_in_greater_sydney_region` which is further used in the
examples below.

The sensor's state will either be `ok` or `unknown` if no data could be retrieved.

The following attributes will be available for use in `template` sensors.

| Attribute             | Description                                 |
|-----------------------|---------------------------------------------|
| district              | District name                               |
| region_number         | Internal number of this district            |
| councils              | List of all councils in this district       |
| danger_level_today    | Today's danger level                        |
| danger_level_tomorrow | Tomorrow's danger level                     |
| fire_ban_today        | Indicates whether there is a fire ban today |
| fire_ban_tomorrow     | Indicates whether there is a fire ban today |


### Danger Level Today

```yaml
sensor:
  - platform: template
    sensors:
      fire_danger_level_today:
        friendly_name: "Danger Level Today"
        value_template: "{{ state_attr('sensor.fire_danger_in_greater_sydney_region', 'danger_level_today') }}"
        icon_template: mdi:speedometer
```

### Fire Ban Today
```yaml
binary_sensor:
  - platform: template
    sensors:
      fire_ban_today:
        friendly_name: "Fire Ban Today"
        value_template: "{{ state_attr('sensor.fire_danger_in_greater_sydney_region', 'fire_ban_today') }}"
        device_class: safety
```
