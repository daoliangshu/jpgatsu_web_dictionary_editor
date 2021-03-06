import csv

from db_editor.models import DictionaryEntry

print('before')
with open("./table_to_import.csv") as f:
    print('entered')
    reader = csv.reader(f)
    # print("start1")
    # my_count = 0
    for row in reader:
        # print(my_count)
        #my_count = my_count + 1
        for i in range(0, len(row)):
            if row[i].strip() == "":
                row[i] = None
        created = DictionaryEntry.objects.get_or_create(
            entry_id=row[0],
            jp_1=row[1],
            jp_2=row[2],
            zh_1=row[3],
            lesson=row[4],
            fr_1=row[5],
            fr_2=row[6],
            thematic=row[7],
            en_1=row[8],
            lv=row[9]
        )
