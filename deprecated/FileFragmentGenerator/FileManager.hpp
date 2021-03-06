#ifndef FILEFRAGMENTGENERATOR_FILEMANAGER_HPP
#define FILEFRAGMENTGENERATOR_FILEMANAGER_HPP

#include <dirent.h>
#include <fstream>
#include "json.hpp"

using json = nlohmann::json;

namespace baryberri {
    class FileManager;
}

class baryberri::FileManager {
public:
    /// create a new FileManager.
    /// as it doesn't call setToNextFileType automatically, it should be called manually.
    explicit FileManager();

    /// create a new FileManager with set to given fileType.
    ///
    /// \param fileType fileType to set
    explicit FileManager(const std::string& fileType);

    /// close the directory before FileManager destructs.
    ~FileManager();

    const std::string& getCurrentFileType();

    /// Returns is directory of given file type exists, and well-opened.
    ///
    /// \return true if directory exists and opened, otherwise false.
    const bool isDirectoryExist();

    /// change currentFileType and currentTypesInputDirectoryPath to next available file type.
    ///
    /// \param reset true if it's wanted to reset currently selected file type.
    /// \return false if there's no next file type available, else returns true.
    const bool setToNextType();

    /// make one fragment, and save it into .csv file.
    void makeFragment();

    /// make the given number of fragments, and save it into .csv file.
    ///
    /// \param fragmentNumber wanted number of fragments to generate
    void makeFragments(const int fragmentNumber);

    /// set settings with given json file.
    ///
    /// \param settings json settings to set
    static void setSettings(json* settings);

private:
    /// settings has "fileType": ["html", "hwp", "pdf", "docx", "xlsx"] field.
    /// currentFileType indicates currently selected file type.
    std::string currentFileType;

    /// saves currently selected file type's index.
    /// for example, "hwp" becomes index 1 in the example above.
    int currentFileTypeIndex;

    /// current input directory path, like "./hwp/"
    std::string currentInputDirectoryPath;

    /// indicates the current directory.
    DIR* currentDirectory;

    /// the starting offset where the fragmentation starts.
    int baseOffset;

    /// current file's offset
    int currentFileOffset;

    /// used gram's size when byte frequency is counted.
    /// set to 0 when raw data is needed.
    int gramSize;

    /// fragment's size
    int fragmentSize;

    /// number of fragments per each csv.
    int numOfFragmentsPerCSV;

    /// input file's path
    std::string inputFilePath;

    /// numerator and denominator of the base offset.
    int numerator;
    int denominator;

    /// indicates the current file.
    struct dirent* currentFile;

    /// save settings.json
    static json* settings;

    /// number of total file types
    static int numOfFileTypes;

    /// number of groups of file types
    static int numOfGroups;

    /// save current output stream's path.
    static std::string outputBasePath;

    /// save current output stream's number.
    static int currentOutputFileNumber;

    /// current input file stream.
    static std::ifstream inputFileStream;

    /// current output file stream.
    static std::ofstream outputFileStream;

    /// reset the currentFile and restart iterating current directory.
    void rewindFile();

    /// Initialize currentFile.
    ///
    /// \return false if initialize fails.
    bool initializeFile();

    /// set currentFileStream to next file.
    void setToNextFile();

    /// gets an available file's path inside currentTypesInputDirectoryPath.
    /// the file is checked whether it has same corresponding extension with currentFileType.
    ///
    /// \return a file's path, if available. If there's no file available, returns empty string.
    const std::string getNextFilePath();

    /// read a new fragment in currentFileStream, and save it into fragmentArray.
    void getFragment(char* fragmentArray);

    /// save raw data read by getFragment into csv file
    void saveRawFragmentData(char* const& fragmentArray);

    /// compute n-gram frequency data from fragmentArray, and save it into gramArray.
    void computeNgram(char* const& fragmentArray, int* gramArray);

    /// save n-gram data into csv file.
    void saveGramData(double* const& gramArray);

    /// set offset to next available offset.
    void setToNextOffset();

    /// reset the start offset.
    void resetOffset();

    /// open an input stream to read.
    void reloadInputStream();

    /// checks whether given str has a given suffix.
    /// \param str string to test whether it has given suffix or not
    /// \param suffix suffix string to test
    /// \return true if given str has given suffix, otherwise false.
    static const bool has_suffix(const std::string& str, const std::string& suffix);

    /// checks whether given string has a given prefix.
    /// \param str string to test whether it has given prefix or not
    /// \param prefix  prefix string to test
    /// \return true if given string has given prefix, otherwise false.
    static const bool has_prefix(const std::string& str, const std::string& prefix);

    /// change current output stream into next output stream.
    static void changeToNextOutputFile();
};

#endif //FILEFRAGMENTGENERATOR_FILEMANAGER_HPP
