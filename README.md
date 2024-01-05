# arachne

Arachne is a next-generation implementation of the timeless object of the [Loom of Time](https://generative.ink/loom/toc/), the True Name of the multiversal interface. Improving upon the [first iteration](https://github.com/socketteer/loom), it is built from the ground up to be maximally extensible and serve as a testbed for new functionalities, remaining agnostic about the type of generative model or the modality (or modalities) thereof. Loom as originally envisioned is an interface which stores multiple trajectories sampled from a stochastic generative model as branches of a directed acyclic graph (often referred to as a "Loom tree").

## architecture

Arachne's primary design principle is that of a "clean ontology": a minimalistic implementation of the Loom of Time, to be extended at will. Unlike its predecessor, Arachne is maximally modular, going so far as to separate its functionality into a backend (containing all the Loom functionality) and frontend (a client for interfacing with the Loom), allowing Arachne to serve as the foundation for any and all future Loom interfaces. It is also designed with support for future multi-user Loom interfaces in mind.

There are three fundamental components to Arachne: **tapestry, weft, and warp.**

### tapestry

The **tapestry** is the underlying data structure of Arachne and a generalization of the Loom tree. In essence, it is a directed acyclic hypergraph which stores histories of operations on some initial data object(s) in a compressed format, such that node boundaries (regardless of the modality) correspond to either boundaries of counterfactuals or the edge of the unknown (the boundary of generated data). The directionality of a **tapestry**, unlike Loom trees, is not inherently tied to any spatiotemporal dimension of the data; it instead serves only as an indicator of computational time, or the order of the updates to the initial data object(s). While **tapestry** nodes are compressed to factor out common data from sibling nodes (in a manner similar to a trie), they preserve the underlying finer-grained update history; think of the refactoring operation as merging contiguous, linear (non-branching) segments of the update history into single nodes.

### weft

**Weft** refers to any external functionalities (calculations, programs, retrieval, calls to simulators, etc) or compound constructions thereof. A **weft** program takes in some data (normally the state of the initial data object(s) at some node in the **tapestry**) as input and returns some data as output. **Weft** programs are defined according to a standardized schema, but can refer to any external functionality whatsoever.

### warp

**Warp** refers to the set of basic operations by which Arachne mediates the exchange of data between a **tapestry** and its **weft** - in other words, the **warp** weaves the **weft** into the **tapestry**. **Warp** operations make alterations to the **tapestry**, sometimes taking parts of the **tapestry** to pass to a **weft** program as input and making the necessary alterations to the **tapestry** to incorporate its output.

## credits

I am of course eternally indebted to my friend and mentor Janus for implementing the [first iteration](https://github.com/socketteer/loom) of the Loom, which showed me what was possible (and perhaps more importantly, what would soon be).

I also owe thanks to my friend [CrazyPython](https://github.com/CrazyPython) for writing [Chapter 2](https://github.com/CrazyPython/chapter2) and showing me what the principle of a "clean ontology" looks like in practice.
