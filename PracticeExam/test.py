def process_temperatures(temps, baseline=98.6):
    variances = []
    labels = []
    for i, temp in enumerate(temps):
        variances.append(round(temp - baseline, 2))
        labels.append(f'Temperature {i+1}')
    return list(zip(labels, temps, variances))


print(process_temperatures([99, 101, 103, 97.5, 69]))