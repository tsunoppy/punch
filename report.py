#! /Users/tsuno/.pyenv/shims/python3
# -*- coding:utf-8 -*-
import os, sys
import punch
#import Image
#import urllib2
#from cStringIO import StringIO


#zipアーカイブからファイルを読み込むため。通常は必要ないはず。
#sys.path.insert(0, 'reportlab.zip')

import reportlab
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm

#
import linecache
#

class Report():

    def __init__(self):
        #self.FONT_NAME = "Helvetica"
        self.FONT_NAME = "GenShinGothic"
        GEN_SHIN_GOTHIC_MEDIUM_TTF = "./fonts/GenShinGothic-Monospace-Medium.ttf"
        # フォント登録
        pdfmetrics.registerFont(TTFont('GenShinGothic', GEN_SHIN_GOTHIC_MEDIUM_TTF))
        #font_size = 20
        #c.setFont('GenShinGothic', font_size)

    ########################################################################
    # 文字と画像を配置
    def create_row(self,c, index, data, index2):
        y_shift = -240 * index
        #y_shift = -180 * index
        c.setFont(self.FONT_NAME, 9)
        """
        for i in range(0,len(data)):
            # txt
            c.drawString(300, 720-(i-1)*10 + y_shift, data[i])
        """
        c.drawString(55, self.ypos(0,y_shift), data[0].encode('utf-8'))
        c.drawString(55, self.ypos(1,y_shift), data[1].encode('utf-8'))

        # Slab Condition
        #lx = "{:.2f}".format(float(data[2]))
        #ly = "{:.2f}".format(float(data[3]))
        c1 = data[2]
        c2 = data[3]
        dp = data[4]
        dt = data[5]
        calType = data[6]
        phai = data[7]
        facdl = data[8]
        facll = data[9]
        vdl = data[10]
        vll = data[11]
        mdl  = data[12]
        mll  = data[13]
        fc   = data[14]
        fy = data[15]
        s = data[16]
        # from out

        b1 = data[17]
        b2 = data[18]
        b0 = data[19]
        d  = data[20]
        #
        vu = data[21]
        mu = data[22]
        ac = data[23]
        jc = data[24]
        cab  = data[25]
        #
        gamma_f = data[26]
        gamma_v   = data[27]
        msc = data[28]
        mv  = data[29]
        tau_u  = data[30]
        tau_v1 = data[31]
        tau_v2 = data[32]
        tau_max = data[33]
        tau_min = data[34]
        vc1 = data[35]
        vc2  = data[36]
        vc3 = data[37]

        vc = data[38]
        pvc = data[39]
        # Check RF.
        vnmax = data[40]
        pvnmax = data[41]
        reqvs = data[42]
        reqas = data[43]
        # Judge
        concreteJudge = data[44]
        judge = data[45]

        # Design Condition
        c.drawString(55, self.ypos(3,y_shift),
                     "Column:"\
                     )
        c.drawString(60, self.ypos(4,y_shift),
                     "c1xc2 = " + c1 + "mm x " + c2 + "mm"\
                     )
        c.drawString(55, self.ypos(5,y_shift),
                     "Drop Panel:"\
                     )
        c.drawString(60, self.ypos(6,y_shift),
                     "dp =" + dp + "mm, dt=" + dt + "mm"\
                     )

        ########################################################################
        c.drawString(55, self.ypos(9,y_shift),
                     "Design Condition"\
                     )
        #
        c.drawString(60, self.ypos(10,y_shift),
                     "Type:" \
                     )
        c.drawString(160, self.ypos(10,y_shift),
                     calType\
                     )
        #
        c.drawString(60, self.ypos(11,y_shift),
                     "Reduction Factor:"\
                     )
        c.drawString(160, self.ypos(11,y_shift),
                     "φ =" + phai + "-"\
                     )
        #
        ##
        c.drawString(60, self.ypos(12,y_shift),
                     "Load Comb.:"\
                     )
        c.drawString(160, self.ypos(12,y_shift),
                     facdl + "DL + " + facll + "LL"\
                     )
        #
        c.drawString(60, self.ypos(13,y_shift),
                     "Shear Force, kN:"\
                     )
        c.drawString(160, self.ypos(13,y_shift),
                     "VDL=" + vdl + ", VLL=" + vll \
                     )
        #
        c.drawString(60, self.ypos(14,y_shift),
                     "Bending Moment, kN.m:"\
                     )
        c.drawString(160, self.ypos(14,y_shift),
                     "MDL=" + mdl  + ", MLL=" + mll \
                     )

        c.drawString(55, self.ypos(16,y_shift),
                     "Material"\
                     )
        c.drawString(60, self.ypos(17,y_shift),
                     "Cocrete:"\
                     )
        c.drawString(160, self.ypos(17,y_shift),
                     "fc=" + fc  + "N/mm2"\
                     )
        c.drawString(60, self.ypos(18,y_shift),
                     "RF.:"\
                     )
        c.drawString(160, self.ypos(18,y_shift),
                     "fy=" + fy  + "N/mm2" + "( @" + s +")"\
                     )
        #
        ########################################################################
        #
        c.drawString(250, self.ypos(9,y_shift),
                     "Dimension"\
                     )

        c.drawString(260, self.ypos(10,y_shift),
                     "b1 = " + b1 + "mm, b2= " + b2 + "mm"\
                     )

        c.drawString(260, self.ypos(11,y_shift),
                     "b0 = " + b0 + "mm, d = " + d + "mm"\
                     )
        #
        c.drawString(250, self.ypos(13,y_shift),
                     "Load"\
                     )

        c.drawString(260, self.ypos(14,y_shift),
                     "Vu = " + vu + "kN" \
                     )
        c.drawString(260, self.ypos(15,y_shift),
                     "Mu = " + mu + "kN.m" \
                     )
        #
        c.drawString(250, self.ypos(17,y_shift),
                     "Prop"\
                     )

        c.drawString(260, self.ypos(18,y_shift),
                     "Ac = " + ac + "mm2" \
                     )
        c.drawString(260, self.ypos(19,y_shift),
                     "Jc = " + jc + "mm4" \
                     )
        c.drawString(260, self.ypos(20,y_shift),
                     "cab= " + cab + "mm" \
                     )
        ########################################################################
        # right side
        c.drawString(390, self.ypos(0,y_shift),
                     "- Evaluate Design Moment"\
                     )
        c.drawString(400, self.ypos(1,y_shift),"γf=")
        c.drawString(430, self.ypos(1,y_shift),
                     gamma_f + "-")
        c.drawString(480, self.ypos(1,y_shift),"γv=")
        c.drawString(510, self.ypos(1,y_shift),
                     gamma_v + "kN.m")
        c.drawString(400, self.ypos(2,y_shift),"Mu'=")
        c.drawString(430, self.ypos(2,y_shift),
                     msc + "kN.m")
        c.drawString(480, self.ypos(2,y_shift),"Msc=")
        c.drawString(510, self.ypos(2,y_shift),
                     mv + "kN.m")
        #
        #
        c.drawString(390, self.ypos(4,y_shift),
                     "- Analysis"\
                     )
        c.drawString(400, self.ypos(5,y_shift),"vug=")
        c.drawString(430, self.ypos(5,y_shift),
                     tau_u + "N/mm2")

        c.drawString(400, self.ypos(6,y_shift),"vv1=")
        c.drawString(430, self.ypos(6,y_shift),
                     tau_v1 + "N/mm2")
        c.drawString(480, self.ypos(6,y_shift),"vv2=")
        c.drawString(510, self.ypos(6,y_shift),
                     tau_v2 + "N/mm2")

        c.drawString(400, self.ypos(7,y_shift),"vmax=")
        c.drawString(430, self.ypos(7,y_shift),
                     tau_max + "N/mm2")
        c.drawString(480, self.ypos(7,y_shift),"vmin=")
        c.drawString(510, self.ypos(7,y_shift),
                     tau_min + "N/mm2")
        #
        #
        c.drawString(390, self.ypos(9,y_shift),
                     "- Check Concrete Capactiy"\
                     )
        c.drawString(400, self.ypos(10,y_shift),"vc1=")
        c.drawString(430, self.ypos(10,y_shift),
                     vc1 + "N/mm2")
        c.drawString(480, self.ypos(10,y_shift),"vc2=")
        c.drawString(510, self.ypos(10,y_shift),
                     vc2 + "N/mm2")
        c.drawString(400, self.ypos(11,y_shift),"vc3=")
        c.drawString(430, self.ypos(11,y_shift),
                     vc3 + "N/mm2")

        c.drawString(400, self.ypos(12,y_shift),"vc= min(vc1,vc2,vc3) =")
        c.drawString(510, self.ypos(12,y_shift),
                     vc + "N/mm2")

        c.drawString(400, self.ypos(13,y_shift),"φvc=")
        c.drawString(430, self.ypos(13,y_shift),
                     pvc + "N/mm2")
        c.drawString(400, self.ypos(14,y_shift),"---" + concreteJudge)
        #
        #
        c.drawString(390, self.ypos(16,y_shift),
                     "- Check Shear RF"\
                     )
        c.drawString(400, self.ypos(17,y_shift),"vnmax=")
        c.drawString(430, self.ypos(17,y_shift),
                     vnmax + "N/mm2")
        c.drawString(480, self.ypos(17,y_shift),"φvnmax")
        c.drawString(510, self.ypos(17,y_shift),
                     pvnmax + "N/mm2")
        c.drawString(400, self.ypos(18,y_shift),"Req(vs)=")
        c.drawString(480, self.ypos(18,y_shift),
                     reqvs + "N/mm2")
        c.drawString(400, self.ypos(19,y_shift),"Req(As)=")
        c.drawString(480, self.ypos(19,y_shift),
                     reqas + "mm2")
        c.drawString(400, self.ypos(20,y_shift),"---" + judge)
        #
