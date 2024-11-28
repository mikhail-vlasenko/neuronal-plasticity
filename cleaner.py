import re


def clean_markdown(input_file, output_file):
    """
    Clean markdown file by removing unwanted sections.
    """
    # Read the entire file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split content into sections (separated by ---)
    sections = content.split('\n---\n')

    def should_keep_section(section):
        # Find the source URL line
        source_match = re.search(r'Source: (.*?)\n', section)
        if not source_match:
            return True

        source_url = source_match.group(1)

        # Check if the source URL is a download or .npy file
        if ('_downloads/' in source_url or
                source_url.endswith('.npy') or
                source_url.endswith('.npz') or
                source_url.endswith('.zip') or
                source_url.endswith('.tar') or
                source_url.endswith('.gz') or
                "https://brian2.readthedocs.io/en/stable/examples/frompapers." in source_url or
                "brian1_to_2" in source_url or
                "https://brian2.readthedocs.io/en/stable/developer/guidelines/" in source_url
        ):
            print(f"Removing section with URL: {source_url}")
            return False

        # Skip sections that are just "Untitled"
        if section.strip().startswith('# Untitled\n\nSource:'):
            return False

        # Skip empty or whitespace-only sections
        if not section.strip():
            return False

        return True

    # Filter sections
    cleaned_sections = [section for section in sections if should_keep_section(section)]

    # Rebuild the content
    cleaned_content = '\n---\n'.join(cleaned_sections)

    # Fix any duplicate newlines
    cleaned_content = re.sub(r'\n{3,}', '\n\n', cleaned_content)

    # Remove 
    cleaned_content = re.sub(r'', '', cleaned_content)

    # Save the cleaned content
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)

    # Print statistics
    original_sections = len(sections)
    final_sections = len(cleaned_sections)
    removed = original_sections - final_sections
    print(f"\nSummary:")
    print(f"Original sections: {original_sections}")
    print(f"Sections removed: {removed}")
    print(f"Final sections: {final_sections}")


if __name__ == "__main__":
    input_file = "brian2_documentation_for_claude.md"
    output_file = "brian2_documentation_for_claude.md"
    clean_markdown(input_file, output_file)
