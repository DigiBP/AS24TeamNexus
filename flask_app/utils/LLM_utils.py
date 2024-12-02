from haystack import Pipeline
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.components.generators import HuggingFaceGenerator
from haystack.utils import Secret
from typing import Optional

from haystack.nodes import TransformersReader
from config import MODEL_NAME

def update_report_with_llm(input_text):
    reader = TransformersReader(model=MODEL_NAME, use_gpu= True)
    