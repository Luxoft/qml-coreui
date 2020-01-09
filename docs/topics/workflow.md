# Design Work Flow

> “Digital design is like painting, except the paint never dries.”
> - Neville Brody

* Agile
* Scaled Agile
* Split Teams
* Asset Pipeline
* Handover Design/Simu/Product
* How to get designs into Qt?

Modern projects tend to be user experience driven. There is a long phase before the actual development where the navigation and visual concepts are defined. Often when the development phase starts these concepts are not fully defined yet and they will be adapted while the software is created.

When a new project is started and the first time visual concepts are defined it is a great opportunity to also attach a small software development team to the design team to create user interface prototypes using the Qt technology. The greatest synergy is created when the technology used in production is also used during prototyping. By this the design team can ensure if the user interface runs on a comparable hardware in a comparable context the user experience is really as envisioned.

> UX is only accomplished when the user interface uses the correct UI technology on a comparable hardware in a comparable context. Or even better on the real hardware.

A design which showcases a great visual concept using PowerPoint, or a UI technology which will not be used in production on hardware which is not comparable to the product always runs the risk to stay a vision and never will reflect the reality of the product.

A prototype should stay simple and not get to complex, it should stay lean and be cheap to change, even rapid change. Qt and QML as UI language support these goals on embedded device very neatly. Qt runs on desktop PC as also on most embedded systems, it has great support stunning user interfaces and support a vast variety of animations and graphical effects. It can be used during prototyping as also later during production, by this shortening the time to market and dramatically simplifying the transition from prototyping to production.

## Designer Types

There is more than one type of designer. Same as developers who specialize in the programming areas (frontend, backend, os, network) designers also specialize on different area. The area could be something like this:

* Concept Designer - New user interface concepts
* Structure/Navigation - Design the UI flow, screen transitions, user stories, personas
* Visual Designer - Polished hero screens with beautiful designs and fonts
* Motion Designer - Animation sequences for design components
* 3D Content Designer - 3D textures, materials as also animations
* Production Designer - Adapt designs to production technology

This would be a typical list in large companies and projects. In smaller projects there are often only one or a few designers trying to deliver not only the visual design but also the UI flow and motions.

## Deliverables

Often the direct design output is not usable for production or even prototyping. The deliverables could be PhotoShop documents or Adobe Illustrator documents. The issue is, these formats are not meant for digital user interface, they are created for media design. There is a new breed of design tools which are specialized for digital screens, these are Sketch, Figma, AdobeXD, ... These tools produce output which can be easily integrated into software solutions and cut a lot of needless asset conversions. They are more direct and increase the designer developer rhythm to create a better UX. Assuming we mean the same UX, as UX running on a comparable HW using a production technology in a comparable context.

A modern user interface is composed of components, which are used and reused across screens. A component library defines the building blocks for the developer. It should be the exception that a developer has to create a new screen specific component. If this happens, often this hints about an inconsistent in the design across screens.

To be able to consume deliverable not designed for direct software consumption the role of a production designer was created. This person will be responsible to convert the incoming designs ready for consumption by the software. Often software developers lack the skills to use the highly specialized designer tools or do not have even access to these tools.


## Production Designer

A production designer takes over the role to convert the visual designs into a format consumable by the software. The most common format is PNG for images/icons. But also Fonts as TTF or audio files. For animations these are often described in a textual format but could also be directly coded into QML.

A production designer understand the design workflow from his colleagues. He is embedded in to the design team. As an additional feature the designer also understands the software solution and the component model.

It is important that the production designer understands both worlds to adapt the design.

!!! note

    During a project we see the flow starts to change. The borders between design and developers start to blur as designers get exposed to the user interface technology. A designer which crosses these borders is also called a fullstack-designer. These designers will start to be the productivity boost for the product.

## Full Stack Designer

A full stack designer understands that the UI technology and its rendering capabilities has direct impact on the user experience and the envisioned design. Often even an understanding of the UI technology and its limitations and features better help to reach a common goal. Sometimes even a designer discovers that complex things are very simple and on the other hand a simple design aspects can be utterly complex to realise in software.

A designer which likes to code in QML/JS to create user interface concepts backed up with designs will realize soon that these UI concepts are much faster to realize than the complex step to create a full user interface specifications. If a flow between design and developers is created the process of discovering user interfaces is so fast that writing a design spec actually hinders the productivity and writing the design spec is then often an after thought to ensure the decisions are documented. We have good experience using shared, transparent documentation tools like Confluence to share design concepts as also user interface specifications. The collaborative aspect allows other stakeholders to asks questions and get knowledge to fulfill their jobs. Sharing concept/specification does not mean attaching documents to pages it means writing these documents inside this collaborative tools.

## Sample Setup

We have great experience with Sketch as a design tool. It is ideally suited for the work. But I would expect also Figma would be a good tool. Sketch as a tool understand the concept of a component and allows effortless to export PNG images in different sizes. These exports have a clear size, meaning with and height which is required for the integration. Doing the same export twice should alway lead to the same asset exports having the same characteristics. Exporting assets by hand is very error prone and very unproductive for the developer later.

There is currently no good tooling to validate an asset delivery. Just think about for a moment. Let us assume we get every week a new delivery from the design department. How do we ensure that

- all assets which where present last week, are also present this week
- how can we track when an asset was renamed or relocated
- How to detect that an asset has changed in size or even for the visual center
- How to know which asset have been added

So if there is no good tooling for this, it can be very hard for a developer to integrate the new delivery. It might that some images will not show up at all, as they where removed or renamed or they show up in a weird place, as image was resized. Changing these thing from delivery to delivery will ead to frustration and a not productive result, which is error prone.


## Evolutionary Prototyping

When you use Qt as a prototyping technology as also as a production technology you can apply a evolutionary prototyping strategy. This means the prototype is not thrown away of the concept phase it is continued to evolve into the product. Not every setup will be suited for this. It is important that the design dn development team continues to work on the software when it comes for production. Also it is important that a scalable architecture like the CoreUI architecture was chosen to ensure the fundamentals are stable enough. When the architecture is well established and the software team continues to work on this during production than a evolutionary prototyping can save valuable time and resource. If these conditions are not met, than its better to star over with a new software solution and use the prototype as an inspiration. No developer wants to maintain someone elses hastily written demo code, and a lack of ownership will lead to not motivated developers and a bad productivity.

> For a developer having ownership over the code a great productivity and responsibility boost.

Evolutionary prototyping is a must for all teams which are working on a new UX centered product where time to market is a deciding factor. So better arrange the teams and involve developers early into the loop.