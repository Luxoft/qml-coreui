import QtQuick.Controls 2.3
import QtQuick 2.10
import "sysui"

/*
The entry point for the system UI.
It sets up the app shell inside the system UI (sysui).
*/

ApplicationWindow {
    id: root
    width: 1280
    height: 800
    visible: true

    AppShell {
        anchors.fill: parent
    }
}