#        c.drawString(260, self.ypos(2,y_shift),
#                     "fc = "
#                     )

        """
        for i in range(2,len(data)):
            # txt
            #c.drawString(300, 720-(i-1)*10 + y_shift, data[i])
            c.drawString(510, 720-(i-1)*10 + y_shift, data[i])
        """
        imagefile="./db/image" + str(index2+index) + ".jpg"
        punch.Punch(float(c1),float(c2),float(d),calType).\
            image_pdf(imagefile,float(c1),float(c2),float(d),float(b1),float(b2),calType,float(tau_max),float(tau_min))

        # png

        print("Index=",index2+index)
        c.drawImage(imagefile, 250,  y_shift + 470, width=5*cm , preserveAspectRatio=True)
        print(os.listdir('./db'))
        os.remove(imagefile)
        print(os.listdir('./db'))

    def boundimage(self,index):

        if index == 0 or index == 1: # ４辺固定
            image_data = "./images/4sideFix.jpg"
        elif index == 2: # ３辺固定
            image_data = "./images/m3_1.jpg"
        elif index == 3:# ３辺固定
            image_data = "./images/m3_2.jpg"
        elif index == 4:# ２辺固定
            image_data = "./images/m2.jpg"
        elif index ==5: # 4辺支持
            image_data = "./images/m4pin.jpg"
        elif index ==6: # 3辺支持長辺支持
            image_data = "./images/m3_1pin.jpg"
        elif index ==7: # ３辺固定短辺支持
            image_data = "./images/m3-1pin2.jpg"
        elif index ==8: # 2辺固定2辺支持
            image_data = "./images/m2_2pin.jpg"
        elif index ==9: # 2辺固定2辺支持
            image_data = "./images/m2_2pin2.jpg"
        elif index ==10: # 2辺固定2辺支持
            image_data = "./images/m2_2pin3.jpg"
        elif IdBound ==11: # 短辺1辺固定3辺支持
            image_data = "./images/m1-3pin1.jpg"
        elif IdBound ==12: # 長辺1辺固定3辺支持
            image_data = "./images/m1-3pin2.jpg"
        else:
            print("Error report/def")

        return image_data

    def ypos(self,ipos,y_shift):
        return 730-(ipos-1)*10 + y_shift

    ########################################################################
    # pdfの作成
    def print_page(self, c, index, nCase):


        #タイトル描画
        c.setFont(self.FONT_NAME, 20)
        #c.drawString(50, 795, u"Design of the twoway slab")
        c.drawString(50, 795, u"Two Way Shear")

        #グリッドヘッダー設定
        xlist = [40, 380, 560]
        ylist = [760, 780]
        c.grid(xlist, ylist)

        #sub title
        c.setFont(self.FONT_NAME, 12)
        c.drawString(55, 765, u"Condtion")
        c.drawString(390, 765, u"Design")

        #データを描画
        ########################################################################
        #for i, data in range(0,int(nCase)):

        for i in range(0,nCase):
