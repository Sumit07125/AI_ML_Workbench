import flappy_bird_gymnasium
import gymnasium as gym
import torch
from dqn import DQN
from experience_replay import Reply_Memory

if hasattr(torch.backends, "mpu") and torch.backends.mpu.is_available():
    device = "mpu"  # Check for custom 'mpu' backend support

elif torch.cuda.is_available():
    device = "cuda"  # Check for NVIDIA GPU (CUDA)

elif hasattr(torch, "xpu") and torch.xpu.is_available():
    device = "xpu"   # Check for Intel GPU/accelerator (XPU)

else:
    device = "cpu" # Default to CPU if no accelerator is available


def run(self , is_training = True , render = False):
    env = gym.make("FlappyBird-v0", render_mode="human" if render else None)# is the lesaer light it help to compute distance to the next pipe

    num_states = env.observation_space.shape[0]  # input dimension of the state space
    num_actions = env.action_space.n  # output dimension of the action space

    policy_dqn = DQN(num_states , num_actions).to(device)
    state , _ = env.reset() #observation is nothing but state

    if is_training:
        memory = Reply_Memory(10000) # experience replay buffer with a maximum length of 10,000
    while True:
        # Next action:
        # (feed the observation to your agent here)
        action = env.action_space.sample()

        # Processing:
        next_state, reward, terminated, _, _ = env.step(action)
        
        if is_training:
            memory.append((state, action, new_state, reward, terminated))

        # Checking if the player is still alive
        if terminated:
            break

    env.close()