# from src.controller.IdentificationController import IdentificationController

# data = IdentificationController().load_data_image()


data = {'iqbal': 1,
        'baqi': 2,
        'muhammad': 3
        }

array_names = list(data)
array_value = list(data.values())

a, seen, result = array_value, set(), []
for idx, item in enumerate(a):
    if item not in seen:
        seen.add(item)          # First time seeing the element
    else:
        result.append(idx)      # Already seen, add the index to the result

if len(array_value) == len(result)+1:
    print('sama semua')
else:
    the_max = max(array_value)
    if result == []:
        print(array_names[array_value.index(the_max)])
    elif the_max <= array_value[result[0]]:
        print('ada yang sama')
    else:
        print(array_names[array_value.index(the_max)])


# duplicate = []
# for i in range(0, len(array_value)-1):
#     for j in range(i+1, len(array_value)):
#         pass
