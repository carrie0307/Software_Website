# -*- coding:utf8 -*-
import MySQLdb

conn=MySQLdb.connect(host='localhost',user='root',passwd='1234',port=3306,charset = 'utf8')
cur=conn.cursor()
cur.execute("use electronics")


def Main_list():
    goods_dict = {}
    return_dict = {}
    sqlstr = "SELECT id,name, price,discount FROM goods_table"
    count = cur.execute(sqlstr)
    result = cur.fetchall()
    for item in result:
        if item[3]:
            discount = int(item[2])
        else:
            discount = 1
        goods_id = "%03d"%int(item[0])
        goods_dict[goods_id] = [str(item[1]), int(item[2]), discount]
    return_dict['length'] = int(count)
    return_dict['data'] = goods_dict
    print return_dict
    return return_dict


# 登录成功返回用户id，失败返回0
def Login_function(acc, passwd):
    sqlstr = "SELECT id FROM user_table WHERE account = '%s' AND password = '%s'" %(acc, passwd)
    count = int(cur.execute(sqlstr))
    if count == 0:
        id =  '0'
    else:
        id = str(cur.fetchone()[0])
    return id


def Reg_function(account, passwd, addr ,tel):
    # a="%5d"%x
    accounts = []
    sqlstr = "SELECT account FROM user_table"
    cur.execute(sqlstr)
    result = cur.fetchall()
    for item in result:
        accounts.append(str(item[0]))
    if account in accounts:
        id = '0'
    else:
        sqlstr = "INSERT INTO user_table(account, password, addr, tel) VALUES('%s','%s','%s','%s') " %(account, passwd, addr,tel)
        cur.execute(sqlstr)
        conn.commit()
        sqlstr = "SELECT id FROM user_table WHERE account = '%s' AND password = '%s'" %(account, passwd)
        cur.execute(sqlstr)
        result = cur.fetchall()
        id = int(result[0][0])
        id = "%03d"%id
    print id
    return id


# 根据id返回表中的detail字段 ,  如果不存在此id，返回0
def Detail_functioni(id):
    sqlstr = "SELECT detail FROM  goods_table WHERE id = %s" %id
    count = int(cur.execute(sqlstr))
    if count == 0:
        detail = '0'
    else:
        detail = str(cur.fetchone()[0])
    return detail


# 查询功能，根据商品类别查出所有商品，并返回   注：没有考虑查不到的情况, length = 0
def List_function(ttype):
    goods_dict = {}
    return_dict = {}
    sqlstr = "SELECT id,name, price,discount FROM goods_table WHERE kind = '%s'" %ttype
    count = cur.execute(sqlstr)
    if count == 0:
        return_dict['length'] = int(count)
        return_dict['data'] = goods_dict
        return return_dict
    else:
        result = cur.fetchall()
        for item in result:
            if item[3]:
                discount = int(item[2])
            else:
                discount = 1
            goods_id = "%03d"%int(item[0])
            goods_dict[goods_id] = [str(item[1]), int(item[2]), discount]
        return_dict['length'] = int(count)
        return_dict['data'] = goods_dict
        print return_dict
        return return_dict


# 查询功能，根据商品名称查出所有商品，并返回    注：没有考虑查不到的情况 length = 0
def Search_function(item):
    goods_dict = {}
    return_dict = {}
    sqlstr = "SELECT id,name, price,discount FROM goods_table WHERE name = '%s'" %item
    count = cur.execute(sqlstr)
    if count == 0:
        return_dict['length'] = int(count)
        return_dict['data'] = goods_dict
        return return_dict
    else:
        result = cur.fetchall()
        for item in result:
            if item[3]:
                discount = int(item[2])
            else:
                discount = 1
            goods_id = "%03d"%int(item[0])
            goods_dict[goods_id] = [str(item[1]), int(item[2]), discount]
        return_dict['length'] = int(count)
        return_dict['data'] = goods_dict
        print return_dict
        return return_dict

# 库存不足需要说明是哪个货物不足吗？？
# def Purchasefunction(dict):





if __name__ == '__main__':
    # Main_list()
    # Login_function('123', 'abc123')
    # Detail_functioni('001')
    # Reg_function('795', 'abc123', 'HIT' ,'18963166073')
    Search_function('computer')
