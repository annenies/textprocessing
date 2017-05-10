import os
import zipfile
import re
import sqlite3
import time

#This code setups a clean test
x = 0
copy = False
lines = []
author = []
title = []
ebook = []
excerpt = []
filez = []
filer = []
filay = []
booker = []

t1 = time.time()
print time.asctime( time.localtime(time.time()) )

#This is the code I'm working on for multiple books. And it works!
for root, dirs, files in os.walk("1/0"):
    for name in files:
        if name.endswith((".ZIP")):
            if name.endswith(("_H.ZIP")):
                continue
            if name.endswith(("_M.ZIP")):
                continue
            else:
                filez.append(root+"/"+name)

print len(filez)

t2 = (time.time() - t1)/60
print "time to complete filez list:"
print t2

for name in filez:
    z = zipfile.ZipFile(name,'r')
    filet = z.namelist()
    for i in range(len(filet)):
        if filet[i].endswith(".txt"):
            try:
                text = z.open(filet[i])
                for line in text:
                    lang = re.findall('^Language: (.+)\r', line)
                    if len(lang)>0 and lang[0]=='English':
                        filer.append(filet[i])
                z.close()
                x = 0
                lines = []
            except:
                print filet[i]
        else:
            continue

print "files selected:"
print len(filer)
t3 = (time.time() - t1)/60
print "time to select files:"
print t3

for name in filez:
    z = zipfile.ZipFile(name,'r')
    filet = z.namelist()
    for i in range(len(filet)):
        if filet[i] in filer:
            try:
                text = z.open(filet[i])
                for line in text:
                    books = re.findall('ebook #([0-9]+)', line.lower())
                    if len(books)>0 and books not in booker:
                        booker.append(books)
                        filay.append(filet[i])
                z.close()
                x = 0
                lines = []
            except:
                print filet[i]
        else:
            continue

print "files selected:"
print len(filay)
print "books selected:"
print len(booker)
t5 = (time.time() - t1)/60
print "Time to refine file list:"
print t5

filer = []
authorer = []

for name in filez:
    z = zipfile.ZipFile(name,'r')
    filet = z.namelist()
    for i in range(len(filet)):
        if filet[i] in filay:
            try:
                text = z.open(filet[i])
                for line in text:
                    authors = re.findall('^Author: (.+)\r', line)
                    if len(authors)>0:
                        authorer.append(authors)
                        filer.append(filet[i])
                z.close()
                x = 0
                lines = []
            except:
                print filet[i]
        else:
            continue

print "files selected:"
print len(filer)
print "authors selected:"
print len(authorer)
t5 = (time.time() - t1)/60
print "Time to refine file list:"
print t5

for name in filez:
    z = zipfile.ZipFile(name, 'r')
    filet = z.namelist()
    for i in range(len(filet)):
        if filet[i] in filer:
            try:
                text = z.open(filet[i])
                for line in text:
                    titlee = re.findall('^Title: (.+)\r', line)
                    authore = re.findall('^Author: (.+)\r', line)
                    ebooke = re.findall('ebook #([0-9]+)', line.lower())
                    if len(titlee) > 0:
                        title.append(titlee)
                    if len(authore) > 0:
                        author.append(authore)
                    if len(ebooke) > 0:
                        ebook.append(ebooke)
                    if line.startswith("*** START OF THIS PROJECT GUTENBERG EBOOK"):
                        copy = True
                    elif line.startswith("End of the Project Gutenberg EBook"):
                        copy = False
                    elif copy:
                        x = x + 1
                        lines.append(line)
                s = x / 5
                l = s + 20
                excerpta = lines[s:l]
                excerpta = ''.join(excerpta)
                excerpt.append(excerpta)
                z.close()
                x = 0
                lines = []
                excerpta = []
            except:
                print filet[i]
        else:
            continue

t4 = (time.time() - t1)/60
print "time to complete:"
print t4

#This should be true
print len(title) == len(author) == len(ebook) == len(filer) == len(excerpt)
print len(title)
print len(author)
print len(ebook)
print len(filay)
print len(excerpt)

# This creates new files one for each excerpt with the book id as the file name.
for i in range(len(ebook)):
    f = open('excerpts/'+ebook[i][0]+'.txt', 'w')
    f.write(excerpt[i])
    f.close()

#To get the words for the Words table
import string
words = []

for i in range(len(excerpt)):
    words.extend(re.sub('['+string.punctuation+']', ' ', excerpt[i]).split())


d = dict()
for word in words:
    if word not in d:
        d[word] = 1
    else:
        d[word] = d[word] + 1

conn = sqlite3.connect('e_test.sqlite3')
cur = conn.cursor()

books = []

cur.execute('SELECT ebookid FROM Excerpts')

for ebid in cur:
    books.append(ebid)

for i in range(len(ebook)):
    if ebook[i][0] in books:
        cur.execute('UPDATE Excerpts SET author=?, title=? WHERE ebookid=?',
                        (unicode(author[i][0], "utf-8"), unicode(title[i][0], "utf-8"), ebook[i][0]))
    else:
        cur.execute('INSERT INTO Excerpts (ebookid, author, title) VALUES (?,?,?)',
                        (ebook[i][0], author[i][0], title[i][0]))
        books.append(ebook[i][0])

conn.commit()