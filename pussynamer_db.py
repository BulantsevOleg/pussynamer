from datetime import datetime, timezone
import psycopg2

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        # params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(
            host = "ec2-63-33-14-215.eu-west-1.compute.amazonaws.com",
            port = "5432",
            database = "d9u6kgfel607so",
            user = "uzdjhqiwswsouh",
            password = "59e32934fe6d12199f6e93c46c2c007f727a972ed2c51f05adfa52720dafdabe"
        )
		
        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT * FROM name')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def insert(id_user_field, created_on_field, name):
    """ Connect to the PostgreSQL database server """

    """ insert a new row into the note table """

    conn = None
    pussy_id = None 
    active_status = ('TRUE', 'FALSE')

    try:
        # read connection parameters
        # params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(
            host = "ec2-63-32-7-190.eu-west-1.compute.amazonaws.com",
            port = "5432",
            database = "d5789ofavjem2n",
            user = "dppxvycvjbbmxm",
            password = "919599b7ef2bd77ad97989e161038040010f70c679ff64d58ec36eee93c4e6bc"
        )
		
        # create a cursor
        cur = conn.cursor()

        # cur.execute("INSERT INTO note(id_user, created_on, note, lat, lon) VALUES({}, {}, {}, {}, {}) RETURNING id;".format(id_user_field, created_on_field, note_field, lat_field, lon_field))
        sql_insert_name = """INSERT INTO pussy (id_user, created_on, name, is_active) VALUES (%s, %s, %s, %s) RETURNING id;"""
        data = (id_user_field, datetime.strptime(created_on_field,'%Y-%m-%dT%H:%M:%S'), name, active_status[1])
        cur.execute(sql_insert_name, data)
        
        # get the generated id back
        pussy_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()

        # close communication with the database
        cur.close()
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    # signal = "🪄🪄🪄 Заметка успешно сохранена с id: {}".format(pussy_id)
    print(pussy_id)
    return pussy_id

def select():
    conn = None
    pussy_id = None 

    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(
        host = "ec2-63-32-7-190.eu-west-1.compute.amazonaws.com",
        port = "5432",
        database = "d5789ofavjem2n",
        user = "dppxvycvjbbmxm",
        password = "919599b7ef2bd77ad97989e161038040010f70c679ff64d58ec36eee93c4e6bc"
    )
    
    # create a cursor
    cur = conn.cursor()

    # GET ALL PUSSIES
    sql_select_name = """SELECT DISTINCT name FROM pussy WHERE is_active=TRUE ORDER BY name;"""
    cur.execute(sql_select_name)
    select_data = cur.fetchall()
    conn.commit()
    # close communication with the database
    cur.close()
    pussy_lst = []
    for i, n in enumerate(select_data, 1):
        pussy_lst.append("{}. {}".format(i, n[0]))
    
    all_pussies = "\n".join(pussy_lst)
    all_pussies = all_pussies + "\n🐈‍"
    return(all_pussies)