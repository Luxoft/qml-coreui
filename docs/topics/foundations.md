# Foundations

!!!info

    This material is work in progress and will change!


!!! abstract

    CoreUI is founded on some core-principles collected over the years, which all contribute to the overall design decisions. These principles are based on the opinions of many but may not be applicable to everyone.

Here are some key principles:

* **Follow the Agile Principles** - UX depends on flexibility and agility. Keep it that way.
* **Enable Hot-Reloading everywhere** - Allow changes to be visible in a fraction of a second.
* **Testability and dependency management is paramount** - You can't trust code you cannot test. And trust is the foundation of large systems.
* **Separation of Hardware and Software** - As a UI developer you don't want to depend on something you cannot control or isn't even available at an early stage.
* **UX Design is a bi-directional conversation** - Design has a great impact on the UX, but also the chosen technology. Finding the balance and pushing forward together makes heroes.
* **Thinking in Components and Building Blocks** - Component-based programming leads to a better structure and allows for building larger user interfaces.
* **Component separation is good, process separation is better** - Trust is good, having control is better. A process gives you more control.
* **Aspect driven components** - Design your component layers around different aspects of your software. Each aspect provides another piece to the puzzle.

A detailed description for each principle can be found below.


## Agile Principles

CoreUI embodies the core values of the Manifesto for Agile Software development. Agility means in its core to "walk the path even if you don't know the whole path yet". It is about taking the opportunity and relying on motivated teams.

* **Individuals and Interactions** over processes and tools: Tools and processes are important, but it's more important to have competent people working together effectively.
* **Working Software over comprehensive documentation**: Good documentation is useful in helping people to understand how the software is built and how to use it, but the main point of development is to create software, not documentation.
* **Customer Collaboration over contract negotiation**: A contract is important but is no substitute for working closely with customers to discover what they need.
* **Responding to Change over following a plan**: A project plan is important, but it mustn't be too rigid to accommodate changes in technology or the environment, stakeholders' priorities, and people's understanding of the problem and its solution.

In short, while there is value in the items on the right, they value the items on the left more. [^AgilePrinciples]
Sources: Wikipedia, Agile Manifesto


## Live-reloading

Live-reloading is the practice of reloading the program as a whole or as part of a particular change in the underlying source code. That change can be triggered by a keystroke, a timer, or based on document persistence. The reloading can be either state preserving or state resetting.

Enabling live-reloading throughout the CoreUI architecture serves several goals:

- Productivity: CoreUI enforces a clean abstraction of business-logic and visual-logic, thus making the reloading of business tests part of the daily work-flow.
- Testability: CoreUI not only supports live-reloading of the whole program but also encourages Developers to live-reload individual pieces of the user interface. As such it encourages the developer to think about components and their dependencies, thus resulting in better testability.
- UX Creation: Reloading also plays a crucial role in enabling great UX by making the conversation that the developer has with the UI teams more fluent.


## Testability and Controlled Dependency

CoreUI separates user interface pieces into different components with clearly-defined dependencies and interfaces. CoreUI encourages the developer to create smaller, well-defined, components. The idea is less about re-use but more about splitting the UI into small, manageable, pieces which can be implemented independently. This principle manages dependencies and smaller components, enabling testability with fewer headaches or overhead.

CoreUI comes with a test harness which enables both manual component testing and automated component testing. Manual component testing is especially useful during development, when you want to try out a specific component. All of this can be paired with live-reloading of such tests: either when the test code itself or the underlying component changes.


## Separation of Hardware from Software

Developing embedded software means always working with the target hardware. However, often the target hardware is not available in the early stages of development or even at later stages. Additionally, there may also be a shortage of devices and each developer can't have his or her own device to work with. These hardware can be big and difficult to place in an office. Consequently, the ability to develop as much software as possible without depending on the target hardware is highly desirable. Nevertheless, it is still required to go on the hardware as early as possible. This brings up the requirement of being flexible enough to support compatibility between different back-ends using the same front-end software.

Ideally, you are able to run the front-end with either a simulation backend or with the real, production, one. Ideally, the simulation back-end can also run on the target HW. To foster easier front-end development it should also be possible to run the front-end on a desktop and have it using a back-end running on the target HW. To achieve this, the interface between front-end and back-end must be done via a cross-device communication protocol (typically TCP/IP based).

## UX Design Conversations

