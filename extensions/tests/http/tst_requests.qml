import QtQuick 2.0
import QtTest 1.2

import CoreUI.Http 1.0


TestCase {
    id: root
    name: "Requests"
    property bool wait: true

    Requests {
        id: requests
    }

    function test_parent() {
        root.wait = true
        requests.get('http://localhost:3000/number', "", function() {
            console.log('hello');
            root.wait = true
        });
        tryVerify(function() { return root.wait == true });
    }

    function test_data() {
    }
}
