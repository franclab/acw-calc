import func
from datetime import datetime

def main():
    q=2.5
    polos=4
    #q=func.get_data('datain.csv')
    current_time = datetime.now().strftime("%d-%m-%y_%H:%M:%S")

    N, beta, a, b, d, ang_s, ang_m = func.frac_slot(q)

    series = func.ran_series(N, d)
    # Cálculo relación acortamiento
    acort_list = func.short_pitching(q)
    acort = min(acort_list, key=lambda x:abs(x-5/6)) #selecciona el acort más cercano a 0.83
    tabla_fact = func.factores(N, acort)
    func.rep_gen(q, polos, N, current_time, a, b, beta, series, acort, tabla_fact)
    #func.slot_star(q, N, ang_m, series)
    print(N)

if __name__ == "__main__":
    main()
