import QtQuick 2.11
import QtQuick.Controls 2.11
import "../stores"
import "../views"

Pane {
    id: root

    property RootStore store

    WelcomePanel {
        title: store.applicationTitle
    }
}
