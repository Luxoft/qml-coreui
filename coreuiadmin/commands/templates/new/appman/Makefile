.PHONY: native

start:
	cd ui && $QTDIR/appman -r -c am-config.yaml -I imports
native:
	qmake
	make
	install