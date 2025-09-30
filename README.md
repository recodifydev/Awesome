# Awesome

## Computer Use Tool

### How It Works

The computer use tool operates in a continuous loop to automate computer interactions:

1. **Action Generation**: The tool sends computer actions like:
   - Mouse clicks (click x,y coordinates)
   - Keyboard input (type text)
   - Scrolling
   - Other interface interactions

2. **Execution**: These actions are executed in a computer or browser environment

3. **Feedback Loop**: 
   - The environment returns screenshots after each action
   - The model analyzes these screenshots to understand the current state
   - Based on this understanding, it determines the next appropriate actions

### Environment Setup

Before integrating the computer use tool, you need to prepare your environment:

1. **Sandboxed Environment**
   - Set up a dedicated sandboxed environment for safety
   - This isolates the tool's operations from your main system
   - Helps prevent unintended interactions with sensitive applications

2. **Screenshot Capabilities**
   - Ensure your environment can capture and process screenshots
   - Set up proper screen resolution and color depth
   - Configure screenshot frequency and storage

3. **Action Execution**
   - Set up necessary permissions for mouse and keyboard control
   - Configure any required accessibility features
   - Test basic input operations in the sandboxed environment

4. **Security Considerations**
   - Limit the tool's access to specific applications only
   - Configure network access restrictions if needed
   - Set up logging for all automated actions

### Quick Start Guide

For a minimal setup, you can use browser automation frameworks like Playwright or Selenium. Here's how to get started:

#### Security Recommendations
- Use a sandboxed environment
- Set empty environment variables to avoid exposing host system data
- Disable browser extensions and file system access
- Use appropriate security flags

#### Installation

**Python Setup**
```bash
pip install playwright
```

**JavaScript Setup**
```bash
npm i playwright
npx playwright install
```

#### Example Implementation

**Python Example**
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        chromium_sandbox=True,
        env={},
        args=[
            "--disable-extensions",
            "--disable-file-system"
        ]
    )
    page = browser.new_page()
    page.set_viewport_size({"width": 1024, "height": 768})
    page.goto("https://bing.com")

    page.wait_for_timeout(10000)
```

**JavaScript Example**
```javascript
import { chromium } from "playwright";

const browser = await chromium.launch({
  headless: false,
  chromiumSandbox: true,
  env: {},
  args: ["--disable-extensions", "--disable-file-system"],
});
const page = await browser.newPage();
await page.setViewportSize({ width: 1024, height: 768 });
await page.goto("https://bing.com");

await page.waitForTimeout(10000);

browser.close();
```

### Advanced Setup: Docker Virtual Machine

For more advanced usage beyond browser automation, you can set up a local virtual machine using Docker. This approach provides a fully isolated environment with complete control over the system.

#### Prerequisites
- Install Docker from [Docker's official website](https://www.docker.com/get-started)
- Ensure Docker service is running on your machine

#### Docker Configuration

1. **Create a Dockerfile**

```dockerfile
FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

# 1) Install Xfce and required tools
RUN apt-get update && apt-get install -y \
    xfce4 \
    xfce4-goodies \
    x11vnc \
    xvfb \
    xdotool \
    imagemagick \
    x11-apps \
    sudo \
    software-properties-common \
    imagemagick \
    && apt-get remove -y light-locker xfce4-screensaver xfce4-power-manager || true \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 2) Install Firefox ESR
RUN add-apt-repository ppa:mozillateam/ppa \
    && apt-get update \
    && apt-get install -y --no-install-recommends firefox-esr \
    && update-alternatives --set x-www-browser /usr/bin/firefox-esr \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 3) Setup non-root user
RUN useradd -ms /bin/bash myuser \
    && echo "myuser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
USER myuser
WORKDIR /home/myuser

# 4) Configure VNC
RUN x11vnc -storepasswd secret /home/myuser/.vncpass

