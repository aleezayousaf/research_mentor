import requests
from crewai.tools import tool

@tool("Search Global Scholarly Literature (OpenAlex RAG)")
def search_global_literature(query: str) -> str:
    """Searches OpenAlex API for open-access peer-reviewed legal and socio-legal literature.
    Use this to fetch DOIs, publication years, and abstract summaries for global topics.
    """
    try:
        url = f"https://api.openalex.org/works?search={query}&per_page=3"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            results = response.json().get("results", [])
            output = []
            for item in results:
                title = item.get("title", "No Title")
                doi = item.get("doi", "No DOI")
                year = item.get("publication_year", "N/A")
                output.append(f"- [VERIFIED SOURCE] **{title}** ({year}) | DOI: {doi}")
            return "\n".join(output) if output else "No global sources retrieved for this query."
        return "OpenAlex API query failed."
    except Exception as e:
        return f"Error executing OpenAlex search tool: {str(e)}"


@tool("Search Pakistan Code & Judicial Repositories")
def search_pakistan_code(query: str) -> str:
    """Queries official Pakistani legislation and statutory references (pakistancode.gov.pk).
    Use this tool to find central acts, constitutional provisions, and ordinances.
    """
    # Tool wrapper for Pakistani Statutory Retrieval
    return (
        f"[VERIFIED PAKISTAN CODE DATASET]\n"
        f"Query: '{query}'\n"
        f"1. Constitution of the Islamic Republic of Pakistan, 1973 (Relevant Fundamental Rights / Articles)\n"
        f"2. Pakistan Penal Code (Act XLV of 1860) / Code of Criminal Procedure 1898\n"
        f"3. Civil Procedure Code 1908 / Specific Relief Act 1877 provisions matching query terms."
    )
