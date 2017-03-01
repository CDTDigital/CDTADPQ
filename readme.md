# Hello, world

## Prototype B

The working prototype will be an application that will allow California residents to establish and manage their profile and receive emergency and non-emergency notifications via email, Short Message Service (SMS), and/or push notification based on the location and contact information provided in their profile and/or the geo-location of their cellphone if they have opted in for this service. In addition, the working prototype will provide the authorized administrative users with the ability to publish notifications and track, and analyze and visualize related data. The working prototype does not need to implement any authentication or authorization against an external directory or authentication mechanism.

[TODO: INSERT INTRO, WHAT DOES IT DO & WHAT VALUE DOES IT ADD]

Our approach is consistent with both the [ADPQ RFI] (https://github.com/CDTProcurement/adpq/blob/master/RFI%20CDT-ADPQ-0117%20-%20PQVP%20DS-AD%20-%20Final%20%2002.06.17.pdf) requirements and the [US Digital Services Playbook] (https://playbook.cio.gov).


## The Team

The Product Manager, Dan Hon, also served as Product Owner in the agile delivery process. He was the assigned leader of the project with responsibility and accountability for the quality of the prototype. 

Composition of the multi-disciplinary team (based on GSA 18F Agile Labor Categories): 

**Dan Hon, Product Manager**

@danhon [LinkedIn Profile](https://www.linkedin.com/in/danhon/)

**Michal Migurski, Technical Architect**

@migurski [LinkedIn Profile](https://www.linkedin.com/in/michalmigurski/)

**Frances Berriman, Interaction Designer / User Researcher / Usability Tester**

@phae [LinkedIn Profile](https://www.linkedin.com/in/fberriman/)

**Erica Kwan, Backend Web Developer**

@pui [LinkedIn Profile](https://www.linkedin.com/in/ericakwan/)

**Kay Chung, Delivery Manager**

@kerrching [LinkedIn Profile](https://www.linkedin.com/in/kerrching/)


## Agile Delivery Process

The agile delivery process used at Very Little Gravitas is based on the open standards Scrum framework, with input and iterative feedback from user-centered design techniques. 

Documentation on the [full agile delivery process](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Agile-Delivery-Process)

For the purposes of the ADPQ submission, we implemented a simplified process, appropriate to the scope and available time. 
The following describes the four 1 week sprints that were completed for the design and build of the prototype. 

#### Sprint 1
* [Design exploration](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Design-exploration) 
* [User research journal](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Research-journal)
* [Technical exploration](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Technical-exploration)
* Set up a Slack group for team communication
* Set up a [kanban board](https://github.com/VeryLittleGravitas/CDTADPQ/projects/1) in the team’s Github repo for use as a lightweight product backlog and sprint task board 

#### Sprint 2

[TODO: LIST OUT DELIVERED SCOPE, REFERENCE USER STORIES FROM KABAN]

#### Sprint 3

[TODO: LIST OUT DELIVERED SCOPE, REFERENCE USER STORIES FROM KABAN]

#### Sprint 4

[TODO: LIST OUT DELIVERED SCOPE, REFERENCE USER STORIES FROM KABAN]


## User-Centered Design 
We used a number of different user-centered design techniques in developing the prototype:

* [User survey](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Research-journal)

[TODO: LIST TWO MORE]


## Deployment Instructions 

See our documentation to [install and run the prototype](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Installing-and-running-the-prototype)


## Additional Material
* [Product Backlog and Sprint Taskboard](https://github.com/VeryLittleGravitas/CDTADPQ/projects/1)
* [Project wiki](https://github.com/VeryLittleGravitas/CDTADPQ/wiki)


## Procurement Requirements

a. Assigned one (1) leader and gave that person authority and responsibility and held that person accountable for the quality of the prototype submitted;

**The leader responsible for the quality of the prototype submitted is @danhon**.

b. Assembled a multidisciplinary and collaborative team that includes, at a minimum, five (5) of the labor categories as identified in Attachment B: PQVP DS-AD Labor Category Descriptions; 

**See the [multidisciplinary team](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Multidisciplinary-team) page on the project wiki**.

c. Understood what people needed, by including people in the prototype development and design process; 

**See the [research journal](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Research-journal) on the project wiki for evidence of how we are including people to understand what they need in making the prototype.**

d. Used at least a minimum of three (3) “user-centric design” techniques and/or tools;

**We are using the following "user-centric design" techniques and/or tools to make this prototype:**

	1. Questionnaires (quantitative feedback)
	2. In-person interviews (qualitative, hands-on usability testing)
	3. Remote user testing (qualitative, individuals providing feedback on experience)
	4. Personas

e. Used GitHub to document code commits; 

**See the project [commit history](https://github.com/VeryLittleGravitas/CDTADPQ/commits/master)**.

f. Used Swagger to document the RESTful API, and provided a link to the Swagger API;

We have created 1 API in this project that returns a zipcode for a given latitude and longitude. 

g. Complied with Section 508 of the Americans with Disabilities Act and WCAG 2.0;

**See the code repository for specifics of implementation. [commit history](https://github.com/VeryLittleGravitas/CDTADPQ/commits/master) The pattern library utilised conforms to ADA and WCAG 2.0, see [Pattern Library Accessibility Notes](https://standards.usa.gov/getting-started/designers/#notes-on-accessibility).**

h. Created or used a design style guide and/or a pattern library;

**This project will use the [Draft U.S. Web Design Standards](https://standards.usa.gov/) as style guide and/or pattern library**.

**See [Pull Request 13](https://github.com/VeryLittleGravitas/CDTADPQ/pull/13) for the initial implementation of the pattern library.**

i. Performed usability tests with people;

**See [Research journal](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Research-journal) for evidence of usability testing videos, as well as notes from interviews.**

j. Used an iterative approach, where feedback informed subsequent work or versions of the prototype;

**The lightweight scrum process we used enabled us to review work delivered at the end of each sprint with users, and  then loop their feedback into the grooming and planning session of the following sprint. This has enabled us to produce features that reflect real users' requirements.**

k. Created a prototype that works on multiple devices, and presents a responsive design;

**We have chosen to use the Draft U.S. Web Design Standards with no custom HTML. This pattern library was chosen to ensure the delivery of a responsive design that works on multiple devices.**

l. Used at least five (5) modern and open-source technologies, regardless of architectural layer (frontend, backend, etc.);

**We are using the following modern, open-source technologies for this prototype:**

1. [Python 3](https://www.python.org/download/releases/3.0/)
2. [Postgres 9](https://www.postgresql.org), an enterprise-grade database used by government agencies in the U.S. such as The National Weather Service, the Centers for Disease Control and Prevention and State Department. 
3. [PostGIS](http://www.postgis.net), a spatial database extender for the Postgres database. PostGIS adds support for geographic objects, allowing for location queries to be run in SQL.
4. The [U.S. Web Design Standards](https://standards.usa.gov), which provides design guidelines and code to quickly create trustworthy, accessible and consistent digital government services that meet Web Content Accessibility Guidelines.
5. [Flask](http://flask.pocoo.org), a microfreamework for Python based on [Werkzeug](http://werkzeug.pocoo.org/docs/0.11/), the WSGI toolkit, and [Jinja 2](http://jinja.pocoo.org/docs/2.9/), a templating language based on Django's templating approach. 
6. [Heroku](https://www.heroku.com/home) as our prototype's platform-as-a-service.
7. [Travis CI](https://travis-ci.org), for continuous integration and testing. 

	To be added: 
	
	8. AWS
	9. Skyliner
	10. Docker
	
m. Deployed the prototype on an Infrastructure as a Service (IaaS) or Platform as Service (PaaS) provider, and indicated which provider they used;

**This project is using [Heroku](https://www.heroku.com) as PaaS provider, see the following [Issue](https://github.com/VeryLittleGravitas/CDTADPQ/issues/3) for the inital setup of the Heroku deployment pipeline.**

**We are currently automatically deploying the master branch to [https://vlg-ctdadpq.herokuapp.com](https://vlg-ctdadpq.herokuapp.com).**

n. Developed automated unit tests for their code;

**Our Github respository includes a master list of unit tests at https://github.com/VeryLittleGravitas/CDTADPQ/blob/master/test.py**

**Automated tests are run by Travis CI, and the results are available at https://travis-ci.org/VeryLittleGravitas/CDTADPQ/builds**

o. Setup or used a continuous integration system to automate the running of tests and continuously deployed their code to their IaaS or PaaS provider;

**We are using [Travis CI](https://travis-ci.org) for continuous integration, automatically and continuously deploying the master branch to [https://vlg-ctdadpq.herokuapp.com](https://vlg-ctdadpq.herokuapp.com). See the following [Issue](https://github.com/VeryLittleGravitas/CDTADPQ/issues/3) for initial setup.**

p. Setup or used configuration management;

**In-progress, dependent upon [Issue 95](https://github.com/VeryLittleGravitas/CDTADPQ/issues/95)**.

q. Setup or used continuous monitoring;

**In-progress, see [Issue 96](https://github.com/VeryLittleGravitas/CDTADPQ/issues/96)**.

r. Deployed their software in an open source container, such as Docker (i.e., utilized operating-system-level virtualization);

**In-progress, see [Issue 95](https://github.com/VeryLittleGravitas/CDTADPQ/issues/95)**.

s. Provided sufficient documentation to install and run their prototype on another machine; and

**Instructions on installation and running of the prototype can be found here: [https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Installing-and-running-the-prototype](https://github.com/VeryLittleGravitas/CDTADPQ/wiki/Installing-and-running-the-prototype).**

t. Prototype and underlying platforms used to create and run the prototype are openly licensed and free of charge.

**We have chosen the [MIT License](https://github.com/VeryLittleGravitas/CDTADPQ/blob/master/LICENSE) for this prototype.**