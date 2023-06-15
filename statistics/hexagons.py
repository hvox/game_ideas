from math import sqrt

min_error = 1
for height in range(2, 16 + 1):
    width = round(height * sqrt(3) / 2 / 2 - 0.5) * 2 + 1
    error = abs(width-1 - (height - 1) * sqrt(3) / 2)
    print(f"w={width:<2} h={height:<2} error={error:0.3f}" + " !" * (error < min_error))
    min_error = min(min_error, error)
