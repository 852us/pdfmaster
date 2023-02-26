#!/usr/bin/python

import os
import time
import pikepdf
from pikepdf import Pdf
from tkinter import *
import tkinter.filedialog
from tkinter.scrolledtext import ScrolledText


def windows():
	global root
	global text
	root = Tk()
	screen_width = root.winfo_screenwidth()  # 缩放后的屏幕水平分辨率
	screen_height = root.winfo_screenheight()  # 缩放后的屏幕垂直分辨率
	print("ScreeN:{}x{}".format(screen_width, screen_height))
	root.geometry('{}x{}+0+0'.format(screen_width, screen_height))
	root.title('PDF编辑大师')
	root.state("zoomed") # 窗口最大化
	frame1 = Frame(root)
	frame1.pack(fill=BOTH, expand=YES, padx=10, pady=10)
	btn = Button(frame1, text='解密PDF文件', font=("楷体", 14, "bold"), bg="#AACCCC",
				  width=30, height=2, relief=RAISED, command=askfiles)
	btn.grid(row=0, column=0, sticky=W, padx=10)
	btn = Button(frame1, text='解密文件夹', font=("楷体", 14, "bold"), bg='#AACCCC',
				  width=30, height=2, relief=RAISED, command=askdirectory)
	btn.grid(row=0, column=1, sticky=W, padx=10)
	btn = Button(frame1, text='合并文件', font=("楷体", 14, "bold"), bg='#AACCCC',
				  width=30, height=2, relief=RAISED, command=askcombinefiles)
	btn.grid(row=0, column=2, sticky=W, padx=10)
	btn = Button(frame1, text='清除屏幕信息', font=("楷体", 14, "bold"), bg='#AACCCC',
				  width=30, height=2, relief=RAISED, command=cls)
	btn.grid(row=0, column=3, sticky=W, padx=10)
	frame2 = Frame(root)
	frame2.pack(fill=BOTH, expand=YES, padx=10, pady=10)
	lb = Label(frame2, font=("楷体", 14), fg="#FF0000", height=1,
			   text="解密PDF文件或文件夹中的所有PDF文件，可以解密许可口令,不能解密文档打开密码。"
					"源文件将被直接覆盖，请在解密前备份PDF文件。")
	separator = Frame(root, height=2, bd=1, relief="sunken")
	lb.pack(side=LEFT)
	separator.pack(fill="x", padx=0, pady=0)
	frame3 = Frame(root)
	frame3.pack(fill=BOTH, expand=YES, padx=10, pady=10)
	text = ScrolledText(frame3, font=("仿宋", 14), width=200, height=500,
				spacing1=5, spacing2=5, undo=True, autoseparators=True)
	text.tag_config('red', foreground='red', font=("仿宋", 14, 'bold'))
	text.tag_config('green', foreground='green', font=("仿宋", 14, 'bold'))
	text.pack(fill=BOTH, expand=NO, padx=0, pady=0)
	root.mainloop()


def askfiles():
	names = tkinter.filedialog.askopenfilenames(filetypes=[("PDF files", ".pdf")])
	if names == "":
		return
	for name in names:
		unlock_file(name)
	text_output("解密完毕!\n\n")


def askdirectory():
	name = tkinter.filedialog.askdirectory()
	if name == "":
		return
	unlock_directory(name)
	text_output("解密完毕!\n\n")


def askcombinefiles():
	names = tkinter.filedialog.askopenfilenames(filetypes=[("PDF files", ".pdf")])
	if names == "":
		return
	dst = tkinter.filedialog.asksaveasfilename(filetypes=[("PDF files", ".pdf")])
	if dst == "":
		return
	combine_pdf_files(names, dst)
	text_output("合并完毕!\n\n")


def text_output(string, tag='default'):
	text.insert(END, string, tag)
	text.focus_force()
	text.see(END)
	text.update()


def unlock_file(name):
	try:
		start_time = time.time()
		pdf = pikepdf.open(name, allow_overwriting_input=True)
		text_output("解密文件：【{}】：".format(name))
		pdf.save(name)
		end_time = time.time()
		text_output("写入{:,}字节，用时：{:,.3}秒。\n".format(os.path.getsize(name), end_time - start_time))
	except:
		text_output("打开文件：{}时出错...\n".format(name), 'red')


def unlock_directory(name = os.path.curdir):
	text_output("\n解密文件夹: 【{}】的文件...\n".format(name), 'green')
	itemlist = os.listdir(name)
	for item in itemlist:
		item = os.path.join(name, item)
		if os.path.isdir(item) :
			unlock_directory(item)
		if os.path.isfile(item):
			filename = os.path.splitext(item)
			if filename[1] == '.pdf':
				unlock_file(item)


def combine_pdf_files(sources, dst):
	pdf = Pdf.new()
	for name in sources:
		try:
			start_time = time.time()
			src = Pdf.open(name)
			end_time = time.time()
			pdf.pages.extend(src.pages)
			text_output("合并文件：【{}】：{:,}字节，用时：{:,.3}秒...\n".format(
				name, os.path.getsize(name), end_time-start_time))
		except:
			text_output("打开文件：{}时出错...\n".format(name), 'red')
	if os.path.splitext(dst)[1] == "":
		dst += ".pdf"
	pdf.save(dst)
	text_output("完成文件合并，写入{}：{:,}字节。\n".format(dst, os.path.getsize(dst)))


def cls():
	text.delete("1.0", "end")


if __name__ == '__main__':
	windows()
