import random


rubric_main = """You are an LLM evaluator. You will be given a prompt and an response in West Frisian, meant for West Frisian readers. 
Your job will be to verify if the response follows certain criteria and give a final ternary (0,1,2) score.

Check the output against the criteria below. If it fulfils the criteria, score it as a 1. Otherwise, 0. 
{aggregator}
"""


output_format_specs_label_only = """
Give your answer in JSON format, using the values 0, 1, or 2. Use this scheme:
{"Label": <the label, 0, 1 or 2>}
Only use the key "Label" and the values 0, 1 or 2.
"""


output_format_specs_all_criteria = """
Give your answer in JSON format, using the values 0 or 1 for each criterion, and 0, 1, 2 for the label. Use this scheme:
{"c1": <the value, 0 or 1>,
"c2a": <the value, 0 or 1>,
"c2b": <the value, 0 or 1>,
"c3": <the value, 0 or 1>,
"c4": <the value, 0 or 1>,
"c5": <the value, 0 or 1>,
"Label": <the value, 0, 1 or 2>}
Only use the keys "c1", "c2a", "c2b", "c3", "c4", "c5", wit values 0 or 1; and "Label", with values 0, 1, or 2.
"""


output_format_specs_all_criteria_with_reasons = """
Give your answer in JSON format, using the values 0 or 1 for each criterion, and 0, 1, 2 for the label. Use this scheme:
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
"Label": <the value, 0, 1 or 2>}
Only use the keys "c1", "c2a", "c2b", "c3", "c4", "c5"; "c1_reason", "c2a_reason", "c2b_reason", "c3_reason", "c4_reason", "c5_reason"; and "Label".
If the value for a key is 0, its corresponding reason cannot be empty.
"""


output_format_specs_label_only_01 = """
Give your answer in JSON format, using the values 0 or 1. Use this scheme:
{"Label": <the label, 0 or 1>}
Only use the key "Label" and the values 0 or 1.
"""

output_format_specs_all_criteria_01 = """
Give your answer in JSON format, using the values 0 or 1 for each criterion, and 0 or 1 for the label. Use this scheme:
{"c1": <the value, 0 or 1>,
"c2a": <the value, 0 or 1>,
"c2b": <the value, 0 or 1>,
"c3": <the value, 0 or 1>,
"c4": <the value, 0 or 1>,
"c5": <the value, 0 or 1>,
"Label": <the value, 0 or 1>}
Only use the keys "c1", "c2a", "c2b", "c3", "c4", "c5", wit values 0 or 1; and "Label", with values 0 or 1.
"""

