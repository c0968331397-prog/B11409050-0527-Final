import json
import os


DATA_FILE = "books.json"


class LibraryManager:
    def __init__(self):
        self.book_list = []
        self._load_from_file()

    def _load_from_file(self):
        if not os.path.exists(DATA_FILE):
            return
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                self.book_list = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"[警告] 無法讀取資料檔案：{e}，以空白資料庫啟動。")
            self.book_list = []

    def save_to_file(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.book_list, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"[錯誤] 儲存失敗：{e}")

    def is_isbn_exists(self, isbn):
        return any(book["isbn"] == isbn for book in self.book_list)

    def add_book(self, title, isbn, status):
        if not title.strip():
            print("[錯誤] 書名不可為空。")
            return
        if not isbn.strip().isdigit():
            print("[錯誤] ISBN 只能包含數字。")
            return
        if self.is_isbn_exists(isbn):
            print(f"[錯誤] ISBN {isbn} 已存在，無法重複新增。")
            return
        self.book_list.append({"title": title, "isbn": isbn, "status": status})
        print(f"[成功] 已新增書籍：{title} (ISBN: {isbn})")

    def show_books(self):
        if not self.book_list:
            print("[提示] 目前書庫中沒有任何書籍。")
            return
        print(f"--- 書籍清單（共 {len(self.book_list)} 筆）---")
        for idx, book in enumerate(self.book_list, start=1):
            print(f"[{idx}] 書名: {book['title']:<16} | ISBN: {book['isbn']} | 狀態: {book['status']}")

    def borrow_book(self, isbn):
        for book in self.book_list:
            if book["isbn"] == isbn:
                if book["status"] == "borrowed":
                    print(f"[提示] 書籍 ISBN {isbn} 目前已被借出。")
                else:
                    book["status"] = "borrowed"
                    print(f"[成功] 書籍 ISBN {isbn} 狀態已更新為「borrowed」。")
                return
        print(f"[錯誤] 找不到 ISBN 為 {isbn} 的書籍。")

    def run(self):
        print("=== 圖書館管理系統 v1.0 ===")
        print("指令：add <書名>/<ISBN>/<狀態> | show | borrow <ISBN> | exit")
        while True:
            try:
                command = input("> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n[系統] 偵測到中斷，儲存資料並關閉。")
                self.save_to_file()
                break

            if command == "exit":
                self.save_to_file()
                print("[系統] 資料已儲存，系統關閉。")
                break

            elif command.startswith("add "):
                parts = command[4:].split("/")
                if len(parts) == 3:
                    self.add_book(parts[0], parts[1], parts[2])
                else:
                    print("[錯誤] 格式錯誤，請使用：add <書名>/<ISBN>/<狀態>")

            elif command == "show":
                self.show_books()

            elif command.startswith("borrow "):
                target_isbn = command[7:].strip()
                self.borrow_book(target_isbn)

            elif command == "":
                continue

            else:
                print("[錯誤] 未知指令，請輸入 add / show / borrow / exit。")


if __name__ == "__main__":
    manager = LibraryManager()
    manager.run()
