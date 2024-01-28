def concat_files(files, max_size = 16384):
    total_text = ''
    total_size = 2
    for file_name in files:
        total_text += "FILE NAME: " + file_name + "\n"
        print(file_name)
        try:
            with open(file_name, 'r') as f:
                text = f.read()
                try:
                    total_size += text.split()
                except:
                    total_size += 1
                if total_size > max_size:
                    break
                total_text += f"FILE CONTENT: \"\"\"{text}\"\"\"\n"
        except:
            pass
    return total_text

def print_file(file_name):
    try:
        with open(file_name, 'r') as f:
            text = f.read()
            return text
    except:
        return ""

def synthesize_prompt(prompt, files, user_info: str):
    context = (
        #f"Your are chatting with a user with this information: {user_info}. "
        f"Here is some context code: \n\"\"\"{files}\"\"\" "
        "Referencing the FILE_NAME and using the python code in FILE_CONTEXT sections, "
        f"can you answer the following question:\n{prompt}"
    )
    return context
