# arachne

Arachne is a next-generation implementation of the timeless object of the [Loom of Time](https://generative.ink/loom/toc/), the True Name of the multiversal interface. Improving upon the [first iteration](https://github.com/socketteer/loom), it is built from the ground up to be maximally extensible and serve as a testbed for new functionalities. Loom as originally envisioned is an interface which stores multiple trajectories sampled from a stochastic generative model as branches of a directed acyclic graph (often referred to as a "Loom tree" or "tapestry").

## architecture

Arachne's primary design principle is that of a "clean ontology": a minimalistic implementation of the Loom of Time, to be extended at will. Unlike its predecessor, Arachne is maximally modular, going so far as to separate its functionality into a backend (containing all the Loom functionality) and frontend (a client for interfacing with the Loom), allowing Arachne to serve as the foundation for any and all future Loom interfaces. It is also designed with support for future multi-user Loom interfaces in mind.

## plugins

Arachne's functionality can be easily extended in the form of plugins. Plugins are modular extensions which can be loaded or unloaded at runtime, with plugin lists definable at both the tree and user level. When (un)loaded, plugins' callbacks are (de)registered across Arachne, and any custom assets are (un)loaded as well.

### plugin: metaprocesses

Metaprocesses are large language model programs ([Schlag et al 2023](https://arxiv.org/abs/2305.05364)) which run "on top of" the primary text generation process (hence the name) - essentially, prompt templates which are formatted when run with relevant information extracted from the context window (current branch) and return output of any form (generally either multiple completions or a probability). *Not yet implemented.*

### plugin: multiloom

Multiloom is a plugin which extends Arachne's base functionality to act as a server through which multiple Weavers (Loom users, potentially with different clientside interfaces) can operate on the same tapestry in a realtime collaborative fashion. *Not yet implemented.*