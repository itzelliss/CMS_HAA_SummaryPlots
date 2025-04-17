#create tan beta files

#write 175 times each value in  the same txt file (overwrite each time)
for tan in [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5]:
    with open(f'tan_beta.txt', 'a') as f:
        for i in range(175):
            f.write(f'{tan}\n')

