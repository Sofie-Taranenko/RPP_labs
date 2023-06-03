def get(name):
    id = check(name)
    cursor.execute("""select rate from currency_rates_values""")
    cursor.execute("""select rate from currency_rates where  currency_rate_id = %s,(id,)""")
    data_id = cursor.fetchall()

async def payload(Request: RequestBody):
        id_cur = check(name)
        print(id_cur)
        for i in rates:
            cursor.execute(""" Insert into currency_rates_values (currency_code,rate,currency_rate_id)""")
            cursor.execute(""" Insert into currency_rates (currency_code,rate,currency_rate_id)
                                         values (%s,%s,%s);""", (i.code, i.rate, id_cur,))
            conn.commit()
        raise HTTPException(200)