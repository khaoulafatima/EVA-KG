import os
import json

if __name__ == "__main__":
    json_path = "../../data/case_detail_json"
    single_value_list = []
    frequency_dict = {}
    for file in os.listdir(json_path):
        cd = json.load(open(json_path + "/" + file, encoding="UTF-8"))
        for key in cd.keys():
            if isinstance(cd[key], str):
                single_value_list.append(key)
                if key in frequency_dict.keys():
                    if cd[key] in frequency_dict[key].keys():
                        frequency_dict[key][cd[key]] += 1
                    else:
                        frequency_dict[key][cd[key]] = 1
                else:
                    frequency_dict[key] = {}
                    frequency_dict[key][cd[key]] = 1
            elif isinstance(cd[key], list):
                for value in cd[key]:
                    if key in frequency_dict.keys():
                        if value in frequency_dict[key].keys():
                            frequency_dict[key][value] += 1
                        else:
                            frequency_dict[key][value] = 1
                    else:
                        frequency_dict[key] = {}
                        frequency_dict[key][value] = 1

    frequency_dict = dict(sorted(frequency_dict.items(), key=lambda item: sum(item[1].values()), reverse=False))
    for key in frequency_dict.keys():
        frequency_dict[key] = dict(sorted(frequency_dict[key].items(), key=lambda item: item[1], reverse=True))

    save_path = "./case_detail_frequency.json"
    with open(save_path, "w", encoding="UTF-8") as f:
        json.dump(frequency_dict, f, ensure_ascii=False, indent=4)

    os.startfile(os.path.abspath(save_path))