# 5) Setup entrypoint
EXPOSE 5900
CMD ["/bin/sh", "-c", "\
    Xvfb :99 -screen 0 1280x800x24 >/dev/null 2>&1 & \
    x11vnc -display :99 -forever -rfbauth /home/myuser/.vncpass -listen 0.0.0.0 -rfbport 5900 >/dev/null 2>&1 & \
    export DISPLAY=:99 && \
    startxfce4 >/dev/null 2>&1 & \
    sleep 2 && echo 'Container running!' && \
    tail -f /dev/null \
"]
```

2. **Build and Run**

```bash
# Build the Docker image
docker build -t cua-image .

# Run the container
docker run --rm -it --name cua-image -p 5900:5900 -e DISPLAY=:99 cua-image
```

#### Command Execution Helpers

**Python Implementation**
```python
import subprocess

def docker_exec(cmd: str, container_name: str, decode=True) -> str:
    safe_cmd = cmd.replace('"', '\"')
    docker_cmd = f'docker exec {container_name} sh -c "{safe_cmd}"'
    output = subprocess.check_output(docker_cmd, shell=True)
    if decode:
        return output.decode("utf-8", errors="ignore")
    return output

class VM:
    def __init__(self, display, container_name):
        self.display = display
        self.container_name = container_name

vm = VM(display=":99", container_name="cua-image")
```

**JavaScript Implementation**
```javascript
async function dockerExec(cmd, containerName, decode = true) {
  const safeCmd = cmd.replace(/"/g, '\"');
  const dockerCmd = `docker exec ${containerName} sh -c "${safeCmd}"`;
  const output = await execAsync(dockerCmd, {
    encoding: decode ? "utf8" : "buffer",
  });
  const result = output && output.stdout ? output.stdout : output;
  if (decode) {
    return result.toString("utf-8");
  }
  return result;
}

const vm = {
    display: ":99",
    containerName: "cua-image",
};
```

### Integrating the CUA Loop

To integrate the computer use agent (CUA) loop in your application, follow these high-level steps:

1. **Send a request to the model**
     - Include the computer use tool in the available tools, specifying display size and environment.
     - Optionally, include a screenshot of the initial state.

2. **Receive a response from the model**
     - Check if the response contains any `computer_call` items (actions like click, type, scroll, etc.).

3. **Execute the requested action**
     - Map the `computer_call` to the corresponding code in your environment (browser, VM, etc.).

4. **Capture the updated state**
     - Take a screenshot after executing the action.

5. **Repeat**
     - Send a new request with the updated state and repeat until the model stops requesting actions or you decide to stop.

#### Example: Sending a Request (Python)
```python
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
        model="computer-use-preview",
        tools=[{
                "type": "computer_use_preview",
                "display_width": 1024,
                "display_height": 768,
                "environment": "browser" # or "mac", "windows", "ubuntu"
        }],    
        input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": "Check the latest OpenAI news on bing.com."
                        }
                        # Optionally include a screenshot as input_image
                    ]
                }
        ],
        reasoning={
                "summary": "concise",
        },
        truncation="auto"
)

print(response.output)
```

#### Example: Sending a Request (JavaScript)
```javascript
import OpenAI from "openai";
const openai = new OpenAI();

const response = await openai.responses.create({
    model: "computer-use-preview",
    tools: [
        {
            type: "computer_use_preview",
            display_width: 1024,
            display_height: 768,
            environment: "browser", // or "mac", "windows", "ubuntu"
        },
    ],
    input: [
        {
            role: "user",
            content: [
                {
                    type: "input_text",
                    text: "Check the latest OpenAI news on bing.com.",
                },
                // Optionally include a screenshot as input_image
            ],
        },
    ],
    reasoning: {
        summary: "concise",
    },
    truncation: "auto",
});

console.log(JSON.stringify(response.output, null, 2));
```

#### Example: Handling Actions (Python, Playwright)
```python
def handle_model_action(page, action):
        """
        Given a computer action (e.g., click, scroll, type), execute it on the Playwright page.
        """
        action_type = action.type
        if action_type == "click":
                page.mouse.click(action.x, action.y, button=action.button)
        elif action_type == "scroll":
                page.mouse.move(action.x, action.y)
                page.evaluate(f"window.scrollBy({action.scroll_x}, {action.scroll_y})")
        elif action_type == "keypress":
                for k in action.keys:
                        page.keyboard.press(k)
        elif action_type == "type":
                page.keyboard.type(action.text)
        elif action_type == "wait":
                time.sleep(2)
        # Add more handlers as needed
