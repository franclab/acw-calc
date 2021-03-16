import ezdxf
import numpy as np

# Datos iniciales

q=2.5 #ranuras por polo y por fase
p=2 #pares de polos
m=3 #fases
cap=2 #nro de capas (1 o 2)
diam=7
# COnductor
denc=2.7
dcond=0.2 # diametro conductor
#calculo nro ranuras
Q=int(q*2*p*m)

pshort=1.5 #acortamiento en ranuras
coil_pitch=Q/(2*p) #paso de bobina en ranuras
ran_ang=2*np.pi*p/Q #ang de ranura en grados electricos
ran_ang_mec=2*np.pi/Q

# coord polares a cartesianas
def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

# Crear nuevo dibujo
doc = ezdxf.new('R12')
msp = doc.modelspace()

msp.add_circle((0,0),radius=diam/2)

# Bloque de ranura 1 capa
if cap==1:
    ranura = doc.blocks.new('ranura')
    ranura.add_line((-dcond/2,0),(-dcond/2,dcond))
    ranura.add_line((-dcond/2,dcond),(dcond/2,dcond))
    ranura.add_line((dcond/2,dcond),(dcond/2,0))
else:
    ranura = doc.blocks.new('ranura')
    ranura.add_line((-dcond / 2, 0), (-dcond / 2, dcond*2))
    ranura.add_line((-dcond / 2, dcond*2), (dcond / 2, dcond*2))
    ranura.add_line((dcond / 2, dcond*2), (dcond / 2, 0))


# Bloque conductor
cond_in = doc.blocks.new('cond_in')
cond_in.add_circle((0,0),radius=dcond/2)
cond_in.add_line((0,-dcond/2),(0,dcond/2))
cond_in.add_line((-dcond/2,0),(dcond/2,0))


cond_out = doc.blocks.new('cond_out')
cond_out.add_circle((0,0),radius=dcond/2)
cond_out.add_circle((0,0),radius=dcond/10)

# Dibujar ranuras
for i in range(Q):
    #msp.add_text(f'{i+1}',dxfattribs={'height':dcond,'rotation':360 / Q * i}).set_pos(pol2cart(diam/2+dcond*3,np.pi/2+(2*np.pi)/Q*i),align='MIDDLE_CENTER')
    msp.add_blockref('ranura',pol2cart(diam/2,np.pi/2+(2*np.pi)/Q*i), dxfattribs={
       'rotation': 360/Q*i
    })
# Dibujar conductores
# capa abajo
for i in range(2*p):
    for j in range(round(q)):
        if i%2==0:
         msp.add_blockref('cond_in', pol2cart(diam/2+dcond/2, np.pi/2-ran_ang_mec*j-i*2*np.pi/(2*p)), dxfattribs={
                'rotation': -ran_ang_mec*j-i*360/(2*p)
            })
        else:
            msp.add_blockref('cond_out', pol2cart(diam / 2 + dcond / 2, np.pi / 2 - ran_ang_mec * j - i * 2 * np.pi / (2 * p)),dxfattribs={
                                 'rotation': -ran_ang_mec * j - i * 360 / (2 * p)
                             })
# capa arriba
for i in range(2*p):
    print(i)
    for j in range(int(q)):
        if i%2==0:
         msp.add_blockref('cond_in', pol2cart(diam/2+dcond*1.5, np.pi/2+ran_ang_mec*pshort-ran_ang_mec*j-i*2*np.pi/(2*p)), dxfattribs={
                'rotation': -ran_ang_mec*j-i*360/(2*p)
            })
        else:
            msp.add_blockref('cond_out', pol2cart(diam / 2 + dcond*1.5, np.pi / 2 +ran_ang_mec*pshort- ran_ang_mec * j - i * 2 * np.pi / (2 * p)),dxfattribs={
                                 'rotation': -ran_ang_mec * j - i * 360 / (2 * p)
                             })

# Cálculo factor acortamiento
def kp1(coil_pitch, pshort):
    return(np.sin((coil_pitch-pshort)/coil_pitch*np.pi/2))
def kp5(coil_pitch, pshort):
    return(np.sin(5*(coil_pitch-pshort)/coil_pitch*np.pi/2))
def kp7(coil_pitch, pshort):
    return(np.sin(7*(coil_pitch-pshort)/coil_pitch*np.pi/2))

# Resultados
print("paso de bobina "+ str(coil_pitch))
print("ángulo de ranura (eléctrico) "+ str(ran_ang))
print("factor de acortamiento 1ra:" + str(kp1(coil_pitch,pshort)))
print("factor de acortamiento 5ta:" + str(kp5(coil_pitch,pshort)))
print("factor de acortamiento 7ma:" + str(kp7(coil_pitch,pshort)))
print("Q: "+str(Q))

doc.saveas('estator.dxf')