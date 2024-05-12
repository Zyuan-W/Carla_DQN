# How to Run


## main.py
Run this file if you want to evaluate the performance of your agent
```
env = SimEnv(visuals=False)
```


```
model.load('weights/model_ep_4400')
```

This loads a trained/pre-trained model. The program will not run unless it can load this model.
The 4400 indicates that this model was trained for 4400 episodes.

For example, if you train your own model for 200 episodes you will see the following files in the weights folder

`model_ep_200_optimizer` and `model_ep_200_Q`

You can then load the model as `model.load('weights/model_ep_200')`. 

## train.py
This is for training the model. The model only starts learning after a certain number of episodes, and it can take from 8-10 hours (at least on my setup) before we see signs of learning. I will now describe a few variables you can set to configure your training process. You can modify them yourself in `config.py`.

`target_speed` --> Speed you want the car to move at in km/h

`max_iter` --> Maximum number of steps before starting a new episode

`start_buffer` --> Number of episodes to run before starting training

`train_freq` --> How often to train (set to 1 to train every step, 2 to train every 2 steps etc)

`save_freq`: --> Frequency of saving our model

`start_ep` --> Which episode should we start on (just a counter which you can update if program crushes while training for example)
