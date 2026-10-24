import math
import os

SUBJECT_TOPICS = {
    "python": [
        "Variables and data types", "Conditions and loops", "Functions",
        "Lists, tuples, and dictionaries", "Classes and objects",
        "File handling and exceptions", "NumPy basics",
    ],
    "c programming": [
        "Data types and operators", "Conditions and loops", "Functions",
        "Arrays and strings", "Pointers", "Structures and unions",
        "File handling",
    ],
    "java programming": [
        "Java basics and data types", "Conditions and loops",
        "Classes and objects", "Inheritance and polymorphism",
        "Exception handling", "Collections", "File handling",
    ],
    "object oriented programming": [
        "Classes and objects", "Encapsulation", "Abstraction",
        "Inheritance", "Polymorphism", "Constructors",
        "Exception handling",
    ],
    "data structures": [
        "Arrays", "Linked lists", "Stacks and queues", "Trees",
        "Graphs", "Searching and sorting", "Hashing",
    ],
    "design and analysis of algorithms": [
        "Algorithm analysis", "Divide and conquer", "Greedy algorithms",
        "Dynamic programming", "Backtracking", "Graph algorithms",
        "Complexity classes",
    ],
    "dbms": [
        "Database concepts", "Entity-relationship model", "Relational model",
        "SQL queries", "Normalization", "Transactions",
        "Concurrency and recovery",
    ],
    "operating systems": [
        "Operating-system basics", "Processes and threads", "CPU scheduling",
        "Process synchronization", "Deadlocks", "Memory management",
        "File systems",
    ],
    "computer networks": [
        "Network fundamentals", "OSI and TCP/IP models", "IP addressing",
        "Routing", "Transport-layer protocols", "Network security",
        "Application-layer protocols",
    ],
    "software engineering": [
        "Software development life cycle", "Requirements analysis",
        "Software design", "Software testing", "Project management",
        "Software maintenance", "Agile methods",
    ],
    "computer organization and architecture": [
        "Number systems", "Digital logic", "Processor organization",
        "Instruction sets", "Memory hierarchy", "Input and output systems",
        "Pipelining",
    ],
    "discrete mathematics": [
        "Logic and propositions", "Sets and relations", "Functions",
        "Combinatorics", "Graph theory", "Trees", "Boolean algebra",
    ],
    "engineering mathematics": [
        "Matrices and determinants", "Differential calculus",
        "Integral calculus", "Differential equations", "Vector calculus",
        "Fourier series", "Numerical methods",
    ],
    "probability and statistics": [
        "Descriptive statistics", "Probability", "Random variables",
        "Probability distributions", "Sampling", "Hypothesis testing",
        "Correlation and regression",
    ],
    "artificial intelligence": [
        "Introduction to artificial intelligence", "Intelligent agents",
        "Search algorithms", "Knowledge representation", "Reasoning",
        "Machine learning basics", "AI applications and ethics",
    ],
    "machine learning": [
        "Introduction to machine learning", "Data preparation",
        "Linear regression", "Classification", "Decision trees",
        "Clustering", "Model evaluation",
    ],
    "deep learning": [
        "Neural network basics", "Perceptrons", "Activation functions",
        "Backpropagation", "Convolutional neural networks",
        "Recurrent neural networks", "Model evaluation",
    ],
    "data mining": [
        "Data preprocessing", "Association rules", "Classification",
        "Clustering", "Outlier detection", "Pattern evaluation",
        "Data mining applications",
    ],
    "big data analytics": [
        "Big data concepts", "Hadoop basics", "HDFS", "MapReduce",
        "Spark basics", "NoSQL databases", "Big data applications",
    ],
    "cloud computing": [
        "Cloud computing concepts", "Service models", "Deployment models",
        "Virtualization", "Cloud storage", "Cloud security", "Cloud platforms",
    ],
    "cybersecurity": [
        "Security principles", "Common cyber threats", "Cryptography basics",
        "Network security", "Authentication and access control",
        "Web security", "Incident response",
    ],
    "internet of things": [
        "IoT architecture", "Sensors and actuators",
        "IoT communication protocols", "Microcontrollers", "Cloud and IoT",
        "IoT security", "IoT applications",
    ],
    "digital electronics": [
        "Number systems and codes", "Boolean algebra", "Logic gates",
        "Combinational circuits", "Sequential circuits",
        "Counters and registers", "Memory devices",
    ],
    "electrical circuits": [
        "Circuit laws", "Network theorems", "DC circuit analysis",
        "AC circuit analysis", "Resonance", "Transient analysis",
        "Two-port networks",
    ],
    "signals and systems": [
        "Signal classification", "System properties",
        "Continuous-time signals", "Discrete-time signals",
        "Fourier analysis", "Laplace transform", "Z-transform",
    ],
    "control systems": [
        "Control-system basics", "Transfer functions", "Block diagrams",
        "Time-response analysis", "Stability", "Root-locus method",
        "Frequency-response analysis",
    ],
    "electrical machines": [
        "Transformer basics", "DC machines", "Induction motors",
        "Synchronous machines", "Machine characteristics",
        "Losses and efficiency", "Electrical machine applications",
    ],
    "power systems": [
        "Power-generation basics", "Transmission lines",
        "Power-system components", "Load-flow analysis", "Fault analysis",
        "Protection systems", "Renewable energy systems",
    ],
    "engineering mechanics": [
        "Force systems", "Equilibrium", "Friction", "Centroids",
        "Kinematics", "Kinetics", "Work and energy",
    ],
    "strength of materials": [
        "Stress and strain", "Elastic constants",
        "Shear force and bending moment", "Bending stress", "Torsion",
        "Columns", "Deflection of beams",
    ],
    "thermodynamics": [
        "Basic thermodynamic concepts", "Laws of thermodynamics",
        "Properties of pure substances", "First-law applications",
        "Second-law applications", "Power cycles", "Refrigeration cycles",
    ],
    "fluid mechanics": [
        "Fluid properties", "Fluid statics", "Fluid kinematics",
        "Continuity equation", "Bernoulli equation", "Flow through pipes",
        "Boundary layers",
    ],
    "engineering physics": [
        "Waves and oscillations", "Optics", "Lasers and fibre optics",
        "Quantum physics", "Semiconductors", "Electromagnetism",
        "Materials science",
    ],
    "engineering chemistry": [
        "Water treatment", "Electrochemistry", "Corrosion",
        "Fuels and combustion", "Polymers", "Nanomaterials",
        "Green chemistry",
    ],
    "environmental science": [
        "Ecosystems", "Natural resources", "Biodiversity", "Air pollution",
        "Water pollution", "Climate change", "Waste management",
    ],
    "english": [
        "Parts of speech", "Tenses", "Active and passive voice",
        "Direct and indirect speech", "Subject-verb agreement",
        "Reading comprehension", "Essay writing",
    ],
    "history": [
        "Ancient history", "Medieval history", "Modern history",
        "Important movements", "Historical leaders", "Major events",
        "Timeline revision",
    ],
    "geography": [
        "Physical geography", "Climate", "Landforms", "Natural resources",
        "Population", "Maps and locations", "Environmental issues",
    ],
    "economics": [
        "Basic economic concepts", "Demand and supply", "Production and costs",
        "Market structures", "National income", "Inflation and unemployment",
        "Economic development",
    ],
    "civics": [
        "Constitution", "Fundamental rights and duties",
        "Government structure", "Legislature", "Executive", "Judiciary",
        "Local government",
    ],
}

