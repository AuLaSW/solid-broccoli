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
- 
"""
import llm


def main(*emails):
    smart = generate_smart_requirements(*emails)


def generate_smart_requirements(*emails: str):
    # pass in email-chain to generate requirements
    email_chain = "\n---\n".join(emails)

    # SMART requirements? How do we generate that?
    # S - 
    # M - aintainable
    # A - ttainable
    # R - elevant
    # T - echnical
    # 
    # Generate an expert for each factor? Generate list of requirements from
    # the email chain, then determine if they are SMART. Alright.

    # Architecture
    # 1. Generate Expert (expert at converting plain-text to requirements list)
    # 2. Extract Requirements
    #   a. Implicit (implied requirements)
    #   b. Explicit (explicit requirements)
    # 3. Combine explicit and implicit requirements into Full Requirements
    # 4. Take Full Requirements and generate SMART requirements

    # ------
    # 1. Generate experts
    # ------
    extraction = LLM(llm=None, system="""Given a list of emails from project managers,
    techincal leads, and others deciding requirements for a contract to be sent
    out for bid for a company, determine both the explicit requirments read in
    the emails and the implicit requirements needed to understand the explicit
    requirements (requiremnts that may be implied by the users but not directly
    stated in the emails)""")

    combination = LLM(llm=None, system="""You will be provided with a list of
    requirements, both explicit and implicit. Please generate a full list of
    requirements that incorporate both the implicit and explicit requirements
    as a single list of requirements.""")

    # ------
    # 2. Extract Requirements
    # 3. Combine Explicit and Implicit requirements
    # ------
    extracted = extraction.invoke(email_chain)
    requirements = combination.invoke(extraction.invoke(email_chain))

    # ------
    # 4. Take Full Requirements and generate SMART Requirements
    # ------
    smart = SmartLLM(llm=None)
    smart_req = smart.get_smart_requirements(requirements)

    return smart_req


class LLM:
    def __init__(self, llm: None, system: str):
        self.definition = system
        if llm is None:
            raise Exception("LLM must not be None")
        self.llm = llm

    def invoke(self, prompt: str):
        ouptut = llm.invoke(system=self.system, prompt=prompt)
        return output


class SmartLLM:
    def __init__(self, llm: None):
        self.llm = llm


    def get_smart_requirements(prompt: str):
        pass


if __name__ == "__main__":
    import json
    with open("data/emails.json", 'r') as fp:
        emails = json.load(fp)
    main(*emails)
