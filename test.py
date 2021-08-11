import numpy as np
import tensorflow as tf
import gym

folder_location = 'Finished/4/'
model_name = 'model_128_node-1.h5'

env = gym.make("LunarLander-v2")

# load model
model = tf.keras.models.load_model(folder_location+model_name)

# Run test for 100 cases
r_list = []
steps = []
for i in range(100):
    curr_state = env.reset()
    curr_state = np.reshape(curr_state, (1, 8))
    total_reward = 0
    time_step = 0

    done = False

    while not done:
        curr_output = model.predict(curr_state)
        action = np.argmax(curr_output[0, :])
        env.render()

        new_state, reward, done, info = env.step(action)
        new_state = np.reshape(new_state, (1, 8))
        total_reward += reward

        time_step += 1
        curr_state = new_state

    r_list.append(total_reward)
    steps.append(time_step)
print(np.mean(r_list))
print(np.mean(steps))
np.savetxt(folder_location + 'test_result.txt', r_list)