ALIASES = {
    "ds": "data structures",
    "data structure": "data structures",
    "dsa": "design and analysis of algorithms",
    "maths": "engineering mathematics",
    "os": "operating systems",
    "cn": "computer networks",
    "coa": "computer organization and architecture",
    "ai": "artificial intelligence",
    "ml": "machine learning",
    "iot": "internet of things",
}

print("Personalised Exam Revision Planner")
print("----------------------------------")

student_name = input("Enter your name: ")
subject = input("Enter the subject name: ").strip()
days_left = int(input("How many days are left until the exam? "))
hours_per_day = float(input("How many hours can you study each day? "))

if days_left <= 0:
    print("Please enter at least 1 day.")
    raise SystemExit

if hours_per_day <= 0:
    print("Please enter more than 0 study hours.")
    raise SystemExit

subject_key = subject.lower()
subject_key = ALIASES.get(subject_key, subject_key)

if subject_key in SUBJECT_TOPICS:
    topics = SUBJECT_TOPICS[subject_key].copy()
    print(f"\nTopics selected automatically for {subject}:")
    for topic in topics:
        print("-", topic)
else:
    print(f"\nNo built-in topic list found for {subject}.")
    print("Enter the topics yourself. Type 'done' when finished.")

    topics = []

    while True:
        topic = input("Enter a topic: ").strip()

        if topic.lower() == "done":
            break

        if topic:
            topics.append(topic)

if not topics:
    print("No topics are available. Please run the program again.")
    raise SystemExit

confidence = {}

print("\nRate your confidence in each topic from 1 to 5.")
print("1 = Not confident, 5 = Very confident")

for topic in topics:
    while True:
        try:
            level = int(input(f"{topic} (1-5): "))

            if 1 <= level <= 5:
                confidence[topic] = level
                break

            print("Please enter a number from 1 to 5.")
        except ValueError:
            print("Please enter a whole number from 1 to 5.")

topics.sort(key=lambda item: confidence[item])
topics_per_day = math.ceil(len(topics) / days_left)

plan_lines = [
    f"Study timetable for {student_name}",
    f"Subject: {subject}",
    f"Days until the exam: {days_left}",
    "",
]

for day in range(days_left):
    start = day * topics_per_day
    end = start + topics_per_day
    todays_topics = topics[start:end]

    if todays_topics:
        average_confidence = sum(
            confidence[item] for item in todays_topics
        ) / len(todays_topics)

        study_percentage = 0.5 + (5 - average_confidence) * 0.075
        topic_study_hours = hours_per_day * study_percentage
        revision_hours = hours_per_day - topic_study_hours

        total_weight = sum(
            6 - confidence[item] for item in todays_topics
        )

        plan_lines.append(f"Day {day + 1}:")

        for item in todays_topics:
            weight = 6 - confidence[item]
            allocated_hours = topic_study_hours * weight / total_weight

            plan_lines.append(
                f"  - {item} "
                f"(confidence: {confidence[item]}/5, "
                f"study: {allocated_hours:.1f} hours)"
            )

        plan_lines.append(
            f"  Quick revision: {revision_hours:.1f} hours"
        )
    else:
        plan_lines.append(f"Day {day + 1}: Revision and practice")
        plan_lines.append(
            f"  Study time: {hours_per_day:.1f} hours"
        )

    plan_lines.append("")

plan_text = "\n".join(plan_lines)
print("\n" + plan_text)

safe_subject = "".join(
    character if character.isalnum() else "_"
    for character in subject
).strip("_")

if not safe_subject:
    safe_subject = "subject"

file_number = 1

while True:
    if file_number == 1:
        filename = f"study_plan_{safe_subject}.txt"
    else:
        filename = f"study_plan_{safe_subject}_{file_number}.txt"

    try:
        with open(filename, "x", encoding="utf-8") as file:
            file.write(plan_text)
        break
    except FileExistsError:
        file_number += 1

print(f"Timetable saved as {filename}")