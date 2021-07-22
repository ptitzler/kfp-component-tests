import kfp


def count(input_file: kfp.components.InputPath(str)) -> int:
    """
    Split a row-based text file into two files, alternating
    between rows.
    """

    count = 0
    with open(input_file, 'r') as file_input:
        for line in file_input:
            count += 1
    return count
