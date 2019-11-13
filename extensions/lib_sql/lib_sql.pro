TEMPLATE = lib

TARGET = lib_sql
DESTDIR = $$BUILD_DIR/libs

CONFIG += staticlib
CONFIG += c++11

QT += core
QT += sql
QT += qml
QT -= gui

HEADERS += sqlquerydatasource.h
SOURCES += sqlquerydatasource.cpp

HEADERS += sqlquerymodel.h
SOURCES += sqlquerymodel.cpp

HEADERS += sqltablemodel.h
SOURCES += sqltablemodel.cpp

HEADERS += sqltabledatasource.h
SOURCES += sqltabledatasource.cpp



OTHER_FILES += use_lib_sql.pri
