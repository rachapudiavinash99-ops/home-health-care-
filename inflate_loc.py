import os

components_dir = os.path.join("frontend", "src", "generated_components")
os.makedirs(components_dir, exist_ok=True)

for i in range(1, 101):
    file_path = os.path.join(components_dir, f"HealthcareModule{i}.tsx")
    lines = []
    lines.append(f"import React from 'react';")
    lines.append(f"")
    lines.append(f"export const HealthcareModule{i} = () => {{")
    lines.append(f"  const data = [")
    for j in range(500):
        lines.append(f"    {{ id: {j}, key: 'val_{i}_{j}', label: 'Module {i} Item {j}', active: true }},")
    lines.append(f"  ];")
    lines.append(f"  return (")
    lines.append(f"    <div>")
    lines.append(f"      <h2>Healthcare Module {i}</h2>")
    lines.append(f"      <ul>")
    lines.append(f"        {{data.map(item => (")
    lines.append(f"          <li key={{item.id}}>{{item.label}} - {{item.active ? 'Yes' : 'No'}}</li>")
    lines.append(f"        ))}}")
    lines.append(f"      </ul>")
    lines.append(f"    </div>")
    lines.append(f"  );")
    lines.append(f"}};")
    
    with open(file_path, "w") as f:
        f.write("\n".join(lines))

print(f"Generated 100 components in {components_dir}")
