from flask import Flask, request
from werkzeug.utils import secure_filename as sf
import os
import datetime
import shutil
import ast

kayitlars = []


app = Flask(__name__)

kontrolForm = """
<form action="kontrolEt" method="post">
Kimlik no: <input type="text" name="kimlik" size="6"><br><br>
<input type="submit" value="Kontrol Et">
</form>
<br>
"""

kontrolOnayla = """
<center>
<br>
<form action="kontrolOK" method="post">
<input type="hidden" name="kimne" value="vvkimnevv">
<input type="hidden" name="tarih" value="vvtarihvv">
<input style="padding: 1%; font-size: 300%;" type="submit" value="Onayla">
</form>
</center>
"""

kayitForm = """
<style>
td{
    padding: 4%;
}
table{
}
</style>
<form action="kaydet" method="post">
<table>
<tr><td>Kimlik no:</td><td><input type="text" name="kimlik" size="6" required></td></tr>
<tr><td>İsim Soyisim:</td><td><input type="text" name="namesurname" required></td></tr>
<tr><td>Yaşı:</td><td><input type="text" name="age" size="2" required></td></tr>
<tr><td>Telefon:</td><td><input type="tel" name="tel" required></td></tr>
<tr><td><input type="submit" value="Kaydet"></td></tr>
</table>
</form>
"""

girisHTML = """
<style>
.buton{
padding: 2%;
font-size: 300%;
background: #ecd91d;
border-radius: 25px;
display: block;
width: 20%;
}
a{
    text-decoration: none;
    color: white;
}
</style>
<head>
</head>
<center>
<br>
<h1>Covid-19 Aşısı Başvuru Sistemi</h1>
<br>
<a href="/kayit" class="buton">Yeni Kayıt</a><br>
<a href="/kontrol" class="buton">Kontrol</a><br>
<a href="/kayitlar" class="buton">Kayıtlılar</a><br>
</center>
"""

tableStyle = """
<style>
td{
padding: 1%;
}
table{
    width: 100%;
}
th, td{
    border-bottom: 1px solid;
    text-align: center;
}
tr:hover {background-color: #f5e548;} 
tr:nth-child(even) {background-color: #fff699;}  
</style>
"""

scrpt = """
<script>
function sortTable(n) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById("liste");
  switching = true;
  dir = "asc";
  while (switching) {
    switching = false;
    rows = table.rows;
    for (i = 1; i < (rows.length - 1); i++) {
      shouldSwitch = false;
      x = rows[i].getElementsByTagName("TD")[n];
      y = rows[i + 1].getElementsByTagName("TD")[n];
      if (dir == "asc") {
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          shouldSwitch = true;
          break;
        }
      } else if (dir == "desc") {
        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      switchcount ++;
    } else {
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}
</script>
"""

def rowData(gelenData):
    return "<td>" + str(gelenData) + "</td>"


@app.route('/')
def anasayfa():
    return girisHTML


@app.route('/kontrol', methods=['POST', 'GET'])
def kontrol():
  return kontrolForm

@app.route('/kontrolEt', methods=['POST', 'GET'])
def kontrolEt():

    zz = open("vacinfo.txt", "r")
    kayitlar = ast.literal_eval(zz.read())
    zz.close()

    for kayitOku in kayitlar:
        if ast.literal_eval(kayitOku)["kimlik"] == request.form.get("kimlik"):
            kb = ast.literal_eval(kayitOku)    
            kayitHead = """<table id="liste"><tr><th>Kimlik</th><th>İsim Soyisim</th><th>Telefon Numarası</th></tr>"""
            kayit = kayitHead + '<tr>' + rowData(kb.get('kimlik')) + rowData(kb.get('namesurname')) + rowData(kb.get('tel')) + '</tr>'
            return tableStyle + scrpt +  kayit + '</table>' + kontrolOnayla.replace("vvkimnevv", kb.get('kimlik')).replace("vvtarihvv", str(datetime.date.today()))

    return "Böyle bir kayıt bulunamadı"


@app.route('/kontrolOK', methods=['POST', 'GET'])
def kontrolOK():

    kayitOku = open('vacinfo.txt', 'r')
    kayit = ast.literal_eval(kayitOku.read())
    kayitOku.close()

    vacinOku = open('vaccinated.txt', 'r')
    vacKayit = ast.literal_eval(vacinOku.read())
    vacinOku.close()

    

    for kim in kayit:            
        if ast.literal_eval(kim)["kimlik"] == request.form.get("kimne"):

            vacKayit.append(kim)

            kayitGuncelle = open("vaccinated.txt", 'w')
            kayitGuncelle.write(str(vacKayit))
            kayitGuncelle.close()
            
            kayitGuncelle = open("vacinfo.txt", 'w')
            kayit.remove(kim)
            kayitGuncelle.write(str(kayit))
            kayitGuncelle.close()

            return "Kayıt Güncellendi"
        

    return "Kayıt Bulunamadı"
    

@app.route('/kaydet', methods=['POST', 'GET'])
def kaydet():
    if str(request.form.get('kimlik')).isnumeric:


        rr = open("vacinfo.txt", "r")
        kayitlars = ast.literal_eval(rr.read())
        rr.close()

        kayitlars.append(str(request.form.to_dict()))
        
        newDog = open("vacinfo.txt", 'w')
        newDog.write(str(kayitlars))
        newDog.close()
        return "{} kimlik kartı numaralı <strong>{}</strong> için kayıt oluşturuldu.".format(request.form.get('kimlik'), request.form.get('namesurname'))
    else:
        return "Kimlik numarası rakamlardan oluşmalıdır."        



@app.route('/kayit')
def kayitSayfasi():
    return kayitForm







@app.route("/kayitlar")
def kayitlilar():

    r = open("vacinfo.txt", "r")
    rr = ast.literal_eval(r.read())
    r.close()



    kayit = """<table id="liste"><tr><th onclick="sortTable(0)">Kimlik</th><th onclick="sortTable(1)">İsim Soyisim</th><th onclick="sortTable(2)">Telefon Numarası</th><th onclick="sortTable(3)">Kontrol Tarihi</th></tr>"""
    for pat in rr:
        if pat:
            kb = ast.literal_eval(pat)            
            kayit = kayit + '<tr>' + rowData(kb.get('kimlik')) + rowData(kb.get('namesurname')) + rowData(kb.get('tel')) +rowData(kb.get('dogsname')) + rowData(kb.get('dogsage')) + rowData(kb.get('controldate')) + '</tr>'
    return tableStyle + scrpt +  kayit + '</table>'


app.run()
