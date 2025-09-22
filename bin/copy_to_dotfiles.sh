#!/usr/bin/env bash
exit_with_usage_info() {
    echo "Usage: $0 [-c] <file_or_directory_path> [additional_paths...]"
    echo "  -c: Copy to dotfiles/.config instead of dotfiles"
    exit 1
}

dotfiles_dir="$HOME/Documents/dotfiles"
target_dir="$dotfiles_dir" # unless -c is passed
if [ $# -eq 0 ]; then
    exit_with_usage_info
else
    case "$1" in
        -c)
            target_dir="$dotfiles_dir/.config"
            shift # remove "-c" arg
            ;;
    esac    
fi

# hopefully also something else supplied after the "-c" ...
if [ $# -eq 0 ]; then
    exit_with_usage_info
fi

for source_path in "$@"; do
    if [ ! -e "$source_path" ]; then
        echo "Error: '$source_path' does not exist"
        exit 1
    fi
    basename=$(basename "$source_path")

    dest_path="$target_dir/$basename"
    if [ -e "$dest_path" ]; then
        rm -rf "$dest_path"
        echo "Removed existing '$dest_path'"
    fi

    if [ -d "$source_path" ]; then
        cp -r "$source_path" "$target_dir/"
        echo "Copied directory '$source_path' recursively to '$dest_path'"
    else
        cp "$source_path" "$target_dir/"
        echo "Copied file '$source_path' to '$dest_path'"
    fi

    echo
done
