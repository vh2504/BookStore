
import datetime
import random
from flask import Flask, render_template, redirect, request, session, sessions
import flask
from flask.helpers import flash
from flask import redirect
from flask_login.utils import login_required, logout_user
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import false
from werkzeug.local import F
from wtforms.validators import Email
from app import app
from app.models import ChiTietHoaDon, HoaDon, Loai, Sach, db,DangNhap
from app.form import LoginForm, RegisterForm
from flask_login import login_user,current_user
from flask import request
from werkzeug.urls import url_parse
import os
from app.models import KhachHang
from sqlalchemy import update
from flask import Flask, render_template, redirect, request, session
from sqlalchemy import desc
from datetime import datetime



# @app.route('/home2',methods=['Get','Post'])
# def home2():
#     ListSach = db.session.query(Sach).all()
#     ListLoai = db.session.query(Loai).all()
#     if request.args.get("MaLoai")!=None:
#         key=request.args.get("MaLoai")
#         ListSach = db.session.query(Sach).filter(Sach.MaLoai==key).all()
#     if request.method=="POST":
#         key=request.form.get("search")
#         search = "%{}%".format(key)
#         ListSach = db.session.query(Sach).filter(Sach.TenSach.like(search)|Sach.TacGia.like(search)).all()
#     #10 cuốn bán chạy nhất
#     if request.args.get("top")!=None:
#         key=request.args.get("MaLoai")
#         ListSach = db.session.query(Sach).filter(Sach.MaSach==ChiTietHoaDon.MaSach).filter(ChiTietHoaDon.MaHoaDon==HoaDon.MaHoaDon).order_by(desc(HoaDon.NgayMua)).limit(10).all()
#     #9 cuốn số lượng lớn nhất
#     if request.args.get("recommend"):
#         ListSach = db.session.query(Sach).order_by(desc(Sach.SoLuong)).limit(10).all()
#     home="current-menu-item"
#     return render_template('home.html',ListLoai = ListLoai, ListSach = ListSach,home=home)

@app.route('/')
@app.route('/index')
@app.route('/home',methods=['Get','Post'])
def home():   
    ListSach = db.session.query(Sach).all()
    ListLoai = db.session.query(Loai).all()
    if request.args.get("MaLoai")!=None:
        key=request.args.get("MaLoai")
        ListSach = db.session.query(Sach).filter(Sach.MaLoai==key).all()
        ls = db.session.query(Loai).filter(Loai.MaLoai==key).first()
        flash('Sách Theo Loại :'+ls.TenLoai,'success')
    if request.method=="POST":
        key=request.form.get("search")
        search = "%{}%".format(key)
        ListSach = db.session.query(Sach).filter(Sach.TenSach.like(search)|Sach.TacGia.like(search)).all()
    #10 cuốn bán chạy nhất
    if request.args.get("top")!=None:
        key=request.args.get("MaLoai")
        ListSach = db.session.query(Sach).filter(Sach.MaSach==ChiTietHoaDon.MaSach).filter(ChiTietHoaDon.MaHoaDon==HoaDon.MaHoaDon).order_by(desc(HoaDon.NgayMua)).limit(10).all()
    #9 cuốn số lượng lớn nhất
    if request.args.get("recommend"):
        ListSach = db.session.query(Sach).order_by(desc(Sach.SoLuong)).limit(10).all()
    home="current-menu-item"
    if request.form.get("search")!=None:
        key=request.form.get("search")
        flash('Kết quả tìm kiếm:','success')
    else: key=""
    
    return render_template('home2.html',ListLoai = ListLoai, ListSach = ListSach,home=home,search=key)

# @app.route('/register',methods=['Get','Post'])
# def register():
#     if current_user.is_authenticated:
#         return redirect('/index')
#     form = RegisterForm()  
#     if request.method=="POST":
        
#         if form.password.data != form.passwordRepeat.data :
#             flash('Mật khẩu không trùng khớp')
#             return redirect('/register')
        
