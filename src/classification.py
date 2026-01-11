from openai import OpenAI
import os

file_path = "data/file.tsv"
base_dir = "output"

def ask_openrouter(item1: str, item2: str, item3: str) -> str:
  client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="<YOURAPI_KEY>",
  )

  completion = client.chat.completions.create(
    extra_headers={
      "HTTP-Referer": "<YOUR_SITE_URL>",
      "X-Title": "<YOUR_SITE_NAME>",
    },
    extra_body={},
    model="meta-llama/llama-4-scout",
    messages=[
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": item1
          },
          {
            "type": "text",
            "text": item2
          },
          {
            "type": "text",
            "text": item3
          }
        ]
      }
    ]
  )
  
  return completion.choices[0].message.content

def prompt (item1: str, item2: str) -> str :
  response = ask_openrouter(
    """As a software engineer performing a code review, evaluate
        code_1 and code_2 indicating which version is
        better in terms of clarity, readability, and
        maintainability, and provide a concise justification.

        Can you rate whether code_1 is better than code_2?
        I would like to know if:
        1) Which code is easier to understand.
        2) Consider changes in naming, structure, or style.
        3) Which code is easier to maintain and extend.

        <output_format>
        Return using this schema:
        {{
            "winner": "code_1" | "code_2" | "tie",
            "reasons": [string, ...]
        }}
        </output_format>
    """,

    "Code 1:" + item1,
    "Code 2:" + item2,
  )

  return response

lines = []

with open(file_path, "r", encoding="utf-8") as file:
    for line in file:
        data = line.strip().split("\t")
        lines.append(data)

for i, line in enumerate(lines):
  if i != 0 and len(line) >= 5:
    col4 = line[3]
    col5 = line[4]

    folder = os.path.join(base_dir, str(i))
    os.makedirs(folder, exist_ok=True)

    for execution in range(1, 6):
      result = prompt(col4, col5)

      output_file = os.path.join(
        folder, f"resultado_{execution}.txt"
      )

      with open(output_file, "w", encoding="utf-8") as f:
        f.write(str(result))

      print(f"Folder {i} | Execution {execution} saved.")
