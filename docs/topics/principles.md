# Design Principles

Software design is an important part of the software development cycle. Thinking about how to create structure before start writing code is critical. Good software design comes from capturing the requirements and playing with the question "What happens when ...?"

"What happens when ...?" captures the moving parts. And parts with move together should stay together and the joints should be protected by interfaces. These principles are expressed in bad and good principles. Please bear in mind principles are not laws. But consider them as good practices and improve on them by discussion.

> Most comes from an article called: [From STUPID to SOLID Code](https://williamdurand.fr/2013/07/30/from-stupid-to-solid-code/)

## STUPID - Bad Principles

* Singleton
* Tight Coupling
* Untestability
* Premature Optimization
* Indescriptive Naming
* Duplication

### Singleton Pattern

The [Singleton pattern](https://en.wikipedia.org/wiki/Singleton_pattern) is probably the most well-known design pattern, but also the most misunderstood one. There is something called a Singleton syndrome. It is when the developer thinks the Singleton pattern is the most appropriate pattern for the current use case. In other words, a Singleton will be used everywhere. That is definitely not cool.

[Singletons are controversial](https://code.google.com/archive/p/google-singleton-detector/wikis/WhySingletonsAreControversial.wiki), and they are often [considered anti-patterns](https://stackoverflow.com/questions/11292109/why-implementing-a-singleton-pattern-in-java-code-is-sometimes-considered-an-a). They should be avoided. Actually, the use of a singleton is not the problem, but the symptom of a problem. Here are two reasons why:

* Programs using global state are very difficult to test
* Programs that rely on global state hide their dependencies

But should they be avoided at all time? You can argue yes, because they can often be replaced by something better. Avoiding global things is important to avoid something called tight coupling.


### Tight Coupling

Tight [coupling](https://en.wikipedia.org/wiki/Coupling_%28computer_programming%29), also known as strong coupling,  it appears together with [cohesion](https://en.wikipedia.org/wiki/Cohesion_%28computer_science%29). Basically, you should [reduce coupling](https://martinfowler.com/ieeeSoftware/coupling.pdf) between your modules and increase cohesion inside a module.

> It boils down to this: If changing one module in a program requires changing another module, then coupling exists.

For instance, you instantiate objects in your constructor’s class instead of passing instances as arguments. That is bad because it doesn’t allow further changes such as replacing the instance by an instance of a sub-class, a mock or whatever.

> Tightly coupled modules are difficult to reuse, and also hard to test.


### Untestability

Testing should not be hard! Really! Whenever there is no time to write unit tests, the real issue is that code is bad, but that is another story.
Making code clean and testable requires time and knowledge.

> Code shall be written with the idea in mind that the team has to maintain it for the next ten years!

Most of the time, untestability is caused by tight coupling.

### Premature Optimization

## SOLID - Good Principles

* Single Responsibility Principle
* Open Closed Principle
* Liskov Substitution Principle
* Interface Segregation Principle
* Dependency Inversion Principle


### Single Responsibility Principle

Single Responsibility Principle or SRP states that every class should have a single responsibility. There should never be more than one reason for a class to change. In other words: `Things what change together, belong together`.

Just because you can add everything you want into your class doesn’t mean that you should. Thinking in terms of responsibilities will help you design your application better. Ask yourself whether the logic you are introducing should live in this class or not. Using layers in your application helps a lot. Split big classes in smaller ones, and avoid god classes. Last but not least, write straightforward comments. If you start writing comments such as in this case, but if, except when, or, then you are doing it wrong.



### Open Closed Principle

Open/Closed Principle or OCP states that software entities should be open for extension, but closed for modification.


The principles tells to write code so that it will be able to add new functionality without changing the existing code. That prevents situations in which a change to one of your classes also requires you to adapt all depending classes. This can be achived using interfaces or composition. Pure inheritance seems to be not a perfect solution, as inheritance introduces tight coupling.


### Liskov Substitution Principle

Liskov Substitution Principle or LSP states that objects in a program should be replaceable with instances of their subtypes without altering the correctness of the program.

A derived type shall be able to replace a super type, without requiring code changes on other places. It can be achived by following a few simple rules, which are similar to [design by contract](https://en.wikipedia.org/wiki/Design_by_contract) by Betrand Meyer.

* An overridden sub type method needs to have the same signature from the super type
* It is allowed to implement less restrictive validation rules in the sub type.
* It is not allowed to enforce stricter validation rules in a sub type.

The result is that substition does not only enforce an API surface but also a behaviour, expressed in rules. These rules can be validated by test cases or code reviews.

### Interface Segregation Principle

Interface Segregation Principle (ISR) states that several focused interfaces are better than one general-purpose interface. In other words, you should not have to implement methods that you don’t use. Enforcing ISP gives you low coupling, and high cohesion.

> An interface is a contract that meets a need.

Coupling as a metric for inter-component binding and cohesion as metric for inside-component binding. High cohesion means to keep similar and related things together. The idea is to keep your components focused and try to minimize the dependencies between them.



### Dependency Inversion Principle


The Dependency Inversion Principle (DIP) states that high level components (policy making) should not depend on low level (details) components; both should depend on abstractions (e.g. interfaces).

* High-level modules should not depend on low-level modules. Both should depend on abstractions (e.g. interfaces).
* Abstractions should not depend on details. Details (concrete implementations) should depend on abstractions.

By both depending of abstraction, effectively the dependency is inverst. This allows us also to replace the low-level component with another component implementing the abstraction.

This goes hand-in-hand with [dependency-injection](https://de.wikipedia.org/wiki/Dependency_Injection). When a component gets an abstraction injected, the using component is free to inject a different implementation.


> Use the same level of abstraction at a given level

## Other Principles

* [Dependency Injection - Wikipedia](https://de.wikipedia.org/wiki/Dependency_Injection)
* [Law of Demeter - Wikipedia](https://en.wikipedia.org/wiki/Law_of_Demeter)
* [Convention over configuration - Wikipedia](https://en.wikipedia.org/wiki/Convention_over_configuration)
* [Don’t repeat yourself - Wikipedia](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself)
