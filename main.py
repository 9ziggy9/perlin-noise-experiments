import random
import graphics
import math

def interpolate(a0, a1, w):
    return (a1 - a0) * ((w * (w * 6.0 - 15.0) + 10.0) * w * w * w) + a0

def generate_noise(x, y, z=0):
    n000 = random.random() * 2 - 1
    n001 = random.random() * 2 - 1
    n010 = random.random() * 2 - 1
    n011 = random.random() * 2 - 1
    n100 = random.random() * 2 - 1
    n101 = random.random() * 2 - 1
    n110 = random.random() * 2 - 1
    n111 = random.random() * 2 - 1

    ix0 = int(x)
    iy0 = int(y)
    iz0 = int(z)
    dx0 = x - ix0
    dy0 = y - iy0
    dz0 = z - iz0

    ix1 = ix0 + 1
    iy1 = iy0 + 1
    iz1 = iz0 + 1

    x000 = interpolate(n000, n100, dx0)
    x100 = interpolate(n001, n101, dx0)
    x010 = interpolate(n010, n110, dx0)
    x110 = interpolate(n011, n111, dx0)

    iy0 = interpolate(x000, x100, dy0)
    iy1 = interpolate(x010, x110, dy0)

    return interpolate(iy0, iy1, dz0)

def generate_noise_matrix(width, height, octaves=1, persistence=0.5):
    """Generates an n by m matrix of Perlin noise values."""
    noise_matrix = []
    for y in range(height):
        row = []
        for x in range(width):
            scale = 1
            amplitude = 1
            noise_value = 0
            for _ in range(octaves):
                noise_value += generate_noise(x * scale, y * scale) * amplitude
                scale *= 2
                amplitude *= persistence
            row.append(noise_value)
        noise_matrix.append(tuple(row))  # Create a tuple of values for each row
    return noise_matrix

def print_noise_matrix(noise_matrix):
    """Prints a grid representation of a noise matrix."""
    for row in noise_matrix:
        print(" ".join(f"{val:.2f}" for val in row))

def noise_to_color(noise_value):
    # Map noise from [-1, 1] to a color gradient from red to violet
    red = max(0, min(255, int(255 * (noise_value + 1))))  # Red goes from 255 to 0
    violet = max(0, min(255, int(255 * -noise_value + 255)))  # Violet goes from 0 to 255
    blue = 128  # A bit of blue in between

    return graphics.color_rgb(red, 0, violet)  # Leaving green at 0 for simplicity 

def draw_noise_grid(noise_matrix, cell_size, window):
    for y, row in enumerate(noise_matrix):
        for x, noise_value in enumerate(row):
            color = noise_to_color(noise_value)
            top_left = graphics.Point(x * cell_size, y * cell_size)
            bottom_right = graphics.Point((x + 1) * cell_size, (y + 1) * cell_size)
            cell = graphics.Rectangle(top_left, bottom_right)
            cell.setFill(color)
            cell.draw(window)

def regenerate_and_redraw(noise_matrix, cell_size, window):
   noise_matrix = generate_noise_matrix(len(noise_matrix[0]), len(noise_matrix))
   window.delete("all")  # Clear existing content
   draw_noise_grid(noise_matrix, cell_size, window)

def main():
   width, height = 20, 20
   cell_size = 25
   matrix = generate_noise_matrix(width, height)
   window = graphics.GraphWin("Perlin Noise Grid", width * cell_size, height * cell_size)
   draw_noise_grid(matrix, cell_size, window)

   while True:
       key = window.checkKey()
       if key == "Escape":
           break

   window.close()

if __name__ == "__main__":
    main()
