import os

TEXT = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n"
BYTES = len(TEXT)


def mb(length: int) -> int: return length * 1000000


def file_name(size: int) -> str: return f"{size}mb.txt"


def create_file(size: int) -> None:
    filename = file_name(size)

    print(f'Creating {size}MB file as "{filename}"...')

    with open(filename, 'w') as f:
        file_size = 0
        target = mb(size)

        while file_size < target:
            f.write(TEXT)
            file_size += BYTES

            print(f'\r{file_size}/{target}', end='')

    print(f' Done {size}MB file')


def create_files(sizes: list[int]) -> None:
    """
    Create random text files with given size
    :param sizes: list of file sizes in megabytes
    """
    files = [(file_name(i), i) for i in sizes]
    generate = []

    for (f, size) in files:
        if f in os.listdir():
            print(
                f"A file with name used in generation already exists in execution folder ('{f}'), delete it and create new one? [y/n]")

            if str(input()) in ('y', 'Y'):
                os.remove(f"./{f}")
                generate.append(size)

    for i in generate:
        create_file(i)


if __name__ == '__main__':
    create_files([1, 200, 500])
