"""命令行入口：职业教育课程“四能重构”方案生成器。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from four_capability_skill import CourseInput, build_ai_prompt, generate_scaffold, save_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="职业教育课程“四能重构”提示词与方案骨架生成器"
    )
    parser.add_argument(
        "input",
        help="课程输入JSON文件路径，例如 examples/robotics_basic.json",
    )
    parser.add_argument(
        "--mode",
        choices=["prompt", "scaffold"],
        default="prompt",
        help="prompt=生成AI提示词；scaffold=生成课程方案骨架",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="",
        help="输出文件路径；不填则打印到控制台",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)

    if not input_path.exists():
        print(f"输入文件不存在：{input_path}", file=sys.stderr)
        return 1

    course = CourseInput.from_json_file(input_path)
    if not course.course_name:
        print("输入JSON缺少 course_name 字段。", file=sys.stderr)
        return 1

    if args.mode == "prompt":
        text = build_ai_prompt(course)
    else:
        text = generate_scaffold(course)

    if args.output:
        save_text(args.output, text)
        print(f"已生成：{args.output}")
    else:
        print(text)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
