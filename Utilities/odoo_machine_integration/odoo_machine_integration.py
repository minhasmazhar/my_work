import psycopg2
import datetime
import logging
from zk import ZK
from datetime import datetime
import schedule
import threading
import config as cfg
import pytz
import xmlrpc.client
import time
import erppeek

_logger = logging.getLogger(__name__)

if not cfg:
    logging.info("No Configuration File Found!")
    print("No Configuration File Found!")

machine_ip = cfg.machine_ip
zk_port = cfg.zk_port
timeout = cfg.timeout
db_logins = cfg.db_logins
run_after_every = cfg.run_after_every
check_out_machine_code = cfg.check_out_machine_code
machine_timezone = cfg.machine_timezone
db_user = cfg.db_user
db_password = cfg.db_password
db_name = cfg.db_name
pg_user = cfg.pg_user


def device_connect(zk):
    try:
        conn = zk.connect()
        return conn
    except Exception as e:
        print("Connection failed! please try again.")
        print(e)


def start(database, user, password, host, port, SERVER):
    logging.info("Starting data synchronization!")
    print("Starting data synchronization!")

    try:
        connection = psycopg2.connect(user=pg_user,
                                      password=password,
                                      host=host,
                                      port=port,
                                      database=database)

        cursor = connection.cursor()
    except Exception as e:
        logging.info("Database connection failed!")
        print("Database connection failed!")
        print(e)

    try:
        zk = ZK(machine_ip, port=zk_port, timeout=timeout, password=0, force_udp=False, ommit_ping=False)
    except Exception as e:
        logging.info("Machine connection failed!")
        print("Machine connection failed!")
        print("Exception: ", e)

    conn = device_connect(zk)

    # print('USERS: ', conn.get_users())
    # print(conn.get_user_extend_fmt())
    user_name = []
    user_id = []
    if conn:
        for rec in conn.get_users():
            user_name.append(rec.name)
            user_id.append(rec.user_id)

    res = {}
    for key in user_id:
        for value in user_name:
            res[key] = value
            user_name.remove(value)
            break

    # Printing resultant dictionary
    # print(res.get('1'))

    if conn:
        try:
            attendance = conn.get_attendance()
            # print(conn.get_users())
        except:
            attendance = False
        if attendance:
            count = 0
            # print(attendance)
            for each in attendance:

                check_out = None
                check_in = None
                count += 1
                atten_time = each.timestamp

                local_tz = pytz.timezone(machine_timezone or 'GMT')
                local_dt = local_tz.localize(atten_time, is_dst=None)
                utc_dt = local_dt.astimezone(pytz.utc)
                utc_dt = utc_dt.strftime("%Y-%m-%d %H:%M:%S")
                atten_time = datetime.strptime(
                    utc_dt, "%Y-%m-%d %H:%M:%S")
                atten_time = str(atten_time)
                # print('my time', atten_time)
                # tste

                if each.punch == check_out_machine_code:
                    check_out = atten_time
                else:
                    check_in = atten_time
                postgres_insert_query = '''INSERT INTO 
                employee_attendance (user_id, check_in, check_out,machine_id,user_name) VALUES (%s,%s,%s,%s,%s)'''
                record_to_insert = (each.user_id, check_in, check_out, each.uid, res[each.user_id])
                # print(record_to_insert)
                try:
                    cursor.execute(postgres_insert_query, record_to_insert)
                    count = cursor.rowcount

                except Exception as e:
                    print(e)
            try:
                connection.commit()
                print(count, "Record inserted successfully into employee.attendance table")
                zk.clear_attendance()
                # conn.disconnect()

                user = db_user
                password = db_password
                database = db_name
                client = erppeek.Client(server=SERVER)
                client.login(user=user, password=password, database=database)
                logging.info("update for %s with username=%s and password=%s initiated", database, user, password)
                # start_time = datetime.datetime.now()
                common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(SERVER))
                uid = common.authenticate(database, user, password, {})
                data = client.execute('employee.attendance', 'get_attendance')
                conn.disconnect();

            except Exception as e:
                logging.info("Error in committing machine data!")
                print("Error in committing machine data!")
                print(e)

    else:
        logging.info("No Connection Found ---- Exiting")
        print("No Connection Found ---- Exiting")


def method_start():
    if __name__ == "__main__":
        format = "%(asctime)s %(levelname)s %(message)s"
        logging.basicConfig(format=format, level=logging.DEBUG, filename='machin_odoo.log',
                            datefmt='%d/%m/%Y %H:%M:%S')

        for db in db_logins:
            logging.info("Starting Update thread for %s", db['db'])
            x = threading.Thread(target=start,
                                 args=(db['db'], db['username'], db['password'], db['host'], db['port'], db['server']))
            x.start()


# method_start()
schedule.every(run_after_every).minutes.do(method_start)
# schedule.every(5).seconds.do(dump_data_pymongo)

while True:
    schedule.run_pending()
    time.sleep(1)
