# Welcome to QML Core UI Guide

> You must be the change
> You wish to see in the world
>
> -- Gandhi (now a bumper sticker)



# Preface

When you are part of a team that works on Qt Automotive Suite (short - Qt Auto), as Qt's vertical extension into the automotive market, you always wonder how new customers will approach Qt Auto, and how they will adapt it to their needs to create a truly stunning user experience for their automotive customers.

From our research projects and production projects with various customers, we have gained valuable insights into this interesting market. Each project has its own unique constellation of management, design, development, and partnerships. This guide attempts to lay out the ground for a discussion about creating user interfaces which scale using technologies included in [Qt](https://www.qt.io) and the [Qt Automotive Suite developed by Luxoft with Partners](https://www.qt.io/qt-automotive-suite/), using an architecture we named the QML Core UI architecture.

Naturally, customers shall be motivated to deviate from this Core UI Guide where necessary. This guide helps customers to get a base for fundamental discussions, internally and externally and hopefully the support required to come to a conclusion that helps them to achieve their own goals.

*/ jryannel*

## Why

> A fundamental aspect of creating an architecture is to define a vocabulary and vision of that architecture.

Most of the work in this guide is funded by Luxoft, an engineering services company. You may wonder why a service company is willing to publish essential knowledge in open source under fairly permissive licenses. This is because, when we conduct customer projects in the UI domain, we have noticed certain recurring patterns. Our philosophy is not based on watching customers stumble over the same problems. Instead, we would like to be part of the solution, and prevent these problems from recurring in the first place.

In this guide, you will see many mentions of "automotive". This starts with the name "Qt Automotive Suite". Automotive has various specifics aspects. The same applies to embedded hardware and software in the Industrial sector. They have one interesting thing in common: they speak about Human Machine Interface (HMI) or about Man-Machine Interface (MMI), whereas HighTech speaks about User Interfaces (UI). User Experience (UX) is still known in Automotive, but for a long time, it mostly was in terms of interior of the car and all about using buttons, switches, and pedals arranged around the steering wheel. In the course of convergence and digitalization, Automotive started to invest in making interfaces for users and less for machines and in seeing this as essential part of UX. We firmly believe that the Industrial sector and Embedded in general will follow this trend soon to and benefit from this guide.


## The Team

This guide was initially designed and worked out as part of the Qt Auto effort at Luxoft. Being part of a team means the author is not the only contributor. Others contributed by ideas, converstations or even contributions. I would like to thank the Qt Auto team at Luxoft to allow me to write this guide as part of my daily work

## License


> Permission is granted to copy, distribute and/or modify this document under the terms of the GNU Free > Documentation License (FDL) version 1.3 or any later version published by the Free Software Foundation; with no Invariant Sections, no Front-Cover Texts, and no Back-Cover Texts.
>
> The code samples in this document are provided under BSD 3-Clause "New" or "Revised" License as published by the SPDX Workgroup a Linux Foundation Project
