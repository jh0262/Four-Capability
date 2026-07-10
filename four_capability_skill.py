"""Four-Capability Skill Generator

职业教育课程“四能重构”方案生成核心模块。

功能：
1. 将课程信息转换为高质量AI提示词；
2. 生成课程“四能重构”方案骨架；
3. 统一结构翻译、运动建模、过程求解、工程判断四类能力的输出格式。

本模块不依赖第三方包，便于在命令行、Streamlit网页、Codex或其他AI工作流中复用。
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


FOUR_CAPABILITIES = {
    "结构翻译能力": "把真实设备、工艺对象、任务场景或故障现象翻译成专业结构、变量参数、功能关系、图表、符号或模型。",
    "运动建模能力": "根据结构、任务和约束，建立可用于分析、计算、仿真、编程或控制的专业模型。",
    "过程求解能力": "按照“已知条件—目标结果—方法选择—分步实施—结果验证”的流程完成任务。",
    "工程判断能力": "判断方案、程序、模型或结果是否满足安全、精度、效率、稳定性、限位、碰撞、成本和工程可执行性要求。",
}

DEFAULT_OUTPUT_REQUIREMENTS = [
    "课程重构定位",
    "课程内容—四能映射表",
    "项目化教学方案",
    "任务链",
    "评价标准",
    "学习成果证据",
]


@dataclass
class CourseInput:
    """课程重构输入数据。"""

    course_name: str
    student_level: str = ""
    major: str = ""
    total_hours: str = ""
    course_contents: List[str] = field(default_factory=list)
    teaching_pain_points: str = ""
    training_conditions: List[str] = field(default_factory=list)
    job_tasks: List[str] = field(default_factory=list)
    project_count: str = "4个项目"
    output_requirements: List[str] = field(default_factory=lambda: DEFAULT_OUTPUT_REQUIREMENTS.copy())
    notes: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CourseInput":
        """从dict构造课程输入，自动兼容缺省字段。"""
        return cls(
            course_name=str(data.get("course_name", "")).strip(),
            student_level=str(data.get("student_level", "")).strip(),
            major=str(data.get("major", "")).strip(),
            total_hours=str(data.get("total_hours", "")).strip(),
            course_contents=_to_list(data.get("course_contents", [])),
            teaching_pain_points=str(data.get("teaching_pain_points", "")).strip(),
            training_conditions=_to_list(data.get("training_conditions", [])),
            job_tasks=_to_list(data.get("job_tasks", [])),
            project_count=str(data.get("project_count", "4个项目")).strip(),
            output_requirements=_to_list(data.get("output_requirements", DEFAULT_OUTPUT_REQUIREMENTS)),
            notes=str(data.get("notes", "")).strip(),
        )

    @classmethod
    def from_json_file(cls, path: str | Path) -> "CourseInput":
        with open(path, "r", encoding="utf-8") as f:
            return cls.from_dict(json.load(f))


def _to_list(value: Any) -> List[str]:
    """把字符串、列表、None统一转换为字符串列表。"""
    if value is None:
        return []
    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]
    if isinstance(value, str):
        lines = [line.strip(" -\t") for line in value.splitlines()]
        return [line for line in lines if line]
    return [str(value).strip()]


def _numbered(items: Iterable[str]) -> str:
    items = list(items)
    if not items:
        return "无"
    return "\n".join(f"{i + 1}. {item}" for i, item in enumerate(items))


def _bullets(items: Iterable[str]) -> str:
    items = list(items)
    if not items:
        return "- 无"
    return "\n".join(f"- {item}" for item in items)


def build_ai_prompt(course: CourseInput | Dict[str, Any]) -> str:
    """生成可直接提交给大模型的“四能重构”提示词。"""
    if isinstance(course, dict):
        course = CourseInput.from_dict(course)

    return f"""
你是一名职业教育课程重构专家，熟悉高职和应用型本科专业课程建设、项目化教学、岗课赛证融通、能力本位课程设计和工程技术类课程教学改革。

请依据“四能重构”框架，为以下课程设计能力培养方案。

## 四能框架

1. 结构翻译能力：{FOUR_CAPABILITIES['结构翻译能力']}
2. 运动建模能力：{FOUR_CAPABILITIES['运动建模能力']}
3. 过程求解能力：{FOUR_CAPABILITIES['过程求解能力']}
4. 工程判断能力：{FOUR_CAPABILITIES['工程判断能力']}

## 课程信息

【课程名称】
{course.course_name}

【授课对象】
{course.student_level}

【所属专业】
{course.major}

【总学时】
{course.total_hours}

【课程主要内容】
{_numbered(course.course_contents)}

【现有教学痛点】
{course.teaching_pain_points or '无'}

【实训条件】
{_bullets(course.training_conditions)}

【对应岗位或典型工作任务】
{_bullets(course.job_tasks)}

【希望重构成项目数量】
{course.project_count}

【输出要求】
{_bullets(course.output_requirements)}

【补充说明】
{course.notes or '无'}

## 请输出以下内容

一、课程重构定位
1. 分析课程原有特点；
2. 判断课程适合重点培养哪几类能力；
3. 给出课程“四能重构”的总主线。

二、课程内容—四能映射表
表头必须为：课程内容｜结构翻译能力｜运动建模能力｜过程求解能力｜工程判断能力｜建议教学任务。

三、项目化教学重构方案
根据课程内容设计若干个递进式项目。每个项目包括：项目名称、工程情境、对应知识点、对应技能点、四能培养目标、教学任务链、学生输出成果、教师指导重点、建议学时。

四、每个项目的四能培养设计
对每个项目分别设计：结构翻译任务、运动/过程/控制/工艺建模任务、过程求解任务、工程判断任务。

