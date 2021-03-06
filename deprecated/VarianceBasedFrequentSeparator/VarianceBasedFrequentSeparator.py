import pickle
import settings
from File import File
from ComputeGramData import compute_gram_variance, count_gram_frequency
from LimitedContainer import LimitedContainer
from PrintProgress import print_progress


def main():
    print("Generating File Fragments and Computing n-gram Frequency...")
    num_fragments_done = 0
    num_total_fragments = settings.num_fragments * len(settings.directory_path) * settings.max_grams
    gram_frequency = []
    grams_introduced = set()
    for gram in range(settings.max_grams):
        gram_size = gram + 1
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

    print("\n\nComputing Variances...")
    variance_result = LimitedContainer(settings.num_separators_to_save, lambda x, y: x[1] > y[1])
    num_total_grams = len(grams_introduced)
    num_processing_done = 0
    for gram_key in grams_introduced:
        variance = compute_gram_variance(gram_key, gram_frequency[gram_key[0] - 1])
        variance_result.push((gram_key, variance))
        num_processing_done += 1
        print_progress(num_processing_done, num_total_grams)
    print_progress(num_processing_done, num_total_grams)

    # pick the topmost and print the result
    print("\n\nSorting and saving...")
    result_gram_values = [[] for _ in range(settings.max_grams)]
    for _ in range(settings.num_separators_to_save):
        gram_size, gram_value = variance_result.pop()[0]
        result_gram_values[gram_size - 1].append(gram_value)

    for gram in range(settings.max_grams):
        result_gram_values[gram] = list(sorted(result_gram_values[gram]))

    result = [dict() for _ in range(settings.max_grams)]
    for gram in range(settings.max_grams):
        for i in range(len(result_gram_values[gram])):
            gram_value = result_gram_values[gram][i]
            result[gram][gram_value] = i

    with open("./frequent_separators.pickle", "wb") as file:
        pickle.dump(result, file)

    print("./frequent_separators.pickle has been saved.")
    print("Done.")

    print("\n\nSelection Result:")
    for gram in range(settings.max_grams):
        print("\t- At {}-gram, {} separators are selected.".format(gram + 1, len(result_gram_values[gram])))


if __name__ == "__main__":
    main()
