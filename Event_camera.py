import random
import time
import glob
import os
import sys
import cv2
import numpy as np

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass


import argparse
import logging
import carla
import pygame


def main():


    actor_list = []

    try:
        client = carla.Client('localhost', 2000)

        client.set_timeout(10.0)

        world = client.load_world('Town01')
        print('World loaded')

        # Get the blueprint library
        blueprint_library = world.get_blueprint_library()
        v_bp = blueprint_library.filter("model3")[0]

        # Get the spawn points
        spawn_point = random.choice(world.get_map().get_spawn_points())
        vehicle = world.spawn_actor(v_bp, spawn_point)
        print('Vehicle spawned')
        actor_list.append(vehicle)
        # vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=0.0))

        # Set up the DVS camera
        dvs_bp = blueprint_library.find('sensor.camera.dvs')
        dvs_bp.set_attribute('image_size_x', '800')
        dvs_bp.set_attribute('image_size_y', '600')
        dvs_camera = world.spawn_actor(dvs_bp, carla.Transform(carla.Location(x=2.5, z=0.7)), attach_to=vehicle)
        actor_list.append(dvs_camera)

        # Initialize Pygame
        pygame.init()
        display = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("CARLA Event Camera (DVS) Display")
        
        def process_dvs_image(image):
            # Create a blank surface to draw events
            surface = pygame.Surface((image.width, image.height))
            surface.fill((0, 0, 0))  # Black background
            
            # Decode each event from the image
            for i in range(0, len(image.raw_data), 4):
                x = image.raw_data[i]
                y = image.raw_data[i + 1]
                # Polarity is either 0 or 1, you could color them differently
                polarity = image.raw_data[i + 2]
                color = (255, 255, 255) if polarity == 1 else (100, 100, 100)
                # Draw each event as a small rectangle or point
                surface.set_at((x, y), color)
                
            # Display in Pygame
            display.blit(surface, (0, 0))
            pygame.display.flip()

        dvs_camera.listen(lambda image: process_dvs_image(image))



        while True:
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

        time.sleep(30)
    finally:
        for actor in actor_list:
            actor.destroy()
        print("All cleaned up!")

if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('\ndone.')
