from crewai import Agent

def get_citation_integrator() -> Agent:
    return Agent(
        role="OSCOLA & Bluebook Legal Citation Verification Specialist",
        goal="Convert messy citations into precise OSCOLA/Bluebook footnote entries.",
        backstory=(
            "You are a legal citation accuracy expert. You ensure every statute, report (PLD, SCMR, YLR), "
            "and journal entry complies strictly with OSCOLA and Bluebook rules."
        ),
        verbose=True
    )
