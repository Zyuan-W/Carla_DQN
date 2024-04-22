import random
import time
import glob
import os
import sys

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


def main():
    argparser = argparse.ArgumentParser(
    description=__doc__)
    argparser.add_argument(
        '--host',
        metavar='H',
        default='127.0.0.1',
        help='IP of the host server (default: 127.0.0.1)')
    argparser.add_argument(
        '-p', '--port',
        metavar='P',
        default=2000,
        type=int,
        help='TCP port to listen to (default: 2000)')
    argparser.add_argument(
        '--tm-port',
        metavar='P',
        default=8000,
        type=int,
        help='Port to communicate with TM (default: 8000)')

    args = argparser.parse_args()

    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)





    actor_list = []

    try:
        # Connect to the server
        client = carla.Client(args.host, args.port)
        # Set the time out of the client
        client.set_timeout(120.0)

        # # Get the world
        # world = client.load_world('Town05')
        world = client.get_world()
        print('world loaded')
        # Get the blueprint library
        blueprint_library = world.get_blueprint_library()

        # Spawn a vehicle use model3
        v_bp = blueprint_library.filter("model3")[0]
        # Set spawn point (random)
        spawn_point = random.choice(world.get_map().get_spawn_points())
        vehicle = world.spawn_actor(v_bp, spawn_point)
        print('vehicle generated')
        # Append the actor to the list
        actor_list.append(vehicle)
        # Set the vehicle control
        vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=0.0))
        time.sleep(5)
    finally:
        for actor in actor_list:
            actor.destroy()
        print('All actors destroyed')

if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('\ndone.')