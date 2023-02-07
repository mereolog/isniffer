from common.constants import DUMMY_CONSTANTS


def find_constant_indices_in_argument_sequence(argument_sequence: list) -> list:
    constant_indices_in_argument_sequence = list()
    for index in range(0, len(argument_sequence)):
        argument = argument_sequence[index]
        if argument in DUMMY_CONSTANTS:
            constant_indices_in_argument_sequence.append(str(index))
    
    return constant_indices_in_argument_sequence