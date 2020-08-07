from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton, MDIconButton
from kivymd.uix.screen import Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
import urllib3
from zipfile import ZipFile
import zipfile
import os
import hashlib
import gzip

Window.size = (360, 600)

tt = """
Screen:
    BoxLayout:
        orientation:"vertical"
        MDToolbar:
            title:"About SecureCheck"
            left_action_items:[["coffee",lambda x:app.help_fun()]]
            elevation:8
            pos_hint:{'center_x':0.5,'center_y':0.5} 
            mode:'end' 
"""

ttop = """
Screen:
    BoxLayout:
        orientation:"vertical"
        MDToolbar:
            title:"         SecureCheck"
            left_action_items:[["security",lambda x:app.help_fun()]]
            elevation:8
            pos_hint:{'center_x':0.5,'center_y':0.5} 
            mode:'end'   
        Widget:      
"""
us = """
MDTextField:
    hint_text:"File Path"
    pos_hint:{'center_x':0.4,'center_y':0.7}
    size_hint:(None,None)
    width:200
    height:5
"""


class SecureCheck(MDApp):
    def build(self):
        self.theme_cls.primary_pallet = "Green"
        self.theme_cls.theme_style = "Dark"
        screen = Screen()
        icon2 = MDIconButton(icon="file-upload-outline",
                             pos_hint={'center_x': 0.8, 'center_y': 0.7}, on_release=self.example_fun)
        top = Builder.load_string(ttop)
        l2 = MDLabel(text="Scan File", pos=(40, 178), font_style="Body2", theme_text_color="Primary")
        self.f = Builder.load_string(us)
        l4 = MDRectangleFlatButton(text="Update", pos_hint={'center_x': 0.747, 'center_y': 0.2},
                                   size_hint=(None, None),
                                   width=5, height=2, on_release=self.update)
        toptoolbar = Builder.load_string(tt)
        bt1 = MDRectangleFlatButton(text='Scan', pos_hint={'center_x': 0.4, 'center_y': 0.6}, size_hint=(None, None),
                                    width=5, height=2, on_release=self.start_scan)
        bt2 = MDRectangleFlatButton(text='Delete', pos_hint={'center_x': 0.74, 'center_y': 0.6}, size_hint=(None, None),
                                    width=5, height=2, on_release=self.delete_infected)
        screen.add_widget(toptoolbar)
        screen.add_widget(l2)
        screen.add_widget(self.f)
        screen.add_widget(l4)
        screen.add_widget(bt1)
        screen.add_widget(bt2)
        screen.add_widget(top)
        screen.add_widget(icon2)
        return screen

    # related to scan file
    def start_scan(self, obj):
        global path
        global md5sum
        if self.f.text == "":
            path = "Please Enter File Path"
        elif os.path.isfile(self.f.text) or zipfile.is_zipfile(self.f.text):
            path = self.f.text
        else:
            md5sum = self.f.text
            path = md5sum

        cb = MDFlatButton(text="EDIT", on_release=self.close_dialog)
        ed = MDFlatButton(text="NEXT", on_release=self.next)
        self.dialog = MDDialog(title="FIle Path", text=path, buttons=[cb, ed],
                               size_hint=(0.7, 1))
        self.dialog.open()
        # print(self.f.text)

    def next(self, obj):
        global x
        try:
            if zipfile.is_zipfile(str(self.f.text).strip()):
                with ZipFile(str(self.f.text).strip(), 'r')as zip:
                    for i in zip.infolist():
                        sd = zip.read(i.filename)
                        mdx2 = hashlib.md5(sd).hexdigest()
                        with gzip.open("batadata.txt.gz", "rb")as writef:
                            xy = writef.read()
                        bindata = bytearray(xy)
                        if bytes(mdx2, 'utf-8') in bindata:
                            ok = MDFlatButton(text="OK", on_release=self.go_back)
                            self.x = MDDialog(text="Infected\n md5 : " + mdx2, buttons=[ok], size_hint=(0.7, 1))
                            self.x.open()
                        else:
                            ok = MDFlatButton(text="OK", on_release=self.go_back)
                            self.x = MDDialog(text="Not Infected\n md5 : " + mdx2, buttons=[ok], size_hint=(0.7, 1))
                            self.x.open()
                        # self.dialog.dismiss()
            elif os.path.isfile(self.f.text):
                with open(str(path).strip(), "rb") as r:
                    sum = r.read()
                mdx = hashlib.md5(sum).hexdigest()
                with gzip.open("batadata.txt.gz", "rb")as writef:
                    xy = writef.read()
                bindata = bytearray(xy)
                if bytes(mdx, 'utf-8') in bindata:
                    ok = MDFlatButton(text="OK", on_release=self.go_back)
                    self.x = MDDialog(text="Infected\n md5 : " + mdx, buttons=[ok], size_hint=(0.7, 1))
                    self.x.open()
                else:
                    ok = MDFlatButton(text="OK", on_release=self.go_back)
                    self.x = MDDialog(text="Not Infected\n md5 : " + mdx, buttons=[ok], size_hint=(0.7, 1))
                    self.x.open()
                # self.dialog.dismiss()
            elif os.path.isdir(self.f.text):
                ok = MDFlatButton(text="OK", on_release=self.go_back)
                self.x = MDDialog(text="It Is Directory Please Enter correct Path of the file", buttons=[ok],
                                  size_hint=(0.7, 1))
                self.x.open()

            else:
                with gzip.open("batadata.txt.gz", "rb")as writef:
                    xy = writef.read()
                bindata = bytearray(xy)
                if bytes(md5sum, 'utf-8') in bindata:
                    ok = MDFlatButton(text="OK", on_release=self.go_back)
                    self.x = MDDialog(text="Infected\n md5 : " + md5sum, buttons=[ok], size_hint=(0.7, 1))
                    self.x.open()
                else:
                    ok = MDFlatButton(text="OK", on_release=self.go_back)
                    self.x = MDDialog(text="Not Infected\n md5 : " + md5sum, buttons=[ok], size_hint=(0.7, 1))
                    self.x.open()

        except:
            ok = MDFlatButton(text="OK", on_release=self.go_back)
            self.x = MDDialog(text="No Such File Please Enter correct Path", buttons=[ok], size_hint=(0.7, 1))
            self.x.open()

    def go_back(self, obj):
        self.x.dismiss()
        self.dialog.dismiss()

    def close_dialog(self, obj):
        self.dialog.dismiss()

    # help button content
    def help_fun(self):
        cdt1 = MDFlatButton(text="close", on_release=self.close_dt1)
        self.dt1 = MDDialog(title="About SecureCheck",
                            text="1.Safeguards Your System\n2.Dectect Infected File\n3.Eleminate Infected File\n4.Can also Check md5 on\n   virustotal to know if it is\n   working write or not\n\n  Made By: Abhay Mishra",
                            pos_hint={'center_x': 0.5, 'center_y': 0.5},
                            size_hint=(0.7, 1), buttons=[cdt1])
        self.dt1.open()

    # example button content
    def example_fun(self, ob):
        cdt1 = MDFlatButton(text="close", on_release=self.close_dt1)
        # ib = MDIconButton(icon="security", pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.dt1 = MDDialog(title="Example Infected MD5_Checksums",
                            text="1.1effb3351bd7222304e188421c52969a\n\n2.2ceee5b70dd6d020cffdcff586cafa0b\n\n"
                                 "3.69c0b64b41f318a4a959d70ea9486157\n\n4.537219e6e52cbbcdae6fdde1e47c9033\n\n5.772c7545a4eade7add5c89654648bbca",
                            pos_hint={'center_x': 0.5, 'center_y': 0.5},
                            size_hint=(0.95, 1), buttons=[cdt1])
        self.dt1.open()

    def close_dt1(self, ob):
        self.dt1.dismiss()

    # file Update button content
    def update(self, ob):
        ok12 = MDFlatButton(text="Update", on_release=self.goback22)
        cl = MDFlatButton(text="Close", on_release=self.goback2)
        self.z2 = MDDialog(title="Goto this Link ",
                           text='https://virusshare.com/hashes.4n6 \n\nIf their is any file after 383\n'
                                ' click on update else close',
                           size_hint=(0.7, 1), buttons=[ok12, cl])
        self.z2.open()

    def goback22(self, ob):
        try:
            res = urllib3.PoolManager()
            response = res.request('GET', 'https://virusshare.com/hashes/')
            with open('files1', 'ab+') as f:
                f.write(response.data)
                f.close()
            num_of_files = sum(1 for line in open('files1'))
            # print(num_of_files,",",num_of_files - 213,",", num_of_files - 13)
            os.remove("files1")

            for i in range(384, num_of_files - 12):
                fileNumber = '%05d' % i
                url = ('https://virusshare.com/hashes/VirusShare_%s.md5') % (fileNumber)
                # print(url)
                http1 = urllib3.PoolManager()
                HTML1 = http1.request('GET', url)  # make requests to website
                with open('recent10.txt', 'ab')as fr:
                    fr.write(HTML1.data)
                    fr.close()
                try:
                    file = open('recent10.txt', 'r')
                    output_stream = []
                    input_stream_lines = (file.read()).split("\n")
                    file.close()
                    for line in input_stream_lines:
                        if "#" in line:
                            pass
                        else:
                            output_stream.append(line)
                    # print(type(output_stream))
                    with open("betadata.txt", "a+") as wr:
                        # wr.write("\n")
                        wr.writelines("%s\n" % i for i in output_stream)
                        wr.close()
                    with open("betadata.txt", "rb")as rw:
                        rwx = rw.read()
                    bindata2 = bytearray(rwx)
                    with gzip.open("batadata.txt.gz", "ab+")as wr1:
                        wr1.write(bindata2)
                        rw.close()
                except IOError:
                    ok12 = MDFlatButton(text="OK", on_release=self.goback2)
                    self.z2 = MDDialog(text='\033[91m' + "Error: can\'t find file or read data." + '\033[0m',
                                       buttons=[ok12], size_hint=(0.7, 1))
                    self.z2.open()
                    exit(0)
                else:
                    ok12 = MDFlatButton(text="OK", on_release=self.goback3)
                    self.z3 = MDDialog(
                        text='\x1b[6;30;42m' + "Unused charactors removed succesfully!!!\n" + '\x1b[0m' + fileNumber,
                        buttons=[ok12], size_hint=(0.7, 1))
                    self.z3.open()
            ok122 = MDFlatButton(text="OK", on_release=self.goback4)
            self.z4 = MDDialog(text="Updated", buttons=[ok122], size_hint=(0.7, 1))
            self.z4.open()
        except:
            print("Done")

    def goback2(self, obj):
        self.z2.dismiss()

    def goback3(self, obj):
        self.z3.dismiss()
        try:
            os.remove("recent10.txt")
            os.remove("beta_data.py")
        except:
            pass

    def goback4(self, obj):
        self.z4.dismiss()
        self.z2.dismiss()

    # related to deletefile
    def delete_infected(self, ob):
        dl = MDFlatButton(text="Delete", on_release=self.delete)
        self.del1_dialog = MDDialog(title="Infected File Name", text=self.f.text,
                                    pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                    size_hint=(0.7, 1), buttons=[dl])
        self.del1_dialog.open()

    def delete(self, ob):
        try:
            os.remove(str(self.f.text).strip())
            self.del1_dialog.dismiss()
        except:
            ok1 = MDFlatButton(text="OK", on_release=self.back)
            self.y = MDDialog(text="No Such File Please Enter correct Path", buttons=[ok1], size_hint=(0.7, 1))
            self.y.open()

    def back(self, ob):
        self.del1_dialog.dismiss()
        self.y.dismiss()


SecureCheck().run()
