import re


def parse_makefile_to_sym(lines, directory, kernel_file, base=None):
    """
    Parses makefile lines to extract symbols and their corresponding
    configurations.

    This function iterates over a sequence of lines from a makefile, extracting
    information based on the presence of a base symbol.  It categorizes each
    line into modes based on the symbol's prefix and collects extensions and
    configurations for each mode.  The function allows for dynamic determination
    of the base symbol if not provided.

    Parameters
    ----------
    **lines** : iterable of str

        An iterable sequence of lines (strings) from a makefile to be processed.
    **directory** : str

        The directory associated with the symbols being parsed.
    **kernel_file** : str

        The kernel file associated with the symbols.
    **base** : str, optional

        The base symbol to look for in the lines. If not provided, the base is
        determined dynamically from the lines.

    Returns
    -------
    **dict**

        A dictionary representing the parsed symbol configurations. It includes
        the base symbol, modes, their directories, kernel files, and extensions.
        The structure is:
    ```
        {
            "base": "<base_symbol>",
            "modes": {
                "<mode>": {
                    "dir": "<directory>",
                    "kernel": "<kernel_file>",
                    "exts": ["<extension1>", "<extension2>", ...]
                },
                ...
            }
        }
    ```

    Examples
    --------
    ```
    >>> lines = [
    ... "$(KDIR)symv_U$(TSUFFIX).$(SUFFIX)  : $(KERNELDIR)/symv_U_kernel $(SOME_DEPENDENCY)",
    ... "$(KDIR)symv_L$(TSUFFIX).$(SUFFIX)  : $(KERNELDIR)/symv_L_kernel $(SOME_DEPENDENCY)"
    ... ]
    >>> directory = "generic"
    >>> kernel_file = "symv_k.c"
    >>> parse_makefile_to_sym(lines, directory, kernel_file, base="symv")
    {
        "base": "symv",
        "modes": {
            "s": {
                "dir": "generic",
                "kernel": "symv_k.c",
                "exts": ["_U", "_L"]
            }
        }
    }
    ```
    """
    result = {"base": base, "modes": {}}

    for line in lines:
        if base:
            # Use the provided base to form the pattern.
            pattern = (
                r"\$\(KDIR\)(?P<mode>[a-z])"
                + re.escape(base)
                + r"(?P<extension>[^\$]+)"
            )
        else:
            # When no base is provided, capture the base and extension separately.
            pattern = (
                r"\$\(KDIR\)(?P<mode>[a-z])(?P<base>\w+)_((?P<extension>[A-Za-z]+))"
            )

        matches = re.finditer(pattern, line)
        for match in matches:
            mode = match.group("mode")

            if not base:
                # Dynamically determine the base for each line/match.
                dynamic_base = match.group("base")
                result["base"] = dynamic_base  # Update the base globally if not set.
                extension = f"_{match.group('extension')}"
            else:
                # Process the extension when the base is provided.
                extension = match.group("extension").strip().split(")")[0]

            if mode not in result["modes"]:
                result["modes"][mode] = {
                    "dir": directory,
                    "kernel": kernel_file,
                    "exts": [extension],
                }
            else:
                if extension not in result["modes"][mode]["exts"]:
                    result["modes"][mode]["exts"].append(extension)

    return result


def parse_compilation_commands(commands, base):
    """
    Parse compilation commands to extract configuration details.

    This function iterates over a list of compilation commands, extracting key
    configuration details such as mode, base, extensions, defined macros
    (`def`), undefined macros (`undef`), and additional flags (`addl`). The
    function utilizes regular expressions to parse each command according to a
    specified pattern, which is dynamically constructed using the provided
    `base`.

    Parameters
    ----------
    **commands** : list of str

        A list of compilation command strings to be parsed.
    **base** : str

        The base identifier used to construct the regular expression pattern for
        parsing the commands. It is used to identify the relevant part of each
        command.

    Returns
    -------
    **list of dict**

        A list of dictionaries, each representing the parsed configuration from
        a command.  Each dictionary contains the following keys:
        - 'name': A string combining the mode, base, and extension identifier.
        - 'undef': A list of strings representing macros that are undefined in
          the command.
        - 'def': A list of strings representing macros that are defined in the
          command.
        - 'addl': A list of additional flags extracted from the command.

    Examples
    --------
    Suppose `commands` is a list of strings, each representing a command in the
    makefile, and `base` is a string like 'symv'. The function will parse these
    commands to extract the configuration details based on the specified `base`.

    ```
    >>> commands = [
    ... "$(KDIR)symv_U$(TSUFFIX).$(SUFFIX) : $(KERNELDIR)/symv_U_kernel -DUSE_UPPER -UDOUBLE",
    ... "$(KDIR)symv_L$(TSUFFIX).$(SUFFIX) : $(KERNELDIR)/symv_L_kernel -DUSE_LOWER -UDOUBLE"
    ... ]
    >>> base = "symv"
    >>> configs = parse_compilation_commands(commands, base)
    >>> print(configs)
    [{'name': 'symv_U', 'undef': ['DOUBLE'], 'def': ['USE_UPPER'], 'addl': []},
     {'name': 'symv_L', 'undef': ['DOUBLE'], 'def': ['USE_LOWER'], 'addl': []}]
    ```

    This illustrates how each command is broken down into its components, aiding
    in the configuration and management of compilation settings in a more
    structured format.
    """
    pattern = r"\$\(KDIR\)(?P<mode>[a-z]{1,2})"  + re.escape(base) + r"(?P<extension>[^\$]+)"
    configs = []

    for command in commands:
        match = re.search(pattern, command)
        if not match:
            continue

        mode = match.group("mode")
        extension = match.group("extension").strip().split()[0]

        # Extract defines and undefines
        defs = re.findall(r"-D(\S+)", command)
        undefs = re.findall(r"-U(\S+)", command)

        # Attempt to capture additional flags more inclusively
        addl_flags_pattern = r"\$\(CFLAGS\)(.*?)\$<"
        addl_flags_match = re.search(addl_flags_pattern, command, re.DOTALL)
        addl_flags = addl_flags_match.group(1).strip() if addl_flags_match else ""
        # Splitting captured flags into a list, filtering out empty strings
        addl_flags_list = [
            flag.strip()
            for flag in re.split(r"\s+", addl_flags)
            if flag.strip() and "-" not in flag
        ]

        kcfg = {
            "name": mode + base + extension,
            "undef": undefs,
            "def": defs,
            "addl": addl_flags_list,
        }

        configs.append(kcfg)

    return configs
