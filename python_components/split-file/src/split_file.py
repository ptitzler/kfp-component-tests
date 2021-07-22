import kfp


def split(input_file: kfp.components.InputPath(str),
          output_file_1: kfp.components.OutputPath(str),
          output_file_2: kfp.components.OutputPath(str)
          ):
    """
    Split a row-based text file into two files, alternating
    between rows.
    """

    with open(input_file, 'r') as file_input:
        with open(output_file_1, 'w') as file_1_output:
            with open(output_file_2, 'w') as file_2_output:
                odd = True
                for line in file_input:
                    if odd:
                        file_1_output.write(line)
                    else:
                        file_2_output.write(line)
                    odd = not odd
