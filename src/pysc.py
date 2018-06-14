import argparse
import numpy as np
from scipy.sparse import coo_matrix

from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.mllib.linalg.distributed import IndexedRow, IndexedRowMatrix

def read_input(contents):
    """
    Assumes a text-based, CSV-type input in a single file. Parses it out
    into dense vectors, then converts to sparse if needed.

    This is run after a zipWithIndex, so everyone knows what row they're on.
    """
    line, index = contents
    sparse = SPARSE.value
    elems = list(map(np.float, line.split()))
    if sparse:
        vector = coo_matrix(elems)
    else:
        vector = np.array(elems)
    return IndexedRow(index, vector)

def distance(rows):
    row1, row2 = rows
    i, j = row1.index, row2.index
    (length, _, gamma, _) = METADATA.value

    # Compute similarity.
    aij = 0

    # Dump into an N-length vector.
    ai = np.zeros(shape = (length,))
    ai[j] = aij

    # Convert to proper sparsity, if needed.

    # All done.
    return (i, aij)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'PySC',
        epilog = 'PySpark Spectral Clustering', add_help = 'How to use',
        prog = 'spark-submit pysc.py <options>')

    # Required arguments.
    parser.add_argument("-i", "--input", required = True,
        help = "Input file containing data.")

    # Optional arguments.
    parser.add_argument("-g", "--gamma", type = float, default = None,
        help = "Width of the neighborhood to be considered. If None, defaults to 1/<dim>. [DEFAULT: None]")
    parser.add_argument("-k", "--clusters", type = int, default = 8,
        help = "Number of clusters to generate. [DEFAULT: 8]")
    parser.add_argument("-s", "--sparse", action = "store_true",
        help = "If set, converts each row to a sparse array. [DEFAULT: False]")
    parser.add_argument("-o", "--output", default = None,
        help = "Path to the output directory <X_i, y_i> pairs will be written. If None, output is written to stdout. [DEFAULT: None]")

    args = vars(parser.parse_args())
    spark = SparkSession(SparkContext())
    SPARSE = spark.sparkContext.broadcast(args['sparse'])

    # Read the input.
    rdd = spark.sparkContext.textFile(args['input']) \
        .zipWithIndex() \
        .map(read_input)
    X = IndexedRowMatrix(rdd)

    # Broadcast everything else.
    METADATA = spark.sparkContext.broadcast([X.numRows(), X.numCols(), args['gamma'], args['clusters']])

    # Compute an affinity matrix.
    A = IndexedRowMatrix(
        X.rows.cartesian(X.rows) \
        .map(distance)
    ) # DO NOT DO THIS. EVER. Except in pre-pre-alpha testing.
    print(A.rows.collect())
