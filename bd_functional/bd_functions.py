import docx2txt, base64, multipledispatch
from bd_connection import DBConnection


@multipledispatch.dispatch(int)
def get_data_from_db(searched_id: int) -> dict:
    connect = DBConnection()
    connect.open_connect()
    cursor = connect.get_cursor()
    cursor.execute(f"select * from historyperiods where idPeriod = {searched_id};")
    searched_id, name, pic, time = cursor.fetchone()
    flag_info = ""
    cursor.execute(f"select flagInfo from flagsinfo where idFlagPeriod = {searched_id};")
    for info in cursor.fetchall():
        flag_info += info[0]
    info_dict = {"name": name, "photo": pic, "time": time, "info": flag_info}
    connect.close_connect()
    return info_dict


@multipledispatch.dispatch(int, bool)
def get_data_from_db(searched_id: int, add_flag: bool) -> dict:
    connect = DBConnection()
    connect.open_connect()
    cursor = connect.get_cursor()
    cursor.execute(f"select * from additionalinfo where idInfo = {searched_id};")
    searched_id, name, pic, flag_info = cursor.fetchone()
    flag_info = ""
    cursor.execute(f"select infoText from additionalinfo where idInfo = {searched_id};")
    for text in cursor.fetchall():
        flag_info += text[0]
    info_dict = {"name": name, "photo": pic, "info": flag_info}
    connect.close_connect()
    return info_dict


@multipledispatch.dispatch(str, str)
def get_data_from_docx(temp_photo_dir: str, path_to_docx: str) -> list:
    # temp_photo_dir - путь до директории, в которую хотим сохранить фото из файла docx
    # path_to_docx - путь до файла docx, из которого хотим получить данные
    text = docx2txt.process(path_to_docx, temp_photo_dir)
    text = [x for x in text.split('\n') if x]
    arr_text = [(text[i].strip().replace('-', '–'), text[i + 1].strip().replace('-', '–')) for i in range(0, len(text)-1, 2)]
    return arr_text


@multipledispatch.dispatch(str, str, int)
def get_data_from_docx(temp_photo_dir: str, path_to_docx: str, searched_id: int) -> list:
    # temp_photo_dir - путь до директории, в которую хотим сохранить фото из файла docx
    # path_to_docx - путь до файла docx, из которого хотим получить данные
    text = docx2txt.process(path_to_docx, temp_photo_dir)
    text = [x for x in text.split('\n') if x]
    arr_text = [text[i].strip().replace('-', '–') for i in range(len(text))]
    return arr_text


@multipledispatch.dispatch(str, str, bool)
def insert_data_to_db(temp_photo_dir: str, path_to_docx: str, add_flag: bool) -> None:
    connect = DBConnection()
    connect.open_connect()
    cursor = connect.get_cursor()
    arr_text = get_data_from_docx(temp_photo_dir, path_to_docx)
    for i in range(len(arr_text)):
        name, text = arr_text[i]
        with open(f"{temp_photo_dir}/image{i + 1}.jpeg", "rb") as pic:
            pic = base64.b64encode(pic.read()).decode()
            cursor.execute(f"insert into additionalinfo (infoName, infoPicture, infoText) "
                           f"values ('{name}', '{pic}', '{text}');")
    connect.close_connect()


@multipledispatch.dispatch(str, str)
def insert_data_to_db(temp_photo_dir: str, path_to_docx: str) -> None:
    connect = DBConnection()
    connect.open_connect()
    cursor = connect.get_cursor()
    arr_text = get_data_from_docx(temp_photo_dir, path_to_docx)
    for i in range(len(arr_text)):
        name, text = arr_text[i]
        with open(f"{temp_photo_dir}/image{i + 1}.jpeg", "rb") as pic:
            pic = base64.b64encode(pic.read()).decode()
            cursor.execute(f"insert into historyperiods (periodName, periodFlag, periodTime) "
                           f"values ('{name}', '{pic}', '{text}');")
    connect.close_connect()


@multipledispatch.dispatch(str, str, int)
def insert_data_to_db(temp_photo_dir: str, path_to_docx: str, searched_id: int) -> None:
    connect = DBConnection()
    connect.open_connect()
    cursor = connect.get_cursor()
    arr_text = get_data_from_docx(temp_photo_dir, path_to_docx, searched_id)
    for i in range(len(arr_text)):
        name, text = arr_text[i]
        cursor.execute(f"insert into flagsinfo (idFlagPeriod, flagInfo) "
                       f"values ('{searched_id}', '{text}');")
    connect.close_connect()
