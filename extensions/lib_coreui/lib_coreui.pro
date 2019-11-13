TEMPLATE = lib

TARGET = lib_coreui
DESTDIR = $$BUILD_DIR/libs

CONFIG += staticlib
CONFIG += c++11

QT += core
QT += qml
QT += quick
QT -= gui

HEADERS += coreui.h
SOURCES += coreui.cpp

HEADERS += object.h
SOURCES += object.cpp

HEADERS += variantmodel.h
SOURCES += variantmodel.cpp

HEADERS += control.h
SOURCES += control.cpp

HEADERS += view.h
SOURCES += view.cpp

HEADERS += panel.h
SOURCES += panel.cpp

HEADERS += store.h
SOURCES += store.cpp

OTHER_FILES += use_lib_coreui.pri
