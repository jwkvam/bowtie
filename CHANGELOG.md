# CHANGELOG

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
