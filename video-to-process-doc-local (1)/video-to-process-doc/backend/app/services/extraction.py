import os
from typing import Dict
from openai import AzureOpenAI
import json

SYSTEM_PROMPT = (
    "You are a process analyst. Given a transcript of people explaining a workflow, "
    "produce a clear, end-to-end business process specification. Use simple language. "
    "Output STRICT JSON matching the schema with: title, summary, purpose, scope, roles, tools, steps[], decisions[], notes[]. "
    "For steps: number (int), action (short imperative), details (1-2 sentences), role, tools[]. "
    "For decisions: condition, path_yes, path_no.
"
)


def build_client() -> AzureOpenAI:
    return AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    )


def extract_process(transcript: str, title: str | None, tone: str = "simple") -> Dict:
    client = build_client()
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")

    user_prompt = f"Tone: {tone}. If a title is missing, infer a concise one. Transcript:

{transcript}"

    resp = client.chat.completions.create(
        model=deployment,
        temperature=0.2,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
    )

    content = resp.choices[0].message.content
    data = json.loads(content)

    if title:
        data["title"] = title

    return data
