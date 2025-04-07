# Winter 2025 Assignment 2

How will your program gather required input?\n
-The program gathers input via command-line arguments.

How will your program accomplish its requirements?\n
-The program uses argparse for parsing command-line args.\n
-The program using shutil for directory/file/archiving operations.\n
-The program uses datetime module for making timestamps.

How will output be presented?\n
-Confimation for operations are output to the command-line.\n
-Metadata file is dropped with backup to show backup info.

What arguments or options will be included?\n
--restore tells the program to restore instead of backup (backup is default behaviour)\n
-positional arguments are 'source' and 'destination'\n
--compression_format specifies what format to compress the backup as.\n

MVP:\n
***Backing up a specified location to a specified file or directory. AND RESTORE SUCCESSFULLY***\n
-Tar, compression\n
-Tracking date/time timestamp, chronology\n
-Showing backup info in a metadata file.
