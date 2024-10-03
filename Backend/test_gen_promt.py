import json

from gpt_prompt import (
    generate_metadata,
    generate_script_prompt,
    get_search_terms_prompt,
)


def prompt_generation(topic, language, paragraph_number, style, target_audience):
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
    # Test generate_script_prompt
    script_prompt = generate_script_prompt(topic, paragraph_number, language, "")
    print("Script Prompt:")
    print(script_prompt)
    print("\n" + "-"*50 + "\n")


if __name__ == "__main__":
    # Example usage
    prompt_generation(
        topic="Giới thiệu về phương pháp price action",
        language="Tiếng Việt",
        paragraph_number=5,
        style="Đầu tư",
        target_audience="Người đầu tư, trader chủ yếu về vàng, forex, crypto"
    )
