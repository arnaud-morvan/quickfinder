##  Changelog

** Version 3.0 ** 25.06.2014

* Complete redesign to centralize all searches in QGIS
* Project search allows to search features in every layer using a full-text search.
  The layers are defined by the user and the search entries are saved in a SQLite file.
* Web-services: searches can be performed on online services: OpenStreetMap and GeoMapFish are available as of today.
* Search is performed through a line edit in the toolbars
* All results are displayed in a single tree

** Version 2.6.2** 11.09.2013

* resize field combo box

** Version 2.6.1** 20.08.2013

* fix using LIKE operator for non-text fields

** Version 2.6** 30.07.2013

* Auto choose current layer when opening the dock
* Improved text search: take care of accents
* Fix text search for new API
* Auto select operator from chosen field type

** Version 2.5** 26.07.2013

* Sort layers by name

** Version 2.4.1** 23.07.2013

* Fix crash when opening a new project

** Version 2.4** 11.07.2013

* Option for dock area
* New SVG icons

** Version 2.3** 20.06.2013

* New API for QGIS 2.0
* Remove 1.8 compatibility
* Fix search in non-geometric layers

**Version 2.2** 18.04.2013

* Performance improvement (for QGIS 2.0)
* Added factor when scaling canvas extent
* Disable scale box if pan is not selected
* Use external [qgistools library](https://github.com/3nids/qgistools/)

**Version 2.1** 01.03.2013

* Compatibility with QGIS 1.8

**Version 2.0** 01.03.2013

* Search also in fields
* fix: launch layers at start

**Version 1.2** 11.02.2013

* Do not list raster layers in the combo box

**Version 1.1** 11.02.2013

* Adapted to new vector API
