# NSW Rural Fire Service - Fire Danger

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![Build Status](https://github.com/exxamalte/home-assistant-custom-components-nsw-rural-fire-service-fire-danger/workflows/CI/badge.svg?branch=main)](https://github.com/exxamalte/home-assistant-custom-components-nsw-rural-fire-service-fire-danger/actions?workflow=CI)
[![codecov](https://codecov.io/gh/exxamalte/home-assistant-custom-components-nsw-rural-fire-service-fire-danger/branch/main/graph/badge.svg?token=PIO76MIVIO)](https://codecov.io/gh/exxamalte/home-assistant-custom-components-nsw-rural-fire-service-fire-danger)
[![GitHub release](https://img.shields.io/github/release/exxamalte/home-assistant-custom-components-nsw-rural-fire-service-fire-danger)](https://gitHub.com/exxamalte/home-assistant-custom-components-nsw-rural-fire-service-fire-danger/releases/)
[![GitHub license](https://img.shields.io/github/license/exxamalte/home-assistant-custom-components-nsw-rural-fire-service-fire-danger)](https://github.com/exxamalte/home-assistant-custom-components-nsw-rural-fire-service-fire-danger/blob/master/LICENSE)
[![Buy me a coffee](https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg)](https://www.buymeacoffee.com/neonninja)
[![neon.ninja](https://img.shields.io/badge/blog-neon.ninja-blue)](https://neon.ninja/2019/02/fire-danger-rating/)

The New South Wales Rural Fire Service provides an [XML feed](http://www.rfs.nsw.gov.au/feeds/fdrToban.xml) that contains the fire danger details for today and tomorrow for districts in the state.

This custom component automatically generates the following entities:
* Danger level today
* Danger level tomorrow
* Danger level day 3 (extended feed only)
* Danger level day 4 (extended feed only)
* Fire ban today
* Fire ban tomorrow
* Fire ban day 3 (extended feed only)
* Fire ban day 4 (extended feed only)

{% if installed %}
## Notes
{% if version_installed.replace("v", "").replace(".","") | int <= 5  %}
* Please update to v0.5 when upgrading to Home Assistant 2020.12.
{% endif %}
{% if version_installed.replace("v", "").replace(".","") | int <= 6  %}
* Please update to v0.6 when upgrading to Home Assistant 2021.1 or later.
{% endif %}
{% if version_installed.replace("v", "").replace(".","") | int <= 9  %}
* Please update to v0.9 when upgrading to Home Assistant 2021.12 or later.
{% endif %}
{% if version_installed.replace("v", "").replace(".","") | int <= 10  %}
* Please update to v0.10 when upgrading to Home Assistant 2022.07 or later.
{% endif %}
{% if version_installed.replace("v", "").replace(".","") | int <= 11  %}
* Please update to v0.11 when upgrading to Home Assistant 2022.12 or later.
{% endif %}
{% if version_installed.replace("v", "").replace(".","") | int <= 14  %}
* Please update to v0.15 when upgrading to Home Assistant 2023.4 or later.
{% endif %}
{% if version_installed.replace("v", "").replace(".","") | int <= 15  %}
* Please update to v0.16 when upgrading to Home Assistant 2023.5 or later.
{% endif %}
{% endif %}

## Installation

Install this component via HACS, then go to "Configuration" -> "Integrations" and search for "NSW Rural Fire Service - Fire Danger".
You have to select your district from the list, choose a feed, and then hit "Submit".

There are currently two different feeds supported:
* Standard: This provides a forecast for today and tomorrow only, and appears as a dedicated feed on the RFS's website.
* Extended: This provides a forecast for 4 days, and is [used on the RFS's website](https://www.rfs.nsw.gov.au/fire-information/fdr-and-tobans). 

There is currently no option to switch between the two feeds, so please delete and recreate the configuration if you want to switch feeds.

The actual feed contains the value "NONE" in case no rating has been issued. This is converted into `None` which has a special meaning in Python and hence in Home Assistant, 
and which subsequently may cause confusion when used in automations. There is an option available when setting up this integration to automatically convert this into "No Rating" 
which is the term used on the RFS website.

**Please note:** If you have previously used the [custom component published on my GitHub repository](https://github.com/exxamalte/home-assistant-customisations/tree/master/nsw-rural-fire-service-fire-danger), please remove this manually including any template sensors you created.

All entities will be generated automatically and the state will be updated every 15 minutes from the external feed.


The following attributes will be available with each entity.

| Attribute             | Description                                         |
|-----------------------|-----------------------------------------------------|
| district              | District name                                       |
| region_number         | Internal number of this district                    |
| councils              | List of all councils in this district               |
| danger_level_today    | Today's danger level                                |
| danger_level_tomorrow | Tomorrow's danger level                             |
| danger_level_day3     | Danger level in two days                            |
| danger_level_day4     | Danger level in three days                          |
| fire_ban_today        | Indicates whether there is a fire ban today         |
| fire_ban_tomorrow     | Indicates whether there is a fire ban tomorrow      |
| fire_ban_day3         | Indicates whether there is a fire ban in two days   |
| fire_ban_day4         | Indicates whether there is a fire ban in three days |

**Please note:** Over the winter period, the Rural Fire Service typically does not publish any fire danger rating, and this component just shows "None" as fire danger level.


## More Information

Please [have a look at my blog](https://neon.ninja/2019/02/fire-danger-rating/) which is showcasing an earlier version of this component.


## Configuration Details

The following [districts are currently supported by this integration](http://www.rfs.nsw.gov.au/feeds/fdrToban.xml):
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

**Please note:** The RFS has recently changed the district name "ACT" to "The Australian Capital Territory". 
For backwards compatibility reasons I decided to keep the name "ACT" for now. Please let me know if you are a 
resident of the ACT and would prefer having the full name in this integration.
