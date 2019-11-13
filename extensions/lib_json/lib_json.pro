TEMPLATE = lib

TARGET = lib_json
DESTDIR = $$BUILD_DIR/libs

CONFIG += staticlib
CONFIG += c++11

QT += core
QT += sql
QT += qml
QT -= gui

HEADERS += jsondatasource.h \
    abstractdatasource.h \
    jsonglobal.h
SOURCES += jsondatasource.cpp \
    abstractdatasource.cpp \
    jsonglobal.cpp


OTHER_FILES += use_lib_json.pri
