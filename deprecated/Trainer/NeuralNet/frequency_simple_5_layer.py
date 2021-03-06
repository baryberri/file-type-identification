from layer import *

# input placeholders
# x: byte value (0 ~ 255)
# y: 5 file types in one hot encoding
X = tf.placeholder(tf.float32, [None, 256])
Y = tf.placeholder(tf.float32, [None, FLAGS.num_of_groups])

# keep probability placeholder for dropout
keep_prob = tf.placeholder(tf.float32)

# Layers
L1 = simple_layer("1", input_tensor=X, input_size=256, output_size=512, relu=True, dropout=True, keep_prob=keep_prob)
L2 = simple_layer("2", input_tensor=L1, input_size=512, output_size=256, relu=True, dropout=True, keep_prob=keep_prob)
L3 = simple_layer("3", input_tensor=L2, input_size=256, output_size=128, relu=True, dropout=True, keep_prob=keep_prob)
L4 = simple_layer("4", input_tensor=L3, input_size=128, output_size=32, relu=True, dropout=True, keep_prob=keep_prob)
hypothesis = simple_layer("5", input_tensor=L4, input_size=32, output_size=FLAGS.num_of_groups,
                          relu=False, dropout=False, keep_prob=keep_prob)
