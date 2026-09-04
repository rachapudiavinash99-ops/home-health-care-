import os
import zipfile

def create_submission_zip(source_dir, output_filename):
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            # Exclude unwanted directories
            if 'node_modules' in dirs:
                dirs.remove('node_modules')
            if 'venv' in dirs:
                dirs.remove('venv')
            if '__pycache__' in dirs:
                dirs.remove('__pycache__')

            for file in files:
                # Exclude unwanted files
                if file.startswith('.env') or file.endswith('.zip'):
                    continue
                
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, arcname)

if __name__ == '__main__':
    create_submission_zip('.', 'D:\\submission_fixed.zip')
    print('Zip created successfully at D:\\submission_fixed.zip including .git')
