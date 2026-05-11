from input_module import (
    read_cfg,
    validate_cfg,
    print_cfg,
    read_input_string
)

from parser_engine import ParserEngine 

cfg_obj = read_cfg()

print("\nValidating CFG...\n")

if validate_cfg(cfg_obj):

    print("CFG is VALID")

    print_cfg(cfg_obj)

    input_string = read_input_string()

    print("\nInput String:", input_string)

    parser = ParserEngine(cfg_obj)

    result = parser.parse_string(input_string)

else:
    print("CFG is INVALID")