五、学习成果证据设计
设计学生需要提交的证据材料，例如：结构标注图、变量表、模型图、计算书、程序文件、仿真截图、调试记录、故障分析表、项目报告、展示视频等。

六、评价方案
设计过程性评价和终结性评价。评价指标必须对应四类能力。

七、教学实施建议
给出课堂组织方式、分组方式、教师引导问题、软件工具、实训设备、教学资源和难点突破建议。

八、课程重构总口号
给出一句能够用于教改申报书或课程建设汇报的总口号。

## 输出要求

1. 使用结构化Markdown；
2. 表格清晰；
3. 紧扣课程内容，不要空泛；
4. 每个项目必须体现“真实任务 → 专业模型 → 过程求解 → 工程判断”；
5. 语言适合用于课程标准、教学改革方案或人才培养方案。
""".strip()


def infer_project_count(project_count: str, fallback: int = 4) -> int:
    """从“4个项目”等文本中提取项目数量。"""
    digits = "".join(ch for ch in str(project_count) if ch.isdigit())
    if digits:
        return max(1, min(12, int(digits)))
    return fallback


def generate_scaffold(course: CourseInput | Dict[str, Any]) -> str:
    """生成一个可继续扩写的课程方案骨架。"""
    if isinstance(course, dict):
        course = CourseInput.from_dict(course)

    n_projects = infer_project_count(course.project_count)
    contents = course.course_contents or ["课程核心内容待补充"]

    mapping_rows = []
    for item in contents:
        mapping_rows.append(
            f"| {item} | 识别对象、部件、变量与约束 | 建立分析/控制/工艺/仿真模型 | 按任务流程完成计算、设计、编程或调试 | 判断安全、精度、效率、稳定性与可执行性 | 围绕“{item}”设计真实任务 |"
        )

    project_sections = []
    for i in range(1, n_projects + 1):
        related = contents[(i - 1) % len(contents)]
        project_sections.append(
            f"""
### 项目{i}：围绕“{related}”的任务化学习项目

| 项目要素 | 设计内容 |
|---|---|
| 工程情境 | 从岗位任务或典型设备中选取与“{related}”相关的真实任务。 |
| 对应知识点 | {related} |
| 对应技能点 | 识别对象、建立模型、分步实施、工程验证。 |
| 建议学时 | 待依据课程总学时细化。 |

#### 1. 结构翻译任务
- 识别任务对象、组成部件、输入输出、变量参数和约束条件。
- 形成结构标注图、变量表或任务对象分析表。

#### 2. 运动/过程/控制/工艺建模任务
- 将真实任务转化为可分析、可计算、可编程或可仿真的专业模型。
- 形成模型图、流程图、数学表达、I/O表、程序框架或仿真模型。

#### 3. 过程求解任务
- 按“已知条件—目标结果—方法选择—分步实施—结果验证”的流程完成任务。
- 形成计算书、程序文件、调试记录、仿真截图或任务报告。

#### 4. 工程判断任务
- 检查方案是否满足安全、精度、效率、稳定性、成本、节拍、限位、干涉或可维护性要求。
- 形成可行性判断表、风险分析表或优化建议。
""".strip()
        )

    return f"""
# {course.course_name}：“四能重构”课程方案骨架

## 一、课程重构定位

- **授课对象**：{course.student_level or '待补充'}
- **所属专业**：{course.major or '待补充'}
- **总学时**：{course.total_hours or '待补充'}
- **课程主线**：真实任务输入 → 结构翻译 → 模型建立 → 过程求解 → 工程判断 → 能力输出。
- **重构目标**：将课程从“知识点讲授”转向“真实任务驱动的四能贯通培养”。

## 二、课程内容—四能映射表

| 课程内容 | 结构翻译能力 | 运动建模能力 | 过程求解能力 | 工程判断能力 | 建议教学任务 |
|---|---|---|---|---|---|
{chr(10).join(mapping_rows)}

## 三、项目化教学重构方案

{chr(10).join(project_sections)}

## 四、学习成果证据设计

| 能力维度 | 学习成果证据 |
|---|---|
| 结构翻译能力 | 结构标注图、变量参数表、任务对象分析表、接口关系图 |
| 运动建模能力 | 模型图、计算模型、控制流程图、I/O表、仿真模型 |
| 过程求解能力 | 计算书、程序文件、调试记录、仿真截图、过程报告 |
| 工程判断能力 | 可达性/安全性/精度/效率判断表、故障分析表、优化建议 |

## 五、评价量规建议

| 评价指标 | 权重 | 评价要点 |
|---|---:|---|
| 结构翻译能力 | 25% | 能否准确识别对象、部件、变量、接口与约束 |
| 运动建模能力 | 25% | 能否建立正确、可用、可验证的专业模型 |
| 过程求解能力 | 25% | 能否按标准流程完成计算、设计、编程、调试或仿真 |
| 工程判断能力 | 25% | 能否判断结果的安全性、可行性、精度、效率和工程适用性 |

## 六、教学实施建议

1. 每个项目先给真实设备、任务图片、工艺视频或故障场景，再引导学生进行结构翻译。
2. 每次计算、编程或仿真前，要求学生先提交“已知量—未知量—模型—流程”任务单。
3. 每个项目结束时，必须进行“结果验证”和“工程判断”，避免只看结果不看可执行性。
4. 建议采用小组协作：结构识别员、建模员、求解员、验证员、汇报员。

## 七、课程重构口号

> 从“会听会算”转向“会看、会建、会解、会判”。
""".strip()


def load_json(path: str | Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_text(path: str | Path, text: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
