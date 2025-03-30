import urllib.request
import time
import sys

# Kernel download URL (change if a newer version is needed)
url = "https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.6.10.tar.xz"
file_name = "linux-6.6.10.tar.xz"

def download_with_progress(url, file_name):
    with urllib.request.urlopen(url) as response:
        total_size = int(response.info().get("Content-Length").strip())
        block_size = 1024 * 8  # 8 KB chunks
        downloaded = 0
        start_time = time.time()

        with open(file_name, "wb") as file:
            while True:
                buffer = response.read(block_size)
                if not buffer:
                    break
                file.write(buffer)
                downloaded += len(buffer)

                # Calculate progress
                progress = downloaded / total_size
                elapsed_time = time.time() - start_time
                speed = downloaded / elapsed_time / (1024 * 1024)  # Speed in MB/s

                # Print progress bar
                bar_length = 40
                filled_length = int(bar_length * progress)
                bar = "=" * filled_length + "-" * (bar_length - filled_length)
                sys.stdout.write(f"\r[{bar}] {progress * 100:.2f}% ({speed:.2f} MB/s)")
                sys.stdout.flush()

    print("\nDownload complete.")

# Run the download
download_with_progress(url, file_name)
