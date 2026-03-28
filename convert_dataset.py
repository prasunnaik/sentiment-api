import bz2
import csv

input_file = "data/train.ft.txt.bz2"
output_file = "data/train.csv"

with bz2.open(input_file, 'rt', encoding='utf-8') as f, \
     open(output_file, 'w', newline='', encoding='utf-8') as out:

    writer = csv.writer(out)
    writer.writerow(["text", "label"])

    for i, line in enumerate(f):
        try:
            label, text = line.split(" ", 1)

            if label == "__label__2":
                label = "positive"
            else:
                label = "negative"

            writer.writerow([text.strip(), label])

        except:
            continue

        # limit for speed
        if i >= 50000:
            break

print("✅ train.csv created successfully!")