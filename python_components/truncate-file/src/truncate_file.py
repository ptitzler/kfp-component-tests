import kfp


def truncate(file_in: kfp.components.InputPath(str),
             threshold: int,
             file_out: kfp.components.OutputPath(str)):

    if threshold < 0:
        threshold = 0

    with open(file_in, 'r') as input_file:
        with open(file_out, 'w') as output_file:
            count = 0
            for line in input_file:
                if count >= threshold:
                    break
                count = count + 1
                output_file.write(line)
