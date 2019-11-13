import QtQuick 2.4
import QtQuick.Controls 2.3

import "views"
import "stores"

/*
  The surface exposed as the application shell for this application.
  It is normally bound to a particular display.
*/
Page {
    width: 1280
    height: 800

    RootStore {
        id: store
    }

    header: StatusView {
        store: store
    }

    HomeView {
        anchors.fill: parent
        store: store
    }

    AppContainerView {
        anchors.fill: parent
        store: store
    }

    OverlaysView {
        anchors.fill: parent
        store: store
    }

    DialogView {
        anchors.fill: parent
        store: store
    }
}
