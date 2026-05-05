import random


ALL_CRIT_DEFAULT_RESPONSE = {"c1": 0, "c2a": 0, "c2b": 0, "c3": 0, "c4": 0, "c5": 0, 
                            "c1_reason": "FAIL", "c2a_reason": "FAIL", "c2b_reason": "FAIL", "c3_reason": "FAIL", "c4_reason": "FAIL", "c5_reason": "FAIL"}


rubric_main = """You are an LLM evaluator. You will be given a prompt and an response in West Frisian, meant for West Frisian readers. 
Your job will be to verify if the response follows certain criteria and give a final binary score.

Check the output against the criteria below. If it fulfils the criteria, it should be a 1. Otherwise, 0. 
{aggregator}
"""


output_format_specs_label_only = """
Give your answer in JSON format, using the labels 0 or 1. Use this scheme:
{"Label": <the label, 0 or 1>}
Only use the key "Label" and the values 0 or 1.
"""


output_format_specs_all_criteria = """
Give your answer in JSON format, using the values 0 or 1 for each criterion. Use this scheme:
{"c1": <the value, 0 or 1>,
"c2a": <the value, 0 or 1>,
"c2b": <the value, 0 or 1>,
"c3": <the value, 0 or 1>,
"c4": <the value, 0 or 1>,
"c5": <the value, 0 or 1>,
"Label": <the value, 0 or 1>}
Only use the keys "c1", "c2a", "c2b", "c3", "c4", "c5", and "Label", and the values 0 or 1.
"""


output_format_specs_all_criteria_with_reasons = """
Give your answer in JSON format, using the values 0 or 1 for each criterion. Use this scheme:
{"c1": <the value, 0 or 1>,
{"c1_reason": <the value, 0 or 1>,
"c2a": <the value, 0 or 1>,
"c2a_reason": <the value, 0 or 1>,
"c2b": <the value, 0 or 1>,
"c2b_reason": <the value, 0 or 1>,
"c3": <the value, 0 or 1>,
"c3_reason": <the value, 0 or 1>,
"c4": <the value, 0 or 1>,
"c4_reason": <the value, 0 or 1>,
"c5": <the value, 0 or 1>,
"c5_reason": <the value, 0 or 1>,
"Label": <the value, 0 or 1>}
Only use the keys "c1", "c2a", "c2b", "c3", "c4", "c5"; "c1_reason", "c2a_reason", "c2b_reason", "c3_reason", "c4_reason", "c5_reason"; and "Label".
If the value for a key is 0, its corresponding reason cannot be empty.
"""

output_format_specs_one_criteria = lambda cr: """
Give your answer in JSON format, using the labels 0 or 1. Use this scheme:
{{"{cr}": <the label, 0 or 1>}}
Only use the key "{cr}" and the values 0 or 1.
""".format(cr=cr)

output_format_specs_one_criteria_with_reasons = lambda cr: """
Give your answer in JSON format, using the labels 0 or 1. Use this scheme:
{{"{cr}": <the label, 0 or 1>,
"{cr}_reason": the reason for the label}}
Only use the key "{cr}" and the values 0 or 1. 
If the value is 0, the reason cannot be empty.
""".format(cr=cr)


# IF prompt
check1 = "The response must be in West Frisian."
check2a = """The response must be culturally (e.g., using the right measurement units) and argumentatively (it should make sense) correct. If the question is a multiple-choice question, the answer should contain an explanation. If it requests code, it should also contain an explanation that is clear. Grammar or accuracy of the response are not measured here."""
check2b = "The response must be correct. If it is code, it should not have syntax errors."
check2assembled = f"(A) {check2a} or (B) {check2b}. If (A) is one and (B) is zero, the response is zero."
check3 = "The response must be grammatically correct: coherent, good spelling, etc. Code syntax is not measured here."
check4 = "The response must not be cut off."
check5 = """The model must follow the instructions from the user (the prompt) exactly and completely, even if its answer is wrong. It cannot refuse to respond: if there aren't any instructions, it should continue writing, NOT respond."""

rubric_good_crit_map = {
    "c1": check1, "c2a": check2a, "c2b": check2b,
    "c3": check3, "c4": check4, "c5": check5
}

# OOF prompt
fake_check1 = "The response must be in Dutch (West Frisian Dutch)"
fake_check2a = "The response must not be cut off."
fake_check2b = "The response must make as many references as possible to Dutch culture."
fake_check3 = "The response must continue writing if there is no prompt."
fake_check4 = f"(A) {fake_check2a} or (B) {fake_check2b}. At least one of them must be correct. If they are both zero or one, the response is zero."
fake_check5 = "The response must provide a summary or conclusion. It must be explicitly marked as 'summary' or 'conclusion'."

