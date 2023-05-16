import subprocess
from pathlib import Path
import tkinter
from tkinter import filedialog
from multiprocessing import Pool
import tqdm
import heapq
import os.path


# https://stackoverflow.com/questions/61648065/split-list-into-n-sublists-with-approximately-equal-sums
def sublist_creator(lst, n):
    lists = [[] for _ in range(n)]
    totals = [(0, i) for i in range(n)]
    heapq.heapify(totals)
    for value in lst:
        total, index = heapq.heappop(totals)
        lists[index].append(value)
        heapq.heappush(totals, (total + value.stat().st_size, index))
    return lists


def process_file(file):
    subprocess.run(["FileOptimizer64.exe", file, "/NOWINDOW"])


def process_files_batch(files):
    subprocess.run(["FileOptimizer64.exe"] + files + ["/NOWINDOW"])


def main():
    num_threads = int(input("Input number of threads to use (usually #cores * 2): "))
    # batch_size = int(input("Input number of files per process (to avoid overhead): "))
    batch_size = 1
    # Directory
    tkinter.Tk().withdraw()
    optimize_path = Path(tkinter.filedialog.askdirectory())
    all_files = list(Path(optimize_path).rglob("*.*"))

    # Ignore Symlinks
    files = [file for file in all_files if not os.path.islink(file)]

    # Close early if no path selected
    if optimize_path == Path("."):
        print("Error: No Path Input")
        return

    # Stats
    size_before = sum(f.stat().st_size for f in optimize_path.rglob('*.*') if f.is_file())

    cont = 'Y'
    if size_before / 1000000 < 5:
        cont = input("Size is small " + str(size_before) + " continue? (Y/N): ")
    else:
        print(f'Size is {size_before / 1000000:.2f}MB')

    if cont == 'n' or cont == 'N':
        return

    cont = 'N'
    cont = input(str(len(files)) + " files to process, continue? (Y/N): ")

    if cont == 'n' or cont == 'N':
        return

    num_files_skip = 0
    num_files_skip = int(input("How many of the first files would you like to skip? (Default 0): "))
    del files[:num_files_skip]


    print("Path (Recursive): ", optimize_path)
    print(f'Size reduced from {size_before / 1000000:.2f}MB')

    print(files)
    # Multithreading
    if batch_size == 1:
        with Pool(num_threads) as pool:
            try:
                for _ in tqdm.tqdm(pool.imap_unordered(process_file, files), total=len(files)):
                    pass
            finally:
                pool.terminate()
    else:  # Batch size greater than 1
        files_divided = sublist_creator(files, batch_size)
        with Pool(num_threads) as pool:
            try:
                for _ in tqdm.tqdm(pool.imap_unordered(process_files_batch, files_divided), total=len(files_divided)):
                    pass
            finally:
                pool.terminate()


    # Final stats
    size_after = sum(f.stat().st_size for f in optimize_path.rglob('*.*') if f.is_file())
    print(f'to {size_after / 1000000:.2f}MB,'
          f'a {(1 - size_after / size_before) * 100:.2f}% reduction.')


if __name__ == "__main__":
    main()
