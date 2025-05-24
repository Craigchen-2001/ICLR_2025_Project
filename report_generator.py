import os
import csv

base_folder = "ICLR_2025_Papers"
report_file = os.path.join(base_folder, "ICLR_2025_Download_Report.csv")

def generate_report():
    if not os.path.exists(base_folder):
        print("No papers downloaded yet.")
        return

    with open(report_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Category", "Title", "File Path"])

        for category in ["Oral", "Spotlight", "Poster"]:
            cat_folder = os.path.join(base_folder, category)
            if not os.path.exists(cat_folder):
                continue
            for file in os.listdir(cat_folder):
                if file.endswith(".pdf"):
                    writer.writerow([category, file, os.path.join(cat_folder, file)])

    print(f"✅ Report generated: {report_file}")

if __name__ == "__main__":
    generate_report()