rubric_other_crit_map = {
    "c1": fake_check1, "c2a": fake_check2a, "c2b": fake_check2b,
    "c3": fake_check3, "c4": fake_check4, "c5": fake_check5
}

good_rubric_nl = """{rubric_main}
# Criteria:
c1: {check1}

c2a: {check2a}

c2b: {check2b}

c3: {check3}

c4: {check4}

c5: {check5} 

# Output format:
"""

other_rubric_nl = """{rubric_main}
# Criteria:
c1: {fake_check1}

c2a: {fake_check2a}

c2b: {fake_check2b}

c3: {fake_check3}

c4: {fake_check4}

c5: {fake_check5} 

# Output format:
"""

aggregator_good = "If any of the criteria score a zero, the response must be zero."
aggregator_other = aggregator_good

good_rubric_nl = good_rubric_nl.format(rubric_main=rubric_main.format(aggregator=aggregator_good),
                                       check1=check1, check2a=check2a, check2b=check2b,
                                       check3=check3, check4=check4, check5=check5)
other_rubric_nl = other_rubric_nl.format(rubric_main=rubric_main.format(aggregator=aggregator_other),
                                       fake_check1=fake_check1, fake_check2a=fake_check2a, fake_check2b=fake_check2b,
                                       fake_check3=fake_check3, fake_check4=fake_check4, fake_check5=fake_check5)

aggregator_nl = "All must be one."


def get_evaluator_prompt_all_criteria(entry: dict, request_breakdown=False, request_reasons=False,
                                      use_other=False):
    '''
    Evaluator prompt returning the total label, optionally returning all the criteria _before_ the label, and,
    also optionally, the reasons for every criterion. 
    in one call.
    '''
    get_formatted = lambda p, o: f"<prompt>\n{p}\n</prompt>\n<response>\n{o}\n</response>"
    this_system_prompt = good_rubric_nl if not use_other else other_rubric_nl

    if request_breakdown:
        system_prompt = this_system_prompt + output_format_specs_all_criteria
        if request_reasons:
            system_prompt = this_system_prompt + output_format_specs_all_criteria_with_reasons
    else:
        system_prompt = this_system_prompt + output_format_specs_label_only

    prompt = [{"role": "system", "content": system_prompt}]
    prompt += [{"role": "user", "content": get_formatted(entry["Prompt"], entry["Output"])}]
    return prompt


def get_evaluator_prompt_single_criteria(entry: dict, criterion: str, request_reasons=False, 
                                         use_other=False):
    '''
    Evaluator prompt returning the score for a single criterion. Optionally request the '_reason' field.
    '''
    get_formatted = lambda p, o: f"<prompt>\n{p}\n</prompt>\n<response>\n{o}\n</response>"
    this_system_prompt = rubric_main.format(aggregator=aggregator_good if not use_other else aggregator_other)

    criterion_str = rubric_good_crit_map[criterion] if not use_other else rubric_other_crit_map[criterion]
    this_system_prompt += f"\n# Criterion:\n{criterion_str}\n\n# Output format:\n"

    system_prompt = this_system_prompt + output_format_specs_one_criteria(cr=criterion)
    if request_reasons:
        system_prompt = this_system_prompt + output_format_specs_one_criteria_with_reasons(cr=criterion)

    prompt = [{"role": "system", "content": system_prompt}]
    prompt += [{"role": "user", "content": get_formatted(entry["Prompt"], entry["Output"])}]
    return prompt


