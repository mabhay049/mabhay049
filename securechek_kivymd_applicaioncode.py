from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton, MDIconButton
from kivymd.uix.screen import Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList
from kivy.uix.scrollview import ScrollView
from zipfile import ZipFile
import zipfile
import os
import hashlib
import gzip

# from securedata import tt,us
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
        #icon = MDIconButton(icon="security", pos_hint={'center_x': 0.1, 'center_y': 0.94})
        icon2 = MDIconButton(icon="file-upload-outline",
                             pos_hint={'center_x': 0.8, 'center_y': 0.7},on_release=self.example_fun)
        top = Builder.load_string(ttop)
        #l1 = MDLabel(text="SecureCheck", pos=(110, 265), font_style="H5", bold=True, underline=True,theme_text_color="Primary")
        l2 = MDLabel(text="Scan File", pos=(40, 178), font_style="Body2", theme_text_color="Primary")
        # l3 = MDLabel(text="Infected Files", pos=(25, 115), font_style="Body2", theme_text_color="Primary")
        self.f = Builder.load_string(us)
        l4 = MDRectangleFlatButton(text="Update", pos_hint={'center_x': 0.747, 'center_y': 0.45},
                                   size_hint=(None, None),
                                   width=5, height=2, on_release=self.file_list)
        toptoolbar = Builder.load_string(tt)
        bt1 = MDRectangleFlatButton(text='Scan', pos_hint={'center_x': 0.4, 'center_y': 0.6}, size_hint=(None, None),
                                    width=5, height=2, on_release=self.start_scan)
        bt2 = MDRectangleFlatButton(text='Delete', pos_hint={'center_x': 0.74, 'center_y': 0.6}, size_hint=(None, None),
                                    width=5, height=2, on_release=self.delete_infected)
        screen.add_widget(toptoolbar)
        #screen.add_widget(l1)
        screen.add_widget(l2)
        # screen.add_widget(l3)
        screen.add_widget(l4)
        screen.add_widget(self.f)
        screen.add_widget(bt1)
        screen.add_widget(bt2)
        screen.add_widget(top)
        #screen.add_widget(icon)
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
                        with gzip.open("data.py.gz", "rb")as writef:
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
                with gzip.open("data.py.gz", "rb")as writef:
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

            else:
                with gzip.open("data.py.gz", "rb")as writef:
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
        # ib = MDIconButton(icon="security", pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.dt1 = MDDialog(title="About SecureCheck",
                            text="1.Safeguards Your System\n2.Dectect Infected File\n3.Eleminate Infected File\n4.Can also Check md5 on\n   virustotal to know if it is\n   working write or not\n\n  Made By: Abhay Mishra",
                            pos_hint={'center_x': 0.5, 'center_y': 0.5},
                            size_hint=(0.7, 1), buttons=[cdt1])
        self.dt1.open()

    # example button content
    def example_fun(self,ob):
        cdt1 = MDFlatButton(text="close", on_release=self.close_dt1)
        # ib = MDIconButton(icon="security", pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.dt1 = MDDialog(title="Example Infected MD5_Checksums",
                            text="1:a224a3894a81147e22974598b237ae70\n\n2:920f62433e0a870c81d75bcd0d49d9f0\n\n"
                                 "3:920f6370f4026581b7e3fca72bedd07e\n\n4:a224a92cbc5fbac29a164400b5619cb6\n\n"
                                 "5:a224aac10c5ecd3f3db7292e7ab567a1",
                            pos_hint={'center_x': 0.5, 'center_y': 0.5},
                            size_hint=(0.95, 1), buttons=[cdt1])
        self.dt1.open()

    def close_dt1(self, ob):
        self.dt1.dismiss()

    # file info button content
    def file_list(self, obj):
        try:
            with open(self.f.text, "rb") as re:
                re.close()
            okf = MDFlatButton(text="OK", on_release=self.close_info)
            self.info = MDDialog(title="Infected File Information", text="MD5_Checksum:" + "2", buttons=[okf],
                                 pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint=(0.7, 1))
            self.info.open()
        except:
            ok12 = MDFlatButton(text="OK", on_release=self.back1)
            self.z = MDDialog(text="No Such File Please Enter correct Path", buttons=[ok12], size_hint=(0.7, 1))
            self.z.open()

    def back1(self, ob):
        self.z.dismiss()

    def close_info(self, ob):
        self.info.dismiss()

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
