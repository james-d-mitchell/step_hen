.. image:: https://mybinder.org/badge_logo.svg
 :target: https://mybinder.org/v2/gh/james-d-mitchell/stephen/main?filepath=demo.ipynb

**********************************************************
README - stephen - by James D. Mitchell and Maria Tsalakou
**********************************************************

``stephen`` contains a rudimentary implementation of three algorithms of J. B.
Stephen and Andrew Cutting for finitely presented monoids and inverse monoids
in python3. These algorithms can be used to check equality of a fixed word
with any other word in a finitely presented monoid, or inverse monoid, and to
compute the structure of a finitely presented inverse monoid. 

The implementation is rudimentary because it lacks many obvious optimisations
and improvements, it is intended as a simple proof of concept.

The algorithms are described in the following:

* J. B. Stephen, "Presentations of inverse monoids", *J. Pure Appl. Algebra*,
  **63** (1990) 81--112; `<http://dx.doi.org/10.1016/0022-4049(90)90057-O>`_

* J. B. Stephen, "Applications of automata theory to presentations of monoids
  and inverse monoids", The University of Nebraska - Lincoln (1987);
  `<https://digitalcommons.unl.edu/dissertations/AAI8803771>`_

* Andrew Cutting, "Todd-Coxeter methods for inverse monoids", PhD thesis,
  University of St Andrews (2001) `<http://hdl.handle.net/10023/15052>`_

.. TODO installation
