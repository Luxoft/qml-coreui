TEMPLATE = lib

TARGET = lib_http
DESTDIR = $$BUILD_DIR/libs

CONFIG += staticlib
CONFIG += c++11

QT += core
QT += network
QT += qml
QT -= gui

HEADERS += requests.h
SOURCES += requests.cpp


OTHER_FILES += use_lib_http.pri
