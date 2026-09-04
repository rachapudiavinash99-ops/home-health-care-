import os

def write_file(rel_path, content):
    p = os.path.join(r'D:\avinash\submission_fixed\frontend\src', rel_path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    print('Wrote:', rel_path)
