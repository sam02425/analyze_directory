# Directory Analysis Scripts

This project contains two Python scripts for analyzing directory structures:

1. `analyze_directory.py`: Generates a detailed directory structure graph.
2. `analyze_directory_with_contents.py`: Generates a directory structure graph including file contents.

## Features

### analyze_directory.py
- Creates a nested dictionary representing the folder structure
- Prints a hierarchical representation of the directory structure
- Generates a detailed graph of the directory structure, including file sizes
- Saves the detailed graph to a text file

### analyze_directory_with_contents.py
- Includes all features of `analyze_directory.py`
- Additionally reads and includes the contents of text files in the output
- Handles binary files and large files safely

## Requirements

- Python 3.6 or higher

## Usage

1. Place the desired script in the directory you want to analyze or in a location accessible from that directory.

2. Open a terminal or command prompt and navigate to the directory containing the script.

3. Run the script using Python:

   For `analyze_directory.py`:
   ```
   python analyze_directory.py
   ```

   For `analyze_directory_with_contents.py`:
   ```
   python analyze_directory_with_contents.py
   ```

4. The script will analyze the current directory and its subdirectories.

5. The results will be displayed in the console and saved to a text file in the current directory:
   - `analyze_directory.py` saves to `directory_structure_detailed.txt`
   - `analyze_directory_with_contents.py` saves to `directory_structure_with_contents.txt`

## Output

The scripts generate a text-based graph of the directory structure. For example:

```
root_directory/
├── subdirectory1/
│   ├── file1.txt (1024 bytes)
│   └── file2.py (2048 bytes)
├── subdirectory2/
│   └── (empty)
└── file3.md (512 bytes)
```

`analyze_directory_with_contents.py` will also include the contents of text files in the output.

## Limitations

- `analyze_directory_with_contents.py` has a file size limit (default 100 KB) for reading file contents to prevent memory issues with large files.
- Binary files are marked as <<Binary File>> and their contents are not included.
- The scripts attempt to read files as UTF-8 text. Files with different encodings might not be read correctly.

## Caution

Be careful when running `analyze_directory_with_contents.py` on directories containing sensitive information, as it will output the contents of all readable text files.

## Customization

You can modify the scripts to change behavior such as:
- Adjusting the file size limit for content inclusion
- Changing the output file names
- Modifying the graph style or included information

## Contributing

Feel free to fork this project and submit pull requests with improvements or additional features.

## License

This project is open source and available under the [MIT License](LICENSE).
