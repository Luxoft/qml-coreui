TEMPLATE = lib
TARGET = {{id}}_frontend

CONFIG += ivigenerator
DESTDIR = $$BUILD_DIR/libs

QT_FOR_CONFIG += ivicore
!qtConfig(ivigenerator): error("No ivigenerator available")

macos: QMAKE_SONAME_PREFIX = @rpath

QT += ivicore ivicore-private qml quick

QFACE_FORMAT = frontend
QFACE_SOURCES = ../../interfaces/{{id}}.qface
