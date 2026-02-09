"""
backend/ai/summarizer.py
-------------------------

Summarizes news articles using Gemini via Langchain.

Responsibilities:
- Take cleaned article text.
- Send structured prompt to Gemini.
- Parse JSON output.
- Return structured summary object.
"""


#----------------------------------------------------------------------
# Imports
#----------------------------------------------------------------------
import json
from typing import Dict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

from backend.config import (
    GEMINI_MODEL,
    GEMINI_API_KEY,
    LLM_TEMPERATURE,
    SUMMARY_BULLETS_COUNT
)
from backend.ai.prompts import SUMMARY_PROMPT
from backend.utils.logger import get_logger

logger = get_logger(__name__)

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model = GEMINI_MODEL,
    api_key = GEMINI_API_KEY,
    temperature = LLM_TEMPERATURE
)

# Create Langchain PromptTemplate
summary_prompt = PromptTemplate(
    input_variables = ["text", "bullet_count"],
    template = SUMMARY_PROMPT
)


#-----------------------------------------------------------------
# Summarize Article
#-----------------------------------------------------------------
def summarize_article(article: str) -> Dict:
    """
    Summarize an Article using Gemini AI.
    Args: article (str): Cleaned article text to summarize.
    Returns: Dict: Structured summary object.
        Structured summary: 
        {
            "bullets": [...],
            "summary": "...",
            "category": "...",
            "importance_score": int
        }
    """

    try:
        text = text[:MAX_ARTICLES_TEXT_CHARS]
        prompt = summary_prompt.format(
            text = text,
            bullet_count = SUMMARY_BULLETS_COUNT
        )
        response = llm.invoke(prompt)
        content = response.content.strip()

        if content.startswith("```"):
            content = content.split("```")[1]
        
        parsed = json.loads(content)

        return parsed

    except Exception as e:
        logger.error(f"Failed to summarize article: {e}")
        return {
            "bullets": [],
            "summary": "Summary unavailable.",
            "category": "General",
            "importance_score": 3
        }

