import sys

from src.functions import copy_dir_to_dir, generate_website

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_dir_to_dir("static", "docs")
    generate_website("content", "template.html", "docs", basepath)

if __name__ == "__main__":
    main()