#            f = open(inputf[index+i],'r')

            """
            tmpData = []
            while True:
                line = f.readline()
                if line:
                    if line != '\n':
                        tmpData.append(line.replace('\n',''))
                    else:
                        tmpData.append('')
                else:
                    break
            """
            line = linecache.getline('./db/rcslab.txt', index+i+1 )
            data = line.split(', ')

            linecache.clearcache()
            #f.close()
            #data = tmpData
            self.create_row( c, i, data, index )

        #最後にグリッドを更新
        ylist = [40,  280,  520,  760]
        #ylist = [40,  160, 280, 400, 520, 640, 760]
        #ylist = [40,  220,  400, 580, 760]4bunnkatsu
        c.grid(xlist, ylist[3 - nCase:])
        #ページを確定
        c.showPage()

    ########################################################################
    # pdfの作成
    def print_head(self, c , title):

        #title = 'Sample Project'

        #タイトル描画
        c.setFont(self.FONT_NAME, 20)
        c.drawString(50, 795, title)

        #sub title
        c.setFont(self.FONT_NAME, 12)

        #データを描画
        ########################################################################
        inputf = './db/input.txt'
        f = open(inputf,'r', encoding='utf-8')
        tmpData = []
        while True:
            line = f.readline()
            if line:
                if line != '\n':
                    tmpData.append(line.replace('\n',''))
                else:
                    tmpData.append('')
            else:
                break
        f.close()
        data = tmpData
        #c.setFont(self.FONT_NAME, 9)
        for i in range(0,len(data)):
            # txt
            c.drawString(55, 720-(i-1)*14, data[i])
        """
        # Model Diagram
        imagefile = './db/model.png'
        c.drawImage(imagefile, 60,  -300, width=18*cm , preserveAspectRatio=True)
        """
        #ページを確定
        c.showPage()
    ########################################################################
    # whole control
    def create_pdf(self, dataNum, pdfFile, title):

        # Parameter -------
        # inputf   : path to text file
        # imagefile: path to png file
        # pdfFile  : name of making pdf file

        #フォントファイルを指定して、フォントを登録
        #folder = os.path.dirname(reportlab.__file__) + os.sep + 'fonts'
        #pdfmetrics.registerFont(TTFont(FONT_NAME, os.path.join(folder, 'ipag.ttf')))
        #出力するPDFファイル
        c = canvas.Canvas(pdfFile)

        # ページ数
        ########################################################################
        #dataNum = len(inputf)
        numPage = dataNum // 3
        numMod = dataNum % 3
        #print(numPage,numMod)
        if numMod >= 1:
            numPage = numPage + 1

        # pdfの作成
        ########################################################################
        #self.print_head( c , title)

        for i in range(0,numPage):
            index = 3*i # index: 参照データのインデックス
            if numPage == 1:
                self.print_page( c, index, dataNum)
            elif i != numPage-1 and numPage != 1:
                self.print_page( c, index, 3)
            else:
                if numMod != 0:
                    self.print_page( c, index, numMod)
                else:
                    self.print_page( c, index, 3 )

        #pdfファイル生成
        ########################################################################
        c.save()
        print ("repot.py is Okay!!.")

########################################################################
# END CLASS


"""
########################################################################
# test script

pathname = "./test.pdf"
obj = Report()
# テキストの読み込み
########################################################################
inputf = []
inputf.append("./db/rcslab.txt")
inputf.append("./db/rcslab.txt")
inputf.append("./db/rcslab.txt")
inputf.append("./db/rcslab.txt")
inputf.append("./db/rcslab.txt")
inputf.append("./db/rcslab.txt")

title = "sample"

obj.create_pdf(3,pathname,title)
"""
