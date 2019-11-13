import QtQuick 2.11
import QtApplicationManager.SystemUI 2.0

Item {
    id: root

    property var applicationModel: ApplicationManager
    property var locale: Qt.locale()
    property string currentDate;
    property string currentDateString;
    property string currentTimeString;

    Timer {
        interval: 100
        running: true
        repeat: true
        onTriggered: {
            var date = new Date();
            root.currentTimeString = date.toLocaleTimeString(root.locale, Locale.ShortFormat)
            root.currentDateString = date.toLocaleDateString(root.locale, Locale.ShortFormat)
            root.currentDate = date;
        }
    }

    function launch(appId) {
        console.log('appId: ', appId)
    }
}
