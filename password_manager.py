import tkinter as tk
from tkinter import font
from tkinter import messagebox
import string
import random

class StrongPassword:
    def generate(self):
        password = []
        while len(password) < 10:
            choice = random.randint(0, 2)
            if choice == 0:
                password.append(random.choice(string.digits))
            elif choice == 1:
                password.append(random.choice(string.ascii_uppercase))
            else:
                password.append(random.choice(string.ascii_lowercase))
        if self.IsStrong(password):
          return ''.join(password)
        else:
            return self.generate()

    def IsStrong(self, password):
        if len(password) < 8:
            return False
        if not any(char.isupper() for char in password):
            return False
        if not any(char.islower() for char in password):
            return False
        if not any(char.isdigit() for char in password):
            return False
        return True

    def __hash__(self) -> int:
       pass

class SavePassword:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.file = open('file.txt', 'a+', encoding='utf-8')
        return self

    def SavePassword(self, service_name, password):
        self.file.write(f'{service_name}: {password}' + '\n')

    def ReadPassword(self):
      self.file.seek(0)
      passwords = self.file.read()
      return passwords

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()


class MyApp(StrongPassword, SavePassword):
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Менеджер Паролей")
        self.window.geometry("1920x1080")
        my_font = font.Font(size=20)

        self.label = tk.Label(self.window, text="Сервис:", font=my_font)
        self.label.grid(row=0, column=0, padx=50, pady=10)

        self.entry = tk.Entry(self.window, font=my_font)
        self.entry.grid(row=0, column=4, padx=5, pady=10)

        self.label1 = tk.Label(self.window, text="Пароль (рекомендованный):", font=my_font)
        self.label1.grid(row=0, column=8, padx=100, pady=10)

        self.entry1 = tk.Entry(self.window, font=my_font)
        self.entry1.insert(0, f"{super().generate()}")
        self.entry1.grid(row=0, column=15, padx=5, pady=10)

        self.button = tk.Button(self.window, text="Сохранить", font=my_font, command=self.button_clicked)
        self.button.grid(row=0, column=16, padx=40, pady=10)

        self.text = tk.Text(self.window, font=my_font, width=40, height=10)
        self.text.grid(row=1, column=0, columnspan=17, padx=20, pady=25)
        self.text.configure(state="disabled")

        self.label3 = tk.Label(self.window, text="Чтоб удалить пароль нажмите привую кнопку мыши", font=my_font)
        self.label3.grid(row=5, column=8, padx=80, pady=10)

        self.text.bind("<Button-3>", self.delete_password)
        self.entry.bind("<Return>", self.button_clicked)

        self.show_info()

    def button_clicked(self, event=None):
      service_name = self.entry.get()
      password = self.entry1.get()
      if len(service_name) == 0 or len(password) == 0:
        messagebox.showinfo("Предупреждение", "Пустое поле")
      else:
        if not super().IsStrong(password):
            messagebox.showinfo("Предупреждение", "Пароль не надежный, но будет сохранен")
        with self as sp:
            sp.SavePassword(service_name, password)
            passwords = sp.ReadPassword()
            self.text.configure(state="normal")
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.END, passwords)
            self.text.configure(state="disabled")
        self.entry.delete(0, tk.END)
        self.entry1.delete(0, tk.END)
        new_password = super().generate()
        self.entry1.insert(tk.END, new_password)


    def show_info(self):
        self.text.configure(state="normal")
        self.text.delete('1.0', tk.END)
        with SavePassword(self.__class__.__name__) as sp:
            passwords = sp.ReadPassword()
            self.text.configure(state="normal")
            self.text.insert(tk.END, passwords)
            self.text.configure(state="disabled")


    def delete_password(self, event):
      self.text.config(state="normal")
      index = self.text.index(tk.CURRENT + " linestart")
      self.text.delete(index, index + " lineend")
      self.text.config(state="disabled")
      del_index = int(float(index))-1

      with open('file.txt', 'r', encoding='utf-8') as file:
          passwords = [i.rstrip('\n') for i in file.readlines()]
          file.seek(0)

      if del_index < len(passwords):
        del passwords[del_index]

        with open('file.txt', 'w', encoding='utf-8') as file:
            for i in passwords:
                file.write(i + "\n")
        self.show_info()
      


    def run(self):
      self.window.mainloop()



app = MyApp()
app.run()
