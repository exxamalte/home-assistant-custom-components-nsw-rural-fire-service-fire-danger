# NSW Rural Fire Service - Fire Danger

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release](https://img.shields.io/github/release/exxamalte/home-assistant-custom-components-nsw-rural-fire-service-fire-danger)](https://gitHub.com/exxamalte/home-assistant-custom-components-nsw-rural-fire-service-fire-danger/releases/)
[![GitHub license](https://img.shields.io/github/license/exxamalte/home-assistant-custom-components-nsw-rural-fire-service-fire-danger)](https://github.com/exxamalte/home-assistant-custom-components-nsw-rural-fire-service-fire-danger/blob/master/LICENSE)

The New South Wales Rural Fire Service provides an 
[XML feed](http://www.rfs.nsw.gov.au/feeds/fdrToban.xml) that contains the 
fire danger details for today and tomorrow for districts in the state.

This custom component is implemented as a simple sensor that fetches the feed
and stores all details of the configured district. You can then use template
sensors to present these details in Home Assistant as you like.

Please note: Over the winter period, the Rural Fire Service typically does not
publish any fire danger rating, and this component just shows "None" as fire
danger level.

## Installation

Install this component via HACS, configure the main sensor and any template
sensors in your `configuration` and then restart Home Assistant.


## Configuration Example

### Fire Danger Sensor

The following [districts are supported by this integration](http://www.rfs.nsw.gov.au/feeds/fdrToban.xml):
* Far North Coast
* North Coast
* Greater Hunter
* Greater Sydney Region
* Illawarra/Shoalhaven
* Far South Coast
* Monaro Alpine
* ACT
* Southern Ranges
* Central Ranges
* New England
* Northern Slopes
* North Western
* Upper Central West Plains
* Lower Central West Plains
* Southern Slopes
* Eastern Riverina
* Southern Riverina
* Northern Riverina
* South Western
* Far Western

Please pick the district you live in and configure it as `district_name` as 
shown in the following example:

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

The following sensor shows today's danger level.

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

The following binary sensor indicates whether there is a fire ban today.

```yaml
binary_sensor:
  - platform: template
    sensors:
      fire_ban_today:
        friendly_name: "Fire Ban Today"
        value_template: "{{ state_attr('sensor.fire_danger_in_greater_sydney_region', 'fire_ban_today') }}"
        device_class: safety
```