#         if KhachHang.query.filter_by(username=form.username.data).first() is not None:
#             flash('Username tồn tại ')
#             return redirect('/register')
#         u1=KhachHang(username=form.username.data,email=form.gmail.data,password=form.password.data)
#         db.session.add(u1)
#         db.session.commit()
#         flash(f'Register of user {form.username.data}')
#         login_user(u1)
#         # session["message"]="vonglam1"
#         return redirect('/register')
#     # else:   session["message"]="cai2"
#     return render_template('register.html',title='Register',form=form)
@app.route('/register', methods=['GET','POST'])
def register():
    if session.get("kh"):
        return redirect('/index')
    if request.method=="POST":
        if request.form.get("password") != request.form.get("passwordRepeat"):
            session["message"]= "Mật khẩu không khớp!"
            return redirect('/register')
        if KhachHang.query.filter_by(Username=request.form.get("username")).first() is not None:
            session["message"]= "Username đã tồn tại!"
            return redirect('/register')
        u1 = KhachHang(Username=request.form.get("username"), Email=request.form.get("email"), _password=request.form.get("password"),HoTen=request.form.get("hoten")
        ,SDT=request.form.get("sdt"), DiaChi=request.form.get("diachi"))
        # KhachHang.query.filter_by(MaKH=MaKH).delete()
        db.session.add(u1)
        db.session.commit() 
        user = {"id" : u1.MaKH, "username " : u1.Username,"name":u1.HoTen }
        session["kh"] = user
        session["message"]= "Đăng kí thành công!"
        return redirect('/index')
    
    
    return render_template('register.html',title='Register')
    ##############################
@app.route('/logout')
def logout():
    session["kh"]=None
    return redirect ('/index')
    #############################
@app.route('/login')
@app.route('/userlogin',methods=['Get','Post'])
def userlogin(): 
    if session.get("kh"):
        return redirect('/index')
    session["kh"]=None
    if request.method == 'POST':
        Username=request.form["Username"]
        _password = request.form["_password"]
        kh = KhachHang.query.filter_by(Username=Username,_password=_password).first()
        if kh is not None:
            user = {"id" : kh.MaKH, "username " : kh.Username,"name":kh.HoTen }
            session["kh"] = user
            return redirect('/index')
        else:
            message = "Đăng nhập sai "
            session["message"] = message
            return render_template('loginuser.html')
        
    else:
        return render_template('loginuser.html')



@app.route('/cart', methods=['Get'])
def cart():
    # param giả
    # listCart = [
    #     {
    #         "masach" : "1",
    #         "tensach" : "Tu tuong",
    #         "soluong" : 1,
    #         "anh" : "../static/image_sach/a1.jpg",
    #         "gia" : 100000
    #     },
    #     {
    #         "masach" : "2",
    #         "tensach" : "Viet Nam",
    #         "soluong" : 1,
    #         "anh" : "../static/image_sach/a3.jpg",
    #         "gia" : 100000
    #     }
    # ]

    # session["gh"] = listCart
    # session.pop('gh')
    hasCart = False
    tongTien = 0
 
    if session.get('gh') is not None:
        hasCart = True
        for item in session["gh"]:
            tongTien += item["soluong"] * item["gia"]

        tongTien = "{:,.0f}".format(tongTien)

    return render_template('cart.html', hasCart = hasCart, tongTien = tongTien)

@app.route('/detail', methods=['Post'])
def detail():
    soluong = request.form.get("soluong")
    type = request.form.get("type")
    masach = request.form.get("masach")

    list = session["gh"]
    session.pop('gh')

    if type == "edit":
        if soluong is None or soluong == "" :
            flash("Vui lòng nhập số lượng.", 'error')
            return redirect('cart')  
        
        for sach in list:
            if sach["masach"] == masach:
                if session.get('sl') is not None:
                    session["sl"] = session["sl"] - sach["soluong"] + int(soluong)
                sach["soluong"] = int(soluong)
                break
    elif type == "delete":
        for sach in list:
            if sach["masach"] == masach:
                if session.get('sl') is not None:
                    session["sl"] = session["sl"] - sach["soluong"] 
                list.remove(sach)
                break 
            
    session["gh"] = list
   
    flash("Cập nhật giỏ hàng thành công.", 'success')
    
    return redirect('cart') 

@app.route('/add-to-cart')
def add_to_cart():
    masach = request.args.get('masach')
    sach = Sach.query.filter_by(MaSach = masach).first()

    if sach is None:
        flash("Không tồn tại sản phẩm.", 'error')
        return 'sai'

    newcart = {
        "masach" : sach.MaSach,
        "tensach" : sach.TenSach,
        "soluong" : 1,
        "anh" : sach.Anh,
        "gia" : sach.Gia
    }

    if session.get('sl') is None:
        session["sl"]  = 1 
    else:
        session["sl"] =  session["sl"] + 1

    gh = None
    if session.get('gh') is not None:
        gh = session["gh"]

    if(gh is None):
        gh = []
        gh.append(newcart)
        session["gh"] = gh
    else:
        for sach in session["gh"]:
            if sach["masach"] == masach:
                sach["soluong"] = sach["soluong"] + 1

                flash("Thêm sản phẩm vào giỏ hàng thành công.", 'success')
                return redirect('cart')

        gh.append(newcart)
        session["gh"] = gh

    flash("Thêm sản phẩm vào giỏ hàng thành công.", 'success')
    return redirect('cart')

