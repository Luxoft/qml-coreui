# Layout

In the past the UI was a static view on the information to be presented. Today this view is very dynamic and the user expects the view to change its appearance based on the context the display is in. Another aspect of layout is the support for different screen sizes out of one code base. This aspect is important to support for example a low-end device and a mid and high-end device from only one code-base without re-writing the whole UI layer.

The dynamic aspect of the layout of the visual elements always requires some fundamental rules defined by the design team the UI shall follow, the so called design language. Often these rules are based on a grid system or on other geometrical constraints. If such a fundamental layout system does not exist it will be impossible for a UI developer to code a UI that follows the UI specification in all different scenarios.

The complexity of testing increases when a new device configuration is added to the supported list of devices. The testing requires to test all device configurations with all market variations. There needs to be though a test strategy planned for the UI testing.

Resources

* https://www.designbetter.co/design-systems-handbook/


## Layout Aspects

The user interface specification is the base for the user interface implementation. To achieve a coherent UI the UI specification is linked to a design style guide identifying the different style elements used in the specification. The information and interaction is derived from an information architecture guide. These documents build the design foundation for the user interface implementation. A document does not have to be a typical document it can also be a set of documents or nowadays often wiki pages. Wiki pages have the advantage that they are less formal and transparent for the users to provide feedback and to interact with the authors of the content. It is important to create an open discussion between design and development teams to enrich the overall content and create the best experience for the users.

The layout of a system includes the placing of UI elements but also their behavior on geometry changes. Additionally the layout also includes information about the used font and icons. The layout needs to adapt to the changes of the display size, or display orientation but also to changes based on the user interaction.


## Design Systems

The most commonly used design system is the grid. It allows to divide the display in equally wide columns with common spacing. The content is vertically aligned which pleases the eye. Each major UI element needs to be placed according to the grid system. The grid content is not static it can be resized but it will snap on these grid cells.


## Geometry

User interface elements are defined by the x,y position and their width, height expansion. The x,y position is relative to the parent element. The place in the UI tree is as such another aspect which defines a UI element. The position in the tree also defines the z-order of the element. The z-order defines if an element is rendered above or below another element.

Through the property binding of QML it is possible to simply define relations between aspects of an item.

```qml

Item {
    id: root
    width: 200
    height: 200
    Item {
      width: root.width / 2
      height: root.height
    }
    Item {
      x: root.width / 2
      width: root.width / 2
      height: root.height
    }
}
```

Geometry relations can be easily expressed using the x,y,width,height properties and bind them either to static values or to another properties as an expression.


## Anchoring

Anchoring is the process to bind one anchor line of an element to another anchor line of another (parent or sibling) element. The anchor lines can be left, right, top, bottom and the vertical and horizontal center. Anchoring can happen with an offset or so called margin to allow spacing of the elements.

Anchoring of UI elements is a very powerful and strong way to express geometrical relationships between UI elements. It is used for major UI elements which should have a clear relationship.

## Positioning

Special positioner elements allow to manipulate the x,y position according given rules. These positioners are called Row, Column, Grid, Flow. Be aware that these positioners only manipulate the x,y position of an element not width and height.

Positioning is used when the width, height of elements should not have an influence on the layout. Most often Layout Managers are the preferred solution.

## Layout Manager

A layout manager manages the full geometry of a UI element. There exist currenty three types of layout managers: RowLayout, ColumnLayout and GridLayout. In practice RowLayout and ColumnLayout are just simplified versions of the GridLayout.

The GridLayout is really powerful, it supports setting preferred sizes, spacing, fills, spans, max/min sizes and margins. As a bonus the Layout supports also mirroring which can be used in user interfaces that should take care about different writing directions or in cars where the steering wheel is placed on the right or left side according to the country rules.


## Custom Layout Manager

A layout of component is often defined inside a panel. It is also possible to extract the layout part of the panel into an own component. The layout component would then use loaders and component properties to load the components taking part in the layout and to control the layout.

Here is an example of a border layout

```qml

import QtQuick 2.10
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.3

Control {
  id: control
  property alias topComponent: topLoader.sourceComponent
  property alias leftComponent: leftLoader.sourceComponent
  property alias rightComponent: rightLoader.sourceComponent
  property alias bottomComponent: bottomLoader.sourceComponent
  property alias centerComponent: centerLoader.sourceComponent

  background: ColumnLayout {
      implicitWidth: 640
      implicitHeight: 480
      spacing: 0
      Loader {
          id: topLoader
          Layout.fillWidth: true
          Layout.preferredHeight: item?item.height:-1
      }
      RowLayout {
          Layout.fillWidth: true
          Layout.fillHeight: true
          spacing: 0
          Loader {
              id: leftLoader
              Layout.fillHeight: true
              Layout.preferredWidth: item?item.width:-1
          }
          Loader {
              id: centerLoader
              Layout.fillWidth: true
              Layout.fillHeight: true
          }
          Loader {
              id: rightLoader
              Layout.fillHeight: true
              Layout.preferredWidth: item?item.width:-1
          }
      }
      Loader {
          id: bottomLoader
          Layout.fillWidth: true
          Layout.preferredHeight: item?item.height:-1
      }
  }
}
```

The loader acts as a placeholder for the control to be placed. The layout parameters depend on the existence of the particular control (e.g. `Layout.preferredHeight: item?item.height:-1`). By this you can create also more complex layouts and testing of these layouts can be done indepently from the UI.


This custom layout can be used like any other component.

```qml

import QtQuick 2.10
import QtQuick.Controls 2.3

BorderLayout {
	topComponent: Button { text: "TOP" }
	bottomComponent: Button { text: "BOTTOM" }
	rightComponent: Button { text: "RIGHT" }
	leftComponent: Button { text: "LEFT" }
	centerComponent: Button { text: "CENTER" }
}
```

!!! note

	A layout can also be implemented in QtC++ in a more performant way. This QML based layout has a small impact on performance as it creates a Loader for each part. In case you notice any delay you might want to look into moving this layout to QtC++.







