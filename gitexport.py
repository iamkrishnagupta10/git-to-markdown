import os
import subprocess
import tempfile
import streamlit as st
from pathlib import Path

def clone_repository(github_url, clone_path):
    subprocess.run(['git', 'clone', github_url, clone_path])

def export_to_text_file(clone_path, output_file):
    exclude_extensions = ('.png', '.jpg', '.gif', '.ico', '.exe', '.dll', '.woff', '.woff2', '.ttf', '.eot', '.otf', '.svg', '.mp3', '.mp4', '.avi', '.pdf', '.zip', '.yaml', '.lock')
    exclude_filenames = ('pnpm-lock.yaml', 'yarn.lock', 'package-lock.json')

    with open(output_file, 'w', encoding='utf-8') as file:
        for root, _, files in os.walk(clone_path):
            for filename in files:
                if '.git' in root or filename.endswith(exclude_extensions) or filename in exclude_filenames:
                    continue
                file_path = Path(root) / filename
                file.write(f"## {filename}\n\n")
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as content_file:
                    file_content = content_file.read().strip()
                    file.write(f"```plaintext\n{file_content}\n```\n\n")

def main():
    st.title("Git to Markdown")
    st.subheader("By Empire Code Foundation")
    st.image("https://github.githubassets.com/images/modules/logos_page/Octocat.png", width=50)
    st.write("Enter the public GitHub repository URL and choose a destination folder to export the code to a Markdown file.")

    github_url = st.text_input("GitHub Repository URL:")
    destination_folder = st.text_input("Destination Folder Path:")

    if st.button("Export"):
        if not github_url or not destination_folder:
            st.error("Please enter both the GitHub URL and destination folder.")
            return

        clone_path = os.path.join(tempfile.gettempdir(), "git_to_markdown_clone")
        output_file = Path(destination_folder) / "github_export.md"

        Path(destination_folder).mkdir(parents=True, exist_ok=True)

        st.write(f"Cloning repository from {github_url}... :floppy_disk:")
        clone_repository(github_url, clone_path)

        st.write(f"Exporting code to {output_file}... :pencil:")
        export_to_text_file(clone_path, output_file)

        st.write(f"Export complete.")
        with open(output_file, 'r', encoding='utf-8') as file:
            markdown_content = file.read()
            st.download_button("Download the Markdown file", markdown_content, file_name="github_export.md")

    st.write("---")
    st.write("Author: [Krishna Krishna](https://www.linkedin.com/in/llt-misty/) | [LinkedIn](https://www.linkedin.com/in/llt-misty/) :link:")
    st.write("© 2023 Empire Code Foundation. All rights reserved.")

if __name__ == "__main__":
    main()
