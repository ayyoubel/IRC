import streamlit as stcreate_symbol_grid
from PIL import Image, ImageDraw
from io import BytesIO




import heapq
from PIL import Image

def heuristic(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

def create_symbol_grid(image_path):
    """Creates a grid of '#' or ' ' symbols based on black/green pixels and their surroundings."""

    image = Image.open(image_path)
    image_rgb = image.convert('RGB')
    width, height = image_rgb.size

    symbol_grid = []
    for y in range(0, height, 12):
        row = []
        for x in range(0, width, 12):
            symbol = ' '  # Assume empty space by default

            # Check current pixel and surrounding pixels for black or green
            for dy in range(-1, 1):
                for dx in range(-1, 1):
                    if 0 <= x + dx < width and 0 <= y + dy < height:
                        pixel = image_rgb.getpixel((x + dx, y + dy))
                        if pixel == (0, 0, 0):
                            symbol = '#'  # Found black or green, set symbol to '#'
                            break  # No need to check further surrounding pixels
                        if pixel == (0, 255, 0):
                            symbol = ' '  # Found black or green, set symbol to '#'
                            break  # No need to check further surrounding pixels

            row.append(symbol)
        symbol_grid.append(row)

    return symbol_grid

def a_star(maze):
    def get_neighbors(node):
        row, col = node
        neighbors = []

        if row > 0 and maze[row - 1][col] != '#':
            neighbors.append((row - 1, col))
        if row < len(maze) - 1 and maze[row + 1][col] != '#':
            neighbors.append((row + 1, col))
        if col > 0 and maze[row][col - 1] != '#':
            neighbors.append((row, col - 1))
        if col < len(maze[0]) - 1 and maze[row][col + 1] != '#':
            neighbors.append((row, col + 1))

        return neighbors

    start = find_start(maze)
    end = find_end(maze)

    heap = [(0, start)]
    visited = set()
    came_from = {start: (0, None)}

    while heap:
        current_cost, current_node = heapq.heappop(heap)

        if current_node == end:
            path = reconstruct_path(came_from, start, end)
            return path

        if current_node in visited:
            continue

        visited.add(current_node)

        for neighbor in get_neighbors(current_node):
            new_cost = current_cost + 1
            if neighbor not in visited and (neighbor not in came_from or new_cost < came_from[neighbor][0]):
                heapq.heappush(heap, (new_cost + heuristic(neighbor, end), neighbor))
                came_from[neighbor] = (new_cost, current_node)

    return None  # No path found

def find_start(maze):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 'S':
                return (i, j)

def find_end(maze):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 'E':
                return (i, j)

def reconstruct_path(came_from, start, end):
    path = []
    current_node = end
    while current_node != start:
        path.append(current_node)
        current_node = came_from[current_node][1]
    path.append(start)
    path.reverse()
    return path

def print_solution(maze, path):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if (i, j) in path:
                print('X', end=' ')
            else:
                print(maze[i][j], end=' ')
        print()

def modify_list(symbol_grid):
    """Modifies a list of lists by adding '#' at the end of each sublist and a full list of '#' at the end."""

    # Add '#' to the end of each existing sublist
    for row in symbol_grid:
        row.append('#')

    # Add a list full of '#' at the end
    symbol_grid.append(['#'] * len(symbol_grid[0]))
    symbol_grid[0] = ['#'] * len(symbol_grid[0])# Ensure the new list has the same width as others
    for i in range (len(symbol_grid)) : symbol_grid[i][0] = "#"
    symbol_grid[1][1] = 'E'
    symbol_grid[-2][-2] = 'S'

    return symbol_grid


def draw_line_between_points(image, point1, point2, line_color='black', line_width=1):
    draw = ImageDraw.Draw(image)
    draw.line([point1, point2], fill=line_color, width=line_width)
    del draw 
    
    
    
def create_white_image(width, height):
    return Image.new('RGB', (width, height), color='white')







################################################




def process_image(input_image):
    # Open the uploaded image
    # Replace with your image path
    symbol_grid = create_symbol_grid(input_image)

    # Example usage (assuming you have the `symbol_grid` from a previous code):
    modified_grid = modify_list(symbol_grid)        

    # Example maze
    # Exemple de labyrinthe
    maze5 = modified_grid

    shortest_path5 = a_star(maze5)

    if shortest_path5:
        #print("Le chemin le plus court est :", shortest_path5)
        print_solution(maze5, shortest_path5)
    else:
        print("Aucun chemin trouvé.")
        
    to_reality = []
    for i in range(len(shortest_path5)):
        to_reality.append((shortest_path5[i][1]*12,shortest_path5[i][0]*12))
        

    existing_image = create_white_image((len(symbol_grid[0])-1)*12, (len(symbol_grid)-1)*12) #her

    for i in range(len(to_reality)-1):
        point1 = to_reality[i]
        point2 = to_reality[i+1]
        draw_line_between_points(existing_image, point1, point2)



    return existing_image

def main():
    st.title("Maze solver app eminers")

    # File upload
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])

    # Input for file name
    file_name = st.text_input("Enter file name (without extension):", "eminers X")

    if uploaded_file is not None:
        # Display the uploaded image
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

        # Process the image
        processed_image = process_image(uploaded_file)

        # Display the processed image
        st.image(processed_image, caption="Processed Image", use_column_width=True)

        # Download button
        if st.button("Download Processed Image"):
            # Convert the processed image to bytes
            processed_image_bytes = BytesIO()
            processed_image.save(processed_image_bytes, format="PNG")

            # Download the processed image with the specified file name
            st.download_button(
                label="Download",
                data=processed_image_bytes.getvalue(),
                file_name=f"{file_name}.png",
                mime="image/png",
            )

if __name__ == "__main__":
    main()
