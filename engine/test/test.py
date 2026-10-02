import subprocess


def send(cmd):
    engine.stdin.write(cmd + "\n")
    engine.stdin.flush()


def get(answer):
    line = engine.stdout.readline().strip()
    return line == answer


print("\n--- Running: Engine Test ---\n")
engine = subprocess.Popen(
    ["../../build/engine"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True,
    bufsize=1,
)
send("uci")
while get("uciok") == False:
    pass

depth = 1
failure_count = 0
with open("test_data/perft.epd", "r", encoding="utf-8") as testfile:
    for index, line in enumerate(testfile):
        tokens = line.split(";")
        fen = tokens.pop(0)
        send("position fen " + fen + " moves")
        tokens = "".join(tokens).split()
        answer = int(tokens[1 + tokens.index(f"D{depth}")])
        send(f"go perft {depth}")
        if get(f"nodes {answer}") == False:
            failure_count += 1
if failure_count > 0:
    print(f"{failure_count} failures")
else:
    print("success")

try:
    send("quit")
    engine.wait(timeout=5)
except subprocess.TimeoutExpired:
    engine.kill()
    engine.wait()
