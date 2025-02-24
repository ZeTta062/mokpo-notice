from flask import Flask, render_template, request
import pandas as pd
from notice import (
    crawl_mokpo_public_notice,
    crawl_mokpo_notice,
    crawl_jeonnam_notice
)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')  # home.html에서 검색 버튼 클릭시 search 페이지로 이동

@app.route("/search", methods=["POST"])
def search():
    if request.method == "POST":
        # 크롤링 실행
        mokpo_public_notice_data = []
        for page in range(1, 3):  # 1~2페이지 크롤링
            mokpo_public_notice_data.extend(crawl_mokpo_public_notice(page))
        df_mokpo_public_notice = pd.DataFrame(mokpo_public_notice_data, columns=["제목", "등록부서", "작성일", "링크"])

        mokpo_notice_data = []
        for page in range(1, 3):  # 1~2페이지 크롤링
            mokpo_notice_data.extend(crawl_mokpo_notice(page))
        df_mokpo_notice = pd.DataFrame(mokpo_notice_data, columns=["제목", "등록부서", "작성일", "링크"])

        jeonnam_notice_data = []
        for page in range(1, 3):  # 1~2페이지 크롤링
            jeonnam_notice_data.extend(crawl_jeonnam_notice(page))
        df_jeonnam_notice = pd.DataFrame(jeonnam_notice_data, columns=["제목", "등록부서", "작성일", "링크"])

        # 링크에 "바로가기" 텍스트 추가 및 새 탭에서 열리도록 처리
        def add_hyperlink(df):
            for i, row in df.iterrows():
                df.at[i, '링크'] = f'<a href="{row["링크"]}" target="_blank">바로가기</a>'
            return df

        df_mokpo_public_notice = add_hyperlink(df_mokpo_public_notice)
        df_mokpo_notice = add_hyperlink(df_mokpo_notice)
        df_jeonnam_notice = add_hyperlink(df_jeonnam_notice)

        # DataFrame을 HTML로 변환하면서 스타일 적용
        def format_table(df):
            table_html = df.to_html(index=False, escape=False)  # escape=False로 HTML을 그대로 렌더링
            # th 태그 가운데 정렬 스타일 추가
            table_html = table_html.replace("<th>", "<th style='text-align: center;'>")
            return table_html

        mokpo_public_notice_html = format_table(df_mokpo_public_notice)
        mokpo_notice_html = format_table(df_mokpo_notice)
        jeonnam_notice_html = format_table(df_jeonnam_notice)

        # 결과를 HTML 템플릿에 전달
        return render_template("search.html",
            mokpo_public_notice=mokpo_public_notice_html,
            mokpo_notice=mokpo_notice_html,
            jeonnam_notice=jeonnam_notice_html
        )


if __name__ == "__main__":
    app.run(debug=True)
