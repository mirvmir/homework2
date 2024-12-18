
import subprocess
import yaml
from datetime import datetime

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def get_commits(repo_path, start_date):
    result = subprocess.run(
        ["git", "-C", repo_path, "log", "--after=" + start_date, "--pretty=format:%H|%ad|%an", "--date=iso"],
        capture_output=True, text=True
    )
    return [line.split("|") for line in result.stdout.splitlines()]

def generate_puml(commits):
    lines = ["@startuml"]
    for i in range(len(commits) - 1):
        commit_hash, date, author = commits[i]
        next_commit_hash, _, _ = commits[i + 1]
        lines.append(f"{commit_hash} --> {next_commit_hash} : {date} by {author}")
    lines.append("@enduml")
    return "\n".join(lines)

def save_puml(puml_text, file_path):
    with open(file_path, "w") as f:
        f.write(puml_text)

def generate_image(puml_path, plantuml_path, output_path):
    subprocess.run(["java", "-jar", plantuml_path, puml_path, "-o", output_path])

def main():
    config = load_config()
    commits = get_commits(config["repository_path"], config["commit_date"])
    puml_text = generate_puml(commits)
    
    # Save .puml file
    puml_path = "dependency_graph.puml"
    save_puml(puml_text, puml_path)

    # Generate PNG image
    generate_image(puml_path, config["visualization_program_path"], config["output_image_path"])
    print("Граф зависимостей успешно построен и сохранён.")

if __name__ == "__main__":
    main()
