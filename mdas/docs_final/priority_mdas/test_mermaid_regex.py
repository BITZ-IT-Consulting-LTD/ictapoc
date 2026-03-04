import re

tests = [
    "Start((Start))",
    "Trigger[\"Coordination Trigger\"]",
    "A[Get Details (System)]",
    "DocsGateway -- \"Yes\" --> VerifyBRS[Verify BRS]",
    "EndApprove((End - Approved))",
    "EndReject((End - Rejected))"
]

# We want to replace unquoted text inside node shapes.
# We'll match NodeID followed by shape brackets.
pattern = r'(?<!")(^\s*[A-Za-z0-9_]+|\s+[A-Za-z0-9_]+|-->\s*[A-Za-z0-9_]+)\s*(\(\(|\{\{|\[\[|\[\(|\(\[|\[/|\[\\|\[|\(|\{|>)([^"\]\)\}][^\n\]\)\}]*)(\)\)|\}\}|\]\]|\)\]|\]\)|/\]|\\\]|\]|\)|\})'

for t in tests:
    print(f"Original: {t}")
    
    def repl(m):
        pre = m.group(1)
        shape_open = m.group(2)
        txt = m.group(3).strip()
        shape_close = m.group(4)
        print(f"   MATCH! pre='{pre}' open='{shape_open}' txt='{txt}' close='{shape_close}'")
        return f'{pre}{shape_open}"{txt}"{shape_close}'
        
    print(f"Replaced: {re.sub(pattern, repl, t)}")
    print("-" * 30)

