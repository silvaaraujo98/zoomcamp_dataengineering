Markdown
## Question 1: Understanding Docker Images

**Task:** Run the `python:3.13` image with a bash entrypoint to identify the `pip` version.

**Options:**
- [x] <span style="color:green">**25.3**</span>
- [ ] 24.3.1
- [ ] 24.2.1
- [ ] 23.3.1

**Solution:**

1. Run the container in interactive mode:
   ```bash
   docker run -it --rm --entrypoint bash python:3.13-slim
2. Execute the version check command:
    ```
    pip --version

**Output:**
```text
pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)