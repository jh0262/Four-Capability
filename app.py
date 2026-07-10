"""Streamlit网页工具：课程“四能重构”助手。

启动：
    streamlit run app.py
"""

from __future__ import annotations

import json

import streamlit as st

from four_capability_skill import CourseInput, build_ai_prompt, generate_scaffold


DEFAULT_DATA = {
    "course_name": "机器人技术基础",
    "student_level": "高职工业机器人技术专业二年级学生",
    "major": "工业机器人技术",
    "total_hours": "48学时",
    "course_contents": [
        "机器人结构组成",
        "关节与自由度",
        "坐标系与位姿描述",
        "正运动学",
        "逆运动学",
        "轨迹规划",
        "工业机器人编程基础",
    ],
    "teaching_pain_points": "学生会背公式，但不会从机器人结构图建立运动模型；会操作软件，但不理解结构与运动之间的关系。",
    "training_conditions": ["ABB工业机器人", "RobotStudio", "MATLAB", "Yalong数字孪生平台", "工业机器人实训站"],
    "job_tasks": ["工业机器人操作与运维", "机器人工作站调试", "机器人轨迹编程", "机器人搬运与装配任务"],
    "project_count": "4个项目",
    "output_requirements": ["课程四能映射表", "项目化教学方案", "任务链", "评价标准", "学习成果证据"],
}


st.set_page_config(page_title="四能重构助手", page_icon="🧩", layout="wide")
st.title("职业教育课程“四能重构”助手")
st.caption("结构翻译能力｜运动建模能力｜过程求解能力｜工程判断能力")

with st.sidebar:
    st.header("使用方式")
    mode = st.radio("输出模式", ["AI提示词", "方案骨架"], index=0)
    st.markdown(
        """
        1. 在左侧或JSON区填写课程信息；
        2. 点击生成；
        3. 将AI提示词复制给大模型，或下载方案骨架继续修改。
        """
    )

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("表单输入")
    course_name = st.text_input("课程名称", DEFAULT_DATA["course_name"])
    student_level = st.text_input("授课对象", DEFAULT_DATA["student_level"])
    major = st.text_input("所属专业", DEFAULT_DATA["major"])
    total_hours = st.text_input("总学时", DEFAULT_DATA["total_hours"])
    project_count = st.text_input("项目数量", DEFAULT_DATA["project_count"])
    teaching_pain_points = st.text_area("教学痛点", DEFAULT_DATA["teaching_pain_points"], height=100)
    course_contents = st.text_area("课程主要内容（一行一项）", "\n".join(DEFAULT_DATA["course_contents"]), height=150)
    training_conditions = st.text_area("实训条件（一行一项）", "\n".join(DEFAULT_DATA["training_conditions"]), height=100)
    job_tasks = st.text_area("岗位任务（一行一项）", "\n".join(DEFAULT_DATA["job_tasks"]), height=100)

with col2:
    st.subheader("JSON输入/导入")
    json_text = st.text_area(
        "可直接粘贴JSON覆盖表单输入；为空则使用左侧表单。",
        "",
        height=430,
        placeholder=json.dumps(DEFAULT_DATA, ensure_ascii=False, indent=2),
    )


def form_to_data() -> dict:
    return {
        "course_name": course_name,
        "student_level": student_level,
        "major": major,
        "total_hours": total_hours,
        "course_contents": course_contents.splitlines(),
        "teaching_pain_points": teaching_pain_points,
        "training_conditions": training_conditions.splitlines(),
        "job_tasks": job_tasks.splitlines(),
        "project_count": project_count,
        "output_requirements": DEFAULT_DATA["output_requirements"],
    }


if st.button("生成", type="primary"):
    try:
        data = json.loads(json_text) if json_text.strip() else form_to_data()
        course = CourseInput.from_dict(data)
        if not course.course_name:
            st.error("课程名称不能为空。")
            st.stop()

        result = build_ai_prompt(course) if mode == "AI提示词" else generate_scaffold(course)
        st.subheader("生成结果")
        st.text_area("结果内容", result, height=600)
        st.download_button(
            "下载Markdown文件",
            data=result.encode("utf-8"),
            file_name="four_capability_result.md",
            mime="text/markdown",
        )
    except json.JSONDecodeError as exc:
        st.error(f"JSON格式错误：{exc}")
    except Exception as exc:  # noqa: BLE001
        st.error(f"生成失败：{exc}")
