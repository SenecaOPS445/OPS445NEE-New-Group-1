# Winter 2025 Assignment 2

How will your program gather required input?
-The program gathers input via command-line arguments.

How will your program accomplish its requirements?
-The program uses argparse for parsing command-line args.
-The program using shutil for directory/file/archiving operations.
-The program uses datetime module for making timestamps.

How will output be presented?
-Confimation for operations are output to the command-line.
-Metadata file is dropped with backup to show backup info.

What arguments or options will be included?
--restore tells the program to restore instead of backup (backup is default behaviour)
-positional arguments are 'source' and 'destination'
--compression_format specifies what format to compress the backup as.

MVP:
***Backing up a specified location to a specified file or directory. AND RESTORE SUCCESSFULLY***
-Tar, compression
-Tracking date/time timestamp, chronology
-Showing backup info in a metadata file.
