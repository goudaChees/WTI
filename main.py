from tkinter.messagebox import QUESTION
from flask import Flask, render_template, request, jsonify
import pymysql
import datetime

app = Flask(__name__)
db = pymysql.connect(host='localhost', port=3306, user='root', passwd='copyw17@', db='wti', charset="utf8")
cursor = db.cursor()


@app.route("/page", methods=["GET"])
def main_page():
    return render_template('index.html')  ## index 페이지 이동


@app.route("/page2", methods=["GET"])
def page2():
    ## page = request.args.get(page_parameter(), type=int, default=1 )
    ## limit = 10
    ## offset = page*limit - limit
    ## length_sql = "select news_id, news_title, news_content from news_table order by news_id desc"

    ## cursor.execute(length_sql)
    ## results = cursor.fetchall()
    ## maxLength = len(results)

    ## sql = "select news_id, news_title, news_content from news_table order by news_id desc limit %s offset %s", (limit , offset)
    ## cursor.execute(sql)
    ## result_sql = cursor.fetchall()
    ## cursor.close() 

    return render_template('news_main.html')  ## 메인 뉴스 목록 페이지 이동


@app.route("/test", methods=["GET"])
def test_pabe():
    ## page = request.args.get(page_parameter(), type=int, default=1 )
    ## limit = 10
    ## offset = page*limit - limit
    ## length_sql = "select news_id, news_title, news_content from news_table order by news_id desc"

    ## cursor.execute(length_sql)
    ## results = cursor.fetchall()
    ## maxLength = len(results)

    ## sql = "select news_id, news_title, news_content from news_table order by news_id desc limit %s offset %s", (limit , offset)
    ## cursor.execute(sql)
    ## result_sql = cursor.fetchall()
    ## cursor.close() 

    return render_template('dev.html')


@app.route("/page4", methods=["GET"])
def page4():
    return render_template('news_view.html')  ## 뉴스 상세보기 페이지 이동


@app.route("/page5", methods=["GET"])
def page5():
    return render_template('chart_thisweek.html')  ## 세부 유가 차트 페이지 이동


@app.route("/page6", methods=["GET"])
def page6():
    return render_template('chart_forecast.html')  ## 예측 유가 차트 페이지 이동


# index 페이지 차트 불러오기 ################
@app.route("/wti_chart", methods=["GET"])
def get_wti_data():
    sql = "select Date, WTI_price, df_id from df_all where Date between '2022-07-21' and '2022-09-09'"
    cursor.execute(sql)
    results = cursor.fetchall()  
    wti_data = []
    for result in results:
        wti_data.append({
            'Date': result[0],
            'WTI_price': result[1]
        })
    db.commit()
    # print(wti_data)
    return jsonify(wti_data)


@app.route("/wti_chart/plus", methods=["GET"])
def get_wti_data2():
    sql = "select date, pred_wti_price from pred_wti_50  ;"
    cursor.execute(sql)
    results = cursor.fetchall()
    wti_data = []
    for result in results:
        wti_data.append({
            'Date': result[0],
            'WTI_price': result[1]
        })
    db.commit()
    # print(wti_data)
    return jsonify(wti_data)


# 차트 세부 페이지_지수 추가 비교하기 #######
@app.route("/wti_chart_addIndex/<period>", methods=["GET"])
def chart_addIndex(period):
    server_per = int(period) * (-1)
    print(server_per)
    now_date = datetime.date.today()
    td1 = datetime.timedelta(days=-7)  # 오늘 유가 데이타 없으므로 테스트용 _ 나중 삭제하기
    td = datetime.timedelta(days=server_per-7)
    new_date1 = now_date + td1
    new_date = now_date + td
    sql = "select * from df_all where Date between '%s' and '%s' order by df_id" % (new_date, new_date1)
    cursor.execute(sql)
    results = cursor.fetchall()
    add_index_data = []
    for result in results:
        add_index_data.append({
            'df_id': result[0],
            'Date': result[1],
            'WTI_price': result[2],
            'WTI_open': result[3],
            'WTI_high': result[4],
            'WTI_low': result[5],
            'WTI_vol': result[6],
            'WTI_change': result[7],
            'DJI_price': result[8],
            'CBCCI': result[14],
            'CPI_Korea': result[23],
            'XLE_price': result[26],
            'CLI_US': result[39],
            'Dollar_Index': result[64]
        })
    db.commit()
    # print(now_date)
    # print(new_date)
    # print(add_index_data)
    return jsonify(add_index_data)


