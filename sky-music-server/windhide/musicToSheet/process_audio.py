import json
import os

import pretty_midi

from windhide.musicToSheet.transfer_MID import inference
from windhide.static.global_variable import GlobalVariable
from windhide.utils.path_util import getResourcesPath

# 15个音符与键盘按键的映射
note_to_key = {"_C_c¹":{36:'1Key0',38:'1Key1',40:'1Key2',41:'1Key3',43:'1Key4',45:'1Key5',47:'1Key6',48:'1Key7',50:'1Key8',52:'1Key9',53:'1Key10',55:'1Key11',57:'1Key12',59:'1Key13',60:'1Key14'},"c_c²":{48:'1Key0',50:'1Key1',52:'1Key2',53:'1Key3',55:'1Key4',57:'1Key5',59:'1Key6',60:'1Key7',62:'1Key8',64:'1Key9',65:'1Key10',67:'1Key11',69:'1Key12',71:'1Key13',72:'1Key14'},'c¹_c³':{60:'1Key0',62:'1Key1',64:'1Key2',65:'1Key3',67:'1Key4',69:'1Key5',71:'1Key6',72:'1Key7',74:'1Key8',76:'1Key9',77:'1Key10',79:'1Key11',81:'1Key12',83:'1Key13',84:'1Key14'},"c²_c⁴":{72:'1Key0',74:'1Key1',76:'1Key2',77:'1Key3',79:'1Key4',81:'1Key5',83:'1Key6',84:'1Key7',86:'1Key8',88:'1Key9',89:'1Key10',91:'1Key11',93:'1Key12',95:'1Key13',96:'1Key14'},"c³_c⁵":{84:'1Key0',86:'1Key1',88:'1Key2',89:'1Key3',91:'1Key4',93:'1Key5',95:'1Key6',96:'1Key7',98:'1Key8',100:'1Key9',101:'1Key10',103:'1Key11',105:'1Key12',107:'1Key13',108:'1Key14'},"_C_c²":{36:'1Key-7',38:'1Key-6',40:'1Key-5',41:'1Key-4',43:'1Key-3',45:'1Key-2',47:'1Key-1',48:'1Key0',50:'1Key1',52:'1Key2',53:'1Key3',55:'1Key4',57:'1Key5',59:'1Key6',60:'1Key7',62:'1Key8',64:'1Key9',65:'1Key10',67:'1Key11',69:'1Key12',71:'1Key13',72:'1Key14'},"c_c³":{48:'1Key-7',50:'1Key-6',52:'1Key-5',53:'1Key-4',55:'1Key-3',57:'1Key-2',59:'1Key-1',60:'1Key0',62:'1Key1',64:'1Key2',65:'1Key3',67:'1Key4',69:'1Key5',71:'1Key6',72:'1Key7',74:'1Key8',76:'1Key9',77:'1Key10',79:'1Key11',81:'1Key12',83:'1Key13',84:'1Key14'},"c¹_c⁴":{60:'1Key-7',62:'1Key-6',64:'1Key-5',65:'1Key-4',67:'1Key-3',69:'1Key-2',71:'1Key-1',72:'1Key0',74:'1Key1',76:'1Key2',77:'1Key3',79:'1Key4',81:'1Key5',83:'1Key6',84:'1Key7',86:'1Key8',88:'1Key9',89:'1Key10',91:'1Key11',93:'1Key12',95:'1Key13',96:'1Key14'},"c²_c⁵":{72:'1Key-7',74:'1Key-6',76:'1Key-5',77:'1Key-4',79:'1Key-3',81:'1Key-2',83:'1Key-1',84:'1Key0',86:'1Key1',88:'1Key2',89:'1Key3',91:'1Key4',93:'1Key5',95:'1Key6',96:'1Key7',98:'1Key8',100:'1Key9',101:'1Key10',103:'1Key11',105:'1Key12',107:'1Key13',108:'1Key14'},"_C_c³":{36:'1Key-14',38:'1Key-13',40:'1Key-12',41:'1Key-11',43:'1Key-10',45:'1Key-9',47:'1Key-8',48:'1Key-7',50:'1Key-6',52:'1Key-5',53:'1Key-4',55:'1Key-3',57:'1Key-2',59:'1Key-1',60:'1Key0',62:'1Key1',64:'1Key2',65:'1Key3',67:'1Key4',69:'1Key5',71:'1Key6',72:'1Key7',74:'1Key8',76:'1Key9',77:'1Key10',79:'1Key11',81:'1Key12',83:'1Key13',84:'1Key14'},"c_c⁴":{48:'1Key-14',50:'1Key-13',52:'1Key-12',53:'1Key-11',55:'1Key-10',57:'1Key-9',59:'1Key-8',60:'1Key-7',62:'1Key-6',64:'1Key-5',65:'1Key-4',67:'1Key-3',69:'1Key-2',71:'1Key-1',72:'1Key0',74:'1Key1',76:'1Key2',77:'1Key3',79:'1Key4',81:'1Key5',83:'1Key6',84:'1Key7',86:'1Key8',88:'1Key9',89:'1Key10',91:'1Key11',93:'1Key12',95:'1Key13',96:'1Key14'},"c¹_c⁵":{60:'1Key-14',62:'1Key-13',64:'1Key-12',65:'1Key-11',67:'1Key-10',69:'1Key-9',71:'1Key-8',72:'1Key-7',74:'1Key-6',76:'1Key-5',77:'1Key-4',79:'1Key-3',81:'1Key-2',83:'1Key-1',84:'1Key0',86:'1Key1',88:'1Key2',89:'1Key3',91:'1Key4',93:'1Key5',95:'1Key6',96:'1Key7',98:'1Key8',100:'1Key9',101:'1Key10',103:'1Key11',105:'1Key12',107:'1Key13',108:'1Key14'},"_C_c⁴":{36:'1Key-14',38:'1Key-13',40:'1Key-12',41:'1Key-11',43:'1Key-10',45:'1Key-9',47:'1Key-8',48:'1Key-7',50:'1Key-6',52:'1Key-5',53:'1Key-4',55:'1Key-3',57:'1Key-2',59:'1Key-1',60:'1Key0',62:'1Key1',64:'1Key2',65:'1Key3',67:'1Key4',69:'1Key5',71:'1Key6',72:'1Key7',74:'1Key8',76:'1Key9',77:'1Key10',79:'1Key11',81:'1Key12',83:'1Key13',84:'1Key14',86:'1Key15',88:'1Key16',89:'1Key17',91:'1Key18',93:'1Key19',95:'1Key20',96:'1Key21',},"c_c⁵":{48:'1Key-14',50:'1Key-13',52:'1Key-12',53:'1Key-11',55:'1Key-10',57:'1Key-9',59:'1Key-8',60:'1Key-7',62:'1Key-6',64:'1Key-5',65:'1Key-4',67:'1Key-3',69:'1Key-2',71:'1Key-1',72:'1Key0',74:'1Key1',76:'1Key2',77:'1Key3',79:'1Key4',81:'1Key5',83:'1Key6',84:'1Key7',86:'1Key8',88:'1Key9',89:'1Key10',91:'1Key11',93:'1Key12',95:'1Key13',96:'1Key14',98:'1Key15',100:'1Key16',101:'1Key17',103:'1Key18',105:'1Key19',107:'1Key20',108:'1Key21',},"_C_c⁵":{36:'1Key-14',38:'1Key-13',40:'1Key-12',41:'1Key-11',43:'1Key-10',45:'1Key-9',47:'1Key-8',48:'1Key-7',50:'1Key-6',52:'1Key-5',53:'1Key-4',55:'1Key-3',57:'1Key-2',59:'1Key-1',60:"1Key0",62:"1Key1",64:"1Key2",65:"1Key3",67:"1Key4",69:"1Key5",71:"1Key6",72:"1Key7",74:"1Key8",76:"1Key9",77:"1Key10",79:"1Key11",81:"1Key12",83:"1Key13",84:"1Key14",86:"1Key15",88:"1Key16",89:"1Key17",91:"1Key18",93:"1Key19",95:"1Key20",96:"1Key21",98:"1Key22",100:"1Key23",101:"1Key24",103:"1Key25",105:"1Key26",107:"1Key27",108:"1Key28"},"_C_b":{36:'1Key0',38:'1Key1',40:'1Key2',41:'1Key3',43:'1Key4',45:'1Key5',47:'1Key6',48:'1Key7',50:'1Key8',52:'1Key9',53:'1Key10',55:'1Key11',57:'1Key12',59:'1Key13'},"c_b¹":{48:'1Key0',50:'1Key1',52:'1Key2',53:'1Key3',55:'1Key4',57:'1Key5',59:'1Key6',60:'1Key7',62:'1Key8',64:'1Key9',65:'1Key10',67:'1Key11',69:'1Key12',71:'1Key13'},'c¹_b²':{60:'1Key0',62:'1Key1',64:'1Key2',65:'1Key3',67:'1Key4',69:'1Key5',71:'1Key6',72:'1Key7',74:'1Key8',76:'1Key9',77:'1Key10',79:'1Key11',81:'1Key12',83:'1Key13'},"c²_b³":{72:'1Key0',74:'1Key1',76:'1Key2',77:'1Key3',79:'1Key4',81:'1Key5',83:'1Key6',84:'1Key7',86:'1Key8',88:'1Key9',89:'1Key10',91:'1Key11',93:'1Key12',95:'1Key13'},"c³_b⁴":{84:'1Key0',86:'1Key1',88:'1Key2',89:'1Key3',91:'1Key4',93:'1Key5',95:'1Key6',96:'1Key7',98:'1Key8',100:'1Key9',101:'1Key10',103:'1Key11',105:'1Key12',107:'1Key13'},"_C_b¹":{36:'1Key-7',38:'1Key-6',40:'1Key-5',41:'1Key-4',43:'1Key-3',45:'1Key-2',47:'1Key-1',48:'1Key0',50:'1Key1',52:'1Key2',53:'1Key3',55:'1Key4',57:'1Key5',59:'1Key6',60:'1Key7',62:'1Key8',64:'1Key9',65:'1Key10',67:'1Key11',69:'1Key12',71:'1Key13'},"c_b²":{48:'1Key-7',50:'1Key-6',52:'1Key-5',53:'1Key-4',55:'1Key-3',57:'1Key-2',59:'1Key-1',60:'1Key0',62:'1Key1',64:'1Key2',65:'1Key3',67:'1Key4',69:'1Key5',71:'1Key6',72:'1Key7',74:'1Key8',76:'1Key9',77:'1Key10',79:'1Key11',81:'1Key12',83:'1Key13'},"c¹_b³":{60:'1Key-7',62:'1Key-6',64:'1Key-5',65:'1Key-4',67:'1Key-3',69:'1Key-2',71:'1Key-1',72:'1Key0',74:'1Key1',76:'1Key2',77:'1Key3',79:'1Key4',81:'1Key5',83:'1Key6',84:'1Key7',86:'1Key8',88:'1Key9',89:'1Key10',91:'1Key11',93:'1Key12',95:'1Key13'},"c²_b⁴":{72:'1Key-7',74:'1Key-6',76:'1Key-5',77:'1Key-4',79:'1Key-3',81:'1Key-2',83:'1Key-1',84:'1Key0',86:'1Key1',88:'1Key2',89:'1Key3',91:'1Key4',93:'1Key5',95:'1Key6',96:'1Key7',98:'1Key8',100:'1Key9',101:'1Key10',103:'1Key11',105:'1Key12',107:'1Key13'},"_C_b²":{36:'1Key-14',38:'1Key-13',40:'1Key-12',41:'1Key-11',43:'1Key-10',45:'1Key-9',47:'1Key-8',48:'1Key-7',50:'1Key-6',52:'1Key-5',53:'1Key-4',55:'1Key-3',57:'1Key-2',59:'1Key-1',60:'1Key0',62:'1Key1',64:'1Key2',65:'1Key3',67:'1Key4',69:'1Key5',71:'1Key6',72:'1Key7',74:'1Key8',76:'1Key9',77:'1Key10',79:'1Key11',81:'1Key12',83:'1Key13'},"c_b³":{48:'1Key-14',50:'1Key-13',52:'1Key-12',53:'1Key-11',55:'1Key-10',57:'1Key-9',59:'1Key-8',60:'1Key-7',62:'1Key-6',64:'1Key-5',65:'1Key-4',67:'1Key-3',69:'1Key-2',71:'1Key-1',72:'1Key0',74:'1Key1',76:'1Key2',77:'1Key3',79:'1Key4',81:'1Key5',83:'1Key6',84:'1Key7',86:'1Key8',88:'1Key9',89:'1Key10',91:'1Key11',93:'1Key12',95:'1Key13'},"c¹_b⁴":{60:'1Key-14',62:'1Key-13',64:'1Key-12',65:'1Key-11',67:'1Key-10',69:'1Key-9',71:'1Key-8',72:'1Key-7',74:'1Key-6',76:'1Key-5',77:'1Key-4',79:'1Key-3',81:'1Key-2',83:'1Key-1',84:'1Key0',86:'1Key1',88:'1Key2',89:'1Key3',91:'1Key4',93:'1Key5',95:'1Key6',96:'1Key7',98:'1Key8',100:'1Key9',101:'1Key10',103:'1Key11',105:'1Key12',107:'1Key13'},"_C_b³":{36:'1Key-14',38:'1Key-13',40:'1Key-12',41:'1Key-11',43:'1Key-10',45:'1Key-9',47:'1Key-8',48:'1Key-7',50:'1Key-6',52:'1Key-5',53:'1Key-4',55:'1Key-3',57:'1Key-2',59:'1Key-1',60:'1Key0',62:'1Key1',64:'1Key2',65:'1Key3',67:'1Key4',69:'1Key5',71:'1Key6',72:'1Key7',74:'1Key8',76:'1Key9',77:'1Key10',79:'1Key11',81:'1Key12',83:'1Key13',84:'1Key14',86:'1Key15',88:'1Key16',89:'1Key17',91:'1Key18',93:'1Key19',95:'1Key20'},"c_b⁴":{48:'1Key-14',50:'1Key-13',52:'1Key-12',53:'1Key-11',55:'1Key-10',57:'1Key-9',59:'1Key-8',60:'1Key-7',62:'1Key-6',64:'1Key-5',65:'1Key-4',67:'1Key-3',69:'1Key-2',71:'1Key-1',72:'1Key0',74:'1Key1',76:'1Key2',77:'1Key3',79:'1Key4',81:'1Key5',83:'1Key6',84:'1Key7',86:'1Key8',88:'1Key9',89:'1Key10',91:'1Key11',93:'1Key12',95:'1Key13',96:'1Key14',98:'1Key15',100:'1Key16',101:'1Key17',103:'1Key18',105:'1Key19',107:'1Key20'},"_C_b⁴":{36:'1Key-14',38:'1Key-13',40:'1Key-12',41:'1Key-11',43:'1Key-10',45:'1Key-9',47:'1Key-8',48:'1Key-7',50:'1Key-6',52:'1Key-5',53:'1Key-4',55:'1Key-3',57:'1Key-2',59:'1Key-1',60:"1Key0",62:"1Key1",64:"1Key2",65:"1Key3",67:"1Key4",69:"1Key5",71:"1Key6",72:"1Key7",74:"1Key8",76:"1Key9",77:"1Key10",79:"1Key11",81:"1Key12",83:"1Key13",84:"1Key14",86:"1Key15",88:"1Key16",89:"1Key17",91:"1Key18",93:"1Key19",95:"1Key20",96:"1Key21",98:"1Key22",100:"1Key23",101:"1Key24",103:"1Key25",105:"1Key26",107:"1Key27"}}
extra_note_to_key = {"_C_c¹":{37:['1Key0','1Key1'],39:['1Key1','1Key2'],42:['1Key3','1Key4'],44:['1Key4','1Key5'],46:['1Key5','1Key6'],49:['1Key6','1Key7'],51:['1Key8','1Key9'],54:['1Key10','1Key11'],56:['1Key11','1Key12'],58:['1Key12','1Key13'],},"c_c²":{49:['1Key0','1Key1'],51:['1Key1','1Key2'],54:['1Key3','1Key4'],56:['1Key4','1Key5'],58:['1Key5','1Key6'],61:['1Key6','1Key7'],63:['1Key8','1Key9'],66:['1Key10','1Key11'],68:['1Key11','1Key12'],70:['1Key12','1Key13'],},'c¹_c³':{61:['1Key0','1Key1'],63:['1Key1','1Key2'],66:['1Key3','1Key4'],68:['1Key4','1Key5'],70:['1Key5','1Key6'],73:['1Key6','1Key7'],75:['1Key8','1Key9'],78:['1Key10','1Key11'],80:['1Key11','1Key12'],82:['1Key12','1Key13'],},"c²_c⁴":{73:['1Key0','1Key1'],75:['1Key1','1Key2'],78:['1Key3','1Key4'],80:['1Key4','1Key5'],82:['1Key5','1Key6'],85:['1Key6','1Key7'],87:['1Key8','1Key9'],90:['1Key10','1Key11'],92:['1Key11','1Key12'],94:['1Key12','1Key13'],},"c³_c⁵":{85:['1Key0','1Key1'],87:['1Key1','1Key2'],90:['1Key3','1Key4'],92:['1Key4','1Key5'],94:['1Key5','1Key6'],97:['1Key6','1Key7'],99:['1Key8','1Key9'],102:['1Key10','1Key11'],104:['1Key11','1Key12'],106:['1Key12','1Key13'],},"_C_c²":{37:['1Key-7','1Key-6'],39:['1Key-6','1Key-5'],42:['1Key-4','1Key-3'],44:['1Key-3','1Key-2'],46:['1Key-2','1Key-1'],49:['1Key0','1Key1'],51:['1Key1','1Key2'],54:['1Key3','1Key4'],56:['1Key4','1Key5'],58:['1Key5','1Key6'],61:['1Key6','1Key7'],63:['1Key8','1Key9'],66:['1Key10','1Key11'],68:['1Key11','1Key12'],70:['1Key12','1Key13'],},"c_c³":{49:['1Key-7','1Key-6'],51:['1Key-6','1Key-5'],54:['1Key-4','1Key-3'],56:['1Key-3','1Key-2'],58:['1Key-2','1Key-1'],61:['1Key0','1Key1'],63:['1Key1','1Key2'],66:['1Key3','1Key4'],68:['1Key4','1Key5'],70:['1Key5','1Key6'],73:['1Key6','1Key7'],75:['1Key8','1Key9'],78:['1Key10','1Key11'],80:['1Key11','1Key12'],82:['1Key12','1Key13'],},"c¹_c⁴":{61:['1Key-7','1Key-6'],63:['1Key-6','1Key-5'],66:['1Key-4','1Key-3'],68:['1Key-3','1Key-2'],70:['1Key-2','1Key-1'],73:['1Key0','1Key1'],75:['1Key1','1Key2'],78:['1Key3','1Key4'],80:['1Key4','1Key5'],82:['1Key5','1Key6'],85:['1Key6','1Key7'],87:['1Key8','1Key9'],90:['1Key10','1Key11'],92:['1Key11','1Key12'],94:['1Key12','1Key13'],},"c²_c⁵":{73:['1Key-7','1Key-6'],75:['1Key-6','1Key-5'],78:['1Key-4','1Key-3'],80:['1Key-3','1Key-2'],82:['1Key-2','1Key-1'],85:['1Key0','1Key1'],87:['1Key1','1Key2'],90:['1Key3','1Key4'],92:['1Key4','1Key5'],94:['1Key5','1Key6'],97:['1Key6','1Key7'],99:['1Key8','1Key9'],102:['1Key10','1Key11'],104:['1Key11','1Key12'],106:['1Key12','1Key13'],},"_C_c³":{37:['1Key-14','1Key-13'],39:['1Key-13','1Key-12'],42:['1Key-11','1Key-10'],44:['1Key-10','1Key-9'],46:['1Key-9','1Key-8'],49:['1Key-7','1Key-6'],51:['1Key-6','1Key-5'],54:['1Key-4','1Key-3'],56:['1Key-3','1Key-2'],58:['1Key-2','1Key-1'],61:['1Key0','1Key1'],63:['1Key1','1Key2'],66:['1Key3','1Key4'],68:['1Key4','1Key5'],70:['1Key5','1Key6'],73:['1Key6','1Key7'],75:['1Key8','1Key9'],78:['1Key10','1Key11'],80:['1Key11','1Key12'],82:['1Key12','1Key13'],},"c_c⁴":{49:['1Key-14','1Key-13'],51:['1Key-13','1Key-12'],54:['1Key-11','1Key-10'],56:['1Key-10','1Key-9'],58:['1Key-9','1Key-8'],61:['1Key-7','1Key-6'],63:['1Key-6','1Key-5'],66:['1Key-4','1Key-3'],68:['1Key-3','1Key-2'],70:['1Key-2','1Key-1'],73:['1Key0','1Key1'],75:['1Key1','1Key2'],78:['1Key3','1Key4'],80:['1Key4','1Key5'],82:['1Key5','1Key6'],85:['1Key6','1Key7'],87:['1Key8','1Key9'],90:['1Key10','1Key11'],92:['1Key11','1Key12'],94:['1Key12','1Key13'],},"c¹_c⁵":{61:['1Key-14','1Key-13'],63:['1Key-13','1Key-12'],66:['1Key-11','1Key-10'],68:['1Key-10','1Key-9'],70:['1Key-9','1Key-8'],73:['1Key-7','1Key-6'],75:['1Key-6','1Key-5'],78:['1Key-4','1Key-3'],80:['1Key-3','1Key-2'],82:['1Key-2','1Key-1'],85:['1Key0','1Key1'],87:['1Key1','1Key2'],90:['1Key3','1Key4'],92:['1Key4','1Key5'],94:['1Key5','1Key6'],97:['1Key6','1Key7'],99:['1Key8','1Key9'],102:['1Key10','1Key11'],104:['1Key11','1Key12'],106:['1Key12','1Key13'],},"_C_c⁴":{37:['1Key-14','1Key-13'],39:['1Key-13','1Key-12'],42:['1Key-11','1Key-10'],44:['1Key-10','1Key-9'],46:['1Key-9','1Key-8'],49:['1Key-7','1Key-6'],51:['1Key-6','1Key-5'],54:['1Key-4','1Key-3'],56:['1Key-3','1Key-2'],58:['1Key-2','1Key-1'],61:['1Key0','1Key1'],63:['1Key1','1Key2'],66:['1Key3','1Key4'],68:['1Key4','1Key5'],70:['1Key5','1Key6'],73:['1Key6','1Key7'],75:['1Key8','1Key9'],78:['1Key10','1Key11'],80:['1Key11','1Key12'],82:['1Key12','1Key13'],85:['1Key14','1Key15'],87:['1Key15','1Key16'],90:['1Key17','1Key18'],92:['1Key18','1Key19'],94:['1Key19','1Key20'],},"c_c⁵":{49:['1Key-14','1Key-13'],51:['1Key-13','1Key-12'],54:['1Key-11','1Key-10'],56:['1Key-10','1Key-9'],58:['1Key-9','1Key-8'],61:['1Key-7','1Key-6'],63:['1Key-6','1Key-5'],66:['1Key-4','1Key-3'],68:['1Key-3','1Key-2'],70:['1Key-2','1Key-1'],73:['1Key0','1Key1'],75:['1Key1','1Key2'],78:['1Key3','1Key4'],80:['1Key4','1Key5'],82:['1Key5','1Key6'],85:['1Key6','1Key7'],87:['1Key8','1Key9'],90:['1Key10','1Key11'],92:['1Key11','1Key12'],94:['1Key12','1Key13'],97:['1Key14','1Key15'],99:['1Key15','1Key16'],102:['1Key17','1Key18'],104:['1Key18','1Key19'],106:['1Key19','1Key20'],},"_C_c⁵":{37:['1Key-14','1Key-13'],39:['1Key-13','1Key-12'],42:['1Key-11','1Key-10'],44:['1Key-10','1Key-9'],46:['1Key-9','1Key-8'],49:['1Key-7','1Key-6'],51:['1Key-6','1Key-5'],54:['1Key-4','1Key-3'],56:['1Key-3','1Key-2'],58:['1Key-2','1Key-1'],61:['1Key0','1Key1'],63:['1Key1','1Key2'],66:['1Key3','1Key4'],68:['1Key4','1Key5'],70:['1Key5','1Key6'],73:['1Key6','1Key7'],75:['1Key8','1Key9'],78:['1Key10','1Key11'],80:['1Key11','1Key12'],82:['1Key12','1Key13'],85:['1Key14','1Key15'],87:['1Key15','1Key16'],90:['1Key17','1Key18'],92:['1Key18','1Key19'],94:['1Key19','1Key20'],97:['1Key21','1Key22'],99:['1Key22','1Key23'],102:['1Key24','1Key25'],104:['1Key25','1Key26'],106:['1Key26','1Key27'],},"_C_b":{37:['1Key0','1Key1'],39:['1Key1','1Key2'],42:['1Key3','1Key4'],44:['1Key4','1Key5'],46:['1Key5','1Key6'],49:['1Key6','1Key7'],51:['1Key8','1Key9'],54:['1Key10','1Key11'],56:['1Key11','1Key12'],58:['1Key12','1Key13'],},"c_b¹":{49:['1Key0','1Key1'],51:['1Key1','1Key2'],54:['1Key3','1Key4'],56:['1Key4','1Key5'],58:['1Key5','1Key6'],61:['1Key6','1Key7'],63:['1Key8','1Key9'],66:['1Key10','1Key11'],68:['1Key11','1Key12'],70:['1Key12','1Key13'],},'c¹_b²':{61:['1Key0','1Key1'],63:['1Key1','1Key2'],66:['1Key3','1Key4'],68:['1Key4','1Key5'],70:['1Key5','1Key6'],73:['1Key6','1Key7'],75:['1Key8','1Key9'],78:['1Key10','1Key11'],80:['1Key11','1Key12'],82:['1Key12','1Key13'],},"c²_b³":{73:['1Key0','1Key1'],75:['1Key1','1Key2'],78:['1Key3','1Key4'],80:['1Key4','1Key5'],82:['1Key5','1Key6'],85:['1Key6','1Key7'],87:['1Key8','1Key9'],90:['1Key10','1Key11'],92:['1Key11','1Key12'],94:['1Key12','1Key13'],},"c³_b⁴":{85:['1Key0','1Key1'],87:['1Key1','1Key2'],90:['1Key3','1Key4'],92:['1Key4','1Key5'],94:['1Key5','1Key6'],97:['1Key6','1Key7'],99:['1Key8','1Key9'],102:['1Key10','1Key11'],104:['1Key11','1Key12'],106:['1Key12','1Key13'],},"_C_b¹":{37:['1Key-7','1Key-6'],39:['1Key-6','1Key-5'],42:['1Key-4','1Key-3'],44:['1Key-3','1Key-2'],46:['1Key-2','1Key-1'],49:['1Key0','1Key1'],51:['1Key1','1Key2'],54:['1Key3','1Key4'],56:['1Key4','1Key5'],58:['1Key5','1Key6'],61:['1Key6','1Key7'],63:['1Key8','1Key9'],66:['1Key10','1Key11'],68:['1Key11','1Key12'],70:['1Key12','1Key13'],},"c_b²":{49:['1Key-7','1Key-6'],51:['1Key-6','1Key-5'],54:['1Key-4','1Key-3'],56:['1Key-3','1Key-2'],58:['1Key-2','1Key-1'],61:['1Key0','1Key1'],63:['1Key1','1Key2'],66:['1Key3','1Key4'],68:['1Key4','1Key5'],70:['1Key5','1Key6'],73:['1Key6','1Key7'],75:['1Key8','1Key9'],78:['1Key10','1Key11'],80:['1Key11','1Key12'],82:['1Key12','1Key13'],},"c¹_b³":{61:['1Key-7','1Key-6'],63:['1Key-6','1Key-5'],66:['1Key-4','1Key-3'],68:['1Key-3','1Key-2'],70:['1Key-2','1Key-1'],73:['1Key0','1Key1'],75:['1Key1','1Key2'],78:['1Key3','1Key4'],80:['1Key4','1Key5'],82:['1Key5','1Key6'],85:['1Key6','1Key7'],87:['1Key8','1Key9'],90:['1Key10','1Key11'],92:['1Key11','1Key12'],94:['1Key12','1Key13'],},"c²_b⁴":{73:['1Key-7','1Key-6'],75:['1Key-6','1Key-5'],78:['1Key-4','1Key-3'],80:['1Key-3','1Key-2'],82:['1Key-2','1Key-1'],85:['1Key0','1Key1'],87:['1Key1','1Key2'],90:['1Key3','1Key4'],92:['1Key4','1Key5'],94:['1Key5','1Key6'],97:['1Key6','1Key7'],99:['1Key8','1Key9'],102:['1Key10','1Key11'],104:['1Key11','1Key12'],106:['1Key12','1Key13'],},"_C_b²":{37:['1Key-14','1Key-13'],39:['1Key-13','1Key-12'],42:['1Key-11','1Key-10'],44:['1Key-10','1Key-9'],46:['1Key-9','1Key-8'],49:['1Key-7','1Key-6'],51:['1Key-6','1Key-5'],54:['1Key-4','1Key-3'],56:['1Key-3','1Key-2'],58:['1Key-2','1Key-1'],61:['1Key0','1Key1'],63:['1Key1','1Key2'],66:['1Key3','1Key4'],68:['1Key4','1Key5'],70:['1Key5','1Key6'],73:['1Key6','1Key7'],75:['1Key8','1Key9'],78:['1Key10','1Key11'],80:['1Key11','1Key12'],82:['1Key12','1Key13'],},"c_b³":{49:['1Key-14','1Key-13'],51:['1Key-13','1Key-12'],54:['1Key-11','1Key-10'],56:['1Key-10','1Key-9'],58:['1Key-9','1Key-8'],61:['1Key-7','1Key-6'],63:['1Key-6','1Key-5'],66:['1Key-4','1Key-3'],68:['1Key-3','1Key-2'],70:['1Key-2','1Key-1'],73:['1Key0','1Key1'],75:['1Key1','1Key2'],78:['1Key3','1Key4'],80:['1Key4','1Key5'],82:['1Key5','1Key6'],85:['1Key6','1Key7'],87:['1Key8','1Key9'],90:['1Key10','1Key11'],92:['1Key11','1Key12'],94:['1Key12','1Key13'],},"c¹_b⁴":{61:['1Key-14','1Key-13'],63:['1Key-13','1Key-12'],66:['1Key-11','1Key-10'],68:['1Key-10','1Key-9'],70:['1Key-9','1Key-8'],73:['1Key-7','1Key-6'],75:['1Key-6','1Key-5'],78:['1Key-4','1Key-3'],80:['1Key-3','1Key-2'],82:['1Key-2','1Key-1'],85:['1Key0','1Key1'],87:['1Key1','1Key2'],90:['1Key3','1Key4'],92:['1Key4','1Key5'],94:['1Key5','1Key6'],97:['1Key6','1Key7'],99:['1Key8','1Key9'],102:['1Key10','1Key11'],104:['1Key11','1Key12'],106:['1Key12','1Key13'],},"_C_b³":{37:['1Key-14','1Key-13'],39:['1Key-13','1Key-12'],42:['1Key-11','1Key-10'],44:['1Key-10','1Key-9'],46:['1Key-9','1Key-8'],49:['1Key-7','1Key-6'],51:['1Key-6','1Key-5'],54:['1Key-4','1Key-3'],56:['1Key-3','1Key-2'],58:['1Key-2','1Key-1'],61:['1Key0','1Key1'],63:['1Key1','1Key2'],66:['1Key3','1Key4'],68:['1Key4','1Key5'],70:['1Key5','1Key6'],73:['1Key6','1Key7'],75:['1Key8','1Key9'],78:['1Key10','1Key11'],80:['1Key11','1Key12'],82:['1Key12','1Key13'],85:['1Key14','1Key15'],87:['1Key15','1Key16'],90:['1Key17','1Key18'],92:['1Key18','1Key19'],94:['1Key19','1Key20'],},"c_b⁴":{49:['1Key-14','1Key-13'],51:['1Key-13','1Key-12'],54:['1Key-11','1Key-10'],56:['1Key-10','1Key-9'],58:['1Key-9','1Key-8'],61:['1Key-7','1Key-6'],63:['1Key-6','1Key-5'],66:['1Key-4','1Key-3'],68:['1Key-3','1Key-2'],70:['1Key-2','1Key-1'],73:['1Key0','1Key1'],75:['1Key1','1Key2'],78:['1Key3','1Key4'],80:['1Key4','1Key5'],82:['1Key5','1Key6'],85:['1Key6','1Key7'],87:['1Key8','1Key9'],90:['1Key10','1Key11'],92:['1Key11','1Key12'],94:['1Key12','1Key13'],97:['1Key14','1Key15'],99:['1Key15','1Key16'],102:['1Key17','1Key18'],104:['1Key18','1Key19'],106:['1Key19','1Key20'],},"_C_b⁴":{37:['1Key-14','1Key-13'],39:['1Key-13','1Key-12'],42:['1Key-11','1Key-10'],44:['1Key-10','1Key-9'],46:['1Key-9','1Key-8'],49:['1Key-7','1Key-6'],51:['1Key-6','1Key-5'],54:['1Key-4','1Key-3'],56:['1Key-3','1Key-2'],58:['1Key-2','1Key-1'],61:['1Key0','1Key1'],63:['1Key1','1Key2'],66:['1Key3','1Key4'],68:['1Key4','1Key5'],70:['1Key5','1Key6'],73:['1Key6','1Key7'],75:['1Key8','1Key9'],78:['1Key10','1Key11'],80:['1Key11','1Key12'],82:['1Key12','1Key13'],85:['1Key14','1Key15'],87:['1Key15','1Key16'],90:['1Key17','1Key18'],92:['1Key18','1Key19'],94:['1Key19','1Key20'],97:['1Key21','1Key22'],99:['1Key22','1Key23'],102:['1Key24','1Key25'],104:['1Key25','1Key26'],106:['1Key26','1Key27'],}}
# 特殊音符的映射规则
special_note_mapping = {'_C_c¹':{62:57,64:59,65:60,},'c_c²':{74:69,76:71,77:72,},'c¹_c³':{86:81,88:83,89:84,},'c²_c⁴':{98:93,100:95,101:96,},'c³_c⁵':{110:105,112:107,113:108,},"_C_c²":{74:69,76:71,77:72,},"c_c³":{86:81,88:83,89:84,},"c¹_c⁴":{98:93,100:95,101:96,},"c²_c⁵":{110:105,112:107,113:108,},"_C_c³":{86:81,88:83,89:84,},"c_c⁴":{98:93,100:95,101:96,},"c¹_c⁵":{110:105,112:107,113:108,},"_C_c⁴":{98:93,100:95,101:96,},"c_c⁵":{110:105,112:107,113:108,},"_C_c⁵":{110:105,112:107,113:108,},"_C_b":{62:57,64:59,},"c_b¹":{74:69,76:71,},"c¹_b²":{86:81,88:83,},"c²_b³":{98:93,100:95,},"c³_b⁴":{110:105,112:107,},"_C_b¹":{74:69,76:71,},"c_b²":{86:81,88:83,},"c¹_b³":{98:93,100:95,},"c²_b⁴":{110:105,112:107,},"_C_b²":{86:81,88:83,},"c_b³":{98:93,100:95,},"c¹_b⁴":{110:105,112:107,},"_C_b³":{98:93,100:95,},"c_b⁴":{110:105,112:107,},"_C_b⁴":{110:105,112:107,}}

