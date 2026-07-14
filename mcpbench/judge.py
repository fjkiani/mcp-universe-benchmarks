"""LLM-as-judge module — provider-agnostic evaluation via LiteLLM.

Reuses the prompt template pattern from domains/web_search/evaluators/functions.py
but routes through LiteLLM so any provider can be used as the judge.
"""
import os
import re
from typing import Optional

from dotenv import load_dotenv

from mcpbench.llm import call_llm_simple

load_dotenv()


def get_judge_prompt(question: str, response: str, correct_answer: str) -> str:
    """Build a judge prompt — same pattern as web_search evaluator."""
    return f"""
Judge whether the following [response] to [question] is correct or not based on the precise and unambiguous [correct_answer] below.

[question]: {question}

[response]: {response}

Your judgement must be in the format and criteria specified below:

extracted_final_answer: The final exact answer extracted from the [response]. Put the extracted answer as 'None' if there is no exact, final answer to extract from the response.

[correct_answer]: {correct_answer}

reasoning: Explain why the extracted_final_answer is correct or incorrect based on [correct_answer], focusing only on if there are meaningful differences between [correct_answer] and the extracted_final_answer.

correct: Answer 'yes' if extracted_final_answer matches the [correct_answer] given above, or is within a small margin of error for numerical problems. Answer 'no' otherwise.
"""


async def llm_as_judge(
    question: str,
    agent_response: str,
    correct_answer: str,
    judge_model: Optional[str] = None,
) -> tuple[bool, str]:
    """Use an LLM to judge whether an agent response is correct.

    Args:
        question: The original question asked
        agent_response: The agent's response to evaluate
        correct_answer: The ground truth answer
        judge_model: Model slug (defaults to env MCPBENCH_JUDGE_MODEL or free OpenRouter model)

    Returns:
        (passed: bool, reasoning: str)
    """
    if judge_model is None:
        judge_model = os.environ.get(
            "MCPBENCH_JUDGE_MODEL",
            "openrouter/openai/gpt-oss-20b:free",
        )

    prompt = get_judge_prompt(question, agent_response, correct_answer)

    max_tries = 3
    for attempt in range(max_tries):
        try:
            response_text = await call_llm_simple(
                judge_model, prompt,
                system="You are a helpful assistant acting as an answer judge.",
                temperature=0.0,
                max_tokens=1024,
            )

            if response_text is None:
                return False, "Judge returned no response"

            match = re.search(r"correct:\s*(yes|no)", response_text, re.IGNORECASE)
            if match:
                is_correct = match.group(1).lower() == "yes"
                reasoning_match = re.search(
                    r"reasoning:\s*(.+?)(?:\n\s*correct:|$)", response_text, re.DOTALL
                )
                reasoning = reasoning_match.group(1).strip() if reasoning_match else response_text
                return is_correct, reasoning
            continue

        except Exception as e:
            if attempt == max_tries - 1:
                return False, f"Judge error after {max_tries} attempts: {e}"
            continue

    return False, "Judge response could not be parsed after multiple attempts"