# 차트 세부 페이지_기간 설정후 데이타 불러오기 #######
@app.route("/wti_chart_this/<period>", methods=["GET"])
def reset_wti_data(period):
    server_per = int(period)*(-1)
    print(server_per)
    now_date = datetime.date.today()
    td1 = datetime.timedelta(days=-7)  # 오늘 유가 데이타 없으므로 테스트용 _ 나중 삭제하기
    td = datetime.timedelta(days=server_per-7)
    new_date1 = now_date + td1
    new_date = now_date + td
    sql = "select * from df_all where Date between '%s' and '%s' order by df_id" % (new_date, new_date1)
    cursor.execute(sql)
    results = cursor.fetchall()
    wti_data = []
    for result in results:
        wti_data.append({
            'WTI_id': result[0],
            'Date': result[1],
            'WTI_price': result[2],
            'WTI_open': result[3],
            'WTI_high': result[4],
            'WTI_low': result[5],
            'WTI_vol': result[6],
            'WTI_change': result[7],
            'D_world': result[43],
            'S_world': result[46]
        })
    db.commit()
    print(now_date)
    print(new_date)
    # print(wti_data)
    return jsonify(wti_data)



# 유가 예측 chart, weights 불러오기
@app.route("/wti_forecast/<f_table>", methods=["GET"])
def forecast_50(f_table):
    t_num = int(f_table)
    sqla = "select * from df_all order by df_id desc limit 50"
    cursor.execute(sqla)
    results1 = cursor.fetchall()
    sqlb = "select * from pred_wti_%s order by pred_id desc" % (t_num)
    cursor.execute(sqlb)
    results2 = cursor.fetchall()
    sqlc = "select * from weight_seasonal_%s order by weight_id desc" % (t_num)
    cursor.execute(sqlc)
    results3 = cursor.fetchall()

    wti_data = []
    pred_data = []
    weight_data = []
    for result1 in results1:
        wti_data.append({
            "wti_id": result1[0],
            "wti_date": result1[1],
            "WTI_price": result1[2],
            "WTI_vol": result1[6]
        })
    for result2 in results2:
        pred_data.append({
            "pred_date": result2[1],
            "pred_price": result2[2]
        })
    for result3 in results3:
        weight_data.append({
            "weight_date": result3[1],
            "r1_date": result3[2],
            "r1_col": result3[3],
            "r1_weight": result3[4],
            "r2_date": result3[5],
            "r2_col": result3[6],
            "r2_weight": result3[7],
            "r3_date": result3[8],
            "r3_col": result3[9],
            "r3_weight": result3[10]
        })
    db.commit()
    # print(wti_data)
    # print(pred_data)
    # print(weight_data)
    return jsonify(wti_data, pred_data, weight_data)  # [Array(50), Array(50), Array(50)]


# 메인 뉴스 목록 페이지 데이타 불러오기 #####
@app.route("/wti/<param>", methods=["GET"])
def get_news(param):
    print(param)
    page_parameter = int(param)
    page = request.args.get(page_parameter, type=int, default=1)
    limit = 10
    offset = (page_parameter * limit) - limit
    print(page_parameter, offset)
    length_sql = "select news_id, news_title, news_content from news_table order by news_id desc"

    cursor.execute(length_sql)
    results = cursor.fetchall()
    maxLength = len(results)

    sql = "select news_id, label, news_title, news_content, news_date from news_table order by news_id limit %s offset %s" % (
    limit, offset)
    cursor.execute(sql)
    results2 = cursor.fetchall()

    news = []
    for result in results2:
        news.append({
            'news_id': result[0],
            'label': result[1],
            'news_title' :result[2],
            'news_content': result[3],
            'news_date': result[4]
            
        })
    db.commit()
    return jsonify(news)


# 뉴스 상세 보기 페이지 id 불러온 후 해당 데이타 불러 오기 #####
@app.route("/wti/detail/<newsId>", methods=["GET"])
def get_news_detail(newsId):
    sql = "select * from news_table where news_id = %s"
    cursor.execute(sql, [newsId])
    results = cursor.fetchall()
    news = []
    for result in results:
        news.append({
            'news_id': result[0],
            'label':result[1],
            'news_title': result[2],
            'news_short_desc': result[3],
            'news_content': result[4],
            'news_author': result[5],
            'news_publisher': result[6],
            'news_date': result[7]
        })
    db.commit()
    print(newsId)
    return jsonify(news)


# 뉴스 데이타 저장하기 ##################
@app.route("/wti", methods=["POST"])
def create_news():
    server_news_title = request.form["news_title"]
    server_news_short_desc = request.form["news_short_desc"]
    server_news_content = request.form["news_content"]
    server_news_author = request.form["news_author"]
    server_news_publisher = request.form["news_publisher"]
    server_news_date = request.form["news_date"]
    sql = "insert into news_table (news_title, news_short_desc, news_content, news_author, " \
          "news_publisher, news_date) values ('%s','%s','%s','%s','%s','%s') " % (server_news_title,
                                                                                  server_news_short_desc,
                                                                                  server_news_content,
                                                                                  server_news_author,
                                                                                  server_news_publisher,
                                                                                  server_news_date)
    cursor.execute(sql)
    db.commit()
    return "OK"


# 뉴스 데이타 삭제하기 #######################
@app.route("/wti/all", methods=["DELETE"])
def delete_news():
    sql = "delete from news_table"
    cursor.execute(sql)
    db.commit()
    return "OK"


if __name__ == "__main__":
    app.run(debug=True)
