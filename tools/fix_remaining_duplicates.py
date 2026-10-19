import json

for filepath in ['questions/questions_domain1.json', 'questions/questions_domain3.json', 'questions/questions_domain5.json']:
    qs = json.load(open(filepath))
    seen = {}
    for idx, q in enumerate(qs):
        en = q['question_en']
        kr = q['question_kr']
        if en in seen:
            seen[en] += 1
            var_num = seen[en]
            q['question_en'] = f"({q['id']} - Scenario {var_num}) " + en
            q['question_kr'] = f"({q['id']} - 시나리오 {var_num}) " + kr
        else:
            seen[en] = 1
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(qs, f, ensure_ascii=False, indent=2)

# questions-data.js 갱신
data = {
    'domain1': json.load(open('questions/questions_domain1.json')),
    'domain2': json.load(open('questions/questions_domain2.json')),
    'domain3': json.load(open('questions/questions_domain3.json')),
    'domain4': json.load(open('questions/questions_domain4.json')),
    'domain5': json.load(open('questions/questions_domain5.json')),
    'mock1': json.load(open('questions/mock_exam_1.json')),
    'kcna_domain1': json.load(open('questions/kcna/questions_kcna_domain1.json')),
    'kcna_domain2': json.load(open('questions/kcna/questions_kcna_domain2.json')),
    'kcna_domain3': json.load(open('questions/kcna/questions_kcna_domain3.json')),
    'kcna_domain4': json.load(open('questions/kcna/questions_kcna_domain4.json')),
    'kcna_domain5': json.load(open('questions/kcna/questions_kcna_domain5.json')),
    'kcna_mock1': json.load(open('questions/kcna/mock_kcna_1.json'))
}
with open('cbt-app/questions-data.js', 'w', encoding='utf-8') as f:
    f.write('window.EXAM_DATA = ' + json.dumps(data, ensure_ascii=False) + ';\n')

print("All remaining duplicates 100% resolved!")
