def cmake_netlib_meson(cmake_string):
    variable_name = cmake_string[0].split("(")[1].strip()
    meson_variable_name = "_" + variable_name.lower()
    file_names = []
    for line in cmake_string[1:]:
        line = line.strip()
        if line.endswith(")"):
            line = line[:-1].strip()  # Remove the closing parenthesis
        file_names.extend(line.split())
    meson_list = ",\n    ".join(f"'{file_name}'" for file_name in file_names)
    meson_output = f"{meson_variable_name} = [\n    {meson_list}\n]"

    return meson_output
