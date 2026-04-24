import os
import sys

from pyspark import SparkContext
#from pyspark import HiveContext

args = sys.argv
inp = args[1]
out = args[2]

sc = SparkContext()
#sqlContext = HiveContext(sc)

text_file = sc.textFile(inp)
counts = text_file.flatMap(lambda line: line.split(" ")) \
             .map(lambda word: (word, 1)) \
             .reduceByKey(lambda a, b: a + b)
counts.saveAsTextFile(out)

sc.stop()







