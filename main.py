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
import itertools
import os

MODEL = os.getenv("SMART_MODEL")
LLM_VAR = llm.Ollama(MODEL, thinking=True)


def main(*emails):
    smart = generate_smart_requirements(*emails)


def generate_smart_requirements(*emails: str):
    options = {
        "num_ctx": 40000,
    }
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
    as a single list of requirements.""",
        options=options
    )

    with open("out/extracted.json", 'w') as fp:
        json.dump(extracted.model_dump(), fp)

    combination = LLM_VAR.invoke(
        prompt=extracted.response,
        system="""You will be provided with a list of
    requirements, both explicit and implicit. Please generate a full list of
    requirements that incorporate both the implicit and explicit requirements
    as a single list of requirements.""",
        options=options,
    )

    with open("out/combination.json", 'w') as fp:
        json.dump(combination, fp)

    smart_requirements = LLM_VAR.invoke(
        prompt=combination.response,
        system=prompts.SMART_SYNTH,
        options=options,
    )

    with open("out/smart_requirements.json", 'w') as fp:
        json.dump(combination.model_dump(), fp)

    eval = LLM_VAR.invoke(
        prompt=smart_requirements.response,
        system=prompts.SMART_AUDIT,
        options=options,
    )

    with open("out/eval.json", 'w') as fp:
        json.dump(combination.model_dump(), fp)

    json_eval = LLM_VAR.invoke(
        prompt=eval.response,
        system="""You will be provided with a list of corrections for SMART
        requirmenets. They all have a specific format and need to be converted
        to JSON for easier processing by a machine. The conversion should follow
        the following example:

        ### Requirement Review

        R-003 - Status: NEEDS WORK
        S: PASS
        M: PASS
        A: PASS
        R: PASS
        T: PASS
        Flags: Vague Terms
        Fix: [fix-text]
        Acceptance Criteria:
          - Given multiple users editing a task simultaneously
          - When one user saves an update
          - Then all users see an updated task within <=1 sec

        ### Output

        {
            "id": 3,
            "Status": "NEEDS WORK",
            "S": "PASS",
            "M": "PASS",
            "A": "PASS",
            "R": "PASS",
            "T": "PASS",
            "Flags": [
                "Vague Terms"
            ],
            "Fix": "[fix-text]",
            "Acceptance Criteria": [
                "Given multiple users editing a task simultaneously",
                "When one user saves an update",
                "Then all users see an updated task within <=1 sec",
            ]
        }

        Only return the json and nothing else.
        If there are multiple requirements, return a list of json objects.
        """,
        options=options,
    )

    with open("out/eval.json", 'w') as fp:
        json.dump(json_eval.model_dump(), fp)


if __name__ == "__main__":
    import json
    with open("data/emails.json", 'r') as fp:
        emails = json.load(fp)
    main(*list(itertools.chain(*emails)))
