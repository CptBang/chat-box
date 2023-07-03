from Application import constants


def inject_personality(incoming_profile):
    print(incoming_profile)
    params_to_sub = {
        'char': incoming_profile['character_name'],
        'user': 'user',
        'char_appearance': incoming_profile['appearance'],
        'char_personality': incoming_profile['character_name'],
        'scenario': incoming_profile['scenario'],
    }
    system_prompt_strings = make_system_prompt(constants.CHARACTER_APPEARANCE_PROMPT,
                                               constants.CHARACTER_PERSONALITY_PROMPT,
                                               constants.CHAT_SCENARIO_PROMPT, constants.GENERAL_RP_PROMPT,
                                               constants.JAILBREAK_PROMPT)
    system_prompt = substitute_params(system_prompt_strings, params_to_sub)
    personality_system_message = {"role": "system", "content": system_prompt}
    return personality_system_message


def make_system_prompt(*args):
    system_prompt = " ".join(str(arg) for arg in args)
    return system_prompt


def substitute_params(input_str, params):
    return input_str.format(**params)
