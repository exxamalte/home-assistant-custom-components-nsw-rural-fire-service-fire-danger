# NSW Rural Fire Service - Fire Danger

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release](https://img.shields.io/github/release/exxamalte/home-assistant-custom-components-nsw-rural-fire-service-fire-danger)](https://gitHub.com/exxamalte/home-assistant-custom-components-nsw-rural-fire-service-fire-danger/releases/)
[![GitHub license](https://img.shields.io/github/license/exxamalte/home-assistant-custom-components-nsw-rural-fire-service-fire-danger)](https://github.com/exxamalte/home-assistant-custom-components-nsw-rural-fire-service-fire-danger/blob/master/LICENSE)
[![Buy me a coffee](https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg)](https://www.buymeacoffee.com/neonninja)
[![neon.ninja](https://img.shields.io/badge/blog-neon.ninja-blue)](https://neon.ninja/2019/02/fire-danger-rating/)

The New South Wales Rural Fire Service provides an [XML feed](http://www.rfs.nsw.gov.au/feeds/fdrToban.xml) that contains the fire danger details for today and tomorrow for districts in the state.

This custom component automatically generates 4 entities:
* Danger level today
* Danger level tomorrow
* Fire ban today
* Fire ban tomorrow

## Installation

Install this component via HACS, then go to "Configuration" -> "Integrations" and search for "NSW Rural Fire Service - Fire Danger".
You have to select your district from the list and then hit "Submit".

All entities will be generated automatically and the state will be updated every 15 minutes from the external feed.


The following attributes will be available with each entity.

| Attribute             | Description                                 |
|-----------------------|---------------------------------------------|
| district              | District name                               |
| region_number         | Internal number of this district            |
| councils              | List of all councils in this district       |
| danger_level_today    | Today's danger level                        |
| danger_level_tomorrow | Tomorrow's danger level                     |
| fire_ban_today        | Indicates whether there is a fire ban today |
| fire_ban_tomorrow     | Indicates whether there is a fire ban today |

**Please note:** Over the winter period, the Rural Fire Service typically does not publish any fire danger rating, and this component just shows "None" as fire danger level.


## More Information

Please [have a look at my blog](https://neon.ninja/2019/02/fire-danger-rating/) which is showcasing an earlier version of this component.

**Please note:** If you have previously used the [custom component published on my GitHub repository](https://github.com/exxamalte/home-assistant-customisations/tree/master/nsw-rural-fire-service-fire-danger), please remove this manually including any template sensors you created.
