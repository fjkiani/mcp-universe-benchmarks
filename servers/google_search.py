"""Mock google-search MCP server — returns deterministic search results."""
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("google-search")

_MOCK_RESULTS = [
    {"title": "OpenAI announces GPT-5 with improved reasoning", "url": "https://example.com/openai-gpt5", "snippet": "OpenAI has released GPT-5, featuring enhanced chain-of-thought reasoning and multimodal capabilities."},
    {"title": "Google DeepMind Gemini 2.5 Pro technical report", "url": "https://example.com/gemini-25-pro", "snippet": "Gemini 2.5 Pro achieves state-of-the-art on MMLU, GSM8K, and HumanEval benchmarks."},
    {"title": "Meta releases Llama 3.3 70B open weights", "url": "https://example.com/llama-33-70b", "snippet": "Meta's Llama 3.3 70B matches GPT-4-class performance while being fully open-weight."},
    {"title": "Anthropic Claude Sonnet 4.5 announcement", "url": "https://example.com/claude-sonnet-45", "snippet": "Claude Sonnet 4.5 introduces extended thinking mode and improved tool use."},
    {"title": "NVIDIA NIM microservices for enterprise AI deployment", "url": "https://example.com/nvidia-nim", "snippet": "NVIDIA NIM provides optimized inference microservices for production AI workloads."},
    {"title": "Qwen3 Coder: Alibaba's open-source coding model", "url": "https://example.com/qwen3-coder", "snippet": "Qwen3 Coder supports 1M token context and achieves competitive coding benchmarks."},
    {"title": "MCP Protocol specification v1.0 released", "url": "https://example.com/mcp-spec", "snippet": "The Model Context Protocol defines a standard for LLM-tool communication via stdio/SSE transports."},
    {"title": "NSF CAREER Program solicitation 2025", "url": "https://example.com/nsf-career-2025", "snippet": "NSF CAREER awards support early-career faculty with $500K over 5 years. Deadline: July 2025."},
    {"title": "NIH R01 grant guidelines updated", "url": "https://example.com/nih-r01-2025", "snippet": "NIH R01 supports up to $500K direct costs per year. Modular budget threshold: $500K."},
    {"title": "DOE Early Career Research Program 2025", "url": "https://example.com/doe-ecrp-2025", "snippet": "DOE ECRP supports early-career researchers with $500K/year for 5 years. Must be untenured."},
]


@mcp.tool()
async def search(query: str, num_results: int = 10) -> str:
    """Search the web for information.

    Args:
        query: The search query string
        num_results: Maximum number of results to return (default 10)

    Returns:
        JSON array of search results with title, url, and snippet fields
    """
    results = _MOCK_RESULTS[:min(num_results, len(_MOCK_RESULTS))]
    return json.dumps({"results": results, "total_results": len(results), "query": query}, indent=2)


@mcp.tool()
async def search_news(query: str, num_results: int = 5) -> str:
    """Search for recent news articles.

    Args:
        query: The news search query
        num_results: Maximum results to return

    Returns:
        JSON array of news articles
    """
    results = _MOCK_RESULTS[:min(num_results, len(_MOCK_RESULTS))]
    return json.dumps({"results": results, "query": query}, indent=2)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
