# FileOptimizerMultithreaded
Adds multithreading support to Nikkho's FileOptimzier (https://sourceforge.net/projects/nikkhokkho/).

pip install -r requirements.txt

Put the multithreaded_fileoptimizer.py file in the same directory where you've downloaded FileOptimizer64.exe.
If you want to edit the options, open FileOptimizer64 first and change the options there (I would recommend setting the process priority to below normal or idle, turning off recycle bin after testing, and turning on cache).

Run multithreaded_fileoptimizer.py, select a path, and wait.
A progress bar is visible and size states are printed after completion.
