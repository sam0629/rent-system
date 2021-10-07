from flask import Flask, render_template, request, jsonify, session, redirect, url_for,json
from dacs.user_dac import UserDac
from dacs.product_dac import ProductDac
from dacs.space_dac import SpaceDac
from dacs.space_time_dac import SpaceTimeDac
from dacs.trade_dac import TradeDac
from dacs.record_dac import RecordDac
from datetime import datetime, timedelta
import time

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def regist(userName, userAccount, userPassword):
    result = user_dac.read_uaccount(userAccount)
    if result is None:
        user_dac.add_user(userName, userAccount, userPassword)
        return True
    else:
        return False


def search(type):
    if type == 'all':
        return product_dac.read_product()
    return product_dac.read_product_by_type(type)


def get_hour(td):
    return td.seconds // 3600


def check_null_space(date, s_type):
    sid_rows = space_dac.read_sid(s_type)
    sids = [str(row.get('SId')) for row in sid_rows]
    # init columns
    columns = [{'title': 'Time', 'data': 'time'}]
    for sid in sids:
        columns.append({'title': sid, 'data': sid})
    # set all space no occupied
    data = []
    for i in range(24):
        dt = datetime.strptime(date, "%Y-%m-%d") + timedelta(hours=i)
        row = {"time": dt}
        for sid in sids:
            row[sid] = sid
        data.append(row)

    # set witch space occupied
    space_times = space_time_dac.qry_space_time(date, sids)
    for st in space_times:
        sid = str(st.get('SId'))
        start_time_hour = get_hour(st.get('StartTime'))
        for t in range(st.get('TotalTime')):
            data[start_time_hour + t][sid] = ''

    resp_data = {
        "columns": columns,
        "data": data,
        "targets": [i for i in range(1, len(columns))]
    }

    return resp_data


def search_one_two_three(sid, time, date):
    data = []
    new_time = int(time[0:2])
    for i in range(24):
        x = 0
        data.append(x)
    qry_startandtotal_time = space_time_dac.qry_startandtotal_time(date, sid)
    for i in qry_startandtotal_time:
        data[get_hour(i.get('StartTime'))] = 1
        if i.get('TotalTime') == 2:
            data[get_hour(i.get('StartTime')) + 1] = 1
        elif i.get('TotalTime') == 2:
            data[get_hour(i.get('StartTime')) + 1] = 1
            data[get_hour(i.get('StartTime')) + 2] = 1
    for j in range(new_time, new_time + 2):
        if new_time <= 21:
            if data[new_time] == data[new_time + 1] == data[new_time + 2] == 0:
                return 3
            elif data[new_time] == data[new_time + 1] == 0:
                return 2
            elif data[new_time] == 0:
                return 1
        elif new_time == 22:
            if data[new_time] == data[new_time + 1] == 0:
                return 2
            elif data[new_time] == 0:
                return 1
        elif new_time == 23:
            if data[new_time] == 0:
                return 1


def reservation(uid, sid, date, start_time, end_time, total_time, totalmoney):
    space_times = space_time_dac.qry_startandtotal_time(date, sid)
    onehourmoney = space_dac.read_smoney(sid).get('sPricePerHour')
    enter_start_time = int(str(start_time[0:2]))
    trade_time = date + " " + start_time
    trade_time = (datetime.strptime(trade_time, "%Y-%m-%d %H:%M"))
    data = []

    for i in range(24):
        data.append(0)
    for st in space_times:
        total = st.get('TotalTime')
        start_time_hour = get_hour(st.get('StartTime'))

        data[start_time_hour] = 1
        for t in range(total):
            data[start_time_hour + t] = 1
    for i in range(int(total_time)):
        if data[enter_start_time + i] == 1:
            return False
        else:
            space_time_dac.write(sid, uid, date, start_time, end_time, total_time, totalmoney)
            trade_dac.writetrade(uid,sid,trade_time)
            return True
def check_tid(date_and_sid,uid):
    trade_time = ''
    sid = ''
    have_trade_time = None
    for i in range(len(date_and_sid)):
        if have_trade_time:
            if ord(date_and_sid[i]) >= 48 and ord(date_and_sid[i]) <= 57:
                sid += date_and_sid[i]
        else:
            if date_and_sid[i] != 'S':
                trade_time += date_and_sid[i]
            else:
                have_trade_time = 1
    tid = trade_dac.qry_tid(trade_time,sid,uid)
    return tid
