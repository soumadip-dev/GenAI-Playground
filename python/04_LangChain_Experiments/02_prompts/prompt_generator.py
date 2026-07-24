from langchain_core.prompts import PromptTemplate
from langchain_core.load import dumpd
import json

# New way: Automatically infers input_variables and runs validate_template=True by default
template = PromptTemplate.from_template(
    """Please summarize the research paper titled "{paper_input}" with the following specifications:
Explanation Style: {style_input}  
Explanation Length: {length_input}  
1. Mathematical Details:  
   - Include relevant mathematical equations if present in the paper.  
   - Explain the mathematical concepts using simple, intuitive code snippets where applicable.  
2. Analogies:  
   - Use relatable analogies to simplify complex ideas.  
If certain information is not available in the paper, respond with: "Insufficient information available" instead of guessing.  
Ensure the summary is clear, accurate, and aligned with the provided style and length.""",
    validate_template=True,
)


# dumpd automatically extracts all settings, parameters, and paths
template_dict = dumpd(template)

# Write it out cleanly using Python's native json module
with open("template.json", "w", encoding="utf-8") as f:
    json.dump(template_dict, f, indent=2)
