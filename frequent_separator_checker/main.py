import pickle
import os
from fragment import Fragment
from separator_checker import SeparatorChecker
from separator_filter import SeparatorFilter


def main():
    # Setup Fragment
    file_types = ["exe", "html", "hwp", "jpg", "mp3", "pdf", "png"]
    directories = ["/Users/barber/Data/fti_small_data/train_data/exe",
                   "/Users/barber/Data/fti_small_data/train_data/html",
                   "/Users/barber/Data/fti_small_data/train_data/hwp",
                   "/Users/barber/Data/fti_small_data/train_data/jpg",
                   "/Users/barber/Data/fti_small_data/train_data/mp3",
                   "/Users/barber/Data/fti_small_data/train_data/pdf",
                   "/Users/barber/Data/fti_small_data/train_data/png"]
    fragment_getter = Fragment(file_types=file_types, directories=directories, fragment_size=4096)

    if os.path.exists("./frequent_separators.pickle"):
        with open("./frequent_separators.pickle", "rb") as file:
            total_frequent_separators = pickle.load(file)
        print("Frequent Separators pickle found and loaded.")
    else:
        print("Frequent Separators pickle not found. Computing with given data.")
        # Setup Separator checker
        separator_checker = SeparatorChecker()
        obvious_separators, obvious_gram_size = SeparatorChecker.obvious_separators()
        candidate_separators, gram_size = SeparatorChecker.init_candidate()
        total_frequent_separators = dict()

        # Compute
        print("At 2-gram:")
        print("\tCandidate: 65536 separators.")
        while len(candidate_separators) != 0:
            separator_checker.set_candidate_separators(candidate_separators=candidate_separators, gram_size=gram_size)
            fragment, _ = fragment_getter.get_fragment()
            while fragment is not None:
                separator_checker.count_fragment(fragment=fragment)
                fragment, _ = fragment_getter.get_fragment()

            frequent_separators_list = separator_checker.get_frequent_separators_frequency(threshold=0.05)

            print("\t{} separators are frequent.".format(len(frequent_separators_list)))

            if len(frequent_separators_list) <= 0:
                break

            SeparatorChecker.print_top_5(frequent_separators_list)
            SeparatorChecker.print_bottom_5(frequent_separators_list)

            frequent_separators_set = SeparatorChecker.separators_into_set_form(frequent_separators_list)
            total_frequent_separators[gram_size] = frequent_separators_set

            candidate_separators = separator_checker.make_candidate_separators(frequent_separators_set)
            gram_size += 1

            if gram_size > 20:
                break

            print("\nAt {}-gram:".format(gram_size))
            print("\tCandidates: {} separators.".format(len(candidate_separators)))

        with open("./frequent_separators.pickle", "wb") as file:
            pickle.dump(total_frequent_separators, file, protocol=pickle.HIGHEST_PROTOCOL)
        print("\nFrequent Separators saved.")

        print()
        total_separators_count = 0
        for gram, separators in total_frequent_separators.items():
            print("At {}-gram, {} separators are selected.".format(gram, len(separators)))
            total_separators_count += len(separators)
        print("Total {} separators are selected.".format(total_separators_count))

    print("\nFiltering Separators...")
    separator_filter = SeparatorFilter(file_types, total_frequent_separators)
    fragment, file_type = fragment_getter.get_fragment()
    while fragment is not None:
        separator_filter.count_fragment(fragment=fragment, file_type=file_type)
        fragment, file_type = fragment_getter.get_fragment()
    filtered_separators = separator_filter.filter_grams(threshold=0.9)
    formatted_separators = SeparatorFilter.change_filtered_gram_form(filtered_separators)

    with open("./filtered_separators.pickle", "wb") as file:
        pickle.dump(formatted_separators, file, protocol=pickle.HIGHEST_PROTOCOL)
    print("\nFiltered separators saved.\n")

    total_separators_count = 0
    for gram, separators in filtered_separators.items():
        print("At {}-gram, {} separators are filtered.".format(gram, len(separators)))
        total_separators_count += len(separators)
    print("Total Separators: {}".format(total_separators_count))
    print(formatted_separators)
    separator_filter.print_gram_type_statistics(formatted_separators)


if __name__ == "__main__":
    main()
