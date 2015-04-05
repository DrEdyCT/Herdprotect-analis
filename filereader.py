#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import hashlib
import os
import win32api
import pefile

folder = os.path.join("C:/Fiels/")
file_list = [folder + i for i in os.listdir(folder) if os.path.isfile(folder + i)]
file_names = list()
md5_list = list()
sha1_list = list()
sha256_list = list()
file_size_list = list()
file_compilation_timestamp_list = list()
product_version_list = list()
file_description_list = list()
product_name_list = list()
company_name_list = list()
legal_copyright_list = list()
all_information = list()

def show():
    print('File name: ', file_names)
    print('Publisher: ', company_name_list)
    print('Product: ', product_name_list)
    print('Description: ', file_description_list)
    print('MD5: ', md5_list)
    print('SHA-1: ',sha1_list)
    print('SHA-256: ',sha256_list)
    print('File size kb: ',file_size_list)
    print('Product version: ', product_version_list)
    print('Copyright: ', legal_copyright_list)
    print('Compilation timestamp: ', file_compilation_timestamp_list)

def find_hash_code(file_path):
    file = open(file_path, 'rb')
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()
    while True:
        data = file.read()
        if not data:
            break
        md5.update(data)
        sha1.update(data)
        sha256.update(data)
    return md5.hexdigest(), sha1.hexdigest(), sha256.hexdigest()

n = 0
while n != len(file_list):
    hash = find_hash_code(file_list[n])
    md5_list.append(hash[0])
    sha1_list.append(hash[1])
    sha256_list.append(hash[2])
    file_names.append(os.path.basename(file_list[n]))
    file_size_list.append("(%s bytes)" % ("{0:,d}".format(os.path.getsize(file_list[n]))))
    file_compilation_timestamp = datetime.datetime.utcfromtimestamp(pefile.PE(file_list[1]).FILE_HEADER.TimeDateStamp)
    file_compilation_timestamp = file_compilation_timestamp.strftime("%m/%d/%Y %H:%M:%S %p")
    file_compilation_timestamp_list.append(file_compilation_timestamp)
    info_in = ["ProductVersion", "FileDescription", "ProductName", "CompanyName", "LegalCopyright"]
    info_out = list()
    for i in info_in:
        try:
            lang, codepage = win32api.GetFileVersionInfo(file_list[n], '\\VarFileInfo\\Translation')[0]
            strInfoPath = u'\\StringFileInfo\\%04X%04X\\%s' % (lang, codepage, i)
            info_out.append(win32api.GetFileVersionInfo(file_list[n], strInfoPath))
        except:
           info_out.append(None)
    product_version_list.append(info_out[0])
    file_description_list.append(info_out[1])
    product_name_list.append(info_out[2])
    company_name_list.append(info_out[3])
    legal_copyright_list.append(info_out[4])
    n += 1

all_information.extend([file_names, company_name_list, product_name_list, file_description_list,\
                        md5_list, sha1_list, sha256_list, file_size_list, product_version_list,\
                        legal_copyright_list, file_compilation_timestamp_list])

show()