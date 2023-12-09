import re, os, json


color_tag_pattern = re.compile(r'<color=(#[A-Fa-f0-9]{8})>(.*?)</color>')
chinese_pattern = re.compile(r'[\u4e00-\u9fff]')


def process_json_file(file_path):
    lines = []
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

        for entry in data["labelDataArray"]:
            lines.append(process_word_data_array(entry["wordDataArray"]))
        return lines


def replace_color_tags(match):
    color_code = match.group(1)  # Extract the color code from the match
    text = match.group(2)  # Extract the text inside the color tags
    return f'<span style="color: {color_code};">{text}</span>'

def convert_color_tags_in_string(s):
    # Define a function to convert color tags to HTML spans
    return re.sub(color_tag_pattern, replace_color_tags, s)



def contains_chinese_character(s):
    # Regular expression pattern to match at least one Chinese character
    return bool(re.search(chinese_pattern, s))

def process_word_data_array(word_data_array):
    """
    :param word_data_array:
    :return: a complete line of text with any empty strings subbed out
    """
    # Process the 'wordDataArray' here as needed
    # For example, concatenate 'str' values
    s = ""
    for word_entry in word_data_array:
        str = word_entry["str"]
        if str == "":
            s += "[]"
        else:
            s += str
    if not contains_chinese_character(s):
        return ""
    return s + "\n"


def extract_chinese_lines(input_directory, output_file):
    output_lines = []
    line_set = set()
    i = 0
    for filename in os.listdir(input_directory):
        if filename.endswith(".json"):
            file_path = os.path.join(input_directory, filename)
            processed_data = process_json_file(file_path)
            for line in processed_data:
                if line not in line_set:
                    output_lines.append(f'{i:05}\t{line}')
                    i += 1
                    line_set.add(line)
    combined_text = "".join(output_lines)  # Combine all lines into one giant string
    final_text = convert_color_tags_in_string(combined_text)  # Apply tag substitutions

    with open(output_file, 'w', encoding='utf-8') as out_file:
        out_file.write(final_text)


# Usage
input_directory = "data"
output_file = "out.txt"
extract_chinese_lines(input_directory, output_file)