Creating a stunning UX is a team effort involving UI designers, UI developers, and other stakeholders. The System needs to be able to deliver the processing power and graphics capabilities allowing a stunning user experience at first place, but even if this is given, still there is not a guarantee that a great UX will be created. To achieve a truly beautiful UX it is required that the visionary people who design the product and deliver the information architecture and UI appearance, work closely together with the people programming the UI. Only then a great UX can be achieved.

The UI developers know what the system can deliver and which special effects and/or animations will take down the system and will start introducing an unsatisfying user experience to the user. The UI designers have their own vision into their head but often the documentation is lacking behind and also does not tell the whole story. These internal concepts not documented but expressed in design are important for the UI developers as they also need to base their detailed UI appearance on fundamental concepts. If these fundamental concepts diverge because of not being aware of each other, the UI code will always look like someone has patched it to make it work.

A true harmony and understanding of UI design of the UI developer can be seen in the UI code produced by the developers.


## Thinking in Components

While the UI developer using QML is forced to think in components as its basic building block, designers often don't think in terms of components. This is probably related to the pixels on a display and the tooling used that is based on pixel manipulation, less vector art, and objects.

A component is a piece of a reusable user interface from which the information architecture receives a clear set of data and provides a clearly defined interaction to the user. This component can then be re-used in other parts of the user interface by manipulating the incoming properties.

For example, a Button receives a text property which can be set when created, and allows the user to click on it as its interaction. This component can be used anywhere a button is used by assigning a different text property and reacting differently to the click interaction.

Designing a square rectangle of pixels with a nice gradient, without thinking about how this rectangle eventually becomes a component with appearance, incoming data, and interaction - will result in the designer not being able to use the button everywhere coherently. Consequently, the developer will have to implement each of these buttons, providing the different flavors of buttons by adding more complex code to the initial component.

Ideally, the designer comes up with a Style and Component guide which lists all common usable components together with their modifiers and interactions. This list should then be used to construct concrete user interfaces out of these components; custom components should be a rare exception.

There is a common set of components that users are used to, which are often provided as standard components by the UI toolkits. Qt, for example, provides the QtQuick Controls 2 library.

On a higher level, it is also worth thinking about larger components, such as components that act as a container for other components. In CoreUI, they are called panels. Panels provide a defined layout and interaction possibility for a set of components laid out together, for either a specific or a more general purpose.

If a component can be re-used in different contexts it can also be re-used in a test setup. That said, it's important to display a component independently from its UI context to validate its appearance and behavior.


## Components vs. Processes

A component is a reusable piece of user interface, with a known exported programming interface. A process is an execution unit, which allows the CPU to schedule it independently from other processes and manage the memory independently from other processes. A process provides security and separation of interfaces. Inside a process, you cannot easily call an API which is available inside another process. You always need to export this API and then make use of that from within the other process via some form of IPC. But processes can be re-used the same as components, but on a different level and with a much stricter control.

Typically an application is a deciding factor to create a new process. An application can stem from a 3rd party and might introduce a security risk, so it is better to control its access to the system. In a single process UI where an application is merely a component, these security mechanisms do not exist, so any application can in general access every API.

## Aspect-driven Components

Traditional UI development follows the user interface specifications and starts with the main document and then the folder structure mirrors the feature set of the UI specification. Applying this on larger user interfaces provides several drawbacks. The code gets more complex as deeper the folder structure goes. There is no guideline about dependency, which leads to the fact that even components on the edge of the UI tree might have dependencies to central components or worse other edges of the tree. Not controlling dependency is the main factor that the development speed slows down when the UI gets more complex.

Aspect driven development tries to focus on the different aspects of a user interface (e.g. views, panels, controls, animations, helpers) and tries to provide clear guidance how such a component shall be constructed and which dependencies it might create.

## Release Early, Release Often

Celebrate releasing your software. Releasing software is a practice which needs to be repeated and automated as much as possible. Always keep your software in a releasable state.

Releasing usually means you have to interrupt your software development to make a release. By repeating this process over and over and perfecting the workflow, you can minimize the disruption a release creates and ensure your code stays in good health.

You want to run a Continuous Integration (CI) workflow with a maximum number of automated tests, which ideally proves the test coverage. Try to release software that acts as feedback to your developers so that they experience releasing as a natural step forward. in the software development process. For example, if you work on the UI, you can release the platform that the UI is based on and ensure all developers use the same platform.

See: https://en.wikipedia.org/wiki/Release_early,_release_often
