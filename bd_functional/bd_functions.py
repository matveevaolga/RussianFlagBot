import docx2txt, base64
import pymysql
from bd_connection import DBConnection


def get_db_cursor():
    try:
        connect = DBConnection()
        connect.open_connect()
        cursor = connect.get_cursor()
    except pymysql.Error:
        print("failed to connect to database", "get_additional_data_from_db")
        return None, None
    return cursor, connect


def get_flags_data_from_db(searched_id: int) -> dict:
    cursor, connect = get_db_cursor()
    if not cursor:
        return {}
    try:
        cursor.execute(f"select * from historyperiods where idPeriod = {searched_id};")
        searched_id, name, pic, time = cursor.fetchone()
        flag_info = ""
        cursor.execute(f"select flagInfo from flagsinfo where idFlagPeriod = {searched_id};")
        for info in cursor.fetchall():
            flag_info += info[0]
    except pymysql.Error:
        print("failed to commit sql-query", "get_flags_data_from_db")
        return {}
    info_dict = {"name": name, "photo": pic, "time": time, "info": flag_info}
    connect.close_connect()
    return info_dict


def get_additional_data_from_db(searched_id: int) -> dict:
    cursor, connect = get_db_cursor()
    if not cursor:
        return {}
    try:
        cursor.execute(f"select * from additionalinfo where idInfo = {searched_id};")
        searched_id, name, pic, flag_info = cursor.fetchone()
        flag_info = ""
        cursor.execute(f"select infoText from additionalinfo where idInfo = {searched_id};")
        for text in cursor.fetchall():
            flag_info += text[0]
    except pymysql.Error:
        print("failed to commit sql-query", "get_additional_data_from_db")
        return {}
    info_dict = {"name": name, "photo": pic, "info": flag_info}
    connect.close_connect()
    return info_dict


def get_pics_data_from_docx(temp_photo_dir: str, path_to_docx: str) -> list:
    # temp_photo_dir - путь до директории, в которую хотим сохранить фото из файла docx
    # path_to_docx - путь до файла docx, из которого хотим получить данные
    try:
        text = docx2txt.process(path_to_docx, temp_photo_dir)
        text = [x for x in text.split('\n') if x]
        arr_text = [(text[i].strip().replace('-', '–'), text[i + 1].strip().replace('-', '–')) for i in range(0, len(text)-1, 2)]
        return arr_text
    except IndexError:
        print("Invalid data in docx file", "get_pics_data_from_docx")


def get_text_data_from_docx(path_to_docx: str) -> list:
    # path_to_docx - путь до файла docx, из которого хотим получить данные
    try:
        text = docx2txt.process(path_to_docx)
        text = [x for x in text.split('\n') if x]
        arr_text = [text[i].strip().replace('-', '–') for i in range(len(text))]
        return arr_text
    except IndexError:
        print("Invalid data in docx file", get_text_data_from_docx)


def insert_additional_data_to_db(temp_photo_dir: str, path_to_docx: str) -> None:
    cursor, connect = get_db_cursor()
    if not cursor:
        return
    arr_text = get_pics_data_from_docx(temp_photo_dir, path_to_docx)
    for i in range(len(arr_text)):
        name, text = arr_text[i]
        with open(f"{temp_photo_dir}/image{i + 1}.jpeg", "rb") as pic:
            pic = base64.b64encode(pic.read()).decode()
            try:
                cursor.execute(f"insert into additionalinfo (infoName, infoPicture, infoText) "
                           f"values ('{name}', '{pic}', '{text}');")
            except pymysql.Error:
                print("failed to commit sql-query", "insert_additional_data_to_db")
                return
    connect.close_connect()


def insert_periods_data_to_db(temp_photo_dir: str, path_to_docx: str) -> None:
    cursor, connect = get_db_cursor()
    if not cursor:
        return
    arr_text = get_pics_data_from_docx(temp_photo_dir, path_to_docx)
    for i in range(len(arr_text)):
        name, text = arr_text[i]
        with open(f"{temp_photo_dir}/image{i + 1}.jpeg", "rb") as pic:
            pic = base64.b64encode(pic.read()).decode()
            try:
                cursor.execute(f"insert into historyperiods (periodName, periodFlag, periodTime) "
                               f"values ('{name}', '{pic}', '{text}');")
            except pymysql.Error:
                print("failed to commit sql-query", "insert_periods_data_to_db")
                return
    connect.close_connect()


def insert_flags_data_to_db(path_to_docx: str, searched_id: int) -> None:
    cursor, connect = get_db_cursor()
    if not cursor:
        return
    arr_text = get_text_data_from_docx(path_to_docx)
    for i in range(len(arr_text)):
        name, text = arr_text[i]
        try:
            cursor.execute(f"insert into flagsinfo (idFlagPeriod, flagInfo) "
                           f"values ('{searched_id}', '{text}');")
        except pymysql.Error:
            print("failed to commit sql-query", "insert_flags_data_to_db")
            return
    connect.close_connect()
