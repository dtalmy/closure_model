from MITgcmutils import *
from pylab import *
from numpy import *
import numpy
from scipy import *

# load data

dat = rdmnc('../ecco_gud_20210726_00*/ptr_tave.0000000000.*',slices=s_[6:11,0,:,:])

lphyto = dat['c01'] 
sphyto = dat['c02'] 
pombac = dat['c03'] 
dombac = dat['c04'] 

#vlphyto = dat['c21'] + dat['c22'] + dat['c23'] + dat['c24'] + dat['c25']
#vsphyto = dat['c26'] + dat['c27'] + dat['c28'] + dat['c29'] + dat['c30']
#vpombac = dat['c31'] + dat['c32'] + dat['c33'] + dat['c34'] + dat['c35']
#vdombac = dat['c36'] + dat['c37'] + dat['c38'] + dat['c39'] + dat['c40']
vlphyto = dat['c05'] 
vsphyto = dat['c05'] 
vpombac = dat['c05'] 
vdombac = dat['c05'] 

zoo = dat['c06']

doc = dat['DOC']
don = dat['DON']
poc = dat['POC']
pon = dat['PON']

# totals for later
tvbac = vpombac + vdombac
tbac = pombac + dombac
tbac = ma.masked_where(tbac<0.125,tbac)

# plot surface maps

lphyto = numpy.average(lphyto,0)
sphyto = numpy.average(sphyto,0)
pombac = numpy.average(pombac,0)
dombac = numpy.average(dombac,0)

vlphyto = numpy.average(vlphyto,0)
vsphyto = numpy.average(vsphyto,0)
vpombac = numpy.average(vpombac,0)
vdombac = numpy.average(vdombac,0)

doc = numpy.average(doc,0)
don = numpy.average(don,0)
poc = numpy.average(poc,0)
pon = numpy.average(pon,0)

zoo = numpy.average(zoo,0)

# set up figures
f1,ax1 = subplots()
f2,ax2 = subplots()
f3,ax3 = subplots()
f4,ax4 = subplots()
f5,ax5 = subplots()
f6,ax6 = subplots()
f7,ax7 = subplots()
f8,ax8 = subplots()
f9,ax9 = subplots()
f10,ax10 = subplots()
f11,ax11 = subplots()
f12,ax12 = subplots()
f13,ax13 = subplots()

# now actually do the plotting
p1 = ax1.pcolor(lphyto)
p2 = ax2.pcolor(sphyto)
p3 = ax3.pcolor(pombac)
p4 = ax4.pcolor(dombac)

p5 = ax5.pcolor(vlphyto)
p6 = ax6.pcolor(vsphyto)
p7 = ax7.pcolor(vpombac)
p8 = ax8.pcolor(vdombac)

p9 = ax9.pcolor(doc)
p10 = ax10.pcolor(don)
p11 = ax11.pcolor(poc)
p12 = ax12.pcolor(pon)

p13 = ax13.pcolor(zoo)

f1.colorbar(p1)
f2.colorbar(p2)
f3.colorbar(p3)
f4.colorbar(p4)
f5.colorbar(p5)
f6.colorbar(p6)
f7.colorbar(p7)
f8.colorbar(p8)
f9.colorbar(p9)
f10.colorbar(p10)
f11.colorbar(p11)
f12.colorbar(p12)
f13.colorbar(p13)

# now save the figures

f1.savefig('figures/mlphyt')
f2.savefig('figures/msphyt')
f3.savefig('figures/mpombac')
f4.savefig('figures/mdombac')

f5.savefig('figures/vlphyt')
f6.savefig('figures/vsphyt')
f7.savefig('figures/vpombac')
f8.savefig('figures/vdombac')

f9.savefig('figures/odoc')
f10.savefig('figures/odon')
f11.savefig('figures/opoc')
f12.savefig('figures/opon')

f13.savefig('figures/zoo')

