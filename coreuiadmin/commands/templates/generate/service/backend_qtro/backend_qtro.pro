TEMPLATE = lib
TARGET = {{id}}_qtro
DESTDIR = $$BUILD_DIR/qtivi
macos: CONFIG += debug_and_release build_all

QT_FOR_CONFIG += ivicore
!qtConfig(ivigenerator): error("No ivigenerator available")

LIBS += -L$$BUILD_DIR/libs -l{{id}}_frontend

INCLUDEPATH += $$OUT_PWD/../frontend
QT += core ivicore ivicore-private

CONFIG += ivigenerator plugin
QFACE_FORMAT = backend_qtro
QFACE_SOURCES = ../../interfaces/{{id}}.qface

PLUGIN_TYPE = qtivi
