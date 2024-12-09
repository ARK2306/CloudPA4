from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, count

# Create a SparkSession
spark = SparkSession.builder.appName("InferenceErrorCount").getOrCreate()

# Read the data from a CSV file
df = spark.read.csv("MapReduce_data.csv", header=True)

# Create a mapping dictionary for class names to class IDs
class_mapping = {
    "beaver": 1, "dolphin": 2, "otter": 3, "seal": 4, "whale": 5,
    "aquarium fish": 6, "flatfish": 7, "ray": 8, "shark": 9, "trout": 10,
    "orchids": 11, "poppies": 12, "roses": 13, "sunflowers": 14, "tulips": 15,
    "bottles": 16, "bowls": 17, "cans": 18, "cups": 19, "plates": 20,
    "apples": 21, "mushrooms": 22, "oranges": 23, "pears": 24, "sweet peppers": 25,
    "clock": 26, "computer keyboard": 27, "lamp": 28, "telephone": 29, "television": 30,
    "bed": 31, "chair": 32, "couch": 33, "table": 34, "wardrobe": 35,
    "bee": 36, "beetle": 37, "butterfly": 38, "caterpillar": 39, "cockroach": 40,
    "bear": 41, "leopard": 42, "lion": 43, "tiger": 44, "wolf": 45,
    "bridge": 46, "castle": 47, "house": 48, "road": 49, "skyscraper": 50,
    "cloud": 51, "forest": 52, "mountain": 53, "plain": 54, "sea": 55,
    "camel": 56, "cattle": 57, "chimpanzee": 58, "elephant": 59, "kangaroo": 60,
    "fox": 61, "porcupine": 62, "possum": 63, "raccoon": 64, "skunk": 65,
    "crab": 66, "lobster": 67, "snail": 68, "spider": 69, "worm": 70,
    "baby": 71, "boy": 72, "girl": 73, "man": 74, "woman": 75,
    "crocodile": 76, "dinosaur": 77, "lizard": 78, "snake": 79, "turtle": 80,
    "hamster": 81, "mouse": 82, "rabbit": 83, "shrew": 84, "squirrel": 85,
    "maple": 86, "oak": 87, "palm": 88, "pine": 89, "willow": 90,
    "bicycle": 91, "bus": 92, "motorcycle": 93, "pickup truck": 94, "train": 95,
    "lawn-mower": 96, "rocket": 97, "streetcar": 98, "tank": 99, "tractor": 100
}

# Map the inferred_value to the corresponding class ID
df = df.withColumn("inferred_value_id", df["inferred_value"].cast("integer"))

# Replace the inferred_value with the mapped class ID
df = df.replace(class_mapping, subset=["inferred_value_id"])

# Map phase: Compute incorrect inference count per producer
incorrect_inferences = df.where(col("inferred_value_id") != col("ground_truth")) \
                        .groupBy("producer") \
                        .agg(count("*").alias("incorrect_inferences_count")) \
                        .orderBy("incorrect_inferences_count", ascending=False)

# Print the results in the desired format
for row in incorrect_inferences.collect():
    print(f"{row.producer:<40} {row.incorrect_inferences_count:>10}")
