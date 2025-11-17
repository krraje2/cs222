import pathlib

# https://stackoverflow.com/questions/65388213/why-is-pathlib-path-file-parent-parent-sensitive-to-my-working-directory
DOWNLOAD_PATH = pathlib.Path(__file__).parent.joinpath("network/downloads").resolve()
CACHE_PATH = pathlib.Path(__file__).parent.joinpath("network/cache").resolve()
TEST_FILE_PATH = pathlib.Path(__file__).parent.joinpath("test_files").resolve()


print(DOWNLOAD_PATH)
