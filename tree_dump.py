import os
import argparse
import fnmatch

tree_output = ""


def read_file_contents(file_path):
    try:
        with open(file_path, "r") as file:
            return file.read()
    except Exception:
        return "<< Cannot show this file>>"


def write_file_beginning_contents(file_path, contents):
    with open(file_path, "r") as file:
        existing_content = file.read()

    with open(file_path, "w") as file:
        file.write(contents)

    with open(file_path, "a") as file:
        file.write(existing_content)


def list_files_and_folders(
    directory,
    mode,
    specified_patterns,
    global_excludes,
    output_file,
    indent="",
    relative_path="",
    is_root=False,
):
    global tree_output
    items = os.listdir(directory)
    items.sort()

    for idx, item in enumerate(items):
        item_relative_path = os.path.join(relative_path, item)
        item_path = os.path.join(directory, item)
        is_last = idx == len(items) - 1

        if any(fnmatch.fnmatch(item, pattern) for pattern in global_excludes):
            continue

        if mode == "exclude" and any(
            fnmatch.fnmatch(item_relative_path, pattern)
            for pattern in specified_patterns
        ):
            continue

        if mode == "include":
            matched = any(
                fnmatch.fnmatch(item_relative_path, pattern)
                for pattern in specified_patterns
            )
            partial_match = any(
                pattern.startswith(item_relative_path + "/")
                for pattern in specified_patterns
            )
            if not matched and not partial_match:
                continue

        prefix = "└── " if is_last else "├── "
        item_type = "(D)" if os.path.isdir(item_path) else "(F)"
        tree_output += indent + prefix + item + "\n"

        if item_type == "(F)":
            file_contents = read_file_contents(item_path)
            if output_file:
                with open(output_file, "a") as out:
                    out.write("```{0}\n{1}\n```\n".format(item_path, file_contents))

        if os.path.isdir(item_path) and (mode != "include" or matched or partial_match):
            new_indent = (
                (indent + "    " if is_last else indent + "│   ") if not is_root else ""
            )
            list_files_and_folders(
                item_path,
                mode,
                specified_patterns,
                global_excludes,
                output_file,
                new_indent,
                item_relative_path,
            )


def main():
    global tree_output
    parser = argparse.ArgumentParser(description="List files and folders as a tree")
    parser.add_argument("--dir", required=True, help="Directory path to list")
    parser.add_argument(
        "--mode",
        choices=["include", "exclude"],
        default="exclude",
        help="Mode to include or exclude specified files/folders",
    )
    parser.add_argument(
        "--items",
        nargs="*",
        help="List of files/folders to include or exclude (relative paths with wildcards supported in include mode)",
        default=[],
    )
    parser.add_argument(
        "--global-excludes",
        nargs="*",
        help="List of files/folders to globally exclude (patterns supported)",
        default=[],
    )
    parser.add_argument(
        "--output", help="Path to output file for contents of text files", default=None
    )
    args = parser.parse_args()

    target_directory = args.dir
    mode = args.mode
    specified_patterns = set(args.items)  # Convert to a set for faster lookups
    global_excludes = set(args.global_excludes)  # Set of globally excluded patterns
    output_file = args.output

    if output_file:
        # Clear contents of the output file if it exists
        open(output_file, "w").close()

    if not os.path.isdir(target_directory):
        print("Error: The specified directory does not exist.")
        return

    list_files_and_folders(
        target_directory, mode, specified_patterns, global_excludes, output_file
    )
    print(tree_output)

    if output_file:
        write_file_beginning_contents(
            output_file, "Tree:\n" + tree_output + "\nFiles:\n"
        )


if __name__ == "__main__":
    main()
