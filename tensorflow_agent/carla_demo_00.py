import carla
import random
import time

actor_list = []

try:
    # Connect to the server
    client = carla.Client('localhost', 2000)
    # Set the time out of the client
    client.set_timeout(5.0)

    # # Get the world
    world = client.load_world('Town05')
    # world = client.get_world()
    # Get the blueprint library
    blueprint_library = world.get_blueprint_library()
    
    # Spawn a vehicle use model3
    v_bp = blueprint_library.filter("model3")[0]
    # Set spawn point (random)
    spawn_point = random.choice(world.get_map().get_spawn_points())
    vehicle = world.spawn_actor(v_bp, spawn_point)
    # Append the actor to the list
    actor_list.append(vehicle)
    # Set the vehicle control
    vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=0.0))
    time.sleep(30)
finally:
    for actor in actor_list:
        actor.destroy()
    print('All actors destroyed')