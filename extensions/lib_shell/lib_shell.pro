TEMPLATE = lib

TARGET = lib_shell
DESTDIR = $$BUILD_DIR/libs

CONFIG += staticlib
CONFIG += c++11

QT += core
QT += sql
QT += qml
QT -= gui

HEADERS += shellglobal.h
SOURCES += shellglobal.cpp

HEADERS += shell.h
SOURCES += shell.cpp

HEADERS += scope.h
SOURCES += scope.cpp

OTHER_FILES += use_lib_shell.pri

include( $$SOURCE_DIR/src/lib_coreui/use_lib_coreui.pri )