output_format_specs_all_criteria_with_reasons_01 = """
Give your answer in JSON format, using the values 0 or 1 for each criterion, and 0 or 1 for the label. Use this scheme:
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



# Criteria are always binary
from no_data_prompts import (output_format_specs_one_criteria,
                             output_format_specs_one_criteria_with_reasons)


from no_data_prompts import (check1, check2a, check2b, check2assembled, check3, check4, check5, 
                            rubric_good_crit_map)

from no_data_prompts import (fake_check1, fake_check2a, fake_check2b, fake_check3, fake_check4, fake_check5, 
                            rubric_other_crit_map)


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

aggregator_good = "If all the criteria are 1, the label should be 2. If there is only one zero, the label is 1. Else, it is 0"
aggregator_other = aggregator_good

# First we split between 0, 12
aggregator_good_kary_01 = "If all the criteria are 1, or there is one zero, the label should be 1. With two or more zeros, it is 0"
aggregator_other_kary_01 = aggregator_good_kary_01
# And now between 1, 2 -- we surrogate to 0/1
aggregator_good_kary_12 = "If all the criteria are 1, the label should be 1. Else it is 0."
aggregator_other_kary_12 = aggregator_good_kary_12

good_rubric_nl = good_rubric_nl.format(rubric_main=rubric_main.format(aggregator=aggregator_good),
                                       check1=check1, check2a=check2a, check2b=check2b,
                                       check3=check3, check4=check4, check5=check5)
other_rubric_nl = other_rubric_nl.format(rubric_main=rubric_main.format(aggregator=aggregator_other),
                                       fake_check1=fake_check1, fake_check2a=fake_check2a, fake_check2b=fake_check2b,
                                       fake_check3=fake_check3, fake_check4=fake_check4, fake_check5=fake_check5)

good_rubric_nl_01 = good_rubric_nl.format(rubric_main=rubric_main.format(aggregator=aggregator_good_kary_01),
                                       check1=check1, check2a=check2a, check2b=check2b,
                                       check3=check3, check4=check4, check5=check5)
good_rubric_nl_12 = good_rubric_nl.format(rubric_main=rubric_main.format(aggregator=aggregator_good_kary_12),
                                       check1=check1, check2a=check2a, check2b=check2b,
                                       check3=check3, check4=check4, check5=check5)
other_rubric_nl_01 = other_rubric_nl.format(rubric_main=rubric_main.format(aggregator=aggregator_other),
                                       fake_check1=fake_check1, fake_check2a=fake_check2a, fake_check2b=fake_check2b,
                                       fake_check3=fake_check3, fake_check4=fake_check4, fake_check5=fake_check5)
other_rubric_nl_12 = other_rubric_nl.format(rubric_main=rubric_main.format(aggregator=aggregator_other),
                                       fake_check1=fake_check1, fake_check2a=fake_check2a, fake_check2b=fake_check2b,
                                       fake_check3=fake_check3, fake_check4=fake_check4, fake_check5=fake_check5)


def get_evaluator_prompt_all_criteria_kary(entry: dict, request_breakdown=False, request_reasons=False,
                                           positive_label=None, use_other=False):
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

    if positive_label is not None:
        if positive_label == 1:
            this_system_prompt = good_rubric_nl_01 if not use_other else other_rubric_nl_01
        if positive_label == 2:
            this_system_prompt = good_rubric_nl_12 if not use_other else other_rubric_nl_12

        if request_breakdown:
            system_prompt = this_system_prompt + output_format_specs_all_criteria_01
            if request_reasons:
                system_prompt = this_system_prompt + output_format_specs_all_criteria_with_reasons_01
        else:
            system_prompt = this_system_prompt + output_format_specs_label_only_01

    prompt = [{"role": "system", "content": system_prompt}]
    prompt += [{"role": "user", "content": get_formatted(entry["Prompt"], entry["Output"])}]
    return prompt


def get_evaluator_prompt_single_criteria_kary(entry: dict, criterion: str, request_reasons=False, 
                                              positive_label=None, use_other=False):
    '''
    Evaluator prompt returning the score for a single criterion. Optionally request the '_reason' field.
    '''
    get_formatted = lambda p, o: f"<prompt>\n{p}\n</prompt>\n<response>\n{o}\n</response>"
    this_system_prompt = rubric_main.format(aggregator=aggregator_good if not use_other else aggregator_other)

    if positive_label is not None:
        if positive_label == 1:
            this_system_prompt = rubric_main.format(aggregator=aggregator_good_kary_01)
            if use_other:
                this_system_prompt = rubric_main.format(aggregator=aggregator_other_kary_01)
        if positive_label == 2:
            this_system_prompt = rubric_main.format(aggregator=aggregator_good_kary_12)
            if use_other:
                this_system_prompt = rubric_main.format(aggregator=aggregator_other_kary_12)

    criterion_str = rubric_good_crit_map[criterion] if not use_other else rubric_other_crit_map[criterion]
    this_system_prompt += f"\n# Criterion:\n{criterion_str}\n\n# Output format:\n"

    system_prompt = this_system_prompt + output_format_specs_one_criteria(cr=criterion)
    if request_reasons:
        system_prompt = this_system_prompt + output_format_specs_one_criteria_with_reasons(cr=criterion)

    prompt = [{"role": "system", "content": system_prompt}]
    prompt += [{"role": "user", "content": get_formatted(entry["Prompt"], entry["Output"])}]
    return prompt


def get_generator_prompt_with_picker_kary(x: dict, y: int, exemplar_dataset: list, test_dataset: list, criteria, positive_label=None, use_other=False):
    '''
    Generator prompt, generating a new x-tilde based on the rubric. `x` is the original datapoint with the estimated label _by_ the verifier.
    `y_tilde` is the estimated label by the evaluator.
    `test_dataset` is a namespace from which to select the _single_ exemplar that matches the estimated
    encoding given by `criteria`, i.e., the estimated crits -- there are no other labels here. 
    Note that `test_dataset` is a much larger dataset, but it could be also whatever you are testing.
    `exemplar_dataset` is specific to the problem.
    '''
    rubric_nl = good_rubric_nl if not use_other else other_rubric_nl
    if positive_label is not None:
        if positive_label == 1:
            rubric_nl = good_rubric_nl_01 if not use_other else other_rubric_nl_01
        if positive_label == 2:
            rubric_nl = good_rubric_nl_12 if not use_other else other_rubric_nl_12

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


def get_generator_prompt_kary(x: dict, y: int, criteria: dict, positive_label=None, use_other=False):
    '''
    Generator prompt, generating a new x-tilde based on the rubric. Here `x` is the original datapoint,
    while `y` is the estimated `y_tilde` (I just misnamed it). `criteria` must be estimated as well.
    '''
    rubric_nl = good_rubric_nl if not use_other else other_rubric_nl
    if positive_label is not None:
        if positive_label == 1:
            rubric_nl = good_rubric_nl_01 if not use_other else other_rubric_nl_01
        if positive_label == 2:
            rubric_nl = good_rubric_nl_12 if not use_other else other_rubric_nl_12

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