# 根据 BPM 动态调整时间合并阈值
def get_dynamic_time_merge_threshold(bpm):
    return max(GlobalVariable.merge_min, min(GlobalVariable.merge_max, int(60000 / bpm / 4)))  # 限制阈值在 范围区间

# 15 个音符与键盘按键的映射
def get_bpm_from_midi(midi_file_path):
    midi = pretty_midi.PrettyMIDI(midi_file_path)
    tempos = midi.get_tempo_changes()
    return tempos[1][0] if len(tempos[1]) > 0 else 120


def merge_keys(keys):
    key_count = len(keys)
    return [f"{key_count}Key{key.replace('1Key', '')}" for key in keys]


def process_midi_to_txt(input_path, output_path, version):
    midi = pretty_midi.PrettyMIDI(input_path)
    bpm = get_bpm_from_midi(input_path)
    time_merge_threshold = get_dynamic_time_merge_threshold(bpm)
    notes = []

    for instrument in midi.instruments:
        if not instrument.is_drum:
            for note in instrument.notes:
                pitch, time, velocity= note.pitch, int(note.start * 1000), note.velocity
                if velocity < GlobalVariable.velocity_filter:
                    continue
                if pitch in note_to_key[version]:
                    notes.append({'time': time, 'key': note_to_key[version][pitch]})
                elif pitch in extra_note_to_key[version]:
                    for extra_key in extra_note_to_key[version][pitch]:
                        notes.append({'time': time, 'key': extra_key})
                elif pitch in special_note_mapping[version]:
                    notes.append({'time': time, 'key': note_to_key[version][special_note_mapping[version][pitch]]})

    notes.sort(key=lambda x: x['time'])
    merged_notes, last_time, temp_keys = [], None, []

    for note in notes:
        if last_time is None or note['time'] - last_time <= time_merge_threshold:
            temp_keys.append(note['key'])
        else:
            merged_notes.extend({'time': last_time, 'key': k} for k in merge_keys(temp_keys))
            temp_keys = [note['key']]
        last_time = note['time']

    merged_notes.extend({'time': last_time, 'key': k} for k in merge_keys(temp_keys))
    output = [{
        "name": os.path.basename(input_path).replace("_basic_pitch.mid","_Range") + version,
        "author": "skyMusic-WindHide",
        "transcribedBy": "WindHide's Software",
        "bpm": bpm,
        "bitsPerPage": 15,
        "pitchLevel": 0,
        "isComposed": True,
        "songNotes": merged_notes,
        "isEncrypted": False,
    }]

    with open(output_path, 'w') as f:
        json.dump(output, f, indent=4)

    return 100