# Thanh toán 
@app.route('/payment')
def payment():
    if session.get("kh") is not None:
        if session.get("sl") is not None and session["sl"] <= 0:
            return redirect('cart')
    else:
        return redirect('userlogin') 

    idKH = session["kh"]["id"]  
    kh = KhachHang.query.filter_by(MaKH=idKH).first()

    tongTien = 0
 
    if session.get('gh') is not None:
        hasCart = True
        for item in session["gh"]:
            tongTien += item["soluong"] * item["gia"]

        tongTien = "{:,.0f}".format(tongTien)
    return render_template('payment.html', kh = kh, tongTien=tongTien);

@app.route('/confirm-payment')
def confirm_payment():
    if session.get("kh") is not None:
        if session.get("sl") is None or session["sl"] <= 0 or session.get('gh') is None:
            return redirect('cart')
    else:
        return redirect('userlogin') 

            
    idKH = session["kh"]["id"]  
    kh = KhachHang.query.filter_by(MaKH=idKH).first()

    now = datetime.now()
    # formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

    #add to bill
    hoadon = HoaDon(MaKH=kh.MaKH, NgayMua=now, damua=0)
    db.session.add(hoadon)
    db.session.commit()
    
    for sach in session["gh"]:
        cthd = ChiTietHoaDon(MaSach = sach["masach"], SoLuongMua = sach["soluong"], MaHoaDon = hoadon.MaHoaDon, damua = 0)
        db.session.add(cthd)
        db.session.commit()

    session["gh"] = None
    session["sl"] = None
    flash('Xác nhận đặt mua thành công', 'success')

    return redirect('home')

@app.route('/history')
def history():
    if session.get('kh') is None:
        return redirect('/userlogin')
    kh = session['kh']
    rs= db.session.query(KhachHang,HoaDon).filter(KhachHang.MaKH==HoaDon.MaKH).filter_by(MaKH=kh["id"]).all()

    def tinhTien(id):
        tongTien = 0
        kq = db.session.query(HoaDon,ChiTietHoaDon, Sach).filter(HoaDon.MaHoaDon==ChiTietHoaDon.MaHoaDon, ChiTietHoaDon.MaSach == Sach.MaSach).filter_by(MaHoaDon=id).all()
        for hd, cthd, sach in kq:
            tongTien += cthd.SoLuongMua * sach.Gia
        return tongTien

    return render_template('history.html', rs = rs, tinhTien=tinhTien)

@app.route('/detail-history')
def detailHistory():
    maDonHang = request.args.get('id')
    rs= db.session.query(HoaDon,ChiTietHoaDon, Sach).filter(HoaDon.MaHoaDon==ChiTietHoaDon.MaHoaDon, ChiTietHoaDon.MaSach == Sach.MaSach).filter_by(MaHoaDon=maDonHang).all()
    
    return render_template('detail-history.html', rs=rs);
######################################
@app.route('/admin')
@app.route('/adminlogin',methods=['Get','Post'])
def adminlogin(): 
    if session.get("TenDangNhap"):
        return redirect('/adminqlysach')
    if request.method == 'POST':
        TenDangNhap=request.form["TenDangNhap"]
        MatKhau = request.form["MatKhau"]
        admin = DangNhap.query.filter_by(TenDangNhap=TenDangNhap,MatKhau=MatKhau).first()
        if admin is not None:
            session["TenDangNhap"] = TenDangNhap
            return redirect('/adminqlysach')
        else:
            message = "Đăng nhập sai " + TenDangNhap
            session["message"] = message
            return render_template('adminlogin.html')
        
    else:
        return render_template('adminlogin.html')

@app.route('/logoutadmin')
def logoutadmin():
    session["TenDangNhap"]=None
    return redirect ('/admin')