```

#### Example: Handling Actions (Python, Docker VM)
```python
def handle_model_action(vm, action):
        action_type = action.type
        if action_type == "click":
                b = {"left": 1, "middle": 2, "right": 3}.get(action.button, 1)
                docker_exec(f"DISPLAY={vm.display} xdotool mousemove {action.x} {action.y} click {b}", vm.container_name)
        elif action_type == "scroll":
                docker_exec(f"DISPLAY={vm.display} xdotool mousemove {action.x} {action.y}", vm.container_name)
                # For vertical scrolling, use button 4 (up) or 5 (down)
                if action.scroll_y != 0:
                        button = 4 if action.scroll_y < 0 else 5
                        for _ in range(abs(action.scroll_y)):
                                docker_exec(f"DISPLAY={vm.display} xdotool click {button}", vm.container_name)
        elif action_type == "keypress":
                for k in action.keys:
                        docker_exec(f"DISPLAY={vm.display} xdotool key '{k}'", vm.container_name)
        elif action_type == "type":
                docker_exec(f"DISPLAY={vm.display} xdotool type '{action.text}'", vm.container_name)
        elif action_type == "wait":
                time.sleep(2)
        # Add more handlers as needed
```

#### Example: Capture Screenshot (Playwright)
```python
def get_screenshot(page):
        return page.screenshot()
```

#### Example: Capture Screenshot (Docker VM)
```python
def get_screenshot(vm):
        docker_exec(f"DISPLAY={vm.display} import -window root /tmp/screenshot.png", vm.container_name)
        # Copy screenshot from container to host as needed
```
### Use Cases

This automation can be used for various tasks such as:
- Booking flights
- Product searches
- Form filling
- Any task requiring UI interaction

### Security Note

When using this tool with APIs:
- Keep API keys secure and never commit them to version control
- Use environment variables or secure secret management
- Follow security best practices for credential handling

### Development

To work with the Generative Language API:
1. Set up proper authentication
2. Make API requests using your preferred method (curl, API client, etc.)
3. Handle the responses appropriately in your application

Remember to always follow security best practices and protect sensitive credentials.

## Limitations and Safety Considerations

### Current Limitations

The `computer-use-preview` model has several important limitations:

1. **Browser-Centric Performance**: 
   - Best suited for browser-based tasks
   - Less reliable in non-browser environments
   - Current OSWorld performance: 38.1%

2. **Rate Limits and Feature Support**:
   - Constrained rate limits
   - Limited feature support
   - Refer to model documentation for details

3. **Data Handling**:
   - Specific data retention policies apply
   - Data residency requirements
   - Follow data handling guidelines

### Safety Best Practices

#### 1. Human Oversight
- Maintain human supervision for high-stakes tasks
- Model may make hard-to-reverse mistakes
- Ensure human confirmation for important actions

#### 2. Prompt Injection Protection
- Guard against malicious instructions in screenshots
- Use sandboxed environments
- Limit access to trusted environments only

#### 3. Access Control
- Implement website blocklists/allowlists
- Control permitted actions
- Manage user access

#### 4. Safety Mechanisms
- Use safety identifiers in requests
- Implement provided safety checks:
  - Malicious instruction detection
  - Irrelevant domain detection
  - Sensitive domain detection
- Pass `current_url` parameter when possible

#### 5. Safety Check Handling
When receiving `pending_safety_checks`:
```json
{
    "pending_safety_checks": [
        {
            "id": "cu_sc_67cb...",
            "code": "malicious_instructions",
            "message": "..."
        }
    ]
}
```
- Increase oversight
- Get explicit user acknowledgment
- Enable active monitoring
- Pass acknowledgments in subsequent requests

### Compliance Requirements

1. Follow OpenAI's [Usage Policy](https://openai.com/policies/usage-policies/)
2. Adhere to [Business Terms](https://openai.com/policies/business-terms/)
3. Implement required safety features
4. Maintain appropriate monitoring and controls

For more detailed implementation examples and best practices, refer to the [CUA sample app repository](https://github.com/openai/openai-cua-sample-app).