def process_directory_with_progress(typeStr, output_dir=getResourcesPath("myTranslate")):
    GlobalVariable.overall_progress = 0
    os.makedirs(output_dir, exist_ok=True)
    files_to_process = [f for f in os.listdir(getResourcesPath("translateOriginalMusic"))
                        if f.endswith(('.mp3', '.ogg', '.wav', '.flac', '.mid', '.m4a'))]
    total_files = len(files_to_process)
    tranMap = []
    if GlobalVariable.is_singular:
        mapping = {
            "2": ["_C_c¹", "c_c²", "c¹_c³", "c²_c⁴", "c³_c⁵"],
            "3": ["_C_c²", "c_c³", "c¹_c⁴", "c²_c⁵"],
            "4": ["_C_c³", "c_c⁴", "c¹_c⁵"],
            "5": ["_C_c⁴", "c_c⁵"],
            "6": ["_C_c⁵"]
        }
    else:
        mapping = {
            "2": ["_C_b",  "c_b¹", "c¹_b²", "c²_b³", "c³_b⁴"],
            "3": ["_C_b¹", "c_b²", "c¹_b³", "c²_b⁴"],
            "4": ["_C_b²", "c_b³", "c¹_b⁴"],
            "5": ["_C_b³", "c_b⁴"],
            "6": ["_C_b⁴"]
        }

    for key in mapping:
        if key in typeStr:
            tranMap.extend(mapping[key])

    if not total_files:
        print("没有找到需要处理的文件")
        return

    for idx, file in enumerate(files_to_process):
        if "_ok" in file:
            continue

        GlobalVariable.now_translate_text = [f"{idx + 1}/{total_files}", file]
        fileNameNoEnd = file.rsplit('.', 1)[0]
        midFilePath = os.path.join(getResourcesPath("translateMID"), f"{fileNameNoEnd}_basic_pitch")
        musicFilePath = os.path.join(getResourcesPath("translateOriginalMusic"), file)

        if not file.endswith(".mid"):
            inference(input_path=musicFilePath)
        else:
            midFilePath = os.path.join(getResourcesPath("translateOriginalMusic"), f"{fileNameNoEnd}")

        for version in tranMap:
            process_midi_to_txt(midFilePath + ".mid", os.path.join(output_dir, f"{fileNameNoEnd}_Range_{version}.txt"),
                                version)

        new_file_path = os.path.join(getResourcesPath("translateOriginalMusic"),
                                     f"{fileNameNoEnd}_ok.{file.split('.')[-1]}")
        os.rename(os.path.join(getResourcesPath("translateOriginalMusic"), file), new_file_path)
        print(f"已将文件 {file} 重命名为 {new_file_path}")
        GlobalVariable.overall_progress = ((idx + 1) / total_files) * 100

    GlobalVariable.overall_progress = 100
