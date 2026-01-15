import markdown
import os
from pygments.formatters import HtmlFormatter


def convert_md_to_printable_html(input_file, output_file):
    # 检查文件是否存在
    if not os.path.exists(input_file):
        print(f"❌ 错误: 找不到文件 {input_file}")
        print("💡 提示: 请检查路径中是否有错别字，或者是否加上了 r\"...\" 前缀")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # --- V3 核心改动: 使用 pymdownx ---
    # 1. 'pymdownx.arithmatex': 完美处理数学公式
    # 2. 'pymdownx.highlight': 代码高亮更强
    # 3. 'pymdownx.superfences': 支持复杂的代码块嵌套
    extensions = [
        'pymdownx.arithmatex',
        'pymdownx.highlight',
        'pymdownx.superfences',
        'tables',
        'nl2br'  # 把换行符转为 <br>
    ]

    # 配置 Arithmatex 使用通用模式 (Generic)，输出 \(...\) 格式
    # 这样 MathJax 3 就能完美识别了
    extension_configs = {
        'pymdownx.arithmatex': {
            'generic': True,
        }
    }

    html_body = markdown.markdown(
        md_text,
        extensions=extensions,
        extension_configs=extension_configs
    )

    # 获取代码高亮样式
    code_css = HtmlFormatter(style='github-dark').get_style_defs('.highlight')

    # --- HTML 模板 ---
    full_html = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>AI 笔记归档</title>

        <script>
        MathJax = {{
          tex: {{
            inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
            displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
            processEscapes: true
          }},
          options: {{
            ignoreHtmlClass: 'tex2jax_ignore',
            processHtmlClass: 'tex2jax_process'
          }}
        }};
        </script>
        <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>

        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                line-height: 1.6;
                color: #24292e;
                max-width: 850px;
                margin: 0 auto;
                padding: 40px;
                background-color: #fff;
            }}

            h1, h2, h3 {{ color: #1a73e8; border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; margin-top: 1.5em;}}

            /* 代码块样式优化 */
            .highlight {{ 
                background: #f6f8fa; 
                padding: 12px; 
                border-radius: 6px; 
                overflow-x: auto; 
                margin: 16px 0;
                border: 1px solid #e1e4e8;
            }}

            /* 公式样式微调 */
            mjx-container {{ font-size: 110% !important; }}

            blockquote {{
                border-left: 4px solid #dfe2e5;
                color: #6a737d;
                padding-left: 16px;
                margin: 16px 0;
            }}

            /* 表格样式 */
            table {{ border-collapse: collapse; width: 100%; margin: 16px 0; }}
            th, td {{ border: 1px solid #dfe2e5; padding: 6px 13px; }}
            th {{ background-color: #f2f2f2; }}

            @media print {{
                body {{ max-width: 100%; padding: 0; }}
                .highlight {{ break-inside: avoid; }}
                h1, h2 {{ page-break-after: avoid; }}
            }}

            {code_css}
        </style>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_html)

    print(f"✅ 转换成功！\n文件位置: {os.path.abspath(output_file)}")
    print("👉 请用浏览器打开 output_v3.html 查看效果")


if __name__ == "__main__":
    # 【特别注意】: 这里一定要保留 r 前缀，否则还会报 unicode error 错误
    input_md = r"C:\Users\Cuphead\OneDrive\桌面\1. 核心痛点分析 (Why).md"
    output_html = "output_v3.html"

    convert_md_to_printable_html(input_md, output_html)