from src.model.General import General


DB = General()

raw = DB.select("SELECT * FROM dataset_image")

print(raw)