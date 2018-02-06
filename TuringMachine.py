from collections import namedtuple


class TuringMachine:
    # Constructor
    def __init__(self, file_one):
        self.input_filename = file_one
        self.tuple_hash = {}
        self.current_state = None

    # break down File1 input line by line into individual values/5-tuples
    def process_tuples(self):
        five_tuple = namedtuple("instruction", "start_state original_char replace_char next_state direction")
        two_key_hash = namedtuple("hash_prep", "start_state original_char")
        # read input file line by line
        in_file = open(self.input_filename)
        for line in in_file:
            line = line.rstrip('\n')
            line_list = line.split()
            # assign individual values per 5-tuple
            read_start_state = line_list[0]
            read_original_char = line_list[1]
            read_replace_char = line_list[2]
            read_next_state = line_list[3]
            read_direction = line_list[4]
            instruction = five_tuple(start_state=read_start_state, original_char=read_original_char,
                                     replace_char=read_replace_char,
                                     next_state=read_next_state, direction=read_direction)
            hash_key = two_key_hash(start_state=read_start_state, original_char=read_original_char)
            self.tuple_hash.update({hash_key: instruction})
            if self.current_state is None:
                self.current_state = read_start_state
        in_file.close()

    # Compute turing machine using given 5-tuples (File1.txt) & input (File2.txt)
    def compute(self, file_two):
        self.process_tuples()
        # Read File2 as turing tape input
        in_file = open(file_two)
        for line in in_file:
            line = line.rstrip('\n')
            turing_tape = list(line)
        in_file.close()
        # Begin computing solution
        scanner_position = 1
        while True:
            try:
                try:
                    two_key_hash = namedtuple("hash_prep", "start_state original_char")
                    curr_hash_key = two_key_hash(start_state=self.current_state,
                                                 original_char=turing_tape[scanner_position])
                    turing_tape[scanner_position] = self.tuple_hash[curr_hash_key].replace_char
                    self.current_state = self.tuple_hash[curr_hash_key].next_state
                    if self.tuple_hash[curr_hash_key].direction == "R":
                        scanner_position = scanner_position + 1
                    if self.tuple_hash[curr_hash_key].direction == "L":
                        scanner_position = scanner_position - 1
                except KeyError:
                    # print("No valid transition, crashing")
                    break
            except IndexError:
                # Scanner has reached given tape limit, 5000bytes
                print("End of tape (5000bytes)")
                break

        out_file = open(file_two, 'w')
        out_file.write("".join(turing_tape))
        out_file.close()


#################################################
# TuringMachine("File1.txt").compute("File2.txt")
#################################################
