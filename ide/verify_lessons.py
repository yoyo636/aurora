#!/usr/bin/env python3
"""Aurora 教学工坊 · 端到端课程验证脚本

用法:
    python3 verify_lessons.py            # 需先启动 server(python3 server.py)
    python3 verify_lessons.py http://127.0.0.1:8697

对每节课:
  1) 运行 示例代码(带所需 stdin)→ 必须无错误
  2) 用 练习参考答案 调 /api/verify → 必须 pass
打印每课结果,任一失败时退出码为 1。
"""

import json
import sys
import urllib.request

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8697"

# 需要键盘输入的课程:示例 vs 练习分开给(按行,每行一个输入)
EX_STDIN = {"l02_vars_input": "Aurora\n10\n170.5"}
SOL_STDIN = {"l02_vars_input": "10\n4"}


def post(path, body):
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
    )
    return json.loads(urllib.request.urlopen(req).read())


def get(path):
    return json.loads(urllib.request.urlopen(BASE + path).read())


def main():
    lessons = get("/api/lessons")["lessons"]
    print(f"共 {len(lessons)} 节课,开始验证…\n")
    all_ok = True
    for lesson in lessons:
        ex = lesson.get("exercise") or {}
        run = post("/api/run", {
            "code": lesson["example"],
            "stdin": EX_STDIN.get(lesson["id"], ""),
        })
        ok_ex = not run.get("errors")
        verify = post("/api/verify", {
            "lesson_id": lesson["id"],
            "code": ex.get("solution", ""),
            "stdin": SOL_STDIN.get(lesson["id"], ""),
        })
        ok_sol = bool(verify.get("pass"))
        if not (ok_ex and ok_sol):
            all_ok = False
        print(f"[{'OK' if ok_ex else 'FAIL'}] 示例  "
              f"[{'OK' if ok_sol else 'FAIL'}] 练习  {lesson['id']}  {lesson['title']}")
        if not ok_ex:
            print("   示例错误:", run["errors"])
        if not ok_sol:
            print("   验证失败: expected=", verify.get("expected"),
                  " actual=", verify.get("actual"), " errors=", verify.get("errors"))
    print("\n" + ("全部课程通过 ✓" if all_ok else "存在失败课程 ✗"))
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
