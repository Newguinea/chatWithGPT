import os
filename = "output.txt"

if os.path.exists(filename):
    os.remove(filename)
def read_code_from_file(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    return code

def write_code_to_file(file_path, code):
    with open(file_path, 'a') as file:
        file.write(code)

file_list = [
    'app/__init__.py',
    'app/api.py',
    'app/forms.py',
    'app/models.py',
    'app/routes.py',
    'app/templates/index.html',
    'app/templates/login.html',
    'app/templates/register.html',
    'app/static/chat.js',
    'app.py',
    'config.py'
]

output_file = 'output.txt'

current_directory = os.getcwd()
output_path = os.path.join(current_directory, output_file)

for file_path in file_list:
    code = read_code_from_file(os.path.join(current_directory, file_path))
    write_code_to_file(output_path, f'{file_path}\n##############################\n{code}\n##############################\n')
    write_code_to_file(output_path, '\n')

filename = 'output.txt'
old_line = 'openai.api_key'

# 打开文件并读取所有行

with open(filename, 'r') as file:
    lines = file.readlines()

# 查找要修改的行
for i, line in enumerate(lines):
    if line.startswith(old_line):
        # 修改行的内容
        new_line = f'{old_line} = "{old_line}"\n'
        lines[i] = new_line
        break

# 将修改后的内容写回文件
with open(filename, 'w') as file:
    file.writelines(lines)

print(f"代码已成功输出到文件 '{output_file}' 中。")