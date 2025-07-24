import requests
import base64
import csv
import os
from difflib import SequenceMatcher
import pandas as pd

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def calculate_cer_details(gt, pred):
    matcher = SequenceMatcher(None, gt, pred)
    opcodes = matcher.get_opcodes()
    S = D = I = 0
    for tag, i1, i2, j1, j2 in opcodes:
        if tag == 'replace':
            S += max(i2 - i1, j2 - j1)
        elif tag == 'delete':
            D += i2 - i1
        elif tag == 'insert':
            I += j2 - j1
    N = len(gt)
    cer = round((S + D + I) / N, 3) if N > 0 else 1.0
    formula = f"CER = ({S} + {D} + {I}) / {N}"
    return cer, formula

# Path file ground truth dan direktori gambar
ground_truth_file =  r"C:\Users\IYO\OneDrive\Documents\Tugas_Semester_6\UAS\Computer_Vission\Plate_test\test\ground_truth.csv"
image_dir = r"C:\Users\IYO\OneDrive\Documents\Tugas_Semester_6\UAS\Computer_Vission\Plate_test\test"

# Baca file CSV ground truth
df = pd.read_csv(ground_truth_file)

# List untuk menyimpan hasil
results = []

# Proses tiap gambar
for index, row in df.iterrows():
    image_path = os.path.join(image_dir, row["image"])
    ground_truth = row["ground_truth"]

    try:
        image_base64 = encode_image_to_base64(image_path)
    except Exception as e:
        pred = f"ERROR: {e}"
        cer, formula = 1.0, "CER = (0 + 0 + 0) / 0"
        results.append([row["image"], ground_truth, pred, formula, cer])
        print(f"ERROR loading image {image_path}: {e}")
        continue

    payload = {
        "model": "llava-llama-3-8b-v1_1",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    },
                    {
                        "type": "text",
                        "text": "What is the license plate number shown in this image? Respond only with the plate number."
                    }
                ]
            }
        ],
        "stream": False
    }

    try:
        response = requests.post("http://localhost:1234/v1/chat/completions", json=payload)
        response.raise_for_status()
        pred = response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        pred = f"ERROR: {e}"

    cer, formula = calculate_cer_details(ground_truth, pred) if not pred.startswith("ERROR") else (1.0, "CER = (0 + 0 + 0) / 0")

    results.append([row["image"], ground_truth, pred, formula, cer])
    print(f"{row['image']} => GT: {ground_truth} | Pred: {pred} | {formula} | CER: {cer}")

# Simpan ke CSV
output_path = "hasil_prediksi.csv"
with open(output_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, quoting=csv.QUOTE_ALL)
    writer.writerow(["image", "ground_truth", "prediction", "CER_formula", "CER_score"])
    writer.writerows(results)

print(f"\nSemua prediksi selesai. Hasil disimpan di '{output_path}'")