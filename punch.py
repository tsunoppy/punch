#! /Users/tsuno/.pyenv/shims/python3
# -*- coding: utf-8 -*-

# Calculation for Steel stiffnering following Building letter By BCJ
# Coded by tsunoppy on Sunday

import math

import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Punch:

    def __init__(self,c1,c2,d,calType):

        # Dimension
        self.c1 = c1 # column widht  (mm)
        self.c2 = c2 # column height (mm)
        self.d  = d  # punching depth (mm)
        self.calType = calType # "Internal" or "Edge" or "Cornner"

        # Section Prop.

        # Section Prop.
        if self.calType == "Internal":

            # Dim
            self.b1 = self.c1 + self.d
            self.b2 = self.c2 + self.d
            self.b0 = 2.0*self.b1 + 2.0*self.b2
            # Critical Section Area
            self.ac = self.b0 * self.d

            # For Xdir
            # Center of Prop
            self.cab = self.b1/2.0
            # Porlar Moment of Inertia
            self.jc = self.b1 * self.d **3 /12.0 + self.d * self.b1**3 / 12.0
            self.jc = 2.0 * self.jc
            self.jc = self.jc + 2.0 * self.b2 * self.d * (self.b1/2.0)**2

            # For Ydir
            # Center of Prop
            self.cba = self.b2/2.0
            # Porlar Moment of Inertia
            self.jcy = self.b2 * self.d **3 /12.0 + self.d * self.b2**3 / 12.0
            self.jcy = 2.0 * self.jcy
            self.jcy = self.jcy + 2.0 * self.b1 * self.d * (self.b2/2.0)**2

        elif self.calType == "Edge":

            # Dim
            self.b1 = self.c1 + self.d / 2.0
            self.b2 = self.c2 + self.d
            self.b0 = 2.0*self.b1 + self.b2
            # Critical Section Area
            self.ac = self.b0 * self.d

            # Xdir
            # Center of Prop
            self.cab = self.b1 **2
            self.cab = self.cab/ ( 2.0*self.b1 + self.b2 )
            # Porlar Moment of Inertia
            self.jc = self.b1 * self.d **3 /12.0 +\
                self.d * self.b1**3 / 12.0 +\
                ( self.b1*self.d ) * ( self.b1/2.0 - self.cab )**2
            self.jc = 2.0 * self.jc
            self.jc = self.jc + self.b2 * self.d * self.cab**2

            # Ydir
            # Center of Prop
            self.cba = self.b2 **2
            self.cba = self.cba/ ( 2.0*self.b1 + self.b2 )
            # Porlar Moment of Inertia
            self.jcy = self.b2 * self.d **3 /12.0 +\
                self.d * self.b2**3 / 12.0 +\
                ( self.b2*self.d ) * ( self.b2/2.0 - self.cba )**2
            self.jcy = 2.0 * self.jcy
            self.jcy = self.jcy + self.b1 * self.d * self.cba**2

        elif self.calType == "Cornner":
            # Dim
            self.b1 = self.c1 + self.d / 2.0
            self.b2 = self.c2 + self.d / 2.0
            self.b0 = self.b1 + self.b2

            # Critical Section Area
            self.ac = self.b0 * self.d

            # For Xdir
            # Center of Prop
            self.cab = self.b1 **2 / 2.0
            self.cab = self.cab/ ( self.b1 + self.b2 )
            # Porlar Moment of Inertia
            self.jc = self.b1 * self.d **3 /12.0 +\
                self.d * self.b1**3 / 12.0 +\
                ( self.b1*self.d ) * ( self.b1/2.0 - self.cab )**2
            self.jc = self.jc + self.b2 * self.d * self.cab**2

            # For Ydir
            # Center of Prop # Ydir
            self.cba = self.b2 **2 / 2.0
            self.cba = self.cba/ ( self.b1 + self.b2 )
            # Porlar Moment of Inertia
            self.jcy = self.b2 * self.d **3 /12.0 +\
                self.d * self.b2**3 / 12.0 +\
                ( self.b2*self.d ) * ( self.b2/2.0 - self.cba )**2
            self.jcy = self.jcy + self.b1 * self.d * self.cba**2


        else:
            print("err, calType")


        # Grobal var
        self.minimum = 0.0

        """
        print("Make Object")
        print("c1  = {:.2f} mm".format(self.c1))
        print("c2  = {:.2f} mm".format(self.c2))
        print("d   = {:.2f} mm".format(self.d))
        print("# Dimension")
        print("b1  = {:.2f} mm".format(self.b1))
        print("b2  = {:.2f} mm".format(self.b2))
        print("b0  = {:.2f} mm".format(self.b0))
        print("cab = {:.2f} mm".format(self.cab))
        print("Ac  = {:.2e} mm2".format(self.ac))
        print("Jc  = {:.2e} mm4".format(self.jc))
        """

    def edgeCal(self, vu, mu, fc, phai, s, fy):


        dx = self.c1/2.0 + self.d/2.0 - self.cab
        msc = mu - vu*dx/1000.0
        gamma_f = 1.0 / ( 1.0 + (2.0/3.0) * math.sqrt(self.b2/self.b1) )
        gamma = 1.0 - gamma_f
        mv = gamma*msc

        tau_u = vu*1000.0 / ( self.b0 *self.d )
        tau_v1 = mv*10**6 * self.cab / self.jc
        tau_v2 = mv*10**6 * (self.b1-self.cab)/self.jc

        tau_max = tau_u + tau_v1
        tau_min = tau_u - tau_v2

        # cal vc capacity
        if self.c1 > self.c2 :
            beta = self.c1/self.c2
        else:
            beta = self.c2/self.c1

        vc1 = 0.17*(1.0+2.0/beta)*math.sqrt(fc)

        if self.calType == "Internal":
            alphas = 40.0
        elif self.calType == "Edge":
            alphas = 30.0
        else:
            alphas = 20.0

        vc2 = 0.083*(alphas * self.d / self.b0 + 2.0) * math.sqrt(fc)
        vc3 = 0.33*math.sqrt(fc)

        vc = min(vc1,vc2)
        vc = min(vc,vc3)

        print("# Prop.")
        print("fc  = {:.0f} N/mm2".format(fc))
        print("# Design Load")
        print("Vu  = {:.2f} kN".format(vu))
        print("Mu  = {:.2f} kN.m".format(mu))
        print("Mu  = {:.2f} kN.m".format(msc))
        print("γ   = {:.2f} -".format(gamma))
        print("Msc'= {:.2f} kN.m".format(mv))
        print("# Calculate maximam v")
        print("vu  = {:.2f} N/mm2".format(tau_u))
        print("vv1 = {:.2f} N/mm2".format(tau_v1))
        print("vv2 = {:.2f} N/mm2".format(tau_v2))
        print("---->")
        print("vmin= {:.2f} N/mm2".format(tau_min))
        print("vmax= {:.2f} N/mm2".format(tau_max))
        print("# Capacity")
        print("vc1 = {:.2f} N/mm2".format(vc1))
        print("vc2 = {:.2f} N/mm2".format(vc2))
        print("vc3 = {:.2f} N/mm2".format(vc3))
        print("vc  = {:.2f} N/mm2".format(vc))
        print("---->")
        print("φ*vc= {:.2f} N/mm2".format(phai*vc))
        print("# Check concrete capacity")
        if phai*vc > tau_max :
            print( "vmax < φvc, OK" )
            vnmax = 0.0
            pvnmax = 0.0
            reqvs = 0.0
            reqas = 0.0

        else:
            print( "vmax > φvc, NG" )

            vnmax = 0.5 * math.sqrt(fc)
            pvnmax = phai*vnmax
            reqvs = (tau_max - phai*0.17*math.sqrt(fc))/phai
            reqas = reqvs * s * 10**6 / (fy*self.d)

            print("# Check capcity W/RF.")
            print("φ*vnmax= {:.2f} N/mm2".format(phai*vnmax))
            print("Req(Vs)= {:.2f} N/mm2".format(reqvs))
            print("Req(As)= {:.2f} mm2".format(reqas))

            if phai*vnmax < tau_max:
                print("φ*vnmax > tau_max, Re-Check dimension")
            else:
                print("φ*vnmax < tau_max, Place RF.")

        self.minimum = tau_min/tau_max


        return self.b1,self.b2,self.b0,self.d,\
            vu,mu,self.ac,self.jc,self.cab,\
            gamma_f,gamma,msc,mv,\
            tau_u,tau_v1,tau_v2,tau_max,tau_min,\
            vc1,vc2,vc3,vc,phai*vc,\
            vnmax,pvnmax,reqvs,reqas

    # matoplot
    #https://note.nkmk.me/python-matplotlib-patches-circle-rectangle/
    ##########################
    def model(self,ax,canv):

        fig = plt.figure()
        #ax = plt.axes()

        # standard parameter
        taumax = 3.0*self.d/4
        taumin = self.minimum*taumax

        # fc = face color, ec = edge color

        column = patches.Rectangle(xy=(0, 0), width=self.c1, height=self.c2, \
                                   linewidth="2.0", ec='#000000', color="gray", alpha=0.5 )

        if self.calType == "Internal":
            b1 = self.c1 + self.d
            b2 = self.c2 + self.d
            punch = patches.Rectangle(xy=(-self.d/2, -self.d/2), width=b1, height=b2, \
                                      ec='#000000', fill=False)

            forward1 = patches.Rectangle(xy=(self.c1+self.d/2.0, -self.d/2), width=taumax, height=b2, \
                                        ec='darkred', fill="lightblue", alpha=0.5)
            forward2 = patches.Rectangle(xy=(-self.d/2.0-taumin, -self.d/2), width=taumin, height=b2, \
                                        ec='darkred', fill="lightblue", alpha=0.5)

            x1 = -self.d/2.0
            y1 = self.c2 + self.d/2 + taumin
            x2 = self.c1 + self.d/2
            y2 = self.c2 + self.d/2 + taumax
            x3 = self.c1 + self.d/2
            y3 = self.c2 + self.d/2
            x4 = -self.d/2.0
            y4 = self.c2 + self.d/2

            #side = patches.Polygon(xy = [(0, 0), (self.d, 0), (0, self.d)],fc = "lightblue", ec = "darkred")
            side1 = patches.Polygon(xy = [(x1, y1), (x2, y2), (x3, y3), (x4,y4)],\
                                    fill = "lightblue", ec = "darkred", alpha=0.5)

            x1 = -self.d/2.0
            y1 = -self.d/2 - taumin
            x2 = self.c1 + self.d/2
            y2 = -self.d/2 - taumax
            x3 = self.c1 + self.d/2
            y3 = -self.d/2
            x4 = -self.d/2.0
            y4 = -self.d/2

            #side = patches.Polygon(xy = [(0, 0), (self.d, 0), (0, self.d)],fc = "lightblue", ec = "darkred")
            side2 = patches.Polygon(xy = [(x1, y1), (x2, y2), (x3, y3), (x4,y4)],\
                                    fill = "lightblue", ec = "darkred", alpha=0.5)
            ax.add_patch(forward1)
            ax.add_patch(forward2)
            ax.add_patch(side1)
            ax.add_patch(side2)

        elif self.calType == "Edge":
            b1 = self.c1 + self.d / 2.0
            b2 = self.c2 + self.d
            punch = patches.Rectangle(xy=(0, -self.d/2), width=b1, height=b2, \
                                      ec='#000000', fill=False)


            forward = patches.Rectangle(xy=(b1, -self.d/2), width=taumax, height=b2, \
                                        ec='darkred', fill="lightblue", alpha=0.5)

            x1 = 0.0
            y1 = self.c2 + self.d/2 + taumin
            x2 = b1
            y2 = self.c2 + self.d/2 + taumax
            x3 = self.c1 + self.d/2
            y3 = self.c2 + self.d/2
            x4 = 0.0
            y4 = self.c2 + self.d/2

            #side = patches.Polygon(xy = [(0, 0), (self.d, 0), (0, self.d)],fc = "lightblue", ec = "darkred")
            side1 = patches.Polygon(xy = [(x1, y1), (x2, y2), (x3, y3), (x4,y4)],\
                                    fill = "lightblue", ec = "darkred", alpha=0.5)

            x1 = 0.0
            y1 = - self.d/2 - taumin
            x2 = b1
            y2 = - self.d/2 - taumax
            x3 = self.c1 + self.d/2
            y3 = - self.d/2
            x4 = 0.0
            y4 = - self.d/2

            side2 = patches.Polygon(xy = [(x1, y1), (x2, y2), (x3, y3), (x4,y4)],\
                                    fill = "lightblue", ec = "darkred", alpha=0.5)

            ax.add_patch(forward)
            ax.add_patch(side1)
            ax.add_patch(side2)

        elif self.calType == "Cornner":
            b1 = self.c1 + self.d / 2.0
            b2 = self.c2 + self.d / 2.0
            punch = patches.Rectangle(xy=(0, -self.d/2), width=b1, height=b2, \
                                      ec='#000000', fill=False)

            forward = patches.Rectangle(xy=(b1, -self.d/2), width=taumax, height=b2, \
                                        ec='darkred', fill="lightblue", alpha=0.5)

            x1 = 0.0
            y1 = - self.d/2 - taumin
            x2 = b1
            y2 = - self.d/2 - taumax
            x3 = self.c1 + self.d/2
            y3 = - self.d/2
            x4 = 0.0
            y4 = - self.d/2

            side1 = patches.Polygon(xy = [(x1, y1), (x2, y2), (x3, y3), (x4,y4)],\
                                    fill = "lightblue", ec = "darkred", alpha=0.5)

            ax.add_patch(forward)
            ax.add_patch(side1)

        else:
            print("Erro, calType invalid")


        ax.add_patch(column)
        ax.add_patch(punch)
        ax.axvline( x = self.c1+self.d/2.0-self.cab , c="black")

        #plt.axis('scaled')
        ax.axis('scaled')
        ax.set_aspect('equal')
        ax.axis("off")
        #ax.set_ylim(hh-1450, hh+50)
        #ax.set_xlim(-50, 1500)
        #plt.savefig('./db/sample.jpg')
        #plt.plot([0,0],[self.c1/2,self.c2/2]) だめ

        """
        plt.show()
        plt.close(fig)
        """
        canv.draw()

        #obj.draw()


    ########################################################################
    def image_pdf(self,imagefile,c1,c2,d,b1,b2,calType,taumax,taumin):

        fig = plt.figure()
        ax = plt.axes()

        # standard parameter
        taumin = taumin/taumax* 3.0/4.0*d
        taumax = 3.0*d/4

        # fc = face color, ec = edge color

        column = patches.Rectangle(xy=(0, 0), width=c1, height=c2, \
                                   linewidth="2.0", ec='#000000', color="gray", alpha=0.5 )

        if calType == "Internal":
            punch = patches.Rectangle(xy=(-d/2, -d/2), width=b1, height=b2, \
                                      ec='#000000', fill=False)

            forward1 = patches.Rectangle(xy=(c1+d/2.0, -d/2), width=taumax, height=b2, \
                                        ec='darkred', fill="lightblue", alpha=0.5)
            forward2 = patches.Rectangle(xy=(-d/2.0-taumin, -d/2), width=taumin, height=b2, \
                                        ec='darkred', fill="lightblue", alpha=0.5)

            x1 = -d/2.0
            y1 = c2 + d/2 + taumin
            x2 = c1 + d/2
            y2 = c2 + d/2 + taumax
            x3 = c1 + d/2
            y3 = c2 + d/2
            x4 = -d/2.0
            y4 = c2 + d/2

            #side = patches.Polygon(xy = [(0, 0), (d, 0), (0, d)],fc = "lightblue", ec = "darkred")
            side1 = patches.Polygon(xy = [(x1, y1), (x2, y2), (x3, y3), (x4,y4)],\
                                    fill = "lightblue", ec = "darkred", alpha=0.5)

            x1 = -d/2.0
            y1 = -d/2 - taumin
            x2 = c1 + d/2
            y2 = -d/2 - taumax
            x3 = c1 + d/2
            y3 = -d/2
            x4 = -d/2.0
            y4 = -d/2

            #side = patches.Polygon(xy = [(0, 0), (d, 0), (0, d)],fc = "lightblue", ec = "darkred")
            side2 = patches.Polygon(xy = [(x1, y1), (x2, y2), (x3, y3), (x4,y4)],\
                                    fill = "lightblue", ec = "darkred", alpha=0.5)
            ax.add_patch(forward1)
            ax.add_patch(forward2)
            ax.add_patch(side1)
            ax.add_patch(side2)

        elif calType == "Edge":
            punch = patches.Rectangle(xy=(0, -d/2), width=b1, height=b2, \
                                      ec='#000000', fill=False)


            forward = patches.Rectangle(xy=(b1, -d/2), width=taumax, height=b2, \
                                        ec='darkred', fill="lightblue", alpha=0.5)

            x1 = 0.0
            y1 = c2 + d/2 + taumin
            x2 = b1
            y2 = c2 + d/2 + taumax
            x3 = c1 + d/2
            y3 = c2 + d/2
            x4 = 0.0
            y4 = c2 + d/2

            #side = patches.Polygon(xy = [(0, 0), (d, 0), (0, d)],fc = "lightblue", ec = "darkred")
            side1 = patches.Polygon(xy = [(x1, y1), (x2, y2), (x3, y3), (x4,y4)],\
                                    fill = "lightblue", ec = "darkred", alpha=0.5)

            x1 = 0.0
            y1 = - d/2 - taumin
            x2 = b1
            y2 = - d/2 - taumax
            x3 = c1 + d/2
            y3 = - d/2
            x4 = 0.0
            y4 = - d/2

            side2 = patches.Polygon(xy = [(x1, y1), (x2, y2), (x3, y3), (x4,y4)],\
                                    fill = "lightblue", ec = "darkred", alpha=0.5)

            ax.add_patch(forward)
            ax.add_patch(side1)
            ax.add_patch(side2)

        elif calType == "Cornner":
            punch = patches.Rectangle(xy=(0, -d/2), width=b1, height=b2, \
                                      ec='#000000', fill=False)

            forward = patches.Rectangle(xy=(b1, -d/2), width=taumax, height=b2, \
                                        ec='darkred', fill="lightblue", alpha=0.5)

            x1 = 0.0
            y1 = - d/2 - taumin
            x2 = b1
            y2 = - d/2 - taumax
            x3 = c1 + d/2
            y3 = - d/2
            x4 = 0.0
            y4 = - d/2

            side1 = patches.Polygon(xy = [(x1, y1), (x2, y2), (x3, y3), (x4,y4)],\
                                    fill = "lightblue", ec = "darkred", alpha=0.5)

            ax.add_patch(forward)
            ax.add_patch(side1)

        else:
            print("Erro, calType invalid")


        ax.add_patch(column)
        ax.add_patch(punch)
        ax.axvline( x = self.c1+self.d/2.0-self.cab , c="black")

        #plt.axis('scaled')
        ax.axis('scaled')
        ax.set_aspect('equal')
        ax.axis("off")
        #ax.set_ylim(hh-1450, hh+50)
        #ax.set_xlim(-50, 1500)
        plt.savefig(imagefile)
        #plt.plot([0,0],[self.c1/2,self.c2/2]) だめ

        """
        plt.show()
        plt.close(fig)
        """
        #canv.draw()

########################################################################
# End Class

# imput data
"""
c1 = 600.
c2 = 600.
d = 440.
calType = "Edge"
fc = 35.0
phai = 0.75
s = 100.0
fy = 390

joint = Punch(c1,c2,d,calType)
vu = 1634.00 #kN
#vu = 0
#vu = 1000.00 #kN
#msc = 1700.0 # kN.m
msc = 1500.0 # kN.m
joint.edgeCal(vu,msc,fc,phai,s,fy)
joint.model()


#Punch(c1,c2,d,"Int").model()
#Punch(c1,c2,d,"Cornner").model()
"""

#Punch(c1,c2,d,"Cornner").image_pdf(c1,c2,d,b1,b2,calType,taumax,taumin):
#Punch(600,600,420,"Cornner").image_pdf(1,600,600,420,1360,1720,"Cornner",2.1,0.4)
