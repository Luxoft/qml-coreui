TEMPLATE = lib
TARGET = lib_trace
DESTDIR = $$BUILD_DIR/libs

CONFIG += staticlib
CONFIG += c++11

QT += qml
QT += quick
QT -= gui

CONFIG += staticlib

SOURCES += tracer.cpp
HEADERS += tracer.h

SOURCES += mousetracer.cpp
HEADERS += mousetracer.h

OTHER_FILES += use_lib_trace.pri
