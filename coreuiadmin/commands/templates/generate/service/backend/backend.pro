TEMPLATE = lib
TARGET = {{id}}_backend
DESTDIR = $$BUILD_DIR/qtivi

QT += core
QT += ivicore
QT += ivicore-private

CONFIG += plugin


PLUGIN_TYPE = qtivi
PLUGIN_EXTENDS = qtivi

LIBS += -L$$BUILD_DIR/libs -l{{id}}_frontend
INCLUDEPATH += $$OUT_PWD/../frontend


HEADERS += plugin.h
SOURCES += plugin.cpp

OTHER_FILES += plugin.json

