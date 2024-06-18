import subprocess
import os

def get_git_diff(repo_path, commit1, commit2):
    try:
        # Change the current working directory to the repository path
        os.chdir(repo_path)
        
        # Run the git diff command and capture the output
        result = subprocess.run(
            ['git', 'diff', commit1, commit2],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Check for errors
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return None
        
        return result.stdout
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def parse_git_diff(diff_output):
    changes = {}
    current_file = None
    
    for line in diff_output.splitlines():
        if line.startswith('diff --git'):
            # Extract the filename from the diff line
            parts = line.split(' ')
            current_file = parts[2][2:]  # Remove the 'a/' prefix
            changes[current_file] = {'added': [], 'removed': []}
        elif line.startswith('+') and not line.startswith('+++'):
            changes[current_file]['added'].append(line[1:])
        elif line.startswith('-') and not line.startswith('---'):
            changes[current_file]['removed'].append(line[1:])
    
    return changes

def output_diff(repo_path, commit1, commit2):

    
    diff_output = get_git_diff(repo_path, commit1, commit2)
    if diff_output is not None:
        changes = parse_git_diff(diff_output)

        with open('diff_output.txt', 'w') as f:
            for file, change in changes.items():
                f.write(f"File: {file}\n")
                f.write("Added lines:\n")
                for line in change['added']:
                    f.write(f"+ {line}\n")
                f.write("Removed lines:\n")
                for line in change['removed']:
                    f.write(f"- {line}\n")
                f.write("\n")

