import csv

class ReflectionAgent:
    def __init__(self, file_path):
        self.nodes = {}
        self.children = {}
        self.state = {
            "answers": {},
            "axis": {
                "axis1": {"internal": 0, "external": 0},
                "axis2": {"contribution": 0, "entitlement": 0},
                "axis3": {"wide": 0, "narrow": 0}
            }
        }
        self.load_tree(file_path)

    def load_tree(self, file_path):
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                self.nodes[row["id"]] = row
                parent = row["parentId"]
                if parent:
                    self.children.setdefault(parent, []).append(row["id"])

    def get_next(self, node_id):
        return self.children.get(node_id, [None])[0]

    def apply_signal(self, signal):
        if not signal:
            return
        axis, value = signal.split(":")
        if axis in self.state["axis"]:
            self.state["axis"][axis][value] += 1

    def dominant(self, axis):
        return max(self.state["axis"][axis], key=self.state["axis"][axis].get)

    def interpolate(self, text):
        for k, v in self.state["answers"].items():
            text = text.replace(f"{{{k}.answer}}", v)
        text = text.replace("{axis1.dominant}", self.dominant("axis1"))
        text = text.replace("{axis2.dominant}", self.dominant("axis2"))
        text = text.replace("{axis3.dominant}", self.dominant("axis3"))
        return text

    def run(self):
        current = "START"
        while current:
            node = self.nodes[current]
            t = node["type"]

            if t == "start":
                print("\n" + node["text"])
                current = self.get_next(current)

            elif t == "question":
                print("\n" + node["text"])
                options = node["options"].split("|")
                for i, opt in enumerate(options):
                    print(f"{i+1}. {opt}")
                choice = int(input("Choose: ")) - 1
                answer = options[choice]
                self.state["answers"][current] = answer
                self.apply_signal(node["signal"])
                current = self.get_next(current)

            elif t == "decision":
                prev = list(self.state["answers"].values())[-1]
                rules = node["options"].split(";")
                for rule in rules:
                    cond, target = rule.split(":")
                    values = cond.split("=")[1].split("|")
                    if prev in values:
                        current = target
                        break

            elif t == "reflection":
                print("\n" + node["text"])
                input("Press Enter...")
                self.apply_signal(node["signal"])
                current = self.get_next(current)

            elif t == "bridge":
                print("\n" + node["text"])
                current = node["target"]

            elif t == "summary":
                print("\n--- SUMMARY ---")
                print(self.interpolate(node["text"]))
                current = self.get_next(current)

            elif t == "end":
                print("\n" + node["text"])
                break


if __name__ == "__main__":
    agent = ReflectionAgent("../tree/reflection-tree.tsv")
    agent.run()
