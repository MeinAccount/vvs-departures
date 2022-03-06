# vvs-departures
[![Docker](https://github.com/MeinAccount/vvs-departures/actions/workflows/docker-image.yml/badge.svg)](https://github.com/MeinAccount/vvs-departures/actions/workflows/docker-image.yml)

Shows real time public transport information in Stuttgart, Germany

## configuration
Set `VVS_BUTTONS` environment variable newline separated list of `Station ID;Station Name`, see https://www.opendata-oepnv.de/ht/de/organisation/verkehrsverbuende/vvs/startseite?tx_vrrkit_view%5Bdataset_name%5D=haltestellen-vvs&tx_vrrkit_view%5Bdataset_formats%5D%5B0%5D=CSV&tx_vrrkit_view%5Baction%5D=details&tx_vrrkit_view%5Bcontroller%5D=View
