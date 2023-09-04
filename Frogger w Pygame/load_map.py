import pygame
import random

pygame.init()

clock = pygame.time.Clock()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

player_image = pygame.image.load("images/frog_image.png")
player_image = pygame.transform.scale(player_image, (25, 25))

car_image = pygame.image.load("images/clipart172344.png")
car_image = pygame.transform.scale(car_image, (25, 25))

# Get the rect for the image
player_rect = player_image.get_rect()
player_rect.x = 400
player_rect.y = 500

grid_x = screen_width / 10
grid_y = screen_height / 10
g = (0, 255, 0)
b = (0, 0, 0)

# Load vehicle images and scale them (you can replace these with your own images)
vehicle_image_left = pygame.image.load("images\clipart172344.png")
vehicle_image_left = pygame.transform.scale(vehicle_image_left, (25, 25))
vehicle_image_left = pygame.transform.rotate(vehicle_image_left, 1800)

vehicle_image_right = pygame.image.load("images\clipart172344.png")
vehicle_image_right = pygame.transform.scale(vehicle_image_right, (25, 25))
vehicle_hit = False

movement_jump = 2


class Player:
    def __init__(self, x, y, width, height):
        # Load and scale the player image
        self.image = pygame.image.load("images/frog_image.png")
        self.image = pygame.transform.scale(self.image, (width, height))

        self.player_image_up = player_image
        self.player_image_down = pygame.transform.rotate(player_image, 180)
        self.player_image_left = pygame.transform.rotate(player_image, 90)
        self.player_image_right = pygame.transform.rotate(player_image, -90)
        self.player_can_move = True
        # Create a rect for the player
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # Player attributes
        self.velocity = movement_jump  # Speed at which the player moves
        self.player_pos = 0  # Initialize player position attribute
        self.dist_traveled = 0
        self.counter = 0
        self.total_time = 0 # Total time
        self.time_elapsed = pygame.time.get_ticks() # Time elapsed
        self.scrolling_time = 0 # Scrolling time
        

    def player_rotate(self, direction):
        if direction == 0:
            self.image = self.player_image_up
        if direction == 1:
            self.image = self.player_image_right
        if direction == 2:
            self.image = self.player_image_left
        if direction == 3:
            self.image = self.player_image_down

    def move(self):
        # Handle player movement
        if self.player_can_move:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and self.player_pos == 0:
                self.rect.y -= self.velocity
                self.dist_traveled += 1
            elif keys[pygame.K_UP] and self.player_pos != 0:
                self.player_pos = 0
                self.player_rotate(self.player_pos)

            if keys[pygame.K_DOWN] and self.player_pos == 3:
                self.rect.y += self.velocity
            elif keys[pygame.K_DOWN] and self.player_pos != 3:
                self.player_pos = 3
                self.player_rotate(self.player_pos)

            if keys[pygame.K_LEFT] and self.player_pos == 2:
                self.rect.x -= (self.velocity * 2)
            elif keys[pygame.K_LEFT] and self.player_pos != 2:
                self.player_pos = 2
                self.player_rotate(self.player_pos)

            if keys[pygame.K_RIGHT] and self.player_pos == 1:
                self.rect.x += (self.velocity * 2)
            elif keys[pygame.K_RIGHT] and self.player_pos != 1:
                self.player_pos = 1
                self.player_rotate(self.player_pos)

            if self.rect.x <= 0:
                self.rect.x += 25
            if self.rect.x >= 775:
                self.rect.x -= 25
            if self.rect.y <= 200:
                self.rect.y += 1
            if self.rect.y >= 575:
                self.game_over()
            if vehicle_hit == True:
                self.game_over()  

    def draw(self, screen):
        # Draw the player on the screen
        screen.blit(self.image, self.rect.topleft)
    def game_over(self):
        if self.rect.y >= 575 or vehicle_hit == True:
            if self.counter == 0:
                self.total_time = pygame.time.get_ticks() - self.time_elapsed - self.scrolling_time
                self.counter += 1
                # Define text attributes (font, size, color)
            total_to_secs = round(self.total_time / 1000)
            font = pygame.font.Font(None, 50)  # None means to use the default system font
            text_color = (255, 255, 255)  # White color
            text = font.render("Game Over :(", True, text_color)
            text_rect = text.get_rect()
            text_rect.center = (screen_width // 2, screen_height // 2)
            minutes = 0
            if total_to_secs >= 60:
                total_to_secs -= 60
                minutes += 1  
            text2 = font.render("You Survived " + str(minutes) + " Minutes " + str(total_to_secs) + " Seconds", True, text_color)
            text2_rect = text2.get_rect()
            text2_rect.center = (screen_width // 2, (screen_height // 2) + 50)
            # Calculate the total background size
            background_width = max(text_rect.width, text2_rect.width) + 20  # Add some padding
            background_height = text_rect.height + text2_rect.height + 50  # Add some padding
            
            # Create a background surface with a black background
            background = pygame.Surface((background_width, background_height))
            background.fill((0, 0, 0))
            # Draw the text onto the screen
            background.blit(text, text_rect)
            background.blit(text2, text2_rect)
            background_x = (screen_width - background_width) // 2
            background_y = (screen_height - text2_rect.height) // 2
        
            # Draw the background onto the screen
            screen.blit(background, (background_x, background_y - 20))

            screen.blit(text, text_rect)
            screen.blit(text2, text2_rect) 

        
            return 1
        else:
            return 0

class Road:
    def __init__(self, width, height, color, x, y):
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        # Draw a yellow dashed line on the road
        dash_width = 10  
        dash_gap = 10    
        dash_color = (255, 255, 0)  
        for x in range(self.rect.left, self.rect.right, dash_width + dash_gap):
            pygame.draw.line(screen, dash_color, (x, self.rect.centery), (x + dash_width, self.rect.centery), 5)

    def random_y():
        return random.randint(0, 75)

class Vehicle:
    def __init__(self, x, y, width, height, speed, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def move(self):
        # Move the vehicle horizontally (you can adjust this logic)
        self.rect.x += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)




start_time = pygame.time.get_ticks()


# Calculate the new vehicle speed based on time_elapsed
initial_speed = 1.25



# Create a player instance
player = Player(400, 500, 25, 25)

#Control the Scrolling
scrolling = False  # Flag to track if scrolling is enabled
scroll_threshold = 450  # Y-coordinate threshold for scrolling
scroll_speed = .1
pushback_speed = .5

roads = []
vehicles = []
running = True
new_road = None
car_speed_left = -1.25
car_speed_right = 1.25
time_threshold = 5000
vehicle_frequency = 7
limit_vehicles = 45
scroll_counter = 0
while running:
    current_time = pygame.time.get_ticks()
    time_elapsed = current_time - start_time


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #Trigger Losing Screen
    if player.game_over() == 1:
        scrolling = False
        player.player_can_move = False

        pygame.display.flip()

        # Handle end of game

    # Check if the player has crossed the scrolling threshold
    if player.rect.y < scroll_threshold and not scrolling:
        scrolling = True
    if scrolling:
        if scroll_counter == 0:
            player.scrolling_time = pygame.time.get_ticks()
            scroll_counter += 1
        player.rect.y += (pushback_speed)
        for road in roads:
            road.rect.y += (pushback_speed)
        for vehicle in vehicles:
            vehicle.rect.y += (pushback_speed)
        # Move and draw vehicles
        for vehicle in vehicles:
            vehicle.move()
            vehicle.draw(screen)
        # Adjust other game elements as needed
        speed_increase = 1.1

        if random.randint(0, 100) < 5:
                # Determine whether to create a vehicle facing left or right based on road position
            for road in roads:
                if len(vehicles) < limit_vehicles:
                    if random.randint(0, 100) < vehicle_frequency:
                        # Create a vehicle facing left
                        vehicle = Vehicle(screen_width, road.rect.y, 25, 25, car_speed_left, vehicle_image_left)
                        vehicles.append(vehicle)
                    if random.randint(0, 100) < vehicle_frequency:
                        # Create a vehicle facing right
                        vehicle = Vehicle(4, road.rect.y + 35, 25, 25, car_speed_right, vehicle_image_right)
                        vehicles.append(vehicle)
        if time_elapsed > time_threshold and car_speed_left > -10 and car_speed_right < 10:
            car_speed_left = car_speed_left * speed_increase
            car_speed_right = car_speed_right * speed_increase
            time_threshold += 50000
            vehicle_frequency += 5
            limit_vehicles += 5


    # Clear the screen
    screen.fill((0, 255, 0))
    # Draw the roads
    # Generate new roads at random intervals
    random_number = random.randint(0, 75)
    road_limit = 5

    if random_number < 3 and len(roads) < road_limit:
        bar_y = Road.random_y()
        new_road = Road(800, 60, (50, 50, 50), 0, bar_y)
        vehicle_collides = any(vehicle.rect.colliderect(road.rect) for vehicle in vehicles)
        if random.randint(0, 15) < vehicle_frequency and scrolling and new_road.rect.y < 150 and not vehicle_collides:
            # Create a vehicle facing left
            vehicle = Vehicle(random.randint(100, 400), road.rect.y, 25, 25, car_speed_left, vehicle_image_left)
            vehicles.append(vehicle)
        if random.randint(0, 15) < vehicle_frequency and scrolling and new_road.rect.y < 150 and not vehicle_collides:
            # Create a vehicle facing right
            vehicle = Vehicle(random.randint(100, 400), road.rect.y + 35, 25, 25, car_speed_right, vehicle_image_right)
            vehicles.append(vehicle)
        
        # Check for collisions with existing roads
        collision = False
        for existing_road in roads:
            if new_road.rect.colliderect(existing_road.rect):
                collision = True
                break
        car_collision = False
        for car in vehicles:
            if car.rect.colliderect(car.rect):
                car_collision = True
                break

        for car in vehicles:
            if car.rect.colliderect(player.rect):
                vehicle_hit = True
                player.game_over()
                break
        # If there's a collision, adjust the new road's position
        if collision:
            continue
        roads.append(new_road)
        # If there's a collision, adjust the new cars position
        if car_collision:
            continue        

    for road in roads:
        road.draw(screen)
    for vehicle in vehicles:
        vehicle.draw(screen)
    # Check for collisions with existing cars

    roads = [road for road in roads if road.rect.y < screen_height]
    vehicles = [vehicle for vehicle in vehicles if -15 < vehicle.rect.x < screen_width + 25 and 0 < vehicle.rect.y < screen_height - 10]

    # Draw the semi-transparent black line
    red_line = pygame.Surface((screen_width, 10), pygame.SRCALPHA)
    pygame.draw.rect(red_line, (255, 0, 0, 128), (0, 0, screen_width, 25))
    screen.blit(red_line, (0, 187))
    # Handle player movement
    player.move()
    # Draw the player
    player.draw(screen)
    # Update the display
    player.game_over()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
