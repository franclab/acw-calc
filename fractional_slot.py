import numpy as np
from fractions import Fraction as frac
import ezdxf
q=3.5

# acortamiento, posibles ratios
def short_pitching(q):
    '''Da relaciones posibles de acortamiento y calcula sus coeficientes kp para fundamental, 5ta y 7ma'''
    y_q = 3 * q  # paso polar en ranuras
    for i in range(3):
        acort=(int(y_q)-i)/y_q
        print(f'{int(y_q)-i}/{round(y_q,1)} -> kp1={kp(acort)[0]}, kp5={kp(acort)[1]}, kp7={kp(acort)[2]}')

def kp(acort):
    kp1=np.sin(acort*np.pi/2)
    kp5 = np.sin(5*acort * np.pi / 2)
    kp7 = np.sin(7*acort * np.pi / 2)
    return(round(kp1,3),round(kp5,3), round(kp7,3))

def frac_slot(q):
    '''Calcula los valores relacionados a q'''
    N, beta= (frac(q).limit_denominator().numerator,frac(q).limit_denominator().denominator)
    a=int(q)
    b=int((q-a)*beta)
    P=1 #con 2.75 P=3 hay que corregir eso
    d=(3*N*P+1)/beta
    while d.is_integer() == False:
        d=(3*N*P+1)/beta
        P+=1
    ang_m=(np.pi/3)/N
    ang_s=(np.pi/3)/q
    return((N, beta, a ,b, d, ang_s, ang_m))

def ran_series(N,d):
    '''Genera la serie de una fase del grupo recurrente'''
    series=[]
    for i in range(int(3*N)):
        new_value = 1+i*d
        while new_value > 3*N:
            j = 1
            new_value = new_value - 3*N*j
            j += 1
        series.append(new_value)
    return(series)

N=frac_slot(q)[0]
beta=frac_slot(q)[1]
a=frac_slot(q)[2]
b=frac_slot(q)[3]
d=frac_slot(q)[4]
ang_s=frac_slot(q)[5]
ang_m=frac_slot(q)[6]
series=ran_series(N, d)


# coord polares a cartesianas
def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

def slot_star(ang_m, series):
    '''Dibuja la estrella de ranuras de una fase del grupo recurrente'''
    # Crear nuevo dibujo
    doc = ezdxf.new('R12')
    msp = doc.modelspace()
    for i in range(len(series)):
        msp.add_line((0,0),pol2cart(5,-ang_m*i+np.pi))
        msp.add_text(f'{int(series[i])}',dxfattribs={'height':0.2}).set_pos(pol2cart(5.5,-ang_m*i+np.pi),align='MIDDLE_CENTER')
    for i in range(3):
        msp.add_arc((0,0),radius=6,start_angle=ang_m*180/np.pi*(N*i+1),end_angle=ang_m*180/np.pi*N*(i+1),is_counter_clockwise=True)
    #msp.add_text(f'angulo campo magnetico: {round((ang_m)*180/np.pi, 3)} grados electricos', dxfattribs={'height': 0.2}).set_pos((-5,-.5))
    msp.add_text('I', dxfattribs={'height': 0.3}).set_pos(pol2cart(6.5,np.pi*5/6))
    msp.add_text('II', dxfattribs={'height': 0.3}).set_pos(pol2cart(6.5, np.pi / 2))
    msp.add_text('III', dxfattribs={'height': 0.3}).set_pos(pol2cart(6.5, np.pi / 6))
    msp.add_text(f'q : {q}', dxfattribs={'height': 0.2}).set_pos((-5,-1))
    msp.add_text(f'N : {N}', dxfattribs={'height': 0.2}).set_pos((-5,-1.5))

    doc.saveas("slot_star.dxf")

slot_star(ang_m, series)
print(f'q={q}')
print("")
print(f'Grupo recurrente (unidad) en beta={beta} polos formado por:')
print(f'-> {beta-b} grupos con {a} bobinas')
print(f'-> {b} grupos con {a+1} bobinas')
print("")
print(f'nro polos/{beta} caminos paralelos posibles')
short_pitching(q)

# Bibliografía:
# Liwschitz AC-Electric Machinery, Appendix I: Fractional-Slot windings