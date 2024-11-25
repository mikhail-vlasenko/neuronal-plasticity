# NDDL-cortical-circuit
Hi all,

Hope you're ready to dive into the realm of cortical circuits.

First of all, I would like to suggest that you each create a **private** Github repository for your code during the project. This way, you can track your progress during the project and ensure that your code doesn't break with no way of fixing it. If you haven't used git or version control before, no worries, here is a link where you can find some basic information about it: https://www.freecodecamp.org/news/what-is-git-learn-git-version-control/. You don't have to look to much into how to collaborate with others using git at this point, as I suggest you use it merely as a way to keep track of your own code. **Why private?** Because in the event that you'll stumble across an interesting discovery that you'll want to continue working on even after the course ends, you can ensure that your project information/implementation is protected, which is important in our field.

**How to start?** I would suggest that you start by reading the papers below, as well as performing the Tutorials from Brian2, which go into how the simulator works, how neuronal populations can be created, how synapses work etc. You can find the tutorials in the original Brian2 documentation: https://brian2.readthedocs.io/en/stable/. In addition, Brian2 has a very active developers community / forum and they take the time to reply to questions related to their simulator. It has proven very useful for me in the past, so I suggest you to not be afraid to post your technical questions on the forum or exchange ideas: https://brian.discourse.group/.

In parallel, it would be useful to start reading some literature on the topic. Here are some useful papers:

**Fundamental Literature**

**1.**  Synaptic plasticity is required for oscillations in a V1 cortical column model with multiple interneuron types. Giulia Moreni, Cyriel M. A. Pennartz, Jorge F. Mejias.
bioRxiv 2023.08.27.555009; doi: https://doi.org/10.1101/2023.08.27.555009: This paper describes the initial cortical column model as implemented by Giulia Moreni, who is a senior PhD in our lab. It gives a description of the parameters, equations and where the data to construct the model comes from. In addition, it has results from simulations in which spike-time dependent plasticity was added to the model, however, you can skip this section and only look at the introductory parts and methods to get a feel of the model. Important parts are the ones refering to spontaneous activity, from which you will start with the model.

**2.** Cell-type-specific firing patterns in a V1 cortical column model depend on feedforward and feedback-driven states. Giulia Moreni, Cyriel M. A. Pennartz, Jorge F. Mejias. bioRxiv 2024.10.24, doi: https://doi.org/10.1101/2024.04.02.587673. This paper takes the model and looks at specific effects of feedforward and feedback stimulation on the network activity. It is interesting to read if you want to know more about the role that specific neuronal populations have in the model and also to link it to visual stimulation. You can take inspiration from the experiments performed here and come up with new ideas.

**Modelling Dendrites**

**1.** Introducing the Dendrify framework for incorporating dendrites to spiking neural networks. M Pagkalos, S Chavlis, P Poirazi, DOI: https://doi.org/10.1038/s41467-022-35747-8. This paper introduces a very nice tool called Dendrify, which allows the implementation of simplified compartmental models to study dendritic contributions to dynamics. The tool itself can be found at: https://dendrify.readthedocs.io/en/latest/index.html. It has good tutorials and examples that you can start from. In general Poirazi's lab (senior authod in the Dendrify paper) is a very good starting point for anything to do with dendrites. Another lab you can check out for such topics is Claudia Clopath's lab at Imperial College London.

**Useful links**
- https://modeldb.science/: ModelDB is a very useful database which contains neuron models (both single neurons and populations) implemented in various languages and simulators, including Brian2. You might want to have a look in there before you implement something yourself (for inspiration or to re-use an already existing implementation, this can save lots of time).
- https://neuronaldynamics.epfl.ch/online/index.html: Online version of a great book on neuronal dynamics by W. Gerstner if you'd like to dive deeper into the theory or gather ideas (it is quite mathematical, although it is very useful to learn some basic concepts).


