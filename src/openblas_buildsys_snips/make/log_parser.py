from dataclasses import dataclass, field
from collections import namedtuple
from typing import List, Dict, Optional, NamedTuple
from textwrap import dedent
import re


class Define(NamedTuple):
    key: str
    value: Optional[str] = None


@dataclass
class CompilationInfo:
    defines: List[Define] = field(default_factory=list)
    undefines: List[str] = field(default_factory=list)
    flags: List[str] = field(default_factory=list)
    input_files: List[str] = field(default_factory=list)
    directory: str = ""
    output_symbol: str = ""


def parse_cc_makelog(log: str) -> List[CompilationInfo]:
    compilation_info_list = []
    current_directory = ""

    log_lines = dedent(log).splitlines()
    for line in log_lines:
        directory_enter_match = re.match(
            r"make\[\d+\]: Entering directory '([^']*)'", line
        )
        if directory_enter_match:
            current_directory = directory_enter_match.group(1)
        command_match = re.match(r"cc .*?-o \S+", line)
        if command_match:
            command = command_match.group(0)

            defines = []
            undefines = []
            flags = []
            input_files = []
            output_symbol = ""

            defines_matches = re.findall(r"-D(\S+?)(?:=(\S+?))?(?=\s|-)", command)
            for key, value in defines_matches:
                defines.append(Define(key, value if value else None))

            undefines_matches = re.findall(r"-U(\S+)", command)
            undefines.extend(undefines_matches)

            # Extract flags (e.g., -O2, -Wall)
            flags_matches = re.findall(r"(-\S+)", command)
            for flag in flags_matches:
                if flag.startswith(("-D", "-U", "-c", "-o")):
                    continue
                flags.append(flag)

            input_files_matches = re.findall(r"(\S+\.(?:c|h))", command)
            input_files.extend(input_files_matches)

            output_symbol_match = re.search(r"-o (\S+)", command)
            if output_symbol_match:
                output_symbol = output_symbol_match.group(1)

            compilation_info = CompilationInfo(
                defines=defines,
                undefines=undefines,
                flags=flags,
                input_files=input_files,
                directory=current_directory,
                output_symbol=output_symbol,
            )
            compilation_info_list.append(compilation_info)

    return compilation_info_list
