import os

from config import AWS_REGION_NAME
from config import AWS_ACCESS_KEY
from config import AWS_SECRET_ACCESS_KEY
from config import ANTHROPIC_API_KEY

from llm import Llm, stream_claude_response, stream_openai_response, stream_claude_response_aws_bedrock
from prompts import assemble_prompt
from prompts.types import Stack


async def generate_code_core(image_url: str, stack: Stack, model: Llm) -> str:
    prompt_messages = assemble_prompt(image_url, stack)
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    anthropic_api_key = ANTHROPIC_API_KEY
    aws_access_key = AWS_ACCESS_KEY
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY
    aws_region_name = AWS_REGION_NAME,
    openai_base_url = None

    async def process_chunk(content: str):
        pass

    if model == Llm.CLAUDE_3_SONNET:
        if not anthropic_api_key and not aws_access_key and not aws_secret_access_key:
            raise Exception("Anthropic API key or AWS Access Key not found")

        if anthropic_api_key:
            completion = await stream_claude_response(
                prompt_messages,
                api_key=anthropic_api_key,
                callback=lambda x: process_chunk(x),
            )
        else:
            completion = await stream_claude_response_aws_bedrock(
                prompt_messages,
                access_key=aws_access_key,
                secret_access_key=aws_secret_access_key,
                aws_region_name=aws_region_name,
                callback=lambda x: process_chunk(x),
            )
    else:
        if not openai_api_key:
            raise Exception("OpenAI API key not found")

        completion = await stream_openai_response(
            prompt_messages,
            api_key=openai_api_key,
            base_url=openai_base_url,
            callback=lambda x: process_chunk(x),
            model=model,
        )

    return completion
