import re

def parse_makefile_lines(lines, directory, kernel_file, base=None):
    result = {"base": base, "modes": {}}

    if base:
        # Pattern to capture everything after the base as the extension
        pattern = (
            r"\$\(KDIR\)(?P<mode>[a-z])" + re.escape(base) + r"(?P<extension>[^\$]+)"
        )
    else:
        # Pattern for dynamically determining the base and capturing the extension
        pattern = r"\$\(KDIR\)(?P<mode>[a-z])(?P<base>\w+)(?P<extension>[^\$]+)"

    for line in lines:
        matches = re.finditer(pattern, line)
        for match in matches:
            mode = match.group("mode")
            if not base:
                # Update the base dynamically if not provided
                base = match.group("base")
                result["base"] = base
            # Adjust the extension, removing the initial underscore from the split operation
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
