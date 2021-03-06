import tensorflow as tf


# Flags to use. DO NOT MODIFY HERE!
# =================================
FLAGS = tf.app.flags.FLAGS
# =================================


# DEFINE CONSTANTS HERE!
# =================================

# model name
FLAGS.model_name = "frequency_symmetric_8_layer_1-1gram"

# input directory
FLAGS.train_data_path = "/Users/barber/Development/GitHub/file-type-identification/Trainer/TrainData/5type_fn_only_m1/train_data"
FLAGS.validation_data_path = "/Users/barber/Development/GitHub/file-type-identification/Trainer/TrainData/5type_fn_only_m1/validation_data"
FLAGS.test_data_path = "/Users/barber/Development/GitHub/file-type-identification/Trainer/TrainData/5type_fn_only_m1/test_data"

# ln earning rate
FLAGS.learning_rate = 1e-5

# keep probability for dropout while training
FLAGS.keep_prob_train = 0.9

# input dimension
FLAGS.input_dimension = 256

# global steps to repeat
FLAGS.num_of_total_global_steps = 10000

# checkpoint steps to save and validate
FLAGS.checkpoint_steps = 2000

# steps to print cost
FLAGS.cost_print_step = 100

# a mini batch's size
FLAGS.batch_size = 100

# csv information
FLAGS.num_of_fragments_per_csv = 100

# file information
FLAGS.num_of_validation_files_per_type = 2000
FLAGS.num_of_test_files_per_type = 4000

# type information
FLAGS.num_of_groups = 5
FLAGS.group_name = ["mp3", "hwp", "pdf", "jpg", "png"]
FLAGS.num_of_types_per_group = [1, 1, 1, 1, 1]
# =================================
