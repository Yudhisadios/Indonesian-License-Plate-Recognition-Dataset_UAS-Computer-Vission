import os
import csv
import logging
from typing import List, Tuple

class PlateDatasetProcessor:
    def __init__(self, dataset_folder: str):
        self.dataset_folder = dataset_folder
        self.output_csv_path = os.path.join(dataset_folder, "ground_truth.csv")
        self.label_map = self._init_label_map()
        self.processed_data = []
        self.skipped_files = []

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(levelname)s: %(message)s"
        )

    def _init_label_map(self) -> dict:
        # Map angka 0–9
        label_map = {i: str(i) for i in range(10)}
        # Map huruf A–Z
        label_map.update({i + 10: chr(ord('A') + i) for i in range(26)})
        return label_map

    def process(self):
        files = os.listdir(self.dataset_folder)
        txt_files = [f for f in files if f.endswith(".txt")]

        logging.info(f"🔍 Ditemukan {len(txt_files)} file anotasi.")

        for txt_file in txt_files:
            txt_path = os.path.join(self.dataset_folder, txt_file)
            image_name = txt_file.replace(".txt", ".jpg")

            try:
                plate_chars = self._parse_annotation(txt_path)
                if not plate_chars:
                    raise ValueError("File kosong atau tidak valid")

                # Urutkan karakter dari kiri ke kanan
                plate_chars.sort(key=lambda x: x[0])
                plate_string = ''.join(char for _, char in plate_chars)

                self.processed_data.append([image_name, plate_string])

            except Exception as e:
                logging.warning(f"⚠️ Gagal memproses {txt_file}: {e}")
                self.skipped_files.append(txt_file)

        self._save_csv()

        # Statistik akhir
        logging.info(f"\n✅ Proses selesai:")
        logging.info(f"   - Sukses: {len(self.processed_data)} file")
        logging.info(f"   - Gagal : {len(self.skipped_files)} file")
        if self.skipped_files:
            logging.info(f"   - File gagal: {self.skipped_files}")

    def _parse_annotation(self, txt_path: str) -> List[Tuple[float, str]]:
        result = []
        with open(txt_path, "r", encoding="utf-8") as file:
            for line_num, line in enumerate(file, start=1):
                parts = line.strip().split()
                if len(parts) < 2:
                    logging.debug(f"  ⛔ Baris {line_num} kosong atau tidak lengkap: {line.strip()}")
                    continue
                try:
                    class_id = int(parts[0])
                    x_center = float(parts[1])
                    char = self.label_map.get(class_id)

                    if char is None:
                        raise KeyError(f"class_id {class_id} tidak dikenali")
                    result.append((x_center, char))
                except (ValueError, KeyError) as e:
                    logging.warning(f"  ⚠️ Error parsing di {os.path.basename(txt_path)} baris {line_num}: {e}")
        return result

    def _save_csv(self):
        with open(self.output_csv_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["image", "ground_truth"])
            writer.writerows(self.processed_data)
        logging.info(f"\n📁 File ground_truth.csv berhasil disimpan di:\n   {self.output_csv_path}")


# === MAIN ===
if __name__ == "__main__":
    dataset_path = r"C:\Users\IYO\OneDrive\Documents\Tugas_Semester_6\UAS\Computer_Vission\Plate_test\test"
  # <- ubah ke direktori datasetmu
    processor = PlateDatasetProcessor(dataset_path)
    processor.process()