@app.route('/adminqlysach',methods=['Get','Post'])
def adminqlysach():
    if session.get("TenDangNhap"):
        sach=db.session.query(Sach).all()
        ListLoai=Loai.query.filter_by().all()
        #sua sach dang test
        if request.method == 'POST' :
            MaSach= request.form.get("MaSach")
            TenSach= request.form.get("TenSach")
            SoLuong= request.form.get("SoLuong")
            Gia= request.form.get("Gia")
            MaLoai= request.form.get("MaLoai")
            SoTap= request.form.get("SoTap")
            NgayNhap= request.form.get("NgayNhap")
            TacGia = request.form.get("TacGia")
            MaSachBanDau = request.form.get("MaSachhidden")
            haveErr=False
            check=False
            try:
                date=datetime.strptime(NgayNhap, "%Y-%m-%d")
                check =MaSach!="" and TenSach!="" and SoLuong!="" and int(SoLuong)>0 and SoTap!="" and Gia!=""
            except:
                haveErr=True
            
            if request.form.get("btnSua")!=None and haveErr==False and check==True:
                MS=None
                if MaSach!=MaSachBanDau:
                    MS= Sach.query.filter_by(MaSach=MaSach).first()
                    #update
                if MS is None:
                    session["message"] = "Sửa thành Công Sách" 
                    Sach.query.filter_by(MaSach=MaSachBanDau).update(dict(MaLoai=MaLoai,SoTap=SoTap,TacGia=TacGia,SoLuong=SoLuong,TenSach=TenSach,MaSach=MaSach,Gia=Gia,NgayNhap=date))
                    ChiTietHoaDon.query.filter_by(MaSach=MaSachBanDau).update(dict(MaSach=MaSach))
                    db.session.commit()
                else:
                    session["message"]= "Mã sách đã tồn tại"
                return redirect('/adminqlysach')
            else:   session["message"]= " Sai định dạng nhập"
            if request.form.get("btnXoa")!=None :
                Sach.query.filter_by(MaSach=MaSachBanDau).delete()
                db.session.commit()
                session["message"] = "Xóa Thành Công Sách"
                return redirect('/adminqlysach')
        adminqlysach="active"
        return render_template('adminqlysach.html',sach=sach,ListLoai=ListLoai,adminqlysach=adminqlysach)
    else:
        return redirect('/admin')

@app.route('/adminthemsach',methods=['Get','Post'])
def adminthemsach():
    if session.get("TenDangNhap"):
        ListLoai=Loai.query.filter_by().all()
        if request.method == 'POST':
            uploaded_file=request.files['file']
            MaSach= request.form.get("MaSach")
            TenSach= request.form.get("TenSach")
            SoLuong= request.form.get("SoLuong")
            Gia= request.form.get("Gia")
            MaLoai= request.form.get("MaLoai")
            SoTap= request.form.get("SoTap")
            NgayNhap= request.form.get("NgayNhap")
            haveErr=False
            check=False
            try:
                date = datetime.datetime.strptime(NgayNhap, "%Y-%m-%d")
                check =MaSach!="" and TenSach!="" and SoLuong!="" and int(SoLuong)>0 and SoTap!="" and Gia!=""  
            except:
                haveErr=True
            TacGia = request.form.get("TacGia")
            Anh=None
            MS=None
            MS= Sach.query.filter_by(MaSach=MaSach).first()
            if MS is None and check and haveErr==False:
                #uploaded_file.save("static/images/"+uploaded_file.filename)
                try:
                    uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename))
                    Anh="image_sach/"+uploaded_file.filename
                    sach = Sach(Anh=Anh,MaSach=MaSach,TenSach=TenSach,SoLuong=SoLuong,Gia=Gia,MaLoai=MaLoai,SoTap=SoTap,NgayNhap=date,TacGia=TacGia)
                    db.session.add(sach)
                    db.session.commit()
                    session["message"] = "Thêm Sách Thành Công !"
                except:
                    session["message"] = "Up file lỗi, vui lòng thử lại"
            else:   session["message"] = "vui lòng nhập đúng thông tin!"
            return redirect('/adminthemsach')
        adminthemsach="active"
        return render_template('adminthemsach.html',ListLoai = ListLoai,adminthemsach=adminthemsach)
    else:
        return redirect('/admin')

