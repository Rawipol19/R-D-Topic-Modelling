import re
from collections import defaultdict

# Define keywords for each group
group_keywords = {
    "Game": ["Game", "Simulation", "Design", "Graphics", "Creative Writing", "Public Speaking"],
    "Coding": ["Programming", "Machine Learning", "Neural Networks", "Data Mining", "Transformer", "NLP", "Computer Vision", "Software Engineering"],
    "Research": ["Research", "Writing", "Academic", "Technical Writing", "Information Retrieval", "Cluster Analysis"],
    "Security": ["Cybersecurity", "Cryptography", "Network Security", "Threat Detection", "Malware Analysis"],
    "Physics": ["Quantum Mechanics", "Electromagnetism", "Classical Mechanics", "Thermodynamics", "Relativity"],
    "Design": ["User Interface", "User Experience", "Industrial Design", "Product Design", "Creative Design"],
    "Business": ["Innovation", "Entrepreneurship", "Management", "Marketing", "Creative Business", "Business Strategy"],
    "AI": ["Artificial Intelligence", "Deep Learning", "Natural Language Processing", "AI Ethics", "Reinforcement Learning"],
    "Network": ["Network Engineering", "Telecommunications", "Routing", "Network Protocols", "Internet of Things"]
}

# Function to classify competencies into groups
def classify_competency(competency_name, group_keywords):
    for group, keywords in group_keywords.items():
        if any(keyword in competency_name for keyword in keywords):
            return group
    return "Other"  # For competencies that don’t match any keywords

# Function to read and classify competencies from file
def read_and_classify_competencies(file_path):
    competencies = defaultdict(list)
    
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

            current_pillar = None
            for line in lines:
                # Trim whitespace for consistent processing
                line = line.strip()
                
                # Check for new pillar section
                if "Pillar:" in line:
                    current_pillar = line.split(":")[1].strip()
                    print(f"\nDetected new pillar: {current_pillar}")
                    continue
                
                # Only process lines that contain a competency code like 'XXX-###'
                if re.search(r"\b[A-Z]{3}-\d{3}\b", line):
                    # Extract the code and the remaining content in a simple way
                    match = re.search(r"([A-Z]{3}-\d{3})\s+(.+)", line)
                    if match:
                        competency_code = match.group(1).strip()
                        competency_name = match.group(2).strip()
                        
                        # Classify the competency and add to respective group
                        group = classify_competency(competency_name, group_keywords)
                        competencies[group].append({
                            "pillar": current_pillar,
                            "competency_code": competency_code,
                            "competency_name": competency_name,
                            "group": group
                        })
                        print(f"Added '{competency_code} - {competency_name}' to group '{group}' under pillar '{current_pillar}'")
                    else:
                        print(f"Skipping line due to unmatched format: {line}")
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None

    return competencies

# File path
file_path = r"C:\Users\acer\Downloads\CMKL_Year3_Term1\R_and_D_ThirdYearCode\CurriculumText\doc\CMKL_V3_all_pillars.txt"

# Classify competencies and display results
competencies = read_and_classify_competencies(file_path)

if competencies:
    # Print the grouped competencies with spacing for readability
    for group, comps in competencies.items():
        print(f"\nGroup: {group}")
        for comp in comps:
            print(f" - {comp['competency_code']} {comp['competency_name']} (Pillar: {comp['pillar']}, Group: {comp['group']})")
        print("\n" + "-" * 40)
else:
    print("No competencies were classified.")