def check_cart(cart):
    if cart:
        for car in range(len(cart)):
            is_correct_product_and_get_amount = product_dac.is_correct_product_and_get_amount(cart[car]['pid'],cart[car]['pname'],cart[car]['pamount'])
            if is_correct_product_and_get_amount is None:
                msg = '交易失敗，商品不存在'
                return {'result': False, 'msg': msg}
            elif int(is_correct_product_and_get_amount.get('PNumber')) < int(cart[car]['pamount']):
                msg = '交易失敗，庫存數量不足'
                return {'result': False, 'msg': msg}
            else:
                price = product_dac.qry_unit_price(cart[car]['pid'])
                cart[car]['price'] = price.get('PUnitPrice')
        return {'result': True, 'msg': cart}
    else:
        msg = '交易失敗，購物車內無東西'
        return {'result': False, 'msg': msg}

@app.route("/")
def home():
    uid = session.get('uid')
    msg = ''
    if uid is not None:
        data = user_dac.read_uname(uid)
        if data is not None:
            uname = data.get('UName')
            msg = 'Welcome'
            if uname != '':
                msg += f', {uname}'

    return render_template('home.html', msg=msg)


@app.route("/product", methods=['GET', 'POST'])
def product():
    if 'uid' in session:
        uid = session.get('uid')
        all_times = trade_dac.qry_times(uid)
        all_types = product_dac.qry_pType()
        if request.method == 'POST':
            entertype = request.form.get("entertype")
            if entertype == 'all':
                res = product_dac.read_all_product()
            else:
                res = product_dac.read_product_by_type(entertype)
            return jsonify(res)
        return render_template('product.html',Alltypes = all_types,Alltimes = all_times)

    return redirect(url_for('login'))


@app.route("/space", methods=['GET', 'POST'])
def space():
    if 'uid' in session:
        uid = session.get('uid')
        msg = ''
        if uid is not None:
            data = user_dac.read_uname(uid)
            if data is not None:
                uname = data.get('UName')
                msg = 'Select your Date'
                if uname != '':
                    msg += f', {uname}'
        if request.method == 'POST':
            date = request.form.get('enterdate')
            s_type = request.form.get('enterspace')
            data = check_null_space(date, s_type)
            return jsonify(data)

        all_types = space_dac.read_type_ddl()
        return render_template('space.html', Alltypes=all_types, msg=msg, uid=uid)
    return redirect(url_for('login'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        userName = request.form['name']
        userAccount = request.form['account']
        userPassword = request.form['password']
        res = regist(userName, userAccount, userPassword)
        return jsonify(res)
    return render_template('register.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    # 用帳密抓用戶名字
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        data = user_dac.read_uid(account, password)
        # 帳號存在給session
        if data is not None:
            session['uid'] = data.get('UId')
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route("/data", methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        sid = request.form.get('sid')
        start_time = request.form.get('startTime')
        date = request.form.get('date')
        number = search_one_two_three(sid, start_time, date)
        unit_price = space_dac.read_smoney(sid).get('sPricePerHour')
        total_time = 1  # default
        money = total_time * unit_price
        stype = space_dac.read_stype(sid).get('SType')
        end_time = (datetime.strptime(start_time, '%H:%M') + timedelta(hours=1)).strftime('%H:%M')


        result = {
            'sid': sid,
            'stype': stype,
            'date': date,
            'start_time': start_time,
            'end_time': end_time,
            'number': number,
            'unit_price': unit_price,
            'money': money,
            'total_time': total_time
        }
        return jsonify(result)


@app.route("/sure", methods=['GET', 'POST'])
def sure():
    if request.method == 'POST':
        uid = session.get('uid')
        sid = request.form.get('sid')
        date = request.form.get('date')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        total_time = request.form.get('total_time')
        totalmoney = request.form.get('money')
        res = reservation(uid, sid, date, start_time, end_time, total_time, totalmoney)
        result = {"result": res}
        return (result)

@app.route("/record", methods=['GET', 'POST'])
def record():
    if request.method == 'POST':
        uid = session.get('uid')
        cart = request.form.get('cart')
        date_and_sid = request.form.get('date_and_sid')

        if check_tid(date_and_sid,uid) is None:
            return {'msg': "Error"}


        tid = check_tid(date_and_sid,uid).get('TId')
        cars = json.loads(cart)
        results = check_cart(cars)


        if results['result'] == False:
            return {'msg': results['msg']}

        total_price = 0
        for r in results['msg']:
            sale_price = int(r['pamount'])*int(r['price'])
            pid = int(r['pid'])
            amount = int(r['pamount'])
            total_price += sale_price
            record_dac.write_record(pid,tid,amount,sale_price)
            print(total_price)
        return {'msg': "交易成功，總金額為"+str(total_price)+"元"}

    else:
        return {'msg':'選擇的時段無效'}

@app.route('/logout')
def logout():
    # 移除session
    session.pop('uid', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    user_dac = UserDac()
    product_dac = ProductDac()
    space_dac = SpaceDac()
    space_time_dac = SpaceTimeDac()
    trade_dac = TradeDac()
    record_dac = RecordDac()

    app.run(debug=True)
