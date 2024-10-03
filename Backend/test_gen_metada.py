import json
import os

from gpt_prompt import (
    generate_metadata,
    generate_script_prompt,
    get_search_terms_prompt,
)


def metadata_generation(topic, language, paragraph_number, style, target_audience):
    """
    Test the prompt generation functions.

    Args:
    topic (str): The main topic of the video
    language (str): The language for the script
    paragraph_number (int): The number of paragraphs to generate
    style (str): The style of the video (e.g., educational, entertaining)
    target_audience (str): The intended audience for the video

    Returns:
    None: Prints the results of each function
    """
    # Read dummy_script from file
    script_path = os.path.join('data', 'script.txt')
    with open(script_path, 'r', encoding='utf-8') as file:
        dummy_script = file.read()

    # Test get_search_terms_prompt
    search_terms_prompt = get_search_terms_prompt(topic, 5, dummy_script)
    print("Search Terms Prompt:")
    print(search_terms_prompt)
    print("\n" + "-"*50 + "\n")

    # Test generate_metadata
    metadata_prompts = generate_metadata(topic, dummy_script)
    print("Metadata Prompts:")
    print(metadata_prompts)


if __name__ == "__main__":
    # Example usage
    metadata_generation(
        topic="Giới thiệu về phương pháp price action",
        language="Tiếng Việt",
        paragraph_number=5,
        style="Đầu tư",
        target_audience="Người đầu tư, trader chủ yếu về vàng, forex, crypto"
    )
