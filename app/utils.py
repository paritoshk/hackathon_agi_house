def concat_files(files):
    total_text = ''
    for file_name in files:
        total_text += "FILE NAME: " + file_name + "\n"
        with open(file_name, 'r') as f:
            text = f.read()
            total_text += f"FILE CONTENT: \"\"\"{text}\"\"\"\n"
    return total_text

def synthesize_prompt(prompt, files, user_info: str):
    context = (
        f"Your are chatting with a user with this information: {user_info}. "
        f"Here is some context code: \n\"\"\"{files}\"\"\" "
        "Referencing the FILE_NAME and using the python code in FILE_CONTEXT sections, "
        f"can you answer the following question:\n{prompt}"
    )
    return context
