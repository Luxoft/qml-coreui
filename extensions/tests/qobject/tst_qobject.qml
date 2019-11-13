import QtQuick 2.0
import QtTest 1.2

import CoreUI 1.0


TestCase {
    id: test
    name: "MathTests"

    CoreObject {
        id: root
        CoreObject {
            id: child
        }
    }

    function test_parent() {
        compare(child.parent, root)
    }

    function test_data() {
    }
}
