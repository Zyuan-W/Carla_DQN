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

        # Set up the sensors
        # Set up the RGB camera

        # Initialize Pygame
        pygame.init()
        display_width = 800
        display_height = 600
        game_display = pygame.display.set_mode((display_width, display_height))
        pygame.display.set_caption('CARLA POV Camera')

        # camera_bp = blueprint_library.find('sensor.camera.rgb')
        # camera_bp.set_attribute('image_size_x', str(display_width))
        # camera_bp.set_attribute('image_size_y', str(display_height))
        # camera_bp.set_attribute('fov', f"110")

        # camera_transform = carla.Transform(carla.Location(x=2.5, z=0.7), carla.Rotation(pitch=-10))

        # camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)
        # print('Camera spawned')
        # actor_list.append(camera)

        # # def process_img(image):
        # #     i = np.array(image.raw_data)
        # #     i2 = i.reshape((600, 800, 4))
        # #     i3 = i2[:, :, :3]
        # #     cv2.imshow("", i3)
        # #     cv2.waitKey(1)
        # #     return i3

        # def process_img(image):
        #     array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
        #     array = np.reshape(array, (image.height, image.width, 4))
        #     array = array[:, :, :3]  # Drop the alpha channel
        #     surface = pygame.surfarray.make_surface(array.swapaxes(0, 1))
        #     return surface
        

        # # Listen to the camera
        # camera.listen(lambda image: game_display.blit(process_img(image), (0, 0)))
        # # camera.listen(lambda image: process_img(image))
        # print('Listening to the camera')

        # Lidar sensor setup
        lidar_bp = blueprint_library.find('sensor.lidar.ray_cast')
        lidar_bp.set_attribute('range', '30')
        lidar_bp.set_attribute('rotation_frequency', '10')
        lidar_bp.set_attribute('points_per_second', '100000')
        lidar_bp.set_attribute('channels', '32')
        # lidar_bp.set_attribute('upper_fov', '10')
        # lidar_bp.set_attribute('lower_fov', '-30')
        lidar_transform = carla.Transform(carla.Location(z=2.5))
        lidar_sensor = world.spawn_actor(lidar_bp, lidar_transform, attach_to=vehicle)
        print('Lidar spawned')
        actor_list.append(lidar_sensor)

        def process_lidar(data):
            """Process LiDAR data and display it using Pygame."""
            lidar_data = np.frombuffer(data.raw_data, dtype=np.dtype('float32'))
            lidar_data = np.reshape(lidar_data, (int(lidar_data.shape[0] / 4), 4))
            # Each point is (X, Y, Z, intensity)
            lidar_points = lidar_data[:, :2]  # We use X, Y for 2D display
            lidar_points = np.copy(lidar_points)  # Make a copy of the array to avoid read-only issues
            lidar_points *= 5.0  # Scale points for better visualization
            lidar_points += (400, 300)  # Move points to screen center
            lidar_points = np.fabs(lidar_points)  # Absolute values for display
            lidar_points = lidar_points.astype(np.int32)
            lidar_points = np.clip(lidar_points, 0, 800)  # Avoid drawing out of bounds
            game_display.fill((0, 0, 0))  # Clear the screen
            for point in lidar_points:
                pygame.draw.circle(game_display, (255, 255, 255), point, 2)

        lidar_sensor.listen(lambda data: process_lidar(data))



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
