# Common Controls

!!!info

    This material is work in progress and will change!

Common Controls are shared controls between the applications. They form semantic user interfaces. Often they are built out of UI primitives such as rectangles, mouse areas, images, etc. and expose a defined high-level API. These controls are designed after the user interface specification and especially they follow the UI style guide as a central guide that defines the visual appearance.

Controls are tightly bound to styles as the style defines the visual appearance of a control. It is often desirable to separate the logic of a control from the visual appearance and ideally make the appearance pluggable. This can be reached by thinking about a control as a template for a real control. This template contains only the common logic of a control and can even be coded in C++ for optimization. The visual appearance would then be added when a concrete control is defined. To know which concrete control needs to be used, the framework contains a logic to use a different control based on the style setting. This acts very much like a factory class where the object creation is separated from the object creation request. The framework takes care about ensuring the correct concrete control is created.

This is the pattern used in the QtQuick.Controls V2 (https://doc.qt.io/qt-5.10/qtquickcontrols2-index.html) controls library. It forms a common set of controls which is used typically in modern touch-based user interfaces without coupling them to the style. The library comes with a common set of styles to get started and allows a team to define fully its own style. On a high level, this is done by having the template classes implement the control logic and a style adding the geometry and appearance of background and content to the control (https://doc.qt.io/qt-5.10/qtquickcontrols2-customize.html).

It is also possible to create completely new controls but often this is not required and a new control can often be formed by either styling or aggregating two or more controls to a new control.

!!! note
As long as a control behaves like an existing control template (e.g. a button is clicked) the visual appearance can be adjusted.

## Typical Controls

These are the controls currently supported by QtQuick Controls 2. This should be used as a short overview of the available controls and to form a vocabulary with the design team.

- **Control** - Control is the base type of user interface controls.

### [Buttons Controls](https://doc.qt.io/qt-5/qtquickcontrols2-buttons.html)

- **AbstractButton** - Abstract base type providing functionality common to buttons
- **Button** - Push-button that can be clicked to perform a command or to answer a question
- **CheckBox** - Check button that can be toggled on or off
- **DelayButton** - Check button that triggers when held down long enough
- **RadioButton** - Exclusive radio button that can be toggled on or off
- **RoundButton** - A push-button control with rounded corners that can be clicked by the user
- **Switch** - Button that can be toggled on or off
- **ToolButton** - Button with a look suitable for a ToolBar

### [Container Controls](https://doc.qt.io/qt-5/qtquickcontrols2-containers.html)

- **ApplicationWindow** - Styled top-level window with support for a header and footer
- **Container** - Abstract base type providing functionality common to containers
- **Frame** - Visual frame for a logical group of controls
- **GroupBox** - Visual frame and title for a logical group of controls
- **Page** - Styled page control with support for a header and footer
- **Pane** - Provides a background matching with the application style and theme
- **ScrollView** - Scrollable view
- **StackView** - Provides a stack-based navigation model
- **SwipeView** - Enables the user to navigate pages by swiping sideways
- **TabBar** - Allows the user to switch between different views or subtasks
- **ToolBar** - Container for context-sensitive controls

### [Delegate Controls](https://doc.qt.io/qt-5/qtquickcontrols2-delegates.html)

- **ItemDelegate** - Presents a checkable control that can be pressed and clicked by the user.
- **CheckDelegate** - Item delegate with a check indicator that can be toggled on or off
- **RadioDelegate** - Exclusive item delegate with a radio indicator that can be toggled on or off
- **SwipeDelegate** - Swipeable item delegate
- **SwitchDelegate** - Item delegate with a switch indicator that can be toggled on or off

### [Indicator Controls](https://doc.qt.io/qt-5/qtquickcontrols2-indicators.html)

- **BusyIndicator** - Indicates background activity, for example, while content is being loaded
- **PageIndicator** - Indicates the currently active page
- **ProgressBar** - Indicates the progress of an operation
- **ScrollBar** - Vertical or horizontal interactive scroll bar
- **ScrollIndicator** - Vertical or horizontal non-interactive scroll indicator

### [Input Controls](https://doc.qt.io/qt-5/qtquickcontrols2-indicators.html)

- **ComboBox** - Combined button and popup list for selecting options
- **Dial** - Circular dial that is rotated to set a value
- **RangeSlider** - Used to select a range of values by sliding two handles along a track
- **Slider** - Used to select a value by sliding a handle along a track
- **TextArea** - Multi-line text input area
- **TextField** - Single-line text input field
- **Tumbler** - Spinnable wheel of items that can be selected

### [Menu Controls](https://doc.qt.io/qt-5/qtquickcontrols2-menus.html)

- **Menu** - Popup that can be used as a context menu or popup menu
- **MenuBar** - Provides a window menu bar
- **MenuBarItem** - Presents a drop-down menu within a MenuBar
- **MenuItem** - Presents an item within a Menu

### [Navigation Controls](https://doc.qt.io/qt-5/qtquickcontrols2-navigation.html)

- **Drawer** - Side panel that can be opened and closed using a swipe gesture
- **StackView** - Provides a stack-based navigation model
- **SwipeView** - Enables the user to navigate pages by swiping sideways
- **TabBar** - Allows the user to switch between different views or subtasks
- **TabButton** - Button with a look suitable for a TabBar

### [Popup Controls](https://doc.qt.io/qt-5/qtquickcontrols2-popups.html)

- **Dialog** - Popup dialog with standard buttons and a title, used for short-term interaction with the user
- **Drawer** - Side panel that can be opened and closed using a swipe gesture
- **Menu** - Popup that can be used as a context menu or popup menu
- **Popup** - a Base type of popup-like user interface controls
- **ToolTip** - Provides tooltips for any control

### [Separator Controls](https://doc.qt.io/qt-5/qtquickcontrols2-separators.html)

- **MenuSeparator** - Separates a group of items in a menu from adjacent items
- **ToolSeparator** - Separates a group of items in a toolbar from adjacent items

## Laying out Controls

Laying out controls is the process of positioning controls on a panel and deciding on their growth policy. Either the control shall expand when the parent is resized or not. If an item is not intended to grow positioners can do the work, otherwise layouts are always preferred.

To support layout mirroring the [LayoutMirroring](https://doc.qt.io/qt-5/qml-qtquick-layoutmirroring.html) attached property is available.

### [Positioners](https://doc.qt.io/qt-5/qtquick-positioning-layouts.html)

Container items that manage the positions of items.

- **Grid** - Positions its children in grid formation
- **Row** - Positions its children in a row
- **Column** - Positions its children in a column
- **Flow** - Positions its children side by side, wrapping as necessary

### [Layouts](https://doc.qt.io/qt-5/qtquicklayouts-overview.html)

Used to arrange items in a user interface.

- **RowLayout** - Identical to GridLayout, but having only one row.
- **ColumnLayout** - Identical to GridLayout, but having only one column.
- **GridLayout** - Provides a way of dynamically arranging items in a grid.
- **StackLayout** - Provides a stack of items where only one item is visible at a time

The behavior of the items inside a layout can be influenced using the [Layout<qml-qtquick-layouts-layout.html>` attached property.

## Common vs. Application Controls

Common controls are shared between all applications and are designed to work in these different contexts. An application control is private to an application. Often an application control is derived from the need of the UI specification for a very special visual appearance. This could be for example a slider to change the radio frequency. This control would be very specific to a radio application and normally not required by other applications. As such it would be defined inside the application and not in a common control library. Besides this difference in physical location, the creation process is the same.
