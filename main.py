"""
main.py
---

F-47 Logistics ERP

Team 1
    - Generate SMART Requirements from email chain.
    - Create RFI (Request For Information) based on:
        - RFI allows industry to ask questions (ensure clear and capable of being completed)
        - Smart Requirements
        - Web Search
            - Can this be done?
            - What does it normally cost?
    - Generate a Market Research Report
        - Gate/check
    - RFP
        - DAU API (guidelines for RFP Generatation)
        - Technical & Functional Factors
            - What the bidders need to meet
        - Instructions to Bidders
            - What the bidders need to do

SMART Requirements:
- Specific
- Measurable
- Achievable
- Relevant
- Time-Bound
"""
import llm, prompts
import os

MODEL = os.getenv("SMART_MODEL")
LLM_VAR = llm.Ollama(MODEL, thinking=True)


def main(*emails):
    smart = generate_smart_requirements(*emails)


def generate_smart_requirements(*emails: str):
    # pass in email-chain to generate requirements
    email_chain = "\n---\n".join(emails)

    # Base Architecture
    # 1. Generate Expert (expert at converting plain-text to requirements list)
    # 2. Extract Requirements
    #   a. Implicit (implied requirements)
    #   b. Explicit (explicit requirements)
    # 3. Combine explicit and implicit requirements into Full Requirements
    # 4. Take Full Requirements and generate SMART requirements

    # ------
    # 1. Generate experts
    # ------

    # ------
    # 2. Extract Requirements
    # 3. Combine Explicit and Implicit requirements
    # ------
    extracted = LLM_VAR.invoke(
        prompt=email_chain,
        system="""You will be provided with a list of
    requirements, both explicit and implicit. Please generate a full list of
    requirements that incorporate both the implicit and explicit requirements
    as a single list of requirements."""
    )
    combination = LLM_VAR.invoke(
        prompt=extracted.response,
        system="""You will be provided with a list of
    requirements, both explicit and implicit. Please generate a full list of
    requirements that incorporate both the implicit and explicit requirements
    as a single list of requirements."""
    )

    # get the body of the requirements
    requirements = combination.response

    smart_requirements = LLM_VAR.invoke(
        prompt=combination.response,
        system=prompts.SMART_SYNTH,
    )

    print("===== SMART REQUIREMENTS GENERATED =====")
    print(smart_requirements.response)
    print()

    eval = LLM_VAR.invoke(
        prompt=smart_requirements.response,
        system=prompts.SMART_AUDIT,
    )

    print("===== SMART EVALS GENERATED =====")
    print(eval.response)
    print()


if __name__ == "__main__":
    import json
    with open("data/emails.json", 'r') as fp:
        emails = json.load(fp)
    main(*emails)
