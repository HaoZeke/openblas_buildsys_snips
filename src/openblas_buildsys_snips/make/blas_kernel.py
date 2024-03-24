import re


def parse_makefile_lines(lines, directory, kernel_file, base=None):
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
