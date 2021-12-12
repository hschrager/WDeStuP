# WDeStuP
This GitHub repository was created for my final project for Model Integrated Computing at Vanderbilt University. 
This repository uses WebGME to create a design studio that works with PetriNets. 
A PetriNet is made up of places, and transitions, and connected by arcs. Arcs can connect places to transitions and
transitions to places. Additionally, each place is represented by a marking, a non-negative integer. Inplaces of a transition t is a set of places where each element of a set is connected to the transition. 
Conversely, outplaces of a transition t is a set of places that are connected to the transition by arcs where the places are the destinations and the transition is the source.
A transition is enabled if for all inplaces of the transition the amount of tokens at the place is non zero.
Firing an enabled transitions decreases the amount of tokens on all inplaces by one and increases the amount of token in all outplaces of the transition by one.

There are 4 ways to classify a PetriNet:
1. Free-choice petri net - each transition has its own unique set if inplaces
2. State machine - every transition has exactly one inplace and one outplace
3. Marked graph - very place has exactly one out transition and one in transition
4. Workflow net - there is exactly one source and one sink, and every place in the PetriNet is reachable on a path from the source to the sink.
These classifications are available to see in a plugin button (?) through the WebGME GUI.

![image](https://user-images.githubusercontent.com/50844436/145728603-651fafad-3c6d-4d9c-931f-b6b0e18030aa.png)

Every place is represented by a circle, with the markings inside, and every transition is represented by the rectangles. 
Arcs are the arrows between each place and transition.

# Installation
To install the design studio, follow the steps below.
1. Clone the repository
2. Open terminal on your computer, and cd into the repository 
3. Run: docker-compose up -d to start the docker image
4. Open localhost:8888 online to access the WebGME GUI
5. Open the PetriNets2 project
6. From here, you can view the example models, make your own, and view the widget to fire transitions.

# How to Model
To create a new model and use the widget, follow the steps below.
1. Open the localhost:8888 and select PetriNets2
2. In Composition, enter into the examples folder
3. To create your own exmaple, drag a new PetriNet element onto the screen
  a. Click into the PetriNet, and create whatever network you like with the places and transitions. Don't forget to set the markings at each place
4. To use an existing example, click into one of the existing examples
5. Under the visualizer selectors, click onthe PNWidget
6. You can now see your network visualized. To fire a transition, double click on the desired rectangle
7. To reset the model, click the back arrows on the top toolbar
8. To view the classifications, click on the question mark on the top toolbar

# Features
This design studio provides a few simple features. The PNWidget visualizer lets the user fire allowed transitions, and 
alerts the user when a transition is not fireable. 
This visualizer also has a reset feature to reset the PetriNet back to the original state/markings. This can be done by clicking the back arrows button on the top toolbar. 
You can also view the classification of the PetriNet using the question mark button on the top toolbar. 
This will alert you on what classifiation the PetriNet created falls into: free-choice, state machine, marked graph, and workflow net.
