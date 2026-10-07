"""
Landing and Learning Page for Python Code Visualizer.
Phase 13: Educational layer explaining Python execution concepts.
"""

import streamlit as st


def render_landing_page():
    """Renders the comprehensive, long-scrollable Python learning guide."""

    landing_css = """
    <style>
        html {
            scroll-behavior: smooth;
        }

        /* Sticky Navigation Bar */
        .edu-sticky-nav {
            position: sticky;
            top: 0;
            z-index: 9999;
            background: rgba(24, 24, 37, 0.95);
            backdrop-filter: blur(10px);
            border: 1px solid #313244;
            border-radius: 8px;
            padding: 12px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
            width: 100%;
            box-sizing: border-box;
        }

        .edu-nav-brand {
            font-size: 1.15rem;
            font-weight: 700;
            color: #89b4fa;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .edu-nav-links {
            display: flex;
            align-items: center;
            gap: 20px;
            flex-wrap: wrap;
        }

        .edu-nav-link {
            color: #cdd6f4;
            text-decoration: none;
            font-size: 0.92rem;
            font-weight: 500;
            transition: color 0.2s ease;
            padding: 4px 8px;
            border-radius: 4px;
        }

        .edu-nav-link:hover {
            color: #89dceb;
            background: #313244;
        }

        .edu-nav-cta {
            background-color: #89b4fa;
            color: #11111b !important;
            font-weight: 700;
            padding: 6px 14px;
            border-radius: 6px;
            transition: all 0.2s ease;
        }

        .edu-nav-cta:hover {
            background-color: #b4befe;
            transform: translateY(-1px);
        }

        /* Hero Section */
        .edu-hero {
            background: linear-gradient(180deg, rgba(30, 30, 46, 0.8) 0%, rgba(24, 24, 37, 0.4) 100%);
            border: 1px solid #313244;
            border-radius: 12px;
            padding: 48px 36px;
            text-align: center;
            margin-bottom: 40px;
        }

        .edu-hero-title {
            font-size: 2.8rem;
            font-weight: 800;
            color: #cdd6f4;
            margin-bottom: 12px;
            letter-spacing: -0.5px;
        }

        .edu-hero-subtitle {
            font-size: 1.35rem;
            color: #89dceb;
            font-weight: 600;
            margin-bottom: 16px;
        }

        .edu-hero-text {
            font-size: 1.05rem;
            color: #a6adc8;
            max-width: 780px;
            margin: 0 auto 28px auto;
            line-height: 1.6;
        }

        .edu-hero-buttons {
            display: flex;
            justify-content: center;
            gap: 16px;
            flex-wrap: wrap;
        }

        .edu-btn-primary {
            display: inline-block;
            background-color: #89b4fa;
            color: #11111b !important;
            font-weight: 700;
            font-size: 1.05rem;
            padding: 12px 26px;
            border-radius: 8px;
            text-decoration: none;
            transition: all 0.2s ease;
            box-shadow: 0 4px 12px rgba(137, 180, 250, 0.25);
        }

        .edu-btn-primary:hover {
            background-color: #b4befe;
            transform: translateY(-2px);
        }

        .edu-btn-secondary {
            display: inline-block;
            background-color: #313244;
            color: #cdd6f4 !important;
            font-weight: 600;
            font-size: 1.05rem;
            padding: 12px 24px;
            border-radius: 8px;
            border: 1px solid #45475a;
            text-decoration: none;
            transition: all 0.2s ease;
        }

        .edu-btn-secondary:hover {
            background-color: #45475a;
            color: #ffffff !important;
            transform: translateY(-2px);
        }

        /* Section Cards & Layout */
        .edu-section {
            background-color: #181825;
            border: 1px solid #313244;
            border-radius: 10px;
            padding: 32px 28px;
            margin-bottom: 32px;
        }

        .edu-section-tag {
            display: inline-block;
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            padding: 3px 8px;
            border-radius: 4px;
            margin-bottom: 8px;
        }

        .tag-blue { background: #313244; color: #89b4fa; }
        .tag-purple { background: #313244; color: #cba6f7; }
        .tag-green { background: #313244; color: #a6e3a1; }
        .tag-yellow { background: #313244; color: #f9e2af; }

        .edu-section-title {
            font-size: 1.6rem;
            font-weight: 700;
            color: #cdd6f4;
            margin-bottom: 12px;
        }

        .edu-section-p {
            font-size: 1rem;
            color: #bac2de;
            line-height: 1.65;
            margin-bottom: 18px;
        }

        /* Diagram Elements */
        .edu-diagram-box {
            background: #11111b;
            border: 1px solid #313244;
            border-radius: 8px;
            padding: 20px;
            margin: 18px 0;
            overflow-x: auto;
        }

        .flow-row {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            flex-wrap: wrap;
            margin: 10px 0;
        }

        .flow-pill {
            background: #1e1e2e;
            border: 1px solid #45475a;
            color: #cdd6f4;
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.95rem;
            text-align: center;
        }

        .flow-pill-highlight {
            background: #313244;
            border: 1px solid #89b4fa;
            color: #89b4fa;
        }

        .flow-pill-green {
            background: #182822;
            border: 1px solid #a6e3a1;
            color: #a6e3a1;
        }

        .flow-pill-purple {
            background: #251b33;
            border: 1px solid #cba6f7;
            color: #cba6f7;
        }

        .flow-arrow-h {
            color: #6c7086;
            font-size: 1.2rem;
            font-weight: bold;
        }

        .flow-arrow-v {
            color: #6c7086;
            font-size: 1.2rem;
            font-weight: bold;
            text-align: center;
            margin: 4px 0;
        }

        .flow-col {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
        }

        /* Educational Disclaimer Card */
        .edu-disclaimer-card {
            background-color: #242220;
            border-left: 4px solid #f9e2af;
            border-radius: 6px;
            padding: 16px 20px;
            margin: 18px 0;
        }

        .edu-disclaimer-header {
            font-weight: 700;
            font-size: 1.05rem;
            color: #f9e2af;
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .edu-disclaimer-text {
            font-size: 0.92rem;
            color: #cdd6f4;
            line-height: 1.55;
            margin-bottom: 10px;
        }

        /* Official Documentation Links */
        .edu-doc-link {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: #1e1e2e;
            border: 1px solid #45475a;
            color: #89b4fa !important;
            padding: 6px 14px;
            border-radius: 6px;
            font-size: 0.88rem;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.2s ease;
            margin-top: 6px;
        }

        .edu-doc-link:hover {
            background: #313244;
            border-color: #89b4fa;
            transform: translateX(3px);
        }

        /* Grid for Cards */
        .edu-grid-3 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 16px;
            margin: 18px 0;
        }

        .edu-subcard {
            background: #11111b;
            border: 1px solid #313244;
            border-radius: 8px;
            padding: 18px;
        }

        .edu-subcard-title {
            font-weight: 700;
            font-size: 1rem;
            color: #89dceb;
            margin-bottom: 8px;
        }

        .edu-subcard-desc {
            font-size: 0.9rem;
            color: #a6adc8;
            line-height: 1.5;
        }

        /* Feature Checklist */
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 12px;
            margin: 18px 0;
        }

        .feature-item {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            background: #11111b;
            border: 1px solid #313244;
            padding: 12px 16px;
            border-radius: 6px;
            font-size: 0.93rem;
            color: #cdd6f4;
        }

        .feature-check {
            color: #a6e3a1;
            font-weight: bold;
        }

        .not-feature-item {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            background: #1a1618;
            border: 1px solid #49262b;
            padding: 12px 16px;
            border-radius: 6px;
            font-size: 0.93rem;
            color: #f38ba8;
        }

        /* Callout / Final Hero */
        .edu-final-cta {
            background: linear-gradient(180deg, #181825 0%, #1e1e2e 100%);
            border: 1px solid #45475a;
            border-radius: 12px;
            padding: 40px 32px;
            text-align: center;
            margin: 40px 0 20px 0;
        }
    </style>
    """

    st.markdown(landing_css, unsafe_allow_html=True)

    # 1. Sticky Navigation Bar
    st.markdown("""
    <nav class="edu-sticky-nav">
        <a href="#hero" class="edu-nav-brand">🐍 Python Code Visualizer</a>
        <div class="edu-nav-links">
            <a href="#basics" class="edu-nav-link">Basics</a>
            <a href="#execution" class="edu-nav-link">Python Execution</a>
            <a href="#memory" class="edu-nav-link">Runtime Memory</a>
            <a href="#connects" class="edu-nav-link">Connection</a>
            <a href="#visualizer" class="edu-nav-cta">▶ Visualizer</a>
        </div>
    </nav>
    """, unsafe_allow_html=True)

    # 2. Hero Section
    st.markdown("""
    <div id="hero" class="edu-hero">
        <div class="edu-hero-title">🐍 Python Code Visualizer</div>
        <div class="edu-hero-subtitle">See what happens when your Python code runs.</div>
        <div class="edu-hero-text">
            Learn Python execution by watching code move through execution events, frames,
            variables, references, objects, and output.
        </div>
        <div class="edu-hero-buttons">
            <a href="#visualizer" class="edu-btn-primary">▶ Start Visualizing</a>
            <a href="#basics" class="edu-btn-secondary">↓ Learn How Python Runs</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3. Section — What is a Computer?
    st.markdown("""
    <div id="basics" class="edu-section">
        <span class="edu-section-tag tag-blue">Basics · Step 1</span>
        <div class="edu-section-title">What is a Computer?</div>
        <div class="edu-section-p">
            At its core, a computer is a machine that processes information. It takes inputs, performs computational
            instructions upon them, and delivers outputs.
        </div>
        <div class="edu-diagram-box">
            <div class="flow-row">
                <div class="flow-pill flow-pill-highlight">INPUT</div>
                <div class="flow-arrow-h">→</div>
                <div class="flow-pill flow-pill-highlight">PROCESSING</div>
                <div class="flow-arrow-h">→</div>
                <div class="flow-pill flow-pill-highlight">OUTPUT</div>
            </div>
        </div>
        <div class="edu-grid-3">
            <div class="edu-subcard">
                <div class="edu-subcard-title">⚡ CPU</div>
                <div class="edu-subcard-desc">The Central Processing Unit performs the physical calculations and executes underlying machine instructions.</div>
            </div>
            <div class="edu-subcard">
                <div class="edu-subcard-title">🧠 Memory (RAM)</div>
                <div class="edu-subcard-desc">Fast, temporary working space where actively running programs, variables, and objects reside.</div>
            </div>
            <div class="edu-subcard">
                <div class="edu-subcard-title">💾 Storage</div>
                <div class="edu-subcard-desc">Persistent long-term storage (SSD/HDD) where files and Python source code are saved when not running.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4. Section — Why do we Program?
    st.markdown("""
    <div class="edu-section">
        <span class="edu-section-tag tag-blue">Basics · Step 2</span>
        <div class="edu-section-title">Why do we Program?</div>
        <div class="edu-section-p">
            Computers cannot solve human problems on their own. Programming is the process of translating a problem
            into a structured sequence of unambiguous instructions that a computer can execute to produce a desired result.
        </div>
        <div class="edu-diagram-box">
            <div class="flow-row">
                <div class="flow-pill">Problem</div>
                <div class="flow-arrow-h">→</div>
                <div class="flow-pill">Instructions</div>
                <div class="flow-arrow-h">→</div>
                <div class="flow-pill flow-pill-highlight">Program</div>
                <div class="flow-arrow-h">→</div>
                <div class="flow-pill">Computer</div>
                <div class="flow-arrow-h">→</div>
                <div class="flow-pill flow-pill-green">Result</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 5. Section — What is a Program?
    st.markdown("""
    <div class="edu-section">
        <span class="edu-section-tag tag-blue">Basics · Step 3</span>
        <div class="edu-section-title">What is a Program?</div>
        <div class="edu-section-p">
            A program is not merely text stored in a file. It is a carefully coordinated structure comprising:
            <strong>Instructions</strong> (actions to perform), <strong>Data</strong> (information being processed),
            <strong>Logic</strong> (decisions and control flow), and <strong>Operations</strong> (manipulations of data).
        </div>
        <div class="edu-diagram-box">
            <p style="color: #a6adc8; margin-bottom: 8px; font-size: 0.9rem;">Consider this Python program:</p>
            <pre style="background: #181825; padding: 12px; border-radius: 6px; border: 1px solid #313244; color: #f9e2af; margin: 0; font-family: monospace;">a = 10
b = 20
c = a + b
print(c)</pre>
        </div>
        <div class="edu-section-p">
            This source code is a sequence of instructions telling Python to create objects, bind variable names to them,
            compute an addition operation, and emit standard output.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 6. Section — What Happens When Python Code Runs?
    st.markdown("""
    <div id="execution" class="edu-section">
        <span class="edu-section-tag tag-purple">Python Execution · Step 4</span>
        <div class="edu-section-title">What Happens When Python Runs?</div>
        <div class="edu-section-p">
            Learners typically see only a fraction of the story:
        </div>
        <div class="edu-diagram-box">
            <div class="flow-row">
                <div class="flow-pill">WRITE CODE</div>
                <div class="flow-arrow-h">→</div>
                <div class="flow-pill">RUN</div>
                <div class="flow-arrow-h">→</div>
                <div class="flow-pill flow-pill-green">OUTPUT: 30</div>
            </div>
        </div>
        <div class="edu-section-p">
            However, beneath the surface, Python executes a series of conceptual stages:
        </div>
        <div class="edu-diagram-box">
            <div class="flow-col">
                <div class="flow-pill flow-pill-highlight">Python Source Code</div>
                <div class="flow-arrow-v">↓</div>
                <div class="flow-pill">Python Handles the Code (Parsing & Bytecode)</div>
                <div class="flow-arrow-v">↓</div>
                <div class="flow-pill flow-pill-purple">Execution Contexts & Frames</div>
                <div class="flow-arrow-v">↓</div>
                <div class="flow-pill">Variables / Name Bindings</div>
                <div class="flow-arrow-v">↓</div>
                <div class="flow-pill flow-pill-green">Heap Objects (Values & Attributes)</div>
                <div class="flow-arrow-v">↓</div>
                <div class="flow-pill flow-pill-green">Program Output</div>
            </div>
        </div>
        <div class="edu-section-p">
            The Python Code Visualizer makes these hidden execution concepts observable step by step.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 7. Section — How Does Python Handle the Code?
    st.markdown("""
    <div class="edu-section">
        <span class="edu-section-tag tag-purple">Python Execution · Step 5</span>
        <div class="edu-section-title">How Does Python Handle the Code?</div>
        <div class="edu-section-p">
            Python does <strong>not</strong> send raw source code directly to the physical CPU. Instead, it processes your code
            through its execution pipeline:
        </div>
        <div class="edu-diagram-box">
            <div class="flow-row">
                <div class="flow-pill">Source Code</div>
                <div class="flow-arrow-h">→</div>
                <div class="flow-pill">Parsing</div>
                <div class="flow-arrow-h">→</div>
                <div class="flow-pill">Compilation</div>
                <div class="flow-arrow-h">→</div>
                <div class="flow-pill flow-pill-highlight">Bytecode (.pyc)</div>
                <div class="flow-arrow-h">→</div>
                <div class="flow-pill flow-pill-purple">Python Virtual Machine / Runtime</div>
                <div class="flow-arrow-h">→</div>
                <div class="flow-pill">Underlying Machine Execution</div>
                <div class="flow-arrow-h">→</div>
                <div class="flow-pill flow-pill-green">Result</div>
            </div>
        </div>
        <div class="edu-section-p">
            Python compiles source statements into internal bytecode instructions, which the Python runtime interpreter
            then executes one by one.
        </div>
        <a href="https://docs.python.org/3/tutorial/interpreter.html" target="_blank" rel="noopener noreferrer" class="edu-doc-link">
            📖 Learn more — Python Official Docs: The Python Interpreter ↗
        </a>
    </div>
    """, unsafe_allow_html=True)

    # 8. Section — Where Does the CPU Come In?
    st.markdown("""
    <div class="edu-section">
        <span class="edu-section-tag tag-purple">Python Execution · Step 6</span>
        <div class="edu-section-title">Where Does the CPU Come In?</div>
        <div class="edu-section-p">
            The CPU is the hardware processor carrying out low-level machine instructions. The Python runtime acts as a high-level manager
            between your Python code and the machine:
        </div>
        <div class="edu-diagram-box">
            <div class="flow-row">
                <div class="flow-pill">Python Code</div>
                <div class="flow-arrow-h">→</div>
                <div class="flow-pill flow-pill-purple">Python Runtime</div>
                <div class="flow-arrow-h">→</div>
                <div class="flow-pill">Bytecode Evaluation</div>
                <div class="flow-arrow-h">→</div>
                <div class="flow-pill">Underlying Machine Work</div>
                <div class="flow-arrow-h">→</div>
                <div class="flow-pill flow-pill-highlight">Physical CPU</div>
            </div>
        </div>
        <div class="edu-section-p">
            <strong>Important note:</strong> This tool is a <em>Python execution visualizer</em>, not a hardware CPU instruction visualizer.
            It teaches how Python conceives of execution frames, variable references, and objects.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 9. Section — What is an Object?
    st.markdown("""
    <div id="memory" class="edu-section">
        <span class="edu-section-tag tag-green">Runtime Memory · Step 7</span>
        <div class="edu-section-title">What is an Object?</div>
        <div class="edu-section-p">
            In Python, <strong>everything is an object</strong>. Integers, floats, strings, booleans, lists, dictionaries,
            functions, and class instances are all objects living in memory.
        </div>
        <div class="edu-diagram-box">
            <p style="color: #a6adc8; margin-bottom: 8px; font-size: 0.9rem;">When you write: <code>a = 10</code></p>
            <div class="flow-row" style="justify-content: flex-start;">
                <div class="flow-pill" style="border-color: #89b4fa; color: #89b4fa; font-weight: 700;">Variable name: a</div>
                <div class="flow-arrow-h">──────────────→</div>
                <div class="flow-pill flow-pill-green" style="text-align: left;">
                    🏷️ <strong>Object #1</strong><br>
                    <span style="font-size: 0.82rem; color: #bac2de;">Type: int | Value: 10</span>
                </div>
            </div>
        </div>
        <div class="edu-section-p">
            A <strong>variable name</strong> is simply a label or identifier. The <strong>object</strong> is the actual entity that
            holds the type and value. They are conceptually distinct!
        </div>
        <a href="https://docs.python.org/3/reference/datamodel.html" target="_blank" rel="noopener noreferrer" class="edu-doc-link">
            📖 Learn more — Python Official Docs: Data Model / Objects ↗
        </a>
    </div>
    """, unsafe_allow_html=True)

    # 10. Section — What is a Reference?
    st.markdown("""
    <div class="edu-section">
        <span class="edu-section-tag tag-green">Runtime Memory · Step 8</span>
        <div class="edu-section-title">What is a Reference?</div>
        <div class="edu-section-p">
            In Python, variables do not "contain" values directly. Instead, variables hold <strong>references</strong> (bindings) to objects.
            When you assign one variable to another, both names refer to the exact same object:
        </div>
        <div class="edu-diagram-box">
            <p style="color: #a6adc8; margin-bottom: 8px; font-size: 0.9rem;">When you write: <code>a = 10; b = a</code></p>
            <div style="font-family: monospace; color: #cdd6f4; line-height: 1.8; font-size: 1rem;">
                &nbsp;&nbsp;a ─────┐<br>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├────→ <span class="flow-pill flow-pill-green" style="padding: 2px 8px;">🏷️ Object #1 (Type: int, Value: 10)</span><br>
                &nbsp;&nbsp;b ─────┘
            </div>
        </div>
        <div class="edu-section-p">
            Here, <code>a</code> and <code>b</code> are aliases referencing the identical object in memory. Understanding this distinction
            is vital for understanding mutability, parameter passing, and state changes.
        </div>
        <a href="https://docs.python.org/3/reference/executionmodel.html#naming-and-binding" target="_blank" rel="noopener noreferrer" class="edu-doc-link">
            📖 Learn more — Python Execution Model: Naming and Binding ↗
        </a>
    </div>
    """, unsafe_allow_html=True)

    # 11. Section — What is the Heap?
    st.markdown("""
    <div class="edu-section">
        <span class="edu-section-tag tag-green">Runtime Memory · Step 9</span>
        <div class="edu-section-title">What is the Heap?</div>
        <div class="edu-section-p">
            The heap is the conceptual memory area where all Python objects are allocated and stored during program execution:
        </div>
        <div class="edu-diagram-box">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div style="border-right: 1px dashed #313244; padding-right: 15px;">
                    <strong style="color: #89b4fa;">GLOBAL FRAME</strong>
                    <div style="font-family: monospace; color: #bac2de; margin-top: 8px; line-height: 2;">
                        🔹 a ───→ Object #1<br>
                        🔹 b ───→ Object #2<br>
                        🔹 c ───→ Object #3
                    </div>
                </div>
                <div>
                    <strong style="color: #a6e3a1;">CONCEPTUAL HEAP / OBJECTS</strong>
                    <div style="font-family: monospace; color: #bac2de; margin-top: 8px; line-height: 2;">
                        🏷️ Object #1 (Type: int, Value: 10)<br>
                        🏷️ Object #2 (Type: int, Value: 20)<br>
                        🏷️ Object #3 (Type: int, Value: 30)
                    </div>
                </div>
            </div>
        </div>
        <div class="edu-disclaimer-card">
            <div class="edu-disclaimer-header">📌 Educational Model</div>
            <div class="edu-disclaimer-text">
                The <strong>HEAP / OBJECTS</strong> view in this visualizer is a conceptual teaching model designed to help you understand
                Python objects, references, and memory management. It does not represent actual physical RAM addresses or an exact diagram of
                CPython's internal memory allocator.
            </div>
            <a href="https://docs.python.org/3/c-api/memory.html" target="_blank" rel="noopener noreferrer" class="edu-doc-link">
                📖 Learn more — Python Official Docs: Memory Management ↗
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 12. Section — What is the Call Stack?
    st.markdown("""
    <div class="edu-section">
        <span class="edu-section-tag tag-purple">Runtime Memory · Step 10</span>
        <div class="edu-section-title">What is the Call Stack?</div>
        <div class="edu-section-p">
            The Call Stack organizes execution frames in a last-in, first-out (LIFO) stack. Whenever a function is invoked,
            a new execution frame is pushed onto the stack. When the function returns, its frame is popped.
        </div>
        <div class="edu-diagram-box">
            <p style="color: #a6adc8; margin-bottom: 8px; font-size: 0.9rem;">Example function call:</p>
            <pre style="background: #181825; padding: 10px; border-radius: 6px; border: 1px solid #313244; color: #f9e2af; margin-bottom: 14px; font-family: monospace;">def add(a, b):
    result = a + b
    return result

x = 10
y = 20
z = add(x, y)</pre>
            <div style="max-width: 360px; margin: 0 auto; font-family: monospace;">
                <div style="background: #251b33; border: 2px solid #cba6f7; border-radius: 6px; padding: 10px; margin-bottom: 8px;">
                    <strong style="color: #cba6f7;">⚡ add Frame</strong><br>
                    <span style="color: #cdd6f4;">🔹 a → Object #1 (10)<br>🔹 b → Object #2 (20)<br>🔹 result → Object #3 (30)</span>
                </div>
                <div style="text-align: center; color: #6c7086; font-size: 1.2rem; font-weight: bold;">↑ (pushed on call)</div>
                <div style="background: #1e1e2e; border: 2px solid #89b4fa; border-radius: 6px; padding: 10px; margin-top: 8px;">
                    <strong style="color: #89b4fa;">🌐 &lt;module&gt; Frame</strong><br>
                    <span style="color: #cdd6f4;">🔹 x → Object #1 (10)<br>🔹 y → Object #2 (20)<br>🔹 z → (pending return)</span>
                </div>
            </div>
        </div>
        <div class="edu-section-p">
            The visualizer displays each frame's local scope, allowing you to trace how variables exist independently within their respective function scopes.
        </div>
        <a href="https://docs.python.org/3/tutorial/controlflow.html#defining-functions" target="_blank" rel="noopener noreferrer" class="edu-doc-link">
            📖 Learn more — Python Official Docs: Defining Functions ↗
        </a>
    </div>
    """, unsafe_allow_html=True)

    # 13. Section — What is an Execution Frame?
    st.markdown("""
    <div class="edu-section">
        <span class="edu-section-tag tag-purple">Runtime Memory · Step 11</span>
        <div class="edu-section-title">What is an Execution Frame?</div>
        <div class="edu-section-p">
            An <strong>execution frame</strong> is the runtime context in which Python executes a code block.
            Every frame maintains its own state:
        </div>
        <div class="edu-diagram-box">
            <div style="font-family: monospace; color: #cdd6f4; line-height: 1.8;">
                <strong style="color: #cba6f7;">Execution Frame</strong><br>
                ├── Current execution context (code position & line)<br>
                ├── Local variables and name bindings<br>
                ├── References to heap objects<br>
                └── Return values and execution metadata
            </div>
        </div>
        <div class="edu-section-p">
            Python's execution model specifies that modules, function bodies, and class definitions each constitute distinct code blocks executed within execution frames.
        </div>
        <a href="https://docs.python.org/3/reference/executionmodel.html" target="_blank" rel="noopener noreferrer" class="edu-doc-link">
            📖 Learn more — Python Official Docs: Execution Model ↗
        </a>
    </div>
    """, unsafe_allow_html=True)

    # 14. Section — What is a Module?
    st.markdown("""
    <div class="edu-section">
        <span class="edu-section-tag tag-purple">Runtime Memory · Step 12</span>
        <div class="edu-section-title">What is a Module? &lt;module&gt; ≠ main()</div>
        <div class="edu-section-p">
            In Python, the top-level execution scope is identified as <code>&lt;module&gt;</code> (the Global Frame).
        </div>
        <div class="edu-diagram-box">
            <strong style="color: #89b4fa;">🌐 &lt;module&gt; (Global Frame)</strong>
            <div style="font-family: monospace; color: #bac2de; margin-top: 6px; line-height: 1.8;">
                🔹 a → Object #1<br>
                🔹 b → Object #2<br>
                🔹 c → Object #3
            </div>
        </div>
        <div class="edu-section-p">
            <strong>Important distinction:</strong> Python does <em>not</em> automatically wrap top-level statements into a hidden <code>main()</code> function.
            Top-level statements run directly inside the module's global execution frame.
        </div>
        <a href="https://docs.python.org/3/tutorial/modules.html" target="_blank" rel="noopener noreferrer" class="edu-doc-link">
            📖 Learn more — Python Official Docs: Modules ↗
        </a>
    </div>
    """, unsafe_allow_html=True)

    # 15. Section — How Everything Connects
    st.markdown("""
    <div id="connects" class="edu-section">
        <span class="edu-section-tag tag-yellow">Architecture · Step 13</span>
        <div class="edu-section-title">How Everything Connects</div>
        <div class="edu-section-p">
            Here is the complete conceptual architecture of Python execution visualized together:
        </div>
        <div class="edu-diagram-box">
            <div class="flow-col" style="gap: 8px;">
                <div class="flow-pill flow-pill-highlight" style="width: 280px;">PYTHON SOURCE CODE</div>
                <div class="flow-arrow-v">↓</div>
                <div class="flow-pill" style="width: 280px;">PYTHON EXECUTION</div>
                <div class="flow-arrow-v">↓</div>
                <div class="flow-pill" style="width: 280px;">CODE BLOCK</div>
                <div class="flow-arrow-v">↓</div>
                <div class="flow-pill flow-pill-purple" style="width: 280px;">EXECUTION FRAME</div>
                <div class="flow-arrow-v">↓</div>
                <div class="flow-pill" style="width: 280px;">VARIABLES / NAMES</div>
                <div class="flow-arrow-v">↓</div>
                <div class="flow-pill" style="width: 280px;">REFERENCES (BINDINGS)</div>
                <div class="flow-arrow-v">↓</div>
                <div class="flow-pill flow-pill-green" style="width: 280px;">OBJECTS (TYPE, VALUE, ATTRS)</div>
                <div class="flow-arrow-v">↓</div>
                <div class="flow-pill flow-pill-green" style="width: 280px;">CONCEPTUAL HEAP MODEL</div>
                <div class="flow-arrow-v">↓</div>
                <div class="flow-pill flow-pill-highlight" style="width: 280px;">PROGRAM OUTPUT</div>
            </div>
            <div style="text-align: center; margin-top: 16px; color: #cba6f7; font-weight: 600; font-size: 0.95rem;">
                Function Invocation: Function Call → New Execution Frame pushed to Call Stack → Return pops Frame
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 16. Section — Why This Visualizer Exists
    st.markdown("""
    <div class="edu-section">
        <span class="edu-section-tag tag-blue">Philosophy · Step 14</span>
        <div class="edu-section-title">Why This Visualizer Exists</div>
        <div class="edu-grid-3">
            <div class="edu-subcard" style="border-color: #45475a;">
                <div class="edu-subcard-title" style="color: #f38ba8;">❌ Traditional Learning</div>
                <div class="edu-subcard-desc" style="line-height: 1.8;">
                    WRITE CODE<br>
                    &nbsp;&nbsp;↓<br>
                    RUN<br>
                    &nbsp;&nbsp;↓<br>
                    OUTPUT: 30<br>
                    <em>(Everything that happened inside Python remains a black box)</em>
                </div>
            </div>
            <div class="edu-subcard" style="border-color: #89b4fa; grid-column: span 2;">
                <div class="edu-subcard-title" style="color: #89b4fa;">✅ Python Code Visualizer</div>
                <div class="edu-subcard-desc" style="line-height: 1.8; color: #cdd6f4;">
                    SOURCE CODE → EXECUTION EVENTS → FRAMES → VARIABLES → REFERENCES → OBJECTS → CALL STACK & HEAP → OUTPUT<br><br>
                    <strong style="color: #f9e2af; font-size: 1.05rem;">Don't just see what Python produces. See how Python executes.</strong>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 17. Section — What the Current Visualizer Can Show
    st.markdown("""
    <div class="edu-section">
        <span class="edu-section-tag tag-green">Capabilities · Step 15</span>
        <div class="edu-section-title">What the Current Visualizer Can Show</div>
        <div class="feature-grid">
            <div class="feature-item"><span class="feature-check">✓</span> Dynamic Python code editor (type or paste any code)</div>
            <div class="feature-item"><span class="feature-check">✓</span> Step-by-step forward & backward execution navigation</div>
            <div class="feature-item"><span class="feature-check">✓</span> Precise execution controls: Previous, Run, Next, Reset</div>
            <div class="feature-item"><span class="feature-check">✓</span> Execution event tracking: call, line, return, exception</div>
            <div class="feature-item"><span class="feature-check">✓</span> Global (&lt;module&gt;) and function-level execution frames</div>
            <div class="feature-item"><span class="feature-check">✓</span> Call Stack hierarchy with active frame highlighting</div>
            <div class="feature-item"><span class="feature-check">✓</span> Current Variables panel with emphasized variable names</div>
            <div class="feature-item"><span class="feature-check">✓</span> Variable → object reference badges</div>
            <div class="feature-item"><span class="feature-check">✓</span> Conceptual Heap / Object model with types and values</div>
            <div class="feature-item"><span class="feature-check">✓</span> Object identity (#N) and aliasing detection</div>
            <div class="feature-item"><span class="feature-check">✓</span> Real-time captured program standard output (stdout)</div>
            <div class="feature-item"><span class="feature-check">✓</span> Runtime exception preservation and syntax error diagnostics</div>
        </div>
        <p style="color: #a6adc8; font-size: 0.88rem; margin-top: 14px; margin-bottom: 6px;">Scope Boundaries (Educational Transparency):</p>
        <div class="feature-grid">
            <div class="not-feature-item"><span>✕</span> No CPU instruction / assembly visualization</div>
            <div class="not-feature-item"><span>✕</span> No physical hardware RAM addressing</div>
            <div class="not-feature-item"><span>✕</span> No CPython internal allocator claims</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 18. Final Call to Action
    st.markdown("""
    <div class="edu-final-cta">
        <h2 style="color: #cdd6f4; font-size: 2rem; margin-bottom: 10px;">You've learned the mental model. Now see it happen.</h2>
        <p style="color: #a6adc8; font-size: 1.1rem; margin-bottom: 24px;">
            Write a Python program and watch its execution unfold step by step.
        </p>
        <a href="#visualizer" class="edu-btn-primary" style="font-size: 1.15rem; padding: 14px 32px;">
            ▶ Open Python Code Visualizer
        </a>
        <p style="color: #89b4fa; font-weight: 700; margin-top: 16px; letter-spacing: 0.5px;">
            Make execution visible.
        </p>
    </div>
    """, unsafe_allow_html=True)
