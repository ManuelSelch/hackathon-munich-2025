from openpi.training import config as _config
from openpi.policies import policy_config
from openpi.shared import download

# load policy
config = _config.get_config("pi05_droid")
checkpoint_dir = download.maybe_download("gs://openpi-assets/checkpoints/pi05_droid")
policy = policy_config.create_trained_policy(config, checkpoint_dir)

# run inference^
example = {
    "observation/images/rgb_static": {},
    
    "prompt": "pick up the fork"
}
action_chunk = policy.infer(example)["actions"]

print(action_chunk)

# todo: send action to robot over grpc