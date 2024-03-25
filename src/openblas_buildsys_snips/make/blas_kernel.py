import re


def parse_makefile_to_sym(lines, directory, kernel_file, base=None):
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
    pattern = r"\$\(KDIR\)(?P<mode>[a-z])" + re.escape(base) + r"(?P<extension>[^\$]+)"
    configs = []

    for command in commands:
        match = re.search(pattern, command)
        if not match:
            continue

        mode = match.group("mode")
        extension = match.group("extension").strip().split()[0]

        # Extract defines and undefines
        defs = re.findall(r"-D([A-Z_]+)", command)
        undefs = re.findall(r"-U([A-Z_]+)", command)

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
