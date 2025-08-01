# Changelog

2025/08/01

The docker dive command used in the lecture:

```bash
# docker in docker command
docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive:latest <image_name:tag>
```

Has been replaced in the challenges with the `apt` package of the same name that is more intuitive and less prone to copy-pasting errors.

Install with:

```bash
DIVE_VERSION=$(curl -sL "https://api.github.com/repos/wagoodman/dive/releases/latest" | grep '"tag_name":' | sed -E 's/.*"v([^"]+)".*/\1/')
curl -fOL "https://github.com/wagoodman/dive/releases/download/v${DIVE_VERSION}/dive_${DIVE_VERSION}_linux_amd64.deb"
sudo apt install ./dive_${DIVE_VERSION}_linux_amd64.deb
```

Check install with:

```bash
which dive

# should return something similar to:
# /usr/bin/dive
```

Use with:

```bash
dive <your_image_name>

# or

dive <your_image_name>:<image_tag>
```
