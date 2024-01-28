def concat_files(files):
    total_text = ''
    for file_name in files:
        total_text += "FILE NAME: " + file_name + "\n"
        with open(file_name, 'r') as f:
            text = f.read()
            total_text += f"FILE CONTENT: \"\"\"{text}\"\"\"\n"
    return total_text

def synthesize_prompt(prompt, files):
    context = f"Here is some context code: \n \"\"\"{files}\"\"\"" + "Referencing the FILE_NAME and using the python code in FILE_CONTEXT sections, can you answer the following question:\n"
    return context + prompt