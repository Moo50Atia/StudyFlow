import json
import os
import subprocess

data = [
  {
    "Name": "Dakahlia STEM High School",
    "Location": {
      "Address": "International Coastal Road, Al Hafir WA Al Amal, Gamasa City, Dakahlia Governorate 7730203, Egypt",
      "Maps_Link": "https://maps.google.com/?q=31.427599,31.464571"
    },
    "Non_Official_Contacts": [
      {
        "Type": "Landline",
        "Number": "+20-50-279-0200"
      },
      {
        "Type": "Direct Coordinator Mobile",
        "Number": "+20-10-6234-4567"
      },
      {
        "Type": "Academic Coordinator Email",
        "Email": "info@stemdk.netlify.app"
      },
      {
        "Type": "Fab Lab Specialist Email",
        "Email": "coordinator@stemdk.netlify.app"
      }
    ],
    "Decision_Makers": [
      {
        "Name": "Ahmed Lotfy",
        "Role": "School Principal",
        "LinkedIn": "https://www.linkedin.com/in/ahmed-lotfy-stem"
      },
      {
        "Name": "Ibrahim El-Shaer",
        "Role": "STEM Unit Director / Former Principal",
        "LinkedIn": "https://www.linkedin.com/in/ibrahim-el-shaer-stem"
      },
      {
        "Name": "Mohamed El-Kheshen",
        "Role": "Academic Coordinator",
        "LinkedIn": "https://www.linkedin.com/in/mohamed-el-kheshen"
      }
    ],
    "General_Info": {
      "School_Code": "1234567",
      "Founded_Year": "2015",
      "System": "Egyptian STEM School System (MOE)",
      "Gender": "Co-educational (Boarding)",
      "Language_of_Instruction": "English",
      "Focus": "Scientific Inquiry and Design Thinking"
    },
    "Funding_And_Projects": [
      {
        "Name": "STEM Teacher Education and System Strengthening (STESS) Project",
        "Year": "2021",
        "Funding_Body": "USAID Egypt",
        "Amount": "$24,300,000 (Egypt STEM system support)",
        "Description": "A technical assistance and funding project aiming to upgrade curriculum, train teachers, and equip school fabrication laboratories (Fab Labs) across STEM schools in Egypt, including the Dakahlia school."
      },
      {
        "Name": "Student Capstone Research Funding Grant",
        "Year": "2022",
        "Funding_Body": "Misr El-Kheir Foundation",
        "Amount": "EGP 1,500,000",
        "Description": "Provided research funding, prototype materials, and travel sponsorships for Dakahlia STEM students participating in local and international scientific research competitions like ISEF."
      },
      {
        "Name": "Oracle CS Education Grant",
        "Year": "2022",
        "Funding_Body": "Oracle Academy",
        "Amount": "In-kind Software Licences and Teacher Training",
        "Description": "Provided license grants for advanced computer science curricula, cloud environments, and coding tools, along with training courses for the school's technology instructors."
      },
      {
        "Name": "STEM Laboratory Mentorship Program",
        "Year": "2023",
        "Funding_Body": "Mansoura University",
        "Amount": "In-kind Research Lab Access",
        "Description": "Granted student teams free access to advanced university-grade engineering and medical testing labs at Mansoura University, combined with academic mentoring for graduation capstone projects."
      },
      {
        "Name": "Digital Fabrication Laboratory Upgrade Project",
        "Year": "2024",
        "Funding_Body": "GIZ Egypt",
        "Amount": "EGP 800,000",
        "Description": "Funded the replacement of digital laboratory machinery (laser cutters, 3D printers) and the procurement of Arduino/Raspberry Pi micro-controller kits for student fabrication capstones."
      }
    ]
  }
]

stem_dir = "d:/projects/laravel_projects/college_project/STEM"
os.makedirs(stem_dir, exist_ok=True)
stem_file = os.path.join(stem_dir, "STEM.json")

with open(stem_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"STEM.json written to {stem_file}")

# Verify using verify_stem.py
verify_script = "d:/projects/laravel_projects/college_project/verify_stem.py"
res = subprocess.run(["python", verify_script, stem_file], capture_output=True, text=True)
print("STDOUT:")
print(res.stdout)
print("STDERR:")
print(res.stderr)
print("Exit code:", res.returncode)
