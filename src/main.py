import shutil

from src.functions import copy_dir_to_dir, generate_website

def main():
    copy_dir_to_dir("static", "public")
    generate_website("content", "template.html", "public")

if __name__ == "__main__":
    main()
