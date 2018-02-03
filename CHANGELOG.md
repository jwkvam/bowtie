# CHANGELOG

## 0.7.0 / ???

### Added

  * Implemented `__getitem__` for the layout enabling for example: `app[1, 0:2] = widget`.

### Breaking

  * `row_end` and `column_end` are now exclusive instead of inclusive.

## 0.6.1 / 2018-02-01

### Added

  * Docstring examples of sizing components.
  * More checks to ensure adding components works as expected.

### Fixed

  * Bug which incorrectly tracked which parts of the grid were occupied by widgets.

## 0.6.0 / 2018-01-31

### Added

  * Removed node and webpack dependencies, the only dependency is yarn.
  * Added a run command that simply combines build and serve together.
  * Smarter build process that saves time on subsequent builds.
  * Handle scheduled tasks when running with debug=True (#185)
  * Improve the Docker experience and docs.
  * Always use the latest compiled bundle.

### Breaking

  * Instead of building the app by running `app.build()` you simply return the App instance.
    See the quick start guide for an example.

## 0.5.1 / 2017-12-31

### Added

  * Expose root `View` attributes as `App` attributes (#175).
    You can access `columns` and `rows` from the `App` instance like pre v0.5.
  * Added column and row gap which inserts space between rows and columns.
    Accessible through `column_gap` and `row_gap` on `View` and `App` instances.
  * Added Gitter chat (#179)
  * Many documentation improvements.
  * Drop Python 3.4 support following pandas lead.

## 0.5.0 / 2017-11-19

### Added

  * Create multiple views to create subpages (#158)
  * Cache is now backed by session storage (#160)
  * Link component for switching views without a page reload

### Breaking

  * Renamed `Layout` class to `App`

## 0.4.2 / 2017-09-05

### Added

  * Programmatic control of sliders (#155)
  * Add message popups and better testing of components (#153)

## 0.4.1 / 2017-07-29

### Added

  * Upload widget
  * Dockerfile for building apps

### Fixed

  * Refactored the data Plotly sends on selection to stop crashes, may break some apps

## 0.4.0 / 2017-06-17

### Added

  * Markdown widget (#135)

### Breaking

  * `description` parameter in Layout removed in favor of Markdown widget

## 0.3.3 / 2017-05-24

### Added

  * new textbox feature to update text (#128)

### Fixed

  * fixed issue preventing controllers from added to layout (#128)
  * updated Layout docstring (#125)

## 0.3.2 / 2017-04-26

### Added

  * Support changing socket.io path for nginx (#118)
  * Pager: to request communication from the client (#122)

### Fixed

  * Nouislider
  * Random walk example
  * pydocstyle suggestions

## 0.3.1 / 2017-04-16

### Fixed

  * isinstance calls use correct arguments

## 0.3.0 / 2017-04-13

### Added

  * New more flexible and powerful layout API.
  * Now using CSS Grid instead of Flexbox.
  * Sidebar is now optional.
  * Control widgets can be placed anywhere.

### Breaking

  * `add_visual` is now simply `add`
  * `add_controller` is now `add_sidebar`
  * DropDown is renamed to Dropdown

## 0.2.6 / 2017-03-27

### Added

  * Upgraded to webpack2 and compressing bundle.js (#59)

## 0.2.5 / 2017-03-16

### Fixed

  * Quick start guide and Nouislider css import path (#103)
  * Document the progress indicator functions properly (#101)

## 0.2.4 / 2017-03-06

### Added

  * add cache feature (#98)

## 0.2.3 / 2017-02-26

### Fixed

  * pin js packages to make bowtie stable

## 0.2.2 / 2017-02-20

### Added

  * add default parameter and choose command to dropdown (#91)

### Fixed

  * fix argument counting in python 2 (#89)

## 0.2.1 / 2017-01-14

### Added

  * `min_width` and `min_height` parameters for laying out visual components

## 0.2.0 / 2017-01-01

### Breaking

  * Changed order of arguments to `subscribe`.

### Added

  * Number input widget.
  * Able to subscribe a function to multiple events
