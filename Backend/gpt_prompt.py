from typing import List, Tuple


def generate_script_prompt(video_subject: str, paragraph_number: int, voice: str, customPrompt: str) -> str:
    """
    Generate a script for a video, depending on the subject of the video, the number of paragraphs, and the AI model.



    Args:

        video_subject (str): The subject of the video.

        paragraph_number (int): The number of paragraphs to generate.



    Returns:

        str: The script for the video.

    """

    # Build prompt

    if customPrompt:
        prompt = customPrompt
    else:
        prompt = """
            Tạo kịch bản cho một video YouTube shorts hoặc tiktok shorts dựa trên chủ đề của video.

            Kịch bản cần được trả về dưới dạng một chuỗi với số đoạn văn được chỉ định.

            Đây là một ví dụ về chuỗi:
            "Đây là một chuỗi ví dụ."

            Không được đề cập đến yêu cầu này trong phản hồi của bạn dưới bất kỳ trường hợp nào.

            Đi thẳng vào vấn đề, đừng bắt đầu bằng những thứ không cần thiết như "chào mừng đến với video này".

            Rõ ràng, kịch bản phải liên quan đến chủ đề của video.

            BẠN KHÔNG ĐƯỢC SỬ DỤNG BẤT KỲ LOẠI MARKDOWN HOẶC ĐỊNH DẠNG NÀO TRONG KỊCH BẢN, KHÔNG BAO GIỜ SỬ DỤNG TIÊU ĐỀ.
            BẠN PHẢI VIẾT KỊCH BẢN BẰNG NGÔN NGỮ ĐƯỢC CHỈ ĐỊNH TRONG [LANGUAGE].
            CHỈ TRẢ VỀ NỘI DUNG THUẦN CỦA KỊCH BẢN. KHÔNG BAO GỒM "VOICEOVER", "NARRATOR" HOẶC CÁC CHỈ DẪN TƯƠNG TỰ VỀ NHỮNG GÌ NÊN ĐƯỢC NÓI Ở ĐẦU MỖI ĐOẠN VĂN HOẶC DÒNG. BẠN KHÔNG ĐƯỢC ĐỀ CẬP ĐẾN YÊU CẦU, HOẶC BẤT CỨ ĐIỀU GÌ VỀ KỊCH BẢN. NGOÀI RA, KHÔNG BAO GIỜ NÓI VỀ SỐ LƯỢNG ĐOẠN VĂN HOẶC DÒNG. CHỈ CẦN VIẾT KỊCH BẢN.
        """

    prompt += f"""
    
    Subject: {video_subject}
    Number of paragraphs: {paragraph_number}
    Language: {voice}

    """

    return prompt


def get_search_terms_prompt(video_subject: str, amount: int, script: str) -> List[str]:
    """
    Generate a JSON-Array of search terms for stock videos,
    depending on the subject of a video.

    Args:
        video_subject (str): The subject of the video.
        amount (int): The amount of search terms to generate.
        script (str): The script of the video.

    Returns:
        List[str]: The search terms for the video subject.
    """

    # Build prompt
    prompt = f"""
    Tạo {amount} từ khóa tìm kiếm cho video stock,
    dựa trên chủ đề của video.
    Chủ đề: {video_subject}

    Các từ khóa tìm kiếm cần được trả về dưới dạng
    một mảng JSON của các chuỗi.

    Mỗi từ khóa tìm kiếm nên bao gồm 1-3 từ,
    luôn thêm chủ đề chính của video.
    
    BẠN CHỈ ĐƯỢC TRẢ VỀ MẢNG JSON CỦA CÁC CHUỖI.
    BẠN KHÔNG ĐƯỢC TRẢ VỀ BẤT CỨ THỨ GÌ KHÁC. 
    BẠN KHÔNG ĐƯỢC TRẢ VỀ KỊCH BẢN.
    
    Các từ khóa tìm kiếm phải liên quan đến chủ đề của video.
    Đây là một ví dụ về mảng JSON của các chuỗi:
    ["từ khóa tìm kiếm 1", "từ khóa tìm kiếm 2", "từ khóa tìm kiếm 3"]

    Để có thêm ngữ cảnh, đây là toàn bộ nội dung:
    {script}
    """

    return prompt


def generate_metadata(video_subject: str, script: str) -> Tuple[str, str, List[str]]:
    """  
    Generate metadata for a YouTube video, including the title, description, and keywords.  

    Args:  
        video_subject (str): The subject of the video.  
        script (str): The script of the video.  
        ai_model (str): The AI model to use for generation.  

    Returns:  
        Tuple[str, str, List[str]]: The title, description, and keywords for the video.  
    """

    # Build prompt for title
    title_prompt = f"""  
    Tạo một tiêu đề hấp dẫn và thân thiện với SEO cho video YouTube shorts về {video_subject}.  
    """

    # Generate title
    # title = generate_response(title_prompt, ai_model).strip()

    # Build prompt for description
    description_prompt = f"""  
    Viết một mô tả ngắn gọn và hấp dẫn cho video YouTube shorts về {video_subject}.  
    Video dựa trên kịch bản sau:  
    {script}  
    """

    # Generate description
    # description = generate_response(description_prompt, ai_model).strip()

    # Generate keywords
    # keywords = get_search_terms(video_subject, 6, script, ai_model)

    return {
        "title_prompt": title_prompt,
        "description_prompt": description_prompt
    }
