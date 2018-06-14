# PySC

PySpark Spectral Clustering.

## Overview and Goal

The goal of this project is to ascertain a performance benchmark for spectral
clustering in Spark, particularly as compared to the native Scala-based
implementation [here](https://github.com/quinngroup/osdsc).

It is also meant as a baseline for comparison against the [dask-ml spectral
clustering](https://dask-ml.readthedocs.io/en/latest/auto_examples/plot_spectral_clustering.html)
pipeline.

Ultimately, this would be a jumping-off point for experimenting with different
methods of approximating the affinity matrix, implicit computation of the
leading eigenvectors, adaptive neighborhood sizes, and other strategies for
improving runtime.

**This is super bleeding-edge, pre-alpha work that is not meant for production!**

## Dependencies

 - Python 3.5
 - Spark 2.2

Other dependencies as development continues.

## Related Projects

[pyspark-lsh](https://github.com/magsol/pyspark-lsh): This was an early attempt
to build a locality-sensitive hashing library from scratch using PySpark. This
approach could still be useful in building a collection of high-probability
neighbors for the affinity graph.

[PySpark-Affinities](https://github.com/magsol/PySpark-Affinities): This was a
an initial foray into computing affinities of images in an efficient, NumPy-friendly
way. However it tended to rely on full cartesian products, infeasible in a
distributed environment.

## How to Contribute

Send in a PR! Would love the help.

## License

MIT.
