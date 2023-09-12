# Install Automatic1111 Web UI on your Network Volume

1. [Create a RunPod Account](https://runpod.io?ref=2xxro4sy).
2. Create a [RunPod Network Volume](https://www.runpod.io/console/user/storage).
3. Attach the Network Volume to a Secure Cloud [GPU pod](https://www.runpod.io/console/gpu-secure-cloud).
4. Select a light-weight template such as RunPod Pytorch.
5. Deploy the GPU Cloud pod.
6. Once the pod is up, open a Terminal and install the required
   dependencies. This can either be done by using the installation
   script, or manually.

## Automatic Installation Script

You can run this automatic installation script which will
automatically install all of the dependencies that get installed
manually below, and then you don't need to follow any of the
manual instructions.

```bash
wget https://raw.githubusercontent.com/ashleykleynhans/runpod-worker-a1111/main/scripts/install.sh
chmod +x install.sh
./install.sh
```

## Manual Installation

You only need to complete the steps below if you did not run the
automatic installation script above.

1. Install the Automatic1111 WebUI and ControlNet extension:

```bash
# Clone the repo
cd /workspace
git clone --depth=1 https://github.com/AUTOMATIC1111/stable-diffusion-webui.git

# Upgrade Python
apt update
apt -y upgrade

# Ensure Python version is 3.10.12
python3 -V

# Create and activate venv
cd stable-diffusion-webui
python -m venv /workspace/venv
source /workspace/venv/bin/activate

# Install Torch and xformers
pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install --no-cache-dir xformers

# Install A1111 Web UI
wget https://raw.githubusercontent.com/ashleykleynhans/runpod-worker-a1111/main/install-automatic.py
python -m install-automatic --skip-torch-cuda-test

# Clone the ControlNet Extension
git clone https://github.com/Mikubill/sd-webui-controlnet.git extensions/sd-webui-controlnet

# Install dependencies for ControlNet
cd extensions/sd-webui-controlnet
pip install -r requirements.txt

# Clone Segment-Anything Extension
git clone https://github.com/continue-revolution/sd-webui-segment-anything

# Install dependencies for Segment-Anything
cd /workspace/stable-diffusion-webui/extensions/sd-webui-segment-anything
pip install -r requirements.txt

```

2. Install the Serverless dependencies:

```bash
cd /workspace/stable-diffusion-webui
pip3 install huggingface_hub runpod>=0.10.0
```

3. Download some models, for example `Deliberate v2`:

```bash
cd /workspace/stable-diffusion-webui/models/Stable-diffusion
wget -O deliberate_v2.safetensors https://civitai.com/api/download/models/15236
```

4. Download ControlNet models, for example `canny`:

```bash
mkdir -p /workspace/stable-diffusion-webui/models/ControlNet
cd /workspace/stable-diffusion-webui/models/ControlNet
wget https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_canny.pth

```

5. Download Segmentation models, for example `sam_vit_h`;

```bash
cd /workspace/stable-diffusion-webui/extensions/sd-webui-segment-anything/models/sam
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth


```

1. Create logs directory:

```bash
mkdir -p /workspace/logs
```

1. Install config files:

```bash
cd /workspace/stable-diffusion-webui
rm webui-user.sh config.json ui-config.json
wget https://raw.githubusercontent.com/ashleykleynhans/runpod-worker-a1111/main/webui-user.sh
wget https://raw.githubusercontent.com/ashleykleynhans/runpod-worker-a1111/main/config.json
wget https://raw.githubusercontent.com/ashleykleynhans/runpod-worker-a1111/main/ui-config.json
```

1. Run the Web UI:

```bash
deactivate
export HF_HOME="/workspace"
cd /workspace/stable-diffusion-webui
./webui.sh -f
```

1. Wait for the Web UI to start up, and download the models. You shoud
   see something like this when it is ready:

```
Model loaded in 16.9s (calculate hash: 8.0s, load weights from disk: 0.4s, create model: 2.1s, apply weights to model: 2.6s, apply half(): 2.6s, move model to device: 0.7s, calculate empty prompt: 0.3s).
```

1. Press Ctrl-C to exit, and then you can terminate the pod.
