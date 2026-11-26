
from database import Database


class Mahasiswa:

    def __init__(self):
        self.db = Database()

    # CREATE: Menambahkan mahasiswa
    def tambah(self, nama, nim, jurusan, email):
        conn = self.db.get_connection()

        try:
            cursor = conn.cursor()

            sql = """
                INSERT INTO mahasiswa
                (nama, nim, jurusan, email)
                VALUES (%s, %s, %s, %s)
            """

            cursor.execute(
                sql,
                (nama, nim, jurusan, email)
            )

            conn.commit()
            return True

        except Exception:
            conn.rollback()
            raise

        finally:
            cursor.close()
            conn.close()

    # READ: Menampilkan semua mahasiswa
    def tampilkan(self):
        conn = self.db.get_connection()

        try:
            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT * FROM mahasiswa
                ORDER BY id DESC
            """)

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    # SEARCH: Mencari mahasiswa
    def cari_data(self, keyword=""):
        conn = self.db.get_connection()

        try:
            cursor = conn.cursor(dictionary=True)

            sql = """
                SELECT * FROM mahasiswa
                WHERE nama LIKE %s
                   OR nim LIKE %s
                   OR jurusan LIKE %s
                ORDER BY id DESC
            """

            pola = f"%{keyword}%"

            cursor.execute(
                sql,
                (pola, pola, pola)
            )

            return cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    # SEARCH: Mencari satu mahasiswa berdasarkan ID
    def cari(self, id):
        conn = self.db.get_connection()

        try:
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                "SELECT * FROM mahasiswa WHERE id = %s",
                (id,)
            )

            return cursor.fetchone()

        finally:
            cursor.close()
            conn.close()

    # UPDATE: Mengubah data mahasiswa
    def update(self, id, nama, nim, jurusan, email):
        conn = self.db.get_connection()

        try:
            cursor = conn.cursor()

            sql = """
                UPDATE mahasiswa
                SET nama = %s,
                    nim = %s,
                    jurusan = %s,
                    email = %s
                WHERE id = %s
            """

            cursor.execute(
                sql,
                (nama, nim, jurusan, email, id)
            )

            conn.commit()
            return True

        except Exception:
            conn.rollback()
            raise

        finally:
            cursor.close()
            conn.close()

    # DELETE: Menghapus mahasiswa
    def hapus(self, id):
        conn = self.db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM mahasiswa WHERE id = %s",
                (id,)
            )

            conn.commit()
            return True

        except Exception:
            conn.rollback()
            raise

        finally:
            cursor.close()
            conn.close()