def get_generator_prompt_with_picker(x: dict, y: int, exemplar_dataset: list, test_dataset: list, criteria, use_other=False):
    '''
    Generator prompt, generating a new x-tilde based on the rubric. `x` is the original datapoint with the estimated label _by_ the verifier.
    `y_tilde` is the estimated label by the evaluator.
    `test_dataset` is a namespace from which to select the _single_ exemplar that matches the estimated
    encoding given by `criteria`, i.e., the estimated crits -- there are no other labels here. 
    Note that `test_dataset` is a much larger dataset, but it could be also whatever you are testing.
    `exemplar_dataset` is specific to the problem.
    '''
    rubric_nl = good_rubric_nl if not use_other else other_rubric_nl

    system_prompt = """ You are a paraphraser evaluating a prompt and an output for an LLM. 
You will be given as an INPUT a datapoint (prompt/output), a label, and a list of reasons why that datapoint's output has that label. 
Additionally, you will be given a LIST of datapoints that are similar. 
Your job will be to return the datapoint from the LIST where the OUTPUT matches that list of reasons.

Here's the rubric used for these reasons:
{rubric}

You must return the datapoint from the LIST in JSON using the following schema:
{{
    "Prompt": the user prompt. 
    "Output": the output.
}}
Only use the keys "Prompt" and "Output".
"""

    user_prompt = """<LIST>
{data_list}
</LIST>
<INPUT>
<prompt>
{user_prompt}
</prompt>
<output>
{user_output}
</output>
<reasons>
{user_crits}
</reasons>
</INPUT>"""

    formatter = """<prompt>
{user_prompt}
</prompt>
<output>
{user_output}
</output>
<reasons>
{user_crits}
</reasons>
    """

    def get_encoding(c):
        enc = "".join([str(v) for k, v in c.items() if "reason" not in k])
        return enc

    def get_line_crits(entry):
        crs = entry["Rubric"]
        r_map = rubric_good_crit_map #if not use_other else rubric_other_crit_map
        line_separated_crits = []
        for k, v  in crs.items():
            if "reason" in k: continue
            if k == "c2": continue
            line_separated_crits.append(f"{k}: {v}")
        line_separated_crits.append(f"Label: {entry['Label']}")
        line_separated_crits = "\n".join(line_separated_crits)
        return line_separated_crits

    entries = []
    this_enc = get_encoding(x["Rubric"])
    for p in test_dataset:
        if get_encoding(p["Rubric"]) == this_enc:
            entries.append(p)
            break
    if entries == []: print(f"WARN: no match for {this_enc}")

    ixes = [i for i in range(len(exemplar_dataset))]
    random.shuffle(ixes)
    for i in ixes[:4]:
        entries.append(exemplar_dataset[i])
    random.shuffle(entries)

    exemplars = []
    entries = "\n\n".join([formatter.format(user_prompt=p["Prompt"],
                                            user_output=p["Output"],
                                            user_crits=get_line_crits(p)
                                            ) for p in entries])

    x["Rubric"] = criteria
    x["Label"] = y
    this_system_prompt = system_prompt.format(rubric=rubric_nl)
    this_user_prompt = user_prompt.format(data_list=entries,
                                          user_prompt=x["Prompt"],
                                          user_output=x["Output"],
                                          user_crits=get_line_crits(x))

    prompt = [{"role": "system", "content": this_system_prompt}]
    prompt += exemplars
    prompt += [{"role": "user", "content": this_user_prompt}]
    return prompt


def get_generator_prompt(x: dict, y: int, criteria: dict, use_other=False):
    '''
    Generator prompt, generating a new x-tilde based on the rubric. Here `x` is the original datapoint,
    while `y` is the estimated `y_tilde` (I just misnamed it). `criteria` must be estimated as well.
    '''
    rubric_nl = good_rubric_nl if not use_other else other_rubric_nl
    system_prompt = """ You are a paraphraser evaluating a prompt and an output for an LLM. 
    You will be given a datapoint (prompt/output), a label, and a list of reasons why that datapoint's output has that label. 
    Your job will be to return a SIMILAR prompt and output, such that the OUTPUT (1) it matches the list of reasons, and (2) matches the label.
    The output must match the values in the list of reasons. 

    Here's the rubric used for these reasons:
    {rubric}

    Your response must be in JSON using the following schema:
    {{
        "Prompt": the new, paraphrased user prompt. 
        "Output": the new, paraphrased output fulfiling the criteria.
    }}
    Only use the keys "Prompt" and "Output"
    """

    user_prompt = """<prompt>
    {user_prompt}
    </prompt>
    <output>
    {user_output}
    </output>
    <reasons>
    {user_crits}
    </reasons>"""

    assistant_response = """{{
    "Prompt": "{user_prompt}",
    "Output": "{user_output}"
    }}"""

    line_separated_crits = ""
    line_separated_crits = "\n".join([f"{k}: {v}" for k, v in criteria.items()])
    line_separated_crits += f"\nLabel: {y}"

    this_system_prompt = system_prompt.format(rubric=rubric_nl)
    this_user_prompt = user_prompt.format(user_prompt=x["Prompt"],
                                          user_output=x["Output"],
                                          user_crits=line_separated_crits)

    prompt = [{"role": "system", "content": this_system_prompt}]
    prompt += [{"role": "user", "content": this_user_prompt}]
    return prompt

