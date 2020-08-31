import psycopg2
import tkinter as tk

# SQL部分

db_info = "hoge"


def exec_query(query):
    with psycopg2.connect(db_info) as connection:
        with connection.cursor() as cur:
            cur.execute(query)
            try:
                res = cur.fetchall()
            except:
                return None
    return res


def search_sent(word):
    rslt = exec_query(
        "select sentence from sentences where sentence like '% {} %' limit 20".format(word))
    return [elem[0] for elem in rslt]

# GUI部分
# 検索結果表示用のtextbox


class SbTextFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        text = tk.Text(self, wrap='none', undo=True)
        x_sb = tk.Scrollbar(self, orient='horizontal')
        y_sb = tk.Scrollbar(self, orient='vertical')
        x_sb.config(command=text.xview)
        y_sb.config(command=text.yview)
        text.config(xscrollcommand=x_sb.set, yscrollcommand=y_sb.set)
        text.grid(column=0, row=0, sticky='nsew')
        x_sb.grid(column=0, row=1, sticky='ew')
        y_sb.grid(column=1, row=0, sticky='ns')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.text = text
        self.x_sb = x_sb
        self.y_sb = y_sb


def get_word_and_search():
    word = txt.get()
    sents = search_sent(word)
    textframe.text.delete("1.0", "end")
    textframe.text.insert("1.0", "\n\n".join(sents))
    # 該当単語にハイライトを作る部分
    for i, sent in enumerate(sents):
        ind = 2*i+1
        s = sent.find(word)
        t = s+len(word)
        textframe.text.tag_add("highlight", str(
            ind)+"."+str(s), str(ind)+"."+str(t))
        textframe.text.tag_config("highlight", foreground="red")


# Tkクラス生成
root = tk.Tk()
# 画面サイズ
root.geometry('1400x600')
# 画面タイトル
root.title('例文検索')
# 表示
# テキストボックス
lbl = tk.Label(text='検索ワード')
lbl.pack(padx=20, side='left')
txt = tk.Entry(width=20)
txt.pack(padx=20, side='left')

# 検索ボタン設置
btn = tk.Button(root, text='検索', command=get_word_and_search)
btn.pack(padx=20, side='left')

# 結果出力
textframe = SbTextFrame(root)
textframe.pack(side="top", expand=True)

root.mainloop()
