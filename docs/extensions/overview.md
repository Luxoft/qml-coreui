# QML CoreUI Extensions

!!!info

    This material is work in progress and will change!


A set of common extensions used for the CoreUI Architecture

## CoreUI SDK

The CoreUI SDK is based on top of the Qt Automotive SDK. At its heart it is a collection of extensions and a comprehensive guide to build user interfaces for embedded systems. The SDK is accompanied by the admin tool to generate project based on the CoreUI principles.

CoreUI extends Qt Automotive by providing a clean architecture to establish  mutli process user interface for embedded systems.

* CoreUI Guide
* CoreUI Extensions
* CoreUI Admin
* CoreUI Demo


## Building the extension

The extension are Qt static libraries and plugins. The plugins are build into the $BUILD_DIR/imports folder and the static libraries into the $BUILD_DIR/libs folder.

    mkdir build && cd build
    qmake ../coreui-extensions.pro && make && make install

After installation the plugins are installed into the $QTDIR/qml folder.

# Extensions

## CoreUI Extension

Provides the common sets of base classes to build the typical CoreUI UI types (e.g. Store, Panel, Control, View)

## JSON Extension

Provide extensions to manage JSON document from QML.

## SQL Extension

Provides extensions to manage SQLITE databases from QML

## Trace Extension

Provides extensions to trace the UI from QML

## Shell Extensions

Provides extensions to use an interactive shell in you UI





