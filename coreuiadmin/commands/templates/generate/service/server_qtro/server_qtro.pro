TEMPLATE = app
TARGET = {{id}}_server_qtro
QT -= gui
QT += core qml
CONFIG += c++11 ivigenerator
CONFIG -= app_bundle
DESTDIR = $$BUILD_DIR/bin

LIBS += -L$$BUILD_DIR/libs -l{{id}}_frontend
INCLUDEPATH += $$OUT_PWD/../frontend

SOURCES += main.cpp

SOURCES += server.cpp
HEADERS += server.h

QFACE_FORMAT = server_qtro
QFACE_SOURCES = ../../interfaces/{{id}}.qface
QML_IMPORT_PATH =
QML_DESIGNER_IMPORT_PATH =

