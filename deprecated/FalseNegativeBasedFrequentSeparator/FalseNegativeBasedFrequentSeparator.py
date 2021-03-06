import pickle
import settings
import os
import copy
from File import File
from ComputeGramData import compute_gram_variance, count_gram_frequency
from PrintProgress import print_progress


def main():
    len_grams = settings.finish_gram - settings.start_gram + 1

    if os.path.exists("./saved_count_data.pickle"):
        print("Do you want to load saved count information?")
        user_selection_input = input("(y / N) : ")
    else:
        user_selection_input = "n"

    if user_selection_input.lower() == "y":
        with open("saved_count_data.pickle", "rb") as file:
            load_data = pickle.load(file)
            grams_introduced = load_data[0]
            gram_frequency = load_data[1]
    else:
        print("Generating File Fragments and Computing n-gram Frequency...")
        num_fragments_done = 0
        num_total_fragments = settings.num_fragments * len(settings.directory_path) * len_grams
        gram_frequency = []
        grams_introduced = set()
        for gram in range(len_grams):
            gram_size = gram + settings.start_gram
            gram_frequency.append(dict())
            for file_type in settings.directory_path.keys():
                gram_frequency[gram][file_type] = dict()
                file = File(settings.directory_path[file_type])

                fragment_data = file.read(settings.fragment_size_in_bytes)
                fragments_processed = 0
                while fragment_data is not None and fragments_processed < settings.num_fragments:
                    count_gram_frequency(gram_size, fragment_data, gram_frequency[gram][file_type], grams_introduced)
                    fragments_processed += 1
                    fragment_data = file.read(settings.fragment_size_in_bytes)

                    num_fragments_done += 1
                    print_progress(num_fragments_done, num_total_fragments)

        print_progress(num_fragments_done, num_total_fragments)

        # print("\n\nSaving Count Information...")
        # with open("saved_count_data.pickle", "wb") as file:
        #     save_data = [grams_introduced, gram_frequency]
        #     pickle.dump(save_data, file, protocol=pickle.HIGHEST_PROTOCOL)
        # print("Successfully saved at './saved_count_data.pickle'.")

    print("\n\nComputing Scores...")
    variance_result = []
    num_total_grams = len(grams_introduced)
    num_processing_done = 0
    for gram_key in grams_introduced:
        fn = compute_gram_variance(gram_key, gram_frequency[gram_key[0] - settings.start_gram])
        if fn <= settings.false_negative_level_to_pick:
            variance_result.append((gram_key, fn))
        num_processing_done += 1
        print_progress(num_processing_done, num_total_grams)
    print_progress(num_processing_done, num_total_grams)
    variance_saved = copy.deepcopy(variance_result)

    # pick the topmost and print the result

    result_gram_values = [[] for _ in range(len_grams)]

    for i in range(len(variance_result)):
        gram_size, gram_value = variance_result[i][0]
        result_gram_values[gram_size - settings.start_gram].append(gram_value)

    for gram in range(len_grams):
        result_gram_values[gram] = list(sorted(result_gram_values[gram]))

    result = dict()
    for gram in range(len_grams):
        result_index = gram + settings.start_gram
        result[result_index] = dict()
        for i in range(len(result_gram_values[gram])):
            gram_value = result_gram_values[gram][i]
            result[result_index][gram_value] = i

    print("\n\nSelection Result:")
    for gram in range(len_grams):
        print("\t- At {}-gram, {} separators are selected."
              .format(gram + settings.start_gram, len(result_gram_values[gram])))

    print("\n\nSaving...")
    with open("./frequent_separators.pickle", "wb") as file:
        pickle.dump(result, file, protocol=pickle.HIGHEST_PROTOCOL)

    print("./frequent_separators.pickle has been saved.")

    print("\n\nSaving Separator Information...")
    with open("./separators_information.csv", "w") as file:
        # saving gram keys
        for i in range(len_grams):
            for gram in result[i + settings.start_gram].keys():
                file.write("{},".format(hex(gram)[2:].upper()))
        for file_type in settings.directory_path.keys():
            file.write("{},".format(file_type))
        file.write("\n")

        # saving false negative rates
        for i in range(len_grams):
            for gram in result[i + settings.start_gram].keys():
                variance = list(filter(lambda x: x[0] == (i + settings.start_gram, gram), variance_saved))[0][1]
                file.write("{:2.6f},".format(variance))

        for file_type in settings.directory_path.keys():
            file.write("{},".format(file_type))

    print("Separator information has been saved at './separators_information.csv'.")


if __name__ == "__main__":
    main()
