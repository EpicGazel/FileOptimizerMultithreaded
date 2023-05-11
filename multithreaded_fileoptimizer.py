import subprocess
from pathlib import Path
import tkinter
from tkinter import filedialog
from multiprocessing import Pool
import tqdm


def process_file(file):
    subprocess.run(["FileOptimizer64.exe", file, "/NOWINDOW"])


def main():
    num_threads = int(input("Input number of threads to use (usually #cores * 2): "))
    # Directory
    tkinter.Tk().withdraw()
    optimize_path = Path(tkinter.filedialog.askdirectory())
    files = list(Path(optimize_path).rglob("*.*"))

    # Close early if no path selected
    if optimize_path == Path("."):
        print("Error: No Path Input")
        return

    # Stats
    size_before = sum(f.stat().st_size for f in optimize_path.glob('*.*') if f.is_file())

    print("Path (Recursive): ", optimize_path)
    print(f'Size reduced from {size_before/1000000:.2f}MB')

    # Multithreading
    with Pool(num_threads) as pool:
        for _ in tqdm.tqdm(pool.imap_unordered(process_file, files), total=len(files)):
            pass

    # Final stats
    size_after = sum(f.stat().st_size for f in optimize_path.glob('*.*') if f.is_file())
    print(f'to {size_after/1000000:.2f}MB,'
          f'a {(1 - size_after/size_before)*100:.2f}% reduction.')


if __name__ == "__main__":
    main()