@app.route('/adminloaisach',methods=['Get','Post'])
def adminloaisach():
    if session.get("TenDangNhap"):
        ListLoai=Loai.query.filter_by().all()
        if request.method == 'POST' :
            TenLoaiThem=request.form.get("TenLoaiThem")
            MaLoaiThem=request.form.get("MaLoaiThem")
            MaLoaiBanDau=request.form.get("MaLoaiBanDau")
            TenLoai=request.form.get("TenLoai")
            MaLoai=request.form.get("MaLoai")
            if request.form.get("btnSua")!=None and MaLoai!="" and TenLoai!="":
                Loai.query.filter_by(MaLoai=MaLoaiBanDau).update(dict(TenLoai=TenLoai,MaLoai=MaLoai))
                Sach.query.filter_by(MaLoai=MaLoaiBanDau).update(dict(MaLoai=MaLoai))
                db.session.commit()
                session["message"] = "Sửa Thành Công" 
                return redirect('/adminloaisach')
            if request.form.get("btnXoa")!=None:
                sach=Sach.query.filter_by(MaLoai=MaLoaiBanDau).first()
                if sach is None:
                    Loai.query.filter_by(MaLoai=MaLoaiBanDau).delete()
                    db.session.commit()
                    session["message"] = "Xóa Thành Công"
                else:  session["message"] = "Loại Sách đang được sử dụng cho sách" 
                return redirect('/adminloaisach')
            if request.form.get("btnThem")!=None and MaLoaiThem!="" and TenLoaiThem!="":
                loai=Loai.query.filter_by(MaLoai=MaLoaiThem).first()
                if loai is None:
                    l = Loai(MaLoai=MaLoaiThem,TenLoai=TenLoaiThem)
                    db.session.add(l)
                    db.session.commit()
                    session["message"] = "Thêm Thành công"
                else:   session["message"] = "Mã loại đã tồn tại" 
                return redirect('/adminloaisach')
                
        adminloaisach="active"
        return render_template('adminloaisach.html',ListLoai=ListLoai,adminloaisach=adminloaisach)
    else:
        return redirect('/admin')

@app.route('/adminqlyKH',methods=['Get','Post'])
def adminqlyKH():
    if session.get("TenDangNhap"):
        MaKH= request.form.get("btnXoa")
        if request.method=='POST' and request.form.get("btnXoa")!=None:
            hd=HoaDon.query.filter_by(MaKH=MaKH).first()
            if hd is None:
                KhachHang.query.filter_by(MaKH=MaKH).delete()
                db.session.commit()
                session["message"] = "Xóa Khách Hàng Thành Công"
            else:    session["message"] = "Khách Hàng Có Xóa Đơn nên không thể xóa!"
            
            return redirect('/adminqlyKH')

        kh=KhachHang.query.filter_by().all()
        adminqlyKH = "active"
        return render_template('adminqlyKH.html',adminqlyKH=adminqlyKH,kh=kh)
    else:
        return redirect('/admin')

@app.route('/adminhoadon',methods=['Get','Post'])
def adminhoadon():
    if session.get("TenDangNhap"):
        hd=HoaDon.query.all()	
        rs= db.session.query(HoaDon,KhachHang).filter(HoaDon.MaKH==KhachHang.MaKH).all()
        rscthd=None
        if request.method=='POST' and request.form.get("btnXacNhanCTHD")!=None:
            MaHDXem = request.args.get("MaHDXem")
            MaCTHD= request.form.get("btnXacNhanCTHD")
            ChiTietHoaDon.query.filter_by(MaCTHD=MaCTHD).update(dict(damua=True))
            db.session.commit()
            session["message"]= "Xác Nhận Thành công"
            cthdTest=None
            cthdTest = ChiTietHoaDon.query.filter_by(MaHoaDon=MaHDXem,damua=False).first()
            if cthdTest==None:
                HoaDon.query.filter_by(MaHoaDon=MaHDXem).update(dict(damua=True))
                db.session.commit()
                session["message"]= "Đã Thanh Toán Cả Hóa Đơn"
                return redirect('/adminhoadon')
            return redirect('/adminhoadon?MaHDXem='+MaHDXem)
            
        if request.method=='POST' :
            if request.form.get("btnXacNhan")!=None:
                MaHoaDon =request.form.get("btnXacNhan")
                HoaDon.query.filter_by(MaHoaDon=MaHoaDon).update(dict(damua=True))
                ChiTietHoaDon.query.filter_by(MaHoaDon=MaHoaDon).update(dict(damua=True))
                db.session.commit()
                session["message"]= "Xác Nhận Thành công"
            return redirect('/adminhoadon')
        #hien thi CTHD
        if request.args.get("MaHDXem")!= None:
            MaHDXem = request.args.get("MaHDXem")   
            rscthd= db.session.query(ChiTietHoaDon,Sach).filter(ChiTietHoaDon.MaSach==Sach.MaSach).filter_by(MaHoaDon=MaHDXem).all()
        

        # session["message"]= h.MaHoaDon
        adminhoadon= "active"
        return render_template('adminhoadon.html',adminhoadon=adminhoadon,hd=hd,rs=rs,rscthd=rscthd)
    else:
        return redirect('/admin')
