# Snappyer

Snappyer is a thin Python library (well, actually, it's a file) on top of [snap.py](http://snap.stanford.edu/snap/snap.py.html), version 0.8.1 or higher.

I wrote this while doing PA1 in 224W because I was tired of SNAP.py's non-Pythonic approach to life.

## What on Earth?
Stop using snap.py directly. Start being happier. Snappyer exposes three classes: *SnapGraph*, *SnapNode*, and *SnapEdge*.
They wrap up all the major functions of snap.py into classes that acutally make sense, take away all playing with pointers,
and use standard Python collections wherever possible.

### How do I program with this?
Put snappyer.py into your main directory. import * from snappyer.

See snappyer_test.py for everything I've implemented. Basically, use SnapGraphs, which will give you SnapNodes and SnapEdges.

### You're missing a function / something is broken
Sorry, I didn't think it was important, or I haven't seen the bug. Fix it, and pull request this repo.

If you just want to get around it, you can get raw snap.py objects and put them into
SNAP yourself: SnapGraph.raw_graph, SnapNode.raw_node, SnapEdge.raw_edge.

### Is this efficient?
Yep. It's a thin wrapper on top of snap.py that literally just rewrites function names. All of PA1 took this lib about
10-12 minutes to finish, which is as fast as I've heard anyone getting.

### Added bonus
My IDE now auto-completes, since it can see snappyer objects.

## Author / License
Stephen Trusheim, CC-BY-SA 3.0.
