import os

frontend_dir = r'D:\avinash\submission_fixed\frontend|src'
for d in ['api', 'layouts', 'pages', 'routes']:
    os.makedirs(os.path.join(frontend_dir, d), exist_ok=True)

print('Directories created')
