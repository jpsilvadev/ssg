# SSG: Static Site Generator

A static site generator built with Python, designed to convert Markdown files into static HTML pages.

## Prerequisites
- **Ensure you have Python installed**
```bash
python3 --version
```

## Getting Started
1. Clone the repo:
```bash
$ git clone https://github.com/jpsilvadev/ssg.git
$ cd ssg
```

2. To generate the static site:
```bash
$ ./main.sh
```
> Note: You might need to `$ chmod +x main.sh`

3. Place your Markdown files in the `content/` directory.
   - If you just wish to test the generator, you can use the provided sample content in `content/` and static assets in `static/`.

4. Your static site will be available in the `public/` directory.
   - `main.sh` will start a local server listening on `localhost:8888` so you can preview your generated site.

5. **Customizing Your Site**
   - You can modify `template.html` and `static/index.css` to fit your needs and personalize the generated site.

## Acknowledgements
Implementation based on Boot.dev - [Build a Static Site Generator in Python](https://www.boot.dev/courses/build-static-site-generator-python)

## License
This project is licensed under the MIT License.
